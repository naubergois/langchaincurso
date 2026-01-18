import os
import glob
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# --- CONFIGURAÇÃO ---
script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env")) # Carrega do .env na mesma pasta do script

# Scopes necessários para ler e escrever no Drive
SCOPES = ['https://www.googleapis.com/auth/drive.file']
# Nome da pasta que será criada no seu Google Drive
TARGET_FOLDER_NAME = os.getenv("TARGET_FOLDER_NAME", "LangChain_Curso_Uploads")
CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

# Diretório local base (onde este script deve rodar ou ser apontado)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def authenticate_drive():
    """Autentica o usuário e retorna o serviço do Drive API."""
    creds = None
    # O arquivo token.json armazena os tokens de acesso e atualização do usuário
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"ERRO: Arquivo '{CREDENTIALS_FILE}' não encontrado.")
                print("1. Vá em https://console.cloud.google.com/")
                print("2. Crie um projeto e habilite a Google Drive API.")
                print("3. Crie credenciais (OAuth Client ID - Desktop App).")
                print(f"4. Salve como '{CREDENTIALS_FILE}' nesta pasta ou atualize o .env.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def create_or_get_folder(service, folder_name, parent_id=None):
    """Cria uma pasta no Drive se não existir, ou retorna o ID se existir."""
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        # Criar pasta
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
        
        folder = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Pasta criada: {folder_name} (ID: {folder['id']})")
        return folder['id']
    else:
        print(f"Pasta encontrada: {folder_name} (ID: {items[0]['id']})")
        return items[0]['id']

def make_file_public(service, file_id):
    """Torna o arquivo público (leitura para qualquer um com o link)."""
    try:
        permission = {
            'role': 'reader',
            'type': 'anyone'
        }
        service.permissions().create(fileId=file_id, body=permission).execute()
        return True
    except Exception as e:
        print(f"Erro ao mudar permissões: {e}")
        return False

def upload_file(service, file_path, folder_id):
    """Faz upload e retorna o ID do arquivo."""
    file_name = os.path.basename(file_path)
    
    # Verificar se arquivo já existe
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    results = service.files().list(q=query, fields="files(id)").execute()
    items = results.get('files', [])

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    mimetype = 'application/json' if file_path.endswith('.ipynb') else 'application/octet-stream'
    media = MediaFileUpload(file_path, mimetype=mimetype, resumable=True)

    if items:
        file_id = items[0]['id']
        service.files().update(fileId=file_id, media_body=media).execute()
        print(f"Atualizado: {file_name}")
    else:
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        file_id = file.get('id')
        print(f"Upload: {file_name}")
        
    return file_id

def main():
    service = authenticate_drive()
    if not service:
        return

    print("--- Iniciando Upload para o Google Drive ---")
    
    root_folder_id = create_or_get_folder(service, TARGET_FOLDER_NAME)
    
    notebooks = glob.glob(os.path.join(BASE_DIR, "**", "*.ipynb"), recursive=True)
    notebooks = [n for n in notebooks if ".venv" not in n and ".git" not in n and "ipynb_checkpoints" not in n]

    print(f"Encontrados {len(notebooks)} notebooks para upload.")

    links_summary = []

    for notebook_path in notebooks:
        relative_path = os.path.relpath(notebook_path, BASE_DIR)
        directory = os.path.dirname(relative_path)
        
        if directory and directory != ".":
            target_id = create_or_get_folder(service, directory, parent_id=root_folder_id)
        else:
            target_id = root_folder_id
            
        try:
            file_id = upload_file(service, notebook_path, target_id)
            
            # Torna Público
            make_file_public(service, file_id)
            
            # Gera Link do Colab
            # Formato: https://colab.research.google.com/drive/<ID>
            colab_link = f"https://colab.research.google.com/drive/{file_id}"
            
            links_summary.append(f"- [{relative_path}]({colab_link})")
            
        except Exception as e:
            print(f"Falha em {relative_path}: {e}")

    # Salva o índice de links
    with open(os.path.join(BASE_DIR, "colab_links.md"), "w") as f:
        f.write("# Links para o Google Colab 🚀\\n\\n")
        f.write("\\n".join(links_summary))
        
    print("\n--- Concluído! ---")
    print(f"Arquivo 'colab_links.md' gerado com {len(links_summary)} links.")

if __name__ == '__main__':
    main()

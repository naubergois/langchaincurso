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
    token_path = os.path.join(script_dir, 'token.json')
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Se o arquivo de credenciais for relativo, tenta achar no scripts/
            if not os.path.isabs(CREDENTIALS_FILE):
                credentials_path = os.path.join(script_dir, os.path.basename(CREDENTIALS_FILE))
            else:
                credentials_path = CREDENTIALS_FILE

            if not os.path.exists(credentials_path):
                print(f"ERRO: Arquivo '{credentials_path}' não encontrado.")
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(token_path, 'w') as token:
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

def get_folder_link(service, folder_id):
    """Retorna o link de visualização da pasta."""
    folder = service.files().get(fileId=folder_id, fields='webViewLink').execute()
    return folder.get('webViewLink')

def main():
    service = authenticate_drive()
    if not service:
        return

    print("--- Iniciando Upload para o Google Drive ---")
    
    root_folder_id = create_or_get_folder(service, TARGET_FOLDER_NAME)
    
    # Procurar por .ipynb e .py
    patterns = ["*.ipynb", "*.py"]
    files_to_upload = []
    for pattern in patterns:
        files_to_upload.extend(glob.glob(os.path.join(BASE_DIR, pattern)))

    # Filtrar arquivos indesejados
    files_to_upload = [
        f for f in files_to_upload 
        if "checkpoint" not in f
        and "test_notebook" not in f
    ]

    print(f"Encontrados {len(files_to_upload)} arquivos para upload.")

    links_summary = []

    for file_path in sorted(files_to_upload):
        relative_path = os.path.basename(file_path)
        
        try:
            file_id = upload_file(service, file_path, root_folder_id)
            
            # Torna Público
            make_file_public(service, file_id)
            
            # Gera Link dependendo do tipo
            if file_path.endswith('.ipynb'):
                link = f"https://colab.research.google.com/drive/{file_id}"
            else:
                f_info = service.files().get(fileId=file_id, fields='webViewLink').execute()
                link = f_info.get('webViewLink')
            
            links_summary.append(f"- [{relative_path}]({link})")
            
        except Exception as e:
            print(f"Falha em {relative_path}: {e}")

    # Faz a pasta raiz pública
    make_file_public(service, root_folder_id)
    folder_link = get_folder_link(service, root_folder_id)

    # Salva o índice de links
    with open(os.path.join(BASE_DIR, "links_drive.md"), "w") as f:
        f.write(f"# Links para o Google Drive 🚀\n\n")
        f.write(f"📂 **Pasta completa:** [Clique aqui para acessar]({folder_link})\n\n")
        f.write("## Arquivos Individuais\n\n")
        f.write("\n".join(links_summary))
        
    print("\n--- Concluído! ---")
    print(f"Pasta no Drive: {folder_link}")
    print(f"Arquivo 'links_drive.md' gerado com {len(links_summary)} links.")

if __name__ == '__main__':
    main()

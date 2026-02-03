import nbformat
import os

def fix_notebook_26():
    nb_path = "26_ReAct_Fundamentos_Prompting.ipynb"
    if not os.path.exists(nb_path):
        print(f"Notebook {nb_path} not found.")
        return

    print(f"Fixing {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    modified = False
    for cell in nb.cells:
        if cell.cell_type == 'code':
            if 'tool_descriptions = """\\n".join' in cell.source:
                print("Found syntax error in cell. Fixing...")
                cell.source = cell.source.replace('tool_descriptions = """\\n".join', 'tool_descriptions = "\\n".join')
                modified = True

    if modified:
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Simultaneously fixed {nb_path}.")
    else:
        print(f"No changes made to {nb_path} (pattern not found).")

def fix_notebook_06():
    nb_path = "06_RAG_Embeddings_VectorStores.ipynb"
    if not os.path.exists(nb_path):
        print(f"Notebook {nb_path} not found.")
        return

    print(f"Fixing {nb_path}...")
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    modified = False
    
    # Robust env loading code
    env_code = (
        "# Configuração da chave de API do Google Generative AI\\n"
        "import os\\n"
        "from dotenv import load_dotenv\\n"
        "import sys\\n"
        "# Carrega .env do local ou de pastas comuns\\n"
        "for p in ['.', '..', 'scripts', '../scripts']:\\n"
        "    path = os.path.join(p, '.env')\\n"
        "    if os.path.exists(path):\\n"
        "        load_dotenv(path)\\n"
        "        break\\n"
        "if os.getenv('GOOGLE_API_KEY'):\\n"
        "    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')\n"
    )

    for cell in nb.cells:
        if cell.cell_type == 'code':
            # Look for the cell setting the API key
            if 'os.environ["GOOGLE_API_KEY"] = "SUA_CHAVE_API"' in cell.source or "os.environ['GOOGLE_API_KEY'] = \"SUA_CHAVE_API\"" in cell.source:
                print("Found API key cell. Replacing with robust dotenv loading...")
                cell.source = env_code
                modified = True
            # Also catch the other variant just in case
            elif 'SUA_CHAVE_API' in cell.source and 'os.environ' in cell.source:
                 print("Found generic API key cell. Replacing...")
                 cell.source = env_code
                 modified = True

    if modified:
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Simultaneously fixed {nb_path}.")
    else:
        print(f"No changes made to {nb_path} (pattern not found).")

if __name__ == "__main__":
    fix_notebook_26()
    fix_notebook_06()

import os
import glob
import nbformat
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load key from scripts/.env
env_path = os.path.join("scripts", ".env")
load_dotenv(env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def generate_explanation(notebook_name, content_preview):
    """
    Uses Gemini to generate a detailed explanation of the notebook subject.
    """
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_template(
        """Você é um especialista técnico em LangChain e IA Generativa.
        Com base no nome do notebook e no conteúdo parcial abaixo, escreva uma seção Markdown detalhada 
        em PORTUGUÊS que será inserida no início do notebook.
        
        NOME DO NOTEBOOK: {name}
        CONTEÚDO PARCIAL:
        {preview}
        
        A explicação deve seguir esta estrutura:
        1. **Resumo Executivo**: O que este notebook aborda.
        2. **Conceitos Chave**: Explique os termos técnicos principais (ex: Chains, RAG, Memória).
        3. **Objetivos de Aprendizado**: O que o aluno será capaz de fazer após este notebook.
        4. **Importância no Ecossistema LangChain**: Por que este tópico é fundamental.

        Use um tom profissional, didático e motivador.
        Retorne APENAS o conteúdo em Markdown, sem blocos de código ```markdown no início ou fim.
        """
    )
    
    chain = prompt | llm
    response = chain.invoke({"name": notebook_name, "preview": content_preview})
    return response.content

def process_notebook(nb_path):
    print(f"\n--- Gerando Explicação para: {nb_path} ---")
    
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        # Check if already documented
        for cell in nb.cells:
            if cell.cell_type == 'markdown' and "Explicação Detalhada do Assunto" in cell.source:
                print("  [!] Notebook já possui explicação detalhada. Pulando.")
                return True

        # Get context preview (first 10 cells or so)
        preview_text = ""
        for cell in nb.cells[:12]:
            if cell.cell_type == 'markdown':
                preview_text += f"\nMarkdown: {cell.source[:200]}..."
            elif cell.cell_type == 'code':
                preview_text += f"\nCode: {cell.source[:200]}..."
        
        # Generate via LLM
        print("  [*] Chamando Gemini para gerar explicação...")
        explanation = generate_explanation(os.path.basename(nb_path), preview_text)
        
        header = f"# Explicação Detalhada do Assunto\n\n{explanation}\n\n---\n"
        
        # Create new markdown cell
        new_cell = nbformat.v4.new_markdown_cell(header)
        
        # Insert at index 1 (usually index 0 is the main title)
        # If index 0 is already our injection (from previous tasks), we skip or replace
        nb.cells.insert(1, new_cell)
        
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        
        print(f"  [+] Explicação injetada com sucesso.")
        return True
        
    except Exception as e:
        print(f"  [!] Erro ao processar: {e}")
        return False

def main():
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not found. Check scripts/.env.")
        return

    notebooks = sorted([f for f in glob.glob("*.ipynb") if "checkpoint" not in f and "test_notebook" not in f])
    print(f"Iniciando documentação de {len(notebooks)} notebooks...")
    
    for nb in notebooks:
        process_notebook(nb)
    
    print("\nProcesso concluído!")

if __name__ == "__main__":
    main()

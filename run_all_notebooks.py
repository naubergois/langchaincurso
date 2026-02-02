import os
import glob
import nbformat
import re
from nbconvert import PythonExporter
from nbconvert.preprocessors import ExecutePreprocessor, ClearOutputPreprocessor
from dotenv import load_dotenv

# Load key from scripts/.env
env_path = os.path.join("scripts", ".env")
load_dotenv(env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def patch_cell_source(source):
    """
    Very robust patching for OpenAI -> Gemini conversion and local .env usage.
    """
    # 1. Robust Import Replacements
    source = re.sub(r'from\s+langchain_openai\s+import\s+', 'from langchain_google_genai import ', source)
    source = source.replace("ChatOpenAI", "ChatGoogleGenerativeAI")
    source = source.replace("OpenAIEmbeddings", "GoogleGenerativeAIEmbeddings")
    source = source.replace("OpenAI", "GoogleGenerativeAI") # Catch all
    
    # 2. Model Mapping & Repair
    source = source.replace("gpt-3.5-turbo", "gemini-2.0-flash")
    source = source.replace("gpt-4", "gemini-2.0-flash")
    source = source.replace("gemini-1.5-flash", "gemini-2.0-flash")
    source = source.replace("gemini-1.5-pro", "gemini-2.0-flash")
    
    # 3. Handle Key Variables
    source = source.replace('OPENAI_API_KEY', 'GOOGLE_API_KEY')
    
    # 4. Patch blocking calls safely to avoid IndentationErrors
    # Instead of commenting out, we replace the call with None or a dummy string
    # but still keep the assignment structure if possible.
    # However, replacing with 'os.getenv("GOOGLE_API_KEY")' is even better!
    
    source = re.sub(r'getpass\.getpass\(.*?\)', 'os.getenv("GOOGLE_API_KEY")', source)
    source = re.sub(r'userdata\.get\(.*?\)', 'os.getenv("GOOGLE_API_KEY")', source)
    source = re.sub(r'input\(.*?\)', 'os.getenv("GOOGLE_API_KEY")', source)
    
    # 5. Patch pip installs
    source = re.sub(r'^!pip install.*', '# \\g<0> # Script-patched', source, flags=re.MULTILINE)
    
    # 6. Final Indentation Check (The "Pass" Injection)
    lines = source.splitlines()
    final_lines = []
    for i, line in enumerate(lines):
        final_lines.append(line)
        stripped = line.strip()
        if stripped.endswith(":") and i + 1 < len(lines):
            next_stripped = lines[i+1].strip()
            # If next line is a comment or empty, we MUST add a pass
            if not next_stripped or next_stripped.startswith("#"):
                indent_match = re.match(r'^(\s*)', line)
                indent = indent_match.group(1) if indent_match else ""
                final_lines.append(f"{indent}    pass # Script-patched: ensure non-empty block")
                
    return "\n".join(final_lines)

def process_notebook(nb_path):
    print(f"\n--- Processing: {nb_path} ---")
    base_name = os.path.splitext(nb_path)[0]
    py_path = f"{base_name}.py"
    
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        
        has_injection = any("### INJECTION START ###" in (cell.source or "") for cell in nb.cells)
        
        inject_code = (
            "### INJECTION START ###\n"
            "import os\n"
            "from dotenv import load_dotenv\n"
            "import sys\n"
            "for p in ['.', '..', 'scripts', '../scripts']:\n"
            "    path = os.path.join(p, '.env')\n"
            "    if os.path.exists(path):\n"
            "        load_dotenv(path)\n"
            "        break\n"
            "if os.getenv('GOOGLE_API_KEY'):\n"
            "    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')\n"
            "    os.environ['OPENAI_API_KEY'] = os.getenv('GOOGLE_API_KEY')\n"
            "### INJECTION END ###\n"
        )
        
        dotenv_injected = False
        for cell in nb.cells:
            if cell.cell_type == 'code':
                cell.source = patch_cell_source(cell.source)
                if not has_injection and not dotenv_injected:
                    cell.source = inject_code + "\n" + cell.source
                    dotenv_injected = True
        
        # Python export
        exporter = PythonExporter()
        source_python, _ = exporter.from_notebook_node(nb)
        source_python = "\n".join([l for l in source_python.splitlines() if not l.strip().startswith("# In[")])

        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(source_python)
        
        # Execution
        co = ClearOutputPreprocessor()
        nb, _ = co.preprocess(nb, {})
        print(f"  [*] Executing notebook...")
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3', allow_errors=True)
        ep.preprocess(nb, {'metadata': {'path': './'}})
        
        # Error check
        execution_errors = []
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                for output in cell.get('outputs', []):
                    if output.output_type == 'error':
                        execution_errors.append(f"Cell {i}: {output.ename}: {output.evalue}")
        
        if execution_errors:
            print(f"  [!] Found {len(execution_errors)} execution errors.")
            for err in execution_errors[:2]: print(f"      - {err}")
        else:
            print(f"  [+] Notebook executed successfully.")

        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"  [+] Notebook saved with outputs.")
        
        return not bool(execution_errors)
        
    except Exception as e:
        print(f"  [!] Fatal error: {e}")
        return False

def main():
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "sua_chave_aqui":
        print("ERROR: GOOGLE_API_KEY not found. Update scripts/.env.")
        return

    notebooks = sorted([f for f in glob.glob("*.ipynb") if "checkpoint" not in f and "test_notebook" not in f])
    print(f"Found {len(notebooks)} notebooks. Starting automation...")
    
    results = {}
    for nb in notebooks:
        success = process_notebook(nb)
        results[nb] = success

    print("\n" + "="*80)
    print(f"{'NOTEBOOK':60} | {'STATUS':10}")
    print("-" * 80)
    for nb, success in results.items():
        print(f"{nb:60} | {'PASSED' if success else 'FAILED'}")
    print("="*80)

if __name__ == "__main__":
    main()

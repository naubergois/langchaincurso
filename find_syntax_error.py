import nbformat
import ast

nb_path = "26_ReAct_Fundamentos_Prompting.ipynb"

try:
    with open(nb_path, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            source = cell.source
            # Filter magic commands if any, though verify_notebooks already considers them
            clean_lines = []
            for line in source.splitlines():
                if line.strip().startswith('!') or line.strip().startswith('%'):
                    clean_lines.append(f"# {line}") # Comment out magic
                else:
                    clean_lines.append(line)
            clean_source = "\n".join(clean_lines)

            if not clean_source.strip():
                continue

            try:
                ast.parse(clean_source)
            except SyntaxError as e:
                print(f"Syntax Error in Cell {i}:")
                print(f"Line {e.lineno}: {e.text}")
                print("-" * 20)
                print(source)
                break
except Exception as e:
    print(f"Error reading notebook: {e}")

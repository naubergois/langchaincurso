
import os
import re

def update_readme():
    readme_path = 'README.md'
    
    # 1. Read existing README to map filenames to Colab links
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    colab_links = {}
    # Regex to find table rows: | Name | Link |
    # Matches: | 01. Intro... | [🚀...](https://...) |
    # We want to extract the number/name to identify the likely file, but better yet, let's look for the Colab link.
    # Actually, the file structure helps. Let's try to map "XX_Name.ipynb" to the link if possible.
    # The current README links don't explicitly show the filename in the link text, usually.
    # But we can assume the table row order or content.
    
    # Strategy: Parse the table, get "Notebook Name" and "Link Colab".
    # Since we can't easily map "01. Introdução" to "01_Introducao...ipynb" perfectly without heuristics,
    # let's try a different approach:
    # We will list all files. for each file, we check if there's a matching entry in the old README based on the prefix number.
    
    # Extract existing links based on numeric prefix
    # Pattern: | XX. Name | [Link](URL) |
    table_lines = [line for line in content.split('\n') if line.strip().startswith('|') and 'Link Colab' not in line and '---' not in line and 'Pasta Completa' not in line]
    
    prefix_map = {}
    for line in table_lines:
        parts = line.split('|')
        if len(parts) < 3: continue
        name_cell = parts[1].strip()
        link_cell = parts[2].strip()
        
        # Extract number
        match = re.match(r'(\d+)\.', name_cell)
        if match:
            num = match.group(1)
            # Store the Colab link part: [🚀 Abrir no Colab](...)
            # Only if it's a colab link
            if "colab.research.google.com" in link_cell:
                prefix_map[int(num)] = link_cell
    
    # 2. List all notebooks
    notebooks = sorted([f for f in os.listdir('.') if f.endswith('.ipynb') and not f.startswith('gerador_')])
    
    new_table_rows = []
    
    for note in notebooks:
        # Extract number if present
        match = re.match(r'(\d+)_', note)
        display_name = note.replace('.ipynb', '').replace('_', ' ')
        
        link_str = f"[📂 Arquivo Local]({note})"
        
        if match:
            num = int(match.group(1))
            display_name = f"{num:02d}. {display_name.split(' ', 1)[1] if ' ' in display_name else display_name}"
            
            # If we have a colab link for this number, use it.
            # Warning: Duplicates (20, 26) might get the same link if we only use number.
            # But the old README only had one 20 and two 26s? No, old README had one 20.
            # Let's simple check if we have a mapped link.
            if num in prefix_map:
                # Special case for duplicates:
                # If we have multiple files with same number, we might need manual care.
                # Since we want to be safe, if there's a collision in numbers in the file system,
                # we only apply the link to the one that likely matches the old name? 
                # For now, let's keep it simple: Use Colab link if available, else Local.
                
                # Check if this specific file matches the old title? Hard.
                # Let's just use the Colab link if the number matches, unless we've used it?
                # Actually, let's prefer Local link for the NEW file (20_Auditoria_Compras).
                if note == "20_Auditoria_Compras_Anomalias.ipynb":
                     link_str = f"[📂 Arquivo Local]({note})"
                else:
                    link_str = prefix_map[num]
        
        new_table_rows.append(f"| {display_name} | {link_str} |")
        
    # 3. Reconstruct content
    # Find start and end of table
    lines = content.split('\n')
    start_idx = -1
    end_idx = -1
    
    for i, line in enumerate(lines):
        if "| Nome do Notebook | Link Colab |" in line:
            start_idx = i
        if start_idx != -1 and i > start_idx and not line.strip().startswith('|'):
            end_idx = i
            break
            
    if start_idx != -1:
        # Header + Separator
        header = lines[start_idx:start_idx+2]
        # Pre-table
        pre = lines[:start_idx]
        # Folder link row (special case, usually first row after separator)
        folder_row = "| **Pasta Completa no Drive** | [📂 Acessar Pasta](https://drive.google.com/drive/folders/1JFrfjXwoP0bIpXttuzx_OUUC2u0yOl_h) |"
        
        # Post-table
        post = lines[end_idx:] if end_idx != -1 else []
        
        new_content = "\n".join(pre + header + [folder_row] + new_table_rows + post)
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("README.md updated successfully.")
    else:
        print("Could not find table in README.md")

if __name__ == "__main__":
    update_readme()

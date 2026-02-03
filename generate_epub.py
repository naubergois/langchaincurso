import os
import glob
import nbformat
import markdown
from ebooklib import epub

def create_epub(output_filename="LangChain_Course.epub"):
    book = epub.EpubBook()

    # Metadata
    book.set_identifier('id123456')
    book.set_title('LangChain Course Notebooks')
    book.set_language('pt-br')
    book.add_author('Francisco Nauber Bernardo Gois')

    # Styles
    style = '''
        @namespace epub "http://www.idpf.org/2007/ops";
        body { font-family: Cambria, Liberation Serif, Bitstream Charter, Georgia, serif; }
        h1 { text-align: left; }
        pre { background-color: #f4f4f4; padding: 10px; border: 1px solid #ddd; white-space: pre-wrap; font-family: monospace}
        code { font-family: monospace; color: #d63384; }
    '''
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # Chapters
    chapters = []
    notebooks = sorted(glob.glob("*.ipynb"))
    
    # Filter only numbered notebooks generally
    notebooks = [nb for nb in notebooks if nb[0].isdigit()]

    for i, nb_path in enumerate(notebooks):
        print(f"Processing {nb_path}...")
        try:
            with open(nb_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
        except Exception as e:
            print(f"Skipping {nb_path}: {e}")
            continue

        chapter_title = os.path.basename(nb_path).replace('.ipynb', '').replace('_', ' ')
        c = epub.EpubHtml(title=chapter_title, file_name=f'chap_{i}.xhtml', lang='pt-br')
        c.add_item(nav_css)

        content = f"<h1>{chapter_title}</h1>"
        
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                html = markdown.markdown(cell.source)
                content += f"<div>{html}</div>"
            elif cell.cell_type == 'code':
                code_source = cell.source
                if code_source.strip():
                    content += f"<pre><code>{code_source}</code></pre>"
                    # Optionally add outputs? For now, code only.
        
        c.content = content
        book.add_item(c)
        chapters.append(c)

    # Navigation and TOC
    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    book.spine = ['nav'] + chapters

    print(f"Writing {output_filename}...")
    epub.write_epub(output_filename, book, {})
    print("Done.")

if __name__ == "__main__":
    create_epub()

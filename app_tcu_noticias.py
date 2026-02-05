"""
Aplicação principal para extração e análise de notícias do TCU.
Gera relatórios executivos usando LangChain e Pydantic.
"""
import argparse
import json
import os
from datetime import datetime
from dotenv import load_dotenv

from tcu_scraper import TCUScraper
from tcu_analyzer import TCUAnalyzer
from tcu_models import RelatorioExecutivo

# Carregar variáveis de ambiente
load_dotenv()


def salvar_json(dados, arquivo: str):
    """Salva dados em arquivo JSON."""
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2, default=str)
    print(f"💾 Dados salvos em: {arquivo}")


def gerar_relatorio_markdown(relatorio: RelatorioExecutivo, arquivo: str):
    """Gera relatório executivo em formato Markdown."""
    
    md = f"""# Relatório Executivo - Notícias TCU

**Período:** {relatorio.periodo}  
**Total de Notícias:** {relatorio.total_noticias}  
**Data de Geração:** {relatorio.data_geracao}

---

## 📊 Estatísticas

### Distribuição por Categoria
"""
    
    for categoria, count in sorted(relatorio.distribuicao_categorias.items(), key=lambda x: x[1], reverse=True):
        md += f"- **{categoria}**: {count} notícia(s)\n"
    
    md += "\n### Distribuição por Relevância\n"
    for relevancia, count in sorted(relatorio.distribuicao_relevancia.items(), key=lambda x: x[1], reverse=True):
        emoji = "🔴" if relevancia == "Alta" else "🟡" if relevancia == "Média" else "🟢"
        md += f"- {emoji} **{relevancia}**: {count} notícia(s)\n"
    
    md += f"\n---\n\n## 🎯 Principais Temas\n\n"
    for i, tema in enumerate(relatorio.principais_temas, 1):
        md += f"{i}. {tema}\n"
    
    if relatorio.principais_entidades:
        md += f"\n## 🏢 Entidades Mais Mencionadas\n\n"
        for i, entidade in enumerate(relatorio.principais_entidades, 1):
            md += f"{i}. {entidade}\n"
    
    if relatorio.noticias_alta_relevancia:
        md += f"\n---\n\n## 🔴 Notícias de Alta Relevância\n\n"
        for i, noticia in enumerate(relatorio.noticias_alta_relevancia, 1):
            md += f"### {i}. {noticia['titulo']}\n\n"
            md += f"**Categoria:** {noticia['categoria']}  \n"
            md += f"**Resumo:** {noticia['resumo']}  \n"
            md += f"**Link:** [{noticia['url']}]({noticia['url']})\n\n"
    
    md += f"\n---\n\n## 💡 Insights Principais\n\n"
    for i, insight in enumerate(relatorio.insights_principais, 1):
        md += f"{i}. {insight}\n"
    
    md += f"\n---\n\n## 📝 Resumo Geral\n\n{relatorio.resumo_geral}\n"
    
    md += f"\n---\n\n*Relatório gerado automaticamente usando LangChain e Google Gemini*\n"
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.write(md)
    
    print(f"📄 Relatório salvo em: {arquivo}")


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description="Extrai notícias do portal TCU e gera relatório executivo"
    )
    parser.add_argument(
        '-q', '--quantidade',
        type=int,
        default=5,
        help='Quantidade de notícias a extrair (padrão: 5)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='relatorio_tcu',
        help='Nome base dos arquivos de saída (padrão: relatorio_tcu)'
    )
    parser.add_argument(
        '--no-analise',
        action='store_true',
        help='Apenas extrair notícias sem análise por IA'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("🏛️  SISTEMA DE ANÁLISE DE NOTÍCIAS DO TCU")
    print("=" * 70)
    print()
    
    # Verificar API Key
    if not os.getenv("GOOGLE_API_KEY") and not args.no_analise:
        print("❌ GOOGLE_API_KEY não configurada!")
        print("Configure a variável de ambiente ou use --no-analise")
        return
    
    # 1. Extrair notícias
    scraper = TCUScraper(delay=1.0)
    noticias = scraper.extrair_noticias_completas(quantidade=args.quantidade)
    
    if not noticias:
        print("❌ Nenhuma notícia foi extraída. Verifique a conexão ou o site.")
        return
    
    # Salvar notícias em JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    arquivo_noticias = f"{args.output}_noticias_{timestamp}.json"
    
    noticias_dict = [n.dict() for n in noticias]
    salvar_json(noticias_dict, arquivo_noticias)
    
    if args.no_analise:
        print("\n✅ Extração concluída! (análise desabilitada)")
        return
    
    # 2. Analisar notícias com IA
    analyzer = TCUAnalyzer()
    noticias_analisadas = analyzer.analisar_noticias(noticias)
    
    if not noticias_analisadas:
        print("❌ Nenhuma notícia foi analisada.")
        return
    
    # Salvar análises em JSON
    arquivo_analises = f"{args.output}_analises_{timestamp}.json"
    analises_dict = [n.dict() for n in noticias_analisadas]
    salvar_json(analises_dict, arquivo_analises)
    
    # 3. Gerar relatório executivo
    relatorio = analyzer.gerar_relatorio_executivo(noticias_analisadas)
    
    # Salvar relatório em JSON
    arquivo_relatorio_json = f"{args.output}_relatorio_{timestamp}.json"
    salvar_json(relatorio.dict(), arquivo_relatorio_json)
    
    # Salvar relatório em Markdown
    arquivo_relatorio_md = f"{args.output}_relatorio_{timestamp}.md"
    gerar_relatorio_markdown(relatorio, arquivo_relatorio_md)
    
    print("\n" + "=" * 70)
    print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
    print("=" * 70)
    print(f"\n📁 Arquivos gerados:")
    print(f"  - {arquivo_noticias}")
    print(f"  - {arquivo_analises}")
    print(f"  - {arquivo_relatorio_json}")
    print(f"  - {arquivo_relatorio_md}")
    print()
    print(f"📊 Resumo:")
    print(f"  - {relatorio.total_noticias} notícias analisadas")
    print(f"  - {len(relatorio.noticias_alta_relevancia)} de alta relevância")
    print(f"  - {len(relatorio.principais_temas)} temas principais identificados")
    print()


if __name__ == "__main__":
    main()

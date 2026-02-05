"""
Aplicação Streamlit para visualização de Relatórios Executivos do TCU.
Interface web para extração e análise de notícias do portal TCU.
"""
import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

from tcu_scraper import TCUScraper
from tcu_analyzer import TCUAnalyzer
from tcu_models import RelatorioExecutivo

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Relatórios TCU",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .news-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    .high-relevance {
        border-left-color: #dc3545;
        background-color: #fff5f5;
    }
    .medium-relevance {
        border-left-color: #ffc107;
        background-color: #fffbf0;
    }
    .low-relevance {
        border-left-color: #28a745;
        background-color: #f0fff4;
    }
    .insight-box {
        background-color: #e7f3ff;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #0066cc;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def carregar_relatorios_salvos():
    """Carrega relatórios salvos em disco."""
    relatorios = []
    for arquivo in Path(".").glob("*_relatorio_*.json"):
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                relatorios.append({
                    'arquivo': arquivo.name,
                    'dados': dados,
                    'timestamp': arquivo.stat().st_mtime
                })
        except:
            continue
    
    # Ordenar por timestamp (mais recente primeiro)
    relatorios.sort(key=lambda x: x['timestamp'], reverse=True)
    return relatorios


def exibir_metricas_principais(relatorio):
    """Exibe métricas principais do relatório."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "📰 Total de Notícias",
            relatorio['total_noticias']
        )
    
    with col2:
        alta = relatorio['distribuicao_relevancia'].get('Alta', 0)
        st.metric(
            "🔴 Alta Relevância",
            alta
        )
    
    with col3:
        temas = len(relatorio['principais_temas'])
        st.metric(
            "🎯 Temas Principais",
            temas
        )
    
    with col4:
        categorias = len(relatorio['distribuicao_categorias'])
        st.metric(
            "📊 Categorias",
            categorias
        )


def exibir_graficos(relatorio):
    """Exibe gráficos de visualização."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Distribuição por Categoria")
        if relatorio['distribuicao_categorias']:
            fig_cat = go.Figure(data=[go.Pie(
                labels=list(relatorio['distribuicao_categorias'].keys()),
                values=list(relatorio['distribuicao_categorias'].values()),
                hole=0.3,
                marker=dict(colors=px.colors.qualitative.Set3)
            )])
            fig_cat.update_layout(height=350, showlegend=True)
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Sem dados de categorias")
    
    with col2:
        st.markdown("### 🎯 Distribuição por Relevância")
        if relatorio['distribuicao_relevancia']:
            cores = {
                'Alta': '#dc3545',
                'Média': '#ffc107',
                'Baixa': '#28a745'
            }
            
            labels = list(relatorio['distribuicao_relevancia'].keys())
            values = list(relatorio['distribuicao_relevancia'].values())
            colors = [cores.get(label, '#667eea') for label in labels]
            
            fig_rel = go.Figure(data=[go.Bar(
                x=labels,
                y=values,
                marker=dict(color=colors),
                text=values,
                textposition='auto'
            )])
            fig_rel.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Nível de Relevância",
                yaxis_title="Quantidade"
            )
            st.plotly_chart(fig_rel, use_container_width=True)
        else:
            st.info("Sem dados de relevância")


def exibir_noticias_destaque(relatorio):
    """Exibe notícias de alta relevância."""
    st.markdown("### 🔴 Notícias de Alta Relevância")
    
    noticias = relatorio.get('noticias_alta_relevancia', [])
    
    if not noticias:
        st.info("Nenhuma notícia de alta relevância neste período")
        return
    
    for i, noticia in enumerate(noticias, 1):
        st.markdown(f"""
        <div class="news-card high-relevance">
            <h4>{i}. {noticia['titulo']}</h4>
            <p><strong>Categoria:</strong> {noticia['categoria']}</p>
            <p>{noticia['resumo']}</p>
            <p><a href="{noticia['url']}" target="_blank">🔗 Ler notícia completa</a></p>
        </div>
        """, unsafe_allow_html=True)


def exibir_insights(relatorio):
    """Exibe insights principais."""
    st.markdown("### 💡 Insights Principais")
    
    insights = relatorio.get('insights_principais', [])
    
    if not insights:
        st.info("Nenhum insight disponível")
        return
    
    for insight in insights:
        # Limpar numeração se existir
        insight_limpo = insight.strip()
        if insight_limpo and insight_limpo[0].isdigit():
            # Remover "1. ", "2. ", etc.
            parts = insight_limpo.split('.', 1)
            if len(parts) > 1:
                insight_limpo = parts[1].strip()
        
        st.markdown(f"""
        <div class="insight-box">
            💡 {insight_limpo}
        </div>
        """, unsafe_allow_html=True)


def exibir_temas_entidades(relatorio):
    """Exibe principais temas e entidades."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Principais Temas")
        temas = relatorio.get('principais_temas', [])
        if temas:
            for i, tema in enumerate(temas[:10], 1):
                st.markdown(f"{i}. **{tema}**")
        else:
            st.info("Nenhum tema identificado")
    
    with col2:
        st.markdown("### 🏢 Entidades Mencionadas")
        entidades = relatorio.get('principais_entidades', [])
        if entidades:
            for i, entidade in enumerate(entidades[:10], 1):
                st.markdown(f"{i}. **{entidade}**")
        else:
            st.info("Nenhuma entidade identificada")


def pagina_visualizar():
    """Página de visualização de relatórios salvos."""
    st.title("🏛️ Relatórios Executivos - TCU")
    st.markdown("### Visualização de Relatórios Salvos")
    
    relatorios = carregar_relatorios_salvos()
    
    if not relatorios:
        st.warning("⚠️ Nenhum relatório encontrado. Gere um relatório primeiro na aba 'Gerar Novo'.")
        return
    
    # Seletor de relatório
    opcoes = [
        f"{r['dados'].get('periodo', 'Sem período')} - {datetime.fromtimestamp(r['timestamp']).strftime('%d/%m/%Y %H:%M')}"
        for r in relatorios
    ]
    
    selecionado = st.selectbox("Selecione um relatório:", opcoes)
    idx = opcoes.index(selecionado)
    relatorio = relatorios[idx]['dados']
    
    # Informações do relatório
    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Período:** {relatorio.get('periodo', 'N/A')}")
    with col2:
        st.markdown(f"**Gerado em:** {relatorio.get('data_geracao', 'N/A')}")
    
    st.markdown("---")
    
    # Métricas principais
    exibir_metricas_principais(relatorio)
    
    st.markdown("---")
    
    # Gráficos
    exibir_graficos(relatorio)
    
    st.markdown("---")
    
    # Temas e Entidades
    exibir_temas_entidades(relatorio)
    
    st.markdown("---")
    
    # Notícias de destaque
    exibir_noticias_destaque(relatorio)
    
    st.markdown("---")
    
    # Insights
    exibir_insights(relatorio)
    
    st.markdown("---")
    
    # Resumo geral
    st.markdown("### 📝 Resumo Geral")
    resumo = relatorio.get('resumo_geral', 'Resumo não disponível')
    st.markdown(f"""
    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
        {resumo}
    </div>
    """, unsafe_allow_html=True)


def pagina_gerar():
    """Página para gerar novo relatório."""
    st.title("🏛️ Gerar Novo Relatório")
    st.markdown("### Extração e Análise de Notícias do TCU")
    
    # Verificar API Key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("❌ GOOGLE_API_KEY não configurada. Configure no arquivo .env")
        return
    
    # Configurações
    col1, col2 = st.columns(2)
    
    with col1:
        quantidade = st.number_input(
            "Quantidade de notícias:",
            min_value=1,
            max_value=50,
            value=5,
            help="Número de notícias a extrair e analisar"
        )
    
    with col2:
        nome_arquivo = st.text_input(
            "Nome do relatório:",
            value="relatorio_tcu",
            help="Nome base para os arquivos gerados"
        )
    
    # Botão de geração
    if st.button("🚀 Gerar Relatório", type="primary", use_container_width=True):
        
        with st.spinner("Extraindo notícias do portal TCU..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # 1. Extração
                status_text.text("📰 Extraindo notícias...")
                progress_bar.progress(20)
                
                scraper = TCUScraper(delay=0.5)
                noticias = scraper.extrair_noticias_completas(quantidade=quantidade)
                
                if not noticias:
                    st.error("❌ Nenhuma notícia foi extraída. Verifique a conexão.")
                    return
                
                st.success(f"✅ {len(noticias)} notícias extraídas!")
                progress_bar.progress(40)
                
                # 2. Análise
                status_text.text("🔍 Analisando notícias com IA...")
                progress_bar.progress(50)
                
                analyzer = TCUAnalyzer()
                noticias_analisadas = analyzer.analisar_noticias(noticias)
                
                if not noticias_analisadas:
                    st.error("❌ Erro na análise das notícias.")
                    return
                
                st.success(f"✅ {len(noticias_analisadas)} notícias analisadas!")
                progress_bar.progress(70)
                
                # 3. Relatório
                status_text.text("📊 Gerando relatório executivo...")
                progress_bar.progress(80)
                
                relatorio = analyzer.gerar_relatorio_executivo(noticias_analisadas)
                
                # 4. Salvar
                status_text.text("💾 Salvando arquivos...")
                progress_bar.progress(90)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                arquivo_json = f"{nome_arquivo}_relatorio_{timestamp}.json"
                
                with open(arquivo_json, 'w', encoding='utf-8') as f:
                    json.dump(relatorio.model_dump(), f, ensure_ascii=False, indent=2)
                
                progress_bar.progress(100)
                status_text.text("✅ Concluído!")
                
                st.success(f"""
                🎉 **Relatório gerado com sucesso!**
                
                - {relatorio.total_noticias} notícias analisadas
                - {len(relatorio.noticias_alta_relevancia)} de alta relevância
                - Arquivo salvo: `{arquivo_json}`
                
                Acesse a aba 'Visualizar' para ver o relatório!
                """)
                
                # Limpar cache para mostrar novo relatório
                st.cache_data.clear()
                
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
                progress_bar.progress(0)


def main():
    """Função principal."""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/government.png", width=80)
        st.title("Menu")
        
        pagina = st.radio(
            "Navegação:",
            ["📊 Visualizar Relatórios", "🚀 Gerar Novo Relatório"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.markdown("""
        Sistema de extração e análise de notícias do portal TCU.
        
        **Tecnologias:**
        - Web Scraping
        - LangChain
        - Google Gemini
        - Pydantic
        - Streamlit
        """)
        
        st.markdown("---")
        
        # Estatísticas
        relatorios = carregar_relatorios_salvos()
        st.metric("Relatórios Salvos", len(relatorios))
        
        if relatorios:
            ultimo = datetime.fromtimestamp(relatorios[0]['timestamp'])
            st.markdown(f"**Último:** {ultimo.strftime('%d/%m/%Y %H:%M')}")
    
    # Renderizar página selecionada
    if pagina == "📊 Visualizar Relatórios":
        pagina_visualizar()
    else:
        pagina_gerar()


if __name__ == "__main__":
    main()

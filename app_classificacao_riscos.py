"""
Sistema de Classificação Automática de Riscos de Auditoria
Aplicação Streamlit com banco de dados SQLite
"""
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from database_riscos import DatabaseRiscos

# Carregar variáveis de ambiente
# Procurar .env em múltiplos locais
import sys
for path in ['.', '..', os.path.dirname(__file__)]:
    env_path = os.path.join(path, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
        break
else:
    load_dotenv()  # Tentar carregar do diretório atual como fallback

# Configuração da página
st.set_page_config(
    page_title="Sistema de Classificação de Riscos",
    page_icon="⚠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .risk-alto {
        background-color: #ffebee;
        border-left: 5px solid #f44336;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .risk-medio {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .risk-baixo {
        background-color: #e8f5e9;
        border-left: 5px solid #4caf50;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .metric-card {
        background-color: #f5f5f5;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# Schema de Saída
class ClassificacaoRisco(BaseModel):
    nivel: str = Field(description="Nível de risco: 'Alto', 'Médio' ou 'Baixo'")
    justificativa: str = Field(description="Explicação breve do porquê desse nível de risco")
    acao_sugerida: str = Field(description="Ação imediata recomendada")


@st.cache_resource
def get_llm():
    """Inicializa e retorna o modelo LLM."""
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)


@st.cache_resource
def get_database():
    """Inicializa e retorna a instância do banco de dados."""
    return DatabaseRiscos()


def criar_chain_classificacao():
    """Cria a chain de classificação de riscos."""
    llm = get_llm()
    structured_llm = llm.with_structured_output(ClassificacaoRisco)
    
    sistema = """
Você é um especialista em Gestão de Riscos Corporativos.
Classifique o seguinte apontamento de auditoria interna conforme a matriz:

- ALTO: Perda financeira significativa (> R$ 100k), fraude, violação legal grave (LGPD, Anticorrupção) ou risco de imagem.
- MÉDIO: Falha de processo repetitiva, perda financeira moderada (< R$ 100k) ou dados imprecisos.
- BAIXO: Erros pontuais, documentação faltante não crítica ou melhoria de eficiência.
"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", sistema),
        ("human", "Apontamento: {apontamento}")
    ]) | structured_llm
    
    return prompt


def exibir_classificacao(resultado, apontamento):
    """Exibe a classificação de risco formatada."""
    nivel = resultado.nivel
    
    # Determinar classe CSS
    if nivel == "Alto":
        css_class = "risk-alto"
        emoji = "🔴"
        color = "#f44336"
    elif nivel == "Médio":
        css_class = "risk-medio"
        emoji = "🟡"
        color = "#ff9800"
    else:
        css_class = "risk-baixo"
        emoji = "🟢"
        color = "#4caf50"
    
    st.markdown(f"""
    <div class="{css_class}">
        <h3>{emoji} Nível de Risco: {nivel}</h3>
        <p><strong>Apontamento:</strong> {apontamento}</p>
        <p><strong>Justificativa:</strong> {resultado.justificativa}</p>
        <p><strong>Ação Sugerida:</strong> {resultado.acao_sugerida}</p>
    </div>
    """, unsafe_allow_html=True)


def pagina_classificacao():
    """Página principal de classificação de riscos."""
    st.title("⚠️ Sistema de Classificação de Riscos")
    st.markdown("### Análise Automática de Apontamentos de Auditoria")
    
    # Verificar API Key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("❌ GOOGLE_API_KEY não configurada. Por favor, configure no arquivo .env")
        return
    
    # Área de entrada
    st.markdown("#### 📝 Digite o apontamento de auditoria:")
    
    # Exemplos pré-definidos
    exemplos = {
        "Selecione um exemplo...": "",
        "Perda de estoque sem controle": "O sistema de almoxarifado permite saída de mercadoria sem requisição aprovada. Identificada perda de estoque de R$ 500.000 no ano.",
        "Documentação incompleta": "Três relatórios de despesas de viagem de Junho/2023 estavam sem carimbo da recepção, mas com notas fiscais válidas.",
        "Conflito de interesses": "Identificamos um funcionário do Depto de Compras que é sócio de um fornecedor recém-contratado sem declaração de conflito de interesses."
    }
    
    exemplo_selecionado = st.selectbox("Ou escolha um exemplo:", list(exemplos.keys()))
    
    apontamento = st.text_area(
        "Apontamento:",
        value=exemplos[exemplo_selecionado],
        height=150,
        placeholder="Descreva o apontamento de auditoria aqui..."
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        classificar_btn = st.button("🔍 Classificar Risco", type="primary", use_container_width=True)
    
    # Processar classificação
    if classificar_btn and apontamento.strip():
        with st.spinner("Analisando o risco..."):
            try:
                chain = criar_chain_classificacao()
                resultado = chain.invoke({"apontamento": apontamento})
                
                # Exibir resultado
                st.markdown("---")
                st.markdown("### 📊 Resultado da Análise")
                exibir_classificacao(resultado, apontamento)
                
                # Salvar no banco de dados
                db = get_database()
                classificacao_id = db.inserir_classificacao(
                    apontamento=apontamento,
                    nivel_risco=resultado.nivel,
                    justificativa=resultado.justificativa,
                    acao_sugerida=resultado.acao_sugerida
                )
                
                st.success(f"✅ Classificação salva com sucesso! (ID: {classificacao_id})")
                
            except Exception as e:
                st.error(f"❌ Erro ao classificar: {str(e)}")
    
    elif classificar_btn:
        st.warning("⚠️ Por favor, digite um apontamento para classificar.")


def pagina_historico():
    """Página de histórico de classificações."""
    st.title("📋 Histórico de Classificações")
    
    db = get_database()
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtro_nivel = st.selectbox(
            "Filtrar por nível:",
            ["Todos", "Alto", "Médio", "Baixo"]
        )
    
    with col2:
        limite = st.number_input("Mostrar últimos:", min_value=5, max_value=100, value=20, step=5)
    
    # Obter dados
    if filtro_nivel == "Todos":
        classificacoes = db.obter_todas_classificacoes()
    else:
        classificacoes = db.obter_classificacoes_por_nivel(filtro_nivel)
    
    # Limitar resultados
    classificacoes = classificacoes[:limite]
    
    if not classificacoes:
        st.info("ℹ️ Nenhuma classificação encontrada.")
        return
    
    st.markdown(f"**Total de registros:** {len(classificacoes)}")
    
    # Exibir classificações
    for i, clf in enumerate(classificacoes, 1):
        with st.expander(f"{i}. {clf['nivel']} - {clf['data_hora']} (ID: {clf['id']})"):
            exibir_classificacao(
                type('obj', (object,), {
                    'nivel': clf['nivel_risco'],
                    'justificativa': clf['justificativa'],
                    'acao_sugerida': clf['acao_sugerida']
                })(),
                clf['apontamento']
            )
            
            # Botão de deletar
            if st.button(f"🗑️ Deletar", key=f"del_{clf['id']}"):
                if db.deletar_classificacao(clf['id']):
                    st.success("Classificação deletada!")
                    st.rerun()


def pagina_dashboard():
    """Página de dashboard com estatísticas."""
    st.title("📊 Dashboard de Riscos")
    
    db = get_database()
    stats = db.obter_estatisticas()
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Análises", stats['total'])
    
    with col2:
        st.metric("🔴 Risco Alto", stats['alto'])
    
    with col3:
        st.metric("🟡 Risco Médio", stats['medio'])
    
    with col4:
        st.metric("🟢 Risco Baixo", stats['baixo'])
    
    if stats['total'] > 0:
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de pizza
            st.markdown("### Distribuição de Riscos")
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Alto', 'Médio', 'Baixo'],
                values=[stats['alto'], stats['medio'], stats['baixo']],
                marker=dict(colors=['#f44336', '#ff9800', '#4caf50']),
                hole=0.3
            )])
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Gráfico de barras
            st.markdown("### Quantidade por Nível")
            fig_bar = go.Figure(data=[go.Bar(
                x=['Alto', 'Médio', 'Baixo'],
                y=[stats['alto'], stats['medio'], stats['baixo']],
                marker=dict(color=['#f44336', '#ff9800', '#4caf50'])
            )])
            fig_bar.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Tabela de dados
        st.markdown("---")
        st.markdown("### 📑 Dados Completos")
        df = db.obter_dataframe()
        st.dataframe(df, use_container_width=True)
        
        # Exportar dados
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar para CSV",
            data=csv,
            file_name=f"classificacoes_risco_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("ℹ️ Nenhuma classificação registrada ainda. Comece classificando alguns apontamentos!")


def pagina_matriz():
    """Página explicativa da matriz de riscos."""
    st.title("📐 Matriz de Riscos")
    st.markdown("### Critérios de Classificação")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="risk-alto">
            <h3>🔴 RISCO ALTO</h3>
            <ul>
                <li>Perda financeira significativa (> R$ 100k)</li>
                <li>Fraude detectada</li>
                <li>Violação legal grave (LGPD, Anticorrupção)</li>
                <li>Risco de imagem corporativa</li>
            </ul>
            <p><strong>Prioridade:</strong> Ação imediata</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="risk-medio">
            <h3>🟡 RISCO MÉDIO</h3>
            <ul>
                <li>Falha de processo repetitiva</li>
                <li>Perda financeira moderada (< R$ 100k)</li>
                <li>Dados imprecisos ou incompletos</li>
                <li>Controles internos fracos</li>
            </ul>
            <p><strong>Prioridade:</strong> Ação em curto prazo</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="risk-baixo">
            <h3>🟢 RISCO BAIXO</h3>
            <ul>
                <li>Erros pontuais e isolados</li>
                <li>Documentação faltante não crítica</li>
                <li>Oportunidades de melhoria de eficiência</li>
                <li>Não conformidades menores</li>
            </ul>
            <p><strong>Prioridade:</strong> Ação em médio prazo</p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Função principal da aplicação."""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/risk.png", width=80)
        st.title("Menu")
        
        pagina = st.radio(
            "Navegação:",
            ["🔍 Classificar Risco", "📋 Histórico", "📊 Dashboard", "📐 Matriz de Riscos"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre")
        st.markdown("""
        Sistema de classificação automática de riscos de auditoria usando IA.
        
        **Tecnologias:**
        - LangChain
        - Google Gemini
        - Streamlit
        - SQLite
        """)
        
        st.markdown("---")
        
        # Opções de administração
        with st.expander("⚙️ Administração"):
            db = get_database()
            stats = db.obter_estatisticas()
            st.metric("Total de registros", stats['total'])
            
            if st.button("🗑️ Limpar todos os dados", type="secondary"):
                if st.checkbox("Confirmar exclusão"):
                    db.limpar_todas_classificacoes()
                    st.success("Dados limpos!")
                    st.rerun()
    
    # Renderizar página selecionada
    if pagina == "🔍 Classificar Risco":
        pagina_classificacao()
    elif pagina == "📋 Histórico":
        pagina_historico()
    elif pagina == "📊 Dashboard":
        pagina_dashboard()
    elif pagina == "📐 Matriz de Riscos":
        pagina_matriz()


if __name__ == "__main__":
    main()

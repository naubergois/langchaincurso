"""
Sistema de Gestão de Riscos de Fornecedores - Interface Web
Aplicação Streamlit para avaliação de fornecedores em contratos municipais.
"""
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

from cnpj_validator import CNPJValidatorMock
from questionario_engine import QuestionarioEngine
from risco_analyzer import RiscoAnalyzer
from fornecedor_models import (
    Fornecedor, QuestionarioResposta, Resposta,
    TipoQuestao
)

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(
    page_title="Gestão de Fornecedores",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .risk-high {
        background-color: #ffebee;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #f44336;
        margin: 10px 0;
    }
    .risk-medium {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
    }
    .risk-low {
        background-color: #e8f5e9;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #4caf50;
        margin: 10px 0;
    }
    .question-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)


# Inicializar session state
if 'fornecedor' not in st.session_state:
    st.session_state.fornecedor = None
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}
if 'relatorio' not in st.session_state:
    st.session_state.relatorio = None


def pagina_cadastro():
    """Página de cadastro de fornecedor."""
    st.title("🏢 Cadastro de Fornecedor")
    st.markdown("### Consulta de Dados do CNPJ")
    
    # Mostrar CNPJs de exemplo
    validator = CNPJValidatorMock()
    empresas_exemplo = validator.listar_empresas_exemplo()
    
    with st.expander("📋 CNPJs de Exemplo Disponíveis"):
        for emp in empresas_exemplo:
            situacao_emoji = "✅" if emp["situacao"] == "Ativa" else "⚠️"
            st.markdown(f"{situacao_emoji} **{emp['cnpj']}** - {emp['razao_social']} ({emp['situacao']})")
    
    st.markdown("---")
    
    # Input de CNPJ
    col1, col2 = st.columns([3, 1])
    
    with col1:
        cnpj = st.text_input(
            "CNPJ do Fornecedor:",
            placeholder="00.000.000/0000-00",
            help="Digite o CNPJ ou use um dos exemplos acima"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        consultar = st.button("🔍 Consultar", type="primary", use_container_width=True)
    
    if consultar and cnpj:
        with st.spinner("Consultando dados da Receita Federal..."):
            dados = validator.consultar_cnpj(cnpj)
            
            if dados:
                st.success("✅ CNPJ encontrado!")
                
                # Criar fornecedor
                fornecedor = Fornecedor(
                    cnpj=dados.cnpj,
                    dados_receita=dados
                )
                st.session_state.fornecedor = fornecedor
                
                # Exibir dados
                st.markdown("### 📊 Dados da Empresa")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Razão Social", dados.razao_social)
                    st.metric("CNPJ", dados.cnpj)
                    st.metric("Situação", dados.situacao_cadastral)
                
                with col2:
                    st.metric("Capital Social", f"R$ {dados.capital_social:,.2f}")
                    st.metric("Porte", dados.porte)
                    st.metric("Município", f"{dados.municipio}/{dados.uf}")
                
                with col3:
                    cert_federal = "✅" if dados.certidao_federal_valida else "❌"
                    cert_fgts = "✅" if dados.certidao_fgts_valida else "❌"
                    cert_trab = "✅" if dados.certidao_trabalhista_valida else "❌"
                    
                    st.markdown(f"**Certidões:**")
                    st.markdown(f"{cert_federal} Federal")
                    st.markdown(f"{cert_fgts} FGTS")
                    st.markdown(f"{cert_trab} Trabalhista")
                
                st.markdown("---")
                st.info("👉 Prossiga para a aba 'Questionário' para iniciar a avaliação de riscos.")
                
            else:
                st.error("❌ CNPJ não encontrado ou inválido.")
    
    elif st.session_state.fornecedor:
        st.info(f"✅ Fornecedor carregado: {st.session_state.fornecedor.dados_receita.razao_social}")


def pagina_questionario():
    """Página do questionário."""
    st.title("📝 Questionário de Avaliação")
    
    if not st.session_state.fornecedor:
        st.warning("⚠️ Cadastre um fornecedor primeiro na aba 'Cadastro'.")
        return
    
    st.markdown(f"### Fornecedor: {st.session_state.fornecedor.dados_receita.razao_social}")
    
    engine = QuestionarioEngine()
    questoes = engine.gerar_questionario_completo()
    
    # Agrupar por categoria
    categorias = engine.listar_categorias()
    
    # Tabs por categoria
    tabs = st.tabs(categorias)
    
    for idx, categoria in enumerate(categorias):
        with tabs[idx]:
            st.markdown(f"### {categoria}")
            questoes_cat = engine.gerar_questionario_por_categoria(categoria)
            
            for questao in questoes_cat:
                with st.container():
                    st.markdown(f"""
                    <div class="question-card">
                        <strong>{questao.id}</strong> - {questao.texto}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Input baseado no tipo
                    if questao.tipo == TipoQuestao.SIM_NAO:
                        resposta = st.radio(
                            "Resposta:",
                            ["Sim", "Não"],
                            key=questao.id,
                            horizontal=True
                        )
                    
                    elif questao.tipo == TipoQuestao.MULTIPLA_ESCOLHA:
                        resposta = st.selectbox(
                            "Selecione:",
                            questao.opcoes,
                            key=questao.id
                        )
                    
                    elif questao.tipo == TipoQuestao.NUMERICO:
                        resposta = st.number_input(
                            "Valor:",
                            min_value=0.0,
                            key=questao.id,
                            format="%.2f"
                        )
                    
                    else:  # TEXTO_LIVRE
                        resposta = st.text_input(
                            "Resposta:",
                            key=questao.id
                        )
                    
                    # Salvar resposta
                    if resposta:
                        st.session_state.respostas[questao.id] = str(resposta)
    
    # Botão de finalizar
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        total_questoes = len(questoes)
        respondidas = len(st.session_state.respostas)
        
        st.progress(respondidas / total_questoes)
        st.markdown(f"**Progresso:** {respondidas}/{total_questoes} questões respondidas")
        
        if st.button("✅ Finalizar Questionário", type="primary", use_container_width=True):
            if respondidas < total_questoes:
                st.warning(f"⚠️ Responda todas as {total_questoes} questões antes de finalizar.")
            else:
                # Criar questionário respondido
                respostas_list = [
                    Resposta(questao_id=qid, valor=valor)
                    for qid, valor in st.session_state.respostas.items()
                ]
                
                questionario = QuestionarioResposta(
                    fornecedor_cnpj=st.session_state.fornecedor.cnpj,
                    respostas=respostas_list,
                    data_conclusao=datetime.now()
                )
                
                st.session_state.fornecedor.questionario = questionario
                st.success("✅ Questionário finalizado! Prossiga para 'Análise de Riscos'.")
                st.balloons()


def pagina_analise():
    """Página de análise de riscos."""
    st.title("📊 Análise de Riscos")
    
    if not st.session_state.fornecedor:
        st.warning("⚠️ Cadastre um fornecedor primeiro.")
        return
    
    if not st.session_state.fornecedor.questionario:
        st.warning("⚠️ Complete o questionário primeiro.")
        return
    
    # Verificar API Key
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("❌ GOOGLE_API_KEY não configurada. Configure no arquivo .env")
        return
    
    if st.button("🚀 Gerar Análise de Riscos", type="primary"):
        with st.spinner("Analisando riscos com IA..."):
            try:
                analyzer = RiscoAnalyzer()
                relatorio = analyzer.gerar_relatorio(st.session_state.fornecedor)
                st.session_state.relatorio = relatorio
                st.success("✅ Análise concluída!")
            except Exception as e:
                st.error(f"❌ Erro na análise: {str(e)}")
                return
    
    # Exibir relatório se existir
    if st.session_state.relatorio:
        rel = st.session_state.relatorio
        
        # Métricas principais
        st.markdown("### 📈 Resumo Executivo")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pontuação Geral", f"{rel.pontuacao_geral:.1f}/10")
        
        with col2:
            cor_class = {
                "Baixo Risco": "🟢",
                "Médio Risco": "🟡",
                "Alto Risco": "🔴"
            }
            st.metric("Classificação", f"{cor_class.get(rel.classificacao.value, '')} {rel.classificacao.value}")
        
        with col3:
            st.metric("Discrepâncias", rel.total_discrepancias)
        
        with col4:
            st.metric("Críticas", rel.discrepancias_criticas)
        
        # Resumo
        st.markdown("---")
        st.markdown(rel.resumo_executivo)
        
        # Análise por categoria
        st.markdown("---")
        st.markdown("### 📊 Análise por Categoria")
        
        for cat_nome, cat_analise in rel.analise_por_categoria.items():
            with st.expander(f"{cat_nome} - {cat_analise.nivel_risco} Risco ({cat_analise.pontuacao:.1f}/10)"):
                st.markdown(f"**Questões respondidas:** {cat_analise.questoes_respondidas}")
                st.markdown(f"**Discrepâncias:** {cat_analise.discrepancias}")
                
                if cat_analise.principais_problemas:
                    st.markdown("**Principais problemas:**")
                    for prob in cat_analise.principais_problemas:
                        st.markdown(f"- {prob}")
        
        # Discrepâncias
        if rel.lista_discrepancias:
            st.markdown("---")
            st.markdown("### ⚠️ Discrepâncias Identificadas")
            
            for disc in rel.lista_discrepancias:
                css_class = {
                    "Alto": "risk-high",
                    "Médio": "risk-medium",
                    "Baixo": "risk-low"
                }.get(disc.nivel_gravidade.value, "risk-medium")
                
                st.markdown(f"""
                <div class="{css_class}">
                    <strong>{disc.nivel_gravidade.value}</strong> - {disc.questao_texto}<br>
                    <strong>Resposta:</strong> {disc.resposta_fornecedor}<br>
                    <strong>Dado Oficial:</strong> {disc.dado_oficial}<br>
                    <strong>Análise:</strong> {disc.explicacao}
                </div>
                """, unsafe_allow_html=True)
        
        # Recomendações
        if rel.recomendacoes:
            st.markdown("---")
            st.markdown("### 💡 Recomendações")
            
            for rec in rel.recomendacoes:
                with st.expander(f"[{rec.prioridade}] {rec.titulo}"):
                    st.markdown(f"**Categoria:** {rec.categoria}")
                    st.markdown(f"**Descrição:** {rec.descricao}")
                    st.markdown(f"**Prazo:** {rec.prazo_sugerido}")
                    st.markdown(f"**Responsável:** {rec.responsavel}")
        
        # Decisão
        st.markdown("---")
        st.markdown("### ⚖️ Decisão Sugerida")
        
        decisao_cor = {
            "Aprovar": "🟢",
            "Aprovar com Ressalvas": "🟡",
            "Rejeitar": "🔴"
        }
        
        st.markdown(f"## {decisao_cor.get(rel.decisao_sugerida, '')} {rel.decisao_sugerida}")
        st.markdown(f"**Justificativa:** {rel.justificativa_decisao}")


def main():
    """Função principal."""
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/business.png", width=80)
        st.title("Menu")
        
        pagina = st.radio(
            "Navegação:",
            ["🏢 Cadastro", "📝 Questionário", "📊 Análise de Riscos"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### ℹ️ Sobre o Sistema")
        st.markdown("""
        Sistema de Gestão de Riscos de Fornecedores para contratos municipais.
        
        **Funcionalidades:**
        - Consulta de CNPJ (mock)
        - 25 questões em 5 categorias
        - Análise de discrepâncias com IA
        - Relatórios executivos
        - Recomendações automáticas
        """)
        
        st.markdown("---")
        
        # Status
        if st.session_state.fornecedor:
            st.success(f"✅ Fornecedor: {st.session_state.fornecedor.dados_receita.razao_social[:20]}...")
            
            if st.session_state.fornecedor.questionario:
                st.success("✅ Questionário completo")
            
            if st.session_state.relatorio:
                st.success("✅ Análise gerada")
        
        # Botão de reset
        if st.button("🔄 Reiniciar", use_container_width=True):
            st.session_state.fornecedor = None
            st.session_state.respostas = {}
            st.session_state.relatorio = None
            st.rerun()
    
    # Renderizar página selecionada
    if pagina == "🏢 Cadastro":
        pagina_cadastro()
    elif pagina == "📝 Questionário":
        pagina_questionario()
    else:
        pagina_analise()


if __name__ == "__main__":
    main()

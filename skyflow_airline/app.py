import streamlit as st
import os
import sys

# Adiciona o diretório base ao path para facilitar imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from skyflow_airline.agents import SkyFlowTeam
from langchain_core.messages import HumanMessage, AIMessage

# Configuração da página
st.set_page_config(
    page_title="SkyFlow Airlines - Premium Concierge",
    page_icon="✈️",
    layout="wide"
)

# Estilização Customizada
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stChatFloatingInputContainer {
        bottom: 20px;
    }
    .agent-header {
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 5px;
    }
    .sidebar-content {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do Time e Histórico
if "team" not in st.session_state:
    st.session_state.team = SkyFlowTeam()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar - Informações da Empresa
with st.sidebar:
    st.title("✈️ SkyFlow Airlines")
    st.markdown("---")
    st.markdown("### 👨‍✈️ Nossa Equipe de Agentes")
    
    with st.expander("🎟️ Consultor de Reservas", expanded=True):
        st.write("Especialista em encontrar as melhores rotas e preços para sua viagem.")
        
    with st.expander("🚀 Especialista em Voos", expanded=True):
        st.write("Monitora o status de todos os nossos voos e portões em tempo real.")
        
    with st.expander("🛠️ Suporte ao Cliente", expanded=True):
        st.write("Dedicado a resolver qualquer imprevisto com sua viagem ou bagagem.")
    
    st.markdown("---")
    if st.button("Limpar Conversa"):
        st.session_state.messages = []
        st.rerun()

# Layout Principal
st.title("SkyFlow Concierge Digital")
st.caption("Central de atendimento inteligente e personalizada para sua viagem.")

# Mostrar mensagens anteriores
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        # Tenta pegar quem respondeu dos metadados ou deixa genérico
        agent_name = msg.additional_kwargs.get("agent_name", "SkyFlow AI")
        icon = msg.additional_kwargs.get("icon", "✈️")
        with st.chat_message("assistant", avatar=icon):
            st.markdown(f"**{agent_name}**")
            st.markdown(msg.content)

# Input do Usuário
if prompt := st.chat_input("Como posso ajudar com sua viagem hoje?"):
    # Renderiza mensagem do usuário
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Processamento com a Equipe
    with st.spinner("A equipa SkyFlow está a analisar o seu pedido..."):
        # Prepara histórico para os agentes
        history = st.session_state.messages
        # Roda o sistema multi-agente
        agent_name, response, icon = st.session_state.team.run(prompt, history)
        
        # Renderiza resposta do assistente
        with st.chat_message("assistant", avatar=icon):
            st.markdown(f"**{agent_name}**")
            st.markdown(response)
        
        # Salva no histórico
        st.session_state.messages.append(HumanMessage(content=prompt))
        st.session_state.messages.append(
            AIMessage(
                content=response, 
                additional_kwargs={"agent_name": agent_name, "icon": icon}
            )
        )

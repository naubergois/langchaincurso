import os
import functools
import operator
from typing import Annotated, Sequence, TypedDict, Union, Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Carrega chaves
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts/.env"))

# 1. Definição das Ferramentas (Wrapper para LangChain)
import skyflow_airline.tools as airline_tools

@tool
def search_flights(origin: str, destination: str):
    """Procura voos disponíveis entre duas cidades. Cidades válidas: São Paulo, Rio de Janeiro, Paris, Londres, Nova York, Tóquio."""
    return airline_tools.search_flights(origin, destination)

@tool
def check_flight_status(flight_number: str):
    """Verifica se um voo está no horário, atrasado ou cancelado, e informa o portão."""
    return airline_tools.check_flight_status(flight_number)

@tool
def create_support_ticket(complaint_type: str, details: str):
    """Cria um ticket de suporte para problemas como bagagem perdida, reembolso ou reclamações."""
    return airline_tools.create_support_ticket(complaint_type, details)

# 2. Estado do Grafo
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str

# 3. Helper para criar agentes especialistas
def create_agent(llm: ChatGoogleGenerativeAI, tools: list, system_prompt: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = prompt | llm.bind_tools(tools)
    return agent

# 4. Implementação dos Agentes
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Agente de Reservas
booking_agent = create_agent(
    llm, [search_flights],
    "Você é o Consultor de Reservas da SkyFlow. Ajude os clientes a encontrar os melhores voos."
)

# Agente de Informação
info_agent = create_agent(
    llm, [check_flight_status],
    "Você é o Especialista em Voos da SkyFlow. Forneça atualizações precisas sobre status e portões."
)

# Agente de Suporte
support_agent = create_agent(
    llm, [create_support_ticket],
    "Você é o Especialista de Suporte da SkyFlow. Seja empático e resolva os problemas dos clientes."
)

# 5. Agente Supervisor (Roteador)
members = ["Booking", "FlightInfo", "Support"]
system_prompt = (
    "Você é um supervisor encarregado de gerenciar o atendimento ao cliente da SkyFlow Airlines."
    " Dada a solicitação do usuário abaixo, responda indicando qual trabalhador deve agir em seguida."
    " Cada trabalhador tem uma especialidade. Se você terminou, responda FINISH."
)

class Router(BaseModel):
    """Selecione o próximo trabalhador."""
    next: Literal["FINISH", "Booking", "FlightInfo", "Support"] = Field(
        description="O próximo trabalhador a agir ou FINISH se concluído."
    )

def supervisor_agent(state):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Dada a conversa acima, quem deve agir em seguida?"
            " Escolha um de: FINISH, Booking, FlightInfo, Support",
        ),
    ])

    chain = prompt | llm.with_structured_output(Router)
    result = chain.invoke(state)
    
    # Garantindo que retornamos um dicionário com a chave 'next'
    if hasattr(result, 'next'):
        return {"next": result.next}
    elif isinstance(result, dict):
        return result
    else:
        # Fallback de segurança
        return {"next": "FINISH"}

# 6. Definindo os Nodos (Funções de execução)
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [result]}

# Simplificação radical para o Streamlit (usando LangChain padrão p/ facilitar visualização)
class SkyFlowTeam:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
        self.agents = {
            "Booking": {"agent": booking_agent, "icon": "🎟️"},
            "FlightInfo": {"agent": info_agent, "icon": "✈️"},
            "Support": {"agent": support_agent, "icon": "🛠️"}
        }
    
    def run(self, user_input, history=[]):
        try:
            # Primeiro, o supervisor decide
            state = {"messages": history + [HumanMessage(content=user_input)]}
            route = supervisor_agent(state)
            next_agent = route["next"]
            
            print(f"Supervisor roteou para: {next_agent}")
            
            if next_agent == "FINISH" or next_agent not in self.agents:
                # O próprio Supervisor responde ou pede pro último repetir
                resp = self.llm.invoke(state["messages"])
                return "Supervisor", resp.content, "🧑‍✈️"
            
            # O especialista selecionado responde
            agent_data = self.agents[next_agent]
            tools_list = [search_flights, check_flight_status, create_support_ticket]
            llm_with_tools = self.llm.bind_tools(tools_list)
            
            resp = llm_with_tools.invoke(state["messages"])
            
            # Processamento de ferramentas (se houver)
            if hasattr(resp, 'tool_calls') and resp.tool_calls:
                for tool_call in resp.tool_calls:
                    t_name = tool_call['name']
                    t_args = tool_call['args']
                    if t_name in airline_tools.TOOLS:
                        print(f"Executando ferramenta: {t_name}")
                        f_resp = airline_tools.TOOLS[t_name](**t_args)
                        final_resp = self.llm.invoke(state["messages"] + [resp, HumanMessage(content=f"Resultado da ferramenta {t_name}: {f_resp}. Por favor, responda ao cliente.")])
                        return next_agent, final_resp.content, agent_data["icon"]
            
            return next_agent, resp.content, agent_data["icon"]
        except Exception as e:
            print(f"ERRO NO RUN: {e}")
            import traceback
            traceback.print_exc()
            return "Erro", f"Desculpe, ocorreu um erro interno: {e}", "⚠️"

#!/usr/bin/env python
# coding: utf-8

# # 25. LangGraph: Multi-Agent Supervisor
# 
# O padrão mais avançado de agentes é ter múltiplos especialistas (ex: um Pesquisador, um Codificador, um Revisor) orquestrados por um Supervisor.
# 
# **Objetivos:**
# - Criar agentes especialistas.
# - Criar um nó Supervisor que decide quem chamar.
# - Criar o grafo de roteamento.



### INJECTION START ###
import os
from dotenv import load_dotenv
import sys
for p in ['.', '..', 'scripts', '../scripts']:
    path = os.path.join(p, '.env')
    if os.path.exists(path):
        load_dotenv(path)
        break
if os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.getenv('GOOGLE_API_KEY')
### INJECTION END ###

import os
from dotenv import load_dotenv
load_dotenv()

# !pip install -qU langchain langchain-openai langchain-community langgraph # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
except:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. Definindo os Agentes Especialistas
# 
# Para simplificar, usaremos chains simples como "agentes".



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def agente_pesquisador(state):
    print("--- PESQUISADOR ATUANDO ---")
    messages = [
        SystemMessage(content="Você é um pesquisador web. Retorne dados factuais sobre o tema."),
        HumanMessage(content=state['tarefa'])
    ]
    res = llm.invoke(messages)
    return {"resultado_pesquisa": res.content, "ultimo_agente": "pesquisador"}

def agente_redator(state):
    print("--- REDATOR ATUANDO ---")
    pesquisa = state.get('resultado_pesquisa', 'Sem dados')
    messages = [
        SystemMessage(content="Você é um redator. Escreva um parágrafo elegante baseada na pesquisa."),
        HumanMessage(content=f"Tarefa original: {state['tarefa']}. Pesquisa: {pesquisa}")
    ]
    res = llm.invoke(messages)
    return {"texto_final": res.content, "ultimo_agente": "redator"}


# ## 2. O Supervisor
# 
# Ele decide qual o próximo passo. Usamos `with_structured_output` para forçar ele a escolher um dos agentes ou FINISH.



from pydantic import BaseModel
from typing import Literal

class DecisaoSupervisor(BaseModel):
    proximo: Literal["pesquisador", "redator", "FINISH"]

supervisor_llm = llm.with_structured_output(DecisaoSupervisor)

def supervisor(state):
    print("--- SUPERVISOR PENSANDO ---")
    prompt = f"""
    Tarefa: {state['tarefa']}
    Último agente: {state.get('ultimo_agente')}
    
    Se não tiver pesquisa, chame o 'pesquisador'.
    Se já tiver pesquisa, chame o 'redator'.
    Se já tiver texto final ('ultimo_agente' for redator), chame 'FINISH'.
    """
    decisao = supervisor_llm.invoke(prompt)
    return {"proximo_passo": decisao.proximo}


# ## 3. Montando o Grafo
# 
# Estado e roteamento.



from typing import TypedDict, Optional
from langgraph.graph import StateGraph, START, END

class TeamState(TypedDict):
    tarefa: str
    resultado_pesquisa: Optional[str]
    texto_final: Optional[str]
    ultimo_agente: Optional[str]
    proximo_passo: str

workflow = StateGraph(TeamState)

workflow.add_node("supervisor", supervisor)
workflow.add_node("pesquisador", agente_pesquisador)
workflow.add_node("redator", agente_redator)

workflow.add_edge(START, "supervisor")

# Arestas normais: depois dos trabalhadores, volta pro supervisor decidir
workflow.add_edge("pesquisador", "supervisor")
workflow.add_edge("redator", "supervisor")

# Aresta condicional saindo do supervisor
def roteador_supervisor(state):
    if state['proximo_passo'] == "FINISH":
        return END
    return state['proximo_passo']

workflow.add_conditional_edges(
    "supervisor",
    roteador_supervisor,
    {
        "pesquisador": "pesquisador",
        "redator": "redator",
        END: END
    }
)

app = workflow.compile()


# ## 4. Executando o Time
# 
# Vamos pedir para escrever sobre Python.



res = app.invoke({"tarefa": "Escreva um resumo histórico sobre a linguagem Python."})




print("\n=== TEXTO FINAL ===")
print(res['texto_final'])


# ## Conclusão
# 
# Criamos uma arquitetura hierárquica onde um Supervisor gerencia o fluxo entre subordinados. Este é o estado da arte em sistemas baseados em Agentes.
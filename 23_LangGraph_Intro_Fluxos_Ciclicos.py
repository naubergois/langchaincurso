#!/usr/bin/env python
# coding: utf-8

# # 23. Introdução ao LangGraph: Fluxos Cíclicos
# 
# Até agora, nossas Chains eram lineares (DAGs). Mas e se precisarmos de um **loop**? Ex: "Escreva um código, teste. Se der erro, corrija e teste de novo". Para isso serve o `LangGraph`.
# 
# **Objetivos:**
# - Entender `StateGraph`, `Nodes` e `Edges`.
# - Criar um fluxo com condicional (Router).



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


# ## 1. Definindo o Estado (State)
# 
# O Estado é um dicionário (ou objeto Pydantic) compartilhado entre todos os nós do grafo.



from typing import TypedDict

class AgenteState(TypedDict):
    pergunta: str
    resposta: str
    revisoes: int


# ## 2. Definindo os Nós (Nodes)
# 
# São funções python simples que recebem o estado e retornam uma atualização para ele.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

def gerador(state: AgenteState):
    print(f"--- GERANDO (Tentativa {state['revisoes']}) ---")
    prompt = ChatPromptTemplate.from_template("Responda a pergunta de forma breve: {pergunta}")
    chain = prompt | llm | StrOutputParser()
    res = chain.invoke({"pergunta": state['pergunta']})
    return {"resposta": res, "revisoes": state['revisoes'] + 1}

def critico(state: AgenteState):
    print("--- CRITICANDO ---")
    # Simulação: se a resposta tiver menos de 20 chars, achamos ruim
    # Se já revisou 3 vezes, aceitamos de qualquer jeito para evitar loop infinito
    if len(state['resposta']) < 20 and state['revisoes'] < 3:
        return {"pergunta": state['pergunta'] + " (Seja mais detalhado!)"}
    return {} # Nenhuma mudança


# ## 3. Definindo a Lógica Condicional (Edges)
# 
# Decide se volta para o gerador ou termina.



from langgraph.graph import END

def router(state: AgenteState):
    pass # Script-patched: ensure non-empty block
    # Se a resposta for curta e tivermos revisões sobrando, volta pro gerador
    if len(state['resposta']) < 20 and state['revisoes'] < 3:
        return "gerador"
    return END


# ## 4. Montando o Grafo
# 
# Adicionamos nós e arestas.



from langgraph.graph import StateGraph, START

workflow = StateGraph(AgenteState)

workflow.add_node("gerador", gerador)
workflow.add_node("critico", critico)

# Fluxo: Start -> Gerador -> Critico -> Router -> (Gerador ou Fim)
workflow.add_edge(START, "gerador")
workflow.add_edge("gerador", "critico")

workflow.add_conditional_edges(
    "critico",
    router,
    {
        "gerador": "gerador",
        END: END
    }
)

app = workflow.compile()


# ## 5. Executando
# 
# Vamos fazer uma pergunta que exige resposta curta para ver se ele entra no loop.



inputs = {"pergunta": "Quem descobriu o Brasil?", "revisoes": 0, "resposta": ""}
output = app.invoke(inputs)

print("\n=== FINAL ===")
print(output['resposta'])
print(f"Total revisões: {output['revisoes']}")


# ## Conclusão
# 
# Criamos um sistema que se auto-corrige! O `LangGraph` permite criar fluxos de trabalho resilientes onde o agente pode tentar novamente se falhar.
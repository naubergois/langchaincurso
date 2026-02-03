#!/usr/bin/env python
# coding: utf-8

# # 23. Introdução ao LangGraph: Fluxos Cíclicos
# 
# Até agora, nossas Chains eram lineares (DAGs). Mas e se precisarmos de um **loop**? Ex: "Escreva um código, teste. Se der erro, corrija e teste de novo". Para isso serve o `LangGraph`.
# 
# **Objetivos:**
# - Entender `StateGraph`, `Nodes` e `Edges`.
# - Criar um fluxo com condicional (Router).

# # Explicação Detalhada do Assunto
# 
# # 23. Introdução ao LangGraph: Fluxos Cíclicos
# 
# Este notebook marca uma transição crucial no nosso aprendizado de LangChain, nos levando além das Chains lineares (DAGs - Directed Acyclic Graphs) para explorar fluxos de trabalho mais dinâmicos e complexos: os **fluxos cíclicos**. Prepare-se para construir aplicações de IA que podem aprender, iterar e refinar suas respostas com base em feedback contínuo.
# 
# ## Resumo Executivo
# 
# Neste notebook, vamos mergulhar no LangGraph e aprender como construir grafos de execução que permitem loops, ou seja, fluxos de trabalho que podem retornar a nós anteriores para refinamento.  Vamos construir um exemplo prático onde um agente gera uma resposta, um crítico a avalia e, se necessário, o agente refina a resposta em um ciclo iterativo até atingir um nível de qualidade aceitável.
# 
# ## Conceitos Chave
# 
# Para entender completamente este notebook, é importante estar familiarizado com os seguintes conceitos:
# 
# *   **Chains (Cadeias)**: Sequências de chamadas a LLMs (Large Language Models) ou outras utilidades, executadas em uma ordem específica. Até agora, nossas Chains eram lineares, com um fluxo unidirecional.
# *   **DAG (Directed Acyclic Graph)**: Um grafo direcionado sem ciclos. As Chains lineares que vimos até agora são DAGs.
# *   **Fluxos Cíclicos**: Fluxos de trabalho que permitem loops, ou seja, a capacidade de retornar a nós anteriores para refinamento ou iteração. Isso é fundamental para construir aplicações que podem aprender e melhorar ao longo do tempo.
# *   **Estado (State)**: Um dicionário (ou objeto Pydantic) compartilhado entre todos os nós do grafo. Ele armazena informações relevantes para o fluxo de trabalho, como a pergunta original, a resposta gerada e o número de revisões.
# *   **Nós (Nodes)**: Funções Python simples que recebem o estado e retornam uma atualização para ele. Cada nó representa uma etapa no fluxo de trabalho, como gerar uma resposta ou avaliar sua qualidade.
# *   **Arestas (Edges)**: Conexões entre os nós do grafo. Elas definem o fluxo de execução e podem ser condicionais, permitindo que o fluxo de trabalho se adapte com base no estado atual.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Compreender o conceito de fluxos cíclicos e sua importância na construção de aplicações de IA mais inteligentes.
# *   Definir o estado compartilhado entre os nós do grafo.
# *   Criar nós que executam tarefas específicas e atualizam o estado.
# *   Implementar lógica condicional para controlar o fluxo de execução do grafo.
# *   Montar um grafo LangGraph com nós e arestas, definindo um fluxo de trabalho cíclico.
# *   Executar o grafo e observar como ele itera para refinar a resposta.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de criar fluxos cíclicos é um passo fundamental para construir aplicações de IA generativa mais avançadas e adaptativas.  LangGraph fornece as ferramentas necessárias para orquestrar esses fluxos complexos, permitindo que você crie agentes que podem aprender com seus erros, refinar suas respostas e se adaptar a novas situações.  Dominar LangGraph abre um mundo de possibilidades para construir aplicações de IA mais poderosas e eficazes.
# 
# ---
# 



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
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
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
#!/usr/bin/env python
# coding: utf-8

# # 08. Agentes e Ferramentas (Tools)
# 
# Chains são sequências fixas de ações (hard-coded). Agentes usam um LLM como "cérebro" para decidir quais ações tomar e em qual ordem, baseando-se nas ferramentas disponíveis.
# 
# **Objetivos:**
# - Entender o conceito de Agente.
# - Usar ferramentas prontas (Busca Web).
# - Inicializar e rodar um agente.



### INJECTION START ###
import os
from dotenv import load_dotenv
import sys
# Carrega .env do local ou de pastas comuns
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
import sys
# Autenticação automática do script
for p in ['.', '..', 'scripts', '../scripts']:
    path = os.path.join(p, '.env')
    if os.path.exists(path):
        load_dotenv(path)
        break
if os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

import os
from dotenv import load_dotenv
load_dotenv()

# !pip install -qU langchain langchain-openai langchain-community duckduckgo-search # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    pass # Script-patched: using env var
except:
    pass # Script-patched: using env var


# ## 1. Definindo as Ferramentas (Tools)
# 
# Vamos dar ao agente acesso à internet usando o DuckDuckGo Search.



from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

# Lista de tools disponíveis para o agente
tools = [search]


# ## 2. Criando o Agente
# 
# Vamos usar `create_tool_calling_agent`, que é otimizado para modelos modernos como GPT-3.5 e GPT-4 que suportam "function calling" nativamente.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Podemos puxar um prompt pronto do LangChain Hub ou criar um simples
# O prompt precisa ter suporte para 'agent_scratchpad' (onde ele anota os pensamentos intermédios)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente útil. Use as ferramentas disponíveis para responder às perguntas."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)


# ## 3. Executando o Agente
# 
# O `AgentExecutor` é o runtime que roda o loop de pensamento do agente (Pensar -> Agir -> Observar -> Repetir).



agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

agent_executor.invoke({"input": "Quem é o atual presidente da França e qual a sua idade aproximada?"})


# Observe no output (verbose=True) que ele decide usar a tool `duckduckgo_search`, recebe a resposta, e depois formula a resposta final.

# ## Conclusão
# 
# Vimos como um agente pode usar ferramentas externas para buscar informações em tempo real.
# 
# No próximo notebook, vamos criar **nossas próprias ferramentas** em Python.
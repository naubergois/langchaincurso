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

# # Explicação Detalhada do Assunto
# 
# # 08. Agentes e Ferramentas (Tools)
# 
# Bem-vindo(a) ao notebook sobre Agentes e Ferramentas no LangChain! Prepare-se para expandir suas habilidades em IA Generativa e construir aplicações ainda mais inteligentes e dinâmicas.
# 
# **Resumo Executivo:**
# 
# Neste notebook, vamos explorar o poder dos Agentes no LangChain. Enquanto as Chains oferecem sequências de ações predefinidas, os Agentes utilizam um LLM (Large Language Model) como um "cérebro" para tomar decisões sobre quais ações realizar e em qual ordem, com base nas ferramentas disponíveis. Aprenderemos a criar agentes que podem interagir com o mundo externo, buscar informações em tempo real e fornecer respostas precisas e contextuais.
# 
# **Conceitos Chave:**
# 
# *   **Chains:** Sequências fixas de ações, com um fluxo de trabalho predefinido.
# *   **Agentes:** Entidades que usam um LLM para decidir dinamicamente quais ações tomar, com base em ferramentas disponíveis.
# *   **Ferramentas (Tools):** Funções ou APIs que o agente pode usar para interagir com o mundo externo (ex: busca na web, cálculos, acesso a bancos de dados).
# *   **Function Calling:** Capacidade dos LLMs (como GPT-3.5 e GPT-4) de identificar quais funções (ferramentas) devem ser usadas com base na pergunta do usuário.
# *   **AgentExecutor:** O componente responsável por executar o ciclo de pensamento do agente (Pensar -> Agir -> Observar -> Repetir).
# 
# **Objetivos de Aprendizado:**
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Entender a diferença fundamental entre Chains e Agentes.
# *   Definir e configurar ferramentas para um agente.
# *   Criar um agente usando `create_tool_calling_agent` (otimizado para modelos com suporte a "function calling").
# *   Executar um agente usando o `AgentExecutor` e interpretar o seu output.
# *   Compreender como o agente decide qual ferramenta usar para responder a uma pergunta.
# 
# **Importância no Ecossistema LangChain:**
# 
# Agentes são um componente crucial do LangChain, pois permitem construir aplicações de IA Generativa que são mais flexíveis, adaptáveis e capazes de interagir com o mundo real. Eles abrem um leque de possibilidades para automatizar tarefas complexas, buscar informações em tempo real, integrar diferentes serviços e criar experiências de usuário mais ricas e personalizadas. Dominar o conceito de Agentes e Ferramentas é um passo fundamental para se tornar um especialista em LangChain e IA Generativa.
# 
# ## 1. Definindo as Ferramentas (Tools)
# 
# Vamos dar ao agente acesso à internet usando o DuckDuckGo Search.
# 
# ```python
# from langchain_community.tools import DuckDuckGoSearchRun
# 
# search = DuckDuckGoSearchRun()
# 
# # Lista de tools disponíveis para o agente
# tools = [search]
# ```
# 
# ## 2. Criando o Agente
# 
# Vamos usar `create_tool_calling_agent`, que é otimizado para modelos modernos como GPT-3.5 e GPT-4 que suportam "function calling" nativamente.
# 
# ```python
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain_core.prompts import ChatPromptTemplate
# 
# llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "Você é muito poderoso assistente, mas útil, que pode responder às perguntas dos usuários usando ferramentas.",
#         ),
#         ("user", "{input}"),
#     ]
# )
# agent = create_tool_calling_agent(llm, tools, prompt)
# ```
# 
# ## 3. Executando o Agente
# 
# O `AgentExecutor` é o runtime que roda o loop de pensamento do agente (Pensar -> Agir -> Observar -> Repetir).
# 
# ```python
# agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# 
# agent_executor.invoke({"input": "Quem é o atual presidente da França e qual a sua idade aproximada?"})
# ```
# 
# Observe no output (verbose=True) que ele decide usar a tool `duckduckgo_search`, recebe a resposta, e depois formula a resposta final.
# 
# ## Conclusão
# 
# Vimos como um agente pode usar ferramentas externas para buscar informações em tempo real.
# 
# No próximo notebook, vamos criar **nossas próprias ferramentas** em Python.
# 
# ---
# 



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
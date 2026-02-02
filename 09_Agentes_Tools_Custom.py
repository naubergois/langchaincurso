#!/usr/bin/env python
# coding: utf-8

# # 09. Agentes com Tools Customizadas
# 
# Muitas vezes precisamos que o agente interaja com nossas próprias APIs, cálculos ou sistemas internos. Para isso, criamos ferramentas customizadas.
# 
# **Objetivos:**
# - Criar uma função Python e decorá-la com `@tool`.
# - Definir tipos e descrições para que o modelo entenda como usar.
# - Passar a tool para o agente.



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

# !pip install -qU langchain langchain-openai langchain-community # Script-patched




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


# ## 1. Criando uma Custom Tool
# 
# Vamos criar uma "ferramenta de cálculo" fictícia, ou algo que o LLM não saiba fazer bem nativamente, como contar letras em uma palavra invertida (só um exemplo bobo para provar que ele chama a função).



from langchain_core.tools import tool

@tool
def multiplica(a: int, b: int) -> int:
    """Multiplica dois números inteiros."""
    return a * b

@tool
def conta_caracteres(texto: str) -> int:
    """Conta o número de caracteres em um texto."""
    return len(texto)

tools = [multiplica, conta_caracteres]


# ## 2. Configurando o Agente
# 
# Mesmo processo do notebook anterior, mas agora com nossas tools.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente matemático e analítico."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ## 3. Testando
# 
# Vamos pedir algo que precise das ferramentas.



# Aqui ele deve chamar a tool 'multiplica' em vez de tentar calcular internamente (embora LLMs saibam multiplicar, estamos forçando o uso da tool pelo prompt/contexto ou apenas testando)
agent_executor.invoke({"input": "Quanto é 1234 vezes 5678?"})




agent_executor.invoke({"input": "Quantas letras tem a palavra 'paralelepípedo'?"})


# ## Conclusão
# 
# Criar ferramentas customizadas é o superpoder dos Agentes. Você pode integrar com Banco de Dados, APIs REST, Slack, E-mail, etc.
# 
# No próximo e último notebook, faremos um **Projeto Final**: Um Chatbot que conversa com seu PDF.
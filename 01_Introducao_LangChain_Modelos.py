#!/usr/bin/env python
# coding: utf-8

# # 01. Introdução ao LangChain e Modelos
# 
# Bem-vindo ao curso prático de LangChain! Neste primeiro notebook, vamos configurar nosso ambiente e fazer nossas primeiras chamadas a modelos de linguagem (LLMs) e ChatModels.
# 
# **Objetivos:**
# - Instalar as bibliotecas necessárias.
# - Configurar chaves de API.
# - Diferenciar LLMs de ChatModels.
# - Fazer a primeira chamada ("Hello World").

# ## 1. Instalação
# 
# Vamos instalar o `langchain`, `langchain-openai` e outras dependências comuns.



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
import sys
# Look for .env in scripts folder
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

# !pip install -qU langchain langchain-openai langchain-community python-dotenv # Script-patched: assumed installed


# ## 2. Configuração da API Key
# 
# Para usar os modelos da OpenAI, precisamos de uma API Key. No Colab, a forma mais segura é usar o `google.colab.userdata` se você tiver salvado a chave nos segredos do Colab, ou usar `getpass` para digitar na hora.



import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    pass # Script-patched
except:
    pass # Added to avoid IndentationError After patching
    # Caso não esteja nos segredos do Colab, pede input
#     pass # Script-patched # Script-patched: using env var


# ## 3. ChatModels vs LLMs
# 
# No LangChain, existem duas abstrações principais para modelos:
# 1. **LLMs**: Recebem uma string e retornam uma string (modelos de completude de texto mais antigos).
# 2. **ChatModels**: Recebem uma lista de mensagens (System, Human, AI) e retornam uma mensagem (modelos de chat modernos, como GPT-3.5 e GPT-4).
# 
# Vamos focar em **ChatModels**, pois são o padrão atual.



from langchain_google_genai import ChatGoogleGenerativeAI

# Inicializando o modelo
# temperature=0 deixa o modelo mais determinístico
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

llm


# ## 4. Invocando o Modelo
# 
# A forma mais simples de usar é chamar o método `.invoke()`. Podemos passar uma string simples, que será convertida automaticamente para uma mensagem de usuário.



response = llm.invoke("Quem foi o primeiro homem a pisar na lua?")
print(response.content)


# ## 5. Tipos de Mensagens
# 
# Para ter mais controle, usamos tipos de mensagens:
# - `SystemMessage`: Define o comportamento ou persona do sistema.
# - `HumanMessage`: A entrada do usuário.
# - `AIMessage`: A resposta do modelo (usada em históricos).



from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="Você é um assistente sarcástico e engraçado."),
    HumanMessage(content="Quanto é 2 + 2?")
]

response = llm.invoke(messages)
print(response.content)


# ## Conclusão
# 
# Neste notebook, aprendemos:
# 1. Instalar o LangChain.
# 2. Autenticar com a OpenAI.
# 3. Inicializar um `ChatOpenAI`.
# 4. Enviar prompts simples e estruturados com mensagens.
# 
# No próximo notebook, veremos como usar **Prompt Templates** para tornar nossos inputs dinâmicos.
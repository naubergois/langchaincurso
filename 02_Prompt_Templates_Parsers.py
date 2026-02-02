#!/usr/bin/env python
# coding: utf-8

# # 02. Prompt Templates e Output Parsers
# 
# Agora que sabemos chamar os modelos, precisamos estruturar melhor nossos prompts e processar as respostas. Usaremos **Prompt Templates** e **Output Parsers**, e introduziremos a sintaxe LCEL (LangChain Expression Language).
# 
# **Objetivos:**
# - Criar templates de prompt dinâmicos.
# - Usar parsers para limpar a saída.
# - Criar nossa primeira Chain usando o operador `|`.



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

# !pip install -qU langchain langchain-openai langchain-community python-dotenv # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    pass # Script-patched
except:
    pass # Script-patched




from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# ## 1. Prompt Templates
# 
# Em vez de concatenar strings manualmente (`"Traduza " + texto + " para inglês"`), usamos `PromptTemplate`. Isso ajuda a organizar variáveis e permite reutilização.



from langchain_core.prompts import ChatPromptTemplate

# Criando um template a partir de mensagens
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor profissional. Traduza o texto a seguir para {idioma}."),
    ("user", "{texto}")
])

# Podemos ver como fica o prompt formatado
prompt_val = prompt_template.invoke({"idioma": "Francês", "texto": "O gato está na mesa."})
print(prompt_val)


# ## 2. Output Parsers
# 
# A resposta do modelo é um objeto `AIMessage`. Frequentemente queremos apenas o texto (string). O `StrOutputParser` extrai o conteúdo da mensagem.



from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()


# ## 3. LCEL: LangChain Expression Language
# 
# É aqui que a mágica acontece. O LangChain moderno usa o operador "pipe" (`|`) para conectar componentes.
# 
# Fluxo: `Prompt -> Modelo -> Parser`



# Criando a chain
chain = prompt_template | llm | parser

# Executando a chain
# Passamos um dicionário com as variáveis definidas no prompt_template
resultado = chain.invoke({"idioma": "Espanhol", "texto": "Eu gosto de programar em Python."})

print(resultado)


# ## 4. Exemplo Prático: Gerador de Nomes de Empresas
# 
# Vamos criar uma chain que sugere nomes de empresas com base em um produto.



name_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um consultor de branding criativo."),
    ("user", "Sugira 3 nomes criativos para uma empresa que fabrica {produto}.")
])

name_chain = name_prompt | llm | parser

print(name_chain.invoke({"produto": "tênis de corrida feitos de material reciclado"}))


# ## Conclusão
# 
# Neste notebook, vimos como:
# 1. Criar prompts com variáveis usando `ChatPromptTemplate`.
# 2. Limpar a saída (extrair texto) usando `StrOutputParser`.
# 3. Encadeá-los usando o pipe `|` (LCEL).
# 
# No próximo notebook, aprenderemos a adicionar **Memória** às nossas conversas.
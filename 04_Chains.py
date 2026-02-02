#!/usr/bin/env python
# coding: utf-8

# # 04. Chains e Sequências
# 
# Já vimos chains simples com `|`. Agora vamos criar fluxos mais complexos, onde a saída de uma chain serve de entrada para outra, e execução paralela.
# 
# **Objetivos:**
# - Criar chains sequenciais.
# - Usar `RunnableParallel` para executar tarefas ao mesmo tempo.



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
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# ## 1. Chain Sequencial
# 
# Imagine que queremos:
# 1. Gerar uma sinopse de um filme dado o título.
# 2. Escrever uma crítica baseada nessa sinopse de filme.
# 
# Isso são duas chains conectadas.



# Chain 1: Sinopse
prompt_sinopse = ChatPromptTemplate.from_template("Escreva uma sinopse breve para um filme chamado {titulo}.")
chain_sinopse = prompt_sinopse | llm | StrOutputParser()

# Chain 2: Crítica
# Nota: o input dessa chain será a sinopse gerada anteriormente
prompt_critica = ChatPromptTemplate.from_template("Escreva uma crítica de cinema para a seguinte sinopse: {sinopse}.")
chain_critica = prompt_critica | llm | StrOutputParser()

# Encadeando tudo
# Usamos um dicionário lambda ou chain pura se o input bater
# Aqui, a chain_sinopse retorna uma string. Precisamos passá-la como 'sinopse' para a chain_critica.
from langchain_core.runnables import RunnablePassthrough

chain_completa = (
    {"sinopse": chain_sinopse} 
    | chain_critica
)

print(chain_completa.invoke({"titulo": "As Aventuras do Programador Python"}))


# ## 2. Execução Paralela (`RunnableParallel`)
# 
# Às vezes queremos rodar duas coisas ao mesmo tempo com o mesmo input. Ex: Dado um tema, escrever um poema E uma piada.



from langchain_core.runnables import RunnableParallel

chain_poema = ChatPromptTemplate.from_template("Escreva um poema curto sobre {tema}.") | llm | StrOutputParser()
chain_piada = ChatPromptTemplate.from_template("Escreva uma piada sobre {tema}.") | llm | StrOutputParser()

mapa_combinado = RunnableParallel(poema=chain_poema, piada=chain_piada)

resultado = mapa_combinado.invoke({"tema": "Inteligência Artificial"})

print("=== POEMA ===")
print(resultado['poema'])
print("\n=== PIADA ===")
print(resultado['piada'])


# ## Conclusão
# 
# Vimos como compor chains sequencialmente e paralelamente.
# 
# No próximo notebook, começaremos a construir nosso sistema RAG (Retrieval Augmented Generation), aprendendo a carregar e processar documentos.
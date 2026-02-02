#!/usr/bin/env python
# coding: utf-8

# # 05. RAG Parte 1: Document Loaders e Text Splitters
# 
# Para que o LLM responda sobre dados que ele não conhece (dados privados), usamos RAG (Retrieval Augmented Generation). O primeiro passo é o **ETL** (Extract, Transform, Load): extrair o texto de fontes e dividi-lo em pedaços menores (chunks).
# 
# **Objetivos:**
# - Carregar dados de uma URL (`WebBaseLoader`).
# - Dividir o texto em partes gerenciáveis (`RecursiveCharacterTextSplitter`).



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

# !pip install -qU langchain langchain-community beautifulsoup4 # Script-patched


# ## 1. Carregando Documentos (Loaders)
# 
# Existem loaders para PDF, CSV, TXT, Notion, Youtube, etc. Vamos usar o `WebBaseLoader` para pegar o conteúdo de uma página web.



from langchain_community.document_loaders import WebBaseLoader

# Vamos carregar um artigo do blog do LangChain, por exemplo
loader = WebBaseLoader("https://python.langchain.com/docs/get_started/introduction")

docs = loader.load()

print(f"Número de documentos carregados: {len(docs)}")
print(f"Tamanho do conteúdo: {len(docs[0].page_content)} caracteres")
print(docs[0].page_content[:500]) # Primeiros 500 caracteres


# ## 2. Dividindo o Texto (Splitters)
# 
# Modelos têm limite de tokens. Além disso, para buscar informação, é melhor ter pedaços pequenos e específicos do que um texto gigante. O `RecursiveCharacterTextSplitter` é o mais comum, pois tenta quebrar em parágrafos e frases.



from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Tamanho alvo de cada pedaço
    chunk_overlap=200     # Sobreposição para manter contexto nas bordas
)

splits = text_splitter.split_documents(docs)

print(f"Foram criados {len(splits)} pedaços (chunks).")
print(f"Conteúdo do primeiro chunk:\n{splits[0].page_content}")


# ## Conclusão
# 
# Agora temos nossos documentos processados e prontos para serem indexados.
# 
# No próximo notebook, vamos transformar esses chunks em vetores (Embeddings) e salvá-los em um Vector Store.
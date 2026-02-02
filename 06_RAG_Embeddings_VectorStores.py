#!/usr/bin/env python
# coding: utf-8

# # 06. RAG Parte 2: Embeddings e Vector Stores
# 
# Com os textos divididos, precisamos transformá-los em números (vetores) para que possamos fazer busca semântica (por significado, não por palavra-chave exata).
# 
# **Objetivos:**
# - Entender o que são Embeddings.
# - Criar um Vector Store (FAISS) para armazenar os vetores.
# - Fazer uma busca de similaridade.



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

# !pip install -qU langchain langchain-openai langchain-community faiss-cpu python-dotenv # Script-patched




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


# ## 1. Prep: Recriando os Chunks
# 
# Vamos repetir rapidamente o passo anterior para ter os dados.



from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Carregando docs pequenos para exemplo
urls = [
    "https://lilianweng.github.io/posts/2023-06-23-agent/",
]

loader = WebBaseLoader(urls)
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)


# ## 2. Embeddings
# 
# Modelo de Embedding converte texto em um vetor de números (ex: lista de 1536 floats).



from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings()


# ## 3. Vector Store (FAISS)
# 
# O FAISS (Facebook AI Similarity Search) é uma biblioteca eficiente para busca de similaridade. Vamos indexar nossos chunks.



from langchain_community.vectorstores import FAISS

# Cria o índice vetorial
vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

# Podemos consultar o índice
retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) # k=2 retorna os 2 mais similares


# ## 4. Busca de Similaridade
# 
# Vamos ver se ele encontra trechos relevantes sobre "Tool use".



docs = vectorstore.similarity_search("What are autonomous agents?")

for doc in docs:
    print(f"--- CONTEÚDO (len={len(doc.page_content)}) ---")
    print(doc.page_content[:300] + "...")
    print("\n")


# ## Conclusão
# 
# Criamos nosso "banco de dados" de conhecimento vetorial.
# 
# No próximo notebook, vamos juntar tudo: pegar a pergunta do usuário, buscar no FAISS, e passar para o LLM responder (RAG completo).
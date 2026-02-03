#!/usr/bin/env python
# coding: utf-8

# # 05. RAG Parte 1: Document Loaders e Text Splitters
# 
# Para que o LLM responda sobre dados que ele não conhece (dados privados), usamos RAG (Retrieval Augmented Generation). O primeiro passo é o **ETL** (Extract, Transform, Load): extrair o texto de fontes e dividi-lo em pedaços menores (chunks).
# 
# **Objetivos:**
# - Carregar dados de uma URL (`WebBaseLoader`).
# - Dividir o texto em partes gerenciáveis (`RecursiveCharacterTextSplitter`).

# # Explicação Detalhada do Assunto
# 
# # 05. RAG Parte 1: Document Loaders e Text Splitters
# 
# Bem-vindo ao primeiro passo na construção de aplicações poderosas com RAG (Retrieval Augmented Generation)! Neste notebook, vamos mergulhar no processo fundamental de preparação dos seus dados para que um LLM (Large Language Model) possa acessá-los e utilizá-los para gerar respostas informativas e relevantes.
# 
# **Resumo Executivo:**
# 
# Este notebook é dedicado ao processo de ETL (Extract, Transform, Load) aplicado a documentos para uso em sistemas RAG. Abordaremos como carregar documentos de diversas fontes usando LangChain Document Loaders e como dividir esses documentos em chunks menores e mais gerenciáveis usando Text Splitters.
# 
# **Conceitos Chave:**
# 
# *   **RAG (Retrieval Augmented Generation):** Uma técnica que combina a capacidade de um LLM de gerar texto com a capacidade de buscar informações relevantes de uma base de dados externa. Isso permite que o LLM responda a perguntas sobre dados que não fazem parte de seu conhecimento prévio.
# *   **ETL (Extract, Transform, Load):** Um processo padrão em ciência de dados que envolve extrair dados de uma ou mais fontes, transformar esses dados para torná-los utilizáveis e, finalmente, carregar os dados transformados em um sistema de destino. No contexto de RAG, o ETL se refere à preparação dos documentos para serem indexados e utilizados pelo LLM.
# *   **Document Loaders:** Ferramentas do LangChain que permitem carregar documentos de diversas fontes, como PDFs, websites, arquivos CSV, etc.
# *   **Text Splitters:** Ferramentas do LangChain que dividem um texto longo em pedaços menores (chunks) para facilitar a indexação e a busca de informações relevantes. A divisão em chunks ajuda a otimizar o uso de tokens e a melhorar a precisão da busca.
# 
# **Objetivos de Aprendizado:**
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Utilizar `Document Loaders` do LangChain para carregar dados de diferentes fontes (ex: web pages).
# *   Empregar `Text Splitters` do LangChain para dividir documentos longos em chunks menores e mais adequados para RAG.
# *   Compreender a importância do tamanho do chunk e do overlap para um bom funcionamento do RAG.
# *   Preparar seus documentos para o próximo passo do processo RAG: a criação de embeddings e a indexação em um vector store.
# 
# **Importância no Ecossistema LangChain:**
# 
# A etapa de carregamento e divisão de documentos é absolutamente crucial para o sucesso de qualquer aplicação RAG. Sem dados bem preparados, o LLM não conseguirá acessar as informações relevantes e gerar respostas precisas. Dominar o uso de Document Loaders e Text Splitters é, portanto, um passo fundamental para se tornar um especialista em LangChain e IA Generativa.
# 
# Vamos começar a construir juntos!
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
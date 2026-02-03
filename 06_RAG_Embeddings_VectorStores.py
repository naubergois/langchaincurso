#!/usr/bin/env python
# coding: utf-8



# Instalação do pymongo para registro de exceções
# !pip install pymongo # Script-patched




# Handler global para capturar exceções e salvar no MongoDB
import sys
import traceback
from datetime import datetime
from pymongo import MongoClient

# Configuração do MongoDB (ajuste o URI conforme necessário)
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "notebooks"
COLLECTION_NAME = "exceptions"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def excecao_para_mongo(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    doc = {
        "timestamp": datetime.utcnow(),
        "type": str(exc_type),
        "value": str(exc_value),
        "traceback": tb_str,
        "notebook": "06_RAG_Embeddings_VectorStores.ipynb"
    }
    collection.insert_one(doc)
    print(f"Exceção registrada no MongoDB: {exc_type} - {exc_value}")

sys.excepthook = excecao_para_mongo




# Instalação dos pacotes necessários para Colab
# !pip install python-dotenv langchain langchain-community langchain-text-splitters langchain-google-genai faiss-cpu bs4 # Script-patched




# Configuração da chave de API do Google Generative AI\nimport os\nfrom dotenv import load_dotenv\nimport sys\n# Carrega .env do local ou de pastas comuns\nfor p in ['.', '..', 'scripts', '../scripts']:\n    path = os.path.join(p, '.env')\n    if os.path.exists(path):\n        load_dotenv(path)\n        break\nif os.getenv('GOOGLE_API_KEY'):\n    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')


# # 06. RAG Parte 2: Embeddings e Vector Stores
# 
# Com os textos divididos, precisamos transformá-los em números (vetores) para que possamos fazer busca semântica (por significado, não por palavra-chave exata).
# 
# **Objetivos:**
# - Entender o que são Embeddings.
# - Criar um Vector Store (FAISS) para armazenar os vetores.
# - Fazer uma busca de similaridade.

# # Explicação Detalhada do Assunto
# 
# # 06. RAG Parte 2: Embeddings e Vector Stores
# 
# Bem-vindo ao segundo notebook da nossa jornada em Retrieval Augmented Generation (RAG)! Neste notebook, mergulharemos no coração do RAG, explorando como transformar texto bruto em representações numéricas significativas, que possibilitam a busca semântica eficiente. Preparar-se para dar vida aos seus dados!
# 
# ## Resumo Executivo
# 
# Este notebook demonstra o processo essencial de criação de um "banco de dados" de conhecimento vetorial. Partindo de textos divididos em chunks, aprenderemos como usar embeddings para representá-los como vetores e, em seguida, como indexá-los em um Vector Store (FAISS) para realizar buscas de similaridade semântica. O objetivo final é construir uma base sólida para o nosso sistema RAG, permitindo que ele encontre informações relevantes com base no significado, e não apenas em palavras-chave.
# 
# ## Conceitos Chave
# 
# Para entender completamente o que faremos, vamos revisar alguns conceitos importantes:
# 
# *   **Embeddings:** Um modelo de embedding converte texto em um vetor de números (uma lista de floats, por exemplo). Esse vetor representa o significado semântico do texto, permitindo que textos com significados semelhantes tenham vetores próximos no espaço vetorial.
# *   **Vector Store:** Um banco de dados especializado para armazenar e indexar vetores (embeddings). Ele permite buscas rápidas e eficientes por vetores similares, o que é crucial para encontrar os chunks de texto mais relevantes para uma determinada consulta. FAISS (Facebook AI Similarity Search) é uma biblioteca popular para construir Vector Stores.
# *   **Busca de Similaridade:** O processo de encontrar os vetores mais próximos (mais similares) a um determinado vetor de consulta dentro de um Vector Store. Isso nos permite encontrar os chunks de texto que são semanticamente mais relacionados à pergunta do usuário.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Transformar documentos de texto em embeddings usando um modelo como o `GoogleGenerativeAIEmbeddings`.
# *   Criar um Vector Store (usando FAISS) para indexar seus embeddings.
# *   Realizar buscas de similaridade em seu Vector Store para encontrar chunks de texto relevantes.
# *   Entender o papel fundamental dos embeddings e Vector Stores na arquitetura RAG.
# 
# ## Importância no Ecossistema LangChain
# 
# Este notebook é crucial porque estabelece a base para a funcionalidade de busca do nosso sistema RAG. A capacidade de encontrar informações relevantes de forma eficiente é o que permite ao LLM gerar respostas informativas e contextualmente apropriadas. Sem embeddings e Vector Stores, estaríamos limitados à busca por palavras-chave, o que frequentemente resulta em resultados irrelevantes ou incompletos. Ao dominar essas técnicas, você estará preparado para construir sistemas RAG poderosos e eficazes com LangChain.
# 
# Vamos começar a transformar texto em conhecimento acionável!
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
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

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

# Substitua 'SUA_CHAVE_API' pela sua chave do Google Generative AI
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY", "SUA_CHAVE_API"))


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

# 

# 

# 

# 

# 

# 
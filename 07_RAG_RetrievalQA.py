#!/usr/bin/env python
# coding: utf-8

# # 07. RAG Parte 3: RetrievalQA
# 
# Agora vamos juntar as peças: Docs -> Split -> Vector Store -> Retriever -> LLM -> Resposta.
# 
# **Objetivos:**
# - Criar uma `create_retrieval_chain` para responder perguntas baseadas nos documentos.



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


# ## 1. Setup Rápido (Load, Split, Index)
# 
# Recriando o índice para usar aqui.



from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Load
loader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")
docs = loader.load()

# 2. Split
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# 3. Index
vectorstore = FAISS.from_documents(splits, GoogleGenerativeAIEmbeddings())
retriever = vectorstore.as_retriever()


# ## 2. Criando a Chain de RAG
# 
# Usaremos `create_stuff_documents_chain` (que insere os docs no prompt) e `create_retrieval_chain` (que gerencia a busca).



from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Prompt do sistema que receberá o contexto
system_prompt = (
    "Você é um assistente para tarefas de perguntas e respostas. "
    "Use os seguintes pedaços de contexto recuperado para responder à pergunta. "
    "Se você não souber a resposta, diga que não sabe. "
    "Use no máximo três frases e mantenha a resposta concisa."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

# Chain que combina documentos no prompt
question_answer_chain = create_stuff_documents_chain(llm, prompt)

# Chain final que recupera docs e passa para a chain acima
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


# ## 3. Testando
# 
# Vamos fazer uma pergunta sobre o artigo.



response = rag_chain.invoke({"input": "What is Task Decomposition?"})

print(response["answer"])


# ## 4. Inspecionando a Fonte
# 
# Podemos ver quais documentos foram usados para gerar a resposta.



for i, doc in enumerate(response["context"]):
    print(f"Documento {i}: {doc.page_content[:100]}...")


# ## Conclusão
# 
# Temos um sistema de RAG funcional! Ele recupera informação relevante e responde de forma fundamentada.
# 
# No próximo notebook, vamos sair do padrão "pergunta-resposta" e entrar no mundo dos **Agentes**, que podem usar ferramentas para agir.
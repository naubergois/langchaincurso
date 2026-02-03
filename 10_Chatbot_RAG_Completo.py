#!/usr/bin/env python
# coding: utf-8

# # 10. Projeto Final: Chatbot com RAG
# 
# Chegamos ao final! Vamos consolidar tudo o que aprendemos criando um Chatbot estilo "ChatPDF". O usuário fará upload de um PDF e poderá conversar sobre ele.
# 
# **Componentes:**
# - Upload de arquivo.
# - PyPDFLoader.
# - Text Splitting & Embeddings.
# - Retrieval Chain.
# - Loop de Chat interativo.
# - Memória de Conversa.

# # Explicação Detalhada do Assunto
# 
# # 10. Projeto Final: Chatbot com RAG
# 
# Bem-vindo ao décimo e último notebook desta série! Aqui, vamos consolidar todo o conhecimento que você adquiriu ao longo do curso criando um chatbot completo, similar ao "ChatPDF". Prepare-se para construir uma aplicação interativa que permite aos usuários fazer upload de um arquivo PDF e conversar com ele, obtendo respostas precisas e relevantes.
# 
# ## Resumo Executivo
# 
# Este notebook é o culminar de tudo o que aprendemos sobre LangChain e IA Generativa. Vamos desenvolver um chatbot que utiliza a técnica de Recuperação Aumentada de Geração (RAG) para responder a perguntas sobre um documento PDF fornecido pelo usuário. Este projeto prático demonstra a aplicação real de conceitos como loaders, splitters, embeddings, vector stores, chains e memória.
# 
# ## Conceitos Chave
# 
# Para construir nosso chatbot, utilizaremos os seguintes conceitos:
# 
# *   **Chains:** Sequências de operações que combinam diferentes componentes do LangChain para realizar uma tarefa específica, como processar uma pergunta e gerar uma resposta.
# *   **RAG (Retrieval-Augmented Generation):** Uma técnica que combina a capacidade de recuperação de informações relevantes de um documento (Retrieval) com a capacidade de gerar texto coerente e informativo (Generation). Isso permite que o chatbot responda a perguntas com base no conteúdo do PDF, em vez de apenas em seu próprio conhecimento pré-existente.
# *   **Memória:** A capacidade do chatbot de lembrar conversas anteriores, permitindo que ele entenda o contexto e responda de forma mais coerente e relevante. Usaremos `create_history_aware_retriever` para reformular a pergunta com base no histórico.
# *   **Loaders:** Componentes que carregam dados de diversas fontes, como arquivos PDF.
# *   **Splitters:** Componentes que dividem documentos grandes em partes menores para facilitar o processamento.
# *   **Embeddings:** Representações numéricas de texto que capturam o significado semântico das palavras e frases.
# *   **Vector Stores:** Bancos de dados que armazenam embeddings para permitir a busca eficiente de informações relevantes.
# 
# ## Objetivos de Aprendizado
# 
# Ao completar este notebook, você será capaz de:
# 
# *   Construir um chatbot funcional que utiliza a técnica de RAG.
# *   Implementar a funcionalidade de upload de arquivos PDF.
# *   Processar documentos PDF, dividindo-os em partes menores e gerando embeddings.
# *   Armazenar embeddings em um vector store.
# *   Criar chains que combinam a recuperação de informações com a geração de respostas.
# *   Implementar a memória para manter o contexto da conversa.
# *   Interagir com o chatbot e obter respostas relevantes sobre o conteúdo do PDF.
# 
# ## Importância no Ecossistema LangChain
# 
# Este projeto demonstra a aplicação prática de muitos dos conceitos fundamentais do LangChain. A capacidade de construir chatbots que podem conversar sobre documentos específicos é extremamente valiosa em diversas áreas, como suporte ao cliente, educação, pesquisa e muito mais. Dominar essas técnicas o colocará em uma posição vantajosa para desenvolver soluções de IA Generativa inovadoras e eficazes.
# 
# Vamos começar!
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

# !pip install -qU langchain langchain-openai langchain-community faiss-cpu pypdf python-dotenv # Script-patched




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


# ## 1. Upload do PDF
# 
# Usaremos a funcionalidade do Colab para upload.



try:
    from google.colab import files

    print("Faça upload do seu PDF:")
    uploaded = files.upload()
    filename = next(iter(uploaded))
    print(f"Arquivo {filename} carregado.")
except ImportError:
    print("Google Colab not detected. Using local file.")
    # Fallback for local execution
#     filename = os.getenv("GOOGLE_API_KEY") # Script-patched: using env var from .env


# ## 2. Processamento (ETL)
# 
# Loader -> Splitter -> VectorStore.



from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Loader
loader = PyPDFLoader("sample.pdf")
docs = loader.load()

# Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)

# Index
vectorstore = FAISS.from_documents(splits, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
retriever = vectorstore.as_retriever()


# ## 3. Configurando a Chain com Histórico
# 
# Vamos usar `create_history_aware_retriever` para reformular a pergunta com base no histórico antes de buscar, garantindo que o chat flua bem.



from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

### 1. Contextualize Question ###
# Reformula a pergunta para incluir o contexto do histórico
contextualize_q_system_prompt = (
    "Dada uma conversa e a última pergunta do usuário, "
    "se ela referir-se ao contexto anterior, formule uma nova pergunta autônoma "
    "que seja compreensível sem o histórico. Não responda à pergunta, "
    "apenas reformule-a se necessário, caso contrário retorne-a como está."
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

### 2. Answer Question ###
# Responde à pergunta usando os docs recuperados
qa_system_prompt = (
    "Você é um assistente útil para tarefas de perguntas e respostas. "
    "Use os seguintes pedaços de contexto recuperado para responder à pergunta. "
    "Se você não souber a resposta, diga que não sabe. "
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

### 3. State Management ###
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


# ## 4. Chat Loop
# 
# Vamos conversar!



session_id = "minha_sessao"

print("Bot: Olá! Pergunte qualquer coisa sobre o documento. Digite 'sair' para encerrar.")

while True:
    pass # Script-patched: ensure non-empty block
#     user_input = os.getenv("GOOGLE_API_KEY") # Script-patched: using env var from .env
    user_input = "sair"
    if user_input.lower() in ["sair", "quit", "exit"]:
        print("Bot: Até mais!")
        break
    
    response = conversational_rag_chain.invoke(
        {"input": user_input},
        config={"configurable": {"session_id": session_id}},
    )
    
    print(f"Bot: {response['answer']}\n")


# ## Conclusão do Curso
# 
# Parabéns! Você completou os 10 exemplos práticos de LangChain.
# 
# **Resumo do que aprendemos:**
# 1. Chamar Modelos (LLMs e ChatModels).
# 2. Usar Prompt Templates e Output Parsers.
# 3. Adicionar Memória.
# 4. Criar Chains Sequenciais e Paralelas.
# 5. Carregar Documentos (ETL).
# 6. Criar Embeddings e Vector Stores.
# 7. Construir sistemas de RAG.
# 8. Usar Agentes com Ferramentas prontas.
# 9. Criar Ferramentas Customizadas.
# 10. Integrar tudo em uma aplicação completa.
# 
# Continue explorando a documentação oficial para recursos mais avançados como LangGraph e LangServe!
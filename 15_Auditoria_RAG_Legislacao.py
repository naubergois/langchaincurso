#!/usr/bin/env python
# coding: utf-8

# # 15. Auditoria: RAG em Legislação (Lei das Estatais/Licitações)
# 
# Auditores precisam consultar leis constantemente. Um chatbot especialista em uma lei específica economiza tempo de pesquisa.
# 
# **Objetivo:** Criar um RAG sobre um texto legal (ex: Lei 13.303 - Lei das Estatais ou 14.133 - Nova Lei de Licitações).
# *Nota: Usaremos um texto de exemplo curto para simular a lei no Colab.*

# # Explicação Detalhada do Assunto
# 
# # 15. Auditoria: RAG em Legislação (Lei das Estatais/Licitações)
# 
# Auditores precisam consultar leis constantemente. Um chatbot especialista em uma lei específica economiza tempo de pesquisa. Este notebook demonstra como construir um sistema de Recuperação Aumentada de Geração (RAG) focado na legislação, especificamente utilizando a Lei nº 13.303 (Lei das Estatais) como exemplo. O objetivo é criar um assistente virtual capaz de responder a perguntas complexas sobre a lei, fornecendo respostas precisas e fundamentadas diretamente no texto legal.
# 
# ## Resumo Executivo
# 
# Este notebook explora a aplicação de técnicas de RAG (Retrieval-Augmented Generation) para a criação de um sistema de consulta jurídica inteligente. Demonstraremos como carregar, indexar e consultar a Lei das Estatais (Lei nº 13.303) utilizando LangChain e modelos de linguagem generativos. O foco é simular um cenário real onde auditores e profissionais jurídicos precisam acessar informações específicas dentro de um grande volume de texto legal de forma rápida e precisa. Ao final, você terá um protótipo funcional capaz de responder a perguntas sobre a lei, citando as fontes relevantes.
# 
# ## Conceitos Chave
# 
# Para entender completamente o que faremos, é importante conhecer alguns conceitos fundamentais:
# 
# *   **RAG (Retrieval-Augmented Generation):** Uma técnica que combina a capacidade de busca (retrieval) em uma base de conhecimento com a habilidade de geração de texto de um modelo de linguagem. Em vez de depender apenas do conhecimento pré-existente do modelo, o RAG permite que ele consulte informações externas relevantes antes de gerar uma resposta, resultando em respostas mais precisas e contextualizadas.
# *   **Chains (Cadeias):** Em LangChain, Chains são sequências de chamadas a componentes, como modelos de linguagem, prompts e outros Chains. Elas permitem criar fluxos de trabalho complexos, como o pipeline de RAG que construiremos neste notebook.
# *   **Text Splitter (Divisor de Texto):** Um componente que divide um texto longo em partes menores (chunks) para facilitar a indexação e a busca. Diferentes estratégias de divisão podem ser utilizadas, como divisão por caracteres, sentenças ou parágrafos.
# *   **Embeddings (Incorporações):** Representações vetoriais de palavras ou frases que capturam seu significado semântico. Embeddings permitem comparar a similaridade entre diferentes textos e encontrar os trechos mais relevantes para uma determinada consulta.
# *   **Vector Store (Banco de Dados Vetorial):** Um banco de dados otimizado para armazenar e buscar embeddings. Ele permite encontrar os trechos de texto mais similares a uma consulta com alta eficiência.
# *   **Prompts:** Instruções textuais fornecidas ao modelo de linguagem para guiá-lo na geração da resposta desejada. Um bom prompt é crucial para obter respostas precisas e relevantes.
# 
# ## Objetivos de Aprendizado
# 
# Ao completar este notebook, você será capaz de:
# 
# *   Carregar e pré-processar um texto legal usando LangChain.
# *   Dividir o texto em chunks utilizando diferentes estratégias de Text Splitter.
# *   Gerar embeddings para os chunks de texto utilizando um modelo de embeddings.
# *   Armazenar os embeddings em um Vector Store.
# *   Implementar um pipeline de RAG para consultar o texto legal.
# *   Avaliar a qualidade das respostas geradas pelo sistema.
# *   Adaptar o pipeline para diferentes textos legais.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de construir sistemas de RAG é fundamental no ecossistema LangChain. Ela permite que você aproveite o poder dos modelos de linguagem generativos para resolver problemas complexos em diversos domínios, desde a consulta de documentos legais até a criação de chatbots especializados em áreas específicas do conhecimento. Este notebook fornece um exemplo prático e detalhado de como construir um sistema de RAG funcional, que pode ser adaptado e expandido para atender às suas necessidades. Dominar essas técnicas abrirá um leque de possibilidades para a criação de aplicações inteligentes e úteis.
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
load_dotenv()

# !pip install -qU langchain langchain-openai langchain-community faiss-cpu # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    pass # Script-patched: ensure non-empty block
#     os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") # Script-patched: using env var from .env
except:
    pass # Added to avoid IndentationError After patching
#     os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") # Script-patched: using env var from .env


# ## 1. Carregando a "Lei"
# 
# Vamos usar alguns artigos chave da Lei 13.303 (Estatais) como exemplo.



lei_texto = """
LEI Nº 13.303, DE 30 DE JUNHO DE 2016

Art. 1º Esta Lei dispõe sobre o estatuto jurídico da empresa pública, da sociedade de economia mista e de suas subsidiárias, abrangendo toda e qualquer empresa pública e sociedade de economia mista da União, dos Estados, do Distrito Federal e dos Municípios.

Art. 28. Os contratos com terceiros destinados à prestação de serviços às empresas públicas e às sociedades de economia mista, inclusive de engenharia e de publicidade, à aquisição e à locação de bens, à alienação de bens e ativos integrantes do respectivo patrimônio ou à execução de obras a serem integradas a esse patrimônio, bem como à implementação de ônus real sobre tais bens, serão precedidos de licitação nos termos desta Lei, ressalvadas as hipóteses previstas nos arts. 29 e 30.

Art. 29. É dispensável a realização de licitação por empresas públicas e sociedades de economia mista:
I - para obras e serviços de engenharia de valor até R$ 100.000,00 (cem mil reais);
II - para outros serviços e compras de valor até R$ 50.000,00 (cinquenta mil reais);
"""


# ## 2. RAG Pipeline
# 
# Text Splitter -> Embeddings -> VectorStore.



from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

# Dividindo por caracteres (idealmente dividiríamos por Artigo, mas manteremos simples)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.create_documents([lei_texto])

vectorstore = FAISS.from_documents(splits, GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
retriever = vectorstore.as_retriever()


# ## 3. Consultoria Jurídica via RAG
# 
# Perguntaremos sobre limites de dispensa de licitação.



from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

system_prompt = (
    "Você é um advogado especialista em Direito Administrativo. "
    "Use os artigos de lei fornecidos para responder à dúvida do auditor. "
    "Cite o número do artigo que embasa sua resposta."
    "\n\n"
    "{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Pergunta prática
response = rag_chain.invoke({"input": "Qual o valor limite para comprar materiais de escritório sem licitação?"})

print(response["answer"])


# ## Conclusão
# 
# O modelo responde com base no Art. 29, inciso II, citando o valor correto (50 mil) e a fonte, evitando alucinações comuns em modelos genéricos.
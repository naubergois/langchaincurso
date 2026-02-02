#!/usr/bin/env python
# coding: utf-8

# # 03. Memória
# 
# Os modelos de linguagem são "stateless" (sem estado), ou seja, eles não lembram da conversa passada por padrão. Para criar chatbots, precisamos gerenciar o histórico da conversa e passá-lo a cada nova interação. O LangChain facilita isso.
# 
# **Objetivos:**
# - Entender como funciona a memória no LCEL.
# - Usar `RunnableWithMessageHistory` para gerenciar histórico automaticamente.



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


# ## 1. O Problema da Falta de Memória
# 
# Vamos ver como o modelo se comporta sem memória.



chain = ChatPromptTemplate.from_template("{input}") | llm | StrOutputParser()

# Primeira interação
print(chain.invoke({"input": "Oi, meu nome é Nauber."}))

# Segunda interação
print(chain.invoke({"input": "Qual é o meu nome?"}))


# Ele provavlemente dirá que não sabe, pois cada chamada é independente.

# ## 2. Adicionando Histórico com `RunnableWithMessageHistory`
# 
# Essa é a forma recomendada no LCEL moderno. Precisamos de uma classe para armazenar o histórico (aqui usaremos `ChatMessageHistory` em memória, mas poderia ser num banco de dados).



from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Dicionário para guardar os históricos de diferentes sessões (session_ids)
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# Agora criamos o prompt aceitando um `MessagesPlaceholder` para injetar o histórico.



from langchain_core.prompts import MessagesPlaceholder

prompt_with_history = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente prestativo."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

runnable = prompt_with_history | llm | StrOutputParser()

# Envolvemos a chain original com a capacidade de histórico
with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)


# ## 3. Testando a Memória
# 
# Agora vamos conversar passando um `session_id`.



# Configurando o ID da sessão
config = {"configurable": {"session_id": "sessao_do_nauber"}}

response1 = with_message_history.invoke(
    {"input": "Oi, meu nome é Nauber."}, 
    config=config
)
print(f"Resposta 1: {response1}")

response2 = with_message_history.invoke(
    {"input": "Qual é o meu nome?"}, 
    config=config
)
print(f"Resposta 2: {response2}")


# ## 4. Chats Diferentes (Session IDs)
# 
# Se mudarmos o `session_id`, ele não lembrará.



config_novo = {"configurable": {"session_id": "sessao_nova"}}

response3 = with_message_history.invoke(
    {"input": "Qual é o meu nome?"}, 
    config=config_novo
)
print(f"Resposta 3 (Sessão Nova): {response3}")


# ## Conclusão
# 
# Neste notebook, aprendemos a manter o estado da conversa usando `RunnableWithMessageHistory` e `ChatMessageHistory`.
# 
# No próximo notebook, vamos explorar **Chains** mais complexas.
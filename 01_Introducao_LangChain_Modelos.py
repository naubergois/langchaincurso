#!/usr/bin/env python
# coding: utf-8

# # 01. Introdução ao LangChain e Modelos
# 
# Bem-vindo ao curso prático de LangChain! Neste primeiro notebook, vamos configurar nosso ambiente e fazer nossas primeiras chamadas a modelos de linguagem (LLMs) e ChatModels.
# 
# **Objetivos:**
# - Instalar as bibliotecas necessárias.
# - Configurar chaves de API.
# - Diferenciar LLMs de ChatModels.
# - Fazer a primeira chamada ("Hello World").

# # Explicação Detalhada do Assunto
# 
# # 01. Introdução ao LangChain e Modelos
# 
# Bem-vindo ao fascinante mundo do LangChain! Este notebook marca o início da sua jornada prática neste poderoso framework, projetado para simplificar e potencializar o desenvolvimento de aplicações baseadas em Inteligência Artificial Generativa. Prepare-se para dar os primeiros passos na construção de soluções inteligentes e inovadoras!
# 
# ## Resumo Executivo
# 
# Neste primeiro notebook, focaremos na configuração do seu ambiente de desenvolvimento e na realização das suas primeiras interações com modelos de linguagem (LLMs) utilizando o LangChain. Aprenderemos a instalar as bibliotecas necessárias, configurar a chave de API para acessar os modelos da OpenAI e explorar as diferentes formas de interagir com os modelos, desde prompts simples até a utilização de mensagens estruturadas.
# 
# ## Conceitos Chave
# 
# Para uma melhor compreensão, vamos definir alguns conceitos-chave que serão abordados ao longo do curso:
# 
# *   **LLMs (Large Language Models):** Modelos de linguagem de grande escala, como os da OpenAI, capazes de gerar texto, traduzir idiomas, responder a perguntas e muito mais.
# *   **ChatModels:** Uma abstração do LangChain para modelos de linguagem projetados especificamente para conversação. Diferente dos LLMs tradicionais, os ChatModels são otimizados para lidar com múltiplos turnos de diálogo e manter o contexto da conversa.
# *   **Prompts:** As instruções ou perguntas que fornecemos aos modelos de linguagem para obter uma resposta. A qualidade do prompt é crucial para obter os resultados desejados.
# *   **Chains:** Sequências de chamadas a LLMs ou outras utilidades. Permitem criar fluxos de trabalho complexos e automatizar tarefas. (Será abordado em notebooks futuros)
# *   **RAG (Retrieval Augmented Generation):** Uma técnica que combina a capacidade de geração de texto dos LLMs com a capacidade de buscar informações relevantes em uma base de conhecimento externa. (Será abordado em notebooks futuros)
# *   **Memória:** A capacidade de um modelo de linguagem de "lembrar" informações de interações passadas. Permite criar conversas mais contextuais e personalizadas. (Será abordado em notebooks futuros)
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# 1.  Instalar o LangChain e suas dependências.
# 2.  Configurar a autenticação para acessar os modelos da OpenAI.
# 3.  Inicializar um `ChatModel` do LangChain.
# 4.  Enviar prompts simples e estruturados aos modelos de linguagem.
# 5.  Compreender a diferença entre `LLMs` e `ChatModels` e quando usar cada um.
# 6.  Utilizar diferentes tipos de mensagens (SystemMessage, HumanMessage, AIMessage) para controlar o comportamento do modelo.
# 
# ## Importância no Ecossistema LangChain
# 
# Este notebook é fundamental porque estabelece as bases para todo o seu aprendizado no LangChain. Dominar a instalação, configuração e interação básica com os modelos de linguagem é essencial para construir aplicações mais complexas e aproveitar ao máximo o potencial do framework. Sem esses fundamentos, será difícil progredir para tópicos mais avançados, como Chains, RAG e Memória.
# 
# Então, prepare-se para mergulhar no mundo do LangChain e desbloquear o poder da IA Generativa! Vamos começar!
# 
# ---
# 

# ## 1. Instalação
# 
# Vamos instalar o `langchain`, `langchain-openai` e outras dependências comuns.



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

# !pip install -qU langchain langchain-openai langchain-community python-dotenv # Script-patched: assumed installed


# ## 2. Configuração da API Key
# 
# Para usar os modelos da OpenAI, precisamos de uma API Key. No Colab, a forma mais segura é usar o `google.colab.userdata` se você tiver salvado a chave nos segredos do Colab, ou usar `getpass` para digitar na hora.



import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    pass # Script-patched
except:
    pass # Added to avoid IndentationError After patching
    # Caso não esteja nos segredos do Colab, pede input
#     pass # Script-patched # Script-patched: using env var


# ## 3. ChatModels vs LLMs
# 
# No LangChain, existem duas abstrações principais para modelos:
# 1. **LLMs**: Recebem uma string e retornam uma string (modelos de completude de texto mais antigos).
# 2. **ChatModels**: Recebem uma lista de mensagens (System, Human, AI) e retornam uma mensagem (modelos de chat modernos, como GPT-3.5 e GPT-4).
# 
# Vamos focar em **ChatModels**, pois são o padrão atual.



from langchain_google_genai import ChatGoogleGenerativeAI

# Inicializando o modelo
# temperature=0 deixa o modelo mais determinístico
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

llm


# ## 4. Invocando o Modelo
# 
# A forma mais simples de usar é chamar o método `.invoke()`. Podemos passar uma string simples, que será convertida automaticamente para uma mensagem de usuário.



response = llm.invoke("Quem foi o primeiro homem a pisar na lua?")
print(response.content)


# ## 5. Tipos de Mensagens
# 
# Para ter mais controle, usamos tipos de mensagens:
# - `SystemMessage`: Define o comportamento ou persona do sistema.
# - `HumanMessage`: A entrada do usuário.
# - `AIMessage`: A resposta do modelo (usada em históricos).



from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="Você é um assistente sarcástico e engraçado."),
    HumanMessage(content="Quanto é 2 + 2?")
]

response = llm.invoke(messages)
print(response.content)


# ## Conclusão
# 
# Neste notebook, aprendemos:
# 1. Instalar o LangChain.
# 2. Autenticar com a OpenAI.
# 3. Inicializar um `ChatOpenAI`.
# 4. Enviar prompts simples e estruturados com mensagens.
# 
# No próximo notebook, veremos como usar **Prompt Templates** para tornar nossos inputs dinâmicos.
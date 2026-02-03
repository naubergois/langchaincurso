#!/usr/bin/env python
# coding: utf-8

# # 02. Prompt Templates e Output Parsers
# 
# Agora que sabemos chamar os modelos, precisamos estruturar melhor nossos prompts e processar as respostas. Usaremos **Prompt Templates** e **Output Parsers**, e introduziremos a sintaxe LCEL (LangChain Expression Language).
# 
# **Objetivos:**
# - Criar templates de prompt dinâmicos.
# - Usar parsers para limpar a saída.
# - Criar nossa primeira Chain usando o operador `|`.

# # Explicação Detalhada do Assunto
# 
# # 02. Prompt Templates e Output Parsers
# 
# Bem-vindo ao segundo notebook da nossa jornada LangChain! Agora que já aprendemos a interagir com modelos de linguagem, é hora de aprimorar a forma como estruturamos nossas solicitações (prompts) e como processamos as respostas geradas. Neste notebook, vamos explorar dois conceitos cruciais: **Prompt Templates** e **Output Parsers**.
# 
# ## Resumo Executivo
# 
# Este notebook é um guia prático para dominar a arte de criar prompts eficazes e de extrair informações valiosas das respostas dos modelos de linguagem. Através de exemplos claros e concisos, você aprenderá a utilizar `Prompt Templates` para organizar e reutilizar seus prompts, e `Output Parsers` para formatar as respostas dos modelos de acordo com suas necessidades.
# 
# ## Conceitos Chave
# 
# *   **Prompt Templates**: São modelos que permitem definir a estrutura de um prompt, incluindo variáveis que podem ser preenchidas dinamicamente. Em vez de construir prompts manualmente concatenando strings, você usará templates para criar prompts mais organizados, legíveis e reutilizáveis.
# *   **Output Parsers**: São ferramentas que permitem processar e formatar as respostas dos modelos de linguagem. Eles extraem o conteúdo relevante da resposta, convertem-no para o formato desejado (por exemplo, string, lista, JSON) e garantem que as informações sejam apresentadas de forma consistente.
# *   **LCEL (LangChain Expression Language)**: É a linguagem de expressão do LangChain que permite conectar diferentes componentes (como Prompt Templates, modelos de linguagem e Output Parsers) em um fluxo de trabalho coeso, utilizando o operador "pipe" (`|`).
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Criar e utilizar `Prompt Templates` para estruturar seus prompts de forma eficiente.
# *   Aplicar `Output Parsers` para extrair e formatar as respostas dos modelos de linguagem.
# *   Construir `Chains` utilizando a `LangChain Expression Language (LCEL)` para conectar diferentes componentes em um fluxo de trabalho.
# *   Desenvolver aplicações práticas que utilizam prompts dinâmicos e processamento de saída.
# 
# ## Importância no Ecossistema LangChain
# 
# Dominar `Prompt Templates` e `Output Parsers` é fundamental para construir aplicações LangChain robustas e escaláveis. Eles permitem que você:
# 
# *   **Otimize a interação com os modelos de linguagem**: Prompts bem estruturados levam a respostas mais precisas e relevantes.
# *   **Automatize o processamento de informações**: Extrair e formatar as respostas dos modelos de forma consistente economiza tempo e evita erros.
# *   **Crie fluxos de trabalho complexos**: Conectar diferentes componentes com a LCEL permite construir aplicações sofisticadas que resolvem problemas reais.
# 
# Prepare-se para elevar suas habilidades LangChain a um novo patamar! Vamos começar a explorar o poder dos Prompt Templates e Output Parsers.
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

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")


# ## 1. Prompt Templates
# 
# Em vez de concatenar strings manualmente (`"Traduza " + texto + " para inglês"`), usamos `PromptTemplate`. Isso ajuda a organizar variáveis e permite reutilização.



from langchain_core.prompts import ChatPromptTemplate

# Criando um template a partir de mensagens
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor profissional. Traduza o texto a seguir para {idioma}."),
    ("user", "{texto}")
])

# Podemos ver como fica o prompt formatado
prompt_val = prompt_template.invoke({"idioma": "Francês", "texto": "O gato está na mesa."})
print(prompt_val)


# ## 2. Output Parsers
# 
# A resposta do modelo é um objeto `AIMessage`. Frequentemente queremos apenas o texto (string). O `StrOutputParser` extrai o conteúdo da mensagem.



from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()


# ## 3. LCEL: LangChain Expression Language
# 
# É aqui que a mágica acontece. O LangChain moderno usa o operador "pipe" (`|`) para conectar componentes.
# 
# Fluxo: `Prompt -> Modelo -> Parser`



# Criando a chain
chain = prompt_template | llm | parser

# Executando a chain
# Passamos um dicionário com as variáveis definidas no prompt_template
resultado = chain.invoke({"idioma": "Espanhol", "texto": "Eu gosto de programar em Python."})

print(resultado)


# ## 4. Exemplo Prático: Gerador de Nomes de Empresas
# 
# Vamos criar uma chain que sugere nomes de empresas com base em um produto.



name_prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um consultor de branding criativo."),
    ("user", "Sugira 3 nomes criativos para uma empresa que fabrica {produto}.")
])

name_chain = name_prompt | llm | parser

print(name_chain.invoke({"produto": "tênis de corrida feitos de material reciclado"}))


# ## Conclusão
# 
# Neste notebook, vimos como:
# 1. Criar prompts com variáveis usando `ChatPromptTemplate`.
# 2. Limpar a saída (extrair texto) usando `StrOutputParser`.
# 3. Encadeá-los usando o pipe `|` (LCEL).
# 
# No próximo notebook, aprenderemos a adicionar **Memória** às nossas conversas.
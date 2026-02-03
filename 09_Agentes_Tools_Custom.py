#!/usr/bin/env python
# coding: utf-8

# # 09. Agentes com Tools Customizadas
# 
# Muitas vezes precisamos que o agente interaja com nossas próprias APIs, cálculos ou sistemas internos. Para isso, criamos ferramentas customizadas.
# 
# **Objetivos:**
# - Criar uma função Python e decorá-la com `@tool`.
# - Definir tipos e descrições para que o modelo entenda como usar.
# - Passar a tool para o agente.

# # Explicação Detalhada do Assunto
# 
# # 09. Agentes com Tools Customizadas
# 
# Bem-vindo(a) ao notebook sobre a criação de Agentes com Tools Customizadas! Este é um passo crucial para desbloquear o verdadeiro potencial da IA Generativa, permitindo que seus agentes interajam com seus próprios sistemas e dados de maneira inteligente e automatizada.
# 
# ## Resumo Executivo
# 
# Neste notebook, vamos nos aprofundar na criação de ferramentas personalizadas (custom tools) para agentes LangChain. A capacidade de integrar seus próprios sistemas, APIs e lógicas de negócio aos agentes é o que os torna verdadeiramente poderosos e adaptáveis às suas necessidades específicas. Aprenderemos a definir, implementar e integrar essas ferramentas para que nossos agentes possam realizar tarefas complexas que vão além das capacidades nativas dos LLMs.
# 
# ## Conceitos Chave
# 
# *   **Agentes:** Entidades que usam um modelo de linguagem para determinar quais ações tomar. Eles são o "cérebro" por trás da automação inteligente.
# *   **Tools (Ferramentas):** Funções ou APIs que os agentes podem usar para interagir com o mundo exterior. São os "braços" do agente, permitindo que ele execute tarefas.
# *   **Custom Tools:** Ferramentas que você define e implementa para atender às necessidades específicas do seu projeto. Elas permitem que você conecte o agente aos seus próprios sistemas, APIs e dados.
# *   **LLM (Large Language Model):** O modelo de linguagem que impulsiona o agente. Ele é responsável por entender as instruções do usuário, planejar as ações a serem tomadas e gerar as respostas.
# *   **LangChain:** Framework que facilita a criação de aplicações usando LLMs.
# 
# ## Objetivos de Aprendizado
# 
# Ao completar este notebook, você será capaz de:
# 
# *   Definir e implementar suas próprias ferramentas customizadas para agentes LangChain.
# *   Integrar essas ferramentas em um agente para que ele possa usá-las de forma inteligente.
# *   Entender como o agente decide quando e como usar cada ferramenta.
# *   Criar agentes que podem interagir com seus próprios sistemas, APIs e dados.
# *   Expandir as capacidades dos agentes para além das limitações nativas dos LLMs.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de criar ferramentas customizadas é fundamental no ecossistema LangChain porque permite que você:
# 
# *   **Personalize seus agentes:** Adapte os agentes às suas necessidades específicas, em vez de depender apenas das ferramentas pré-definidas.
# *   **Integre com seus sistemas:** Conecte os agentes aos seus bancos de dados, APIs, sistemas internos e outros recursos.
# *   **Automatize tarefas complexas:** Crie agentes que podem realizar tarefas que seriam impossíveis ou muito difíceis de fazer manualmente.
# *   **Desbloqueie o verdadeiro potencial da IA Generativa:** Vá além das demonstrações e crie aplicações de IA que resolvem problemas reais e agregam valor ao seu negócio.
# 
# Prepare-se para mergulhar no mundo da criação de ferramentas customizadas e elevar seus agentes LangChain a um novo patamar!
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

# !pip install -qU langchain langchain-openai langchain-community # Script-patched




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


# ## 1. Criando uma Custom Tool
# 
# Vamos criar uma "ferramenta de cálculo" fictícia, ou algo que o LLM não saiba fazer bem nativamente, como contar letras em uma palavra invertida (só um exemplo bobo para provar que ele chama a função).



from langchain_core.tools import tool

@tool
def multiplica(a: int, b: int) -> int:
    """Multiplica dois números inteiros."""
    return a * b

@tool
def conta_caracteres(texto: str) -> int:
    """Conta o número de caracteres em um texto."""
    return len(texto)

tools = [multiplica, conta_caracteres]


# ## 2. Configurando o Agente
# 
# Mesmo processo do notebook anterior, mas agora com nossas tools.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente matemático e analítico."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ## 3. Testando
# 
# Vamos pedir algo que precise das ferramentas.



# Aqui ele deve chamar a tool 'multiplica' em vez de tentar calcular internamente (embora LLMs saibam multiplicar, estamos forçando o uso da tool pelo prompt/contexto ou apenas testando)
agent_executor.invoke({"input": "Quanto é 1234 vezes 5678?"})




agent_executor.invoke({"input": "Quantas letras tem a palavra 'paralelepípedo'?"})


# ## Conclusão
# 
# Criar ferramentas customizadas é o superpoder dos Agentes. Você pode integrar com Banco de Dados, APIs REST, Slack, E-mail, etc.
# 
# No próximo e último notebook, faremos um **Projeto Final**: Um Chatbot que conversa com seu PDF.
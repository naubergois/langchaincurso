#!/usr/bin/env python
# coding: utf-8

# # 27. ReAct: A Abordagem LangChain
# 
# No notebook anterior, construímos um agente "na mão". Agora vamos ver como o LangChain abstrai isso para facilitar a construção de sistemas complexos.
# 
# **Objetivos:**
# 1. Usar ferramentas pré-construídas do LangChain.
# 2. Criar um Agente ReAct padrão (`create_react_agent`).
# 3. **Engenharia de Prompt Reversa:** Baixar e analisar o prompt padrão do LangChain Hub para entender as boas práticas embutidas nele.
# 
# ---



### INJECTION START ###
import os
from dotenv import load_dotenv
import sys
for p in ['.', '..', 'scripts', '../scripts']:
    path = os.path.join(p, '.env')
    if os.path.exists(path):
        load_dotenv(path)
        break
if os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
    os.environ['OPENAI_API_KEY'] = os.getenv('GOOGLE_API_KEY')
### INJECTION END ###

# !pip install -q langchain langchain-openai langchainhub google-search-results numexpr # Script-patched




import os
import getpass

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
    
# Opcional: SerpAPI para busca real no Google
# if "SERPAPI_API_KEY" not in os.environ:
    pass # Script-patched: ensure non-empty block
#     os.environ["SERPAPI_API_KEY"] = os.getenv("GOOGLE_API_KEY"): ")


# ## 1. Definindo Ferramentas no LangChain
# 
# O LangChain facilita a criação de ferramentas robustas usando o decorador `@tool`. O docstring da função é **CRUCIAL**, pois ele é injetado no prompt para o LLM entender quando usar a ferramenta.



from langchain.agents import tool

@tool
def get_word_length(word: str) -> int:
    """Retorna o tamanho (número de caracteres) de uma palavra."""
    return len(word)

@tool
def get_weather(city: str) -> str:
    """Retorna a previsão do tempo para uma cidade específica. Use para perguntas sobre clima."""
    # Mock para exemplo
    return f"O tempo em {city} está ensolarado, 25 graus."

tools = [get_word_length, get_weather]


# ## 2. O Prompt do LangChain Hub
# 
# Ao invés de escrevermos o prompt template gigante (como no notebook anterior), vamos puxar o padrão da comunidade testado em batalha.
# 
# O prompt `hwchase17/react` é o padrão *gold standard*.



from langchain import hub

# Baixando o prompt
prompt = hub.pull("hwchase17/react")

# Vamos imprimir para estudar sua estrutura
print("--- Prompt Template Padrão ---")
print(prompt.template)


# ### Análise do Prompt
# 
# Note que ele possui variáveis como `{tools}`, `{tool_names}` e `{agent_scratchpad}`.
# 
# - **{tools}**: Descrições das ferramentas (automático).
# - **{tool_names}**: Lista de nomes (automático).
# - **{agent_scratchpad}**: Onde o histórico de Pensamento/Ação/Observação é injetado para manter o contexto.

# ## 3. Criando o Agente (Agent Construction)
# 
# Vamos usar `create_react_agent`. O "Executor" é quem roda o loop (o equivalente ao nosso `run_agent_step` manual).



from langchain.agents import AgentExecutor, create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Criação do Agente (a "mente" que decide o que fazer baseada no prompt)
agent = create_react_agent(llm, tools, prompt)

# Criação do Executor (o "corpo" que executa as ações e loops)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# handle_parsing_errors=True é uma técnica de engenharia de prompt automática!
# Se o LLM falhar no formato, o LangChain injeta uma instrução de erro no prompt pedindo para corrigir.


# ## 4. Rodando o Agente
# 
# Vamos ver o `verbose=True` em ação, mostrando o pensamento.



query = "Quantas letras tem a palavra 'paralelepípedo' e como está o tempo no Rio de Janeiro?"

response = agent_executor.invoke({"input": query})

print(f"\nResposta: {response['output']}")


# ## 5. Exercício Prático: Modificando o Prompt Base
# 
# E se quisermos que o agente sempre responda como um pirata?
# Podemos injetar instruções no topo do prompt.



# Modificando o template manualmente
prompt.template = "VOCÊ É UM PIRATA REBULIÇO! SEMPRE RESPONDA COMO TAL.\n\n" + prompt.template

agent_pirata = create_react_agent(llm, tools, prompt)
executor_pirata = AgentExecutor(agent=agent_pirata, tools=tools, verbose=True)

executor_pirata.invoke({"input": "Como está o tempo em São Paulo?"})

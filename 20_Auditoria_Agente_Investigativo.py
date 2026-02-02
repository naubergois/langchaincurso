#!/usr/bin/env python
# coding: utf-8

# # 20. Auditoria: Agente Investigativo
# 
# O auge da automação é um Agente que cruza dados autônomamente. Vamos criar um agente que recebe um nome de fornecedor e usa "tools" (simuladas aqui) para verificar CNPJ, lista de sócios e busca de notícias negativas.
# 
# **Objetivo:** Investigar a reputação de um Fornecedor.



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

import os
from dotenv import load_dotenv
load_dotenv()

# !pip install -qU langchain langchain-openai langchain-community duckduckgo-search # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
except:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. Criando Tools de Investigação
# 
# Simularemos APIs de Receita Federal e Compliance.



from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()

@tool
def consulta_receita_federal(cnpj: str) -> dict:
    """Consulta situação cadastral do CNPJ na Receita Federal."""
    # Simulação
    if cnpj == "00.000.000/0001-00":
        return {"status": "ATIVA", "socios": ["João Laranja", "Maria Silva"]}
    elif cnpj == "99.999.999/0001-99":
        return {"status": "BAIXADA", "socios": ["Carlos Golpe"]}
    return {"status": "DESCONHECIDO"}

@tool
def lista_negra_compliance(nome: str) -> bool:
    """Verifica se o nome consta na lista negra de terrorismo ou lavagem de dinheiro."""
    lista = ["Carlos Golpe", "Empresa Fantasma LTDA"]
    return nome in lista

tools = [consulta_receita_federal, lista_negra_compliance, search]


# ## 2. Configurando o Agente
# 
# O agente decidirá quais tools chamar.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um Agente de Investigação de Fraudes. Use as ferramentas para levantar a ficha completa do alvo."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# ## 3. Investigando
# 
# Vamos investigar um CNPJ suspeito.



agent_executor.invoke({
    "input": "Investigue a empresa CNPJ 99.999.999/0001-99. Verifique o status na receita, quem são os sócios e se algum sócio está na lista negra."
})


# ## Conclusão Final do Curso
# 
# Neste módulo de Auditoria, vimos como a IA Generativa pode:
# 1. Analisar conformidade em massa.
# 2. Ler e extrair dados de contratos.
# 3. Resumir relatórios.
# 4. Classificar riscos.
# 5. Atuar como consultor jurídico.
# 6. Comparar normas.
# 7. Detectar anomalias em e-mails.
# 8. Agenciar investigações complexas.
# 
# Essas ferramentas não substituem o auditor, mas aumentam exponencialmente sua produtividade.
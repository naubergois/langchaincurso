#!/usr/bin/env python
# coding: utf-8

# # 20. Auditoria: Agente Investigativo
# 
# O auge da automação é um Agente que cruza dados autônomamente. Vamos criar um agente que recebe um nome de fornecedor e usa "tools" (simuladas aqui) para verificar CNPJ, lista de sócios e busca de notícias negativas.
# 
# **Objetivo:** Investigar a reputação de um Fornecedor.

# # Explicação Detalhada do Assunto
# 
# # 20. Auditoria: Agente Investigativo
# 
# Bem-vindo ao ápice da automação com LangChain! Neste notebook, exploraremos a criação de um Agente Investigativo, capaz de cruzar dados de forma autônoma para realizar auditorias e investigações. Vamos construir um sistema que, dado o nome de um fornecedor (ou CNPJ), utiliza "tools" (simuladas e reais) para verificar sua situação cadastral, identificar sócios e verificar a existência de irregularidades.
# 
# ## Resumo Executivo
# 
# Este notebook demonstra como construir um agente inteligente capaz de realizar investigações complexas, simulando um processo de auditoria. Utilizaremos LangChain para orquestrar a interação entre um modelo de linguagem (LLM) e diversas ferramentas (tools) para coletar e analisar informações sobre uma empresa. Ao final, você terá um protótipo funcional de um agente capaz de auxiliar em processos de due diligence e compliance.
# 
# ## Conceitos Chave
# 
# Para aproveitar ao máximo este notebook, é importante entender os seguintes conceitos:
# 
# *   **Agentes (Agents):** São sistemas que utilizam um LLM para determinar quais ações devem ser tomadas com base em uma entrada (input). Eles "pensam" sobre a tarefa, decidem qual ferramenta usar e executam essa ferramenta, repetindo o processo até atingir um objetivo.
# *   **Ferramentas (Tools):** São funções específicas que o agente pode usar para interagir com o mundo externo. Neste notebook, criaremos ferramentas simuladas para consulta de dados cadastrais e verificação de listas de restrição. Ferramentas reais podem incluir acesso a APIs de bancos de dados, sistemas de busca na web e outras fontes de informação.
# *   **LLM (Large Language Model):** O modelo de linguagem grande é o "cérebro" do agente. Ele recebe as informações, decide qual ferramenta usar e interpreta os resultados. Neste notebook, utilizaremos um modelo do Google AI.
# *   **Chains:** Sequências de chamadas a LLMs ou outras utilidades. Agentes são uma forma mais dinâmica de chains, onde a ordem das chamadas é determinada pelo LLM.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Criar ferramentas (tools) personalizadas para um agente LangChain.
# *   Configurar um agente LangChain para utilizar diversas ferramentas de forma inteligente.
# *   Utilizar o agente para investigar empresas e identificar possíveis irregularidades.
# *   Compreender o fluxo de trabalho de um agente investigativo e como ele pode ser aplicado em casos reais de auditoria e compliance.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de criar agentes inteligentes é um dos pilares do LangChain. Este notebook demonstra como usar agentes para automatizar tarefas complexas que antes exigiam intervenção humana significativa. Ao dominar a criação de agentes investigativos, você estará apto a construir soluções de ponta para auditoria, compliance, análise de risco e outras áreas que exigem a coleta e análise de grandes volumes de dados. Este é um passo crucial para desbloquear o potencial da IA Generativa em aplicações práticas e relevantes para o mundo real. Prepare-se para transformar a forma como as investigações são conduzidas!
# 
# ---
# 



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
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
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
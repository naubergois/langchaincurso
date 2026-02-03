#!/usr/bin/env python
# coding: utf-8

# # 29. Integrando LangChain com n8n (Webhook Client)
# 
# O **n8n** é uma ferramenta poderosa para conectar serviços (Slack, Google Sheets, Email, etc). Ao invés de reimplementar toda essa lógica em Python, podemos usar o LangChain apenas como o "Cérebro" e o n8n como os "Músculos".
# 
# **Objetivos:**
# 1. Entender como acionar workflows do n8n via Webhook (HTTP POST).
# 2. Criar uma **Tool** do LangChain que encapsula essa chamada.
# 3. Criar um Agente que decide *quando* chamar o n8n.
# 
# ---

# # Explicação Detalhada do Assunto
# 
# # Integrando LangChain com n8n: Automatizando Workflows com Webhooks
# 
# Bem-vindo(a) a este guia prático sobre como integrar o poder do LangChain com a versatilidade do n8n, uma ferramenta de automação de workflows robusta e flexível. Neste notebook, exploraremos como usar o n8n para expandir as capacidades do LangChain, conectando seus agentes e aplicações de IA a uma vasta gama de serviços e APIs.
# 
# ## Resumo Executivo
# 
# Este notebook demonstra como integrar o LangChain com o n8n, uma ferramenta de automação de workflows, utilizando webhooks. Em vez de reimplementar a lógica de conexão com diversos serviços (Slack, Google Sheets, Email, etc.) diretamente no seu código Python, você aprenderá a delegar essa tarefa ao n8n, criando workflows complexos e reutilizáveis. O objetivo é capacitar seus agentes LangChain a interagir com o mundo externo de forma eficiente e escalável.
# 
# ## Conceitos Chave
# 
# *   **n8n:** Uma plataforma de automação de workflows que permite conectar diferentes aplicativos e serviços sem a necessidade de código complexo.
# *   **Webhook:** Um mecanismo que permite que um aplicativo envie informações em tempo real para outro aplicativo sempre que um determinado evento acontece. No contexto deste notebook, o LangChain enviará dados para um workflow do n8n via webhook.
# *   **LangChain Tools:** Funções encapsuladas que permitem que um agente LangChain interaja com o mundo externo. Neste caso, criaremos uma Tool que envia dados para o n8n.
# *   **Agentes LangChain:** Entidades que utilizam um modelo de linguagem (LLM) para tomar decisões sobre quais ações executar com base em uma entrada (prompt). O agente utilizará a Tool criada para interagir com o n8n.
# *   **Pydantic BaseModel:** Utilizado para definir o schema dos dados que serão enviados para o n8n, garantindo que os dados estejam no formato esperado.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Compreender o conceito de webhooks e como eles funcionam no n8n.
# *   Criar um workflow simples no n8n que recebe dados via webhook.
# *   Definir um schema de dados usando Pydantic para garantir a integridade dos dados enviados para o n8n.
# *   Encapsular a interação com o n8n como uma Tool do LangChain.
# *   Utilizar um agente LangChain para chamar a Tool e enviar dados para o workflow do n8n.
# *   Adaptar este conhecimento para criar integrações mais complexas com outros serviços e APIs através do n8n.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de integrar o LangChain com ferramentas de automação como o n8n é fundamental para construir aplicações de IA generativa robustas e escaláveis. Ao abstrair a complexidade da integração com diferentes serviços para o n8n, você pode focar no desenvolvimento do seu agente e na lógica principal da sua aplicação. Além disso, essa abordagem permite reutilizar workflows do n8n em diferentes partes da sua aplicação LangChain, promovendo a modularidade e a manutenibilidade do seu código. Esta integração abre um leque de possibilidades para automatizar tarefas, integrar dados de diversas fontes e criar fluxos de trabalho inteligentes impulsionados pela IA generativa.
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

# !pip install -q langchain langchain-openai # Script-patched




import os
import getpass
import requests
import json

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. O Conceito de Webhook
# 
# No n8n, você cria um workflow que começa com um nó **Webhook**. Ele te dá uma URL (ex: `https://seu-n8n.com/webhook/test`).
# 
# Quando fazemos um POST para essa URL enviando JSON, o n8n recebe os dados e inicia o processo.



# URL de Exemplo (Substitua pela sua URL real do n8n)
# Se não tiver um n8n rodando, usaremos um mock para teste
N8N_WEBHOOK_URL = "https://postman-echo.com/post" # Mock que retorna o que enviamos

def trigger_n8n_workflow(data: dict):
    """Envia dados para o n8n."""
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Erro ao chamar n8n: {e}"

# Teste manual
print(trigger_n8n_workflow({"message": "Olá n8n!", "source": "Colab"}))


# ## 2. Encapsulando como Ferramenta LangChain
# 
# Agora vamos dar poder ao Agente. Imagine que temos um workflow no n8n que **Adiciona uma Linha no Google Sheets**.



from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

# 1. Definir Schema dos dados que o n8n espera para esse workflow específico
class AddSpreadsheetRowInput(BaseModel):
    nome: str = Field(description="Nome do cliente")
    email: str = Field(description="Email do cliente")
    interesse: str = Field(description="Resumo do interesse do cliente")

# 2. Função da Tool
def add_to_spreadsheet(nome: str, email: str, interesse: str) -> str:
    """Envia os dados para o n8n adicionar na planilha de Leads."""
    payload = {
        "action": "add_row",
        "data": {
            "nome": nome,
            "email": email,
            "interesse": interesse
        }
    }
    # Chamada real (simulada aqui)
    result = trigger_n8n_workflow(payload)
    return f"Comando enviado ao n8n. Resposta do servidor: {result}"

# 3. Criar a Tool
n8n_tool = StructuredTool.from_function(
    func=add_to_spreadsheet,
    name="AddLeadToSheets",
    description="Use esta ferramenta SEMPRE que precisar salvar um novo lead ou cliente na planilha.",
    args_schema=AddSpreadsheetRowInput
)


# ## 3. Agente em Ação
# 
# O Agente recebe um texto não estruturado (ex: email ou conversa) e decide estruturar e chamar o n8n.



from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, [n8n_tool], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[n8n_tool], verbose=True)

input_text = """
Recebi um contato de um tal de Carlos Silva.
O email dele é carlos.silva@exemplo.com e ele disse que queria comprar um seguro de vida.
"""

agent_executor.invoke({"input": f"Processe esse texto e salve se for relevante: {input_text}"})

#!/usr/bin/env python
# coding: utf-8

# # Introdução ao LangSmith
# 
# O LangSmith é uma plataforma para testar, depurar e avaliar aplicativos baseados em LLM.
# Neste notebook, vamos explorar os conceitos fundamentais:
# 1. **Tracing**: Como visualizar o fluxo de execução das suas chains.
# 2. **Datasets**: Como criar conjuntos de dados para testes.
# 3. **Avaliação**: Como rodar testes automatizados nos seus datasets.
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
    os.environ['OPENAI_API_KEY'] = os.getenv('GOOGLE_API_KEY')
### INJECTION END ###

import os
from dotenv import load_dotenv
load_dotenv()

get_ipython().run_line_magic('pip', 'install -qU langsmith langchain langchain-openai')




import os
import getpass

# LangSmith Config
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

if not os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("GOOGLE_API_KEY")

if not os.environ.get("LANGCHAIN_PROJECT"):
    os.environ["LANGCHAIN_PROJECT"] = "curso-langsmith-intro" # Nome do projeto no LangSmith

# GoogleGenerativeAI API Key
if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. Tracing Básico
# 
# O tracing já está ativo porque definimos `LANGCHAIN_TRACING_V2="true"`. Qualquer chamada feita com componentes do LangChain será registrada automaticamente.



from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Simples chamada, isso vai gerar um trace
response = llm.invoke("Explique o que é LangSmith em uma frase.")
print(response.content)


# Vá para [smith.langchain.com](https://smith.langchain.com) e verifique o projeto `curso-langsmith-intro`. Você deve ver o trace da execução acima.

# ## 2. Datasets
# 
# Datasets são coleções de exemplos (entradas e saídas esperadas) usados para testar e avaliar seu aplicativo.



from langsmith import Client

client = Client()

dataset_name = "Perguntas de Exemplo"

# Criar Dataset se não existir
if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(
        dataset_name=dataset_name,
        description="Um dataset de exemplo com perguntas e respostas."
    )
    
    # Adicionar exemplos
    client.create_examples(
        inputs=[
            {"pergunta": "Qual é a capital da França?"},
            {"pergunta": "Quanto é 2 + 2?"},
            {"pergunta": "Quem escreveu Dom Casmurro?"}
        ],
        outputs=[
            {"resposta": "Paris"},
            {"resposta": "4"},
            {"resposta": "Machado de Assis"}
        ],
        dataset_id=dataset.id
    )
    print("Dataset criado!")
else:
    print("Dataset já existe.")


# ## 3. Avaliação
# 
# Agora vamos usar o dataset criado para avaliar nosso modelo.



from langchain.smith import RunEvalConfig, run_on_dataset

# 1. Definir o que vamos testar (nosso "sistema")
# O sistema deve aceitar a entrada do dataset e produzir uma saída.

def meu_app(inputs):
    return llm.invoke(inputs["pergunta"]).content

# 2. Configurar Avaliadores
# Avaliadores "QA" verificam a precisão comparando com a resposta de referência (output do dataset)
eval_config = RunEvalConfig(
    evaluators=["qa"], # usa um LLM para julgar se a resposta bate com o gabarito
)

# 3. Rodar Avaliação
results = run_on_dataset(
    client=client,
    dataset_name=dataset_name,
    llm_or_chain_factory=meu_app,
    evaluation=eval_config,
)

print(results)


# Agora você pode visualizar os resultados da avaliação no painel do LangSmith.
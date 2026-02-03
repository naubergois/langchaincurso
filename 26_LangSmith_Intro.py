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

# # Explicação Detalhada do Assunto
# 
# # Introdução ao LangSmith
# 
# Bem-vindo ao fascinante mundo do LangSmith, a plataforma essencial para transformar seus aplicativos baseados em LLM de protótipos promissores em soluções robustas e confiáveis. Neste notebook, embarcaremos em uma jornada prática para desvendar os segredos do LangSmith e capacitá-lo a dominar o teste, a depuração e a avaliação de seus projetos de IA Generativa.
# 
# ## Resumo Executivo
# 
# Este notebook serve como um guia introdutório ao LangSmith, explorando seus conceitos fundamentais e demonstrando como utilizá-lo para aprimorar a qualidade e a confiabilidade de seus aplicativos de linguagem. Através de exemplos práticos, você aprenderá a rastrear execuções, criar datasets para testes e avaliar o desempenho de seus modelos.
# 
# ## Conceitos Chave
# 
# Antes de mergulharmos no código, é importante compreender alguns conceitos-chave que permeiam o LangSmith e o ecossistema LangChain:
# 
# *   **Tracing:** O tracing permite visualizar o fluxo de execução do seu aplicativo LangChain, desde a entrada até a saída final, revelando insights valiosos sobre o comportamento do seu modelo e identificando gargalos de desempenho. Pense nisso como um raio-x do seu aplicativo!
# *   **Datasets:** Datasets são coleções de exemplos cuidadosamente selecionados que representam os diferentes cenários que seu aplicativo precisa lidar. Eles são cruciais para testar a robustez e a precisão do seu modelo em uma variedade de situações.
# *   **Avaliação:** A avaliação é o processo de medir o desempenho do seu modelo em relação a um dataset, fornecendo métricas quantitativas e insights qualitativos que ajudam a identificar áreas de melhoria.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Configurar o LangSmith e ativar o tracing em seus aplicativos LangChain.
# *   Navegar na interface do LangSmith e interpretar os traces de execução.
# *   Criar datasets personalizados para testar e avaliar seus modelos.
# *   Executar avaliações automatizadas e analisar os resultados no painel do LangSmith.
# *   Compreender o papel do LangSmith no ciclo de vida de desenvolvimento de aplicativos de IA Generativa.
# 
# ## Importância no Ecossistema LangChain
# 
# O LangSmith é uma peça fundamental do ecossistema LangChain, preenchendo uma lacuna crítica no desenvolvimento de aplicativos baseados em LLM. Ao fornecer ferramentas poderosas para teste, depuração e avaliação, o LangSmith permite que você:
# 
# *   **Reduza o tempo de desenvolvimento:** Identifique e corrija erros mais rapidamente, acelerando o ciclo de desenvolvimento.
# *   **Melhore a qualidade do seu aplicativo:** Garanta que seu modelo funcione de forma confiável e precisa em uma variedade de cenários.
# *   **Aumente a confiança:** Valide o desempenho do seu modelo e tome decisões informadas sobre como otimizá-lo.
# 
# Prepare-se para dominar o LangSmith e elevar seus projetos de IA Generativa a um novo patamar! Vamos começar explorando o tracing básico.
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
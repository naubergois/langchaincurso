#!/usr/bin/env python
# coding: utf-8

# # 17. Auditoria: Geração de Checklists de Verificação
# 
# Ao iniciar uma auditoria em um processo novo, o auditor precisa criar um "Programa de Trabalho" (Checklist). LLMs podem gerar checklists baseados na descrição do processo e nas melhores práticas (COSO/ISO).
# 
# **Objetivo:** Gerar um checklist de auditoria para o processo de "Admissão de Funcionários".

# # Explicação Detalhada do Assunto
# 
# # 17. Auditoria: Geração de Checklists de Verificação
# 
# Bem-vindo a este notebook dedicado à aplicação de Large Language Models (LLMs) na auditoria, especificamente na geração automatizada de checklists de verificação. Em processos de auditoria, a criação de um programa de trabalho detalhado (checklist) é um passo crucial. Este notebook demonstra como podemos alavancar o poder dos LLMs para automatizar e otimizar essa etapa, tornando o processo mais eficiente e preciso.
# 
# ## Resumo Executivo
# 
# Neste notebook, exploraremos como utilizar a LangChain e modelos de linguagem generativa para criar checklists de auditoria. Abordaremos desde a definição do processo a ser auditado até a geração de prompts eficazes que extraiam os passos de verificação de riscos chave. Através de exemplos práticos, você aprenderá a adaptar e aplicar essa técnica em seus próprios projetos de auditoria.
# 
# ## Conceitos Chave
# 
# *   **LLMs (Large Language Models):** Modelos de linguagem de grande escala, como o Gemini, capazes de gerar texto coerente e relevante com base em um prompt. Usaremos suas capacidades para criar checklists de auditoria.
# *   **LangChain:** Uma framework poderosa que facilita a construção de aplicações utilizando LLMs. A LangChain nos permite orquestrar prompts, modelos e outras ferramentas de forma eficiente e modular.
# *   **Prompts:** Instruções específicas fornecidas ao LLM para direcionar sua resposta. A qualidade do prompt é crucial para obter um checklist de auditoria preciso e relevante.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Compreender o processo de geração de checklists de auditoria utilizando LLMs.
# *   Definir e descrever um processo de negócio para fins de auditoria.
# *   Criar prompts eficazes para extrair passos de verificação de riscos chave de um LLM.
# *   Interpretar e avaliar a qualidade das checklists geradas pelo modelo.
# *   Adaptar e aplicar esta técnica em diferentes contextos de auditoria.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de gerar checklists de auditoria automaticamente demonstra o potencial da LangChain para automatizar tarefas complexas e repetitivas. Ao integrar LLMs em processos de auditoria, podemos aumentar a eficiência, reduzir o risco de erros e liberar os auditores para se concentrarem em atividades de maior valor agregado, como análise e tomada de decisões. Este notebook ilustra um caso de uso prático e valioso da LangChain no mundo real, destacando seu papel como uma ferramenta essencial para profissionais de dados e desenvolvedores de IA.
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
load_dotenv()

# !pip install -qU langchain langchain-openai langchain-community # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    pass # Script-patched: ensure non-empty block
#     os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") # Script-patched: using env var from .env
except:
    pass # Added to avoid IndentationError After patching
#     os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") # Script-patched: using env var from .env


# ## 1. Descrição do Processo
# 
# Descrição breve de como funciona a Admissão.



processo_admissao = """
O RH recebe a requisição de vaga aprovada. O recrutador entrevista candidatos. Após seleção, o candidato envia documentos (RG, CPF, Carteira de Trabalho). O RH cadastra no sistema de folha e agenda o exame admissional. Após o exame apto, o contrato é assinado e o funcionário começa.
"""


# ## 2. Prompt Gerador de Checklist
# 
# Pediremos passos de verificação de riscos chave.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7) # Temp mais alta para criatividade

prompt = ChatPromptTemplate.from_template(
    """Você é um Auditor Sênior planejando uma auditoria.
    Com base na descrição do processo abaixo, crie um Checklist de Auditoria com 5 a 7 testes para validar a efetividade dos controles.
    
    Foque em riscos como: admissão fantasma, falta de documentação, erro de salário, falta de exame médico.
    
    PROCESSO:
    {processo}
    
    Formato de saída:
    - [ ] [O que verificar] (Risco coberto: X)
    """
)

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"processo": processo_admissao}))


# ## Conclusão
# 
# O modelo gera testes lógicos como "Verificar se existe requisição aprovada para cada admissão" e "Conferir se a data do exame admissional é anterior ao início do trabalho".
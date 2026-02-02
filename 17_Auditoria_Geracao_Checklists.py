#!/usr/bin/env python
# coding: utf-8

# # 17. Auditoria: Geração de Checklists de Verificação
# 
# Ao iniciar uma auditoria em um processo novo, o auditor precisa criar um "Programa de Trabalho" (Checklist). LLMs podem gerar checklists baseados na descrição do processo e nas melhores práticas (COSO/ISO).
# 
# **Objetivo:** Gerar um checklist de auditoria para o processo de "Admissão de Funcionários".



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
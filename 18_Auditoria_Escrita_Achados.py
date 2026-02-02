#!/usr/bin/env python
# coding: utf-8

# # 18. Auditoria: Escrita de Achados (Método 5Cs)
# 
# Auditores sabem identificar problemas, mas nem sempre escrevem de forma clara. O padrão global do IIA (Institute of Internal Auditors) são os 5 Cs: Condition, Criteria, Cause, Consequence, Corrective Action.
# 
# **Objetivo:** Transformar anotações rascunhadas em um achado formal.



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


# ## 1. O Rascunho (Input)
# 
# Notas de campo do auditor.



notas_auditor = """
Fui no estoque e vi que a porta fica aberta o dia todo. Qualquer um entra. Contei as caixas de iphone e faltavam 2. O guarda disse que as vezes sai pra almoçar e deixa sem chave. A norma diz que tem que trancar. Isso pode dar roubo.
"""


# ## 2. Prompt de Formatação
# 
# Instruindo o modelo a usar a estrutura formal.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """Você é um revisor de relatórios de auditoria.
    Reescreva as notas abaixo no formato padrão '5 Cs' (Critério, Condição, Causa, Consequência, Correção).
    Use linguagem formal e impessoal.
    
    NOTAS:
    {notas}
    """
)

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"notas": notas_auditor}))


# ## Conclusão
# 
# O LLM estrutura perfeitamente:
# - **Critério**: Norma de segurança física.
# - **Condição**: Porta destrancada e falta de 2 itens.
# - **Causa**: Falha na supervisão durante intervalo do guarda.
# - **Consequência**: Perda de ativos (roubo).
# - **Correção**: Implementar controle de acesso eletrônico ou escala de guardas.
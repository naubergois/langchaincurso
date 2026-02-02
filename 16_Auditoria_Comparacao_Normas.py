#!/usr/bin/env python
# coding: utf-8

# # 16. Auditoria: Comparação de Normas (Diff Semântico)
# 
# Normas internas mudam. Ferramentas de "diff" de texto mostram o que mudou letra por letra, mas não explicam o impacto. Um LLM pode ler a Versão A e a Versão B e explicar: "O prazo de pagamento aumentou de 30 para 45 dias".
# 
# **Objetivo:** Comparar duas versões de um parágrafo normativo.



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


# ## 1. As Duas Versões
# 
# Exemplo de mudança em política de Home Office.



versao_2022 = """
O colaborador poderá realizar Home Office até 2 (duas) vezes por semana, devendo alinhar com o gestor imediato com 24h de antecedência. A empresa fornecerá ajuda de custo de R$ 100,00 mensais para internet.
"""

versao_2023 = """
O regime de trabalho é híbrido. O colaborador deve comparecer ao escritório obrigatoriamente às terças e quintas. Nos demais dias, o trabalho remoto é livre. Foi extinta a ajuda de custo para internet, sendo incorporada ao salário base.
"""


# ## 2. Prompt de Comparação
# 
# Vamos pedir para listar as alterações de impacto.



from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """Compare as duas versões da norma abaixo e liste as principais mudanças práticas para o colaborador.
    Não se preocupe com mudanças de redação, apenas mudanças de regra/direito/dever.
    
    ### VERSÃO ANTIGA ###
    {v_antiga}
    
    ### VERSÃO NOVA ###
    {v_nova}
    
    Saída desejada:
    - Mudança 1
    - Mudança 2
    """
)

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"v_antiga": versao_2022, "v_nova": versao_2023}))


# ## Conclusão
# 
# O LLM identifica que a flexibilidade de dias mudou (agora dias fixos) e que a ajuda de custo foi removida/incorporada. Isso é muito mais útil que um diff colorido do Word.
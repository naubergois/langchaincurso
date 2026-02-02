#!/usr/bin/env python
# coding: utf-8

# # 14. Auditoria: Classificação Automática de Riscos
# 
# Um dos passos da auditoria é classificar os apontamentos conforme seu risco (Alto, Médio, Baixo) para priorizar correções. LLMs são excelentes classificadores zero-shot.
# 
# **Objetivo:** Classificar descrições de falhas de controle e gerar uma justificativa para a nota.



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


# ## 1. Definindo a Matriz de Riscos no Prompt
# 
# Instruímos o modelo sobre o que constitui cada nível de risco.



from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Schema de Saída
class ClassificacaoRisco(BaseModel):
    nivel: str = Field(description="Nível de risco: 'Alto', 'Médio' ou 'Baixo'")
    justificativa: str = Field(description="Explicação breve do porquê desse nível de risco")
    acao_sugerida: str = Field(description="Ação imediata recomendada")

structured_llm = llm.with_structured_output(ClassificacaoRisco)

sistema = """
Você é um especialista em Gestão de Riscos Corporativos.
Classifique o seguinte apontamento de auditoria interna conforme a matriz:
    pass # Script-patched: ensure non-empty block

- ALTO: Perda financeira significativa (> R$ 100k), fraude, violação legal grave (LGPD, Anticorrupção) ou risco de imagem.
- MÉDIO: Falha de processo repetitiva, perda financeira moderada (< R$ 100k) ou dados imprecisos.
- BAIXO: Erros pontuais, documentação faltante não crítica ou melhoria de eficiência.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", sistema),
    ("human", "Apontamento: {apontamento}")
]) | structured_llm


# ## 2. Testando com Casos Reais
# 
# Vamos passar alguns cenários para ver a classificação.



cenarios = [
    "O sistema de almoxarifado permite saída de mercadoria sem requisição aprovada. Identificada perda de estoque de R$ 500.000 no ano.",
    "Três relatórios de despesas de viagem de Junho/2023 estavam sem carimbo da recepção, mas com notas fiscais válidas.",
    "Identificamos um funcionário do Depto de Compras que é sócio de um fornecedor recém-contratado sem declaração de conflito de interesses."
]

for cenario in cenarios:
    print(f"--- CENÁRIO: {cenario[:60]}... ---")
    res = prompt.invoke({"apontamento": cenario})
    print(f"NÍVEL: {res.nivel}")
    print(f"JUSTIFICATIVA: {res.justificativa}")
    print(f"AÇÃO: {res.acao_sugerida}\n")


# ## 3. Tagging Chain (Opção Alternativa)
# 
# O LangChain também possui `create_tagging_chain` para casos simples onde queremos apenas categorizar (tags).

# ## Conclusão
# 
# Automatizar a classificação inicial ajuda a direcionar o foco dos auditores seniores para os problemas de Risco Alto.
#!/usr/bin/env python
# coding: utf-8

# # 13. Auditoria: Resumo de Relatórios Longos
# 
# Relatórios de auditoria podem ter centenas de páginas. Para a alta gestão, precisamos extrair apenas os "Pontos de Atenção" e "Recomendações". Quando o texto é maior que a janela de contexto do LLM, usamos técnicas como **Map-Reduce**.
# 
# **Objetivo:** Resumir um texto longo identificando principais riscos.



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


# ## 1. Carregando Texto Longo
# 
# Vamos simular um relatório longo (repetindo texto) para forçar o uso da chain de resumo.



texto_base = """
RELATÓRIO DE AUDITORIA INTERNA - ÁREA DE COMPRAS

1. INTRODUÇÃO
O objetivo desta auditoria foi avaliar os controles internos do ciclo de compras.

2. ACHADO: FALTA DE TRÊS COTAÇÕES
Identificamos que em 40% dos processos de compra acima de R$ 10.000, não houve a realização de três cotações conforme norma interna. Isso gera risco de sobrepreço.
Recomendação: Implementar trava no sistema SAP impedindo pedido de compra sem anexos de cotação.

3. ACHADO: APROVAÇÃO POR ALÇADA INCORRETA
O Diretor Financeiro aprovou compras de TI que deveriam ser aprovadas pelo CTO. Risco: Aquisição de tecnologia incompatível.
Recomendação: Revisar fluxo de workflow de aprovação.

4. ACHADO: CADASTRO DE FORNECEDORES
Fornecedores cadastrados sem documentação de Compliance. Risco: Contratação de empresas idôneas.
Recomendação: Bloquear pagamentos a fornecedores com cadastro incompleto.
"""

# Multiplicando para ficar "longo" (simulação)
docs_texto = [texto_base] * 3 


# ## 2. Preparando Documentos
# 
# Transformando strings em objetos `Document`.



from langchain_core.documents import Document

docs = [Document(page_content=t) for t in docs_texto]


# ## 3. Criando a Chain de Summarization (Map-Reduce)
# 
# O LangChain possuía `load_summarize_chain`, mas em LCEL moderno construímos manualmente ou usamos a chain pronta de `stuff` se couber no contexto. Como modelos modernos (GPT-4-Turbo, Gemini 1.5) têm contextos gigantes (128k+ tokens), muitas vezes não precisamos mais de Map-Reduce complexo. Vamos usar a abordagem `Stuff` (colocar tudo no prompt) que é mais comum hoje, mas estruturando o resumo.



from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """Você é um assistente executivo.
    
    Resuma os seguintes relatórios de auditoria em uma lista de bullet points contendo apenas os ACHADOS e as RECOMENDAÇÕES principais.
    Ignore textos introdutórios.
    
    RELATÓRIOS:
    {context}
    """
)

chain = create_stuff_documents_chain(llm, prompt)

resumo = chain.invoke({"context": docs})
print(resumo)


# ## Conclusão
# 
# Com poucas linhas, consolidamos informações repetitivas ou extensas em um sumário executivo direto ao ponto.
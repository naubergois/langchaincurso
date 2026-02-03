#!/usr/bin/env python
# coding: utf-8

# # 18. Auditoria: Escrita de Achados (Método 5Cs)
# 
# Auditores sabem identificar problemas, mas nem sempre escrevem de forma clara. O padrão global do IIA (Institute of Internal Auditors) são os 5 Cs: Condition, Criteria, Cause, Consequence, Corrective Action.
# 
# **Objetivo:** Transformar anotações rascunhadas em um achado formal.

# # Explicação Detalhada do Assunto
# 
# # 18. Auditoria: Escrita de Achados (Método 5Cs)
# 
# Bem-vindo a este notebook dedicado à arte de redigir achados de auditoria de forma clara, concisa e impactante! Auditores possuem a capacidade crítica de identificar problemas, mas a comunicação eficaz desses achados é igualmente crucial para gerar mudanças positivas. Este notebook explora como a IA Generativa, e especificamente o LangChain, podem auxiliar na estruturação e apresentação de achados de auditoria, seguindo o padrão global dos 5 Cs do IIA (Institute of Internal Auditors).
# 
# **Resumo Executivo:**
# 
# Neste notebook, você aprenderá a utilizar o LangChain para transformar notas de campo de auditoria em relatórios concisos e profissionais, aderentes aos princípios dos 5 Cs (Critério, Condição, Causa, Consequência e Correção). Demonstraremos como prompts bem elaborados podem instruir modelos de linguagem a estruturar informações complexas de forma clara e persuasiva.
# 
# **Conceitos Chave:**
# 
# *   **LangChain:** Um framework para desenvolver aplicações impulsionadas por modelos de linguagem. Ele facilita a criação de pipelines complexos, permitindo a integração de LLMs com diversas fontes de dados e ferramentas.
# *   **LLMs (Large Language Models):** Modelos de linguagem treinados em grandes volumes de texto, capazes de gerar texto, traduzir idiomas, escrever diferentes tipos de conteúdo criativo e responder às suas perguntas de forma informativa. Neste contexto, usaremos o LLM para formatar e refinar os achados de auditoria.
# *   **Prompts:** Instruções fornecidas ao LLM para guiar a geração de texto. A qualidade do prompt é crucial para obter resultados precisos e relevantes. Aprenderemos a criar prompts eficazes para a redação de achados de auditoria.
# *   **Chains:** Sequências de chamadas a LLMs ou outras utilidades. O LangChain permite criar chains complexas para automatizar tarefas repetitivas.
# *   **Output Parsers:** Ferramentas que estruturam a saída dos LLMs em formatos específicos, como strings, JSON ou objetos Python.
# 
# **Objetivos de Aprendizado:**
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Entender a importância da clareza e concisão na redação de achados de auditoria.
# *   Aplicar os princípios dos 5 Cs na estruturação de achados de auditoria.
# *   Utilizar o LangChain para automatizar a formatação de achados de auditoria.
# *   Criar prompts eficazes para instruir modelos de linguagem a redigir achados de auditoria.
# *   Avaliar a qualidade dos achados de auditoria gerados por LLMs.
# 
# **Importância no Ecossistema LangChain:**
# 
# Este notebook demonstra um caso de uso prático e relevante do LangChain no campo da auditoria. A capacidade de automatizar a redação de achados de auditoria pode economizar tempo, melhorar a consistência e aumentar a eficácia dos processos de auditoria. Ao dominar esta técnica, você estará apto a aplicar o LangChain em uma variedade de outros contextos que exigem a estruturação e apresentação de informações complexas. Prepare-se para aprimorar suas habilidades de comunicação e elevar o nível de seus relatórios de auditoria com o poder da IA Generativa!
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
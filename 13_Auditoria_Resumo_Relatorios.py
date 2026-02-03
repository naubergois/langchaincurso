#!/usr/bin/env python
# coding: utf-8

# # 13. Auditoria: Resumo de Relatórios Longos
# 
# Relatórios de auditoria podem ter centenas de páginas. Para a alta gestão, precisamos extrair apenas os "Pontos de Atenção" e "Recomendações". Quando o texto é maior que a janela de contexto do LLM, usamos técnicas como **Map-Reduce**.
# 
# **Objetivo:** Resumir um texto longo identificando principais riscos.

# # Explicação Detalhada do Assunto
# 
# # 13. Auditoria: Resumo de Relatórios Longos
# 
# Bem-vindo(a) ao notebook de número 13! Prepare-se para dominar a arte de resumir relatórios de auditoria extensos, transformando montanhas de texto em insights acionáveis.
# 
# ## Resumo Executivo
# 
# Neste notebook, mergulharemos no desafio de lidar com relatórios de auditoria volumosos. Nosso objetivo é extrair as informações mais cruciais para a alta gestão: os "Pontos de Atenção" e as "Recomendações". Utilizaremos as poderosas ferramentas do LangChain para resumir automaticamente grandes quantidades de texto, permitindo que você forneça resumos executivos concisos e impactantes.
# 
# ## Conceitos Chave
# 
# Para aproveitar ao máximo este notebook, é importante entender alguns conceitos fundamentais:
# 
# *   **Chains:** No LangChain, as Chains são sequências de chamadas a LLMs (Large Language Models) ou outras utilidades. Elas permitem criar fluxos de trabalho complexos, como o resumo de documentos.
# *   **LLMs (Large Language Models):** Modelos de linguagem poderosos, como o Gemini, capazes de gerar texto, traduzir idiomas, responder a perguntas e muito mais.
# *   **Summarization (Sumarização):** O processo de condensar um texto longo em uma versão mais curta, preservando os pontos principais.
# *   **Map-Reduce:** Uma técnica de processamento paralelo que divide um problema grande em problemas menores, resolve-os individualmente e, em seguida, combina os resultados. No contexto de resumo de documentos, o Map-Reduce permite resumir partes do documento separadamente e, em seguida, combinar os resumos.
# *   **Document:** No LangChain, um `Document` é uma abstração que representa um pedaço de texto junto com seus metadados.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Carregar e processar documentos de texto extensos.
# *   Implementar uma chain de summarization utilizando a técnica Map-Reduce.
# *   Extrair informações cruciais, como "Pontos de Atenção" e "Recomendações", de relatórios de auditoria.
# *   Criar resumos executivos concisos e informativos.
# *   Compreender e aplicar os conceitos de Chains e LLMs no contexto de resumo de documentos.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de resumir documentos longos é uma habilidade essencial no ecossistema LangChain. Ela permite que você lide com grandes volumes de informação de forma eficiente, extraindo insights valiosos e automatizando tarefas que antes exigiam horas de trabalho manual. O resumo de documentos é fundamental em diversas aplicações, como análise de relatórios, pesquisa de informações e criação de chatbots informativos. Dominar essa técnica abrirá portas para uma ampla gama de projetos e oportunidades no mundo da IA Generativa.
# 
# Vamos começar a transformar relatórios extensos em resumos executivos poderosos!
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
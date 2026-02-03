#!/usr/bin/env python
# coding: utf-8

# # 14. Auditoria: Classificação Automática de Riscos
# 
# Um dos passos da auditoria é classificar os apontamentos conforme seu risco (Alto, Médio, Baixo) para priorizar correções. LLMs são excelentes classificadores zero-shot.
# 
# **Objetivo:** Classificar descrições de falhas de controle e gerar uma justificativa para a nota.

# # Explicação Detalhada do Assunto
# 
# # 14. Auditoria: Classificação Automática de Riscos
# 
# Este notebook explora a aplicação de Inteligência Artificial Generativa e LangChain para automatizar uma etapa crucial no processo de auditoria: a classificação de riscos. Tradicionalmente, a classificação de apontamentos de auditoria em categorias de risco (Alto, Médio, Baixo) é uma tarefa manual e demorada. Aqui, demonstraremos como LLMs (Large Language Models) podem ser utilizados para realizar essa classificação de forma eficiente e precisa, permitindo que auditores seniores foquem em problemas de maior impacto.
# 
# ## Conceitos Chave
# 
# Para entender o que será abordado, é importante ter clareza sobre alguns conceitos-chave:
# 
# *   **LLMs (Large Language Models):** Modelos de linguagem treinados em grandes volumes de texto, capazes de gerar texto, traduzir idiomas, escrever diferentes tipos de conteúdo criativo e responder às suas perguntas de forma informativa. Neste contexto, eles são utilizados para analisar descrições de apontamentos de auditoria e inferir o nível de risco associado.
# *   **Prompt Engineering:** A arte de criar prompts (instruções) claros e eficazes para direcionar o LLM a produzir os resultados desejados. Um prompt bem elaborado é crucial para garantir a precisão e a relevância da classificação de riscos.
# *   **LangChain:** Um framework para construir aplicações baseadas em LLMs. Ele oferece ferramentas e abstrações que facilitam a criação de fluxos de trabalho complexos, como a definição de prompts, a integração com diferentes modelos de linguagem e a criação de chains (cadeias) de operações.
# *   **Chains:** Sequências de chamadas a LLMs ou outras utilidades. Neste notebook, utilizaremos chains para orquestrar o processo de classificação de riscos, desde a entrada do texto até a saída da classificação.
# *   **Tagging Chain:** Uma funcionalidade específica do LangChain projetada para categorizar dados através da atribuição de "tags" (rótulos). É uma alternativa simplificada para a classificação em cenários onde apenas a categorização é necessária.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Compreender como os LLMs podem ser aplicados para automatizar a classificação de riscos em auditoria.
# *   Definir uma matriz de riscos clara e concisa para orientar o LLM na classificação.
# *   Criar prompts eficazes para direcionar o LLM a classificar apontamentos de auditoria com base no nível de risco.
# *   Utilizar LangChain para construir chains de classificação de riscos, integrando prompts e LLMs.
# *   Avaliar a precisão e a eficácia da classificação automática de riscos em cenários reais.
# *   Explorar a alternativa do `create_tagging_chain` do LangChain para tarefas de categorização simples.
# 
# ## Importância no Ecossistema LangChain
# 
# A capacidade de automatizar a classificação de riscos é um exemplo poderoso de como o LangChain pode ser utilizado para otimizar processos de negócios. Este notebook demonstra como o framework pode ser aplicado em um contexto específico (auditoria), mas os princípios e as técnicas aprendidas podem ser generalizados para outras áreas, como análise de sentimentos, triagem de tickets de suporte e detecção de fraudes. Dominar essa habilidade é fundamental para qualquer profissional que deseja construir aplicações inteligentes e eficientes com LLMs e LangChain.
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
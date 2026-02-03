#!/usr/bin/env python
# coding: utf-8

# # 19. Auditoria: Detecção de Anomalias em Texto (Forensic)
# 
# Em investigações forenses, procuramos e-mails ou mensagens com tom de pressão, conluio ou desvio de conduta. Podemos usar analise de sentimento e intenção.
# 
# **Objetivo:** Analisar e-mails e flagrar possíveis fraudes.

# # Explicação Detalhada do Assunto
# 
# # 19. Auditoria: Detecção de Anomalias em Texto (Forensic)
# 
# Este notebook explora o uso de IA Generativa e LangChain para automatizar a detecção de anomalias e "red flags" em textos, especificamente em e-mails. Em investigações forenses, a identificação de mensagens com tom de pressão, indícios de conluio ou desvio de conduta é crucial. Este notebook demonstra como construir um sistema capaz de analisar textos e sinalizar automaticamente aqueles que merecem uma análise mais aprofundada.
# 
# **Conceitos Chave:**
# 
# *   **LangChain:** Framework para o desenvolvimento de aplicações de IA alimentadas por modelos de linguagem. Facilita a criação de pipelines complexos e o uso de diversos LLMs (Large Language Models).
# *   **LLMs (Large Language Models):** Modelos de linguagem poderosos capazes de gerar texto, traduzir idiomas, escrever diferentes tipos de conteúdo criativo e responder às suas perguntas de forma informativa. Neste notebook, utilizamos um LLM do Google.
# *   **Chains:** Sequências de chamadas a componentes (como LLMs, prompts e outros utilitários) que permitem construir fluxos de trabalho complexos e automatizados.
# *   **Prompt Engineering:** A arte de criar prompts (instruções) eficazes para LLMs, de modo a obter os resultados desejados. Um bom prompt é fundamental para o sucesso da detecção de anomalias.
# 
# **Objetivos de Aprendizado:**
# 
# Ao completar este notebook, você será capaz de:
# 
# *   Entender como usar LangChain e LLMs para análise forense de texto.
# *   Definir prompts eficazes para a detecção de "red flags" em e-mails.
# *   Implementar um pipeline para identificar e classificar e-mails suspeitos.
# *   Adaptar o sistema para detectar diferentes tipos de anomalias em outros contextos textuais.
# *   Compreender a importância da IA Generativa na automatização de tarefas de auditoria e investigação.
# 
# **Importância no Ecossistema LangChain:**
# 
# Este notebook demonstra um caso de uso prático e relevante de LangChain na área de auditoria e forense. A capacidade de automatizar a detecção de anomalias em texto é fundamental para:
# 
# *   **Aumentar a eficiência:** Reduzir o tempo e o esforço manual necessários para revisar grandes volumes de texto.
# *   **Melhorar a precisão:** Identificar padrões e nuances que podem passar despercebidos por analistas humanos.
# *   **Escalabilidade:** Analisar grandes volumes de dados de forma rápida e eficiente.
# *   **Redução de Riscos:** Identificar comportamentos inadequados e prevenir fraudes ou outras irregularidades.
# 
# Este notebook é um passo importante para entender como LangChain pode ser aplicado em diversas áreas para automatizar tarefas complexas e melhorar a tomada de decisões. Ao dominar as técnicas apresentadas aqui, você estará preparado para construir soluções inovadoras e impactantes.
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

# !pip install -qU langchain langchain-openai langchain-community # Script-patched




import os
try:
    from google.colab import userdata
except ImportError:
    userdata = None
import getpass

try:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
except:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. Dataset de E-mails
# 
# Mistura de e-mails normais e suspeitos.



emails = [
    "Prezados, favor enviar o relatório mensal de vendas até sexta-feira.",
    "Olha, precisamos pagar esse fornecedor HOJE. O diretor mandou. Paga logo e depois a gente vê a nota fiscal. Se não pagar, vai sobrar pra você.",
    "Segue anexo o comprovante de pagamento da taxa de renovação.",
    "Vamos fechar com a empresa Alpha. Eles prometeram um 'retorno' legal pra gente por fora. Apaga essa mensagem depois."
]


# ## 2. Prompt Detector de Red Flags
# Focamos em: Pressão indevida, contorno de controles, benefícios pessoais.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

class AnaliseRisco(BaseModel):
    risco: bool = Field(description="True se houver risco de fraude/compliance, False caso contrário")
    categoria: str = Field(description="Categoria: 'Pressão', 'Conluio', 'Bypass de Controle', 'Normal'")
    explicacao: str = Field(description="Explicação curta")

structured_llm = llm.with_structured_output(AnaliseRisco)

prompt = ChatPromptTemplate.from_template(
    """Analise o seguinte e-mail corporativo em busca de indicadores de fraude ou desvio de conduta.
    
    E-MAIL:
    {email}
    """
)

chain = prompt | structured_llm


# ## 3. Avaliação
# 
# Filtrando apenas os suspeitos.



for email in emails:
    res = chain.invoke({"email": email})
    if res.risco:
        print(f"[SUSPEITO] {res.categoria}: {res.explicacao}")
        print(f"Trecho: {email}\n")


# ## Conclusão
# 
# Identificamos bypass de controle ("paga logo e depois vê nota") e conluio ("retorno por fora"). Ferramenta poderosa para e-discovery.
#!/usr/bin/env python
# coding: utf-8

# # 19. Auditoria: Detecção de Anomalias em Texto (Forensic)
# 
# Em investigações forenses, procuramos e-mails ou mensagens com tom de pressão, conluio ou desvio de conduta. Podemos usar analise de sentimento e intenção.
# 
# **Objetivo:** Analisar e-mails e flagrar possíveis fraudes.



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
    os.environ['OPENAI_API_KEY'] = os.getenv('GOOGLE_API_KEY')
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
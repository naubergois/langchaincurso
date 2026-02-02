#!/usr/bin/env python
# coding: utf-8

# # 11. Auditoria: Análise de Conformidade
# 
# Neste módulo de Auditoria, focaremos em casos de uso reais. O primeiro é a **Verificação de Conformidade**. Dado um texto (ex: uma transação ou descrição de despesa) e uma política/regra, o LLM deve julgar se está conforme ou não.
# 
# **Cenário Real:** Analisar justificativas de despesas de viagem contra a política de viagens da empresa.



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
import sys
# Autenticação automática do script
for p in ['.', '..', 'scripts', '../scripts']:
    path = os.path.join(p, '.env')
    if os.path.exists(path):
        load_dotenv(path)
        break
if os.getenv('GOOGLE_API_KEY'):
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

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
    pass # Script-patched: using env var
except:
    pass # Script-patched: using env var


# ## 1. Definindo as Regras (Critérios)
# 
# Vamos definir a política da empresa.



politica_viagem = """
1. Despesas com alimentação não podem exceder R$ 100,00 por refeição.
2. O uso de táxi/Uber só é permitido se não houver transporte público disponível ou se for após as 22h.
3. Bebidas alcoólicas não são reembolsáveis em nenhuma hipótese.
4. Todas as despesas devem ter nota fiscal legível.
"""


# ## 2. Criando o Analisador de Conformidade
# 
# Usaremos um `ChatPromptTemplate` para instruir o modelo a agir como um auditor.



from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

prompt = ChatPromptTemplate.from_template(
    """Você é um Auditor Interno rigoroso.
    
    Analise a seguinte despesa com base na Política de Viagem fornecida.
    
    ### POLÍTICA DE VIAGEM ###
    {politica}
    
    ### DESPESA ###
    {despesa}
    
    Responda com:
    1. STATUS: [CONFORME / NÃO CONFORME]
    2. JUSTIFICATIVA: Breve explicação citando a regra violada, se houver.
    """
)

chain = prompt | llm | StrOutputParser()


# ## 3. Executando Testes
# 
# Vamos testar com alguns casos.



casos = [
    "Jantar no restaurante 'O Bom Garfo', valor R$ 85,00. Inclui um suco de laranja. Nota fiscal anexada.",
    "Almoço de negócios com cliente. Total R$ 150,00. Nota fiscal inclusa.",
    "Corrida de Uber às 14h para o aeroporto. Não verifiquei ônibus. Valor R$ 40,00.",
    "Happy hour com equipe. Valor R$ 200,00 sendo R$ 100,00 em cervejas."
]

for i, caso in enumerate(casos):
    print(f"--- CASO {i+1} ---")
    print(f"Descrição: {caso}")
    res = chain.invoke({"politica": politica_viagem, "despesa": caso})
    print(res)
    print("\n")


# ## 4. Evolução (Batch)
# 
# Para auditar milhares de linhas, usaríamos `chain.batch(lista_de_inputs)` para processar em paralelo.

# ## Conclusão
# 
# Este padrão simples pode ser escalado para analisar contratos, e-mails ou logs de sistemas, filtrando o que realmente precisa de atenção humana.
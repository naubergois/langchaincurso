#!/usr/bin/env python
# coding: utf-8

# # 12. Auditoria: Extração de Dados de Contratos
# 
# Auditores frequentemente precisam ler contratos PDF e preencher planilhas com dados chaves (Datas, Valores, Multas). Fazer isso manualmente é propenso a erro. Vamos usar LLMs para extrair dados estruturados (JSON).
# 
# **Objetivo:** Extrair Contratante, Contratada, Valor Mensal e Foro de um texto jurídico.



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


# ## 1. Definindo o Schema de Saída (Pydantic)
# 
# A melhor forma de garantir JSON válido é usar Pydantic com o método `.with_structured_output()` (disponível em modelos OpenAI recentes).



from langchain_core.pydantic_v1 import BaseModel, Field

class DadosContrato(BaseModel):
    contratante: str = Field(description="Nome da empresa ou pessoa contratante")
    contratada: str = Field(description="Nome da empresa ou pessoa contratada")
    valor_total: float = Field(description="Valor total do contrato em reais (numérico)")
    foro: str = Field(description="Cidade do foro de eleição")
    objeto: str = Field(description="Resumo breve do objeto do contrato")

# Exemplo de contrato (texto fictício)
contrato_texto = """
CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Pelo presente instrumento, de um lado a empresa TECNOLOGIA INOVADORA S.A., inscrita no CNPJ 12.345.678/0001-90, doravante denominada CONTRATANTE, e de outro lado JOÃO DA SILVA DESENVOLVIMENTO ME, CNPJ 98.765.432/0001-10, denominado CONTRATADA.

Têm entre si justo e contratado o seguinte:
    pass # Script-patched: ensure non-empty block

CLÁUSULA PRIMEIRA - DO OBJETO
O presente contrato tem por objeto a prestação de serviços de desenvolvimento de software em Python.

CLÁUSULA SEGUNDA - DO PREÇO
Pela prestação dos serviços, a CONTRATANTE pagará à CONTRATADA o valor global de R$ 50.000,00 (cinquenta mil reais), divididos em 5 parcelas.

CLÁUSULA DÉCIMA - DO FORO
As partes elegem o foro da Comarca de São Paulo/SP para dirimir quaisquer dúvidas.
"""


# ## 2. Configurando o Modelo para Extração
# 
# Usaremos `ChatOpenAI` com `with_structured_output`.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# Vinculamos o schema Pydantic ao LLM
structured_llm = llm.with_structured_output(DadosContrato)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em extração de dados jurídicos."),
    ("human", "Extraia as informações do seguinte contrato:\n\n{texto_contrato}")
])

extractor_chain = prompt | structured_llm


# ## 3. Extraindo os Dados
# 
# O resultado será um objeto Python da classe `DadosContrato`, fácil de usar no código.



dados = extractor_chain.invoke({"texto_contrato": contrato_texto})

print("Tipo do retorno:", type(dados))
print(f"Contratante: {dados.contratante}")
print(f"Contratada: {dados.contratada}")
print(f"Valor: {dados.valor_total}")
print(f"Foro: {dados.foro}")


# ## 4. Exportando para Dicionário/JSON
# 
# Para salvar num Excel ou Banco de Dados.



print(dados.dict())


# ## Conclusão
# 
# Conseguimos transformar texto não estruturado (contrato) em dados estruturados (objeto Python/JSON) com alta precisão.
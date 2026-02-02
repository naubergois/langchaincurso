#!/usr/bin/env python
# coding: utf-8

# # 22. Saída Estruturada com LangChain e Pydantic
# 
# Agora vamos instruir o LLM a retornar dados validade pelo Pydantic, garantindo confiabilidade para automações.
# 
# **Objetivo:** Usar `.with_structured_output()` para extrair informações complexas.



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

# !pip install -qU langchain langchain-openai langchain-community pydantic # Script-patched




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


# ## 1. Definindo o Schema
# 
# Imagine que queremos extrair informações de um currículo.



from pydantic import BaseModel, Field
from typing import List

class Experiencia(BaseModel):
    cargo: str = Field(description="Cargo ocupado")
    empresa: str = Field(description="Nome da empresa")
    anos: int = Field(description="Duração em anos (arredondado)")

class Curriculo(BaseModel):
    nome: str = Field(description="Nome do candidato")
    skills: List[str] = Field(description="Lista de habilidades técnicas")
    historico: List[Experiencia]
    resumo_perfil: str = Field(description="Resumo do perfil em 1 frase")


# ## 2. Configurando o LLM
# 
# O método `.with_structured_output` usa Function Calling por baixo dos panos (na OpenAI) para garantir o formato.



from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

structured_llm = llm.with_structured_output(Curriculo)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um recrutador especialista. Extraia os dados do currículo fornecido."),
    ("human", "{cv_text}")
])

extractor = prompt | structured_llm


# ## 3. Extraindo Dados
# 
# Vamos passar um texto não estruturado.



texto_cv = """
Me chamo Ana Souza. Sou desenvolvedora Python há 5 anos, tendo trabalhado na TechCorp. 
Antes disso, fui estagiária de Java na BancoDev por 1 ano. 
Sei muito de SQL e Docker também.
"""

resultado = extractor.invoke({"cv_text": texto_cv})

print(f"Candidata: {resultado.nome}")
print(f"Skills: {resultado.skills}")
for exp in resultado.historico:
    print(f" - {exp.cargo} na {exp.empresa} ({exp.anos} anos)")


# ## 4. Por que isso é melhor que JSON puro no prompt?
# 
# 1. **Validação**: Se o LLM alucinar um campo obrigatório faltando, o Pydantic avisa.
# 2. **Tipagem**: `anos` vem como `int`, não `string`.
# 3. **Facilidade**: O objeto retornado já é uma classe Python, com autocompletar no IDE.

# ## Conclusão
# 
# Essa é a base para criar Agentes Confiáveis. Se o agente precisa chamar uma API que exige `int`, o Pydantic garante que ele não vai enviar `"dez"` por escrito.
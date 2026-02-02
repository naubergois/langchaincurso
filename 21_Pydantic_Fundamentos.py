#!/usr/bin/env python
# coding: utf-8

# # 21. Fundamentos de Pydantic
# 
# Antes de mergulhar em LangChain avançado e Agentes, é crucial entender o **Pydantic**. Ele é a biblioteca padrão para validação de dados em Python e a base para estruturar outputs de LLMs.
# 
# **Objetivos:**
# - Criar modelos de dados (`BaseModel`).
# - Validar tipos e regras de negócio (`validator`).
# - Exportar para JSON (Schema).



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

# !pip install -qU pydantic # Script-patched


# ## 1. Criando um Modelo Básico
# 
# Diferente de `dataclasses` padrão, o Pydantic valida os tipos em tempo de execução.



from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

class Usuario(BaseModel):
    id: int
    nome: str = Field(description="Nome completo do usuário")
    email: str
    idade: Optional[int] = None
    interesses: List[str] = []

# Criando uma instância válida
user = Usuario(id=1, nome="Nauber Gois", email="nauber@example.com", interesses=["IA", "Python"])
print(user)
print(user.model_dump_json(indent=2))


# ## 2. Validação Automática
# 
# O Pydantic tenta converter os tipos (Coercion). Se falhar, lança erro.



try:
    pass # Script-patched: ensure non-empty block
    # Passando string '123' para id (int) funciona (converte)
    # Mas passando lista para nome falha
    Usuario(id="123", nome=["Errado"], email="email@teste")
except ValidationError as e:
    print("Erro de validação detectado:")
    print(e)


# ## 3. Validadores Customizados (`@field_validator`)
# 
# Podemos impor regras de negócio, como "idade deve ser maior que 18".



from pydantic import field_validator

class Produto(BaseModel):
    nome: str
    preco: float

    @field_validator('preco')
    @classmethod
    def preco_positivo(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('O preço deve ser positivo')
        return v

try:
    Produto(nome="Celular", preco=-10)
except ValidationError as e:
    print(e)


# ## 4. Aninhamento de Modelos
# 
# Poderoso para representar estruturas complexas que os LLMs vão gerar.



class Endereco(BaseModel):
    rua: str
    cidade: str

class Cliente(BaseModel):
    nome: str
    endereco: Endereco

dados = {
    "nome": "Empresa X",
    "endereco": {
        "rua": "Av. Paulista",
        "cidade": "São Paulo"
    }
}

cliente = Cliente(**dados)
print(cliente.endereco.cidade)


# ## Conclusão
# 
# Dominar Pydantic é essencial para usar `Function Calling` e `Structured Output` no LangChain, pois é assim que definimos o "formato" que o LLM deve obedecer.
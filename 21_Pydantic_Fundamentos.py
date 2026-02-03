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

# # Explicação Detalhada do Assunto
# 
# # 21. Fundamentos de Pydantic
# 
# Este notebook é uma imersão no **Pydantic**, uma biblioteca essencial para validação de dados em Python e um pilar fundamental para construir aplicações robustas com LangChain e IA Generativa. Antes de explorarmos os tópicos mais avançados como Agentes e Function Calling, é crucial dominar os conceitos básicos do Pydantic.
# 
# **Conceitos Chave:**
# 
# *   **Pydantic:** Uma biblioteca Python para definir modelos de dados com validação de tipos e coerção automática. Ele garante que os dados que sua aplicação recebe e processa estejam no formato esperado.
# *   **Modelos Pydantic (BaseModel):** Classes que definem a estrutura dos seus dados, incluindo os tipos de cada campo e regras de validação.
# *   **Validação de Dados:** O processo de verificar se os dados estão corretos e consistentes, de acordo com as regras definidas no seu modelo Pydantic.
# *   **Coerção de Tipos:** A capacidade do Pydantic de converter automaticamente os dados para o tipo correto, quando possível (ex: converter a string "123" para o inteiro 123).
# *   **Validadores Customizados (`@field_validator`):** Funções que você define para adicionar regras de validação personalizadas, como verificar se um número está dentro de um determinado intervalo.
# *   **Aninhamento de Modelos:** A capacidade de definir modelos Pydantic que contêm outros modelos Pydantic, permitindo representar estruturas de dados complexas.
# 
# **Objetivos de Aprendizado:**
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Criar modelos Pydantic básicos para definir a estrutura dos seus dados.
# *   Entender como o Pydantic valida automaticamente os tipos de dados.
# *   Implementar validadores customizados para impor regras de negócio específicas.
# *   Criar modelos Pydantic aninhados para representar estruturas de dados complexas.
# *   Reconhecer a importância do Pydantic para o uso eficaz de `Function Calling` e `Structured Output` no LangChain.
# 
# **Importância no Ecossistema LangChain:**
# 
# Dominar o Pydantic é **absolutamente essencial** para utilizar `Function Calling` e `Structured Output` no LangChain. Pense no Pydantic como o "contrato" que você estabelece com o LLM. Ele define o formato exato dos dados que você espera receber do modelo. Quando você usa `Function Calling`, por exemplo, o LLM gera dados que correspondem à estrutura definida por seus modelos Pydantic. Sem um bom entendimento do Pydantic, você terá dificuldades em garantir que o LLM retorne informações no formato correto, o que pode levar a erros e resultados inesperados. Este notebook é o alicerce para construir aplicações LangChain mais poderosas e confiáveis. Prepare-se para aprofundar seus conhecimentos e desbloquear o verdadeiro potencial da IA Generativa!
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
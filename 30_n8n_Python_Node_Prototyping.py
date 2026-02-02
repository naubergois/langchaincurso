#!/usr/bin/env python
# coding: utf-8

# # 30. Prototipagem de Nós Python para n8n
# 
# O n8n permite executar Python nativo em seus fluxos (Code Node), mas a interface web não é ideal para debug ou desenvolvimento pesado.
# 
# Neste notebook, vamos emular o ambiente de dados do n8n para que você possa desenvolver sua lógica aqui no Colab e depois apenas copiar e colar no n8n.
# 
# **Objetivos:**
# 1. Entender a estrutura `items` (Lista de Dicionários).
# 2. Simular a entrada de dados do n8n.
# 3. Escrever código de transformação complexa (ex: limpeza de dados).
# 4. Validar o output no formato esperado pelo n8n.

# ## 1. A Estrutura de Dados do n8n
# 
# No n8n, a variável global `items` contém os dados que chegam no nó. É sempre uma lista de objetos, onde cada objeto tem uma chave `json`.
# 
# Estrutura padrão:
# ```python
# items = [
#     { "json": { "id": 1, "nome": "Ana" } },
#     { "json": { "id": 2, "nome": "Bob" } }
# ]
# ```



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

# MOCK: Simulando dados que viriam de um nó anterior (ex: Google Sheets ou Banco de Dados)
items = [
    { 
        "json": { 
            "order_id": "ORD-001", 
            "products": "Tv, Suporte, Cabo HDMI", 
            "total": "R$ 2.500,00" 
        } 
    },
    { 
        "json": { 
            "order_id": "ORD-002", 
            "products": "Notebook Gamer", 
            "total": "R$ 5.000,00" 
        } 
    }
]

print("Dados de Entrada (Mock n8n):")
print(items)


# ## 2. Desenvolvendo a Lógica (Code Node)
# 
# Imagine que precisamos separar os produtos em uma lista e converter o total para float.
# 
# Este é o código que você escreveria dentro do nó "Code" do n8n.



# --- INICIO DO CÓDIGO PARA COPIAR PARA O N8N ---

output_items = []

for item in items:
    pass # Script-patched: ensure non-empty block
    # Acessamos os dados 'json' do item atual
    dados = item['json']
    
    # Lógica de Transformação
    # 1. Split produtos
    lista_produtos = [p.strip() for p in dados['products'].split(",")]
    
    # 2. Convert Price
    price_str = dados['total'].replace("R$ ", "").replace(".", "").replace(",", ".")
    price_float = float(price_str)
    
    # Criamos o novo objeto transformado
    # No Python do n8n, retornamos uma lista de dicionários também
    output_items.append({
        "json": {
            "id_limpo": dados['order_id'],
            "produtos_lista": lista_produtos,
            "valor_numerico": price_float,
            "categoria": "Alto Valor" if price_float > 3000 else "Padrão"
        }
    })

# No n8n, a última variável retornada é o que sai do nó
# Em alguns casos específicos do n8n v1+, você deve apenas retornar a lista
# return output_items 

# --- FIM DO CÓDIGO ---




# Validação do Resultado
print("Output Gerado:")
for out in output_items:
    print(out)


# ## 3. Instalando Pacotes Externos
# 
# No n8n self-hosted, você pode permitir bibliotecas externas (como `numpy` ou `pandas`).
# 
# Para testar aqui:



# !pip install -q pandas # Script-patched




import pandas as pd

# Exemplo: Usando Pandas para agregar dados antes de enviar pro próximo nó
df = pd.DataFrame([i['json'] for i in output_items])
media = df['valor_numerico'].mean()

print(f"Média dos pedidos: {media}")

# Transformando de volta para formato n8n
output_agg = [{"json": {"media_pedidos": media}}]
print(output_agg)

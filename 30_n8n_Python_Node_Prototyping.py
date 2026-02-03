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

# # Explicação Detalhada do Assunto
# 
# # 30. Prototipagem de Nós Python para n8n
# 
# O n8n é uma poderosa ferramenta de automação que permite criar fluxos de trabalho complexos sem a necessidade de escrever código extenso. No entanto, quando se trata de lógica mais complexa, a capacidade de executar código Python nativo dentro dos nós (Code Node) se torna essencial. A interface web do n8n, embora funcional, pode não ser a mais eficiente para depuração e desenvolvimento iterativo.
# 
# Este notebook foi criado para solucionar essa limitação, oferecendo um ambiente de prototipagem local para seus nós Python do n8n.  Aqui, você poderá desenvolver, testar e depurar seu código Python de forma mais rápida e eficiente antes de implementá-lo no n8n.
# 
# ## 1. A Estrutura de Dados do n8n
# 
# No n8n, a variável global `items` desempenha um papel central na passagem de dados entre os nós. Ela sempre se apresenta como uma lista de objetos, onde cada objeto contém uma chave fundamental chamada `json`. Essa estrutura é crucial para entender como os dados são processados e transformados dentro dos seus fluxos de trabalho.
# 
# Estrutura padrão:
# ```python
# [
#     {
#         "json": {
#             "chave1": "valor1",
#             "chave2": "valor2"
#             # ... outras chaves e valores
#         }
#     },
#     {
#         "json": {
#             "chave1": "valor3",
#             "chave2": "valor4"
#             # ... outras chaves e valores
#         }
#     },
#     # ... mais itens
# ]
# ```
# 
# ## 2. Desenvolvendo a Lógica (Code Node)
# 
# Imagine a seguinte situação: você precisa processar uma lista de produtos, separando-os e convertendo o valor total para um formato numérico adequado. Este notebook irá guiá-lo na criação do código Python que realizará essa tarefa, simulando o ambiente do Code Node do n8n. Você aprenderá a acessar e manipular os dados dentro da estrutura `items`, aplicando a lógica necessária para transformar os dados conforme suas necessidades.
# 
# ## 3. Instalando Pacotes Externos
# 
# O n8n self-hosted oferece a flexibilidade de integrar bibliotecas externas, como `numpy` e `pandas`, expandindo significativamente suas capacidades de processamento de dados. Este notebook demonstrará como instalar e utilizar essas bibliotecas em seu ambiente de prototipagem, permitindo que você experimente e valide seu código antes de implementá-lo no n8n.
# 
# **Resumo Executivo:** Este notebook oferece um ambiente para prototipar nós Python para o n8n fora da interface web, permitindo um desenvolvimento e depuração mais eficientes.
# 
# **Conceitos Chave:**
# *   **n8n Code Node:** Um nó no n8n que permite a execução de código Python.
# *   **Estrutura de Dados `items`:** A variável global no n8n que contém os dados passados entre os nós. É uma lista de dicionários, onde cada dicionário tem uma chave `json`.
# 
# **Objetivos de Aprendizado:** Após este notebook, você será capaz de:
# 
# *   Entender a estrutura de dados `items` no n8n.
# *   Desenvolver e testar a lógica do seu nó Python localmente.
# *   Simular o ambiente do Code Node do n8n.
# *   Instalar e usar pacotes Python externos em seu ambiente de prototipagem.
# *   Transferir o código prototipado para o nó Code do n8n.
# 
# **Importância no Ecossistema LangChain:** Embora este notebook não envolva diretamente o LangChain, ele capacita você a criar nós Python personalizados no n8n, que podem ser usados para integrar o LangChain em seus fluxos de trabalho de automação. Isso permite que você combine o poder da IA Generativa com a flexibilidade do n8n para construir soluções complexas e personalizadas. Domine essa habilidade e expanda as fronteiras do que você pode automatizar!
# 
# ---
# 

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
    os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')
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

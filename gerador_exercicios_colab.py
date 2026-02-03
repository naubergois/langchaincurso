#!/usr/bin/env python
# coding: utf-8

# # Gerador de Novas Versões dos Exercícios
# 
# Este notebook automatiza a criação de novas versões dos exercícios a partir de um conjunto original, facilitando o uso em Google Colab e outros ambientes interativos.

# ## 1. Importar Bibliotecas Necessárias
# 
# Instale e importe as bibliotecas necessárias para manipulação e geração dos exercícios.



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

# Instalação das bibliotecas (caso necessário no Colab)
# !pip install pandas numpy # Script-patched

# Importação das bibliotecas
import pandas as pd
import numpy as np


# ## 2. Carregar Exercícios Originais
# 
# Carregue os exercícios originais a partir de um arquivo (exemplo: CSV, TXT ou JSON).



# Exemplo: Carregar exercícios de um arquivo CSV
# Substitua 'exercicios.csv' pelo caminho do seu arquivo
try:
    df_exercicios = pd.read_csv('exercicios.csv')
    print(df_exercicios.head())
except Exception as e:
    print('Erro ao carregar arquivo:', e)
    # Exemplo de dados caso não exista arquivo
    df_exercicios = pd.DataFrame({
        'enunciado': ['Qual a capital do Brasil?', 'Resolva: 2 + 2'],
        'resposta': ['Brasília', '4']
    })
    print(df_exercicios.head())


# ## 3. Gerar Novas Versões dos Exercícios
# 
# Implemente funções para modificar, embaralhar ou parametrizar os exercícios, criando novas versões automaticamente.



# Função para embaralhar enunciados e respostas

def gerar_novas_versoes(df, n=3):
    novas_versoes = []
    for i in range(n):
        df_embaralhado = df.sample(frac=1).reset_index(drop=True)
        novas_versoes.append(df_embaralhado)
    return novas_versoes

novas_versoes = gerar_novas_versoes(df_exercicios, n=3)
print('Exemplo de nova versão:')
print(novas_versoes[0].head())


# ## 4. Salvar Exercícios Gerados
# 
# Salve as novas versões dos exercícios em arquivos separados para uso posterior.



# Salvar cada nova versão em um arquivo CSV
for idx, df_novo in enumerate(novas_versoes):
    nome_arquivo = f'exercicios_versao_{idx+1}.csv'
    df_novo.to_csv(nome_arquivo, index=False)
    print(f'Salvo: {nome_arquivo}')


# ## 5. Visualizar Exemplos das Novas Versões
# 
# Exiba exemplos das novas versões dos exercícios gerados para conferência.



# Visualizar exemplos das novas versões
for idx, df_novo in enumerate(novas_versoes):
    print(f'Exemplo da versão {idx+1}:')
    print(df_novo.head())
    print('-'*40)

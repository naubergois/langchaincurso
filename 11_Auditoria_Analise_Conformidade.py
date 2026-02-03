#!/usr/bin/env python
# coding: utf-8

# # 11. Auditoria: Análise de Conformidade
# 
# Neste módulo de Auditoria, focaremos em casos de uso reais. O primeiro é a **Verificação de Conformidade**. Dado um texto (ex: uma transação ou descrição de despesa) e uma política/regra, o LLM deve julgar se está conforme ou não.
# 
# **Cenário Real:** Analisar justificativas de despesas de viagem contra a política de viagens da empresa.

# # Explicação Detalhada do Assunto
# 
# # 11. Auditoria: Análise de Conformidade
# 
# Bem-vindo ao módulo de Auditoria, onde exploraremos aplicações práticas da LangChain para resolver desafios do mundo real. Neste notebook, focaremos na **Verificação de Conformidade**, um caso de uso essencial para garantir que processos e dados estejam alinhados com políticas e regulamentos. Imagine ter um sistema capaz de analisar automaticamente transações, contratos ou e-mails, identificando desvios e alertando para potenciais problemas. É isso que vamos construir!
# 
# ## Resumo Executivo
# 
# Este notebook demonstra como usar a LangChain para criar um sistema de auditoria automatizado capaz de verificar a conformidade de informações textuais com regras predefinidas. Analisaremos exemplos práticos, desde a verificação de despesas de viagem até a conformidade de contratos, mostrando como a IA Generativa pode otimizar processos de auditoria e liberar recursos humanos para tarefas mais estratégicas.
# 
# ## Conceitos Chave
# 
# Para aproveitar ao máximo este notebook, é importante entender alguns conceitos fundamentais:
# 
# *   **Chains (Correntes):** São sequências de chamadas a componentes da LangChain, como LLMs (Large Language Models), prompts e parsers. Permitem construir fluxos de trabalho complexos de forma modular e reutilizável. Neste caso, criaremos uma chain para analisar a conformidade de um texto com uma política.
# *   **LLMs (Large Language Models):** Modelos de linguagem grandes, como o Gemini, capazes de gerar texto, traduzir idiomas, escrever diferentes tipos de conteúdo criativo e responder às suas perguntas de forma informativa. Usaremos um LLM para interpretar as regras de conformidade e avaliar se um determinado texto as cumpre.
# *   **Prompts:** Instruções específicas fornecidas ao LLM para direcionar sua resposta. Criaremos um prompt detalhado para instruir o LLM a agir como um auditor e a seguir as regras de conformidade definidas.
# *   **Output Parsers:** Componentes que estruturam a saída do LLM em um formato específico, facilitando o processamento posterior. Usaremos um parser para garantir que a resposta do LLM seja clara e concisa, indicando se o texto está em conformidade ou não.
# 
# ## Objetivos de Aprendizado
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Definir regras de conformidade claras e concisas para um determinado contexto.
# *   Criar um `ChatPromptTemplate` para instruir um LLM a agir como um auditor.
# *   Construir uma chain (corrente) usando LangChain para analisar a conformidade de textos com regras predefinidas.
# *   Avaliar a conformidade de diferentes exemplos de texto usando a chain criada.
# *   Entender como escalar o processo de auditoria para grandes volumes de dados usando `chain.batch()`.
# *   Adaptar o sistema de auditoria para diferentes casos de uso, como análise de contratos, e-mails ou logs de sistemas.
# 
# ## Importância no Ecossistema LangChain
# 
# A análise de conformidade é um caso de uso poderoso e relevante no ecossistema LangChain. Ela demonstra como a IA Generativa pode ser aplicada para automatizar tarefas repetitivas e demoradas, permitindo que as equipes de auditoria e compliance se concentrem em atividades de maior valor agregado. Este notebook fornece uma base sólida para construir sistemas de auditoria mais complexos e personalizados, integrando-os com outras ferramentas e plataformas. Ao dominar este conceito, você estará um passo à frente na aplicação da LangChain para resolver desafios de negócios reais.
# 
# Vamos começar a construir nosso sistema de auditoria!
# 
# ---
# 



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
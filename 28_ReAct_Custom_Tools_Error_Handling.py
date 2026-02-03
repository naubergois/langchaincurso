#!/usr/bin/env python
# coding: utf-8

# # 28. ReAct Avançado: Ferramentas Personalizadas e Robustez
# 
# A parte mais crítica da engenharia de prompt em agentes não é o prompt principal do agente (que é bem padronizado), mas sim **como descrevemos as ferramentas**.
# 
# Se o LLM não entender o que a ferramenta faz ou como passar os parâmetros, ele vai alucinar ou falhar.
# 
# **Objetivos:**
# 1. Criar ferramentas com argumentos complexos (Pydantic).
# 2. Engenharia de Prompt nas descrições das ferramentas.
# 3. Lidar com erros de formatação.
# 
# ---

# # Explicação Detalhada do Assunto
# 
# # 28. ReAct Avançado: Ferramentas Personalizadas e Robustez
# 
# Bem-vindo(a) ao notebook 28 da nossa série sobre LangChain e IA Generativa! Neste módulo avançado, mergulharemos na criação de agentes ReAct robustos e personalizados, com foco em ferramentas customizadas e tratamento de erros. A capacidade de construir agentes que interagem de forma eficaz com ferramentas complexas e que lidam graciosamente com erros é crucial para aplicações de IA generativa no mundo real.
# 
# **Resumo Executivo:**
# 
# Este notebook te guiará na construção de agentes ReAct que utilizam ferramentas personalizadas com múltiplos argumentos (ferramentas estruturadas) e que implementam estratégias de tratamento de erros. Aprenderemos a definir o schema de entrada dessas ferramentas, a entender o impacto da descrição da ferramenta no prompt do agente e a personalizar o tratamento de erros para garantir que o agente se recupere de falhas de formatação de forma inteligente.
# 
# **Conceitos Chave:**
# 
# *   **ReAct:** Uma metodologia para construir agentes que combinam "Reasoning" (raciocínio) e "Acting" (ação). Agentes ReAct geram pensamentos (Thoughts) para raciocinar sobre o problema, decidem qual ação (Action) tomar e observam os resultados (Observation) antes de repetir o ciclo.
# *   **Ferramentas Estruturadas (Structured Tools):** Ferramentas que aceitam múltiplos argumentos, definidos através de um schema de entrada. Isso permite a criação de ferramentas mais complexas e flexíveis.
# *   **Schema de Entrada:** A definição dos argumentos que uma ferramenta estruturada espera receber, incluindo o tipo de dado de cada argumento e uma descrição. Usamos Pydantic `BaseModel` para definir esses schemas.
# *   **Prompt Engineering:** A arte de criar prompts eficazes para guiar o comportamento de um modelo de linguagem. Neste contexto, exploraremos como a descrição da ferramenta influencia a forma como o agente a utiliza.
# *   **Tratamento de Erros (Error Handling):** A capacidade de um agente de detectar e se recuperar de erros, como falhas de formatação na entrada da ferramenta. Personalizaremos o tratamento de erros para fornecer feedback útil ao agente e guiá-lo na correção do problema.
# 
# **Objetivos de Aprendizado:**
# 
# Ao final deste notebook, você será capaz de:
# 
# *   Criar ferramentas estruturadas com múltiplos argumentos usando Pydantic.
# *   Entender como a descrição da ferramenta afeta o comportamento do agente.
# *   Construir um agente ReAct que utiliza ferramentas estruturadas.
# *   Implementar estratégias personalizadas de tratamento de erros para agentes ReAct.
# *   Personalizar o prompt para a correção de erros de formatação.
# 
# **Importância no Ecossistema LangChain:**
# 
# O LangChain simplifica a construção de agentes complexos, mas o sucesso depende da capacidade de integrar ferramentas personalizadas e de garantir que o agente lide com erros de forma graciosa. Este notebook explora aspectos cruciais da engenharia de agentes ReAct no LangChain, permitindo que você crie aplicações de IA generativa mais robustas e confiáveis. Dominar esses conceitos é fundamental para construir agentes que resolvem problemas complexos no mundo real. Vamos começar!
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

# !pip install -q langchain langchain-openai pydantic # Script-patched




import os
import getpass

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. Ferramentas Estruturadas (Structured Tools)
# 
# Ferramentas simples recebem uma única string. Ferramentas reais precisam de múltiplos argumentos (ex: `reservar_passagem(origem, destino, data)`).
# 
# Usamos **Pydantic** para definir o schema dos argumentos. Esse schema é **convertido em texto/JSON** e inserido no prompt do LLM.



from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

# 1. Definir o Schema de Entrada
class CalculadoraInvestimentoInput(BaseModel):
    valor_inicial: float = Field(description="O valor inicial do investimento em reais")
    anos: int = Field(description="Duração do investimento em anos")
    risco: str = Field(description="Perfil de risco: 'baixo', 'medio' ou 'alto'")

# 2. Definir a Função
def simular_investimento(valor_inicial: float, anos: int, risco: str) -> str:
    """Calcula o retorno estimado de um investimento baseado no perfil de risco."""
    taxas = {"baixo": 0.10, "medio": 0.15, "alto": 0.25}
    taxa = taxas.get(risco.lower(), 0.10)
    
    final = valor_inicial * ((1 + taxa) ** anos)
    return f"Investimento com risco {risco} após {anos} anos resultará em aproximadamente R$ {final:.2f}"

# 3. Criar a Ferramenta
ferramenta_investimento = StructuredTool.from_function(
    func=simular_investimento,
    name="SimuladorInvestimentos",
    description="Útil para calcular projeções financeiras. Requer valor inicial, anos e perfil de risco.",
    args_schema=CalculadoraInvestimentoInput
)

tools = [ferramenta_investimento]


# ## 2. O Impacto da Descrição no Prompt
# 
# Vamos ver como o LLM "enxerga" essa ferramenta. É isso que o `create_react_agent` coloca no prompt.



print(f"Nome: {ferramenta_investimento.name}")
print(f"Descrição: {ferramenta_investimento.description}")
print(f"Schema JSON:\n{ferramenta_investimento.args}")


# ## 3. Rodando com Agente Multi-Argumento
# 
# Nota: O ReAct padrão do LangChain espera `Action Input` como uma STRING única. Para usar ferramentas multi-argumento com ReAct clássico, o agente precisa gerar um **JSON string** dentro do `Action Input`.
# 
# Prompt Engineering Dica: Às vezes precisamos explicitar isso no prompt principal.



from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

query = "Se eu investir 1000 reais por 5 anos num perfil de alto risco, quanto terei?"

try:
    agent_executor.invoke({"input": query})
except Exception as e:
    print(f"Erro esperado (às vezes): {e}")
    # O ReAct padrão às vezes luta para formatar múltiplos argumentos como string única.
    # É aqui que entra o 'Structured Chat Agent' ou a melhoria do Prompt.


# ## 4. Prompt Engineering para Correção de Erros
# 
# Quando definimos `handle_parsing_errors=True`, o LangChain usa um prompt interno para corrigir o agente quando ele falha. Podemos personalizar isso?
# 
# Sim, passando uma string customizada ou função para `handle_parsing_errors`.



def custom_error_handler(error) -> str:
    return f"""ERRO DE FORMATAÇÃO ENCONTRADO NO SEU ULTIMO TURNO:
    {error}
    
    LEMBRE-SE: Para usar 'SimuladorInvestimentos', o input deve ser UM JSON VÁLIDO.
    Exemplo: Action Input: {{"valor_inicial": 100, "anos": 2, "risco": "alto"}}
    Tente novamente corrigindo o formato."""

runner_robusto = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True, 
    handle_parsing_errors=custom_error_handler # Injeta isso no prompt se der erro
)

runner_robusto.invoke({"input": "Invista 500 reais por 10 anos risco medio"})


# ### Conclusão dos 3 Notebooks
# 
# 1. **Fundamentos:** Vimos que agentes são apenas loops `while` com prompts inteligentes de `Thought/Action`.
# 2. **LangChain:** Vimos como usar abstrações para escalar isso.
# 3. **Avançado:** Viu que a "inteligência" muitas vezes reside na descrição precisa das ferramentas (docstrings) e nas mensagens de erro (correction prompts).
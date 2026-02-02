#!/usr/bin/env python
# coding: utf-8

# # 26. Engenharia de Prompt para Agentes: O Padrão ReAct
# 
# Neste notebook, vamos mergulhar no coração dos Agentes de IA: o padrão **ReAct (Reasoning + Acting)**. Ao invés de usar frameworks prontos imediatamente, vamos construir um loop ReAct "na unha" para entender exatamente como a engenharia de prompt guia o modelo.
# 
# **Objetivos:**
# 1. Entender a evolução: Zero-shot -> Chain of Thought (CoT) -> ReAct.
# 2. Analisar a estrutura de um Prompt ReAct.
# 3. Implementar um loop de Agente Manual em Python puro.
# 
# ---



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

# !pip install -q langchain langchain-openai openai google-search-results # Script-patched




import os
import getpass

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")


# ## 1. Teoria: De Pensamento à Ação
# 
# ### O Problema do LLM Isolado
# LLMs são ótimos em prever texto, mas ruins em:
# 1. Conhecimento atualizado (corte de treino).
# 2. Matemática precisa.
# 3. Interagir com o mundo real.
# 
# ### A Solução ReAct (Yao et al., 2022)
# O paper *ReAct: Synergizing Reasoning and Acting in Language Models* propôs um formato de prompt onde o modelo gera intercaladamente:
# - **Thought (Pensamento):** Raciocínio sobre o estado atual.
# - **Action (Ação):** Um comando específico para uma ferramenta externa.
# - **Observation (Observação):** O resultado real da ferramenta (inserido pelo código, não gerado pelo LLM).

# ## 2. Anatomia de um Prompt ReAct
# 
# Um prompt ReAct clássico precisa de:
# 1. **Instrução de Ferramentas:** Quais ferramentas existem e como usá-las.
# 2. **Formato de Saída:** Instruções rígidas sobre como escrever `Thought`, `Action`, `Action Input`.
# 3. **Exemplos (Few-Shot):** Demonstrations de como resolver problemas passo-a-passo. É aqui que a mágica da engenharia de prompt acontece.
# 
# Vamos definir nosso prompt manual:



REACT_PROMPT_TEMPLATE = """
Responda as seguintes questões o melhor que puder. Você tem acesso às seguintes ferramentas:
    pass # Script-patched: ensure non-empty block

{tool_descriptions}

Use o seguinte formato:
    pass # Script-patched: ensure non-empty block

Questão: a questão de entrada que você deve responder
Thought: você deve sempre pensar sobre o que fazer
Action: a ação a ser tomada, deve ser uma de [{tool_names}]
Action Input: a entrada para a ação
Observation: o resultado da ação
... (esse padrão Thought/Action/Action Input/Observation pode se repetir N vezes)
Thought: agora eu sei a resposta final
Final Answer: a resposta final para a questão original

Comece!

Questão: {input}
Thought:"""


# ## 3. Implementadando Ferramentas (Simuladas)
# 
# Para este exercício, vamos criar ferramentas simples em Python.



def search_wikipedia(query):
    """Simula uma busca na Wikipedia (retorna um resumo fixo para teste)."""
    print(f"[TOOL] Buscando na Wikipedia por: {query}")
    # Simulação de retorno
    if "População do Brasil" in query:
        return "A população do Brasil em 2023 era estimada em 203 milhões de pessoas."
    if "PIB do Brasil" in query:
        return "O PIB do Brasil em 2023 foi de aproximadamente 2.17 trilhões de dólares."
    return "Sem resultados relevantes."

def calculator(expression):
    """Calcula expressões matemáticas simples."""
    print(f"[TOOL] Calculando: {expression}")
    try:
        return str(eval(expression))
    except:
        return "Erro no cálculo"

tools = {
    "Wikipedia": search_wikipedia,
    "Calculator": calculator
}

tool_names = list(tools.keys())
tool_descriptions = """\n".join([f"{name}: {func.__doc__}" for name, func in tools.items()])

print("Ferramentas Disponíveis:")
print(tool_descriptions)


# ## 4. O Loop ReAct Manual
# 
# Agora vamos implementar o loop que:
# 1. Chama o LLM com o histórico atual.
# 2. Detecta se o LLM quer executar uma Ação (Regex).
# 3. Se sim, executa a ação e anexa o resultado (`Observation`).
# 4. Se não (ou se for `Final Answer`), termina.



from langchain_google_genai import ChatGoogleGenerativeAI
import re

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

def run_agent_step(prompt_so_far, max_steps=5):
    step = 0
    while step < max_steps:
        pass # Script-patched: ensure non-empty block
        # 1. Chamar o LLM
        response = llm.invoke(prompt_so_far).content
        prompt_so_far += response # Adiciona a resposta do LLM ao histórico
        
        print(f"\n--- Passo {step+1} LLM Output ---\n{response}")
        
        # 2. Verificar se terminou
        if "Final Answer:" in response:
            return response.split("Final Answer:")[-1].strip()
        
        # 3. Parsear Ação com Regex
        # Procuramos por: Action: Nome\nAction Input: Entrada
        action_match = re.search(r"Action: (.*?)(\n)*Action Input: (.*)", response)
        
        if action_match:
            action_name = action_match.group(1).strip()
            action_input = action_match.group(3).strip()
            
            observation = f"Erro: Ferramenta {action_name} não encontrada."
            
            if action_name in tools:
                observation = tools[action_name](action_input)
            
            observation_str = f"\nObservation: {observation}\nThought:"
            prompt_so_far += observation_str
            print(f"--- Execução Ferramenta ---\n{observation_str}")
            
        else:
            pass # Script-patched: ensure non-empty block
            # Se o LLM não seguiu o formato, tentamos forçar ou paramos
            print("Agente não gerou uma ação válida. Encerrando.")
            break
            
        step += 1
    
    return "Limite de passos atingido sem resposta final."




# Teste 1: Pergunta que exige Tool
question = "Qual é a população do Brasil dividida por 2?"

final_prompt = REACT_PROMPT_TEMPLATE.format(
    tool_descriptions=tool_descriptions,
    tool_names=tool_names,
    input=question
)

result = run_agent_step(final_prompt)
print(f"\n>>> Resposta Final: {result}")


# ### Análise do Prompting
# 
# Perceba que a "inteligência" do agente vem inteiramente do Prompt:
# 1. **Thought:** O modelo "fala consigo mesmo" para planejar.
# 2. **Stop Sequences:** Embora injeções manuais funcionem, frameworks otimizam isso parando a geração assim que veem `Observation:`.
# 
# No próximo notebook, veremos como o LangChain abstrai essa complexidade, mas usa EXATAMENTE a mesma lógica por baixo dos panos.
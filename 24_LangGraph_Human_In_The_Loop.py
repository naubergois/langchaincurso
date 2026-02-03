#!/usr/bin/env python
# coding: utf-8

# # 24. LangGraph: Human-in-the-Loop
# 
# Em sistemas críticos, não queremos que o Agente tome a decisão final sem aprovação. O LangGraph permite pausar a execução, esperar o input humano (aprovar ou editar o estado) e depois continuar.
# 
# **Objetivos:**
# - Usar `MemorySaver` para persistir o estado.
# - Usar `interrupt_before` para pausar.
# - Simular uma aprovação humana.

# # Explicação Detalhada do Assunto
# 
# # 24. LangGraph: Human-in-the-Loop
# 
# Este notebook explora a integração de interação humana em fluxos de trabalho LangGraph, permitindo a criação de sistemas de IA mais seguros e controlados, onde a decisão final não é tomada automaticamente pelo agente, mas sim aprovada (ou editada) por um humano.
# 
# **Conceitos Chave:**
# 
# *   **LangGraph:** Uma estrutura para construir aplicações de IA complexas, modelando-as como grafos, onde cada nó representa uma ação ou componente (ex: um agente, uma ferramenta).
# *   **Checkpointing:** O processo de salvar o estado de execução do grafo em um determinado ponto. Isso permite pausar a execução e retomá-la mais tarde, preservando o progresso.
# *   **Interrupção (`interrupt_before`):** Uma funcionalidade que permite pausar a execução do grafo antes de um determinado nó ser executado, dando a oportunidade para intervenção humana.
# *   **Thread ID:** Um identificador único para cada sessão de execução do grafo, permitindo rastrear e gerenciar o estado da execução.
# *   **Estado (State):** Representa as variáveis e dados que são passados entre os nós do grafo, mantendo o contexto da execução.
# 
# **Objetivos de Aprendizado:**
# 
# Ao concluir este notebook, você será capaz de:
# 
# *   Construir um grafo LangGraph que envolve um agente para escrever um e-mail e um agente para enviá-lo.
# *   Implementar o checkpointing para salvar o estado do grafo durante a execução.
# *   Utilizar a funcionalidade `interrupt_before` para pausar a execução do grafo antes de um nó específico.
# *   Simular a intervenção humana, inspecionando o estado do grafo e tomando decisões (aprovar ou editar).
# *   Entender como a interação humana pode ser integrada em fluxos de trabalho LangGraph para criar sistemas mais seguros e controlados.
# 
# **Importância no Ecossistema LangChain:**
# 
# A capacidade de integrar a intervenção humana é crucial em sistemas de IA que lidam com tarefas críticas ou sensíveis. O LangGraph, com seus recursos de checkpointing e interrupção, oferece uma maneira flexível e poderosa de construir esses sistemas. Ao permitir que humanos revisem e aprovem as decisões tomadas pela IA, podemos garantir que os sistemas de IA sejam usados de forma responsável e ética. Este notebook demonstra como usar esses recursos para criar um fluxo de trabalho onde um rascunho de e-mail gerado por IA é revisado e aprovado por um humano antes de ser enviado, mas os princípios aqui apresentados podem ser aplicados a uma ampla gama de tarefas e domínios.
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

# !pip install -qU langchain langchain-openai langchain-community langgraph # Script-patched




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


# ## 1. Setup do Grafo Simples
# 
# Um agente que escreve um e-mail.



from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI

class State(TypedDict):
    topic: str
    email_draft: str
    feedback: str

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

def writer(state: State):
    print("--- ESCREVENDO RASCUNHO ---")
    msg = f"Escreva um e-mail curto sobre: {state['topic']}."
    if state.get('feedback'):
        msg += f" Considere este feedback: {state['feedback']}"
    res = llm.invoke(msg)
    return {"email_draft": res.content}

def sender(state: State):
    print("--- ENVIANDO E-MAIL (Simulado) ---")
    print(f"ENVIADO: {state['email_draft']}")
    return {}


# ## 2. Checkpointing e Interrupção
# 
# Para pausar, precisamos de um `checkpointer` (memória) e configurar `interrupt_before`.



from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(State)
workflow.add_node("writer", writer)
workflow.add_node("sender", sender)

workflow.add_edge(START, "writer")
workflow.add_edge("writer", "sender")
workflow.add_edge("sender", END)

# Checkpointer em memória
memory = MemorySaver()

# Pausar ANTES de entrar no nó 'sender'
app = workflow.compile(checkpointer=memory, interrupt_before=["sender"])


# ## 3. Rodando até a pausa
# 
# Precisamos de uma `thread_id` para manter a sessão.



thread_config = {"configurable": {"thread_id": "1"}}

# Roda até parar antes do 'sender'
app.invoke({"topic": "Convite para Webinar de IA"}, config=thread_config)


# ## 4. O Humano Intervém
# 
# Agora podemos inspecionar o estado e decidir.



# Pegando o estado atual
state = app.get_state(thread_config)
print("RASCUNHO ATUAL:")
print(state.values['email_draft'])

# Decisão Humana (Simulada)
decisao = "aprovar" # ou "editar"

if decisao == "aprovar":
    print("\nHumano: Aprovado! Continuando...")
    # Continuar de onde parou (None = sem novos inputs)
    app.invoke(None, config=thread_config)
else:
    print("\nHumano: Precisa melhorar...")
    # Atualizamos o estado com feedback e voltamos pro writer (seria outra logica de grafo, mas aqui é só exemplo)
    # Para editar o estado, usaríamos app.update_state(...)


# ## Conclusão
# 
# O `interrupt_before` é poderoso para criar sistemas seguros onde o humano tem a palavra final.
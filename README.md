# Curso Prático de LangChain 🦜🔗

Este repositório contém 10 notebooks Jupyter com exemplos práticos de como usar o LangChain para criar aplicações com LLMs. O curso foi desenhado para ser executado no **Google Colab**.

## Conteúdo

Os notebooks estão organizados de forma progressiva, do básico ao avançado:

1.  **[01_Introducao_LangChain_Modelos.ipynb](./01_Introducao_LangChain_Modelos.ipynb)**: Introdução, instalação e chamadas básicas a ChatModels.
2.  **[02_Prompt_Templates_Parsers.ipynb](./02_Prompt_Templates_Parsers.ipynb)**: Criação de Templates de Prompt e Formatação de Saída (LCEL).
3.  **[03_Memoria.ipynb](./03_Memoria.ipynb)**: Como adicionar memória (histórico) às conversas.
4.  **[04_Chains.ipynb](./04_Chains.ipynb)**: Criando cadeias sequenciais e execução paralela.
5.  **[05_RAG_Document_Loaders.ipynb](./05_RAG_Document_Loaders.ipynb)**: RAG Parte 1 - Carregando e dividindo documentos da web.
6.  **[06_RAG_Embeddings_VectorStores.ipynb](./06_RAG_Embeddings_VectorStores.ipynb)**: RAG Parte 2 - Criando Embeddings e armazenando no FAISS.
7.  **[07_RAG_RetrievalQA.ipynb](./07_RAG_RetrievalQA.ipynb)**: RAG Parte 3 - Chain completa de perguntas e respostas sobre documentos.
8.  **[08_Agentes_Tools_Intro.ipynb](./08_Agentes_Tools_Intro.ipynb)**: Introdução a Agentes e uso de ferramentas prontas (DuckDuckGo).
9.  **[09_Agentes_Tools_Custom.ipynb](./09_Agentes_Tools_Custom.ipynb)**: Criando suas próprias ferramentas (Tools) em Python.
10. **[10_Chatbot_RAG_Completo.ipynb](./10_Chatbot_RAG_Completo.ipynb)**: **Projeto Final** - Chatbot que interage com arquivos PDF (ChatPDF).

## Como Usar

1.  Abra o arquivo `.ipynb` desejado.
2.  Clique no botão "Open in Colab" (se disponível) ou faça upload para o seu Google Drive/Colab.
3.  Você precisará de uma **OpenAI API Key**.
4.  Execute as células sequencialmente.

## Pré-requisitos

- Conta no Google (para usar o Colab).
- Chave de API da OpenAI (paga) ou adaptação para outros modelos (Gemini/Google GenAI, HuggingFace, etc).

## Tecnologias

- LangChain
- OpenAI GPT-3.5 / GPT-4
- FAISS (Vector Database)
- DuckDuckGo Search (Tool)

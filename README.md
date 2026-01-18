# Curso Prático de LangChain 🦜🔗

Este repositório contém **20 notebooks Jupyter** com exemplos práticos de como usar o LangChain, divididos em um módulo fundamental e um **módulo focado em Auditoria**. O curso foi desenhado para ser executado no **Google Colab**.

## Módulo 1: Fundamentos

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

## Módulo 2: Casos de Uso em Auditoria 🕵️‍♂️📋

Este módulo foca na aplicação de IA Generativa para rotinas de Auditores, Analistas de Risco e Compliance.

11. **[11_Auditoria_Analise_Conformidade.ipynb](./11_Auditoria_Analise_Conformidade.ipynb)**: Verificação automática de regras em despesas e transações.
12. **[12_Auditoria_Extracao_Dados_Contratos.ipynb](./12_Auditoria_Extracao_Dados_Contratos.ipynb)**: Extração de dados estruturados (JSON) de textos jurídicos.
13. **[13_Auditoria_Resumo_Relatorios.ipynb](./13_Auditoria_Resumo_Relatorios.ipynb)**: Sumarização de relatórios longos focada em riscos.
14. **[14_Auditoria_Classificacao_Riscos.ipynb](./14_Auditoria_Classificacao_Riscos.ipynb)**: Classificação automática de apontamentos (Alto/Médio/Baixo).
15. **[15_Auditoria_RAG_Legislacao.ipynb](./15_Auditoria_RAG_Legislacao.ipynb)**: Chatbot especialista em legislação específica (ex: Lei das Estatais).
16. **[16_Auditoria_Comparacao_Normas.ipynb](./16_Auditoria_Comparacao_Normas.ipynb)**: Diff semântico entre duas versões de normas internas.
17. **[17_Auditoria_Geracao_Checklists.ipynb](./17_Auditoria_Geracao_Checklists.ipynb)**: Geração de programas de trabalho baseados na descrição do processo.
18. **[18_Auditoria_Escrita_Achados.ipynb](./18_Auditoria_Escrita_Achados.ipynb)**: Reformatação de achados no padrão "5 Cs" (Condition, Criteria, etc).
19. **[19_Auditoria_Deteccao_Anomalias.ipynb](./19_Auditoria_Deteccao_Anomalias.ipynb)**: Detecção de fraude e pressão em e-mails corporativos.

## Módulo 3: Avançado - Pydantic e LangGraph 🤖🕸️

Este módulo explora técnicas modernas de engenharia de software para IA, focando em robustez e agentes complexos.

21. **[21_Pydantic_Fundamentos.ipynb](./21_Pydantic_Fundamentos.ipynb)**: Fundamentos de validação de dados em Python.
22. **[22_LangChain_Structured_Output_Pydantic.ipynb](./22_LangChain_Structured_Output_Pydantic.ipynb)**: Garantindo saídas JSON válidas com modelos de linguagem.
23. **[23_LangGraph_Intro_Fluxos_Ciclicos.ipynb](./23_LangGraph_Intro_Fluxos_Ciclicos.ipynb)**: Introdução a grafos e loops de feedback (não-linear).
24. **[24_LangGraph_Human_In_The_Loop.ipynb](./24_LangGraph_Human_In_The_Loop.ipynb)**: Pausando a execução para aprovação humana segura.
25. **[25_LangGraph_Multi_Agent_Supervisor.ipynb](./25_LangGraph_Multi_Agent_Supervisor.ipynb)**: Arquitetura de Supervisor orquestrando múltiplos agentes especialistas.

## Módulo 4: Engenharia de Prompt ReAct 🧠⚡

Este módulo aprofunda no funcionamento interno dos Agentes, focando na construção de prompts robustos.

26. **[26_ReAct_Fundamentos_Prompting.ipynb](./26_ReAct_Fundamentos_Prompting.ipynb)**: Entendendo e implementando o loop ReAct (Thought/Action/Observation) manualmente em Python.
27. **[27_ReAct_LangChain_Implementation.ipynb](./27_ReAct_LangChain_Implementation.ipynb)**: Usando `create_react_agent` e analisando os prompts padrão do LangChain Hub.
28. **[28_ReAct_Custom_Tools_Error_Handling.ipynb](./28_ReAct_Custom_Tools_Error_Handling.ipynb)**: Criando ferramentas complexas e prompts para recuperação automática de erros.

## Módulo 5: Integração n8n 🟦⚡

Este módulo foca na integração entre Agentes LangChain (Cérebro) e n8n (Músculos).

29. **[29_n8n_Webhook_Client.ipynb](./29_n8n_Webhook_Client.ipynb)**: Usando Tools do LangChain para acionar Webhooks do n8n (Agente -> n8n).
30. **[30_n8n_Python_Node_Prototyping.ipynb](./30_n8n_Python_Node_Prototyping.ipynb)**: Ambiente para prototipar código Python complexo antes de colar no "Code Node" do n8n.


## Como Usar

1.  Abra o arquivo `.ipynb` desejado.
2.  Clique no botão "Open in Colab" (se disponível) ou faça upload para o seu Google Drive/Colab.
3.  Você precisará de uma **OpenAI API Key**.
4.  Execute as células sequencialmente.

## Tecnologias

- LangChain
- OpenAI GPT-3.5 / GPT-4
- FAISS (Vector Database)
- DuckDuckGo Search (Tool)

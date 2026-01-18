# Integração n8n + LangChain 🦜🔗 + 🟦

Esta pasta é dedicada a fluxos de trabalho (workflows) do **n8n** que se integram com os agentes desenvolvidos neste curso.

## O que é n8n?
O n8n é uma ferramenta de automação de fluxo de trabalho "fair-code" que permite conectar qualquer coisa a qualquer coisa via nós visuais. É excelente para orquestrar a entrada e saída de dados para seus Agentes LangChain.

## Rodando no Google Colab ☁️
Para rodar uma instância completa do n8n no Colab (gratuito) e acessar via navegador, use este notebook:
**[01_Rodar_n8n_no_Colab.ipynb](./01_Rodar_n8n_no_Colab.ipynb)**

## Exemplos de Integração (Ideias)

1.  **Webhook Trigger**: Receber uma mensagem do WhatsApp/Slack -> Chamar Agente LangChain via API -> Responder.
2.  **Agendamento**: Rodar um Agente de Análise de Auditoria toda segunda-feira às 8h e enviar relatório por email.
3.  **Human-in-the-loop**: O Agente processa até certo ponto e usa o n8n para mandar um formulário de aprovação para um humano (via Email/Slack).

## Como Importar
Os arquivos `.json` nesta pasta podem ser importados diretamente na UI do n8n via "Import from File".

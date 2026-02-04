# Sistema de Classificação Automática de Riscos de Auditoria

Sistema completo desenvolvido com Streamlit e SQLite para classificação automática de riscos de auditoria usando IA (Google Gemini + LangChain).

## 🎯 Funcionalidades

- **Classificação Automática**: Análise de apontamentos de auditoria com IA
- **Matriz de Riscos**: Classificação em 3 níveis (Alto, Médio, Baixo)
- **Banco de Dados**: Armazenamento persistente em SQLite
- **Dashboard**: Visualizações e estatísticas interativas
- **Histórico**: Consulta e filtro de classificações anteriores
- **Exportação**: Download de dados em formato CSV

## 📋 Pré-requisitos

- Python 3.9+
- Conta Google Cloud com API Key do Gemini
- Arquivo `.env` com a variável `GOOGLE_API_KEY`

## 🚀 Instalação

1. **Instalar dependências:**
```bash
pip install -r requirements_riscos.txt
```

2. **Configurar API Key:**
Crie um arquivo `.env` na raiz do projeto:
```
GOOGLE_API_KEY=sua_chave_aqui
```

## ▶️ Executar a Aplicação

```bash
streamlit run app_classificacao_riscos.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

## 📖 Como Usar

### 1. Classificar Risco

- Acesse a página "🔍 Classificar Risco"
- Digite ou selecione um exemplo de apontamento de auditoria
- Clique em "Classificar Risco"
- Veja o resultado com nível, justificativa e ação sugerida
- A classificação é automaticamente salva no banco de dados

### 2. Visualizar Histórico

- Acesse "📋 Histórico"
- Filtre por nível de risco (Alto, Médio, Baixo)
- Visualize todas as classificações anteriores
- Delete registros específicos se necessário

### 3. Dashboard

- Acesse "📊 Dashboard"
- Veja métricas totais e por nível
- Analise gráficos de distribuição
- Exporte dados para CSV

### 4. Matriz de Riscos

- Acesse "📐 Matriz de Riscos"
- Consulte os critérios de classificação
- Entenda os níveis de prioridade

## 🎨 Matriz de Riscos

### 🔴 RISCO ALTO
- Perda financeira significativa (> R$ 100k)
- Fraude detectada
- Violação legal grave (LGPD, Anticorrupção)
- Risco de imagem corporativa
- **Prioridade**: Ação imediata

### 🟡 RISCO MÉDIO
- Falha de processo repetitiva
- Perda financeira moderada (< R$ 100k)
- Dados imprecisos ou incompletos
- Controles internos fracos
- **Prioridade**: Ação em curto prazo

### 🟢 RISCO BAIXO
- Erros pontuais e isolados
- Documentação faltante não crítica
- Oportunidades de melhoria de eficiência
- Não conformidades menores
- **Prioridade**: Ação em médio prazo

## 🗂️ Estrutura do Projeto

```
langchaincurso/
├── app_classificacao_riscos.py    # Aplicação Streamlit principal
├── database_riscos.py              # Módulo de gerenciamento SQLite
├── requirements_riscos.txt         # Dependências do projeto
├── classificacoes_risco.db         # Banco de dados SQLite (criado automaticamente)
└── .env                            # Variáveis de ambiente (não versionado)
```

## 🛠️ Tecnologias Utilizadas

- **Streamlit**: Interface web interativa
- **LangChain**: Framework para aplicações com LLMs
- **Google Gemini**: Modelo de IA para classificação
- **SQLite**: Banco de dados local
- **Pandas**: Manipulação de dados
- **Plotly**: Visualizações interativas

## 📊 Banco de Dados

### Tabela: classificacoes

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária (auto-incremento) |
| data_hora | TIMESTAMP | Data e hora da classificação |
| apontamento | TEXT | Texto do apontamento |
| nivel_risco | TEXT | Nível de risco (Alto/Médio/Baixo) |
| justificativa | TEXT | Justificativa da classificação |
| acao_sugerida | TEXT | Ação recomendada |

## 🔧 Administração

No menu lateral, acesse "⚙️ Administração" para:
- Ver total de registros
- Limpar todos os dados do banco

## 📝 Exemplos de Uso

### Exemplo 1: Perda de Estoque
**Apontamento**: "O sistema de almoxarifado permite saída de mercadoria sem requisição aprovada. Identificada perda de estoque de R$ 500.000 no ano."

**Resultado Esperado**: Risco Alto

### Exemplo 2: Documentação Incompleta
**Apontamento**: "Três relatórios de despesas de viagem de Junho/2023 estavam sem carimbo da recepção, mas com notas fiscais válidas."

**Resultado Esperado**: Risco Baixo

### Exemplo 3: Conflito de Interesses
**Apontamento**: "Identificamos um funcionário do Depto de Compras que é sócio de um fornecedor recém-contratado sem declaração de conflito de interesses."

**Resultado Esperado**: Risco Alto

## 🤝 Contribuindo

Este projeto foi desenvolvido como parte do curso de LangChain, baseado no exercício 14 (Auditoria: Classificação Automática de Riscos).

## 📄 Licença

Este projeto é parte do material educacional do curso de LangChain.

## 🆘 Suporte

Em caso de problemas:
1. Verifique se a `GOOGLE_API_KEY` está configurada corretamente
2. Confirme que todas as dependências estão instaladas
3. Verifique os logs do Streamlit no terminal

## 🎓 Baseado em

- **Exercício 14**: Auditoria - Classificação Automática de Riscos
- **Notebook**: `14_Auditoria_Classificacao_Riscos.ipynb`

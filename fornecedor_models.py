"""
Modelos Pydantic para o Sistema de Gestão de Riscos de Fornecedores.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class TipoQuestao(str, Enum):
    """Tipos de questões disponíveis."""
    SIM_NAO = "sim_nao"
    MULTIPLA_ESCOLHA = "multipla_escolha"
    TEXTO_LIVRE = "texto_livre"
    NUMERICO = "numerico"
    DATA = "data"


class NivelGravidade(str, Enum):
    """Níveis de gravidade de discrepâncias."""
    BAIXO = "Baixo"
    MEDIO = "Médio"
    ALTO = "Alto"


class ClassificacaoRisco(str, Enum):
    """Classificação geral de risco do fornecedor."""
    BAIXO_RISCO = "Baixo Risco"
    MEDIO_RISCO = "Médio Risco"
    ALTO_RISCO = "Alto Risco"


# ============================================================================
# DADOS DA RECEITA FEDERAL
# ============================================================================

class DadosReceita(BaseModel):
    """Dados obtidos da Receita Federal (ou mock)."""
    cnpj: str = Field(description="CNPJ formatado")
    razao_social: str = Field(description="Razão social da empresa")
    nome_fantasia: Optional[str] = Field(default=None, description="Nome fantasia")
    situacao_cadastral: str = Field(description="Ativa, Suspensa, Inapta, Baixada")
    data_situacao_cadastral: str = Field(description="Data da situação cadastral")
    capital_social: float = Field(description="Capital social em R$")
    natureza_juridica: str = Field(description="Código da natureza jurídica")
    porte: str = Field(description="ME, EPP, Demais")
    atividade_principal: str = Field(description="CNAE principal")
    data_abertura: str = Field(description="Data de abertura da empresa")
    logradouro: str = Field(description="Endereço")
    numero: str = Field(description="Número")
    municipio: str = Field(description="Município")
    uf: str = Field(description="UF")
    cep: str = Field(description="CEP")
    telefone: Optional[str] = Field(default=None, description="Telefone")
    email: Optional[str] = Field(default=None, description="E-mail")
    
    # Certidões (simuladas)
    certidao_federal_valida: bool = Field(default=True, description="CND Federal válida")
    certidao_fgts_valida: bool = Field(default=True, description="CRF FGTS válida")
    certidao_trabalhista_valida: bool = Field(default=True, description="CNDT válida")
    
    # Dados adicionais
    qtd_funcionarios: Optional[int] = Field(default=None, description="Quantidade de funcionários")
    faturamento_anual: Optional[float] = Field(default=None, description="Faturamento anual estimado")


# ============================================================================
# QUESTIONÁRIOS
# ============================================================================

class Questao(BaseModel):
    """Modelo de uma questão do questionário."""
    id: str = Field(description="ID único da questão")
    categoria: str = Field(description="Categoria de risco")
    texto: str = Field(description="Texto da pergunta")
    tipo: TipoQuestao = Field(description="Tipo da questão")
    opcoes: Optional[List[str]] = Field(default=None, description="Opções para múltipla escolha")
    peso_risco: float = Field(description="Peso da questão no cálculo de risco (0.0 a 1.0)")
    campo_validacao: Optional[str] = Field(
        default=None,
        description="Campo dos dados da Receita para validação"
    )


class Resposta(BaseModel):
    """Resposta a uma questão."""
    questao_id: str = Field(description="ID da questão")
    valor: str = Field(description="Valor da resposta")
    data_resposta: datetime = Field(default_factory=datetime.now)


class QuestionarioResposta(BaseModel):
    """Questionário completo respondido."""
    fornecedor_cnpj: str = Field(description="CNPJ do fornecedor")
    data_inicio: datetime = Field(default_factory=datetime.now)
    data_conclusao: Optional[datetime] = Field(default=None)
    respostas: List[Resposta] = Field(default_factory=list)
    pontuacao_total: float = Field(default=0.0, description="Pontuação total calculada")


# ============================================================================
# FORNECEDOR
# ============================================================================

class Fornecedor(BaseModel):
    """Modelo completo de um fornecedor."""
    cnpj: str = Field(description="CNPJ do fornecedor")
    dados_receita: DadosReceita = Field(description="Dados da Receita Federal")
    questionario: Optional[QuestionarioResposta] = Field(
        default=None,
        description="Questionário respondido"
    )
    data_cadastro: datetime = Field(default_factory=datetime.now)
    
    # Contrato
    numero_contrato: Optional[str] = Field(default=None)
    objeto_contrato: Optional[str] = Field(default=None)
    valor_contrato: Optional[float] = Field(default=None)
    gestor_contrato: Optional[str] = Field(default=None)
    fiscal_contrato: Optional[str] = Field(default=None)


# ============================================================================
# ANÁLISE DE RISCOS
# ============================================================================

class AnaliseDiscrepancia(BaseModel):
    """Análise de discrepância entre resposta e dado oficial."""
    questao_id: str = Field(description="ID da questão")
    questao_texto: str = Field(description="Texto da questão")
    resposta_fornecedor: str = Field(description="Resposta fornecida")
    dado_oficial: str = Field(description="Dado oficial da Receita")
    discrepancia_detectada: bool = Field(description="Se há discrepância")
    nivel_gravidade: NivelGravidade = Field(description="Nível de gravidade")
    explicacao: str = Field(description="Explicação da discrepância")
    impacto: str = Field(description="Impacto no contrato")


class RiscoCategoria(BaseModel):
    """Análise de risco por categoria."""
    categoria: str = Field(description="Nome da categoria")
    pontuacao: float = Field(description="Pontuação de 0 a 10")
    nivel_risco: str = Field(description="Baixo, Médio ou Alto")
    questoes_respondidas: int = Field(description="Quantidade de questões")
    discrepancias: int = Field(description="Quantidade de discrepâncias")
    principais_problemas: List[str] = Field(default_factory=list)


class Recomendacao(BaseModel):
    """Recomendação de ação."""
    prioridade: str = Field(description="Alta, Média, Baixa")
    categoria: str = Field(description="Categoria de risco relacionada")
    titulo: str = Field(description="Título da recomendação")
    descricao: str = Field(description="Descrição detalhada")
    prazo_sugerido: str = Field(description="Prazo para implementação")
    responsavel: str = Field(description="Gestor ou Fiscal")


# ============================================================================
# RELATÓRIO
# ============================================================================

class RelatorioFornecedor(BaseModel):
    """Relatório completo de análise de fornecedor."""
    # Identificação
    fornecedor_cnpj: str
    razao_social: str
    data_geracao: datetime = Field(default_factory=datetime.now)
    
    # Análise geral
    pontuacao_geral: float = Field(description="Pontuação de 0 a 10")
    classificacao: ClassificacaoRisco = Field(description="Classificação de risco")
    
    # Análise por categoria
    analise_por_categoria: Dict[str, RiscoCategoria] = Field(
        description="Análise detalhada por categoria"
    )
    
    # Discrepâncias
    total_discrepancias: int = Field(description="Total de discrepâncias encontradas")
    discrepancias_criticas: int = Field(description="Discrepâncias de alta gravidade")
    lista_discrepancias: List[AnaliseDiscrepancia] = Field(default_factory=list)
    
    # Recomendações
    recomendacoes: List[Recomendacao] = Field(default_factory=list)
    
    # Resumo executivo
    resumo_executivo: str = Field(description="Resumo para gestores")
    principais_riscos: List[str] = Field(default_factory=list)
    pontos_positivos: List[str] = Field(default_factory=list)
    
    # Decisão sugerida
    decisao_sugerida: str = Field(
        description="Aprovar, Aprovar com Ressalvas, Rejeitar"
    )
    justificativa_decisao: str = Field(description="Justificativa da decisão")

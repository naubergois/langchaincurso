"""
Modelos Pydantic para estruturação de dados de notícias do TCU.
"""
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from datetime import datetime


class NoticiaBasica(BaseModel):
    """Modelo básico de uma notícia do TCU."""
    titulo: str = Field(description="Título da notícia")
    data: str = Field(description="Data de publicação (formato: DD/MM/YYYY)")
    url: str = Field(description="URL completa da notícia")
    resumo: Optional[str] = Field(default=None, description="Resumo ou lead da notícia")


class NoticiaCompleta(NoticiaBasica):
    """Modelo completo de uma notícia com conteúdo detalhado."""
    conteudo: str = Field(description="Conteúdo completo da notícia")
    temas: List[str] = Field(default_factory=list, description="Temas/categorias da notícia")
    autor: Optional[str] = Field(default=None, description="Autor da notícia")


class AnaliseNoticia(BaseModel):
    """Análise estruturada de uma notícia usando LLM."""
    categoria: str = Field(description="Categoria principal da notícia (ex: Fiscalização, Jurídico, Institucional)")
    relevancia: str = Field(description="Nível de relevância: Alta, Média ou Baixa")
    palavras_chave: List[str] = Field(description="Principais palavras-chave extraídas")
    resumo_executivo: str = Field(description="Resumo executivo em 2-3 frases")
    impacto: str = Field(description="Descrição do impacto ou importância da notícia")
    entidades_mencionadas: List[str] = Field(
        default_factory=list,
        description="Órgãos, empresas ou entidades mencionadas"
    )


class NoticiaAnalisada(BaseModel):
    """Notícia completa com análise."""
    noticia: NoticiaCompleta
    analise: AnaliseNoticia


class RelatorioExecutivo(BaseModel):
    """Relatório executivo consolidado de múltiplas notícias."""
    periodo: str = Field(description="Período analisado")
    total_noticias: int = Field(description="Número total de notícias analisadas")
    data_geracao: str = Field(description="Data de geração do relatório")
    
    # Estatísticas
    distribuicao_categorias: dict = Field(
        description="Distribuição de notícias por categoria"
    )
    distribuicao_relevancia: dict = Field(
        description="Distribuição por nível de relevância"
    )
    
    # Principais temas
    principais_temas: List[str] = Field(
        description="Temas mais frequentes nas notícias"
    )
    principais_entidades: List[str] = Field(
        description="Entidades mais mencionadas"
    )
    
    # Destaques
    noticias_alta_relevancia: List[dict] = Field(
        description="Notícias de alta relevância com título e resumo"
    )
    
    # Insights
    insights_principais: List[str] = Field(
        description="Principais insights e tendências identificadas"
    )
    
    resumo_geral: str = Field(
        description="Resumo geral do período analisado"
    )

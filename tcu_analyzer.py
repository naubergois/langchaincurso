"""
Analisador de notícias do TCU usando LangChain e Google Gemini.
"""
import os
from typing import List
from datetime import datetime
from collections import Counter

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from tcu_models import (
    NoticiaCompleta,
    AnaliseNoticia,
    NoticiaAnalisada,
    RelatorioExecutivo
)


class TCUAnalyzer:
    """Analisador de notícias usando LLM."""
    
    def __init__(self, model: str = "gemini-2.0-flash", temperature: float = 0):
        """
        Inicializa o analisador.
        
        Args:
            model: Nome do modelo Gemini a usar
            temperature: Temperatura para geração (0 = determinístico)
        """
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
        self.structured_llm = self.llm.with_structured_output(AnaliseNoticia)
    
    def analisar_noticia(self, noticia: NoticiaCompleta) -> AnaliseNoticia:
        """
        Analisa uma notícia e extrai informações estruturadas.
        
        Args:
            noticia: Notícia completa a ser analisada
            
        Returns:
            AnaliseNoticia com informações extraídas
        """
        sistema = """
Você é um especialista em análise de notícias do Tribunal de Contas da União (TCU).

Analise a notícia fornecida e extraia as seguintes informações:

1. **Categoria**: Classifique em uma das categorias principais:
   - Fiscalização (auditorias, inspeções, monitoramentos)
   - Jurídico (acórdãos, decisões, processos)
   - Institucional (eventos, nomeações, comunicados)
   - Obras e Infraestrutura
   - Gestão Pública
   - Transparência e Controle
   - Outros

2. **Relevância**: Avalie como Alta, Média ou Baixa considerando:
   - Impacto financeiro
   - Abrangência (nacional, regional, local)
   - Interesse público
   - Urgência

3. **Palavras-chave**: Identifique 3-5 palavras-chave principais

4. **Resumo Executivo**: Crie um resumo objetivo em 2-3 frases

5. **Impacto**: Descreva brevemente o impacto ou importância da notícia

6. **Entidades Mencionadas**: Liste órgãos, empresas ou entidades citadas
"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", sistema),
            ("human", """
Título: {titulo}
Data: {data}
Conteúdo: {conteudo}

Analise esta notícia do TCU.
""")
        ]) | self.structured_llm
        
        resultado = prompt.invoke({
            "titulo": noticia.titulo,
            "data": noticia.data,
            "conteudo": noticia.conteudo[:3000]  # Limitar tamanho para evitar tokens excessivos
        })
        
        return resultado
    
    def analisar_noticias(self, noticias: List[NoticiaCompleta]) -> List[NoticiaAnalisada]:
        """
        Analisa múltiplas notícias.
        
        Args:
            noticias: Lista de notícias a analisar
            
        Returns:
            Lista de NoticiaAnalisada
        """
        noticias_analisadas = []
        
        print(f"🔍 Analisando {len(noticias)} notícias com IA...\n")
        
        for i, noticia in enumerate(noticias, 1):
            print(f"[{i}/{len(noticias)}] Analisando: {noticia.titulo[:60]}...")
            
            try:
                analise = self.analisar_noticia(noticia)
                
                noticia_analisada = NoticiaAnalisada(
                    noticia=noticia,
                    analise=analise
                )
                
                noticias_analisadas.append(noticia_analisada)
                print(f"  ✓ Categoria: {analise.categoria} | Relevância: {analise.relevancia}\n")
                
            except Exception as e:
                print(f"  ❌ Erro na análise: {e}\n")
                continue
        
        print(f"✅ {len(noticias_analisadas)} notícias analisadas!\n")
        return noticias_analisadas
    
    def gerar_relatorio_executivo(
        self,
        noticias_analisadas: List[NoticiaAnalisada]
    ) -> RelatorioExecutivo:
        """
        Gera relatório executivo consolidado.
        
        Args:
            noticias_analisadas: Lista de notícias analisadas
            
        Returns:
            RelatorioExecutivo
        """
        print("📊 Gerando relatório executivo...\n")
        
        # Estatísticas
        categorias = [n.analise.categoria for n in noticias_analisadas]
        relevancia = [n.analise.relevancia for n in noticias_analisadas]
        
        distribuicao_categorias = dict(Counter(categorias))
        distribuicao_relevancia = dict(Counter(relevancia))
        
        # Principais temas (palavras-chave mais frequentes)
        todas_palavras = []
        for n in noticias_analisadas:
            todas_palavras.extend(n.analise.palavras_chave)
        
        principais_temas = [palavra for palavra, _ in Counter(todas_palavras).most_common(10)]
        
        # Principais entidades
        todas_entidades = []
        for n in noticias_analisadas:
            todas_entidades.extend(n.analise.entidades_mencionadas)
        
        principais_entidades = [ent for ent, _ in Counter(todas_entidades).most_common(10)]
        
        # Notícias de alta relevância
        noticias_alta = [
            {
                "titulo": n.noticia.titulo,
                "resumo": n.analise.resumo_executivo,
                "categoria": n.analise.categoria,
                "url": n.noticia.url
            }
            for n in noticias_analisadas
            if n.analise.relevancia == "Alta"
        ]
        
        # Gerar insights usando LLM
        insights = self._gerar_insights(noticias_analisadas)
        resumo_geral = self._gerar_resumo_geral(noticias_analisadas)
        
        # Período
        if noticias_analisadas:
            datas = [n.noticia.data for n in noticias_analisadas if n.noticia.data]
            periodo = f"Últimas {len(noticias_analisadas)} notícias"
        else:
            periodo = "Sem período definido"
        
        relatorio = RelatorioExecutivo(
            periodo=periodo,
            total_noticias=len(noticias_analisadas),
            data_geracao=datetime.now().strftime("%d/%m/%Y %H:%M"),
            distribuicao_categorias=distribuicao_categorias,
            distribuicao_relevancia=distribuicao_relevancia,
            principais_temas=principais_temas,
            principais_entidades=principais_entidades,
            noticias_alta_relevancia=noticias_alta,
            insights_principais=insights,
            resumo_geral=resumo_geral
        )
        
        print("✅ Relatório executivo gerado!\n")
        return relatorio
    
    def _gerar_insights(self, noticias_analisadas: List[NoticiaAnalisada]) -> List[str]:
        """Gera insights principais usando LLM."""
        
        # Preparar contexto
        contexto = "\n\n".join([
            f"- {n.noticia.titulo} ({n.analise.categoria}, {n.analise.relevancia}): {n.analise.resumo_executivo}"
            for n in noticias_analisadas[:10]  # Limitar para evitar tokens excessivos
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um analista do TCU. Analise as notícias fornecidas e identifique 
3-5 insights principais, tendências ou padrões importantes. Seja conciso e objetivo."""),
            ("human", "Notícias:\n{contexto}\n\nQuais são os principais insights?")
        ])
        
        chain = prompt | self.llm
        
        try:
            resultado = chain.invoke({"contexto": contexto})
            # Dividir em lista de insights
            insights_text = resultado.content
            insights = [line.strip("- ").strip() for line in insights_text.split("\n") if line.strip()]
            return insights[:5]
        except:
            return ["Análise de insights não disponível"]
    
    def _gerar_resumo_geral(self, noticias_analisadas: List[NoticiaAnalisada]) -> str:
        """Gera resumo geral do período."""
        
        contexto = "\n\n".join([
            f"- {n.noticia.titulo}: {n.analise.resumo_executivo}"
            for n in noticias_analisadas[:10]
        ])
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um analista do TCU. Crie um resumo executivo geral 
(2-3 parágrafos) das principais atividades e notícias do período."""),
            ("human", "Notícias:\n{contexto}\n\nResumo geral:")
        ])
        
        chain = prompt | self.llm
        
        try:
            resultado = chain.invoke({"contexto": contexto})
            return resultado.content
        except:
            return "Resumo geral não disponível"

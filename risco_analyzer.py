"""
Analisador de riscos de fornecedores usando LangChain e Google Gemini.
Compara respostas do questionário com dados oficiais e gera recomendações.
"""
import os
from typing import List, Dict
from datetime import datetime
from collections import Counter

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

from fornecedor_models import (
    AnaliseDiscrepancia, NivelGravidade, RiscoCategoria,
    Recomendacao, RelatorioFornecedor, ClassificacaoRisco,
    Fornecedor, DadosReceita
)
from questionario_engine import QuestionarioEngine

load_dotenv()


class RiscoAnalyzer:
    """Analisador de riscos usando IA."""
    
    def __init__(self, model: str = "gemini-2.0-flash", temperature: float = 0):
        self.llm = ChatGoogleGenerativeAI(model=model, temperature=temperature)
        self.engine = QuestionarioEngine()
    
    def analisar_discrepancia(
        self,
        questao_id: str,
        resposta_fornecedor: str,
        dado_oficial: str
    ) -> AnaliseDiscrepancia:
        """
        Analisa discrepância entre resposta e dado oficial usando IA.
        """
        questao = self.engine.obter_questao(questao_id)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um auditor especialista em gestão de riscos de fornecedores.

Analise a discrepância entre a informação fornecida pelo fornecedor e o dado oficial.

Determine:
1. Se há discrepância real (Sim/Não)
2. Nível de gravidade (Baixo/Médio/Alto)
3. Explicação clara da discrepância
4. Impacto potencial no contrato

Seja objetivo e técnico."""),
            ("human", """
Questão: {questao_texto}
Resposta do Fornecedor: {resposta}
Dado Oficial: {dado_oficial}

Analise a discrepância.""")
        ])
        
        chain = prompt | self.llm
        
        try:
            resultado = chain.invoke({
                "questao_texto": questao.texto,
                "resposta": resposta_fornecedor,
                "dado_oficial": dado_oficial
            })
            
            conteudo = resultado.content.lower()
            
            # Detectar discrepância
            tem_discrepancia = any(palavra in conteudo for palavra in ["discrepância", "divergência", "diferença", "incompatível"])
            
            # Detectar gravidade
            if "alto" in conteudo or "grave" in conteudo or "crítico" in conteudo:
                gravidade = NivelGravidade.ALTO
            elif "médio" in conteudo or "moderado" in conteudo:
                gravidade = NivelGravidade.MEDIO
            else:
                gravidade = NivelGravidade.BAIXO
            
            # Extrair explicação e impacto
            linhas = resultado.content.split("\n")
            explicacao = resultado.content[:200] + "..." if len(resultado.content) > 200 else resultado.content
            impacto = "Verificar documentação e solicitar esclarecimentos ao fornecedor."
            
            return AnaliseDiscrepancia(
                questao_id=questao_id,
                questao_texto=questao.texto,
                resposta_fornecedor=resposta_fornecedor,
                dado_oficial=dado_oficial,
                discrepancia_detectada=tem_discrepancia,
                nivel_gravidade=gravidade,
                explicacao=explicacao,
                impacto=impacto
            )
            
        except Exception as e:
            # Fallback sem IA
            return AnaliseDiscrepancia(
                questao_id=questao_id,
                questao_texto=questao.texto,
                resposta_fornecedor=resposta_fornecedor,
                dado_oficial=dado_oficial,
                discrepancia_detectada=resposta_fornecedor != dado_oficial,
                nivel_gravidade=NivelGravidade.MEDIO,
                explicacao=f"Divergência detectada entre resposta e dado oficial. Erro na análise: {str(e)}",
                impacto="Requer verificação manual."
            )
    
    def gerar_relatorio(self, fornecedor: Fornecedor) -> RelatorioFornecedor:
        """
        Gera relatório completo de análise de fornecedor.
        """
        print(f"📊 Gerando relatório para {fornecedor.dados_receita.razao_social}...")
        
        if not fornecedor.questionario:
            raise ValueError("Fornecedor não possui questionário respondido")
        
        # 1. Analisar discrepâncias
        discrepancias = self._analisar_todas_discrepancias(fornecedor)
        
        # 2. Calcular pontuações
        pontuacoes = self.engine.calcular_pontuacao(
            fornecedor.questionario.respostas,
            fornecedor.dados_receita.model_dump()
        )
        
        # 3. Análise por categoria
        analise_categorias = self._analisar_por_categoria(
            fornecedor.questionario.respostas,
            discrepancias,
            pontuacoes
        )
        
        # 4. Classificação geral
        pontuacao_geral = pontuacoes["Total"]
        if pontuacao_geral >= 7.0:
            classificacao = ClassificacaoRisco.BAIXO_RISCO
        elif pontuacao_geral >= 4.0:
            classificacao = ClassificacaoRisco.MEDIO_RISCO
        else:
            classificacao = ClassificacaoRisco.ALTO_RISCO
        
        # 5. Gerar recomendações
        recomendacoes = self._gerar_recomendacoes(
            discrepancias,
            analise_categorias,
            classificacao
        )
        
        # 6. Resumo executivo
        resumo = self._gerar_resumo_executivo(
            fornecedor,
            pontuacao_geral,
            classificacao,
            discrepancias
        )
        
        # 7. Decisão sugerida
        decisao, justificativa = self._sugerir_decisao(
            classificacao,
            len([d for d in discrepancias if d.nivel_gravidade == NivelGravidade.ALTO])
        )
        
        # Principais riscos e pontos positivos
        principais_riscos = [d.explicacao[:100] for d in discrepancias if d.discrepancia_detectada][:5]
        pontos_positivos = self._identificar_pontos_positivos(fornecedor, pontuacoes)
        
        relatorio = RelatorioFornecedor(
            fornecedor_cnpj=fornecedor.cnpj,
            razao_social=fornecedor.dados_receita.razao_social,
            pontuacao_geral=pontuacao_geral,
            classificacao=classificacao,
            analise_por_categoria=analise_categorias,
            total_discrepancias=len(discrepancias),
            discrepancias_criticas=len([d for d in discrepancias if d.nivel_gravidade == NivelGravidade.ALTO]),
            lista_discrepancias=discrepancias,
            recomendacoes=recomendacoes,
            resumo_executivo=resumo,
            principais_riscos=principais_riscos,
            pontos_positivos=pontos_positivos,
            decisao_sugerida=decisao,
            justificativa_decisao=justificativa
        )
        
        print("✅ Relatório gerado com sucesso!\n")
        return relatorio
    
    def _analisar_todas_discrepancias(self, fornecedor: Fornecedor) -> List[AnaliseDiscrepancia]:
        """Analisa todas as discrepâncias entre respostas e dados oficiais."""
        discrepancias = []
        dados_receita = fornecedor.dados_receita.model_dump()
        
        for resposta in fornecedor.questionario.respostas:
            questao = self.engine.obter_questao(resposta.questao_id)
            
            if not questao or not questao.campo_validacao:
                continue
            
            # Obter dado oficial
            dado_oficial = dados_receita.get(questao.campo_validacao)
            if dado_oficial is None:
                continue
            
            # Converter para string para comparação
            dado_oficial_str = str(dado_oficial)
            resposta_str = str(resposta.valor)
            
            # Verificar discrepância
            if self._tem_discrepancia(questao.tipo.value, resposta_str, dado_oficial_str):
                analise = self.analisar_discrepancia(
                    questao.id,
                    resposta_str,
                    dado_oficial_str
                )
                if analise.discrepancia_detectada:
                    discrepancias.append(analise)
        
        return discrepancias
    
    def _tem_discrepancia(self, tipo_questao: str, resposta: str, dado_oficial: str) -> bool:
        """Verifica se há discrepância significativa."""
        if tipo_questao == "sim_nao":
            return resposta.lower() != dado_oficial.lower()
        elif tipo_questao == "multipla_escolha":
            return resposta.lower() not in dado_oficial.lower()
        elif tipo_questao == "numerico":
            try:
                diff = abs(float(resposta) - float(dado_oficial))
                return diff > float(dado_oficial) * 0.1  # 10% de tolerância
            except:
                return False
        else:
            return resposta.lower() != dado_oficial.lower()
    
    def _analisar_por_categoria(
        self,
        respostas,
        discrepancias,
        pontuacoes
    ) -> Dict[str, RiscoCategoria]:
        """Analisa riscos por categoria."""
        analise = {}
        
        for categoria in self.engine.listar_categorias():
            questoes_cat = [r for r in respostas if self.engine.obter_questao(r.questao_id).categoria == categoria]
            disc_cat = [d for d in discrepancias if self.engine.obter_questao(d.questao_id).categoria == categoria]
            
            pontuacao = pontuacoes.get(categoria, 5.0)
            
            if pontuacao >= 7.0:
                nivel = "Baixo"
            elif pontuacao >= 4.0:
                nivel = "Médio"
            else:
                nivel = "Alto"
            
            problemas = [d.explicacao[:80] + "..." for d in disc_cat if d.discrepancia_detectada][:3]
            
            analise[categoria] = RiscoCategoria(
                categoria=categoria,
                pontuacao=pontuacao,
                nivel_risco=nivel,
                questoes_respondidas=len(questoes_cat),
                discrepancias=len(disc_cat),
                principais_problemas=problemas
            )
        
        return analise
    
    def _gerar_recomendacoes(
        self,
        discrepancias,
        analise_categorias,
        classificacao
    ) -> List[Recomendacao]:
        """Gera recomendações baseadas na análise."""
        recomendacoes = []
        
        # Recomendações por discrepâncias críticas
        for disc in discrepancias:
            if disc.nivel_gravidade == NivelGravidade.ALTO:
                recomendacoes.append(Recomendacao(
                    prioridade="Alta",
                    categoria=self.engine.obter_questao(disc.questao_id).categoria,
                    titulo=f"Verificar: {disc.questao_texto[:50]}...",
                    descricao=disc.explicacao,
                    prazo_sugerido="Imediato",
                    responsavel="Gestor do Contrato"
                ))
        
        # Recomendações por categoria de alto risco
        for cat, analise in analise_categorias.items():
            if analise.nivel_risco == "Alto":
                recomendacoes.append(Recomendacao(
                    prioridade="Alta",
                    categoria=cat,
                    titulo=f"Revisar categoria {cat}",
                    descricao=f"Categoria apresenta risco alto com {analise.discrepancias} discrepâncias.",
                    prazo_sugerido="7 dias",
                    responsavel="Fiscal do Contrato"
                ))
        
        # Recomendação geral baseada na classificação
        if classificacao == ClassificacaoRisco.ALTO_RISCO:
            recomendacoes.append(Recomendacao(
                prioridade="Alta",
                categoria="Geral",
                titulo="Aumentar frequência de fiscalização",
                descricao="Fornecedor classificado como alto risco. Recomenda-se fiscalização mensal.",
                prazo_sugerido="Imediato",
                responsavel="Gestor e Fiscal"
            ))
        
        return recomendacoes[:10]  # Limitar a 10 recomendações
    
    def _gerar_resumo_executivo(
        self,
        fornecedor,
        pontuacao,
        classificacao,
        discrepancias
    ) -> str:
        """Gera resumo executivo do relatório."""
        return f"""
O fornecedor {fornecedor.dados_receita.razao_social} (CNPJ: {fornecedor.cnpj}) foi avaliado e classificado como {classificacao.value}.

Pontuação geral: {pontuacao:.1f}/10.0

Foram identificadas {len(discrepancias)} discrepâncias entre as informações fornecidas e os dados oficiais, sendo {len([d for d in discrepancias if d.nivel_gravidade == NivelGravidade.ALTO])} de alta gravidade.

A empresa está {fornecedor.dados_receita.situacao_cadastral.lower()} na Receita Federal e possui capital social de R$ {fornecedor.dados_receita.capital_social:,.2f}.

Recomenda-se atenção especial aos pontos críticos identificados neste relatório.
        """.strip()
    
    def _identificar_pontos_positivos(self, fornecedor, pontuacoes) -> List[str]:
        """Identifica pontos positivos do fornecedor."""
        positivos = []
        
        if fornecedor.dados_receita.situacao_cadastral == "Ativa":
            positivos.append("Situação cadastral ativa na Receita Federal")
        
        if fornecedor.dados_receita.certidao_federal_valida:
            positivos.append("Certidão Federal válida")
        
        if fornecedor.dados_receita.certidao_fgts_valida:
            positivos.append("Regularidade com FGTS")
        
        for cat, pont in pontuacoes.items():
            if cat != "Total" and pont >= 8.0:
                positivos.append(f"Excelente pontuação em {cat} ({pont:.1f}/10)")
        
        return positivos[:5]
    
    def _sugerir_decisao(self, classificacao, discrepancias_criticas) -> tuple:
        """Sugere decisão sobre o fornecedor."""
        if classificacao == ClassificacaoRisco.BAIXO_RISCO and discrepancias_criticas == 0:
            return "Aprovar", "Fornecedor apresenta baixo risco e não possui discrepâncias críticas."
        elif classificacao == ClassificacaoRisco.MEDIO_RISCO or discrepancias_criticas <= 2:
            return "Aprovar com Ressalvas", "Fornecedor apresenta riscos moderados. Recomenda-se fiscalização reforçada."
        else:
            return "Rejeitar", "Fornecedor apresenta alto risco e múltiplas discrepâncias críticas."

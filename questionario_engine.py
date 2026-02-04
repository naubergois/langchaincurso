"""
Motor de questionários dinâmicos para avaliação de riscos de fornecedores.
"""
from typing import List, Dict
from fornecedor_models import (
    Questao, TipoQuestao, QuestionarioResposta, Resposta
)


class QuestionarioEngine:
    """Motor de geração e gerenciamento de questionários."""
    
    # Definição de questões por categoria
    QUESTOES_POR_CATEGORIA = {
        "Compliance": [
            Questao(
                id="COMP_001",
                categoria="Compliance",
                texto="A empresa possui Certidão Negativa de Débitos Federais (CND) válida?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.9,
                campo_validacao="certidao_federal_valida"
            ),
            Questao(
                id="COMP_002",
                categoria="Compliance",
                texto="A empresa possui Certificado de Regularidade do FGTS (CRF) válido?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.9,
                campo_validacao="certidao_fgts_valida"
            ),
            Questao(
                id="COMP_003",
                categoria="Compliance",
                texto="A empresa possui Certidão Negativa de Débitos Trabalhistas (CNDT) válida?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.9,
                campo_validacao="certidao_trabalhista_valida"
            ),
            Questao(
                id="COMP_004",
                categoria="Compliance",
                texto="Qual a situação cadastral da empresa na Receita Federal?",
                tipo=TipoQuestao.MULTIPLA_ESCOLHA,
                opcoes=["Ativa", "Suspensa", "Inapta", "Baixada"],
                peso_risco=1.0,
                campo_validacao="situacao_cadastral"
            ),
            Questao(
                id="COMP_005",
                categoria="Compliance",
                texto="A empresa já sofreu alguma sanção administrativa nos últimos 5 anos?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.8
            ),
        ],
        
        "Financeiro": [
            Questao(
                id="FIN_001",
                categoria="Financeiro",
                texto="Qual o capital social da empresa (em R$)?",
                tipo=TipoQuestao.NUMERICO,
                peso_risco=0.7,
                campo_validacao="capital_social"
            ),
            Questao(
                id="FIN_002",
                categoria="Financeiro",
                texto="Qual o faturamento anual da empresa (em R$)?",
                tipo=TipoQuestao.NUMERICO,
                peso_risco=0.8,
                campo_validacao="faturamento_anual"
            ),
            Questao(
                id="FIN_003",
                categoria="Financeiro",
                texto="Qual o porte da empresa?",
                tipo=TipoQuestao.MULTIPLA_ESCOLHA,
                opcoes=["ME - Microempresa", "EPP - Empresa de Pequeno Porte", "Demais"],
                peso_risco=0.5,
                campo_validacao="porte"
            ),
            Questao(
                id="FIN_004",
                categoria="Financeiro",
                texto="A empresa possui histórico de inadimplência nos últimos 2 anos?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.9
            ),
            Questao(
                id="FIN_005",
                categoria="Financeiro",
                texto="A empresa possui capacidade financeira para executar o contrato?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.9
            ),
        ],
        
        "Operacional": [
            Questao(
                id="OPER_001",
                categoria="Operacional",
                texto="Quantos funcionários a empresa possui atualmente?",
                tipo=TipoQuestao.NUMERICO,
                peso_risco=0.6,
                campo_validacao="qtd_funcionarios"
            ),
            Questao(
                id="OPER_002",
                categoria="Operacional",
                texto="Há quantos anos a empresa está em atividade?",
                tipo=TipoQuestao.NUMERICO,
                peso_risco=0.7,
                campo_validacao="data_abertura"
            ),
            Questao(
                id="OPER_003",
                categoria="Operacional",
                texto="A empresa possui certificações técnicas necessárias para o objeto do contrato?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.8
            ),
            Questao(
                id="OPER_004",
                categoria="Operacional",
                texto="A empresa possui infraestrutura adequada para execução do contrato?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.7
            ),
            Questao(
                id="OPER_005",
                categoria="Operacional",
                texto="Qual a atividade principal da empresa (CNAE)?",
                tipo=TipoQuestao.TEXTO_LIVRE,
                peso_risco=0.6,
                campo_validacao="atividade_principal"
            ),
        ],
        
        "Reputacional": [
            Questao(
                id="REP_001",
                categoria="Reputacional",
                texto="A empresa já executou contratos com outros órgãos públicos?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.5
            ),
            Questao(
                id="REP_002",
                categoria="Reputacional",
                texto="A empresa possui avaliações negativas em contratos anteriores?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.8
            ),
            Questao(
                id="REP_003",
                categoria="Reputacional",
                texto="A empresa possui processos judiciais em andamento?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.7
            ),
            Questao(
                id="REP_004",
                categoria="Reputacional",
                texto="A empresa já teve contratos rescindidos por descumprimento?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.9
            ),
            Questao(
                id="REP_005",
                categoria="Reputacional",
                texto="A empresa possui referências comerciais positivas?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.6
            ),
        ],
        
        "Integridade": [
            Questao(
                id="INT_001",
                categoria="Integridade",
                texto="Algum sócio ou administrador da empresa possui vínculo com servidor público?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=1.0
            ),
            Questao(
                id="INT_002",
                categoria="Integridade",
                texto="A empresa possui programa de compliance e integridade implementado?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.6
            ),
            Questao(
                id="INT_003",
                categoria="Integridade",
                texto="Há conflito de interesses declarado em relação a este contrato?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=1.0
            ),
            Questao(
                id="INT_004",
                categoria="Integridade",
                texto="A empresa já foi investigada ou processada por fraude ou corrupção?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=1.0
            ),
            Questao(
                id="INT_005",
                categoria="Integridade",
                texto="A empresa possui canal de denúncias ativo?",
                tipo=TipoQuestao.SIM_NAO,
                peso_risco=0.5
            ),
        ],
    }
    
    def gerar_questionario_completo(self) -> List[Questao]:
        """
        Gera questionário completo com todas as categorias.
        
        Returns:
            Lista de todas as questões
        """
        questoes = []
        for categoria, lista_questoes in self.QUESTOES_POR_CATEGORIA.items():
            questoes.extend(lista_questoes)
        return questoes
    
    def gerar_questionario_por_categoria(self, categoria: str) -> List[Questao]:
        """
        Gera questionário de uma categoria específica.
        
        Args:
            categoria: Nome da categoria
            
        Returns:
            Lista de questões da categoria
        """
        return self.QUESTOES_POR_CATEGORIA.get(categoria, [])
    
    def obter_questao(self, questao_id: str) -> Questao:
        """
        Obtém uma questão específica pelo ID.
        
        Args:
            questao_id: ID da questão
            
        Returns:
            Questão encontrada ou None
        """
        for questoes in self.QUESTOES_POR_CATEGORIA.values():
            for questao in questoes:
                if questao.id == questao_id:
                    return questao
        return None
    
    def calcular_pontuacao(
        self,
        respostas: List[Resposta],
        dados_receita: dict = None
    ) -> Dict[str, float]:
        """
        Calcula pontuação por categoria e total.
        
        Args:
            respostas: Lista de respostas
            dados_receita: Dados da Receita para validação
            
        Returns:
            Dict com pontuações por categoria e total
        """
        pontuacoes = {
            "Compliance": 0.0,
            "Financeiro": 0.0,
            "Operacional": 0.0,
            "Reputacional": 0.0,
            "Integridade": 0.0,
            "Total": 0.0
        }
        
        contadores = {cat: 0 for cat in pontuacoes.keys()}
        
        for resposta in respostas:
            questao = self.obter_questao(resposta.questao_id)
            if not questao:
                continue
            
            # Calcular pontos da resposta
            pontos = self._calcular_pontos_resposta(
                questao,
                resposta.valor,
                dados_receita
            )
            
            # Adicionar à categoria
            pontuacoes[questao.categoria] += pontos
            contadores[questao.categoria] += 1
        
        # Calcular médias por categoria
        for categoria in ["Compliance", "Financeiro", "Operacional", "Reputacional", "Integridade"]:
            if contadores[categoria] > 0:
                pontuacoes[categoria] = pontuacoes[categoria] / contadores[categoria]
        
        # Calcular total (média ponderada)
        total_questoes = sum(contadores.values())
        if total_questoes > 0:
            pontuacoes["Total"] = sum([
                pontuacoes[cat] for cat in ["Compliance", "Financeiro", "Operacional", "Reputacional", "Integridade"]
            ]) / 5
        
        return pontuacoes
    
    def _calcular_pontos_resposta(
        self,
        questao: Questao,
        resposta: str,
        dados_receita: dict = None
    ) -> float:
        """
        Calcula pontos de uma resposta individual.
        Pontuação de 0 (pior) a 10 (melhor).
        """
        # Respostas Sim/Não
        if questao.tipo == TipoQuestao.SIM_NAO:
            # Questões negativas (resposta "Sim" é ruim)
            if any(palavra in questao.texto.lower() for palavra in ["sanção", "inadimplência", "negativa", "vínculo", "conflito", "fraude", "processo"]):
                return 10.0 if resposta.lower() == "não" else 0.0
            # Questões positivas (resposta "Sim" é bom)
            else:
                return 10.0 if resposta.lower() == "sim" else 0.0
        
        # Múltipla escolha
        elif questao.tipo == TipoQuestao.MULTIPLA_ESCOLHA:
            if questao.id == "COMP_004":  # Situação cadastral
                return 10.0 if resposta == "Ativa" else 0.0
            elif questao.id == "FIN_003":  # Porte
                # Maior porte = mais pontos (geralmente)
                if "Demais" in resposta:
                    return 10.0
                elif "EPP" in resposta:
                    return 7.0
                else:
                    return 5.0
        
        # Numérico - retornar valor médio por enquanto
        elif questao.tipo == TipoQuestao.NUMERICO:
            try:
                valor = float(resposta)
                # Normalizar para escala 0-10 (simplificado)
                if questao.id == "OPER_001":  # Funcionários
                    return min(10.0, valor / 10)
                elif questao.id == "OPER_002":  # Anos de atividade
                    return min(10.0, valor / 2)
                else:
                    return 5.0  # Valor neutro
            except:
                return 5.0
        
        # Texto livre - valor neutro
        return 5.0
    
    def listar_categorias(self) -> List[str]:
        """Retorna lista de categorias disponíveis."""
        return list(self.QUESTOES_POR_CATEGORIA.keys())
    
    def contar_questoes_por_categoria(self) -> Dict[str, int]:
        """Retorna quantidade de questões por categoria."""
        return {
            categoria: len(questoes)
            for categoria, questoes in self.QUESTOES_POR_CATEGORIA.items()
        }

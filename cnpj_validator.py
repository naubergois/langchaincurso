"""
Mock de integração com dados da Receita Federal.
Simula consulta de CNPJ e retorna dados fictícios realistas.
"""
import random
from typing import Optional
from fornecedor_models import DadosReceita


class CNPJValidatorMock:
    """
    Mock de validação de CNPJ.
    Simula consulta à Receita Federal com dados fictícios.
    """
    
    # Dados mock para diferentes CNPJs
    EMPRESAS_MOCK = {
        "12.345.678/0001-90": {
            "razao_social": "CONSTRUTORA EXEMPLO LTDA",
            "nome_fantasia": "Exemplo Construções",
            "situacao_cadastral": "Ativa",
            "capital_social": 500000.00,
            "porte": "EPP",
            "atividade_principal": "4120-4/00 - Construção de edifícios",
            "data_abertura": "15/03/2015",
            "municipio": "São Paulo",
            "uf": "SP",
            "qtd_funcionarios": 45,
            "faturamento_anual": 3500000.00,
            "certidao_federal_valida": True,
            "certidao_fgts_valida": True,
            "certidao_trabalhista_valida": False,  # Problema!
        },
        "98.765.432/0001-10": {
            "razao_social": "TECNOLOGIA E SERVICOS SA",
            "nome_fantasia": "TechServ",
            "situacao_cadastral": "Ativa",
            "capital_social": 1000000.00,
            "porte": "Demais",
            "atividade_principal": "6201-5/00 - Desenvolvimento de programas de computador",
            "data_abertura": "10/01/2010",
            "municipio": "Brasília",
            "uf": "DF",
            "qtd_funcionarios": 120,
            "faturamento_anual": 8500000.00,
            "certidao_federal_valida": True,
            "certidao_fgts_valida": True,
            "certidao_trabalhista_valida": True,
        },
        "11.222.333/0001-44": {
            "razao_social": "FORNECEDORA MATERIAIS EIRELI",
            "nome_fantasia": "Materiais Plus",
            "situacao_cadastral": "Ativa",
            "capital_social": 200000.00,
            "porte": "ME",
            "atividade_principal": "4744-0/99 - Comércio varejista de materiais de construção",
            "data_abertura": "20/06/2018",
            "municipio": "Rio de Janeiro",
            "uf": "RJ",
            "qtd_funcionarios": 15,
            "faturamento_anual": 850000.00,
            "certidao_federal_valida": False,  # Problema!
            "certidao_fgts_valida": True,
            "certidao_trabalhista_valida": True,
        },
        "55.666.777/0001-88": {
            "razao_social": "CONSULTORIA EMPRESARIAL LTDA",
            "nome_fantasia": "ConsultPro",
            "situacao_cadastral": "Suspensa",  # Problema grave!
            "capital_social": 100000.00,
            "porte": "ME",
            "atividade_principal": "7020-4/00 - Atividades de consultoria em gestão",
            "data_abertura": "05/09/2012",
            "municipio": "Belo Horizonte",
            "uf": "MG",
            "qtd_funcionarios": 8,
            "faturamento_anual": 450000.00,
            "certidao_federal_valida": False,
            "certidao_fgts_valida": False,
            "certidao_trabalhista_valida": False,
        },
    }
    
    @staticmethod
    def validar_cnpj(cnpj: str) -> bool:
        """
        Valida formato do CNPJ.
        Simplificado - apenas verifica formato básico.
        """
        # Remover formatação
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        return len(cnpj_limpo) == 14 and cnpj_limpo.isdigit()
    
    @staticmethod
    def formatar_cnpj(cnpj: str) -> str:
        """Formata CNPJ no padrão XX.XXX.XXX/XXXX-XX."""
        cnpj_limpo = cnpj.replace(".", "").replace("/", "").replace("-", "")
        return f"{cnpj_limpo[:2]}.{cnpj_limpo[2:5]}.{cnpj_limpo[5:8]}/{cnpj_limpo[8:12]}-{cnpj_limpo[12:]}"
    
    def consultar_cnpj(self, cnpj: str) -> Optional[DadosReceita]:
        """
        Consulta dados do CNPJ (mock).
        
        Args:
            cnpj: CNPJ a ser consultado
            
        Returns:
            DadosReceita ou None se não encontrado
        """
        if not self.validar_cnpj(cnpj):
            return None
        
        cnpj_formatado = self.formatar_cnpj(cnpj)
        
        # Verificar se existe nos dados mock
        if cnpj_formatado in self.EMPRESAS_MOCK:
            dados_mock = self.EMPRESAS_MOCK[cnpj_formatado]
        else:
            # Gerar dados fictícios aleatórios
            dados_mock = self._gerar_dados_aleatorios(cnpj_formatado)
        
        # Criar objeto DadosReceita
        return DadosReceita(
            cnpj=cnpj_formatado,
            razao_social=dados_mock["razao_social"],
            nome_fantasia=dados_mock.get("nome_fantasia"),
            situacao_cadastral=dados_mock["situacao_cadastral"],
            data_situacao_cadastral=dados_mock.get("data_situacao_cadastral", "01/01/2024"),
            capital_social=dados_mock["capital_social"],
            natureza_juridica=dados_mock.get("natureza_juridica", "206-2 - Sociedade Empresária Limitada"),
            porte=dados_mock["porte"],
            atividade_principal=dados_mock["atividade_principal"],
            data_abertura=dados_mock["data_abertura"],
            logradouro=dados_mock.get("logradouro", "Rua Exemplo"),
            numero=dados_mock.get("numero", "123"),
            municipio=dados_mock["municipio"],
            uf=dados_mock["uf"],
            cep=dados_mock.get("cep", "01234-567"),
            telefone=dados_mock.get("telefone", "(11) 1234-5678"),
            email=dados_mock.get("email", "contato@exemplo.com.br"),
            certidao_federal_valida=dados_mock.get("certidao_federal_valida", True),
            certidao_fgts_valida=dados_mock.get("certidao_fgts_valida", True),
            certidao_trabalhista_valida=dados_mock.get("certidao_trabalhista_valida", True),
            qtd_funcionarios=dados_mock.get("qtd_funcionarios"),
            faturamento_anual=dados_mock.get("faturamento_anual"),
        )
    
    def _gerar_dados_aleatorios(self, cnpj: str) -> dict:
        """Gera dados fictícios aleatórios para CNPJ não cadastrado."""
        
        razoes_sociais = [
            "EMPRESA EXEMPLO LTDA",
            "SERVICOS GERAIS SA",
            "COMERCIO E INDUSTRIA LTDA",
            "TECNOLOGIA AVANCADA EIRELI",
            "CONSTRUCAO E ENGENHARIA LTDA",
        ]
        
        atividades = [
            "4120-4/00 - Construção de edifícios",
            "6201-5/00 - Desenvolvimento de programas",
            "4744-0/99 - Comércio varejista",
            "7020-4/00 - Consultoria em gestão",
            "8211-3/00 - Serviços combinados de escritório",
        ]
        
        municipios = ["São Paulo", "Rio de Janeiro", "Brasília", "Belo Horizonte", "Salvador"]
        ufs = ["SP", "RJ", "DF", "MG", "BA"]
        
        idx = random.randint(0, 4)
        
        # Simular alguns problemas aleatoriamente
        tem_problema = random.random() < 0.3  # 30% de chance de ter problema
        
        return {
            "razao_social": razoes_sociais[idx],
            "nome_fantasia": f"Empresa {idx + 1}",
            "situacao_cadastral": "Suspensa" if tem_problema and random.random() < 0.2 else "Ativa",
            "capital_social": random.choice([50000, 100000, 250000, 500000, 1000000]),
            "porte": random.choice(["ME", "EPP", "Demais"]),
            "atividade_principal": atividades[idx],
            "data_abertura": f"{random.randint(1, 28):02d}/{random.randint(1, 12):02d}/{random.randint(2010, 2022)}",
            "municipio": municipios[idx],
            "uf": ufs[idx],
            "qtd_funcionarios": random.randint(5, 150),
            "faturamento_anual": random.randint(200000, 10000000),
            "certidao_federal_valida": not (tem_problema and random.random() < 0.5),
            "certidao_fgts_valida": not (tem_problema and random.random() < 0.5),
            "certidao_trabalhista_valida": not (tem_problema and random.random() < 0.5),
        }
    
    def listar_empresas_exemplo(self) -> list:
        """Retorna lista de CNPJs de exemplo disponíveis."""
        return [
            {
                "cnpj": cnpj,
                "razao_social": dados["razao_social"],
                "situacao": dados["situacao_cadastral"]
            }
            for cnpj, dados in self.EMPRESAS_MOCK.items()
        ]


# Função auxiliar para uso direto
def consultar_cnpj_mock(cnpj: str) -> Optional[DadosReceita]:
    """
    Função auxiliar para consultar CNPJ usando o mock.
    
    Args:
        cnpj: CNPJ a ser consultado
        
    Returns:
        DadosReceita ou None
    """
    validator = CNPJValidatorMock()
    return validator.consultar_cnpj(cnpj)

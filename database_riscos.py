"""
Módulo de gerenciamento do banco de dados SQLite para classificações de risco.
"""
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd


class DatabaseRiscos:
    """Gerencia o banco de dados SQLite para classificações de risco."""
    
    def __init__(self, db_path: str = "classificacoes_risco.db"):
        """
        Inicializa a conexão com o banco de dados.
        
        Args:
            db_path: Caminho para o arquivo do banco de dados SQLite
        """
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Cria e retorna uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Cria a tabela de classificações se não existir."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classificacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                apontamento TEXT NOT NULL,
                nivel_risco TEXT NOT NULL,
                justificativa TEXT NOT NULL,
                acao_sugerida TEXT NOT NULL
            )
        """)
        
        conn.commit()
        conn.close()
    
    def inserir_classificacao(
        self,
        apontamento: str,
        nivel_risco: str,
        justificativa: str,
        acao_sugerida: str
    ) -> int:
        """
        Insere uma nova classificação no banco de dados.
        
        Args:
            apontamento: Texto do apontamento de auditoria
            nivel_risco: Nível de risco (Alto, Médio, Baixo)
            justificativa: Justificativa da classificação
            acao_sugerida: Ação sugerida
            
        Returns:
            ID da classificação inserida
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO classificacoes (apontamento, nivel_risco, justificativa, acao_sugerida)
            VALUES (?, ?, ?, ?)
        """, (apontamento, nivel_risco, justificativa, acao_sugerida))
        
        classificacao_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return classificacao_id
    
    def obter_todas_classificacoes(self) -> List[Dict]:
        """
        Retorna todas as classificações do banco de dados.
        
        Returns:
            Lista de dicionários com as classificações
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, data_hora, apontamento, nivel_risco, justificativa, acao_sugerida
            FROM classificacoes
            ORDER BY data_hora DESC
        """)
        
        colunas = ['id', 'data_hora', 'apontamento', 'nivel_risco', 'justificativa', 'acao_sugerida']
        resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        conn.close()
        return resultados
    
    def obter_classificacao_por_id(self, classificacao_id: int) -> Optional[Dict]:
        """
        Retorna uma classificação específica por ID.
        
        Args:
            classificacao_id: ID da classificação
            
        Returns:
            Dicionário com os dados da classificação ou None se não encontrada
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, data_hora, apontamento, nivel_risco, justificativa, acao_sugerida
            FROM classificacoes
            WHERE id = ?
        """, (classificacao_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            colunas = ['id', 'data_hora', 'apontamento', 'nivel_risco', 'justificativa', 'acao_sugerida']
            return dict(zip(colunas, row))
        return None
    
    def obter_classificacoes_por_nivel(self, nivel_risco: str) -> List[Dict]:
        """
        Retorna todas as classificações de um nível específico.
        
        Args:
            nivel_risco: Nível de risco (Alto, Médio, Baixo)
            
        Returns:
            Lista de dicionários com as classificações
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, data_hora, apontamento, nivel_risco, justificativa, acao_sugerida
            FROM classificacoes
            WHERE nivel_risco = ?
            ORDER BY data_hora DESC
        """, (nivel_risco,))
        
        colunas = ['id', 'data_hora', 'apontamento', 'nivel_risco', 'justificativa', 'acao_sugerida']
        resultados = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        
        conn.close()
        return resultados
    
    def obter_estatisticas(self) -> Dict:
        """
        Retorna estatísticas sobre as classificações.
        
        Returns:
            Dicionário com estatísticas (total, por nível, etc.)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total de classificações
        cursor.execute("SELECT COUNT(*) FROM classificacoes")
        total = cursor.fetchone()[0]
        
        # Contagem por nível
        cursor.execute("""
            SELECT nivel_risco, COUNT(*) as count
            FROM classificacoes
            GROUP BY nivel_risco
        """)
        
        por_nivel = {row[0]: row[1] for row in cursor.fetchall()}
        
        conn.close()
        
        return {
            'total': total,
            'alto': por_nivel.get('Alto', 0),
            'medio': por_nivel.get('Médio', 0),
            'baixo': por_nivel.get('Baixo', 0)
        }
    
    def obter_dataframe(self) -> pd.DataFrame:
        """
        Retorna todas as classificações como um DataFrame pandas.
        
        Returns:
            DataFrame com todas as classificações
        """
        conn = self.get_connection()
        df = pd.read_sql_query("""
            SELECT id, data_hora, apontamento, nivel_risco, justificativa, acao_sugerida
            FROM classificacoes
            ORDER BY data_hora DESC
        """, conn)
        conn.close()
        
        return df
    
    def deletar_classificacao(self, classificacao_id: int) -> bool:
        """
        Deleta uma classificação do banco de dados.
        
        Args:
            classificacao_id: ID da classificação a ser deletada
            
        Returns:
            True se deletada com sucesso, False caso contrário
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM classificacoes WHERE id = ?", (classificacao_id,))
        
        linhas_afetadas = cursor.rowcount
        conn.commit()
        conn.close()
        
        return linhas_afetadas > 0
    
    def limpar_todas_classificacoes(self):
        """Deleta todas as classificações do banco de dados."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM classificacoes")
        
        conn.commit()
        conn.close()


from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'DIÁRIO OFICIAL DE TESTE LOCAL', 0, 1, 'C')
        self.ln(10)

pdf = PDF()
pdf.add_page()
pdf.set_font("Arial", size=10)

texto = """
EXTRATO DE CONTRATO Nº 999/2024
Contratante: Prefeitura Municipal de Teste.
Contratada: EMPRESA DE TESTE LTDA.
Objeto: Fornecimento de licenças de software para o departamento de TI.
Valor: R$ 50.000,00.
Vigência: 12 meses.
"""
pdf.multi_cell(0, 10, texto)
pdf.output("diario_teste.pdf")
print("PDF gerado: diario_teste.pdf")

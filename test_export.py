from exporter.generator import ReportGenerator
from analyzer import ContractAnalyzer

analyzer = ContractAnalyzer()
with open('sample_contract.txt', 'r', encoding='utf-8') as f:
    findings = analyzer.analyze(f.read())
gen = ReportGenerator(findings)
gen.generate_excel('risks.xlsx')
gen.generate_word('report.docx')
gen.generate_pdf('report.pdf')
gen.generate_ppt('summary.pptx')
print('Exports created')

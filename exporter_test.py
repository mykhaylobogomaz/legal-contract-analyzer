import unittest
from analyzer import ContractAnalyzer
from risk_patterns import RISK_PATTERNS

class TestExporter(unittest.TestCase):
    def setUp(self):
        self.analyzer = ContractAnalyzer()
        with open("sample_contract.txt", "r", encoding="utf-8") as f:
            self.text = f.read()

    def test_analysis(self):
        findings = self.analyzer.analyze(self.text)
        self.assertGreater(len(findings), 0)
        print(f"Findings count: {len(findings)}")

if __name__ == "__main__":
    unittest.main()

# Legal Contract Risk Analyzer

Enterprise-grade LegalTech pipeline for automated detection of high-risk clauses in franchise and commercial agreements.

## 🔬 Architecture

This project implements a hybrid analysis engine combining linguistic pattern matching with structured document export capabilities.

### Pipeline Components
1. **Analysis Engine**: NLP-driven (spaCy) rule-based matcher for high-risk legal clauses.
2. **Persistence Layer**: SQLite-based storage for contract history and findings.
3. **Enterprise Exporter**: Multi-format reporting module.
4. **Humanizer Engine**: Post-generation processing to remove AI-generated linguistic markers.

## 🛠 Technology Stack

*   **Languages**: Python (Analysis/Backend), C++ (Performance core)
*   **Infrastructure**: SQLite, Supabase MCP (Integration ready)
*   **Document Generation**: ReportLab (PDF), python-pptx (Presentation), Openpyxl (Excel), python-docx (Word)
*   **Security & NLP**: spaCy, proprietary pattern library, AI-stamp humanizer

## 📁 Project Structure

```
legal-contract-analyzer/
├── analyzer.py          # NLP analysis core
├── persistence.py       # SQLite persistence layer
├── exporter/            # Report generation (.xlsx, .docx, .pdf, .pptx)
├── humanizer_module.py  # AI-stamp detection and removal
├── risk_patterns.py     # Legal risk definitions
└── tests/               # Validation suite
```

## 🚀 Getting Started

### Installation
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Running Tests
Execute the full integration test suite:
```bash
python test_final.py
```

## 📄 License
MIT © 2026 [Mykhaylo Bogomaz](LICENSE).

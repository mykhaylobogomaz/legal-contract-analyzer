# ⚖ Legal Contract Risk Analyzer

> **Automated toxic-clause detection for franchise agreements and commercial contracts.**  
> *Where Computer Science meets Jurisprudence.*

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5?logo=spacy)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-prototype-orange)

---

## 🎯 The Problem

Every year, thousands of entrepreneurs sign franchise and commercial contracts containing
clauses that severely limit their rights, expose them to uncapped financial liability, or
allow the counterparty to terminate unilaterally — often without a lawyer review.

Traditional legal review is expensive (£300–£700/hour) and inaccessible to small business
owners. Most people sign without understanding what they have agreed to.

**Legal Contract Risk Analyzer solves this by applying NLP to surface hidden risks before
you sign.**

---

## 🔬 Interdisciplinary Architecture

This project sits at the intersection of **Computer Science** and **Jurisprudence**:

| Discipline | Contribution |
|---|---|
| Natural Language Processing | Sentence segmentation, text normalisation via spaCy |
| Legal Engineering | Curated risk-pattern library based on common-law contract principles |
| Software Engineering | Clean MVC separation: engine ↔ UI ↔ patterns |
| Legal Risk Management | CRITICAL / HIGH / MEDIUM / LOW severity taxonomy |

The analysis engine uses a **two-pass architecture**:

```
Raw Contract Text
       │
       ▼
  [Pass 1 – NLP]   spaCy tokenises & segments into sentences
       │
       ▼
  [Pass 2 – Rules] Each sentence matched against 25+ legal risk patterns
       │
       ▼
  RiskFinding objects  →  Sorted by severity  →  Rendered in GUI
```

### Why rule-based rather than pure ML?

- **Auditability**: Every finding traces back to a named pattern — essential in a legal context.
- **Zero training data**: Works out of the box with no labelled dataset.
- **Lawyer-editable**: Legal professionals can add patterns in `risk_patterns.py` without touching application code.
- **Production roadmap**: A fine-tuned BERT/LegalBERT classifier sits naturally on top of this foundation for v2.

---

## 🛡 Risk Categories Detected

| Category | Example Clause | Severity |
|---|---|---|
| Unilateral Decision Power | "at the Franchisor's sole discretion" | 🔴 CRITICAL |
| Instant Termination | "terminate immediately without notice" | 🔴 CRITICAL |
| Arbitrary Termination | "without cause" termination right | 🔴 CRITICAL |
| Restraint of Trade | Worldwide 5-year non-compete | 🔴 CRITICAL |
| Unilateral Modification | Fee changes without notice | 🔴 CRITICAL |
| Ongoing Financial Obligation | Open-ended royalty fee | 🟠 HIGH |
| Indemnification | Covers counterparty's own negligence | 🟠 HIGH |
| Liquidated Damages | Remaining-term royalty penalties | 🟠 HIGH |
| Non-Refundable Fees | USD 75,000 non-refundable deposit | 🟠 HIGH |
| IP Rights | Auto-assignment of Franchisee improvements | 🟠 HIGH |
| Dispute Resolution | Mandatory Delaware arbitration | 🟡 MEDIUM |
| Jurisdiction | Foreign governing law | 🟡 MEDIUM |
| Territory Rights | Vague exclusive territory | 🟡 MEDIUM |
| Force Majeure | One-sided relief | 🟡 MEDIUM |
| Confidentiality | Bars disclosure to legal counsel | 🟡 MEDIUM |
| Rights Waiver | Permanent waiver risk | 🔵 LOW |
| Entire Agreement | Voids pre-contractual representations | 🔵 LOW |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- `tkinter` (bundled with Python on Windows/macOS; on Linux: `sudo apt install python3-tk`)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mykhaylobogomaz/legal-contract-analyzer.git
cd legal-contract-analyzer

# 2. Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy language model
python -m spacy download en_core_web_sm

# 5. Launch the application
python main.py
```

### Running on the sample contract

1. Click **📂 Open Contract**
2. Select `sample_contract.txt` (included in this repository)
3. Click **🔍 Analyze**
4. Browse findings sorted by severity in the left panel
5. Click any finding to see a detailed explanation and recommendation

---

## 📁 Project Structure

```
legal-contract-analyzer/
│
├── main.py              # GUI application (tkinter) — View layer
├── analyzer.py          # NLP engine (spaCy) — Controller + Model
├── risk_patterns.py     # Curated risk pattern library — Domain Knowledge
│
├── sample_contract.txt  # Test contract with intentional toxic clauses
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

**Separation of concerns:**

- `risk_patterns.py` — Add new legal patterns here. No programming required beyond Python dicts.
- `analyzer.py` — Swap the matching engine (rules → ML) without touching the UI.
- `main.py` — Restyle or replace the GUI without touching business logic.

---

## 🔧 Extending the Pattern Library

Open `risk_patterns.py` and append a new entry to `RISK_PATTERNS`:

```python
{
    "pattern": "penalty clause",
    "category": "Financial Penalty",
    "severity": "HIGH",
    "explanation": "Penalty clauses impose pre-set fines that may not reflect actual loss.",
    "recommendation": "Verify proportionality; unenforceable penalties may be struck out.",
},
```

That's all. The engine picks it up automatically on the next run.

---

## 🗺 Roadmap

- [ ] **v1.1** — PDF ingestion (PyMuPDF)
- [ ] **v1.2** — Export findings to PDF report
- [ ] **v2.0** — LegalBERT fine-tuned classifier for semantic risk detection
- [ ] **v2.1** — Multi-jurisdiction risk flags (UK, EU, AU)
- [ ] **v3.0** — Web interface (FastAPI + React)
- [ ] **v3.1** — API endpoint for integration with DocuSign / contract management platforms

---

## ⚠ Disclaimer

This tool is a **prototype for educational and research purposes only**.  
It does **not** constitute legal advice. Always consult a qualified solicitor or attorney
before signing any legal agreement.

---

## 📄 License

MIT © 2024 — See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Pull requests are welcome. For significant changes, please open an issue first to discuss
what you would like to change. When adding new risk patterns, please cite the legal
principle or jurisdiction where the risk has been tested in case law.

"""
analyzer.py
===========
NLP analysis core for the Legal Contract Analyzer.

Responsibilities:
  1. Load and pre-process text (sentence segmentation via spaCy).
  2. Match each sentence against the RISK_PATTERNS library.
  3. Return structured RiskFinding objects sorted by severity.

No UI logic lives here — pure analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

import spacy

from risk_patterns import RISK_PATTERNS, SEVERITY_ORDER


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class RiskFinding:
    """Represents a single risk identified in a contract sentence."""
    sentence: str
    category: str
    severity: str          # "CRITICAL" | "HIGH" | "MEDIUM" | "LOW"
    explanation: str
    recommendation: str
    pattern_matched: str
    sentence_index: int    # 1-based position in the document

    @property
    def severity_rank(self) -> int:
        return SEVERITY_ORDER.get(self.severity, 99)


# ---------------------------------------------------------------------------
# Analyzer class
# ---------------------------------------------------------------------------

class ContractAnalyzer:
    """
    Performs rule-based NLP analysis on legal contract text.

    Architecture decision: We use a two-pass approach.
      Pass 1 – spaCy tokenises and segments the document into sentences.
      Pass 2 – Each sentence is matched against the pattern library using
               case-insensitive substring search (fast, explainable, auditable).

    Why not a pure ML model?
      • Rule-based systems are fully auditable — critical for legal use.
      • Zero training data required for the prototype.
      • Easy for non-technical lawyers to add/modify patterns.
      • A production v2 would layer a fine-tuned BERT classifier on top.
    """

    _MODEL_PREFERENCE = ["en_core_web_sm", "en_core_web_md", "en_core_web_lg"]

    def __init__(self) -> None:
        self.nlp = self._load_spacy_model()

    # ── Model loading ────────────────────────────────────────────────────────

    def _load_spacy_model(self):
        """Try to load a spaCy model; fall back to blank 'en' if none installed."""
        for model_name in self._MODEL_PREFERENCE:
            try:
                nlp = spacy.load(model_name)
                return nlp
            except OSError:
                continue

        # Last resort: blank model still provides sentence segmentation via
        # the sentencizer component.
        nlp = spacy.blank("en")
        nlp.add_pipe("sentencizer")
        return nlp

    # ── Public interface ─────────────────────────────────────────────────────

    def analyze(self, text: str) -> List[RiskFinding]:
        """
        Analyse contract text and return a list of RiskFinding objects.

        Parameters
        ----------
        text : str
            Raw contract text (UTF-8).

        Returns
        -------
        List[RiskFinding]
            Findings sorted by severity (CRITICAL first).
        """
        cleaned_text = self._clean_text(text)
        sentences = self._segment_sentences(cleaned_text)
        findings = self._match_patterns(sentences)
        findings.sort(key=lambda f: (f.severity_rank, f.sentence_index))
        return findings

    def get_summary(self, findings: List[RiskFinding]) -> dict:
        """Return a summary dict for display in the UI header."""
        counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for f in findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        return {
            "total": len(findings),
            "by_severity": counts,
            "categories": list({f.category for f in findings}),
        }

    # ── Internal helpers ─────────────────────────────────────────────────────

    @staticmethod
    def _clean_text(text: str) -> str:
        """Normalise whitespace while preserving sentence boundaries."""
        # Collapse multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)
        # Collapse intra-line multiple spaces
        text = re.sub(r"[ \t]{2,}", " ", text)
        return text.strip()

    def _segment_sentences(self, text: str) -> List[str]:
        """Use spaCy to split text into individual sentences."""
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
        return sentences

    def _match_patterns(self, sentences: List[str]) -> List[RiskFinding]:
        """
        For each sentence, check every pattern in RISK_PATTERNS.

        A sentence can match multiple patterns (e.g. 'sole discretion'
        AND 'terminate immediately' in the same clause).
        """
        findings: List[RiskFinding] = []
        seen: set = set()  # deduplicate identical (sentence, pattern) pairs

        for idx, sentence in enumerate(sentences, start=1):
            sentence_lower = sentence.lower()

            for rule in RISK_PATTERNS:
                pattern_lower = rule["pattern"].lower()

                if pattern_lower in sentence_lower:
                    dedup_key = (sentence, pattern_lower)
                    if dedup_key in seen:
                        continue
                    seen.add(dedup_key)

                    findings.append(
                        RiskFinding(
                            sentence=sentence,
                            category=rule["category"],
                            severity=rule["severity"],
                            explanation=rule["explanation"],
                            recommendation=rule["recommendation"],
                            pattern_matched=rule["pattern"],
                            sentence_index=idx,
                        )
                    )

        return findings

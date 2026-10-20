import sqlite3
import json
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ContractRecord:
    id: int
    filename: str
    content: str
    analysis_result: str # JSON

class PersistenceLayer:
    def __init__(self, db_path: str = "contracts.db"):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                content TEXT NOT NULL,
                analysis_result TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contract_id INTEGER,
                severity TEXT,
                category TEXT,
                pattern_matched TEXT,
                FOREIGN KEY(contract_id) REFERENCES contracts(id)
            )
        """)
        self.conn.commit()

    def save_contract(self, filename: str, content: str, analysis_result: List[dict]):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO contracts (filename, content, analysis_result) VALUES (?, ?, ?)",
            (filename, content, json.dumps(analysis_result))
        )
        contract_id = cursor.lastrowid
        for finding in analysis_result:
            cursor.execute(
                "INSERT INTO findings (contract_id, severity, category, pattern_matched) VALUES (?, ?, ?, ?)",
                (contract_id, finding['severity'], finding['category'], finding['pattern_matched'])
            )
        self.conn.commit()
        return contract_id


import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class DatabaseManager:
    """SQLite Database Manager for persisting ResumeIQ AI analysis history."""

    def __init__(self, db_path: str = "database/history.db"):
        self.db_path = db_path
        # Ensure database directory exists
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        """Initialize tables if they do not exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    job_role TEXT NOT NULL,
                    overall_score REAL NOT NULL,
                    semantic_score REAL NOT NULL,
                    skill_score REAL NOT NULL,
                    matched_skills TEXT NOT NULL,
                    missing_skills TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
            """)
            conn.commit()

    def save_analysis(
        self,
        filename: str,
        job_role: str,
        overall_score: float,
        semantic_score: float,
        skill_score: float,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> int:
        """Saves a new resume analysis record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO history (
                    filename, job_role, overall_score, semantic_score, 
                    skill_score, matched_skills, missing_skills, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                filename,
                job_role or "Unspecified Role",
                float(overall_score),
                float(semantic_score),
                float(skill_score),
                json.dumps(matched_skills),
                json.dumps(missing_skills),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all_history(self) -> List[Dict[str, Any]]:
        """Retrieves all past resume analysis records sorted by date."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM history ORDER BY created_at DESC")
            rows = cursor.fetchall()
            
            records = []
            for row in rows:
                rec = dict(row)
                rec["matched_skills"] = json.loads(rec["matched_skills"])
                rec["missing_skills"] = json.loads(rec["missing_skills"])
                records.append(rec)
            return records

    def delete_record(self, record_id: int) -> bool:
        """Deletes a single history record by ID."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (record_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_history(self) -> None:
        """Wipes all analysis history."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            conn.commit()

    def get_summary_stats(self) -> Dict[str, Any]:
        """Calculates aggregate statistical metrics for the dashboard."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_analyzed,
                    AVG(overall_score) as avg_score,
                    MAX(overall_score) as highest_score,
                    MIN(overall_score) as lowest_score
                FROM history
            """)
            row = cursor.fetchone()
            if not row or row["total_analyzed"] == 0:
                return {
                    "total_analyzed": 0,
                    "avg_score": 0.0,
                    "highest_score": 0.0,
                    "lowest_score": 0.0
                }
            return {
                "total_analyzed": row["total_analyzed"],
                "avg_score": round(row["avg_score"] or 0.0, 1),
                "highest_score": round(row["highest_score"] or 0.0, 1),
                "lowest_score": round(row["lowest_score"] or 0.0, 1)
            }
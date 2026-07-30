"""Persist Super Resumer jobs and automation state."""

from __future__ import annotations

import json
import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
JOBS_FILE = DATA_DIR / "super_resumer_jobs.json"
JOBS_DB = DATA_DIR / "super_resumer_jobs.db"


def _now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def job_key(job: Dict[str, Any]) -> str:
    source = str(job.get("source") or job.get("platform") or "unknown").strip().lower()
    external_id = str(job.get("external_id") or "").strip()
    url = str(job.get("url") or "").strip().lower()
    title = str(job.get("title") or "").strip()
    company = str(job.get("company") or "").strip()
    if source and external_id:
        return f"{source}:{external_id}"
    if source and url:
        return f"{source}:{url}"
    return f"{source}:{title}_{company}".lower()


class JobStore:
    """SQLite-backed persistence with JSON compatibility for the dashboard."""

    def __init__(self, db_path: Path | str = JOBS_DB, json_path: Path | str = JOBS_FILE):
        self.db_path = Path(db_path)
        self.json_path = Path(json_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_schema()
        self._bootstrap_from_json_if_needed()

    def _create_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                job_key TEXT PRIMARY KEY,
                source TEXT,
                external_id TEXT,
                url TEXT,
                title TEXT,
                company TEXT,
                location TEXT,
                salary TEXT,
                description TEXT,
                status TEXT,
                match_score REAL,
                auto_applied INTEGER DEFAULT 0,
                application_method TEXT,
                applied_date TEXT,
                rejected_date TEXT,
                updated_at TEXT,
                created_at TEXT,
                raw_json TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS apply_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_key TEXT NOT NULL,
                platform TEXT,
                status TEXT,
                message TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                details_json TEXT,
                FOREIGN KEY(job_key) REFERENCES jobs(job_key)
            );

            CREATE TABLE IF NOT EXISTS source_checkpoints (
                source TEXT PRIMARY KEY,
                cursor TEXT,
                last_run_at TEXT,
                metadata_json TEXT
            );
            """
        )
        self.conn.commit()

    def _bootstrap_from_json_if_needed(self) -> None:
        row = self.conn.execute("SELECT COUNT(*) AS count FROM jobs").fetchone()
        if row and row["count"]:
            return
        jobs = _load_jobs_from_json(self.json_path)
        if jobs:
            self.upsert_jobs(jobs)

    def load_jobs(self) -> List[Dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT raw_json FROM jobs ORDER BY COALESCE(applied_date, updated_at, created_at) DESC"
        ).fetchall()
        jobs = [json.loads(row["raw_json"]) for row in rows]
        _write_jobs_json(self.json_path, jobs)
        return jobs

    def upsert_jobs(self, jobs: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        stored: List[Dict[str, Any]] = []
        for job in jobs:
            normalized = dict(job)
            normalized["job_key"] = job_key(normalized)
            normalized.setdefault("source", normalized.get("platform", "unknown"))
            normalized.setdefault("status", "discovered")
            normalized.setdefault("created_at", _now_iso())
            normalized["updated_at"] = _now_iso()
            self.conn.execute(
                """
                INSERT INTO jobs (
                    job_key, source, external_id, url, title, company, location, salary,
                    description, status, match_score, auto_applied, application_method,
                    applied_date, rejected_date, updated_at, created_at, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(job_key) DO UPDATE SET
                    source=excluded.source,
                    external_id=excluded.external_id,
                    url=excluded.url,
                    title=excluded.title,
                    company=excluded.company,
                    location=excluded.location,
                    salary=excluded.salary,
                    description=excluded.description,
                    status=excluded.status,
                    match_score=excluded.match_score,
                    auto_applied=excluded.auto_applied,
                    application_method=excluded.application_method,
                    applied_date=excluded.applied_date,
                    rejected_date=excluded.rejected_date,
                    updated_at=excluded.updated_at,
                    created_at=COALESCE(jobs.created_at, excluded.created_at),
                    raw_json=excluded.raw_json
                """,
                (
                    normalized["job_key"],
                    normalized.get("source"),
                    normalized.get("external_id"),
                    normalized.get("url"),
                    normalized.get("title"),
                    normalized.get("company"),
                    normalized.get("location"),
                    normalized.get("salary"),
                    normalized.get("description"),
                    normalized.get("status"),
                    normalized.get("match_score"),
                    int(bool(normalized.get("auto_applied"))),
                    normalized.get("application_method"),
                    normalized.get("applied_date"),
                    normalized.get("rejected_date"),
                    normalized.get("updated_at"),
                    normalized.get("created_at"),
                    json.dumps(normalized, default=str),
                ),
            )
            stored.append(normalized)
        self.conn.commit()
        _write_jobs_json(self.json_path, self.load_jobs())
        return stored

    def record_apply_attempt(
        self,
        job: Dict[str, Any],
        status: str,
        message: str = "",
        error: str = "",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO apply_attempts (
                job_key, platform, status, message, error, created_at, details_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_key(job),
                job.get("source") or job.get("platform") or "unknown",
                status,
                message,
                error,
                _now_iso(),
                json.dumps(details or {}, default=str),
            ),
        )
        self.conn.commit()

    def get_known_job_keys(self) -> List[str]:
        rows = self.conn.execute("SELECT job_key FROM jobs").fetchall()
        return [row["job_key"] for row in rows]

    def update_checkpoint(
        self,
        source: str,
        cursor: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO source_checkpoints (source, cursor, last_run_at, metadata_json)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(source) DO UPDATE SET
                cursor=excluded.cursor,
                last_run_at=excluded.last_run_at,
                metadata_json=excluded.metadata_json
            """,
            (source, cursor, _now_iso(), json.dumps(metadata or {}, default=str)),
        )
        self.conn.commit()

    def get_checkpoint(self, source: str) -> Dict[str, Any]:
        row = self.conn.execute(
            "SELECT source, cursor, last_run_at, metadata_json FROM source_checkpoints WHERE source = ?",
            (source,),
        ).fetchone()
        if not row:
            return {"source": source, "cursor": "", "last_run_at": None, "metadata": {}}
        return {
            "source": row["source"],
            "cursor": row["cursor"] or "",
            "last_run_at": row["last_run_at"],
            "metadata": json.loads(row["metadata_json"] or "{}"),
        }

    def close(self) -> None:
        self.conn.close()


def _load_jobs_from_json(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Could not load jobs file: %s", e)
    return []


def _write_jobs_json(path: Path, jobs: List[Dict[str, Any]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, default=str)


def load_jobs() -> List[Dict[str, Any]]:
    return JobStore().load_jobs()


def save_jobs(jobs: List[Dict[str, Any]]) -> None:
    JobStore().upsert_jobs(jobs)

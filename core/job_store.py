"""Persist Super Resumer job list across app restarts."""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

JOBS_FILE = Path(__file__).resolve().parent.parent / "data" / "super_resumer_jobs.json"


def job_key(job: Dict[str, Any]) -> str:
    return f"{job.get('title', '')}_{job.get('company', '')}"


def load_jobs() -> List[Dict[str, Any]]:
    if not JOBS_FILE.exists():
        return []
    try:
        with open(JOBS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError) as e:
        logger.warning("Could not load jobs file: %s", e)
    return []


def save_jobs(jobs: List[Dict[str, Any]]) -> None:
    JOBS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(JOBS_FILE, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, default=str)

"""Live job discovery for Super Resumer."""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, Iterable, List, Optional, Set

from agents.live_search import (
    BoardFeedAdapter,
    IndeedSearchAdapter,
    LinkedInSearchAdapter,
    NaukriSearchAdapter,
)
from core.job_store import job_key

logger = logging.getLogger(__name__)


class SuperResumerJobScraper:
    """Live search adapter that aggregates jobs from public boards."""

    def __init__(self, config):
        self.config = config
        self.location = config.LOCATION
        self.min_salary = config.MIN_SALARY_LPA
        self.target_roles = config.TARGET_ROLES
        self.job_sources = config.JOB_SOURCES
        self.max_results_per_source = config.MAX_RESULTS_PER_SOURCE
        self.discovery_errors: List[str] = []

    def _search_keywords(self) -> List[str]:
        return self.config.SEARCH_KEYWORDS or self.target_roles

    def _collect_all_listings(self) -> List[Dict[str, Any]]:
        all_jobs: List[Dict[str, Any]] = []
        self.discovery_errors = []
        keywords = self._search_keywords()

        if "linkedin" in self.job_sources:
            result = LinkedInSearchAdapter().search(keywords, self.location)
            all_jobs.extend(result.jobs)
            self.discovery_errors.extend(result.errors)

        if "indeed" in self.job_sources:
            result = IndeedSearchAdapter().search(keywords, self.location)
            all_jobs.extend(result.jobs)
            self.discovery_errors.extend(result.errors)

        if "naukri" in self.job_sources:
            result = NaukriSearchAdapter().search(keywords, self.location)
            all_jobs.extend(result.jobs)
            self.discovery_errors.extend(result.errors)

        board_sources = {
            "greenhouse": self.config.GREENHOUSE_BOARD_URLS,
            "lever": self.config.LEVER_BOARD_URLS,
            "workday": self.config.WORKDAY_BOARD_URLS,
        }
        for source, urls in board_sources.items():
            if source not in self.job_sources:
                continue
            result = BoardFeedAdapter(source, urls).search()
            all_jobs.extend(result.jobs)
            self.discovery_errors.extend(result.errors)

        unique: Dict[str, Dict[str, Any]] = {}
        for job in all_jobs:
            if not job.get("url"):
                continue
            unique[job_key(job)] = job
        return list(unique.values())

    def add_manual_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        job = dict(job_data)
        job["source"] = "manual"
        job["platform"] = "manual"
        return job

    def filter_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered_jobs = []
        role_terms = {term.lower() for term in self.target_roles}
        generic_terms = {
            "developer",
            "engineer",
            "software",
            "python",
            "c#",
            ".net",
            "machine learning",
            "ai",
            "backend",
            "full stack",
        }

        for job in jobs:
            location = str(job.get("location") or "").lower()
            if self.location.lower() not in location and "remote" not in location and "india" not in location:
                continue

            salary_text = str(job.get("salary") or "")
            max_lpa = self._extract_max_lpa(salary_text)
            if max_lpa is not None and max_lpa < self.min_salary:
                continue

            title_lower = str(job.get("title") or "").lower()
            desc_lower = str(job.get("description") or "").lower()
            if not any(term in title_lower or term in desc_lower for term in role_terms | generic_terms):
                continue

            filtered_jobs.append(job)
        return filtered_jobs

    def _extract_max_lpa(self, salary_text: str) -> Optional[int]:
        match = re.findall(r"(\d+)", salary_text.lower())
        if not match or "lpa" not in salary_text.lower():
            return None
        return max(int(value) for value in match)

    def scrape_all_sources(self, known_job_keys: Optional[Set[str]] = None) -> List[Dict[str, Any]]:
        known_job_keys = known_job_keys or set()
        filtered_jobs = self.filter_jobs(self._collect_all_listings())
        fresh_jobs = [job for job in filtered_jobs if job_key(job) not in known_job_keys]
        logger.info(
            "Discovery found %d filtered jobs, %d new, %d errors",
            len(filtered_jobs),
            len(fresh_jobs),
            len(self.discovery_errors),
        )
        return fresh_jobs[: self.max_results_per_source * max(len(self.job_sources), 1)]
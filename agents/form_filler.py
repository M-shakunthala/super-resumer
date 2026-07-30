"""Question/field answer helper backed by profile memory and env vars."""

from __future__ import annotations

import os
from typing import Any, Dict

from memory.profile_memory import ProfileMemory


class FormFiller:
    def __init__(self) -> None:
        self.profile_memory = ProfileMemory()
        self.personal_info = self.profile_memory.get_personal_info()
        self.preferences = self.profile_memory.get_preferences()

    def fill(self, question: str) -> str:
        return self.get_answer(question)

    @classmethod
    def get_answer(cls, question: str) -> str:
        return cls()._lookup(question)

    def _lookup(self, question: str) -> str:
        q = (question or "").lower()
        answers: Dict[str, Any] = {
            "name": self.personal_info.get("name") or os.getenv("APPLICANT_NAME", ""),
            "first_name": os.getenv("APPLICANT_FIRST_NAME", self._first_name()),
            "last_name": os.getenv("APPLICANT_LAST_NAME", self._last_name()),
            "email": self.personal_info.get("email") or os.getenv("APPLICANT_EMAIL", ""),
            "phone": self.personal_info.get("phone") or os.getenv("APPLICANT_PHONE", ""),
            "location": self.personal_info.get("location") or os.getenv("APPLICANT_LOCATION", ""),
            "linkedin_url": self.personal_info.get("linkedin_url") or os.getenv("APPLICANT_LINKEDIN_URL", ""),
            "github_url": self.personal_info.get("github_url") or os.getenv("APPLICANT_GITHUB_URL", ""),
            "portfolio_url": os.getenv("APPLICANT_PORTFOLIO_URL", ""),
            "work_authorization": os.getenv("APPLICANT_WORK_AUTHORIZATION", "Yes"),
            "notice_period": os.getenv("APPLICANT_NOTICE_PERIOD", ""),
            "salary_expectation": os.getenv("APPLICANT_SALARY_EXPECTATION", ""),
            "years_of_experience": os.getenv("APPLICANT_YEARS_OF_EXPERIENCE", ""),
            "experience": ", ".join(exp.get("title", "") for exp in self.profile_memory.get_experience()),
        }

        keyword_map = {
            "first": "first_name",
            "given": "first_name",
            "last": "last_name",
            "family": "last_name",
            "email": "email",
            "phone": "phone",
            "mobile": "phone",
            "linkedin": "linkedin_url",
            "github": "github_url",
            "portfolio": "portfolio_url",
            "website": "portfolio_url",
            "authorization": "work_authorization",
            "visa": "work_authorization",
            "notice": "notice_period",
            "salary": "salary_expectation",
            "experience": "years_of_experience",
            "location": "location",
            "name": "name",
        }

        for needle, key in keyword_map.items():
            if needle in q:
                return str(answers.get(key, "") or "")
        return ""

    def _first_name(self) -> str:
        return (self.personal_info.get("name") or "").split(" ")[0] if self.personal_info.get("name") else ""

    def _last_name(self) -> str:
        parts = (self.personal_info.get("name") or "").split(" ")
        return " ".join(parts[1:]) if len(parts) > 1 else ""
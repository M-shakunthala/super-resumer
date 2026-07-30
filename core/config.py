from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _split_env(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
    """Central runtime configuration."""

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")

    LOCATION = os.getenv("SR_LOCATION", "Bangalore")
    MIN_SALARY_LPA = int(os.getenv("SR_MIN_SALARY_LPA", "7"))
    MATCH_THRESHOLD = int(os.getenv("SR_MATCH_THRESHOLD", "85"))
    MAX_RESULTS_PER_SOURCE = int(os.getenv("SR_MAX_RESULTS_PER_SOURCE", "25"))
    AUTO_SEARCH_INTERVAL_SEC = int(os.getenv("SR_AUTO_SEARCH_INTERVAL_SEC", "300"))
    AUTO_APPLY_ENABLED = os.getenv("SR_AUTO_APPLY_ENABLED", "true").lower() == "true"
    DRY_RUN = os.getenv("SR_DRY_RUN", "false").lower() == "true"
    HEADLESS_BROWSER = os.getenv("SR_HEADLESS_BROWSER", "true").lower() == "true"

    TARGET_ROLES = _split_env(
        "SR_TARGET_ROLES",
        "Software Developer,C# Developer,Python AI Developer,AI Engineer,"
        "Machine Learning Engineer,.NET Developer,Backend Engineer",
    )
    SEARCH_KEYWORDS = _split_env(
        "SR_SEARCH_KEYWORDS",
        "C# Developer,Python AI Engineer,Machine Learning Engineer,.NET Developer,"
        "Backend Engineer,Software Engineer",
    )

    RESUME_C_SHARP = os.getenv("SR_RESUME_C_SHARP", "resumes/Shakunthala_c#_Resume.pdf")
    RESUME_PYTHON_AI = os.getenv("SR_RESUME_PYTHON_AI", "resumes/Shakunthala_python_Resume.pdf")

    JOB_SOURCES = _split_env(
        "SR_JOB_SOURCES",
        "linkedin,indeed,naukri,greenhouse,lever,workday",
    )

    GREENHOUSE_BOARD_URLS = _split_env(
        "SR_GREENHOUSE_BOARD_URLS",
        "https://boards.greenhouse.io/stripe,https://boards.greenhouse.io/notion",
    )
    LEVER_BOARD_URLS = _split_env(
        "SR_LEVER_BOARD_URLS",
        "https://jobs.lever.co/postman,https://jobs.lever.co/canva",
    )
    WORKDAY_BOARD_URLS = _split_env(
        "SR_WORKDAY_BOARD_URLS",
        "https://wd1.myworkdaysite.com/recruiting/spotify/Spotify/jobs,"
        "https://salesforce.wd1.myworkdayjobs.com/External_Career_Site",
    )

    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
    INDEED_EMAIL = os.getenv("INDEED_EMAIL")
    INDEED_PASSWORD = os.getenv("INDEED_PASSWORD")
    NAUKRI_EMAIL = os.getenv("NAUKRI_EMAIL")
    NAUKRI_PASSWORD = os.getenv("NAUKRI_PASSWORD")

    @classmethod
    def resume_path_for(cls, resume_type: str) -> str:
        if "c#" in resume_type.lower():
            return cls.RESUME_C_SHARP
        return cls.RESUME_PYTHON_AI

    @classmethod
    def resolve_path(cls, value: str) -> str:
        return str(Path(value).expanduser())

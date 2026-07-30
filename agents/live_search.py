"""Live discovery adapters for public job boards and company ATS pages."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    )
}


def extract_tech_stack(text: str) -> List[str]:
    catalog = [
        "C#",
        ".NET",
        "ASP.NET",
        "ASP.NET Core",
        ".NET Core",
        "Python",
        "FastAPI",
        "Django",
        "Flask",
        "TensorFlow",
        "PyTorch",
        "Machine Learning",
        "Deep Learning",
        "LangChain",
        "NLP",
        "SQL",
        "PostgreSQL",
        "Azure",
        "AWS",
        "Kubernetes",
        "React",
    ]
    haystack = (text or "").lower()
    return [item for item in catalog if item.lower() in haystack]


def extract_salary_from_text(text: str) -> str:
    """Try to extract salary mention from description text."""
    patterns = [
        r"\b(\d+\s*[-–]\s*\d+\s*LPA)\b",
        r"\b(\d+\s*LPA)\b",
        r"\b(\$\d+[kK]?\s*[-–]\s*\$?\d+[kK]?)\b",
        r"\b(INR\s*\d+[,\d]*\s*[-–]\s*\d+[,\d]*)\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text or "", re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return ""


def normalize_job(source: str, job: Dict[str, Any]) -> Dict[str, Any]:
    text = " ".join(
        [
            str(job.get("title", "")),
            str(job.get("description", "")),
            str(job.get("summary", "")),
        ]
    )
    salary = (job.get("salary") or "").strip()
    if not salary:
        salary = extract_salary_from_text(text)
    normalized = {
        "source": source,
        "platform": source,
        "external_id": job.get("external_id") or job.get("id") or job.get("url"),
        "title": (job.get("title") or "Unknown Role").strip(),
        "company": (job.get("company") or "Unknown Company").strip(),
        "location": (job.get("location") or "").strip(),
        "salary": salary,
        "description": (job.get("description") or job.get("summary") or "").strip(),
        "url": (job.get("url") or "").strip(),
        "tech_stack": job.get("tech_stack") or extract_tech_stack(text),
    }
    if not normalized["description"]:
        normalized["description"] = normalized["title"]
    return normalized


@dataclass
class SourceResult:
    source: str
    jobs: List[Dict[str, Any]]
    errors: List[str]


class HTTPMixin:
    timeout = 20

    def fetch(self, url: str) -> str:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def soup(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(self.fetch(url), "html.parser")


class LinkedInSearchAdapter(HTTPMixin):
    source = "linkedin"

    def _fetch_job_details(self, url: str) -> Dict[str, Any]:
        """Fetch salary and description from individual LinkedIn job page."""
        try:
            soup = self.soup(url)
            salary = ""
            description = ""

            for el in soup.select(
                ".job-details-jobs-unified-top-card__job-insight, "
                ".compensation__salary, [class*='salary'], [class*='compensation']"
            ):
                text = el.get_text(" ", strip=True)
                if any(c in text.lower() for c in ["lpa", "\u20b9", "$", "per year", "per month", "annum"]):
                    salary = text
                    break

            desc_el = soup.select_one(
                ".jobs-description__content, .show-more-less-html__markup, #job-details"
            )
            if desc_el:
                description = desc_el.get_text(" ", strip=True)[:1000]

            if not salary and description:
                salary = extract_salary_from_text(description)

            return {"salary": salary, "description": description}
        except Exception:
            return {"salary": "", "description": ""}

    def search(self, keywords: Iterable[str], location: str) -> SourceResult:
        jobs: List[Dict[str, Any]] = []
        errors: List[str] = []
        seen_urls: set = set()
        for keyword in keywords:
            url = (
                "https://www.linkedin.com/jobs/search/"
                f"?keywords={quote_plus(keyword)}&location={quote_plus(location)}"
            )
            try:
                soup = self.soup(url)
                cards = soup.select("a[href*='/jobs/view/']")
                for card in cards[:20]:
                    href = urljoin("https://www.linkedin.com", card.get("href") or "")
                    clean_href = href.split("?")[0]
                    title = card.get_text(" ", strip=True)
                    if not href or not title or clean_href in seen_urls:
                        continue
                    seen_urls.add(clean_href)
                    jobs.append(
                        normalize_job(
                            self.source,
                            {
                                "title": title,
                                "company": "LinkedIn Listing",
                                "location": location,
                                "url": href,
                                "salary": "",
                                "description": title,
                            },
                        )
                    )
            except Exception as exc:
                errors.append(f"LinkedIn search failed for '{keyword}': {exc}")
        return SourceResult(self.source, jobs, errors)


class IndeedSearchAdapter(HTTPMixin):
    source = "indeed"

    def _fetch_job_details(self, url: str) -> Dict[str, Any]:
        try:
            soup = self.soup(url)
            salary = ""
            description = ""

            salary_el = soup.select_one(
                "[data-testid='jobsearch-SalaryInfoAndJobType'], "
                "[class*='salary'], [class*='compensation'], "
                "#salaryInfoAndJobType"
            )
            if salary_el:
                salary = salary_el.get_text(" ", strip=True)

            desc_el = soup.select_one(
                "#jobDescriptionText, [data-testid='jobsearch-jobDescriptionText']"
            )
            if desc_el:
                description = desc_el.get_text(" ", strip=True)[:1000]

            if not salary and description:
                salary = extract_salary_from_text(description)

            return {"salary": salary, "description": description}
        except Exception:
            return {"salary": "", "description": ""}

    def search(self, keywords: Iterable[str], location: str) -> SourceResult:
        jobs: List[Dict[str, Any]] = []
        errors: List[str] = []
        seen_urls: set = set()
        for keyword in keywords:
            url = (
                "https://in.indeed.com/jobs"
                f"?q={quote_plus(keyword)}&l={quote_plus(location)}"
            )
            try:
                soup = self.soup(url)
                cards = soup.select("div.job_seen_beacon, div.cardOutline")
                for card in cards[:20]:
                    title_el = card.select_one("h2 a, a.jcs-JobTitle")
                    company_el = card.select_one("[data-testid='company-name'], span.companyName")
                    location_el = card.select_one("[data-testid='text-location'], div.companyLocation")
                    salary_el = card.select_one("[data-testid='attribute_snippet_testid'], span.salary-snippet")
                    summary_el = card.select_one("[data-testid='job-snippet']")
                    if not title_el:
                        continue
                    href = urljoin("https://in.indeed.com", title_el.get("href") or "")
                    clean_href = href.split("?")[0]
                    if clean_href in seen_urls:
                        continue
                    seen_urls.add(clean_href)
                    jobs.append(
                        normalize_job(
                            self.source,
                            {
                                "title": title_el.get_text(" ", strip=True),
                                "company": company_el.get_text(" ", strip=True) if company_el else "Indeed Listing",
                                "location": location_el.get_text(" ", strip=True) if location_el else location,
                                "salary": salary_el.get_text(" ", strip=True) if salary_el else "",
                                "description": summary_el.get_text(" ", strip=True) if summary_el else "",
                                "url": href,
                            },
                        )
                    )
            except Exception as exc:
                errors.append(f"Indeed search failed for '{keyword}': {exc}")
        return SourceResult(self.source, jobs, errors)


class NaukriSearchAdapter(HTTPMixin):
    source = "naukri"

    def _fetch_job_details(self, url: str) -> Dict[str, Any]:
        try:
            soup = self.soup(url)
            salary = ""
            description = ""

            salary_el = soup.select_one(
                "[class*='salary'], span.sal, div.salary, "
                "[data-testid='salary'], .other-details span"
            )
            if salary_el:
                salary = salary_el.get_text(" ", strip=True)

            desc_el = soup.select_one(
                "[class*='job-desc'], section.job-desc, "
                "div.dang-inner-html, [class*='description']"
            )
            if desc_el:
                description = desc_el.get_text(" ", strip=True)[:1000]

            if not salary and description:
                salary = extract_salary_from_text(description)

            return {"salary": salary, "description": description}
        except Exception:
            return {"salary": "", "description": ""}

    def search(self, keywords: Iterable[str], location: str) -> SourceResult:
        jobs: List[Dict[str, Any]] = []
        errors: List[str] = []
        seen_urls: set = set()
        clean_location = quote_plus(location.replace(" ", "-").lower())
        for keyword in keywords:
            slug = quote_plus(keyword.replace("#", "sharp").replace(" ", "-").lower())
            url = f"https://www.naukri.com/{slug}-jobs-in-{clean_location}"
            try:
                soup = self.soup(url)
                cards = soup.select("article.jobTuple, div.srp-jobtuple-wrapper")
                for card in cards[:20]:
                    title_el = card.select_one("a.title")
                    company_el = card.select_one("a.comp-name")
                    location_el = card.select_one("span.locWdth")
                    salary_el = card.select_one("span.sal")
                    desc_el = card.select_one("span.job-desc")
                    if not title_el:
                        continue
                    job_url = title_el.get("href") or url
                    if job_url in seen_urls:
                        continue
                    seen_urls.add(job_url)
                    jobs.append(
                        normalize_job(
                            self.source,
                            {
                                "title": title_el.get_text(" ", strip=True),
                                "company": company_el.get_text(" ", strip=True) if company_el else "Naukri Listing",
                                "location": location_el.get_text(" ", strip=True) if location_el else location,
                                "salary": salary_el.get_text(" ", strip=True) if salary_el else "",
                                "description": desc_el.get_text(" ", strip=True) if desc_el else "",
                                "url": job_url,
                            },
                        )
                    )
            except Exception as exc:
                errors.append(f"Naukri search failed for '{keyword}': {exc}")
        return SourceResult(self.source, jobs, errors)


class BoardFeedAdapter(HTTPMixin):
    """Fetch jobs from direct ATS boards such as Greenhouse, Lever, and Workday."""

    def __init__(self, source: str, board_urls: Iterable[str]):
        self.source = source
        self.board_urls = [url for url in board_urls if url]

    def search(self) -> SourceResult:
        jobs: List[Dict[str, Any]] = []
        errors: List[str] = []
        for url in self.board_urls:
            try:
                jobs.extend(self._search_one(url))
            except Exception as exc:
                errors.append(f"{self.source} board failed for {url}: {exc}")
        return SourceResult(self.source, jobs, errors)

    def _search_one(self, url: str) -> List[Dict[str, Any]]:
        html = self.fetch(url)
        soup = BeautifulSoup(html, "html.parser")
        discovered: List[Dict[str, Any]] = []

        if self.source == "greenhouse":
            for office in soup.select("section.level-0"):
                location_el = office.select_one("h3, h2")
                for link in office.select("a[href*='/jobs/']"):
                    job_url = urljoin(url, link.get("href") or "")
                    discovered.append(
                        normalize_job(
                            self.source,
                            {
                                "title": link.get_text(" ", strip=True),
                                "company": self._company_from_url(url),
                                "location": location_el.get_text(" ", strip=True) if location_el else "",
                                "url": job_url,
                                "salary": "",
                                "description": link.get_text(" ", strip=True),
                            },
                        )
                    )
            return discovered

        if self.source == "lever":
            for link in soup.select("a[href*='/jobs/'], a.posting-title"):
                text = link.get_text(" ", strip=True)
                if not text:
                    continue
                parent = link.parent
                location = ""
                if parent:
                    loc = parent.select_one(".sort-by-location, .posting-categories .location")
                    if loc:
                        location = loc.get_text(" ", strip=True)
                job_url = urljoin(url, link.get("href") or "")
                discovered.append(
                    normalize_job(
                        self.source,
                        {
                            "title": text,
                            "company": self._company_from_url(url),
                            "location": location,
                            "url": job_url,
                            "salary": "",
                            "description": text,
                        },
                    )
                )
            return discovered

        if self.source == "workday":
            for script in soup.select("script[type='application/ld+json']"):
                try:
                    payload = json.loads(script.get_text())
                except json.JSONDecodeError:
                    continue
                jobs_payload = payload if isinstance(payload, list) else [payload]
                for item in jobs_payload:
                    if item.get("@type") != "JobPosting":
                        continue
                    job_url = item.get("url") or url
                    raw_desc = _strip_html(item.get("description", ""))
                    # Workday structured data sometimes includes salary
                    salary = ""
                    base_salary = item.get("baseSalary") or {}
                    if base_salary:
                        low = base_salary.get("value", {}).get("minValue", "")
                        high = base_salary.get("value", {}).get("maxValue", "")
                        currency = base_salary.get("currency", "")
                        if low and high:
                            salary = f"{currency} {low} - {high}".strip()
                    if not salary:
                        salary = extract_salary_from_text(raw_desc)
                    discovered.append(
                        normalize_job(
                            self.source,
                            {
                                "title": item.get("title", ""),
                                "company": self._company_from_url(url),
                                "location": _json_location(item),
                                "description": raw_desc,
                                "salary": salary,
                                "url": job_url,
                                "external_id": item.get("identifier", {}).get("value"),
                            },
                        )
                    )
            return discovered

        return discovered

    def _fetch_detail_page(self, url: str) -> Dict[str, Any]:
        """Fetch salary and description from a company ATS job detail page."""
        try:
            soup = self.soup(url)
            description = ""
            salary = ""

            # Generic description selectors that work across Greenhouse/Lever
            desc_el = soup.select_one(
                "#content, .content, .posting-description, "
                "[class*='description'], [class*='job-details'], main"
            )
            if desc_el:
                description = desc_el.get_text(" ", strip=True)[:1000]

            # Try structured data first
            for script in soup.select("script[type='application/ld+json']"):
                try:
                    data = json.loads(script.get_text())
                    if data.get("@type") == "JobPosting":
                        raw = _strip_html(data.get("description", ""))
                        if raw:
                            description = raw[:1000]
                        base_salary = data.get("baseSalary") or {}
                        if base_salary:
                            low = base_salary.get("value", {}).get("minValue", "")
                            high = base_salary.get("value", {}).get("maxValue", "")
                            currency = base_salary.get("currency", "")
                            if low and high:
                                salary = f"{currency} {low} - {high}".strip()
                        break
                except Exception:
                    continue

            if not salary:
                salary = extract_salary_from_text(description)

            return {"salary": salary, "description": description}
        except Exception:
            return {"salary": "", "description": ""}

    @staticmethod
    def _company_from_url(url: str) -> str:
        host = re.sub(r"^https?://", "", url).split("/")[0]
        return host.replace("jobs.", "").replace("careers.", "").split(".")[0].title()


def _strip_html(value: str) -> str:
    return BeautifulSoup(value or "", "html.parser").get_text(" ", strip=True)


def _json_location(item: Dict[str, Any]) -> str:
    job_location = item.get("jobLocation") or {}
    if isinstance(job_location, list):
        job_location = job_location[0] if job_location else {}
    address = job_location.get("address") or {}
    parts = [address.get("addressLocality"), address.get("addressRegion"), address.get("addressCountry")]
    return ", ".join(part for part in parts if part)

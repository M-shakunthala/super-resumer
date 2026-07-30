"""Shared Selenium-powered ATS handler infrastructure."""

from __future__ import annotations

import os
import time
from abc import ABC
from typing import Any, Dict, Iterable, List, Tuple

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from agents.form_filler import FormFiller
from infra.browser import BrowserManager


class BaseATSHandler(ABC):
    platform_name = "unknown"
    start_button_selectors: List[Tuple[str, str]] = []
    submit_button_selectors: List[Tuple[str, str]] = []
    file_input_selectors: List[Tuple[str, str]] = [(By.CSS_SELECTOR, "input[type='file']")]

    def __init__(self, headless: bool = True):
        self.browser = BrowserManager(headless=headless)
        self.answers = FormFiller()

    def apply(self, job: Dict[str, Any], resume_path: str, auto_submit: bool = True) -> Dict[str, Any]:
        is_valid, error_msg = self.validate_job(job)
        if not is_valid:
            return self._result(job, "failed", error=error_msg)

        if not os.path.exists(resume_path):
            return self._result(job, "failed", error=f"Resume file not found: {resume_path}")

        driver = self.browser.get_driver()
        try:
            driver.get(job["url"])
            self._wait_for_page(driver)
            self.ensure_logged_in(driver)

            started = self.start_application(driver)
            uploaded = self.upload_resume(driver, resume_path)
            filled = self.fill_known_fields(driver)

            if auto_submit:
                submitted = self.submit(driver)
                if submitted:
                    return self._result(
                        job,
                        "submitted",
                        message="Browser-confirmed submission flow completed",
                        details={"started": started, "uploaded": uploaded, "filled": filled},
                    )
                return self._result(
                    job,
                    "needs_manual_review",
                    message="Submission button or confirmation not detected",
                    details={"started": started, "uploaded": uploaded, "filled": filled},
                )

            return self._result(
                job,
                "prepared",
                message="Application prepared without final submit",
                details={"started": started, "uploaded": uploaded, "filled": filled},
            )
        except (TimeoutException, WebDriverException) as exc:
            return self._result(job, "failed", error=str(exc))
        except Exception as exc:
            return self._result(job, "failed", error=str(exc))

    def validate_job(self, job: Dict[str, Any]) -> tuple[bool, str]:
        if not job.get("url"):
            return False, "Job URL is required"
        if not job.get("company"):
            return False, "Company name is required"
        return True, ""

    def ensure_logged_in(self, driver: WebDriver) -> None:
        """Override when a platform requires explicit login checks."""

    def start_application(self, driver: WebDriver) -> bool:
        button = self._find_clickable(driver, self.start_button_selectors, timeout=5)
        if not button:
            return False
        button.click()
        time.sleep(2)
        return True

    def upload_resume(self, driver: WebDriver, resume_path: str) -> bool:
        element = self._find_visible(driver, self.file_input_selectors, timeout=5)
        if not element:
            return False
        element.send_keys(os.path.abspath(resume_path))
        time.sleep(2)
        return True

    def fill_known_fields(self, driver: WebDriver) -> bool:
        field_keywords = {
            "email": ["email"],
            "phone": ["phone", "mobile"],
            "first_name": ["first", "given"],
            "last_name": ["last", "family", "surname"],
            "linkedin_url": ["linkedin"],
            "github_url": ["github"],
            "portfolio_url": ["portfolio", "website"],
            "work_authorization": ["authorization", "visa"],
            "notice_period": ["notice"],
            "salary_expectation": ["salary", "compensation", "ctc"],
            "location": ["location", "city"],
        }
        filled_any = False

        for element in driver.find_elements(By.CSS_SELECTOR, "input, textarea, select"):
            name = " ".join(
                filter(
                    None,
                    [
                        element.get_attribute("name"),
                        element.get_attribute("id"),
                        element.get_attribute("placeholder"),
                        element.get_attribute("aria-label"),
                    ],
                )
            ).lower()
            if not name:
                continue

            for answer_key, aliases in field_keywords.items():
                if not any(alias in name for alias in aliases):
                    continue
                value = FormFiller.get_answer(answer_key)
                if not value:
                    continue
                try:
                    tag = element.tag_name.lower()
                    if tag == "select":
                        Select(element).select_by_visible_text(value)
                    elif element.get_attribute("type") in {"checkbox", "radio"}:
                        if value.lower() in {"yes", "true", "1"} and not element.is_selected():
                            driver.execute_script("arguments[0].click();", element)
                    else:
                        if not element.get_attribute("value"):
                            element.clear()
                            element.send_keys(value)
                    filled_any = True
                    break
                except Exception:
                    continue
        return filled_any

    def submit(self, driver: WebDriver) -> bool:
        button = self._find_clickable(driver, self.submit_button_selectors, timeout=5)
        if not button:
            return False
        driver.execute_script("arguments[0].click();", button)
        time.sleep(3)
        return self.detect_confirmation(driver)

    def detect_confirmation(self, driver: WebDriver) -> bool:
        page_text = driver.page_source.lower()
        return any(
            marker in page_text
            for marker in [
                "application submitted",
                "thanks for applying",
                "you have applied",
                "thank you for applying",
                "application received",
            ]
        )

    def _wait_for_page(self, driver: WebDriver) -> None:
        WebDriverWait(driver, 20).until(
            lambda current: current.execute_script("return document.readyState") == "complete"
        )

    def _find_clickable(
        self,
        driver: WebDriver,
        selectors: Iterable[Tuple[str, str]],
        timeout: int,
    ):
        for by, selector in selectors:
            try:
                return WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((by, selector))
                )
            except TimeoutException:
                continue
        return None

    def _find_visible(
        self,
        driver: WebDriver,
        selectors: Iterable[Tuple[str, str]],
        timeout: int,
    ):
        for by, selector in selectors:
            try:
                return WebDriverWait(driver, timeout).until(
                    EC.visibility_of_element_located((by, selector))
                )
            except TimeoutException:
                continue
        return None

    def _result(
        self,
        job: Dict[str, Any],
        status: str,
        message: str = "",
        error: str = "",
        details: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        return {
            "status": status,
            "platform": self.platform_name,
            "job": job,
            "message": message,
            "error": error,
            "details": details or {},
        }

    def get_platform_info(self) -> Dict[str, Any]:
        return {
            "platform": self.platform_name,
            "handler": self.__class__.__name__,
            "supports_application": True,
            "supports_status_check": False,
            "requires_login": True,
        }

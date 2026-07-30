"""LinkedIn ATS handler."""

from selenium.webdriver.common.by import By

from agents.handlers.base_handler import BaseATSHandler


class LinkedInHandler(BaseATSHandler):
    platform_name = "linkedin"
    start_button_selectors = [
        (By.CSS_SELECTOR, ".jobs-apply-button"),
        (By.CSS_SELECTOR, "button[aria-label*='Easy Apply']"),
        (By.XPATH, "//button[contains(., 'Easy Apply')]"),
    ]
    submit_button_selectors = [
        (By.CSS_SELECTOR, "button[aria-label*='Submit application']"),
        (By.CSS_SELECTOR, "button[aria-label*='Review your application']"),
        (By.XPATH, "//button[contains(., 'Submit application')]"),
        (By.XPATH, "//button[contains(., 'Next')]"),
    ]

    def validate_job(self, job):
        valid, error = super().validate_job(job)
        if not valid:
            return valid, error
        if "linkedin.com" not in job["url"].lower():
            return False, "URL must be from LinkedIn"
        return True, ""

"""Naukri ATS handler."""

from selenium.webdriver.common.by import By

from agents.handlers.base_handler import BaseATSHandler


class NaukriHandler(BaseATSHandler):
    platform_name = "naukri"
    start_button_selectors = [
        (By.CSS_SELECTOR, "button.apply-button"),
        (By.CSS_SELECTOR, "button.styles_apply-button__uJI3A"),
        (By.XPATH, "//button[contains(., 'Apply')]"),
        (By.XPATH, "//a[contains(., 'Apply')]"),
    ]
    submit_button_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(., 'Submit')]"),
        (By.XPATH, "//button[contains(., 'Continue')]"),
    ]

    def validate_job(self, job):
        valid, error = super().validate_job(job)
        if not valid:
            return valid, error
        if "naukri.com" not in job["url"].lower():
            return False, "URL must be from Naukri"
        return True, ""

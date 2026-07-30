"""Workday ATS handler."""

from selenium.webdriver.common.by import By

from agents.handlers.base_handler import BaseATSHandler


class WorkdayHandler(BaseATSHandler):
    platform_name = "workday"
    start_button_selectors = [
        (By.CSS_SELECTOR, "a[data-automation-id='applyManually']"),
        (By.CSS_SELECTOR, "button[data-automation-id='applyManually']"),
        (By.XPATH, "//a[contains(., 'Apply')]"),
        (By.XPATH, "//button[contains(., 'Apply')]"),
    ]
    submit_button_selectors = [
        (By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']"),
        (By.CSS_SELECTOR, "button[data-automation-id='submit']"),
        (By.XPATH, "//button[contains(., 'Submit')]"),
        (By.XPATH, "//button[contains(., 'Continue')]"),
    ]

    def validate_job(self, job):
        valid, error = super().validate_job(job)
        if not valid:
            return valid, error
        if "workday" not in job["url"].lower():
            return False, "URL must be from Workday"
        return True, ""

"""Indeed ATS handler."""

from selenium.webdriver.common.by import By

from agents.handlers.base_handler import BaseATSHandler


class IndeedHandler(BaseATSHandler):
    platform_name = "indeed"
    start_button_selectors = [
        (By.CSS_SELECTOR, "[data-testid='indeedApplyButton']"),
        (By.XPATH, "//button[contains(., 'Apply now')]"),
        (By.XPATH, "//a[contains(., 'Apply now')]"),
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
        if "indeed." not in job["url"].lower():
            return False, "URL must be from Indeed"
        return True, ""

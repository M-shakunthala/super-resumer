"""Lever ATS handler."""

from selenium.webdriver.common.by import By

from agents.handlers.base_handler import BaseATSHandler


class LeverHandler(BaseATSHandler):
    platform_name = "lever"
    start_button_selectors = [
        (By.CSS_SELECTOR, "a.postings-btn"),
        (By.CSS_SELECTOR, "a[href*='apply']"),
        (By.XPATH, "//a[contains(., 'Apply')]"),
        (By.XPATH, "//button[contains(., 'Apply')]"),
    ]
    submit_button_selectors = [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(., 'Submit')]"),
        (By.XPATH, "//button[contains(., 'Send Application')]"),
    ]

    def validate_job(self, job):
        valid, error = super().validate_job(job)
        if not valid:
            return valid, error
        if "lever.co" not in job["url"].lower():
            return False, "URL must be from Lever"
        return True, ""

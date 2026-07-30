"""
LinkedIn Apply Handler
Uses robust infrastructure (BrowserManager, Waits, SafeActions) for reliable job applications
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from loguru import logger
import sys
import os

from agents.base_apply import BaseApply

# Import infrastructure modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from job_agent.infra.browser import BrowserManager
from job_agent.infra.waits import Waits
from job_agent.infra.safe_actions import SafeActions

# Import form filler for user data
from automation.form_filler import FormFiller
from automation.linkedin_login import LinkedInLogin


class LinkedInApply(BaseApply):
    """Robust LinkedIn job application engine using improved infrastructure"""

    def __init__(self, headless: bool = False):
        """
        Initialize LinkedIn apply engine
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.browser_manager = BrowserManager(headless=headless)
        self.driver = None
        self.login_checker = LinkedInLogin()

    def _get_driver(self):
        """Get or create WebDriver instance"""
        if self.driver is None:
            self.driver = self.browser_manager.get_driver()
        return self.driver

    def _ensure_logged_in(self):
        """Ensure user is logged into LinkedIn"""
        try:
            driver = self._get_driver()
            
            if not self.login_checker.is_logged_in(driver):
                logger.warning("Not logged into LinkedIn, please log in manually...")
                logger.info("Waiting for manual login (60 seconds timeout)...")
                
                if self.login_checker.wait_for_login(driver, timeout=60):
                    logger.info("✅ Login successful")
                    return True
                else:
                    logger.error("❌ Login timeout")
                    return False
            
            logger.info("✅ Already logged into LinkedIn")
            return True
            
        except Exception as e:
            logger.error(f"Error ensuring login: {e}")
            return False

    def _find_easy_apply_button(self, driver):
        """
        Find Easy Apply button using multiple selectors
        
        Args:
            driver: WebDriver instance
            
        Returns:
            WebElement if found, None otherwise
        """
        easy_apply_selectors = [
            (By.CLASS_NAME, "jobs-apply-button"),
            (By.CSS_SELECTOR, "button[aria-label*='Easy Apply']"),
            (By.CSS_SELECTOR, "button[data-test='easy-apply-button']"),
            (By.XPATH, "//button[contains(text(), 'Easy Apply')]"),
            (By.CSS_SELECTOR, ".jobs-apply-button--top-card"),
        ]
        
        for selector_type, selector_value in easy_apply_selectors:
            try:
                element = Waits.visible(driver, (selector_type, selector_value), timeout=5)
                if element:
                    logger.info(f"Found Easy Apply button using selector: {selector_value}")
                    return element
            except TimeoutException:
                logger.debug(f"Easy Apply button not found with selector: {selector_value}")
                continue
        
        logger.warning("Easy Apply button not found with any selector")
        return None

    def _fill_form_fields(self, driver):
        """
        Fill common form fields (phone, email, etc.)
        
        Args:
            driver: WebDriver instance
        """
        try:
            # Phone number field
            phone_selectors = [
                (By.CSS_SELECTOR, "input[type='tel']"),
                (By.CSS_SELECTOR, "input[name='phone']"),
                (By.CSS_SELECTOR, "input[id*='phone']"),
                (By.CSS_SELECTOR, "input[placeholder*='phone']"),
            ]
            
            phone = FormFiller.get_answer("phone")
            if phone:
                for selector_type, selector_value in phone_selectors:
                    try:
                        phone_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if phone_input:
                            SafeActions.safe_send_keys(driver, phone_input, phone, clear_first=True)
                            logger.info(f"Filled phone number: {phone}")
                            break
                    except TimeoutException:
                        continue
            
            # Email field (if needed)
            email = FormFiller.get_answer("email")
            if email:
                email_selectors = [
                    (By.CSS_SELECTOR, "input[type='email']"),
                    (By.CSS_SELECTOR, "input[name='email']"),
                    (By.CSS_SELECTOR, "input[id*='email']"),
                ]
                
                for selector_type, selector_value in email_selectors:
                    try:
                        email_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if email_input and email_input.get_attribute("value") == "":
                            SafeActions.safe_send_keys(driver, email_input, email, clear_first=True)
                            logger.info(f"Filled email: {email}")
                            break
                    except TimeoutException:
                        continue
            
            logger.info("Form fields filled successfully")
            
        except Exception as e:
            logger.warning(f"Error filling form fields: {e}")

    def _upload_resume(self, driver, resume_path):
        """
        Upload resume using file input
        
        Args:
            driver: WebDriver instance
            resume_path: Path to resume file
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            if not os.path.exists(resume_path):
                logger.error(f"Resume file not found: {resume_path}")
                return False
            
            upload_selectors = [
                (By.CSS_SELECTOR, "input[type='file']"),
                (By.CSS_SELECTOR, "input[name='file']"),
                (By.CSS_SELECTOR, "input[id*='resume']"),
                (By.CSS_SELECTOR, "input[id*='upload']"),
            ]
            
            for selector_type, selector_value in upload_selectors:
                try:
                    upload_input = Waits.visible(driver, (selector_type, selector_value), timeout=5)
                    if upload_input:
                        upload_input.send_keys(resume_path)
                        logger.info(f"Resume uploaded: {resume_path}")
                        
                        # Wait for upload to complete
                        import time
                        time.sleep(2)
                        
                        return True
                except TimeoutException:
                    continue
            
            logger.warning("No file upload input found")
            return False
            
        except Exception as e:
            logger.error(f"Error uploading resume: {e}")
            return False

    def _submit_application(self, driver):
        """
        Submit the application
        
        Args:
            driver: WebDriver instance
            
        Returns:
            True if submission successful, False otherwise
        """
        try:
            submit_selectors = [
                (By.CSS_SELECTOR, "button[aria-label='Submit application']"),
                (By.CSS_SELECTOR, "button[aria-label*='Submit']"),
                (By.CSS_SELECTOR, "button[data-test='submit-application']"),
                (By.XPATH, "//button[contains(text(), 'Submit')]"),
                (By.CSS_SELECTOR, ".jobs-apply-button"),
            ]
            
            for selector_type, selector_value in submit_selectors:
                try:
                    submit_button = Waits.clickable(driver, (selector_type, selector_value), timeout=5)
                    if submit_button:
                        SafeActions.safe_click(driver, submit_button)
                        logger.info("Application submitted successfully")
                        
                        # Wait for confirmation
                        import time
                        time.sleep(2)
                        
                        return True
                except TimeoutException:
                    continue
            
            logger.warning("Submit button not found")
            return False
            
        except Exception as e:
            logger.error(f"Error submitting application: {e}")
            return False

    def apply(
        self,
        job_url,
        resume_path,
        auto_submit: bool = True
    ):
        """
        Apply to a LinkedIn job with robust error handling
        
        Args:
            job_url: LinkedIn job URL
            resume_path: Path to resume file
            auto_submit: Whether to automatically submit the application
            
        Returns:
            Dictionary with application status and details
        """
        result = {
            "success": False,
            "job_url": job_url,
            "resume_uploaded": False,
            "form_filled": False,
            "submitted": False,
            "error": None,
            "message": ""
        }
        
        try:
            logger.info(f"Starting application process for: {job_url}")
            driver = self._get_driver()
            
            # Ensure logged in
            if not self._ensure_logged_in():
                result["error"] = "Not logged into LinkedIn"
                result["message"] = "Please log in and try again"
                return result
            
            # Navigate to job page
            logger.info(f"Navigating to job page: {job_url}")
            driver.get(job_url)
            Waits.page_loaded(driver, timeout=30)
            
            # Find and click Easy Apply button
            logger.info("Looking for Easy Apply button...")
            easy_apply_button = self._find_easy_apply_button(driver)
            
            if not easy_apply_button:
                result["error"] = "Easy Apply button not found"
                result["message"] = "Job may not support Easy Apply or button selector changed"
                return result
            
            # Click Easy Apply button
            logger.info("Clicking Easy Apply button...")
            SafeActions.safe_click(driver, easy_apply_button)
            
            # Wait for application modal
            import time
            time.sleep(3)
            
            # Fill form fields
            logger.info("Filling form fields...")
            self._fill_form_fields(driver)
            result["form_filled"] = True
            
            # Upload resume
            logger.info("Uploading resume...")
            if self._upload_resume(driver, resume_path):
                result["resume_uploaded"] = True
            else:
                logger.warning("Resume upload failed, but continuing...")
            
            if auto_submit:
                # Submit application
                logger.info("Submitting application...")
                if self._submit_application(driver):
                    result["submitted"] = True
                    result["success"] = True
                    result["message"] = "Application submitted successfully"
                    logger.info("✅ Application submitted successfully")
                else:
                    result["error"] = "Failed to submit application"
                    result["message"] = "Please review and submit manually"
            else:
                result["message"] = "Application prepared, please review and submit manually"
                logger.info("Application prepared for manual review")
            
        except TimeoutException as e:
            logger.error(f"Timeout during application: {e}")
            result["error"] = "Timeout"
            result["message"] = "Operation timed out, please try again"
            
        except WebDriverException as e:
            logger.error(f"WebDriver error during application: {e}")
            result["error"] = "WebDriver error"
            result["message"] = f"Browser error: {e}"
            
        except Exception as e:
            logger.error(f"Unexpected error during application: {e}")
            result["error"] = "Unexpected error"
            result["message"] = f"Error: {e}"
        
        return result

    def apply_batch(self, job_urls: list, resume_path: str) -> list:
        """
        Apply to multiple jobs in batch
        
        Args:
            job_urls: List of LinkedIn job URLs
            resume_path: Path to resume file
            
        Returns:
            List of application results
        """
        results = []
        
        for i, job_url in enumerate(job_urls, 1):
            logger.info(f"Processing job {i}/{len(job_urls)}: {job_url}")
            
            result = self.apply(job_url, resume_path)
            results.append(result)
            
            # Wait between applications to avoid rate limiting
            if i < len(job_urls):
                import time
                wait_time = 5 + (i * 2)  # Progressive wait
                logger.info(f"Waiting {wait_time} seconds before next application...")
                time.sleep(wait_time)
        
        successful = sum(1 for r in results if r["success"])
        logger.info(f"Batch application complete: {successful}/{len(job_urls)} successful")
        
        return results

    def close(self):
        """Close browser instance"""
        if self.browser_manager:
            self.browser_manager.close()
            logger.info("Browser closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
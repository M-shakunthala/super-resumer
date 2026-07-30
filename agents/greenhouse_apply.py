"""
Greenhouse Apply Handler
Handles job applications on Greenhouse-based company career pages
"""
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from loguru import logger
import sys
import os
import time

from agents.base_apply import BaseApply

# Import infrastructure modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from job_agent.infra.browser import BrowserManager
from job_agent.infra.waits import Waits
from job_agent.infra.safe_actions import SafeActions

# Import form filler for user data
from automation.form_filler import FormFiller


class GreenhouseApply(BaseApply):
    """Greenhouse job application handler with standardized form detection"""

    def __init__(self, headless: bool = False):
        """
        Initialize Greenhouse apply engine
        
        Args:
            headless: Whether to run browser in headless mode
        """
        self.browser_manager = BrowserManager(headless=headless)
        self.driver = None

    def _get_driver(self):
        """Get or create WebDriver instance"""
        if self.driver is None:
            self.driver = self.browser_manager.get_driver()
        return self.driver

    def _detect_greenhouse_page(self, driver):
        """
        Detect if current page is a Greenhouse application page
        
        Args:
            driver: WebDriver instance
            
        Returns:
            True if Greenhouse page detected, False otherwise
        """
        greenhouse_indicators = [
            "greenhouse",
            "greenhouse.io",
            "boards.greenhouse"
        ]
        
        current_url = driver.current_url.lower()
        return any(indicator in current_url for indicator in greenhouse_indicators)

    def _find_resume_upload(self, driver):
        """
        Find resume upload input on Greenhouse page
        
        Args:
            driver: WebDriver instance
            
        Returns:
            WebElement if found, None otherwise
        """
        upload_selectors = [
            (By.CSS_SELECTOR, "input[type='file']"),
            (By.CSS_SELECTOR, "input[name*='resume']"),
            (By.CSS_SELECTOR, "input[id*='resume']"),
            (By.CSS_SELECTOR, "input[accept*='pdf']"),
            (By.CSS_SELECTOR, "input[accept*='.doc']"),
            (By.XPATH, "//input[contains(@accept, 'pdf')]"),
        ]
        
        for selector_type, selector_value in upload_selectors:
            try:
                upload_input = Waits.visible(driver, (selector_type, selector_value), timeout=5)
                if upload_input:
                    logger.info(f"Found resume upload using selector: {selector_value}")
                    return upload_input
            except TimeoutException:
                continue
        
        logger.warning("Resume upload input not found")
        return None

    def _fill_text_field(self, driver, field_name, value, selectors=None):
        """
        Fill a text field with multiple selector fallbacks
        
        Args:
            driver: WebDriver instance
            field_name: Name of the field (for logging and default selectors)
            value: Value to fill
            selectors: Optional list of (By, selector) tuples
            
        Returns:
            True if field filled successfully, False otherwise
        """
        if not value:
            logger.debug(f"No value provided for {field_name}")
            return False
            
        if selectors is None:
            selectors = [
                (By.CSS_SELECTOR, f"input[name*='{field_name}']"),
                (By.CSS_SELECTOR, f"input[id*='{field_name}']"),
                (By.CSS_SELECTOR, f"input[placeholder*='{field_name}']"),
                (By.XPATH, f"//label[contains(text(), '{field_name}')]/following-sibling::input"),
                (By.XPATH, f"//label[contains(text(), '{field_name}')]/../input"),
            ]
        
        for selector_type, selector_value in selectors:
            try:
                field_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                if field_input and field_input.get_attribute("value") == "":
                    SafeActions.safe_send_keys(driver, field_input, value, clear_first=True)
                    logger.info(f"Filled {field_name}: {value}")
                    return True
            except TimeoutException:
                continue
        
        logger.debug(f"Could not find field: {field_name}")
        return False

    def _fill_linkedin_url(self, driver):
        """
        Fill LinkedIn URL field
        
        Args:
            driver: WebDriver instance
        """
        try:
            linkedin_url = FormFiller.get_answer("linkedin_url")
            if linkedin_url:
                linkedin_selectors = [
                    (By.CSS_SELECTOR, "input[name*='linkedin']"),
                    (By.CSS_SELECTOR, "input[id*='linkedin']"),
                    (By.CSS_SELECTOR, "input[placeholder*='LinkedIn']"),
                    (By.XPATH, "//label[contains(text(), 'LinkedIn')]/following-sibling::input"),
                    (By.XPATH, "//label[contains(text(), 'linkedin')]/following-sibling::input"),
                ]
                
                for selector_type, selector_value in linkedin_selectors:
                    try:
                        linkedin_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if linkedin_input and linkedin_input.get_attribute("value") == "":
                            SafeActions.safe_send_keys(driver, linkedin_input, linkedin_url, clear_first=True)
                            logger.info(f"Filled LinkedIn URL: {linkedin_url}")
                            return True
                    except TimeoutException:
                        continue
            
            return False
            
        except Exception as e:
            logger.warning(f"Error filling LinkedIn URL: {e}")
            return False

    def _fill_phone(self, driver):
        """
        Fill phone number field
        
        Args:
            driver: WebDriver instance
        """
        try:
            phone = FormFiller.get_answer("phone")
            if phone:
                return self._fill_text_field(driver, "phone", phone)
            
            return False
            
        except Exception as e:
            logger.warning(f"Error filling phone: {e}")
            return False

    def _fill_portfolio(self, driver):
        """
        Fill portfolio URL field
        
        Args:
            driver: WebDriver instance
        """
        try:
            portfolio_url = FormFiller.get_answer("portfolio_url")
            if portfolio_url:
                portfolio_selectors = [
                    (By.CSS_SELECTOR, "input[name*='portfolio']"),
                    (By.CSS_SELECTOR, "input[name*='website']"),
                    (By.CSS_SELECTOR, "input[id*='portfolio']"),
                    (By.CSS_SELECTOR, "input[placeholder*='portfolio']"),
                    (By.CSS_SELECTOR, "input[placeholder*='website']"),
                    (By.XPATH, "//label[contains(text(), 'Portfolio')]/following-sibling::input"),
                    (By.XPATH, "//label[contains(text(), 'Website')]/following-sibling::input"),
                ]
                
                for selector_type, selector_value in portfolio_selectors:
                    try:
                        portfolio_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if portfolio_input and portfolio_input.get_attribute("value") == "":
                            SafeActions.safe_send_keys(driver, portfolio_input, portfolio_url, clear_first=True)
                            logger.info(f"Filled portfolio URL: {portfolio_url}")
                            return True
                    except TimeoutException:
                        continue
            
            return False
            
        except Exception as e:
            logger.warning(f"Error filling portfolio: {e}")
            return False

    def _fill_email(self, driver):
        """
        Fill email field (if not pre-filled)
        
        Args:
            driver: WebDriver instance
        """
        try:
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
                            return True
                    except TimeoutException:
                        continue
            
            return False
            
        except Exception as e:
            logger.warning(f"Error filling email: {e}")
            return False

    def _fill_name_fields(self, driver):
        """
        Fill name fields (first name, last name)
        
        Args:
            driver: WebDriver instance
        """
        try:
            # First name
            first_name = FormFiller.get_answer("first_name")
            if first_name:
                first_name_selectors = [
                    (By.CSS_SELECTOR, "input[name*='first']"),
                    (By.CSS_SELECTOR, "input[name*='given']"),
                    (By.CSS_SELECTOR, "input[id*='first']"),
                    (By.XPATH, "//label[contains(text(), 'First')]/following-sibling::input"),
                ]
                
                for selector_type, selector_value in first_name_selectors:
                    try:
                        name_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if name_input and name_input.get_attribute("value") == "":
                            SafeActions.safe_send_keys(driver, name_input, first_name, clear_first=True)
                            logger.info(f"Filled first name: {first_name}")
                            break
                    except TimeoutException:
                        continue
            
            # Last name
            last_name = FormFiller.get_answer("last_name")
            if last_name:
                last_name_selectors = [
                    (By.CSS_SELECTOR, "input[name*='last']"),
                    (By.CSS_SELECTOR, "input[name*='family']"),
                    (By.CSS_SELECTOR, "input[id*='last']"),
                    (By.XPATH, "//label[contains(text(), 'Last')]/following-sibling::input"),
                ]
                
                for selector_type, selector_value in last_name_selectors:
                    try:
                        name_input = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if name_input and name_input.get_attribute("value") == "":
                            SafeActions.safe_send_keys(driver, name_input, last_name, clear_first=True)
                            logger.info(f"Filled last name: {last_name}")
                            break
                    except TimeoutException:
                        continue
            
            return True
            
        except Exception as e:
            logger.warning(f"Error filling name fields: {e}")
            return False

    def _find_submit_button(self, driver):
        """
        Find submit button on Greenhouse form
        
        Args:
            driver: WebDriver instance
            
        Returns:
            WebElement if found, None otherwise
        """
        submit_selectors = [
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Submit')]"),
            (By.XPATH, "//button[contains(text(), 'Apply')]"),
            (By.XPATH, "//button[contains(text(), 'Send')]"),
            (By.CSS_SELECTOR, ".submit"),
            (By.CSS_SELECTOR, "[value*='Submit']"),
        ]
        
        for selector_type, selector_value in submit_selectors:
            try:
                submit_button = Waits.clickable(driver, (selector_type, selector_value), timeout=5)
                if submit_button:
                    logger.info(f"Found submit button using selector: {selector_value}")
                    return submit_button
            except TimeoutException:
                continue
        
        logger.warning("Submit button not found")
        return None

    def apply(
        self,
        job_url,
        resume_path,
        auto_submit: bool = True
    ):
        """
        Apply to a Greenhouse job with robust error handling
        
        Args:
            job_url: Greenhouse job URL
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
            logger.info(f"Starting Greenhouse application for: {job_url}")
            driver = self._get_driver()
            
            # Navigate to job page
            logger.info(f"Navigating to job page: {job_url}")
            driver.get(job_url)
            Waits.page_loaded(driver, timeout=30)
            
            # Verify it's a Greenhouse page
            if not self._detect_greenhouse_page(driver):
                result["error"] = "Not a Greenhouse page"
                result["message"] = "URL does not appear to be a Greenhouse application page"
                logger.warning("Page does not appear to be a Greenhouse application")
                return result
            
            logger.info("✅ Greenhouse page detected")
            
            # Upload resume
            logger.info("Uploading resume...")
            resume_input = self._find_resume_upload(driver)
            
            if resume_input:
                if os.path.exists(resume_path):
                    resume_input.send_keys(resume_path)
                    logger.info(f"Resume uploaded: {resume_path}")
                    time.sleep(2)  # Wait for upload processing
                    result["resume_uploaded"] = True
                else:
                    logger.error(f"Resume file not found: {resume_path}")
                    result["error"] = "Resume file not found"
                    return result
            else:
                logger.warning("Resume upload input not found, continuing...")
            
            # Fill standard Greenhouse fields
            logger.info("Filling standard fields...")
            
            # Name fields
            self._fill_name_fields(driver)
            
            # Email
            self._fill_email(driver)
            
            # LinkedIn URL
            self._fill_linkedin_url(driver)
            
            # Phone
            self._fill_phone(driver)
            
            # Portfolio
            self._fill_portfolio(driver)
            
            result["form_filled"] = True
            logger.info("Standard fields filled successfully")
            
            if auto_submit:
                # Submit application
                logger.info("Looking for submit button...")
                submit_button = self._find_submit_button(driver)
                
                if submit_button:
                    SafeActions.safe_click(driver, submit_button)
                    logger.info("Application submitted")
                    result["submitted"] = True
                    result["success"] = True
                    result["message"] = "Application submitted successfully"
                    
                    # Wait for confirmation
                    time.sleep(2)
                else:
                    result["error"] = "Submit button not found"
                    result["message"] = "Please review and submit manually"
                    logger.warning("Could not find submit button - manual submission required")
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
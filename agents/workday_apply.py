"""
Workday Apply Handler
Handles job applications on Workday-based company career pages
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


class WorkdayApply(BaseApply):
    """Workday job application handler with robust field detection"""

    def __init__(self, headless: bool = False):
        """
        Initialize Workday apply engine
        
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

    def _detect_workday_page(self, driver):
        """
        Detect if current page is a Workday application page
        
        Args:
            driver: WebDriver instance
            
        Returns:
            True if Workday page detected, False otherwise
        """
        workday_indicators = [
            "workday",
            "wd5.myworkday",
            "myworkdayjobs",
            "workday.com"
        ]
        
        current_url = driver.current_url.lower()
        return any(indicator in current_url for indicator in workday_indicators)

    def _find_resume_upload(self, driver):
        """
        Find resume upload input on Workday page
        
        Args:
            driver: WebDriver instance
            
        Returns:
            WebElement if found, None otherwise
        """
        upload_selectors = [
            (By.CSS_SELECTOR, "input[type='file']"),
            (By.CSS_SELECTOR, "input[name*='resume']"),
            (By.CSS_SELECTOR, "input[id*='resume']"),
            (By.CSS_SELECTOR, "input[id*='upload']"),
            (By.XPATH, "//input[contains(@accept, 'pdf')]"),
            (By.XPATH, "//input[contains(@accept, 'doc')]"),
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
            field_name: Name of the field (for logging)
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

    def _fill_personal_info(self, driver):
        """
        Fill personal information fields using ProfileMemory
        
        Args:
            driver: WebDriver instance
        """
        try:
            # First name
            first_name = FormFiller.get_answer("first_name")
            if first_name:
                self._fill_text_field(driver, "first", first_name)
                self._fill_text_field(driver, "given", first_name)
                self._fill_text_field(driver, "fname", first_name)
            
            # Last name
            last_name = FormFiller.get_answer("last_name")
            if last_name:
                self._fill_text_field(driver, "last", last_name)
                self._fill_text_field(driver, "family", last_name)
                self._fill_text_field(driver, "lname", last_name)
            
            # Email
            email = FormFiller.get_answer("email")
            if email:
                self._fill_text_field(driver, "email", email)
            
            # Phone
            phone = FormFiller.get_answer("phone")
            if phone:
                self._fill_text_field(driver, "phone", phone)
                self._fill_text_field(driver, "mobile", phone)
                self._fill_text_field(driver, "telephone", phone)
            
            logger.info("Personal information fields filled")
            
        except Exception as e:
            logger.warning(f"Error filling personal info: {e}")

    def _fill_experience_section(self, driver):
        """
        Fill work experience section if present
        
        Args:
            driver: WebDriver instance
        """
        try:
            # This is complex as Workday forms vary significantly
            # For now, we'll detect common patterns and log them
            
            experience_indicators = [
                "experience",
                "employment",
                "work history",
                "job history"
            ]
            
            page_source = driver.page_source.lower()
            if any(indicator in page_source for indicator in experience_indicators):
                logger.info("Experience section detected - manual review may be needed")
                # In a full implementation, this would:
                # 1. Detect experience form structure
                # 2. Parse data from ProfileMemory
                # 3. Fill each experience entry
            
        except Exception as e:
            logger.warning(f"Error handling experience section: {e}")

    def _fill_authorization_fields(self, driver):
        """
        Fill work authorization and visa status fields
        
        Args:
            driver: WebDriver instance
        """
        try:
            # Work authorization status
            authorization = FormFiller.get_answer("work_authorization")
            if authorization:
                # Try different selector patterns for dropdowns/radios
                auth_selectors = [
                    (By.XPATH, "//label[contains(text(), 'authorization')]/../select"),
                    (By.XPATH, "//label[contains(text(), 'visa')]/../select"),
                    (By.CSS_SELECTOR, "select[name*='authorization']"),
                    (By.CSS_SELECTOR, "select[name*='visa']"),
                ]
                
                for selector_type, selector_value in auth_selectors:
                    try:
                        select_element = Waits.visible(driver, (selector_type, selector_value), timeout=3)
                        if select_element:
                            # Try to find matching option
                            from selenium.webdriver.support.ui import Select
                            select = Select(select_element)
                            
                            # Try to find option by text
                            for option in select.options:
                                if authorization.lower() in option.text.lower():
                                    select.select_by_visible_text(option.text)
                                    logger.info(f"Selected authorization status: {option.text}")
                                    return True
                    except TimeoutException:
                        continue
            
            logger.info("Authorization fields processed")
            
        except Exception as e:
            logger.warning(f"Error filling authorization fields: {e}")

    def _handle_additional_questions(self, driver):
        """
        Handle additional questions that may appear on Workday forms
        
        Args:
            driver: WebDriver instance
        """
        try:
            # Look for common question patterns
            question_patterns = [
                "expected salary",
                "notice period",
                "relocation",
                "gender",
                "ethnicity",
                "veteran"
            ]
            
            page_source = driver.page_source.lower()
            found_questions = [q for q in question_patterns if q in page_source]
            
            if found_questions:
                logger.info(f"Additional questions detected: {found_questions}")
                logger.info("These may require manual review")
            
        except Exception as e:
            logger.warning(f"Error handling additional questions: {e}")

    def _find_submit_button(self, driver):
        """
        Find submit button on Workday form
        
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
            (By.XPATH, "//button[contains(text(), 'Continue')]"),
            (By.CSS_SELECTOR, "button[data-automation-id='submit']"),
            (By.CSS_SELECTOR, "button[data-automation-id='continue']"),
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
        Apply to a Workday job with robust error handling
        
        Args:
            job_url: Workday job URL
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
            logger.info(f"Starting Workday application for: {job_url}")
            driver = self._get_driver()
            
            # Navigate to job page
            logger.info(f"Navigating to job page: {job_url}")
            driver.get(job_url)
            Waits.page_loaded(driver, timeout=30)
            
            # Verify it's a Workday page
            if not self._detect_workday_page(driver):
                result["error"] = "Not a Workday page"
                result["message"] = "URL does not appear to be a Workday application page"
                logger.warning("Page does not appear to be a Workday application")
                return result
            
            logger.info("✅ Workday page detected")
            
            # Upload resume
            logger.info("Uploading resume...")
            resume_input = self._find_resume_upload(driver)
            
            if resume_input:
                if os.path.exists(resume_path):
                    resume_input.send_keys(resume_path)
                    logger.info(f"Resume uploaded: {resume_path}")
                    time.sleep(3)  # Wait for upload processing
                    result["resume_uploaded"] = True
                else:
                    logger.error(f"Resume file not found: {resume_path}")
                    result["error"] = "Resume file not found"
                    return result
            else:
                logger.warning("Resume upload input not found, continuing...")
            
            # Fill personal information
            logger.info("Filling personal information...")
            self._fill_personal_info(driver)
            result["form_filled"] = True
            
            # Handle experience section
            logger.info("Processing experience section...")
            self._fill_experience_section(driver)
            
            # Handle authorization fields
            logger.info("Processing authorization fields...")
            self._fill_authorization_fields(driver)
            
            # Handle additional questions
            logger.info("Checking for additional questions...")
            self._handle_additional_questions(driver)
            
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
                    time.sleep(3)
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
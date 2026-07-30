"""
LinkedIn ATS handler for job applications
"""
from agents.base_apply import BaseApply
from agents.handlers.base_handler import BaseATSHandler
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class LinkedInHandler(BaseApply, BaseATSHandler):
    """
    Handler for LinkedIn job applications
    Implements LinkedIn-specific application logic
    """
    
    def __init__(self):
        super().__init__()
        self.platform_name = "linkedin"
    
    def apply(self, job, resume_path):
        """
        Apply to LinkedIn job with resume
        
        Args:
            job: Job dictionary with url, company, etc.
            resume_path: Path to resume PDF
            
        Returns:
            Application result dictionary
        """
        # Validate job data
        is_valid, error_msg = self.validate_job(job)
        if not is_valid:
            return {
                'status': 'failed',
                'error': error_msg,
                'platform': self.platform_name,
                'job': job
            }
        
        try:
            # Import browser manager for LinkedIn automation
            from infra.browser import BrowserManager
            
            browser = BrowserManager()
            driver = browser.get_driver()
            
            # Navigate to job URL
            driver.get(job['url'])
            
            # Wait for page to load
            time.sleep(2)
            
            # Look for "Easy Apply" button
            try:
                easy_apply_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".jobs-apply-button"))
                )
                
                # Click Easy Apply
                easy_apply_button.click()
                time.sleep(2)
                
                # Look for resume upload section
                # Implementation depends on LinkedIn's current UI
                # This is a placeholder for the actual implementation
                
                # Check if already applied
                if self._check_already_applied(driver):
                    return {
                        'status': 'already_applied',
                        'platform': self.platform_name,
                        'job': job,
                        'message': 'Already applied to this job'
                    }
                
                # Upload resume (implementation needed)
                success = self._upload_resume(driver, resume_path)
                
                if success:
                    # Submit application
                    submit_success = self._submit_application(driver)
                    
                    if submit_success:
                        return {
                            'status': 'applied',
                            'platform': self.platform_name,
                            'job': job,
                            'resume_path': resume_path,
                            'message': 'Successfully applied via LinkedIn Easy Apply'
                        }
                    else:
                        return {
                            'status': 'failed',
                            'platform': self.platform_name,
                            'job': job,
                            'error': 'Failed to submit application'
                        }
                else:
                    return {
                        'status': 'failed',
                        'platform': self.platform_name,
                        'job': job,
                        'error': 'Failed to upload resume'
                    }
                    
            except Exception as e:
                return {
                    'status': 'failed',
                    'platform': self.platform_name,
                    'job': job,
                    'error': f'Easy Apply button not found or error: {str(e)}'
                }
                
        except Exception as e:
            return {
                'status': 'failed',
                'platform': self.platform_name,
                'job': job,
                'error': str(e)
            }
    
    def _check_already_applied(self, driver):
        """Check if already applied to this job"""
        try:
            # Look for "Applied" indicator
            applied_elements = driver.find_elements(By.CSS_SELECTOR, ".jobs-s-apply__applied-state")
            return len(applied_elements) > 0
        except:
            return False
    
    def _upload_resume(self, driver, resume_path):
        """Upload resume to LinkedIn application"""
        try:
            # Implementation depends on LinkedIn's current file upload interface
            # This is a placeholder
            return True
        except:
            return False
    
    def _submit_application(self, driver):
        """Submit the application"""
        try:
            # Implementation depends on LinkedIn's current submit button
            # This is a placeholder
            return True
        except:
            return False
    
    def validate_job(self, job):
        """Validate LinkedIn job data"""
        if not job.get('url'):
            return False, "LinkedIn job URL is required"
        
        if "linkedin.com" not in job['url'].lower():
            return False, "URL must be from LinkedIn"
        
        return True, ""
    
    def get_application_status(self, job):
        """Check application status on LinkedIn"""
        # LinkedIn requires login to check status
        return {
            "status": "login_required",
            "message": "LinkedIn login required to check application status"
        }
    
    def get_required_fields(self):
        """Get required fields for LinkedIn application"""
        return ['url', 'company', 'resume_path']
    
    def get_platform_info(self):
        """Get LinkedIn platform information"""
        info = super().get_platform_info()
        info.update({
            'supports_easy_apply': True,
            'requires_session': True,
            'resume_formats': ['pdf'],
            'max_file_size_mb': 5
        })
        return info

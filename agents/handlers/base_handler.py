"""
Base handler class for platform-specific ATS handlers
"""
from abc import ABC, abstractmethod


class BaseATSHandler(ABC):
    """
    Abstract base class for all platform-specific ATS handlers
    Each platform (LinkedIn, Workday, Greenhouse, etc.) implements this interface
    """
    
    def __init__(self):
        """Initialize handler with platform-specific settings"""
        self.platform_name = self.__class__.__name__.replace('Handler', '').lower()
    
    @abstractmethod
    def apply(self, job, resume_path):
        """
        Apply to job using platform-specific logic
        
        Args:
            job: Job dictionary with url, company, description, etc.
            resume_path: Path to resume PDF for application
            
        Returns:
            Dictionary with application status and details
        """
        pass
    
    def validate_job(self, job):
        """
        Validate job data for this platform
        
        Args:
            job: Job dictionary
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not job.get('url'):
            return False, "Job URL is required"
        
        if not job.get('company'):
            return False, "Company name is required"
        
        return True, ""
    
    def get_application_status(self, job):
        """
        Check application status for a job (if supported by platform)
        
        Args:
            job: Job dictionary
            
        Returns:
            Status information (implementation varies by platform)
        """
        return {"status": "unknown", "message": "Status checking not implemented for this platform"}
    
    def extract_job_details(self, url):
        """
        Extract job details from platform URL
        
        Args:
            url: Job URL
            
        Returns:
            Dictionary with job details (implementation varies by platform)
        """
        return {"url": url, "platform": self.platform_name}
    
    def get_required_fields(self):
        """
        Get required fields for this platform's application form
        
        Returns:
            List of required field names
        """
        return ['url', 'company']
    
    def get_platform_info(self):
        """
        Get information about this platform
        
        Returns:
            Dictionary with platform details
        """
        return {
            'platform': self.platform_name,
            'handler': self.__class__.__name__,
            'supports_application': True,
            'supports_status_check': False,
            'requires_login': True
        }

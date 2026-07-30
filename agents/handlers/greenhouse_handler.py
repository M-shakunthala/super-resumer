"""
Greenhouse ATS handler for job applications
"""
from agents.base_apply import BaseApply
from agents.handlers.base_handler import BaseATSHandler


class GreenhouseHandler(BaseApply, BaseATSHandler):
    """
    Handler for Greenhouse job applications
    Implements Greenhouse-specific application logic
    """
    
    def __init__(self):
        super().__init__()
        self.platform_name = "greenhouse"
    
    def apply(self, job, resume_path):
        """Apply to Greenhouse job with resume"""
        return {
            'status': 'not_implemented',
            'platform': self.platform_name,
            'job': job,
            'message': 'Greenhouse handler not fully implemented yet'
        }
    
    def validate_job(self, job):
        """Validate Greenhouse job data"""
        if not job.get('url'):
            return False, "Greenhouse job URL is required"
        
        if "greenhouse" not in job['url'].lower():
            return False, "URL must be from Greenhouse"
        
        return True, ""

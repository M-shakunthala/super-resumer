"""
Lever ATS handler for job applications
"""
from agents.base_apply import BaseApply
from agents.handlers.base_handler import BaseATSHandler


class LeverHandler(BaseApply, BaseATSHandler):
    """
    Handler for Lever job applications
    Implements Lever-specific application logic
    """
    
    def __init__(self):
        super().__init__()
        self.platform_name = "lever"
    
    def apply(self, job, resume_path):
        """Apply to Lever job with resume"""
        return {
            'status': 'not_implemented',
            'platform': self.platform_name,
            'job': job,
            'message': 'Lever handler not fully implemented yet'
        }
    
    def validate_job(self, job):
        """Validate Lever job data"""
        if not job.get('url'):
            return False, "Lever job URL is required"
        
        if "lever.co" not in job['url'].lower():
            return False, "URL must be from Lever"
        
        return True, ""

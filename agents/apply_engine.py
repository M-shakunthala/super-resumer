"""
Apply Engine - Multi-platform job application system
Routes job applications to platform-specific ATS handlers
"""
from agents.platform_detector import PlatformDetector


class ApplyEngine:
    """
    Main engine for job applications across multiple platforms
    Detects platform and routes to appropriate ATS handler
    """
    
    def __init__(self):
        """Initialize apply engine with platform detector"""
        self.platform_detector = PlatformDetector()
        self.handlers = {}
        self._initialize_handlers()
    
    def _initialize_handlers(self):
        """Initialize platform-specific handlers"""
        # Import handlers (will be created as separate modules)
        try:
            from agents.handlers.linkedin_handler import LinkedInHandler
            self.handlers['linkedin'] = LinkedInHandler()
        except ImportError:
            print("⚠️ LinkedIn handler not available")
            self.handlers['linkedin'] = None
        
        try:
            from agents.handlers.workday_handler import WorkdayHandler
            self.handlers['workday'] = WorkdayHandler()
        except ImportError:
            print("⚠️ Workday handler not available")
            self.handlers['workday'] = None
        
        try:
            from agents.handlers.greenhouse_handler import GreenhouseHandler
            self.handlers['greenhouse'] = GreenhouseHandler()
        except ImportError:
            print("⚠️ Greenhouse handler not available")
            self.handlers['greenhouse'] = None
        
        try:
            from agents.handlers.lever_handler import LeverHandler
            self.handlers['lever'] = LeverHandler()
        except ImportError:
            print("⚠️ Lever handler not available")
            self.handlers['lever'] = None
        
        try:
            from agents.handlers.indeed_handler import IndeedHandler
            self.handlers['indeed'] = IndeedHandler()
        except ImportError:
            print("⚠️ Indeed handler not available")
            self.handlers['indeed'] = None
    
    def apply(self, job, resume_path):
        """
        Apply to job using platform-specific handler
        
        Args:
            job: Job dictionary with url, company, etc.
            resume_path: Path to resume PDF for application
            
        Returns:
            Application result with status and platform info
        """
        # Detect platform from job URL
        platform = self.platform_detector.detect(job.get('url', ''))
        
        print(f"🔍 Detected platform: {platform}")
        
        # Get appropriate handler
        handler = self.handlers.get(platform)
        
        if not handler:
            return {
                'status': 'failed',
                'platform': platform,
                'error': f'No handler available for platform: {platform}',
                'job': job
            }
        
        # Apply using platform-specific handler
        try:
            result = handler.apply(job, resume_path)
            result['platform'] = platform
            return result
        except Exception as e:
            return {
                'status': 'failed',
                'platform': platform,
                'error': str(e),
                'job': job
            }
    
    def get_supported_platforms(self):
        """Get list of supported platforms with available handlers"""
        supported = []
        for platform, handler in self.handlers.items():
            if handler is not None:
                supported.append(platform)
        return supported
    
    def get_platform_stats(self):
        """Get statistics about available handlers"""
        stats = {
            'total_platforms': len(self.handlers),
            'available_handlers': len([h for h in self.handlers.values() if h is not None]),
            'platforms': {}
        }
        
        for platform, handler in self.handlers.items():
            stats['platforms'][platform] = {
                'available': handler is not None,
                'handler_class': handler.__class__.__name__ if handler else None
            }
        
        return stats

"""
Platform-specific ATS handlers
"""
from agents.handlers.base_handler import BaseATSHandler

try:
    from agents.handlers.linkedin_handler import LinkedInHandler
    LINKEDIN_AVAILABLE = True
except ImportError:
    LINKEDIN_AVAILABLE = False

try:
    from agents.handlers.workday_handler import WorkdayHandler
    WORKDAY_AVAILABLE = True
except ImportError:
    WORKDAY_AVAILABLE = False

try:
    from agents.handlers.greenhouse_handler import GreenhouseHandler
    GREENHOUSE_AVAILABLE = True
except ImportError:
    GREENHOUSE_AVAILABLE = False

try:
    from agents.handlers.lever_handler import LeverHandler
    LEVER_AVAILABLE = True
except ImportError:
    LEVER_AVAILABLE = False

try:
    from agents.handlers.indeed_handler import IndeedHandler
    INDEED_AVAILABLE = True
except ImportError:
    INDEED_AVAILABLE = False

__all__ = [
    'BaseATSHandler',
    'LinkedInHandler',
    'WorkdayHandler',
    'GreenhouseHandler',
    'LeverHandler',
    'IndeedHandler'
]

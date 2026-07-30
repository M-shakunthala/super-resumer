from agents.platform_detector import PlatformDetector
from agents.linkedin_apply import LinkedInApply
from agents.workday_apply import WorkdayApply
from agents.greenhouse_apply import GreenhouseApply


class ApplyEngine:

    def __init__(self):

        self.detector = PlatformDetector()

    def apply(
        self,
        job_url,
        resume
    ):

        platform = self.detector.detect(job_url)

        engines = {
            "linkedin": LinkedInApply(),
            "workday": WorkdayApply(),
            "greenhouse": GreenhouseApply()
        }

        engine = engines.get(platform)

        if engine:
            engine.apply(job_url, resume)

        else:
            print("Unsupported ATS")
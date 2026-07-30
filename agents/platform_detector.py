class PlatformDetector:
    def detect(self, url: str) -> str:
        url = (url or "").lower()
        if "linkedin.com" in url:
            return "linkedin"
        if "workday" in url or "myworkdayjobs" in url:
            return "workday"
        if "greenhouse" in url:
            return "greenhouse"
        if "lever.co" in url:
            return "lever"
        if "indeed." in url:
            return "indeed"
        if "naukri.com" in url:
            return "naukri"
        return "unknown"

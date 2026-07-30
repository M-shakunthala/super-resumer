class PlatformDetector:

    def detect(self, url):

        url = url.lower()

        if "linkedin.com" in url:
            return "linkedin"

        if "workday" in url:
            return "workday"

        if "greenhouse" in url:
            return "greenhouse"

        if "lever.co" in url:
            return "lever"

        if "indeed.com" in url:
            return "indeed"

        return "unknown"

from selenium.webdriver.common.by import By
from urllib.parse import quote

from infra.browser import BrowserManager


class JobScraper:

    def __init__(self):
        self.driver = (
            BrowserManager().get_driver()
        )

    def fetch_jobs(
        self,
        keyword,
        location="Bengaluru"
    ):

        driver = self.driver

        search_url = (
            "https://www.linkedin.com/jobs/search/"
            f"?keywords={quote(keyword)}"
            f"&location={quote(location)}"
        )

        driver.get(search_url)

        jobs = []

        cards = driver.find_elements(
            By.CSS_SELECTOR,
            ".job-card-container"
        )

        for card in cards:

            try:
                link = card.find_element(
                    By.TAG_NAME,
                    "a"
                )

                title = card.text

                jobs.append({
                    "title": title,
                    "url": link.get_attribute("href")
                })

            except:
                continue

        return jobs

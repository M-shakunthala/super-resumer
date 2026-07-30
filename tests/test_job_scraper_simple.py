"""
Test the simple job scraper with config system
"""
from agents.job_scraper import JobScraper
from core.config import Config


def test_job_scraper():
    # Load config
    config = Config.load()
    print("Loaded config:")
    print(config)
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Test with first keyword and location
    keyword = config['keywords'][0]
    location = config['locations'][0]
    
    print(f"\nTesting scraper with:")
    print(f"Keyword: {keyword}")
    print(f"Location: {location}")
    
    # Note: This will open a browser and navigate to LinkedIn
    # Uncomment to actually test:
    # jobs = scraper.fetch_jobs(keyword, location)
    # print(f"\nFound {len(jobs)} jobs")
    # for job in jobs[:3]:
    #     print(f"- {job['title'][:50]}...")
    
    # Clean up
    scraper.driver.close()
    print("\nTest completed (browser closed)")


if __name__ == "__main__":
    test_job_scraper()

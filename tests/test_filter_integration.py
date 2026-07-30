"""
Integration test: Scraper + Filter + Config
"""
from agents.job_scraper import JobScraper
from agents.job_filter import JobFilter
from core.config import Config


def test_integration():
    # Load configuration
    config = Config.load()
    
    # Initialize components
    scraper = JobScraper()
    filter = JobFilter()
    
    # Example profile skills (could be loaded from resume/config)
    profile_skills = ["python", "javascript", "sql", "django"]
    
    print("Job Search Configuration:")
    print(f"Keywords: {config['keywords']}")
    print(f"Locations: {config['locations']}")
    print(f"Experience Level: {config['experience_level']}")
    print(f"Easy Apply Only: {config['easy_apply_only']}")
    
    # Example: Simulate job scraping results
    # (In real usage, you would call scraper.fetch_jobs())
    mock_jobs = [
        {"title": "Senior Python Developer", "url": "https://linkedin.com/jobs/1"},
        {"title": "Python Developer", "url": "https://linkedin.com/jobs/2"},
        {"title": "Lead Software Engineer", "url": "https://linkedin.com/jobs/3"},
        {"title": "Junior Backend Developer", "url": "https://linkedin.com/jobs/4"},
        {"title": "Software Architect", "url": "https://linkedin.com/jobs/5"},
        {"title": "Associate Software Engineer", "url": "https://linkedin.com/jobs/6"},
    ]
    
    print(f"\nTotal jobs found: {len(mock_jobs)}")
    
    # Filter jobs based on experience level
    valid_jobs = []
    for job in mock_jobs:
        if filter.is_valid(job, profile_skills):
            valid_jobs.append(job)
    
    print(f"Valid jobs after filtering: {len(valid_jobs)}")
    
    # Show results
    print("\nFiltered Results:")
    print("=" * 50)
    for job in valid_jobs:
        print(f"✅ {job['title']}")
        print(f"   {job['url']}")
    
    # Clean up
    scraper.driver.close()
    
    print("\nIntegration test completed successfully!")


if __name__ == "__main__":
    test_integration()

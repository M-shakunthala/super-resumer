"""
Complete pipeline test: Scraper -> Filter -> Ranker
"""
from agents.job_ranker import JobRanker
from agents.job_filter import JobFilter
from core.config import Config


def test_full_pipeline():
    # Load configuration
    config = Config.load()
    
    # Initialize components
    filter = JobFilter()
    ranker = JobRanker()
    
    # Example profile skills
    profile_skills = ["python", "javascript", "sql", "django"]
    
    # Simulate scraped jobs with scores
    mock_jobs = [
        {"title": "Senior Python Developer", "url": "https://linkedin.com/jobs/1", "score": 0.92},
        {"title": "Python Developer", "url": "https://linkedin.com/jobs/2", "score": 0.85},
        {"title": "Lead Software Engineer", "url": "https://linkedin.com/jobs/3", "score": 0.88},
        {"title": "Junior Backend Developer", "url": "https://linkedin.com/jobs/4", "score": 0.72},
        {"title": "Software Architect", "url": "https://linkedin.com/jobs/5", "score": 0.95},
        {"title": "Associate Software Engineer", "url": "https://linkedin.com/jobs/6", "score": 0.78},
        {"title": "Backend Developer", "url": "https://linkedin.com/jobs/7", "score": 0.90},
    ]
    
    print("🚀 COMPLETE JOB SEARCH PIPELINE")
    print("=" * 50)
    
    print(f"\n📋 Configuration:")
    print(f"   Keywords: {config['keywords']}")
    print(f"   Locations: {config['locations']}")
    print(f"   Experience: {config['experience_level']}")
    
    print(f"\n🔍 STEP 1: Raw jobs from scraper")
    print(f"   Total jobs found: {len(mock_jobs)}")
    for job in mock_jobs:
        print(f"   - {job['title']} (score: {job['score']})")
    
    # Filter jobs
    valid_jobs = []
    for job in mock_jobs:
        if filter.is_valid(job, profile_skills):
            valid_jobs.append(job)
    
    print(f"\n✅ STEP 2: Filtered jobs (experience-appropriate)")
    print(f"   Valid jobs: {len(valid_jobs)}")
    filtered_count = len(mock_jobs) - len(valid_jobs)
    print(f"   Filtered out: {filtered_count} senior/lead roles")
    
    for job in valid_jobs:
        print(f"   - {job['title']} (score: {job['score']})")
    
    # Rank jobs
    ranked_jobs = ranker.rank(valid_jobs)
    
    print(f"\n🏆 STEP 3: Ranked jobs (best match first)")
    print(f"   Jobs to apply: {len(ranked_jobs)}")
    
    for i, job in enumerate(ranked_jobs, 1):
        print(f"   {i}. {job['title']}")
        print(f"      Score: {job['score']}")
        print(f"      URL: {job['url']}")
    
    print(f"\n🎯 Top recommendation: {ranked_jobs[0]['title']}")
    print(f"   Score: {ranked_jobs[0]['score']}")
    print(f"   This is your best match to apply first!")
    
    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    test_full_pipeline()

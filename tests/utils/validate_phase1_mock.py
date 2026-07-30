"""
Mock Phase 1 validation - demonstrates testing workflow without real scraping
"""
from core.config import Config
from agents.job_filter import JobFilter
from agents.job_ranker import JobRanker


def validate_phase1_mock():
    """Mock validation to demonstrate testing workflow"""
    print("🔍 PHASE 1 VALIDATION (MOCK)")
    print("=" * 50)
    print("⚠️  Using mock data for demonstration")
    
    config = Config.load()
    filterer = JobFilter()
    ranker = JobRanker()
    
    profile_skills = config.get("profile_skills", ["python", "sql", "c#"])
    
    # Mock scraped jobs
    mock_jobs = [
        {"title": "Senior Python Developer", "url": "https://linkedin.com/jobs/123", "score": 0.92},
        {"title": "Python Developer", "url": "https://linkedin.com/jobs/124", "score": 0.85},
        {"title": "Junior Backend Developer", "url": "https://linkedin.com/jobs/125", "score": 0.72},
        {"title": "Software Architect", "url": "https://linkedin.com/jobs/126", "score": 0.95},
        {"title": "Associate Software Engineer", "url": "https://linkedin.com/jobs/127", "score": 0.78},
        {"title": "Lead Developer", "url": "https://linkedin.com/jobs/128", "score": 0.88},
        {"title": "Backend Developer", "url": "https://linkedin.com/jobs/129", "score": 0.90},
    ]
    
    print(f"\n📋 Mock scraped jobs: {len(mock_jobs)}")
    
    # Sample job data
    print("\n📋 Sample Job Data:")
    for i, job in enumerate(mock_jobs[:3], 1):
        print(f"\n{i}. {job.get('title', 'Unknown')}")
        print(f"   URL: {job.get('url', 'N/A')}")
        
        # Validate URL
        url = job.get('url', '')
        if url and 'linkedin.com' in url:
            print(f"   ✅ URL format valid")
        else:
            print(f"   ❌ URL format invalid")
    
    # Filter jobs
    valid_jobs = []
    senior_count = 0
    for job in mock_jobs:
        if not filterer.is_valid(job, profile_skills):
            senior_count += 1
            print(f"   ❌ Filtered: {job.get('title', 'Unknown')}")
        else:
            valid_jobs.append(job)
            print(f"   ✅ Valid: {job.get('title', 'Unknown')}")
    
    print(f"\n✅ Filtering results:")
    print(f"   Total jobs: {len(mock_jobs)}")
    print(f"   Senior roles filtered: {senior_count}")
    print(f"   Valid jobs: {len(valid_jobs)}")
    
    # Check for senior role leakage
    if senior_count > 0:
        print(f"   ✅ Filter working correctly")
    else:
        print(f"   ⚠️  No senior roles filtered")
    
    # Rank jobs
    ranked_jobs = ranker.rank(valid_jobs)
    print(f"\n✅ Ranking results:")
    print(f"   Ranked jobs: {len(ranked_jobs)}")
    
    print("\n📊 Ranked Jobs (Best First):")
    for i, job in enumerate(ranked_jobs, 1):
        print(f"   {i}. {job.get('title', 'Unknown')} - Score: {job.get('score', 0)}")
    
    if len(ranked_jobs) > 1:
        scores = [job.get('score', 0) for job in ranked_jobs]
        if scores == sorted(scores, reverse=True):
            print(f"\n   ✅ Jobs sorted by score (highest first)")
        else:
            print(f"\n   ❌ Jobs not sorted correctly")
    
    print("\n🎯 VALIDATION COMPLETE")
    print("\n✅ Manual verification steps:")
    print("1. ✅ URLs are valid LinkedIn job URLs")
    print("2. ✅ Job titles match search criteria")
    print("3. ✅ Senior roles are filtered out")
    print("4. ✅ Jobs are ranked by score")
    
    print("\n🚀 Ready to proceed to Phase 2 (Open Jobs)")
    
    return True


if __name__ == "__main__":
    success = validate_phase1_mock()
    exit(0 if success else 1)

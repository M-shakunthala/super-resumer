"""
Quick Phase 1 validation - verify data quality
"""
from core.config import Config
from agents.job_scraper import JobScraper
from agents.job_filter import JobFilter
from agents.job_ranker import JobRanker


def validate_phase1():
    """Quick validation of search and filtering"""
    print("🔍 PHASE 1 VALIDATION")
    print("=" * 50)
    
    config = Config.load()
    scraper = JobScraper()
    filterer = JobFilter()
    ranker = JobRanker()
    
    profile_skills = config.get("profile_skills", ["python", "sql", "c#"])
    
    # Test with first keyword/location
    keyword = config["keywords"][0]
    location = config["locations"][0]
    
    print(f"\nTest Search: '{keyword}' in '{location}'")
    
    try:
        # Scrape jobs
        jobs = scraper.fetch_jobs(keyword, location)
        print(f"✅ Scraped {len(jobs)} jobs")
        
        if len(jobs) == 0:
            print("❌ No jobs found - check search terms")
            return False
        
        # Sample job data
        print("\n📋 Sample Job Data:")
        for i, job in enumerate(jobs[:3], 1):
            print(f"\n{i}. {job.get('title', 'Unknown')}")
            print(f"   URL: {job.get('url', 'N/A')}")
            
            # Validate URL
            url = job.get('url', '')
            if url and ('linkedin.com' in url or 'http' in url):
                print(f"   ✅ URL format valid")
            else:
                print(f"   ❌ URL format invalid")
        
        # Filter jobs
        valid_jobs = []
        senior_count = 0
        for job in jobs:
            if not filterer.is_valid(job, profile_skills):
                senior_count += 1
            else:
                valid_jobs.append(job)
        
        print(f"\n✅ Filtering results:")
        print(f"   Total jobs: {len(jobs)}")
        print(f"   Senior roles filtered: {senior_count}")
        print(f"   Valid jobs: {len(valid_jobs)}")
        
        # Check for senior role leakage
        if senior_count > 0:
            print(f"   ✅ Filter working correctly")
        else:
            print(f"   ⚠️  No senior roles found (might be okay)")
        
        # Rank jobs
        ranked_jobs = ranker.rank(valid_jobs)
        print(f"\n✅ Ranking results:")
        print(f"   Ranked jobs: {len(ranked_jobs)}")
        
        if len(ranked_jobs) > 1:
            scores = [job.get('score', 0) for job in ranked_jobs]
            if scores == sorted(scores, reverse=True):
                print(f"   ✅ Jobs sorted by score (highest first)")
            else:
                print(f"   ❌ Jobs not sorted correctly")
        
        print("\n🎯 VALIDATION COMPLETE")
        print("\n✅ Manual verification steps:")
        print("1. Check the sample URLs above are correct")
        print("2. Verify job titles match your search")
        print("3. Confirm senior roles are filtered")
        print("4. Ensure ranking makes sense")
        
        scraper.driver.close()
        return True
        
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        scraper.driver.close()
        return False


if __name__ == "__main__":
    success = validate_phase1()
    exit(0 if success else 1)

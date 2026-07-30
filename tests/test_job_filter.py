"""
Test the job filter system
"""
from agents.job_filter import JobFilter


def test_job_filter():
    filter = JobFilter()
    profile_skills = ["python", "javascript", "sql"]  # Example skills
    
    # Test jobs with different titles
    test_jobs = [
        {"title": "Senior Python Developer", "url": "http://example.com/1"},
        {"title": "Software Engineer", "url": "http://example.com/2"},
        {"title": "Lead Backend Developer", "url": "http://example.com/3"},
        {"title": "Junior Python Developer", "url": "http://example.com/4"},
        {"title": "Software Architect", "url": "http://example.com/5"},
        {"title": "Engineering Manager", "url": "http://example.com/6"},
        {"title": "Python Developer", "url": "http://example.com/7"},
        {"title": "Backend Developer", "url": "http://example.com/8"},
        {"title": "Principal Engineer", "url": "http://example.com/9"},
        {"title": "Associate Software Engineer", "url": "http://example.com/10"},
    ]
    
    print("Testing Job Filter")
    print("=" * 50)
    
    valid_jobs = []
    invalid_jobs = []
    
    for job in test_jobs:
        is_valid = filter.is_valid(job, profile_skills)
        
        if is_valid:
            valid_jobs.append(job)
            print(f"✅ VALID: {job['title']}")
        else:
            invalid_jobs.append(job)
            print(f"❌ INVALID: {job['title']}")
    
    print("\n" + "=" * 50)
    print(f"Total jobs: {len(test_jobs)}")
    print(f"Valid jobs: {len(valid_jobs)}")
    print(f"Invalid jobs: {len(invalid_jobs)}")
    
    print("\nValid jobs for application:")
    for job in valid_jobs:
        print(f"  - {job['title']}")
    
    print("\nFiltered out (senior/lead roles):")
    for job in invalid_jobs:
        print(f"  - {job['title']}")


if __name__ == "__main__":
    test_job_filter()

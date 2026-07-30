"""
Test the job ranking system
"""
from agents.job_ranker import JobRanker


def test_job_ranker():
    ranker = JobRanker()
    
    # Example jobs with different scores
    jobs = [
        {"title": "Python Developer", "url": "http://example.com/1", "score": 0.85},
        {"title": "Backend Developer", "url": "http://example.com/2", "score": 0.92},
        {"title": "Software Engineer", "url": "http://example.com/3", "score": 0.78},
        {"title": "Junior Developer", "url": "http://example.com/4", "score": 0.65},
        {"title": "Senior Developer", "url": "http://example.com/5", "score": 0.88},
        {"title": "Full Stack Developer", "url": "http://example.com/6", "score": 0.95},
    ]
    
    print("Original jobs (unsorted):")
    print("=" * 50)
    for job in jobs:
        print(f"{job['title']}: {job['score']}")
    
    # Rank jobs
    ranked_jobs = ranker.rank(jobs)
    
    print("\nRanked jobs (best first):")
    print("=" * 50)
    for i, job in enumerate(ranked_jobs, 1):
        print(f"{i}. {job['title']}: {job['score']}")
    
    # Verify sorting
    scores = [job['score'] for job in ranked_jobs]
    assert scores == sorted(scores, reverse=True), "Jobs not sorted correctly"
    
    print("\n✅ Ranking system working correctly!")
    print(f"Best job: {ranked_jobs[0]['title']} (score: {ranked_jobs[0]['score']})")
    print(f"Worst job: {ranked_jobs[-1]['title']} (score: {ranked_jobs[-1]['score']})")


if __name__ == "__main__":
    test_job_ranker()

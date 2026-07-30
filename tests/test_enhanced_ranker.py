"""
Test enhanced job ranker with config parameters
"""
from agents.job_ranker import JobRanker


def test_enhanced_ranker():
    ranker = JobRanker()
    
    print(f"Ranker Configuration:")
    print(f"  Min score threshold: {ranker.min_score}")
    print(f"  Max ranked jobs: {ranker.max_jobs}")
    
    # Example jobs with various scores
    jobs = [
        {"title": "Python Developer", "url": "http://example.com/1", "score": 0.92},
        {"title": "Backend Developer", "url": "http://example.com/2", "score": 0.85},
        {"title": "Software Engineer", "url": "http://example.com/3", "score": 0.45},  # Below threshold
        {"title": "Junior Developer", "url": "http://example.com/4", "score": 0.65},
        {"title": "Senior Developer", "url": "http://example.com/5", "score": 0.88},
        {"title": "Full Stack Developer", "url": "http://example.com/6", "score": 0.35},  # Below threshold
        {"title": "Data Engineer", "url": "http://example.com/7", "score": 0.78},
        {"title": "DevOps Engineer", "url": "http://example.com/8", "score": 0.82},
    ]
    
    print(f"\n📋 Original jobs: {len(jobs)}")
    for job in jobs:
        print(f"  - {job['title']}: {job['score']}")
    
    # Rank jobs
    ranked_jobs = ranker.rank(jobs)
    
    print(f"\n🏆 Ranked jobs (qualified and sorted): {len(ranked_jobs)}")
    for i, job in enumerate(ranked_jobs, 1):
        print(f"  {i}. {job['title']}: {job['score']}")
    
    # Verify filtering
    qualified_count = len([j for j in jobs if j.get('score', 0) >= ranker.min_score])
    print(f"\n✅ Qualified jobs (score >= {ranker.min_score}): {qualified_count}")
    print(f"✅ Filtered out (score < {ranker.min_score}): {len(jobs) - qualified_count}")
    
    # Verify sorting
    if len(ranked_jobs) > 1:
        scores = [job['score'] for job in ranked_jobs]
        assert scores == sorted(scores, reverse=True), "Jobs not sorted correctly"
        print("✅ Jobs sorted correctly by score")


if __name__ == "__main__":
    test_enhanced_ranker()

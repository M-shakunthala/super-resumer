"""
Simulation test of the smart runner workflow
"""
from core.config import Config
from agents.job_filter import JobFilter
from agents.job_ranker import JobRanker
from core.orchestrator import Orchestrator
from memory.job_memory import JobMemory


def simulate_smart_runner():
    config = Config.load()

    filterer = JobFilter()
    ranker = JobRanker()
    memory = JobMemory()
    bot = Orchestrator()

    profile_skills = config.get("profile_skills", ["python", "sql", "c#"])

    all_jobs = []

    print("🚀 SIMULATING intelligent job search automation...")
    print(f"Keywords: {config['keywords']}")
    print(f"Locations: {config['locations']}")
    print(f"Profile Skills: {profile_skills}")

    # Simulate scraped jobs for each keyword/location combination
    mock_job_data = [
        # Bengaluru jobs
        {"title": "Senior Python Developer", "url": "https://linkedin.com/jobs/1", "score": 0.92},
        {"title": "Python Developer", "url": "https://linkedin.com/jobs/2", "score": 0.85},
        {"title": "Junior Backend Developer", "url": "https://linkedin.com/jobs/3", "score": 0.72},
        {"title": "Software Architect", "url": "https://linkedin.com/jobs/4", "score": 0.95},
        {"title": "Associate Software Engineer", "url": "https://linkedin.com/jobs/5", "score": 0.78},
        # Remote jobs  
        {"title": "Backend Developer", "url": "https://linkedin.com/jobs/6", "score": 0.90},
        {"title": "Senior Software Engineer", "url": "https://linkedin.com/jobs/7", "score": 0.88},
        {"title": "Full Stack Developer", "url": "https://linkedin.com/jobs/8", "score": 0.82},
    ]

    for keyword in config["keywords"]:
        for location in config["locations"]:
            print(f"\n🔍 Searching: '{keyword}' in '{location}'")
            
            # Simulate scraper results
            jobs = mock_job_data.copy()
            print(f"   Found {len(jobs)} raw jobs")

            valid_jobs = []
            for job in jobs:
                if memory.exists(job["url"]):
                    print(f"   ⏭️  Skipping duplicate: {job.get('title', 'Unknown')}")
                    continue

                if not filterer.is_valid(job, profile_skills):
                    print(f"   ❌ Filtering senior role: {job.get('title', 'Unknown')}")
                    continue
                
                valid_jobs.append(job)

            print(f"   {len(valid_jobs)} valid jobs after filtering")

            # Rank jobs by score
            ranked_jobs = ranker.rank(valid_jobs)
            
            for job in ranked_jobs:
                print(f"   🤖 Processing: {job.get('title', 'Unknown')} (score: {job.get('score', 0)})")

                result = bot.process(job)

                if result:
                    all_jobs.append(result)
                    memory.save(job["url"], "applied")
                    print(f"   ✅ Applied successfully")
                else:
                    memory.save(job["url"], "failed")
                    print(f"   ❌ Application failed")

    print(f"\n🎯 Simulation complete!")
    print(f"Total jobs processed: {len(all_jobs)}")
    print(f"Successful applications: {len([j for j in all_jobs if j['status'] == 'applied'])}")
    print(f"Failed applications: {len([j for j in all_jobs if j['status'] == 'failed'])}")

    # Show memory stats
    stats = memory.get_stats() if hasattr(memory, 'get_stats') else {}
    if stats:
        print(f"\n📊 Memory stats: {stats}")

    memory.close()


if __name__ == "__main__":
    simulate_smart_runner()

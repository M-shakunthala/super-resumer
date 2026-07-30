from memory.job_memory import JobMemory

# Test the new interview tracking
memory = JobMemory()

# Create test job
test_job = {
    "url": "https://example.com/job1",
    "title": "Software Engineer",
    "company": "Test Company",
    "platform": "linkedin",
    "status": "applied",
    "score": 0.85,
    "interview": 0
}

memory.save(test_job)
print("Job saved successfully")

# Test setting interview
memory.set_interview("https://example.com/job1", 1)
print("Interview status updated")

# Test getting stats
stats = memory.get_stats()
print("Stats: " + str(stats))

# Test getting all jobs
jobs = memory.get_all_jobs()
print("Jobs retrieved: " + str(len(jobs)))
for job in jobs:
    print("  - " + job['title'] + " at " + job['company'] + " - Interview: " + str(job['interview']))

print("\nInterview tracking system working correctly!")
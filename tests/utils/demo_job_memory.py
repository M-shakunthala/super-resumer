#!/usr/bin/env python3
"""
Demo script for job memory system
Shows duplicate filtering and status management in action
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_agent.memory.job_memory import JobMemory, JobStatus, check_duplicate, record_application


def demo_basic_usage():
    """Demonstrate basic job memory usage"""
    print("=" * 50)
    print("Demo: Basic Job Memory Usage")
    print("=" * 50)
    
    # Use in-memory database for demo
    memory = JobMemory(":memory:")
    
    # Test 1: New job
    print("\n1. Checking new job:")
    should_skip, reason = memory.should_skip("https://linkedin.com/jobs/123")
    print(f"   Should skip: {should_skip}")
    print(f"   Reason: {reason}")
    
    # Test 2: Save job as applied
    print("\n2. Marking job as applied:")
    memory.mark_applied("https://linkedin.com/jobs/123")
    should_skip, reason = memory.should_skip("https://linkedin.com/jobs/123")
    print(f"   Should skip: {should_skip}")
    print(f"   Reason: {reason}")
    
    # Test 3: Failed job (first time)
    print("\n3. Marking job as failed (first attempt):")
    memory.mark_failed("https://linkedin.com/jobs/456")
    should_skip, reason = memory.should_skip("https://linkedin.com/jobs/456")
    print(f"   Should skip: {should_skip}")
    print(f"   Reason: {reason}")
    
    # Test 4: Failed job (after 3 retries)
    print("\n4. Marking job as failed (3 retries):")
    for i in range(3):
        memory.mark_failed("https://linkedin.com/jobs/789")
    
    should_skip, reason = memory.should_skip("https://linkedin.com/jobs/789")
    print(f"   Should skip: {should_skip}")
    print(f"   Reason: {reason}")


def demo_status_tracking():
    """Demonstrate status tracking"""
    print("\n" + "=" * 50)
    print("Demo: Status Tracking")
    print("=" * 50)
    
    memory = JobMemory(":memory:")
    
    # Add jobs with different statuses
    print("\n1. Adding jobs with different statuses:")
    memory.save("https://linkedin.com/jobs/1", JobStatus.NEW.value, "Google", "Engineer")
    memory.save("https://linkedin.com/jobs/2", JobStatus.APPLIED.value, "Facebook", "Developer")
    memory.save("https://linkedin.com/jobs/3", JobStatus.FAILED.value, "Amazon", "Manager")
    memory.save("https://linkedin.com/jobs/4", JobStatus.APPLIED.value, "Apple", "Designer")
    
    # Get statistics
    stats = memory.get_stats()
    print("\n2. Job Statistics:")
    print(f"   Total: {stats['total']}")
    print(f"   New: {stats[JobStatus.NEW.value]}")
    print(f"   Applied: {stats[JobStatus.APPLIED.value]}")
    print(f"   Failed: {stats[JobStatus.FAILED.value]}")
    
    # Get jobs by status
    print("\n3. Applied Jobs:")
    applied_jobs = memory.get_jobs_by_status(JobStatus.APPLIED.value)
    for job in applied_jobs:
        print(f"   - {job['company']}: {job['position']}")


def demo_retry_logic():
    """Demonstrate retry logic for failed jobs"""
    print("\n" + "=" * 50)
    print("Demo: Retry Logic")
    print("=" * 50)
    
    memory = JobMemory(":memory:")
    
    # Simulate failed applications
    print("\n1. Simulating failed applications:")
    job_url = "https://linkedin.com/jobs/999"
    
    for attempt in range(4):
        memory.mark_failed(job_url)
        job = memory.get_job(job_url)
        
        should_skip, reason = memory.should_skip(job_url)
        print(f"   Attempt {attempt + 1}: Retry count = {job['retry_count']}, Should skip = {should_skip}")
        print(f"   Reason: {reason}")
        print()
    
    # Get retryable jobs
    print("2. Getting retryable failed jobs:")
    retryable = memory.get_failed_jobs(max_retries=3)
    print(f"   Found {len(retryable)} retryable jobs")
    
    for job in retryable:
        print(f"   - {job['url']} (retries: {job['retry_count']})")


def demo_convenience_functions():
    """Demonstrate convenience functions"""
    print("\n" + "=" * 50)
    print("Demo: Convenience Functions")
    print("=" * 50)
    
    # Use temporary database
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
        db_path = tmp.name
    
    try:
        print("\n1. Using check_duplicate:")
        should_skip, reason = check_duplicate("https://linkedin.com/jobs/new", db_path)
        print(f"   New job - Should skip: {should_skip}, Reason: {reason}")
        
        print("\n2. Using record_application (success):")
        record_application("https://linkedin.com/jobs/new", True, db_path)
        should_skip, reason = check_duplicate("https://linkedin.com/jobs/new", db_path)
        print(f"   After success - Should skip: {should_skip}, Reason: {reason}")
        
        print("\n3. Using record_application (failure):")
        record_application("https://linkedin.com/jobs/failed", False, db_path)
        should_skip, reason = check_duplicate("https://linkedin.com/jobs/failed", db_path)
        print(f"   After failure - Should skip: {should_skip}, Reason: {reason}")
    
    finally:
        import os
        if os.path.exists(db_path):
            os.remove(db_path)


def demo_integration_scenario():
    """Demonstrate realistic integration scenario"""
    print("\n" + "=" * 50)
    print("Demo: Realistic Integration Scenario")
    print("=" * 50)
    
    memory = JobMemory(":memory:")
    
    # Simulate job list
    jobs = [
        {"url": "https://linkedin.com/jobs/1", "company": "Google", "position": "Engineer"},
        {"url": "https://linkedin.com/jobs/2", "company": "Facebook", "position": "Developer"},
        {"url": "https://linkedin.com/jobs/3", "company": "Amazon", "position": "Manager"},
    ]
    
    print("\n1. Processing job list:")
    results = {"processed": 0, "skipped": 0}
    
    for job in jobs:
        should_skip, reason = memory.should_skip(job['url'])
        
        if should_skip:
            print(f"   ⏭️  Skipping {job['company']}: {reason}")
            results["skipped"] += 1
            continue
        
        print(f"   🚀 Processing {job['company']} - {job['position']}")
        
        # Simulate application (random success/failure)
        import random
        success = random.choice([True, True, False])  # 2/3 success rate
        
        if success:
            memory.mark_applied(job['url'])
            print(f"   ✅ Applied successfully")
        else:
            memory.mark_failed(job['url'])
            print(f"   ❌ Application failed")
        
        results["processed"] += 1
    
    print(f"\n2. Results: {results}")
    
    # Show final stats
    stats = memory.get_stats()
    print(f"\n3. Final Database Statistics:")
    print(f"   Total: {stats['total']}")
    print(f"   Applied: {stats[JobStatus.APPLIED.value]}")
    print(f"   Failed: {stats[JobStatus.FAILED.value]}")


def main():
    """Run all demos"""
    print("🎯 Job Memory System Demo")
    print("=" * 50)
    
    demo_basic_usage()
    demo_status_tracking()
    demo_retry_logic()
    demo_convenience_functions()
    demo_integration_scenario()
    
    print("\n" + "=" * 50)
    print("✅ Demo Complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()

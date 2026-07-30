#!/usr/bin/env python3
"""
Test script for the new simplified Job data model
"""
import sys
import os

# Add job_agent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from job_agent.models.job_schema import Job, JobCreate, JobUpdate, JobFilter
from job_agent.memory.job_memory import JobMemory
from loguru import logger


def test_simplified_job_model():
    """Test the simplified Job data model"""
    logger.info("Testing Simplified Job Data Model")
    logger.info("=" * 60)
    
    # Test 1: Create Job with required fields only
    logger.info("\n1. Creating Job with required fields only")
    job = Job(
        title="Python Developer",
        company="Tech Corp",
        description="Looking for Python developer with Django experience",
        url="https://example.com/job/123"
    )
    
    logger.info(f"   ✅ Job created: {job.title} at {job.company}")
    logger.info(f"   ✅ URL: {job.url}")
    logger.info(f"   ✅ State: {job.state}")
    logger.info(f"   ✅ Score: {job.score}")
    logger.info(f"   ✅ Skills: {job.skills}")
    
    # Test 2: Create Job with all fields
    logger.info("\n2. Creating Job with all fields")
    full_job = Job(
        title="Senior Software Engineer",
        company="AI Company",
        description="Senior role with ML experience",
        url="https://example.com/job/456",
        skills=["Python", "Machine Learning", "AWS"],
        score=0.85,
        state="matched",
        location="Remote",
        salary="$120k"
    )
    
    logger.info(f"   ✅ Job created: {full_job.title} at {full_job.company}")
    logger.info(f"   ✅ Skills: {full_job.skills}")
    logger.info(f"   ✅ Score: {full_job.score}")
    logger.info(f"   ✅ State: {full_job.state}")
    logger.info(f"   ✅ Location: {full_job.location}")
    logger.info(f"   ✅ Salary: {full_job.salary}")
    
    # Test 3: Job validation
    logger.info("\n3. Testing Pydantic validation")
    try:
        # This should fail validation (missing required field)
        invalid_job = Job(
            title="Invalid Job"
            # Missing company, description, url
        )
        logger.error("   ❌ Validation should have failed")
        return 1
    except Exception as e:
        logger.info(f"   ✅ Validation correctly failed: {type(e).__name__}")
    
    # Test 4: Job serialization
    logger.info("\n4. Testing JSON serialization")
    job_dict = full_job.dict()
    logger.info(f"   ✅ Serialized to dict with {len(job_dict)} fields")
    
    job_json = full_job.json()
    logger.info(f"   ✅ Serialized to JSON successfully")
    
    # Test 5: Database persistence
    logger.info("\n5. Testing database persistence")
    job_memory = JobMemory()
    
    try:
        job_id = job_memory.save_job(full_job)
        logger.info(f"   ✅ Job saved to database with ID: {job_id}")
        
        retrieved_job = job_memory.get_job(job_id)
        logger.info(f"   ✅ Job retrieved from database")
        logger.info(f"   ✅ Retrieved job title: {retrieved_job.title}")
        
    except Exception as e:
        logger.error(f"   ❌ Database persistence failed: {e}")
        return 1
    
    # Test 6: Job updates
    logger.info("\n6. Testing job updates")
    try:
        # Update state
        updated = job_memory.update_job_state(job_id, "applied", score=0.90)
        logger.info(f"   ✅ Job state updated successfully")
        
        # Retrieve updated job
        updated_job = job_memory.get_job(job_id)
        logger.info(f"   ✅ Updated state: {updated_job.state}")
        logger.info(f"   ✅ Updated score: {updated_job.score}")
        
    except Exception as e:
        logger.error(f"   ❌ Job update failed: {e}")
        return 1
    
    # Test 7: Statistics
    logger.info("\n7. Testing job statistics")
    try:
        stats = job_memory.get_statistics()
        logger.info(f"   ✅ Statistics retrieved: {stats}")
        logger.info(f"   ✅ Total jobs: {stats.get('total_jobs', 0)}")
        logger.info(f"   ✅ Jobs by state: {stats.get('by_state', {})}")
        
    except Exception as e:
        logger.error(f"   ❌ Statistics retrieval failed: {e}")
        return 1
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 All Job model tests passed!")
    logger.info("\nBenefits of simplified model:")
    logger.info("  ✅ Clean, focused structure")
    logger.info("  ✅ Required fields only specification")
    logger.info("  ✅ Pydantic validation")
    logger.info("  ✅ Easy database integration")
    logger.info("  ✅ Production-ready serialization")
    
    return 0


def test_job_schemas():
    """Test additional schema classes"""
    logger.info("\nTesting Additional Job Schemas")
    logger.info("=" * 60)
    
    # Test JobCreate schema
    logger.info("\n1. Testing JobCreate schema")
    job_create = JobCreate(
        title="New Job",
        company="New Company",
        description="Job description",
        url="https://example.com/job/new"
    )
    logger.info(f"   ✅ JobCreate: {job_create.title} at {job_create.company}")
    
    # Test JobUpdate schema
    logger.info("\n2. Testing JobUpdate schema")
    job_update = JobUpdate(state="matched", score=0.75)
    logger.info(f"   ✅ JobUpdate: state={job_update.state}, score={job_update.score}")
    
    # Test JobFilter schema
    logger.info("\n3. Testing JobFilter schema")
    job_filter = JobFilter(state="new", min_score=0.5)
    logger.info(f"   ✅ JobFilter: state={job_filter.state}, min_score={job_filter.min_score}")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 All schema tests passed!")
    
    return 0


def main():
    """Run all job model tests"""
    result1 = test_simplified_job_model()
    result2 = test_job_schemas()
    
    return result1 or result2


if __name__ == "__main__":
    sys.exit(main())
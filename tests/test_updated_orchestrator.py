#!/usr/bin/env python3
"""
Test the updated AI-driven orchestrator
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from automation.orchestrator import JobOrchestrator
from loguru import logger


def test_orchestrator_basic():
    """Test the basic orchestrator functionality"""
    logger.info("Testing Updated AI-Driven Orchestrator")
    logger.info("=" * 60)
    
    try:
        # Initialize orchestrator
        orchestrator = JobOrchestrator()
        
        # Test job data
        test_job = {
            "role": "Senior Python Developer",
            "company": "Tech Corp",
            "description": "We are looking for a Senior Python Developer with experience in Django, PostgreSQL, and cloud services to build scalable web applications.",
            "job_url": "https://example.com/job/123"
        }
        
        logger.info(f"Processing test job: {test_job['role']}")
        
        # Process the job
        orchestrator.process_job(test_job)
        
        logger.info("\n✅ Orchestrator test completed")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Orchestrator test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


def test_threshold_filtering():
    """Test threshold filtering"""
    logger.info("Testing Threshold Filtering")
    logger.info("=" * 60)
    
    try:
        orchestrator = JobOrchestrator()
        
        # Test jobs with different quality levels
        test_jobs = [
            {
                "role": "Perfect Match Python Developer",
                "description": "Senior Python Developer with Django, PostgreSQL, AWS, and extensive cloud experience building scalable microservices."
            },
            {
                "role": "Low Match Java Developer", 
                "description": "Junior Java Developer with basic Spring Boot experience and limited database knowledge."
            },
            {
                "role": "Partial Match Software Engineer",
                "description": "Software Developer with some Python experience and general web development skills."
            }
        ]
        
        for job in test_jobs:
            logger.info(f"\nTesting: {job['role']}")
            orchestrator.process_job(job)
        
        logger.info("\n✅ Threshold filtering test completed")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Threshold filtering test failed: {e}")
        return 1


def test_with_profile_data():
    """Test with actual profile data"""
    logger.info("Testing with Profile Data Integration")
    logger.info("=" * 60)
    
    try:
        # Set some test profile data
        from automation.profile_memory import ProfileMemory
        
        ProfileMemory.save("skills", "Python, Django, PostgreSQL, AWS, Docker, React")
        ProfileMemory.save("experience", "5 years in software development")
        ProfileMemory.save("name", "Test Developer")
        ProfileMemory.save("projects", "Built several scalable web applications")
        
        logger.info("Profile data set for testing")
        
        # Test orchestrator with profile data
        orchestrator = JobOrchestrator()
        
        test_job = {
            "role": "Senior Python Developer",
            "description": "Looking for experienced Python developer with Django and PostgreSQL skills for building cloud applications."
        }
        
        logger.info(f"Processing job with profile integration: {test_job['role']}")
        orchestrator.process_job(test_job)
        
        logger.info("\n✅ Profile integration test completed")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Profile integration test failed: {e}")
        return 1


def main():
    """Run all orchestrator tests"""
    import sys
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        
        if test_type == "basic":
            return test_orchestrator_basic()
        elif test_type == "threshold":
            return test_threshold_filtering()
        elif test_type == "profile":
            return test_with_profile_data()
        else:
            logger.error(f"Unknown test type: {test_type}")
            return 1
    else:
        # Run basic test
        return test_orchestrator_basic()


if __name__ == "__main__":
    sys.exit(main())
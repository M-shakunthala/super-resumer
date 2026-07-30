#!/usr/bin/env python3
"""
Test script for the new Job Agent architecture
"""
import sys
import os

# Add job_agent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from job_agent.core.config import config
from job_agent.memory.job_memory import JobMemory
from job_agent.memory.profile_memory import ProfileMemory
from job_agent.core.orchestrator import JobOrchestrator
from job_agent.models.job_schema import JobSchema, JobSource, JobStatus
from loguru import logger


def test_new_architecture():
    """Test the new architecture components"""
    logger.info("Testing New Job Agent Architecture")
    logger.info("=" * 60)
    
    try:
        # Test 1: Configuration
        logger.info("1. Testing configuration...")
        logger.info(f"   Base dir: {config.BASE_DIR}")
        logger.info(f"   Database path: {config.DATABASE_PATH}")
        logger.info(f"   Match threshold: {config.MATCH_THRESHOLD}")
        logger.info("   ✅ Configuration loaded successfully")
        
        # Test 2: Profile Memory
        logger.info("2. Testing profile memory...")
        profile_memory = ProfileMemory()
        profile_memory.save("test_name", "Test User")
        profile_memory.save("test_skills", "Python, Django, AWS")
        assert profile_memory.get("test_name") == "Test User"
        logger.info("   ✅ Profile memory working")
        
        # Test 3: Job Memory
        logger.info("3. Testing job memory...")
        job_memory = JobMemory()
        stats = job_memory.get_statistics()
        logger.info(f"   Statistics: {stats}")
        logger.info("   ✅ Job memory working")
        
        # Test 4: Job Schema
        logger.info("4. Testing job schema...")
        test_job = JobSchema(
            title="Python Developer",
            company="Tech Corp",
            description="Looking for Python developer with Django experience",
            job_url="https://example.com/job/123",
            source=JobSource.LINKEDIN
        )
        logger.info(f"   Created job: {test_job.title} at {test_job.company}")
        logger.info("   ✅ Job schema working")
        
        # Test 5: Save and retrieve job
        logger.info("5. Testing job persistence...")
        job_id = job_memory.save_job(test_job)
        retrieved_job = job_memory.get_job(job_id)
        assert retrieved_job.title == test_job.title
        logger.info(f"   ✅ Job persistence working (ID: {job_id})")
        
        # Test 6: Orchestrator
        logger.info("6. Testing orchestrator...")
        orchestrator = JobOrchestrator()
        logger.info(f"   Match threshold: {orchestrator.match_threshold}")
        logger.info("   ✅ Orchestrator initialized")
        
        # Test 7: AI Engine
        logger.info("7. Testing AI engine...")
        from job_agent.agents.ai_engine import AIEngine
        ai_engine = AIEngine()
        logger.info("   ✅ AI engine initialized")
        
        # Test 8: Matcher
        logger.info("8. Testing matcher...")
        from job_agent.agents.matcher import JobMatcher
        matcher = JobMatcher()
        logger.info("   ✅ Matcher initialized")
        
        # Test 9: State Machine
        logger.info("9. Testing state machine...")
        from job_agent.core.state_machine import JobStateMachine, JobState, JobContext
        state_machine = JobStateMachine()
        context = JobContext(
            job_data={"title": "Test"},
            current_state=JobState.DISCOVERED
        )
        new_context = state_machine.transition(context, JobState.PARSED)
        assert new_context.current_state == JobState.PARSED
        logger.info("   ✅ State machine working")
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 All architecture tests passed!")
        logger.info("New Job Agent architecture is working correctly")
        
        return 0
        
    except Exception as e:
        logger.error(f"Architecture test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


if __name__ == "__main__":
    sys.exit(test_new_architecture())
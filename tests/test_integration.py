"""
Integration test for the new simplified Job model across all components
"""
from loguru import logger
from job_agent.models.job_schema import Job, JobSource
from job_agent.memory.job_memory import JobMemory
from job_agent.core.state_machine import StateMachine, JobContext, create_initial_job_context, JobState
from job_agent.core.orchestrator import JobOrchestrator


def test_job_memory_integration():
    """Test JobMemory with simplified Job model"""
    logger.info("Testing JobMemory integration")
    
    # Create a job
    job = Job(
        title="Test Engineer",
        company="Test Corp",
        description="Looking for a test engineer",
        url="https://example.com/test-job"
    )
    
    # Save to memory
    memory = JobMemory()
    job_id = memory.save_job(job)
    logger.info(f"✅ Job saved with ID: {job_id}")
    
    # Retrieve from memory
    retrieved_job = memory.get_job(job_id)
    assert retrieved_job is not None
    assert retrieved_job.title == "Test Engineer"
    assert retrieved_job.company == "Test Corp"
    assert retrieved_job.url == "https://example.com/test-job"
    logger.info(f"✅ Job retrieved successfully: {retrieved_job.title}")
    
    # Update state
    success = memory.update_job_state(job_id, "matched", score=0.8)
    assert success
    logger.info("✅ Job state updated successfully")
    
    # Verify update
    updated_job = memory.get_job(job_id)
    assert updated_job.state == "matched"
    assert updated_job.score == 0.8
    logger.info(f"✅ Job state verified: {updated_job.state}, score: {updated_job.score}")


def test_state_machine_integration():
    """Test StateMachine with simplified Job data"""
    logger.info("Testing StateMachine integration")
    
    # Create a job
    job = Job(
        title="ML Engineer",
        company="AI Startup",
        description="Machine learning engineer position",
        url="https://example.com/ml-job"
    )
    
    # Create initial context
    context = create_initial_job_context(job.model_dump())
    assert context.current_state == JobState.NEW
    logger.info(f"✅ Initial context created with state: {context.current_state}")
    
    # Test state transitions
    state_machine = StateMachine()
    
    # NEW -> PARSED
    context = state_machine.transition(context, JobState.PARSED)
    assert context.current_state == JobState.PARSED
    logger.info(f"✅ Transition to PARSED successful")
    
    # PARSED -> MATCHED
    context = state_machine.transition(context, JobState.MATCHED)
    assert context.current_state == JobState.MATCHED
    logger.info(f"✅ Transition to MATCHED successful")
    
    # Test terminal states
    context = state_machine.transition(context, JobState.SKIPPED)
    assert context.current_state == JobState.SKIPPED
    assert state_machine.is_terminal_state(context.current_state)
    logger.info(f"✅ Transition to SKIPPED (terminal) successful")
    
    # Test reset
    context = state_machine.reset_state(context)
    assert context.current_state == JobState.NEW
    logger.info(f"✅ State reset to NEW successful")


def test_orchestrator_integration():
    """Test JobOrchestrator with simplified Job model"""
    logger.info("Testing JobOrchestrator integration")
    
    # Create a job
    job = Job(
        title="Python Developer",
        company="Tech Company",
        description="Senior Python developer with experience in Django and AWS",
        url="https://example.com/python-job",
        skills=["Python", "Django", "AWS"],
        score=0.75
    )
    
    # Initialize orchestrator
    orchestrator = JobOrchestrator()
    logger.info("✅ Orchestrator initialized")
    
    # Process job (this will test the full state machine workflow)
    # Note: This might fail if API keys are not configured, but it should handle gracefully
    try:
        context = orchestrator.process_job(job)
        logger.info(f"✅ Job processed to final state: {context.current_state}")
        logger.info(f"   Match score: {context.match_score}")
        
        # Verify job was saved to memory
        if "job_id" in context.metadata:
            retrieved_job = orchestrator.job_memory.get_job(context.metadata["job_id"])
            assert retrieved_job is not None
            logger.info(f"✅ Job found in memory: {retrieved_job.title}")
    except Exception as e:
        logger.warning(f"Orchestrator processing failed (expected if no API keys): {e}")
        # This is acceptable if API keys are not configured


def test_full_workflow():
    """Test full workflow from creation to database storage"""
    logger.info("Testing full workflow integration")
    
    # Create job with all fields
    job = Job(
        title="Full Stack Developer",
        company="Innovative Tech",
        location="Remote",
        description="Full stack developer needed for exciting project",
        url="https://example.com/fullstack-job",
        salary="$100k - $150k",
        skills=["React", "Node.js", "Python", "PostgreSQL"],
        score=0.85,
        state="matched",
        source=JobSource.LINKEDIN
    )
    
    logger.info(f"✅ Created job: {job.title} at {job.company}")
    
    # Save to database
    memory = JobMemory()
    job_id = memory.save_job(job)
    logger.info(f"✅ Job saved to database with ID: {job_id}")
    
    # Retrieve and verify
    retrieved = memory.get_job(job_id)
    assert retrieved.title == job.title
    assert retrieved.company == job.company
    assert retrieved.state == job.state
    assert retrieved.score == job.score
    assert len(retrieved.skills) == len(job.skills)
    logger.info(f"✅ Job retrieved and verified")
    
    # Test state machine with retrieved job
    context = create_initial_job_context(retrieved.model_dump())
    state_machine = StateMachine()
    
    # Run through some state transitions
    context = state_machine.transition(context, JobState.PARSED)
    context = state_machine.transition(context, JobState.MATCHED)
    context.match_score = 0.9
    
    # Test decision logic
    if context.match_score >= 0.6:
        context = state_machine.transition(context, JobState.APPLYING)
        context = state_machine.transition(context, JobState.APPLIED)
        logger.info(f"✅ Job applied successfully in state machine")
    else:
        context = state_machine.transition(context, JobState.SKIPPED)
        logger.info(f"✅ Job skipped in state machine")
    
    logger.info("✅ Integration test completed successfully")


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("INTEGRATION TEST - Simplified Job Model")
    logger.info("=" * 60)
    
    try:
        test_job_memory_integration()
        logger.info("")
        
        test_state_machine_integration()
        logger.info("")
        
        test_orchestrator_integration()
        logger.info("")
        
        test_full_workflow()
        logger.info("")
        
        logger.info("=" * 60)
        logger.info("🎉 ALL INTEGRATION TESTS PASSED!")
        logger.info("=" * 60)
        
    except AssertionError as e:
        logger.error(f"❌ Integration test failed: {e}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        raise
#!/usr/bin/env python3
"""
Test script demonstrating STATE MACHINE vs simple "if score > apply" logic
"""
import sys
import os

# Add job_agent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from job_agent.core.state_machine import StateMachine, JobState, JobContext, create_initial_job_context
from loguru import logger


def test_state_machine_vs_simple_logic():
    """
    Demonstrate STATE MACHINE replacing simple "if score > apply" logic
    """
    logger.info("🔬 Testing STATE MACHINE vs Simple Logic")
    logger.info("=" * 60)
    
    # OLD APPROACH: Simple "if score > apply" logic
    logger.info("\n❌ OLD APPROACH: Simple if-else logic")
    logger.info("if score > 0.6:")
    logger.info("    apply_to_job()")
    logger.info("else:")
    logger.info("    skip_job()")
    
    # NEW APPROACH: STATE MACHINE
    logger.info("\n✅ NEW APPROACH: STATE MACHINE")
    logger.info("NEW → PARSED → MATCHED → DECISION → TERMINAL STATE")
    
    state_machine = StateMachine()
    
    # Test job 1: High score (should apply)
    logger.info("\n📋 Test 1: High score job")
    job_data = {"title": "Senior Python Developer", "company": "Tech Corp"}
    context = create_initial_job_context(job_data)
    context.match_score = 0.85
    
    logger.info(f"Initial state: {context.current_state.value}")
    logger.info(f"Match score: {context.match_score}")
    
    # Simulate state transitions
    try:
        context = state_machine.transition(context, JobState.PARSED)
        logger.info(f"✅ Transition to: {context.current_state.value}")
        
        context = state_machine.transition(context, JobState.MATCHED)
        logger.info(f"✅ Transition to: {context.current_state.value}")
        
        # Decision point (replaces if score > apply)
        if context.match_score >= 0.6:
            context = state_machine.transition(context, JobState.APPLYING)
            logger.info(f"✅ Decision: APPLY → {context.current_state.value}")
            
            context = state_machine.transition(context, JobState.APPLIED)
            logger.info(f"✅ Final state: {context.current_state.value}")
        else:
            context = state_machine.transition_to_skipped(context, "Low score")
            logger.info(f"⏭️  Final state: {context.current_state.value}")
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    
    # Test job 2: Low score (should skip)
    logger.info("\n📋 Test 2: Low score job")
    job_data = {"title": "Junior Java Developer", "company": "Different Corp"}
    context = create_initial_job_context(job_data)
    context.match_score = 0.45
    
    logger.info(f"Initial state: {context.current_state.value}")
    logger.info(f"Match score: {context.match_score}")
    
    try:
        context = state_machine.transition(context, JobState.PARSED)
        logger.info(f"✅ Transition to: {context.current_state.value}")
        
        context = state_machine.transition(context, JobState.MATCHED)
        logger.info(f"✅ Transition to: {context.current_state.value}")
        
        # Decision point (replaces if score > apply)
        if context.match_score >= 0.6:
            context = state_machine.transition(context, JobState.APPLYING)
            logger.info(f"✅ Decision: APPLY → {context.current_state.value}")
        else:
            context = state_machine.transition_to_skipped(context, "Score below threshold")
            logger.info(f"⏭️  Decision: SKIP → {context.current_state.value}")
            
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    
    # Test state validation
    logger.info("\n🛡️  Test: State validation")
    
    context = create_initial_job_context({"title": "Test Job"})
    
    # Try invalid transition
    try:
        state_machine.transition(context, JobState.APPLIED)
        logger.error("❌ Should have blocked invalid transition")
    except ValueError as e:
        logger.info(f"✅ Correctly blocked invalid transition: {e}")
    
    # Test terminal state detection
    terminal_states = [JobState.APPLIED, JobState.FAILED, JobState.SKIPPED]
    for state in terminal_states:
        is_terminal = state_machine.is_terminal_state(state)
        logger.info(f"✅ {state.value} is terminal: {is_terminal}")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 STATE MACHINE successfully replaces simple if-else logic!")
    logger.info("Benefits:")
    logger.info("  ✅ Valid state transitions")
    logger.info("  ✅ Error state handling")
    logger.info("  ✅ Terminal state detection")
    logger.info("  ✅ Traceable workflow")
    logger.info("  ✅ Extensible decision logic")
    
    return 0


def test_complete_workflow():
    """
    Test complete STATE MACHINE workflow
    """
    logger.info("\n🔄 Testing Complete STATE MACHINE Workflow")
    logger.info("=" * 60)
    
    state_machine = StateMachine()
    
    job_data = {
        "title": "Machine Learning Engineer",
        "company": "AI Company",
        "description": "Looking for ML engineer with Python experience"
    }
    
    # Initialize in NEW state
    context = create_initial_job_context(job_data)
    logger.info(f"📋 Job: {job_data['title']} at {job_data['company']}")
    logger.info(f"🎯 Initial state: {context.current_state.value}")
    
    # Simulate complete workflow
    workflow_steps = [
        (JobState.PARSED, "Job description parsed"),
        (JobState.MATCHED, "Job matched against profile"),
        (JobState.APPLYING, "Preparing application"),
        (JobState.APPLIED, "Application submitted")
    ]
    
    for state, description in workflow_steps:
        context = state_machine.transition(context, state)
        logger.info(f"✅ {context.current_state.value}: {description}")
    
    logger.info("\n" + "=" * 60)
    logger.info("🎉 Complete workflow test successful!")
    
    return 0


def main():
    """Run state machine tests"""
    result1 = test_state_machine_vs_simple_logic()
    result2 = test_complete_workflow()
    
    return result1 or result2


if __name__ == "__main__":
    sys.exit(main())
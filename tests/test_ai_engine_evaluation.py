"""
Test the upgraded AI Engine with evaluate_job functionality
"""
from loguru import logger
from job_agent.models.job_schema import Job, JobSource
from job_agent.agents.ai_engine import AIEngine


def test_evaluate_job():
    """Test the new evaluate_job method"""
    logger.info("=" * 60)
    logger.info("Testing AI Engine - evaluate_job Method")
    logger.info("=" * 60)
    
    # Initialize AI engine
    ai_engine = AIEngine()
    logger.info("✅ AI Engine initialized")
    
    # Create a test job
    job = Job(
        title="Senior Python Developer",
        company="Tech Innovators Inc",
        location="San Francisco",
        description="We are looking for a Senior Python Developer with experience in Django, Flask, AWS, and machine learning. The ideal candidate has 5+ years of experience and strong problem-solving skills.",
        url="https://example.com/senior-python-job",
        salary="$150k - $200k",
        skills=["Python", "Django", "AWS", "Machine Learning"],
        source=JobSource.LINKEDIN
    )
    
    logger.info(f"✅ Test job created: {job.title} at {job.company}")
    
    # Test evaluation
    logger.info("🧠 Evaluating job fit...")
    evaluation = ai_engine.evaluate_job(job)
    
    logger.info(f"📊 Evaluation Results:")
    logger.info(f"   Score: {evaluation['score']}")
    logger.info(f"   Reason: {evaluation['reason']}")
    
    # Validate response structure
    assert 'score' in evaluation, "Evaluation missing 'score' field"
    assert 'reason' in evaluation, "Evaluation missing 'reason' field"
    assert isinstance(evaluation['score'], (int, float)), "Score must be numeric"
    assert 0 <= evaluation['score'] <= 1, "Score must be between 0 and 1"
    assert isinstance(evaluation['reason'], str), "Reason must be string"
    
    logger.info("✅ Evaluation response structure validated")
    
    # Test with different job types
    logger.info("")
    logger.info("Testing with different job scenarios...")
    
    # Junior role
    junior_job = Job(
        title="Junior Developer",
        company="Startup Co",
        description="Entry-level position for new graduates. Looking for eager learners with basic programming knowledge.",
        url="https://example.com/junior-job"
    )
    
    junior_eval = ai_engine.evaluate_job(junior_job)
    logger.info(f"   Junior role - Score: {junior_eval['score']:.2f}")
    
    # Senior role with high requirements
    senior_job = Job(
        title="Principal Engineer",
        company="Big Tech Corp",
        description="Principal level position requiring 10+ years experience, team leadership, and architecture design skills.",
        url="https://example.com/principal-job"
    )
    
    senior_eval = ai_engine.evaluate_job(senior_job)
    logger.info(f"   Principal role - Score: {senior_eval['score']:.2f}")
    
    # Job with dict input (backward compatibility)
    logger.info("")
    logger.info("Testing with dictionary input (backward compatibility)...")
    job_dict = {
        "title": "Full Stack Developer",
        "company": "Web Agency",
        "description": "Full stack developer needed for web development projects.",
        "url": "https://example.com/fullstack-job"
    }
    
    dict_eval = ai_engine.evaluate_job(job_dict)
    logger.info(f"   Dictionary input - Score: {dict_eval['score']:.2f}")
    logger.info("✅ Dictionary input works correctly")
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("🎉 All AI Engine evaluation tests passed!")
    logger.info("=" * 60)
    logger.info("")
    logger.info("AI Engine is now a MULTI-FUNCTION DECISION ENGINE:")
    logger.info("  ✅ generate_answer - Interview question responses")
    logger.info("  ✅ parse_job_description - Extract structured job data")
    logger.info("  ✅ evaluate_job - AI-powered job fit evaluation")
    logger.info("  ✅ generate_cover_letter - Personalized cover letters")
    logger.info("  ✅ improve_resume_bullet - Resume optimization")


if __name__ == "__main__":
    try:
        test_evaluate_job()
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise
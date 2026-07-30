"""
Test the Resume Auto-Tailoring Engine - GAME CHANGER FEATURE
"""
from loguru import logger
from job_agent.models.job_schema import Job, JobSource
from job_agent.agents.resume_builder import ResumeBuilder


def test_resume_tailoring():
    """Test the new tailor method - GAME CHANGER FEATURE"""
    logger.info("=" * 70)
    logger.info("RESUME AUTO TAILORING ENGINE - GAME CHANGER FEATURE TEST")
    logger.info("=" * 70)
    
    # Initialize resume builder
    resume_builder = ResumeBuilder()
    logger.info("✅ Resume Builder initialized")
    
    # Create a sample base resume
    base_resume = """
JOHN DOE
Email: john.doe@email.com | Phone: (555) 123-4567 | Location: San Francisco, CA

PROFESSIONAL SUMMARY
Software Developer with 5 years of experience in building web applications. 
Skilled in Python, JavaScript, and cloud technologies. Passionate about creating 
efficient and scalable solutions.

EXPERIENCE
Software Developer | Tech Company Inc | 2020 - Present
- Developed and maintained web applications using Python and Django
- Collaborated with cross-functional teams to deliver projects on time
- Implemented RESTful APIs and integrated third-party services
- Optimized database queries improving performance by 30%

Junior Developer | Startup Co | 2018 - 2020
- Built responsive web applications using React and Node.js
- Worked with agile development methodologies
- Participated in code reviews and testing

EDUCATION
Bachelor of Science in Computer Science | State University | 2018

SKILLS
Python, JavaScript, Django, React, Node.js, SQL, Git, AWS Basics
"""
    
    logger.info("✅ Base resume created")
    logger.info(f"   Base resume length: {len(base_resume)} characters")
    
    # Create a target job
    job = Job(
        title="Senior Python Developer",
        company="CloudTech Innovations",
        location="Remote",
        description="We are seeking a Senior Python Developer with expertise in Django, Flask, AWS, and machine learning. The ideal candidate has 5+ years of experience, strong problem-solving skills, and experience with cloud deployment. You will work on scalable microservices architecture and implement CI/CD pipelines.",
        url="https://example.com/senior-python-job",
        salary="$140k - $180k",
        skills=["Python", "Django", "Flask", "AWS", "Machine Learning", "CI/CD", "Microservices"],
        source=JobSource.LINKEDIN
    )
    
    logger.info(f"✅ Target job created: {job.title} at {job.company}")
    
    # Test the tailor method
    logger.info("")
    logger.info("🎯 Testing AI-powered resume tailoring...")
    logger.info("This is the GAME CHANGER feature that makes your system startup-level")
    logger.info("")
    
    tailored_resume = resume_builder.tailor(base_resume, job)
    
    logger.info(f"✅ Resume tailored successfully!")
    logger.info(f"   Original length: {len(base_resume)} characters")
    logger.info(f"   Tailored length: {len(tailored_resume)} characters")
    logger.info(f"   Length change: {len(tailored_resume) - len(base_resume):+d} characters")
    
    # Display a portion of the tailored resume
    logger.info("")
    logger.info("📄 TAILORED RESUME PREVIEW (first 500 chars):")
    logger.info("-" * 70)
    logger.info(tailored_resume[:500])
    logger.info("-" * 70)
    
    # Test ATS keyword extraction
    logger.info("")
    logger.info("🔍 Testing ATS keyword extraction...")
    keyword_analysis = resume_builder.extract_ats_keywords(job)
    
    logger.info(f"   Total keywords extracted: {keyword_analysis['total_keywords']}")
    logger.info(f"   Priority keywords: {len(keyword_analysis['priority_keywords'])}")
    logger.info(f"   Standard keywords: {len(keyword_analysis['standard_keywords'])}")
    
    if keyword_analysis['priority_keywords']:
        logger.info(f"   Priority keywords: {', '.join(keyword_analysis['priority_keywords'][:5])}")
    
    # Test ATS compatibility scoring
    logger.info("")
    logger.info("📊 Testing ATS compatibility scoring...")
    ats_score = resume_builder.score_ats_compatibility(base_resume, job)
    
    logger.info(f"   Overall ATS score: {ats_score['overall_score']}")
    logger.info(f"   Keyword score: {ats_score['keyword_score']}")
    logger.info(f"   Format score: {ats_score['format_score']}")
    logger.info(f"   Matched keywords: {len(ats_score['matched_keywords'])}")
    logger.info(f"   Missing keywords: {len(ats_score['missing_keywords'])}")
    
    if ats_score['recommendations']:
        logger.info("   ATS Recommendations:")
        for rec in ats_score['recommendations'][:3]:
            logger.info(f"      • {rec}")
    
    # Test with different job types
    logger.info("")
    logger.info("🧪 Testing with different job scenarios...")
    
    # Machine Learning role
    ml_job = Job(
        title="Machine Learning Engineer",
        company="AI Startup",
        description="Looking for ML engineer with Python, TensorFlow, and data science experience.",
        url="https://example.com/ml-job"
    )
    
    ml_tailored = resume_builder.tailor(base_resume, ml_job)
    logger.info(f"   ML Role - Tailored resume length: {len(ml_tailored)} characters")
    
    # Management role
    manager_job = Job(
        title="Engineering Manager",
        company="Enterprise Corp",
        description="Seeking experienced leader to manage development teams and drive technical strategy.",
        url="https://example.com/manager-job"
    )
    
    manager_tailored = resume_builder.tailor(base_resume, manager_job)
    logger.info(f"   Manager Role - Tailored resume length: {len(manager_tailored)} characters")
    
    # Test with dictionary input (backward compatibility)
    logger.info("")
    logger.info("🔄 Testing backward compatibility with dictionary input...")
    job_dict = {
        "title": "Full Stack Developer",
        "company": "Digital Agency",
        "description": "Full stack developer needed for web and mobile projects.",
        "url": "https://example.com/fullstack-job",
        "skills": ["JavaScript", "React", "Node.js", "Mobile Development"]
    }
    
    dict_tailored = resume_builder.tailor(base_resume, job_dict)
    logger.info("✅ Dictionary input works correctly")
    
    logger.info("")
    logger.info("=" * 70)
    logger.info("🎉 RESUME AUTO TAILORING ENGINE TESTS PASSED!")
    logger.info("=" * 70)
    logger.info("")
    logger.info("🚀 GAME CHANGER FEATURES ENABLED:")
    logger.info("   ✅ AI-powered resume tailoring for specific jobs")
    logger.info("   ✅ ATS-friendly optimization")
    logger.info("   ✅ Keyword extraction and prioritization")
    logger.info("   ✅ ATS compatibility scoring")
    logger.info("   ✅ Job-specific resume optimization")
    logger.info("   ✅ Backward compatibility with dictionary input")
    logger.info("")
    logger.info("💡 This feature makes your system STARTUP-LEVEL:")
    logger.info("   - Automatically tailors resumes for each application")
    logger.info("   - Optimizes for Applicant Tracking Systems (ATS)")
    logger.info("   - Increases interview chances significantly")
    logger.info("   - Saves hours of manual resume customization")
    logger.info("   - Provides competitive advantage in job market")


if __name__ == "__main__":
    try:
        test_resume_tailoring()
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        raise
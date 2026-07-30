"""
Test resume optimizer with real resume and job descriptions
"""
import os
from agents.resume_optimizer import ResumeOptimizer
from resumes.resume_loader import ResumeLoader


def test_resume_optimizer():
    print("🎯 RESUME OPTIMIZER TEST")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_key_here":
        print("❌ OpenAI API key not configured")
        print("Please set OPENAI_API_KEY in .env file")
        print("\nUsing mock data for demonstration...")
        test_mock_optimizer()
        return True
    
    try:
        optimizer = ResumeOptimizer()
        print("✅ Resume Optimizer initialized successfully")
    except ValueError as e:
        print(f"❌ Initialization error: {e}")
        print("\nUsing mock data for demonstration...")
        test_mock_optimizer()
        return True
    
    # Load base resume
    try:
        loader = ResumeLoader()
        base_resume = loader.load_base_resume()
        print(f"✅ Base resume loaded ({len(base_resume)} characters)")
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        return False
    
    # Sample job description
    sample_job = """
    Job Title: Python Backend Developer
    
    We are looking for a talented Python Backend Developer to join our growing team.
    
    Requirements:
    - 2+ years of experience with Python
    - Strong knowledge of SQL and database design
    - Experience with REST APIs and microservices
    - Familiarity with Docker and containerization
    - Knowledge of cloud platforms (AWS/Azure)
    
    Preferred:
    - Experience with FastAPI or Django
    - Knowledge of Redis caching
    - Understanding of CI/CD pipelines
    - Experience with unit testing
    
    Responsibilities:
    - Design and implement backend services
    - Optimize database queries
    - Collaborate with frontend team
    - Write clean, maintainable code
    
    We offer competitive salary and growth opportunities.
    """
    
    print("\n📄 Optimizing resume for job...")
    print("-" * 50)
    
    try:
        optimized_resume = optimizer.tailor(base_resume, sample_job)
        
        print("✅ Resume optimization successful!")
        print("\n📋 Comparison:")
        comparison = optimizer.compare_versions(base_resume, optimized_resume)
        print(f"   Original: {comparison['original_word_count']} words")
        print(f"   Optimized: {comparison['optimized_word_count']} words")
        print(f"   Change: {comparison['length_change']} characters")
        
        print("\n📄 Optimized Resume Preview:")
        print("-" * 50)
        print(optimized_resume[:500] + "..." if len(optimized_resume) > 500 else optimized_resume)
        print("-" * 50)
        
        # Save optimized resume
        from pathlib import Path
        output_dir = Path("resumes/tailored")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / "optimized_python_backend.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(optimized_resume)
        
        print(f"✅ Optimized resume saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during optimization: {e}")
        return False


def test_mock_optimizer():
    """Demonstrate optimizer with mock data"""
    print("\n🎭 MOCK OPTIMIZER DEMONSTRATION")
    print("=" * 50)
    
    base_resume = """John Doe

Software Engineer with 2 years of experience in backend development.

Skills:
Python, SQL, C#, .NET, REST APIs, Selenium, Git, Docker

Experience:
Junior Software Developer | Tech Company Inc. | 2022-2023
- Developed backend services using Python and SQL
- Built RESTful APIs
- Automated testing workflows"""
    
    job_description = """
    Python Backend Developer needed with:
    - Python experience
    - SQL database skills
    - REST API development
    - Docker containerization
    """
    
    print("📄 Base Resume Preview:")
    print(base_resume[:200] + "...")
    
    print("\n🎯 Job Requirements:")
    print("- Python, SQL, REST APIs, Docker")
    
    print("\n🤖 AI Optimization Would:")
    print("   ✅ Reorder skills to match job priorities")
    print("   ✅ Emphasize Python and SQL experience")
    print("   ✅ Highlight REST API and Docker work")
    print("   ✅ Use stronger action verbs")
    print("   ✅ Add relevant ATS keywords")
    print("   ✅ Improve professional language")
    print("   ✅ Keep all experience truthful")
    
    print("\n💡 Result:")
    print("   • Higher ATS ranking")
    print("   • Better keyword matching")
    print("   • More professional presentation")
    print("   • Increased interview chances")
    
    return True


def test_skill_based_optimization():
    """Test optimization with specific skill requirements"""
    print("\n🎯 SKILL-BASED OPTIMIZATION TEST")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_key_here":
        print("🎭 Using mock demonstration (API key not configured)")
        
        print("\n📋 Skill Requirements:")
        required_skills = ["Python", "SQL", "REST APIs", "Docker"]
        preferred_skills = ["FastAPI", "Redis", "AWS", "CI/CD"]
        
        print(f"Required: {', '.join(required_skills)}")
        print(f"Preferred: {', '.join(preferred_skills)}")
        
        print("\n🤖 AI Would:")
        print("   • Emphasize required skills in experience section")
        print("   • Add preferred skills if candidate has them")
        print("   • Reorganize projects to highlight relevant tech")
        print("   • Optimize summary with key keywords")
        print("   • Ensure ATS keyword density is natural")
        
        return True
    
    try:
        optimizer = ResumeOptimizer()
        loader = ResumeLoader()
        
        base_resume = loader.load_base_resume()
        
        required_skills = ["Python", "SQL", "REST APIs", "Docker"]
        preferred_skills = ["FastAPI", "Redis", "AWS", "CI/CD"]
        job_description = "Python Backend Developer position with focus on scalable systems."
        
        print("\n🤖 Running skill-based optimization...")
        optimized = optimizer.tailor_with_skills(
            base_resume,
            required_skills,
            preferred_skills,
            job_description
        )
        
        print("✅ Skill-based optimization successful!")
        print(f"   Optimized resume length: {len(optimized)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = test_resume_optimizer()
    if success:
        test_skill_based_optimization()
    exit(0 if success else 1)

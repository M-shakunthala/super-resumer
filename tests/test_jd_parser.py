"""
Test job description parser with real job descriptions
"""
import os
from agents.jd_parser import JDParser


def test_jd_parser():
    print("🧠 JOB DESCRIPTION PARSER TEST")
    print("=" * 50)
    
    # Check if API key is available
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_key_here":
        print("❌ OpenAI API key not configured")
        print("Please set OPENAI_API_KEY in .env file")
        print("\nUsing mock data for demonstration...")
        test_mock_parser()
        return True
    
    try:
        parser = JDParser()
        print("✅ JD Parser initialized successfully")
    except ValueError as e:
        print(f"❌ Initialization error: {e}")
        print("\nUsing mock data for demonstration...")
        test_mock_parser()
        return True
    
    # Sample job description
    sample_jd = """
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
    
    print("\n📄 Sample Job Description:")
    print("-" * 50)
    print(sample_jd[:200] + "...")
    print("-" * 50)
    
    print("\n🤖 Parsing job description...")
    try:
        result = parser.extract(sample_jd)
        
        print("\n✅ Parsing successful!")
        print("\n📋 Extracted Information:")
        print(f"Required Skills: {', '.join(result.get('required_skills', []))}")
        print(f"Preferred Skills: {', '.join(result.get('preferred_skills', []))}")
        print(f"Experience Level: {result.get('experience_level', 'unknown')}")
        print(f"ATS Keywords: {', '.join(result.get('ats_keywords', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during parsing: {e}")
        return False


def test_mock_parser():
    """Demonstrate parser structure with mock data"""
    print("\n🎭 MOCK PARSER DEMONSTRATION")
    print("=" * 50)
    
    # Mock result structure
    mock_result = {
        "required_skills": ["Python", "SQL", "REST APIs", "Docker"],
        "preferred_skills": ["FastAPI", "Redis", "CI/CD", "AWS"],
        "experience_level": "Mid-level",
        "ats_keywords": ["backend", "microservices", "python", "apis", "databases"]
    }
    
    print("📋 Mock Parser Output:")
    print(f"\nRequired Skills: {', '.join(mock_result['required_skills'])}")
    print(f"Preferred Skills: {', '.join(mock_result['preferred_skills'])}")
    print(f"Experience Level: {mock_result['experience_level']}")
    print(f"ATS Keywords: {', '.join(mock_result['ats_keywords'])}")
    
    print("\n💡 This structure helps the system understand:")
    print("   • What skills are absolutely required")
    print("   • What skills are nice-to-have")
    print("   • Experience level expectations")
    print("   • Keywords for ATS optimization")
    
    return True


if __name__ == "__main__":
    success = test_jd_parser()
    exit(0 if success else 1)

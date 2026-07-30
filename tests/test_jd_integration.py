"""
Integration test: JD Parser with job search workflow
"""
from agents.jd_parser import JDParser
import os


def demonstrate_jd_workflow():
    print("🚀 JOB DESCRIPTION PARSER - WORKFLOW DEMONSTRATION")
    print("=" * 60)
    
    # Sample job descriptions from different searches
    job_descriptions = [
        {
            "title": "Python Developer",
            "jd": """
            We are seeking a Python Developer to build scalable backend services.
            
            Requirements:
            - 3+ years Python development experience
            - Strong SQL and database design skills
            - Experience with REST APIs and microservices
            - Knowledge of Docker and Kubernetes
            - Familiarity with AWS or Azure cloud platforms
            
            Bonus points for:
            - Experience with Django or FastAPI
            - Knowledge of Redis caching
            - Understanding of CI/CD pipelines
            
            Join our innovative team and work on cutting-edge projects!
            """
        },
        {
            "title": "Backend Engineer",
            "jd": """
            Backend Engineer needed for our growing platform.
            
            Must have:
            - Python programming expertise
            - SQL database experience (PostgreSQL preferred)
            - API development skills
            - Container deployment knowledge
            
            Nice to have:
            - C#/.NET background
            - Microservices architecture experience
            - Cloud platform experience
            
            We're looking for someone passionate about backend systems.
            """
        },
        {
            "title": "Software Engineer - AI/ML",
            "jd": """
            Software Engineer focused on AI/ML applications.
            
            Required:
            - Python programming
            - Machine Learning frameworks (TensorFlow, PyTorch)
            - Data processing skills
            - API development experience
            
            Preferred:
            - MLOps experience
            - Cloud deployment skills
            - Docker and Kubernetes
            - SQL and NoSQL databases
            
            Experience level: Mid to Senior
            
            Work on exciting AI projects!
            """
        }
    ]
    
    # Check if real API is available
    api_key = os.getenv("OPENAI_API_KEY")
    use_real_api = api_key and api_key != "your_openai_key_here"
    
    if use_real_api:
        print("🤖 Using Real OpenAI API")
        try:
            parser = JDParser()
        except Exception as e:
            print(f"❌ Failed to initialize parser: {e}")
            print("Using mock demonstration instead...")
            use_real_api = False
    else:
        print("🎭 Using Mock Demonstration (API key not configured)")
    
    print("\n")
    
    for i, job in enumerate(job_descriptions, 1):
        print(f"📋 Job {i}: {job['title']}")
        print("-" * 60)
        
        if use_real_api:
            try:
                result = parser.extract(job['jd'])
                display_result(result, job['title'])
            except Exception as e:
                print(f"❌ Error parsing: {e}")
                # Use mock for fallback
                result = get_mock_result(job['title'])
                display_result(result, job['title'])
        else:
            result = get_mock_result(job['title'])
            display_result(result, job['title'])
        
        print("\n")
    
    print("=" * 60)
    print("✅ WORKFLOW DEMONSTRATION COMPLETE")
    print("\n💡 Integration Benefits:")
    print("   • Understands job requirements automatically")
    print("   • Separates required vs preferred skills")
    print("   • Identifies experience level expectations")
    print("   • Extracts ATS keywords for optimization")
    print("   • Enables intelligent resume tailoring")


def display_result(result, job_title):
    """Display parsed job description results"""
    print(f"\n🎯 {job_title} - Parsed Results:")
    print(f"   Required Skills: {', '.join(result.get('required_skills', []))}")
    print(f"   Preferred Skills: {', '.join(result.get('preferred_skills', []))}")
    print(f"   Experience Level: {result.get('experience_level', 'unknown')}")
    print(f"   ATS Keywords: {', '.join(result.get('ats_keywords', []))}")
    
    # Show how this helps the system
    print(f"\n   💡 System now knows:")
    print(f"      • Must match: {result.get('required_skills', [])[:3]}")
    print(f"      • Nice to have: {result.get('preferred_skills', [])[:2]}")


def get_mock_result(job_title):
    """Generate mock results based on job title"""
    if "Python" in job_title:
        return {
            "required_skills": ["Python", "SQL", "REST APIs", "Docker"],
            "preferred_skills": ["FastAPI", "Redis", "AWS", "CI/CD"],
            "experience_level": "Mid-level",
            "ats_keywords": ["python", "backend", "apis", "microservices", "databases"]
        }
    elif "Backend" in job_title:
        return {
            "required_skills": ["Python", "SQL", "APIs", "Docker"],
            "preferred_skills": ["C#", ".NET", "Microservices", "Cloud"],
            "experience_level": "Mid-level",
            "ats_keywords": ["backend", "python", "sql", "apis", "databases"]
        }
    elif "AI" in job_title or "ML" in job_title:
        return {
            "required_skills": ["Python", "TensorFlow", "PyTorch", "Data Processing"],
            "preferred_skills": ["MLOps", "Docker", "Kubernetes", "SQL"],
            "experience_level": "Senior",
            "ats_keywords": ["ai", "machine learning", "python", "data science", "ml"]
        }
    else:
        return {
            "required_skills": ["Python", "SQL", "APIs"],
            "preferred_skills": ["Docker", "Cloud", "CI/CD"],
            "experience_level": "Mid-level",
            "ats_keywords": ["software", "engineering", "python", "development"]
        }


if __name__ == "__main__":
    demonstrate_jd_workflow()

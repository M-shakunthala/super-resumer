"""
Test the resume system functionality
"""
from resumes.resume_loader import ResumeLoader


def test_resume_system():
    print("🧪 RESUME SYSTEM TEST")
    print("=" * 50)
    
    # Initialize loader
    loader = ResumeLoader()
    
    # Test 1: Load base resume
    print("\n1. Loading base resume...")
    if loader.resume_exists():
        base_resume = loader.load_base_resume()
        print(f"   ✅ Loaded resume ({len(base_resume)} characters)")
    else:
        print("   ❌ Resume file not found")
        return False
    
    # Test 2: Parse sections
    print("\n2. Parsing resume sections...")
    sections = loader.get_resume_sections()
    print(f"   ✅ Found {len(sections)} sections:")
    for section in sections.keys():
        print(f"      - {section}")
    
    # Test 3: Save tailored resume
    print("\n3. Saving tailored resume...")
    tailored_content = """John Doe

Software Engineer with 2 years of experience specialized in Python backend development.

Skills:
Python, SQL, Django, FastAPI, PostgreSQL, Redis, Docker, REST APIs

Experience:
Junior Python Developer | Tech Company Inc. | 2022-2023
- Developed and maintained Python backend services
- Built RESTful APIs using Django and FastAPI
- Optimized SQL queries improving performance by 30%
- Automated deployment using Docker and CI/CD

Projects:
Python Backend API | Personal Project
- Built scalable REST API using FastAPI
- Implemented PostgreSQL database with complex queries
- Added Redis caching for improved performance
"""
    
    output_path = loader.save_tailored_resume(tailored_content, "Python Developer")
    print(f"   ✅ Saved tailored resume to: {output_path}")
    
    # Verify the file was created
    from pathlib import Path
    if Path(output_path).exists():
        print(f"   ✅ File created successfully")
    else:
        print(f"   ❌ File creation failed")
        return False
    
    # Test 4: Load tailored resume
    print("\n4. Loading tailored resume...")
    tailored_loader = ResumeLoader(output_path)
    loaded_content = tailored_loader.load_base_resume()
    print(f"   ✅ Loaded tailored resume ({len(loaded_content)} characters)")
    
    print("\n✅ ALL TESTS PASSED")
    print("\n📁 Resume system is ready for AI integration!")
    return True


if __name__ == "__main__":
    success = test_resume_system()
    exit(0 if success else 1)

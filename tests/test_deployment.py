# -*- coding: utf-8 -*-
"""
Test deployment without Docker
Verifies that the application can run in manual mode
"""
import os
import sys

def test_environment():
    """Test if environment is properly configured"""
    print("Testing environment configuration...")
    
    # Check .env file
    if not os.path.exists(".env"):
        print("FAIL .env file not found")
        return False
    
    # Check OPENAI_API_KEY
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("FAIL OPENAI_API_KEY not set")
        return False
    
    print("OK Environment configured correctly")
    return True

def test_dependencies():
    """Test if required dependencies are installed"""
    print("Testing dependencies...")
    
    required_modules = [
        "streamlit",
        "pandas", 
        "plotly",
        "sqlite3",
        "loguru"
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
            print("OK " + module)
        except ImportError:
            print("FAIL " + module)
            missing.append(module)
    
    if missing:
        print("Missing modules: " + str(missing))
        return False
    
    print("All dependencies installed")
    return True

def test_database():
    """Test database initialization"""
    print("Testing database...")
    
    try:
        from memory.job_memory import JobMemory
        
        memory = JobMemory()
        print("OK Database initialized")
        
        # Test basic operations
        test_job = {
            "url": "https://test.com/job",
            "title": "Test Job",
            "company": "Test Company",
            "platform": "test",
            "status": "new",
            "score": 0.5,
            "interview": 0
        }
        
        memory.save(test_job)
        print("OK Database write successful")
        
        jobs = memory.get_all_jobs()
        print("OK Database read successful (" + str(len(jobs)) + " jobs)")
        
        memory.close()
        return True
        
    except Exception as e:
        print("FAIL Database error: " + str(e))
        return False

def test_dashboard():
    """Test dashboard configuration"""
    print("Testing dashboard...")
    
    if not os.path.exists("ui/dashboard.py"):
        print("FAIL Dashboard file not found")
        return False
    
    print("OK Dashboard file exists")
    return True

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI Job Agent - Deployment Test")
    print("=" * 50)
    print()
    
    tests = [
        ("Environment", test_environment),
        ("Dependencies", test_dependencies),
        ("Database", test_database),
        ("Dashboard", test_dashboard)
    ]
    
    results = []
    for test_name, test_func in tests:
        print("\n" + test_name + ":")
        print("-" * 30)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(test_name + ": " + status)
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("All tests passed! Ready for deployment.")
        print("Run: ./start_all.sh")
    else:
        print("Some tests failed. Please fix issues before deployment.")
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
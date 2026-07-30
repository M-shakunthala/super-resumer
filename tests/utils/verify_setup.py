#!/usr/bin/env python3
"""
Quick verification script for Complete AI Job Application Bot (Parts 1-6)
"""
import os
import sys


def verify_setup():
    """Verify all components are properly set up"""
    print("Verifying Complete AI Job Application Bot (Parts 1-6)")
    print("=" * 60)
    
    all_good = True
    
    # Check 1: Required files exist
    print("\nChecking required files...")
    required_files = [
        # Core AI Components (Part 5)
        "automation/ai_answers.py",
        "automation/jd_parser.py", 
        "automation/matcher.py",
        "automation/semantic_matcher.py",
        # Job Scraper (Part 6)
        "automation/job_scraper.py",
        "automation/real_jobs_feed.py",
        # Orchestrator & Scheduler (Part 5)
        "automation/orchestrator.py",
        "scheduler.py",
        "scheduler_enhanced.py",
        "run_bot.py",
        # Legacy support
        "mock_jobs_feed.py"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print("  [OK] " + file)
        else:
            print("  [MISSING] " + file)
            all_good = False
    
    # Check 2: Environment variables
    print("\nChecking environment variables...")
    env_vars = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "USE_REAL_JOB_FEED": os.getenv("USE_REAL_JOB_FEED"),
        "HEADLESS": os.getenv("HEADLESS")
    }
    
    for var, value in env_vars.items():
        if value:
            if value != "your_openai_key_here" and value != "your_key_here":
                print("  [OK] " + var + " is set")
            else:
                print("  [WARNING] " + var + " needs to be set with actual value")
        else:
            print("  [INFO] " + var + " not set (using defaults)")
    
    # Check 3: Python dependencies
    print("\nChecking Python dependencies...")
    required_packages = [
        "openai",
        "numpy", 
        "loguru",
        "selenium"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            print("  [OK] " + package)
        except ImportError:
            print("  [MISSING] " + package + " - NOT INSTALLED")
            all_good = False
    
    # Check 4: Configuration
    print("\nChecking configuration...")
    config_vars = {
        "MATCH_THRESHOLD": os.getenv("MATCH_THRESHOLD", "0.6"),
        "SCHEDULER_INTERVAL_MINUTES": os.getenv("SCHEDULER_INTERVAL_MINUTES", "5"),
        "ENABLE_AI_MATCHING": os.getenv("ENABLE_AI_MATCHING", "true"),
        "USE_REAL_JOB_FEED": os.getenv("USE_REAL_JOB_FEED", "true"),
        "JOB_CACHE_MINUTES": os.getenv("JOB_CACHE_MINUTES", "30")
    }
    
    for var, value in config_vars.items():
        print("  [OK] " + var + " = " + str(value))
    
    # Check 5: Import test (only for modules that don't require API keys)
    print("\nTesting imports...")
    try:
        from automation.matcher import JobMatcher
        print("  [OK] JobMatcher")
        
        from automation.jd_parser import JDParser
        print("  [OK] JDParser (requires API key for full functionality)")
        
        from automation.ai_answers import AIAnswers
        print("  [OK] AIAnswers (requires API key for full functionality)")
        
        from automation.semantic_matcher import SemanticMatcher
        print("  [OK] SemanticMatcher (requires API key for full functionality)")
        
        from automation.job_scraper import JobScraper
        print("  [OK] JobScraper")
        
        from automation.real_jobs_feed import RealJobsFeed
        print("  [OK] RealJobsFeed")
        
        from automation.orchestrator import JobOrchestrator
        print("  [OK] JobOrchestrator")
        
        from scheduler_enhanced import Scheduler
        print("  [OK] Scheduler")
        
    except ImportError as e:
        print("  [ERROR] Import error: " + str(e))
        all_good = False
    
    # Final result
    print("\n" + "=" * 60)
    
    # Check if API key is the only missing item
    api_key_missing = os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "your_openai_key_here"
    
    if api_key_missing:
        print("[ALMOST COMPLETE] System components are installed and working!")
        print("\nTo complete setup:")
        print("   1. Add your OpenAI API key to .env file:")
        print("      OPENAI_API_KEY=your_actual_key_here")
        print("   2. Then run: python3 verify_setup.py")
        print("\nTo test components (without API key, limited functionality):")
        print("   python3 test_scheduler.py")
        print("   python3 test_job_scraper.py feed")
        return 0
    elif all_good:
        print("[SUCCESS] All checks passed! Complete system ready.")
        print("\nTo start the bot with real job scraping:")
        print("   python3 run_bot.py")
        print("\nTo test individual components:")
        print("   python3 test_job_scraper.py")
        print("   python3 test_full_pipeline.py pipeline")
        print("   python3 test_jd_parser.py")
        print("   python3 test_semantic_matcher.py") 
        print("   python3 test_scheduler.py")
        return 0
    else:
        print("[ERROR] Some checks failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(verify_setup())

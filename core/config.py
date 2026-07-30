from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # API Configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")  # Fallback
    
    # Job Search Configuration
    LOCATION = "Bangalore"
    MIN_SALARY_LPA = 7
    MATCH_THRESHOLD = 85  # 85% match threshold
    
    # Role Configuration
    TARGET_ROLES = ["Software Developer", "C# Developer", "Python AI Developer", "AI Engineer"]
    
    # Resume Configuration (using PDF files)
    RESUME_C_SHARP = "resumes/Shakunthala_c#_Resume.pdf"
    RESUME_PYTHON_AI = "resumes/Shakunthala_python_Resume.pdf"
    
    # Job Sources
    JOB_SOURCES = ["linkedin", "indeed", "naukri", "company_websites"]
    
    # LinkedIn Credentials (optional for manual workflow)
    LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
    LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

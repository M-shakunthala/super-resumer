from automation.matcher import JobMatcher

# Test the Job Matcher with a sample job description
jd_text = """
We are looking for a Senior Python Developer with 5+ years of experience.
Required skills: Python, Django, PostgreSQL, AWS, Docker, Machine Learning.
You will be working on building scalable web applications and microservices.
"""

try:
    matcher = JobMatcher()
    score, parsed = matcher.score(jd_text)
    print("Job Matcher Result:")
    print(f"Match Score: {score}")
    print(f"Parsed Data: {parsed}")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure to:")
    print("1. Set OPENAI_API_KEY in your .env file")
    print("2. Set your skills in profile_memory (skills key)")

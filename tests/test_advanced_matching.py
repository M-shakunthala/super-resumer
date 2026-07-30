from automation.semantic_matcher import SemanticMatcher
from automation.jd_parser import JDParser
from automation.profile_memory import ProfileMemory

def advanced_job_matching(job_description):
    """
    Advanced job matching using semantic similarity
    """
    # Parse the job description
    parsed_job = JDParser.extract(job_description)
    
    # Get user profile
    user_profile = f"""
    Name: {ProfileMemory.get("name")}
    Experience: {ProfileMemory.get("experience")}  
    Skills: {ProfileMemory.get("skills")}
    Projects: {ProfileMemory.get("projects")}
    """
    
    # Calculate semantic similarity
    matcher = SemanticMatcher()
    similarity_score = matcher.similarity(job_description, user_profile)
    
    # Also match specific skills
    user_skills = ProfileMemory.get("skills").lower()
    job_skills = " ".join(parsed_job.get("skills", [])).lower()
    
    skill_matches = [skill for skill in user_skills.split(",") 
                    if skill.strip().lower() in job_skills]
    
    return {
        "semantic_similarity": similarity_score,
        "parsed_job": parsed_job,
        "skill_matches": skill_matches,
        "match_quality": "High" if similarity_score > 0.8 else "Medium" if similarity_score > 0.6 else "Low",
        "recommended": similarity_score > 0.7  # Threshold for applying
    }

# Test with a real job description
job_jd = """
We are seeking a Senior Software Engineer to join our growing team.
Requirements:
- 5+ years of experience in software development
- Strong proficiency in Python, JavaScript, and React
- Experience with cloud platforms (AWS/GCP)
- Knowledge of databases (PostgreSQL, MongoDB)
- Excellent problem-solving skills
"""

try:
    result = advanced_job_matching(job_jd)
    print("Advanced Job Matching Results:")
    print(f"Semantic Similarity: {result['semantic_similarity']:.4f}")
    print(f"Match Quality: {result['match_quality']}")
    print(f"Recommended to Apply: {result['recommended']}")
    print(f"Parsed Job: {result['parsed_job']}")
    print(f"Skill Matches: {result['skill_matches']}")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure to set OPENAI_API_KEY in your .env file")

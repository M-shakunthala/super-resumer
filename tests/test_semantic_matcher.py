from automation.semantic_matcher import SemanticMatcher

# Test the Semantic Matcher
job_description = "We are looking for a Senior Python Developer with experience in Django, PostgreSQL, and AWS to build scalable web applications."

user_profile = "Experienced software developer with 5+ years in Python, Django framework, PostgreSQL databases, and AWS cloud services. Passionate about building scalable web applications and microservices."

try:
    matcher = SemanticMatcher()
    similarity_score = matcher.similarity(job_description, user_profile)
    print("Semantic Matcher Result:")
    print(f"Similarity Score: {similarity_score:.4f}")
    print(f"Match Quality: {'High' if similarity_score > 0.8 else 'Medium' if similarity_score > 0.6 else 'Low'}")
except Exception as e:
    print(f"Error: {e}")
    print("Make sure to set OPENAI_API_KEY in your .env file")

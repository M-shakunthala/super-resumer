import os
from openai import OpenAI
from core.config import Config


class ResumeOptimizer:

    def __init__(self):
        """Initialize resume optimizer with configuration"""
        self.config = Config.load()
        ai_config = self.config.get('ai', {})
        openai_config = ai_config.get('openai', {})
        
        # Get API key from environment
        api_key = os.getenv(openai_config.get('api_key_env', 'OPENAI_API_KEY'))
        
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = openai_config.get('model', 'gpt-4o-mini')
        
        optimizer_config = openai_config.get('resume_optimizer', {})
        self.temperature = optimizer_config.get('temperature', 0.4)
        self.max_tokens = optimizer_config.get('max_tokens', 1000)

    def tailor(
        self,
        base_resume,
        job_description
    ):
        """
        Optimize resume for specific job description using AI
        
        Args:
            base_resume: Original resume text
            job_description: Job description text
            
        Returns:
            Optimized resume text
        """
        # Validate inputs
        if not base_resume or len(base_resume.strip()) < 100:
            raise ValueError("Base resume is too short or empty")
        
        if not job_description or len(job_description.strip()) < 50:
            raise ValueError("Job description is too short or empty")
        
        prompt = f"""
You are an expert ATS (Applicant Tracking System) resume optimizer with extensive experience in recruitment and resume writing.

TASK:
Optimize the provided resume for the specific job description while maintaining complete honesty.

CRITICAL RULES:
1. KEEP IT TRUTHFUL: Never invent fake experience, skills, or achievements
2. ATS FRIENDLY: Use standard formatting, clear section headers, relevant keywords
3. IMPROVE KEYWORDS: Add relevant keywords from the job description that match the candidate's actual experience
4. PROFESSIONAL LANGUAGE: Use strong action verbs and professional terminology
5. MAINTAIN INTEGRITY: Only highlight skills and experience the candidate actually possesses
6. FOCUS ON RELEVANCE: Emphasize aspects most relevant to the target job
7. QUANTIFIABLE ACHIEVEMENTS: Where possible, use numbers and metrics (if present in original)
8. CLEAR STRUCTURE: Maintain standard resume sections (Summary, Skills, Experience, Projects, Education)

BASE RESUME:
{base_resume}

TARGET JOB DESCRIPTION:
{job_description}

OPTIMIZATION APPROACH:
1. Analyze the job requirements and identify key skills/keywords
2. Match these with the candidate's actual experience from the base resume
3. Reorganize content to highlight most relevant experience first
4. Optimize language to be more professional and action-oriented
5. Ensure all keywords are naturally integrated (not keyword stuffing)
6. Maintain truthful representation of candidate's background

Return the optimized resume in clean text format.
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert ATS resume optimizer who helps candidates present their genuine experience in the best possible light for specific job opportunities."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            optimized_resume = response.choices[0].message.content
            return optimized_resume
            
        except Exception as e:
            print(f"Error optimizing resume: {e}")
            # Return original resume on failure
            return base_resume
    
    def tailor_with_skills(
        self,
        base_resume,
        required_skills,
        preferred_skills,
        job_description
    ):
        """
        Optimize resume with specific skill requirements
        
        Args:
            base_resume: Original resume text
            required_skills: List of required skills for job
            preferred_skills: List of preferred skills for job
            job_description: Full job description text
            
        Returns:
            Optimized resume text
        """
        skills_text = f"""
REQUIRED SKILLS: {', '.join(required_skills)}
PREFERRED SKILLS: {', '.join(preferred_skills)}
"""
        
        enhanced_jd = f"{job_description}\n\n{skills_text}"
        return self.tailor(base_resume, enhanced_jd)
    
    def compare_versions(self, original, optimized):
        """
        Compare original and optimized resumes to show improvements
        
        Args:
            original: Original resume text
            optimized: Optimized resume text
            
        Returns:
            Dictionary with comparison metrics
        """
        return {
            "original_length": len(original),
            "optimized_length": len(optimized),
            "length_change": len(optimized) - len(original),
            "original_word_count": len(original.split()),
            "optimized_word_count": len(optimized.split())
        }

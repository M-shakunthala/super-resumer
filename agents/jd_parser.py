import json
import os
from openai import OpenAI
from core.config import Config


class JDParser:

    def __init__(self):
        """Initialize JD parser with configuration"""
        self.config = Config.load()
        ai_config = self.config.get('ai', {})
        openai_config = ai_config.get('openai', {})
        
        # Get API key from environment
        api_key = os.getenv(openai_config.get('api_key_env', 'OPENAI_API_KEY'))
        
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.model = openai_config.get('model', 'gpt-4o-mini')
        
        jd_parser_config = openai_config.get('jd_parser', {})
        self.temperature = jd_parser_config.get('temperature', 0.3)
        self.max_tokens = jd_parser_config.get('max_tokens', 500)

    def extract(self, jd):
        """
        Extract key information from job description using AI
        
        Args:
            jd: Job description text
            
        Returns:
            Dictionary with extracted information
        """
        if not jd or len(jd.strip()) < 50:
            return self._empty_result()
        
        prompt = f"""
Extract the following information from this job description:

1. Required skills (hard skills needed for the job)
2. Preferred skills (nice-to-have skills)
3. Experience level (entry, mid, senior, etc.)
4. Important ATS keywords (keywords for applicant tracking systems)

Job description:
{jd}

Return the result as a JSON object with this exact structure:
{{
    "required_skills": ["skill1", "skill2", ...],
    "preferred_skills": ["skill1", "skill2", ...],
    "experience_level": "level",
    "ats_keywords": ["keyword1", "keyword2", ...]
}}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at parsing job descriptions and extracting key information for resume matching and ATS optimization."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )

            content = response.choices[0].message.content
            
            # Parse JSON response
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON response: {e}")
            return self._empty_result()
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return self._empty_result()
    
    def _empty_result(self):
        """Return empty result structure for error cases"""
        return {
            "required_skills": [],
            "preferred_skills": [],
            "experience_level": "unknown",
            "ats_keywords": []
        }

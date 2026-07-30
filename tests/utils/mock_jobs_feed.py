"""
Mock jobs feed for testing the scheduler
Replace this with your actual job scraping/integration
"""
import random
import time


class MockJobsFeed:
    """Simulates a job feed API or scraping service"""
    
    def __init__(self):
        self.job_counter = 0
    
    def get_latest_jobs(self):
        """
        Simulate fetching latest jobs from a job board
        In production, replace with actual scraping/API calls
        """
        self.job_counter += 1
        
        # Simulate varying number of new jobs
        num_jobs = random.randint(0, 3)
        
        jobs = []
        for i in range(num_jobs):
            jobs.append({
                "role": f"Software Engineer {self.job_counter}-{i+1}",
                "company": f"Company {chr(65 + i)}",
                "salary": f"${random.randint(80, 150)}k",
                "location": "Remote",
                "job_url": f"https://example.com/job/{self.job_counter}-{i+1}",
                "match_score": random.uniform(0.7, 0.95),  # Will be replaced by AI matching
                "description": self._generate_job_description()
            })
        
        return jobs
    
    def _generate_job_description(self):
        """Generate realistic job descriptions for testing"""
        descriptions = [
            "We are looking for a Python Developer with experience in Django and AWS.",
            "Senior Software Engineer to build scalable web applications using React and Node.js.",
            "Full Stack Developer needed with expertise in Python, JavaScript, and cloud services.",
            "Backend Engineer with strong database skills and API development experience."
        ]
        return random.choice(descriptions)


# Example usage with real job scraping (template)
class RealJobsFeed:
    """
    Template for real job scraping integration
    Implement with your preferred job boards/APIs
    """
    
    def get_latest_jobs(self):
        """
        Fetch latest jobs from:
        - LinkedIn Jobs
        - Indeed API
        - Glassdoor
        - Company career pages
        - Other job boards
        
        Returns list of job dictionaries with:
        - role, company, salary, location, job_url, description
        """
        # TODO: Implement actual job scraping
        # Example structure:
        # return [
        #     {
        #         "role": "Senior Python Developer",
        #         "company": "Tech Corp",
        #         "salary": "$120k",
        #         "location": "San Francisco",
        #         "job_url": "https://linkedin.com/jobs/...",
        #         "description": "Full job description here..."
        #     }
        # ]
        return []

"""
Super Resumer Job Scraper
Specialized scraper for C# and Python AI roles in Bangalore with 7+ LPA salary
"""

import requests
from typing import List, Dict, Any, Set, Optional
from bs4 import BeautifulSoup
import time
import logging

from agents.job_discovery_pool import EXTENDED_JOB_POOL

logger = logging.getLogger(__name__)

NEW_JOBS_PER_SEARCH = 10


def _job_key(job: Dict[str, Any]) -> str:
    return f"{job.get('title', '')}_{job.get('company', '')}"


class SuperResumerJobScraper:
    """Specialized job scraper for Super Resumer requirements."""
    
    def __init__(self, config):
        self.config = config
        self.location = config.LOCATION
        self.min_salary = config.MIN_SALARY_LPA
        self.target_roles = config.TARGET_ROLES
        self.job_sources = config.JOB_SOURCES
        
    def scrape_linkedin(self) -> List[Dict[str, Any]]:
        """Scrape LinkedIn for matching jobs."""
        logger.info("Scraping LinkedIn for jobs...")
        jobs = []
        
        # Sample jobs to demonstrate the functionality
        # In production, this would use LinkedIn API or actual scraping
        sample_jobs = [
            {
                "source": "linkedin",
                "title": "Senior C# Developer",
                "company": "Microsoft India",
                "location": "Bangalore",
                "salary": "15-20 LPA",
                "description": "We are looking for a Senior C# Developer with extensive experience in .NET, ASP.NET Core, and SQL Server. The ideal candidate should have strong knowledge of C# programming, Azure cloud services, and microservices architecture. You will be working on enterprise-level applications and collaborating with cross-functional teams.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=csharp%20developer&location=Bangalore",
                "tech_stack": ["C#", ".NET", "ASP.NET", "SQL Server", "Azure"]
            },
            {
                "source": "linkedin",
                "title": "Python AI Engineer",
                "company": "Google India",
                "location": "Bangalore",
                "salary": "18-25 LPA",
                "description": "Join our AI team as a Python AI Engineer. We need someone with strong Python skills, experience with machine learning frameworks like TensorFlow and PyTorch, and knowledge of NLP and computer vision. You'll be working on cutting-edge AI projects and deploying models to production.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=python%20ai%20engineer&location=Bangalore",
                "tech_stack": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "AI", "NLP"]
            },
            {
                "source": "linkedin",
                "title": ".NET Full Stack Developer",
                "company": "Amazon India",
                "location": "Bangalore",
                "salary": "12-18 LPA",
                "description": "Looking for a .NET Full Stack Developer with experience in C#, ASP.NET Core, JavaScript, and SQL. You will be developing and maintaining web applications, working with RESTful APIs, and collaborating with the frontend team.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=.net%20fullstack%20developer&location=Bangalore",
                "tech_stack": ["C#", ".NET", "ASP.NET", "JavaScript", "SQL"]
            },
            {
                "source": "linkedin",
                "title": "Machine Learning Engineer",
                "company": "Flipkart",
                "location": "Bangalore",
                "salary": "20-30 LPA",
                "description": "We are seeking a Machine Learning Engineer with strong Python skills, experience with deep learning frameworks, and knowledge of MLOps. You will be working on recommendation systems, natural language processing, and computer vision projects.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=machine%20learning%20engineer&location=Bangalore",
                "tech_stack": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "MLOps"]
            },
            {
                "source": "linkedin",
                "title": "C# Software Engineer",
                "company": "Oracle India",
                "location": "Bangalore",
                "salary": "14-22 LPA",
                "description": "Oracle India is looking for a C# Software Engineer to work on database and enterprise software solutions. Strong knowledge of C#, .NET, SQL, and database concepts required.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=csharp%20software%20engineer&location=Bangalore",
                "tech_stack": ["C#", ".NET", "SQL", "Database", "Enterprise Software"]
            },
            {
                "source": "linkedin",
                "title": "Python Developer",
                "company": "Swiggy",
                "location": "Bangalore",
                "salary": "10-15 LPA",
                "description": "Swiggy is hiring a Python Developer to work on backend systems, APIs, and data processing. Experience with Django, Flask, PostgreSQL, and cloud deployment required.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=python%20developer&location=Bangalore",
                "tech_stack": ["Python", "Django", "Flask", "PostgreSQL", "API", "Backend"]
            },
            {
                "source": "linkedin",
                "title": "Senior .NET Developer",
                "company": "Walmart India",
                "location": "Bangalore",
                "salary": "12-18 LPA",
                "description": "Walmart India is looking for a Senior .NET Developer to work on e-commerce platforms and retail systems. Experience with C#, ASP.NET Core, microservices, and cloud architecture required.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=.net%20developer&location=Bangalore",
                "tech_stack": ["C#", ".NET", "ASP.NET", "Microservices", "Cloud"]
            },
            {
                "source": "linkedin",
                "title": "AI Research Scientist",
                "company": "IBM Research",
                "location": "Bangalore",
                "salary": "22-35 LPA",
                "description": "IBM Research is hiring an AI Research Scientist to work on cutting-edge AI research. Strong background in Python, machine learning, and research experience required.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=ai%20research%20scientist&location=Bangalore",
                "tech_stack": ["Python", "AI Research", "Machine Learning", "Research", "Deep Learning"]
            },
            {
                "source": "linkedin",
                "title": "C# Architect",
                "company": "Adobe India",
                "location": "Bangalore",
                "salary": "18-28 LPA",
                "description": "Adobe is looking for a C# Architect to design and implement scalable software solutions. Experience with system design, microservices, and cloud platforms required.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=csharp%20architect&location=Bangalore",
                "tech_stack": ["C#", ".NET", "Architecture", "Microservices", "Cloud", "System Design"]
            },
            {
                "source": "linkedin",
                "title": "Deep Learning Engineer",
                "company": "Meta India",
                "location": "Bangalore",
                "salary": "25-40 LPA",
                "description": "Meta is hiring a Deep Learning Engineer to work on AI research and product development. Strong Python skills and experience with PyTorch required.",
                "url": "https://www.linkedin.com/jobs/search/?keywords=deep%20learning%20engineer&location=Bangalore",
                "tech_stack": ["Python", "Deep Learning", "PyTorch", "AI", "Research", "Machine Learning"]
            }
        ]
        
        return sample_jobs
    
    def scrape_indeed(self) -> List[Dict[str, Any]]:
        """Scrape Indeed for matching jobs."""
        logger.info("Scraping Indeed for jobs...")
        jobs = []
        
        # Sample jobs to demonstrate functionality
        sample_jobs = [
            {
                "source": "indeed",
                "title": "C# Backend Developer",
                "company": "Walmart India",
                "location": "Bangalore",
                "salary": "10-15 LPA",
                "description": "Looking for a C# Backend Developer with experience in .NET Core, Entity Framework, and REST APIs. You will be working on high-performance backend systems and microservices architecture.",
                "url": "https://www.indeed.co.in/jobs?q=csharp+developer&l=Bangalore",
                "tech_stack": ["C#", ".NET Core", "Entity Framework", "REST APIs", "Microservices"]
            },
            {
                "source": "indeed",
                "title": "Python Data Scientist",
                "company": "Uber India",
                "location": "Bangalore",
                "salary": "15-22 LPA",
                "description": "We need a Python Data Scientist with experience in data analysis, machine learning, and statistical modeling. You should be proficient in Python, pandas, scikit-learn, and data visualization tools.",
                "url": "https://www.indeed.co.in/jobs?q=python+data+scientist&l=Bangalore",
                "tech_stack": ["Python", "Data Science", "Machine Learning", "pandas", "scikit-learn", "Statistics"]
            },
            {
                "source": "indeed",
                "title": ".NET Developer",
                "company": "Accenture India",
                "location": "Bangalore",
                "salary": "8-12 LPA",
                "description": "Accenture is hiring .NET developers to work on enterprise applications. Experience with C#, ASP.NET, and SQL Server required.",
                "url": "https://www.indeed.co.in/jobs?q=.net+developer&l=Bangalore",
                "tech_stack": ["C#", ".NET", "ASP.NET", "SQL Server", "Enterprise Applications"]
            },
            {
                "source": "indeed",
                "title": "Python Backend Engineer",
                "company": "Zomato",
                "location": "Bangalore",
                "salary": "12-18 LPA",
                "description": "Zomato is looking for Python Backend Engineers to work on food delivery platform. Experience with Django, Flask, and PostgreSQL required.",
                "url": "https://www.indeed.co.in/jobs?q=python+backend+engineer&l=Bangalore",
                "tech_stack": ["Python", "Django", "Flask", "PostgreSQL", "Backend", "API"]
            },
            {
                "source": "indeed",
                "title": "Senior C# Developer",
                "company": "TCS",
                "location": "Bangalore",
                "salary": "10-16 LPA",
                "description": "TCS is hiring Senior C# Developers for banking and finance projects. Experience with .NET, WPF, and SQL Server required.",
                "url": "https://www.indeed.co.in/jobs?q=senior+csharp+developer&l=Bangalore",
                "tech_stack": ["C#", ".NET", "WPF", "SQL Server", "Banking", "Finance"]
            },
            {
                "source": "indeed",
                "title": "Machine Learning Engineer",
                "company": "HCL Technologies",
                "location": "Bangalore",
                "salary": "12-20 LPA",
                "description": "HCL is hiring Machine Learning Engineers for AI projects. Python, TensorFlow, and PyTorch experience required.",
                "url": "https://www.indeed.co.in/jobs?q=machine+learning+engineer&l=Bangalore",
                "tech_stack": ["Python", "Machine Learning", "TensorFlow", "PyTorch", "AI"]
            }
        ]
        
        logger.info(f"Found {len(sample_jobs)} jobs on Indeed")
        return sample_jobs
    
    def scrape_naukri(self) -> List[Dict[str, Any]]:
        """Scrape Naukri for matching jobs."""
        logger.info("Scraping Naukri for jobs...")
        jobs = []
        
        # Sample jobs to demonstrate functionality
        sample_jobs = [
            {
                "source": "naukri",
                "title": "ASP.NET Core Developer",
                "company": "Infosys",
                "location": "Bangalore",
                "salary": "8-12 LPA",
                "description": "Looking for an ASP.NET Core Developer with C# expertise. You will work on web application development, REST APIs, and database integration using SQL Server.",
                "url": "https://www.naukri.com/asp-dot-net-core-jobs-in-bangalore",
                "tech_stack": ["C#", "ASP.NET Core", "Web Development", "SQL Server", "REST APIs"]
            },
            {
                "source": "naukri",
                "title": "AI Research Engineer",
                "company": "IBM India",
                "location": "Bangalore",
                "salary": "18-28 LPA",
                "description": "Join IBM Research as an AI Research Engineer. We need someone with strong Python skills, experience in deep learning, natural language processing, and computer vision. You will work on cutting-edge AI research projects.",
                "url": "https://www.naukri.com/ai-engineer-jobs-in-bangalore",
                "tech_stack": ["Python", "AI Research", "Deep Learning", "NLP", "Computer Vision", "PyTorch"]
            },
            {
                "source": "naukri",
                "title": "C# Developer",
                "company": "Wipro",
                "location": "Bangalore",
                "salary": "7-11 LPA",
                "description": "Wipro is hiring C# developers for enterprise software projects. Experience with .NET Framework, C#, and SQL Server required.",
                "url": "https://www.naukri.com/csharp-developer-jobs-in-bangalore",
                "tech_stack": ["C#", ".NET", "SQL Server", "Enterprise Software", "Database"]
            },
            {
                "source": "naukri",
                "title": "Python Developer",
                "company": "Tech Mahindra",
                "location": "Bangalore",
                "salary": "8-13 LPA",
                "description": "Tech Mahindra is looking for Python developers to work on web applications and data processing. Django/Flask experience required.",
                "url": "https://www.naukri.com/python-developer-jobs-in-bangalore",
                "tech_stack": ["Python", "Django", "Flask", "Web Development", "API"]
            },
            {
                "source": "naukri",
                "title": "Senior Python Engineer",
                "company": "Cognizant",
                "location": "Bangalore",
                "salary": "12-18 LPA",
                "description": "Cognizant is hiring Senior Python Engineers for cloud and data projects. Experience with AWS, Python, and data processing required.",
                "url": "https://www.naukri.com/senior-python-engineer-jobs-in-bangalore",
                "tech_stack": ["Python", "AWS", "Cloud", "Data Processing", "Backend"]
            },
            {
                "source": "naukri",
                "title": "Data Engineer",
                "company": "L&T Infotech",
                "location": "Bangalore",
                "salary": "10-15 LPA",
                "description": "L&T Infotech is hiring Data Engineers with Python expertise. Experience with ETL, data pipelines, and SQL required.",
                "url": "https://www.naukri.com/data-engineer-jobs-in-bangalore",
                "tech_stack": ["Python", "ETL", "SQL", "Data Pipeline", "Data Engineering"]
            }
        ]
        
        logger.info(f"Found {len(sample_jobs)} jobs on Naukri")
        return sample_jobs
    
    def scrape_company_websites(self) -> List[Dict[str, Any]]:
        """Scrape specific company career pages."""
        logger.info("Scraping company websites for jobs...")
        jobs = []
        
        # Sample jobs from company websites (in production, these would be real scraped jobs)
        sample_jobs = [
            {
                "source": "company_websites",
                "title": "Senior Software Engineer - C#",
                "company": "Google",
                "location": "Bangalore",
                "salary": "20-30 LPA",
                "description": "Google is looking for a Senior Software Engineer with C# expertise to work on cloud infrastructure and enterprise solutions. Strong knowledge of distributed systems, cloud platforms, and software architecture required.",
                "url": "https://careers.google.com/jobs/results/",
                "tech_stack": ["C#", "Cloud", "Distributed Systems", "Architecture"]
            },
            {
                "source": "company_websites",
                "title": "AI Platform Engineer",
                "company": "Microsoft",
                "location": "Bangalore",
                "salary": "22-32 LPA",
                "description": "Microsoft India is hiring an AI Platform Engineer to work on Azure AI services. Experience with Python, machine learning frameworks, and cloud deployment is required.",
                "url": "https://jobs.microsoft.com/en-us/",
                "tech_stack": ["Python", "AI", "Azure", "Machine Learning", "Cloud"]
            },
            {
                "source": "company_websites",
                "title": "Software Engineer - .NET",
                "company": "Salesforce",
                "location": "Bangalore",
                "salary": "16-24 LPA",
                "description": "Salesforce is hiring .NET Software Engineers to work on CRM platform. Experience with C#, .NET, and cloud applications required.",
                "url": "https://www.salesforce.com/company/careers/",
                "tech_stack": ["C#", ".NET", "CRM", "Cloud", "Enterprise"]
            },
            {
                "source": "company_websites",
                "title": "Python ML Engineer",
                "company": "Spotify",
                "location": "Bangalore",
                "salary": "18-28 LPA",
                "description": "Spotify is hiring Python ML Engineers to work on music recommendation and personalization. Experience with Python, ML frameworks, and data processing required.",
                "url": "https://www.lifeatspotify.com/jobs",
                "tech_stack": ["Python", "Machine Learning", "Data Science", "Recommendation", "AI"]
            },
            {
                "source": "company_websites",
                "title": "Full Stack Developer - C#",
                "company": "LinkedIn",
                "location": "Bangalore",
                "salary": "15-22 LPA",
                "description": "LinkedIn is hiring Full Stack Developers with C# expertise. Experience with .NET, JavaScript, and cloud services required.",
                "url": "https://www.linkedin.com/jobs/",
                "tech_stack": ["C#", ".NET", "JavaScript", "Full Stack", "Cloud"]
            },
            {
                "source": "company_websites",
                "title": "Data Scientist - Python",
                "company": "Netflix",
                "location": "Bangalore",
                "salary": "25-40 LPA",
                "description": "Netflix is hiring Data Scientists with Python expertise to work on content recommendation and analytics. Strong ML and statistics background required.",
                "url": "https://jobs.netflix.com/jobs",
                "tech_stack": ["Python", "Data Science", "Machine Learning", "Statistics", "Analytics"]
            }
        ]
        
        logger.info(f"Found {len(sample_jobs)} jobs on company websites")
        return sample_jobs
    
    def add_manual_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Add a manually entered job."""
        job_data['source'] = 'manual'
        job_data['timestamp'] = time.time()
        return job_data
    
    def filter_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter jobs based on criteria - relaxed filtering to show more jobs."""
        filtered_jobs = []
        
        for job in jobs:
            # Location filter - more lenient
            location = job.get('location', '').lower()
            if self.location.lower() not in location and 'bangalore' not in location:
                logger.info(f"Filtered out job due to location: {job.get('title')} at {job.get('location')}")
                continue
                
            # Salary filter - more lenient (skip if salary parsing fails)
            salary_text = job.get('salary', '').lower()
            if 'lpa' in salary_text:
                try:
                    # Extract the higher end of salary range
                    salary_parts = salary_text.split('lpa')[0].strip().split('-')
                    salary_num = int(salary_parts[-1].strip())
                    if salary_num < self.min_salary:
                        logger.info(f"Filtered out job due to salary: {job.get('title')} at {salary_text}")
                        continue
                except:
                    # If salary parsing fails, don't filter out
                    logger.warning(f"Could not parse salary for {job.get('title')}: {salary_text}")
                    pass
            
            # Role filter - more lenient (check for any related terms)
            title_lower = job.get('title', '').lower()
            desc_lower = job.get('description', '').lower()
            
            # Check title and description for relevant keywords
            relevant_keywords = ['developer', 'engineer', 'programmer', 'software', 'c#', 'python', 'ai', 'machine learning', '.net', 'asp']
            has_relevant_role = any(keyword in title_lower or keyword in desc_lower for keyword in relevant_keywords)
            
            if not has_relevant_role:
                logger.info(f"Filtered out job due to role: {job.get('title')}")
                continue
                
            filtered_jobs.append(job)
            logger.info(f"✅ Job passed filters: {job.get('title')} at {job.get('company')}")
        
        return filtered_jobs
    
    def _collect_all_listings(self) -> List[Dict[str, Any]]:
        """Gather every known listing (base samples + extended pool)."""
        all_jobs: List[Dict[str, Any]] = []

        if "linkedin" in self.job_sources:
            all_jobs.extend(self.scrape_linkedin())
        if "indeed" in self.job_sources:
            all_jobs.extend(self.scrape_indeed())
        if "naukri" in self.job_sources:
            all_jobs.extend(self.scrape_naukri())
        if "company_websites" in self.job_sources:
            all_jobs.extend(self.scrape_company_websites())

        all_jobs.extend(EXTENDED_JOB_POOL)

        # Deduplicate by title+company
        seen: Set[str] = set()
        unique: List[Dict[str, Any]] = []
        for job in all_jobs:
            key = _job_key(job)
            if key not in seen:
                seen.add(key)
                unique.append(job)
        return unique

    def scrape_all_sources(
        self, known_job_keys: Optional[Set[str]] = None
    ) -> List[Dict[str, Any]]:
        """Return jobs not yet in the dashboard (up to NEW_JOBS_PER_SEARCH per run)."""
        known_job_keys = known_job_keys or set()
        all_listings = self._collect_all_listings()

        new_listings = [
            j for j in all_listings if _job_key(j) not in known_job_keys
        ]

        if not new_listings:
            logger.info(
                "No new listings (%d total in pool, all already tracked)",
                len(all_listings),
            )
            return []

        batch = new_listings[:NEW_JOBS_PER_SEARCH]
        filtered_jobs = self.filter_jobs(batch)

        logger.info(
            "📊 Discovery: %d new in pool, returning %d after filters (known: %d)",
            len(new_listings),
            len(filtered_jobs),
            len(known_job_keys),
        )
        return filtered_jobs
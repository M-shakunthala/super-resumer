from core.config import Config
from agents.job_scraper import JobScraper
from agents.job_filter import JobFilter
from agents.job_ranker import JobRanker
from core.orchestrator import Orchestrator
from memory.job_memory import JobMemory
from loguru import logger
import time


config = Config.load()

# Check testing phase
testing_config = config.get("testing", {})
current_phase = testing_config.get("current_phase", 4)
dry_run = testing_config.get("dry_run", False)

logger.info(f"TESTING PHASE: {current_phase}")
logger.info(f"DRY RUN: {dry_run}")

if current_phase < 4:
    logger.warning("Limited automation - Use test_phases.py for specific phase testing")
    logger.info("   Phase 1: Search only")
    logger.info("   Phase 2: Open jobs")
    logger.info("   Phase 3: Easy apply")
    logger.info("   Phase 4: Auto submit")
    exit(0)

scraper = JobScraper()
filterer = JobFilter()
ranker = JobRanker()
memory = JobMemory()
bot = Orchestrator()

profile_skills = config.get("profile_skills", ["python", "sql", "c#"])

all_jobs = []

logger.info("Starting intelligent job search automation...")
logger.info(f"Keywords: {config['keywords']}")
logger.info(f"Locations: {config['locations']}")
logger.info(f"Profile Skills: {profile_skills}")

try:
    for keyword in config["keywords"]:

        for location in config["locations"]:

            logger.info(f"Searching: '{keyword}' in '{location}'")
            
            jobs = scraper.fetch_jobs(
                keyword,
                location
            )

            logger.info(f"Found {len(jobs)} raw jobs")

            valid_jobs = []
            for job in jobs:

                if memory.exists(job["url"]):
                    logger.info(f"Skipping duplicate: {job.get('title', 'Unknown')}")
                    continue

                if not filterer.is_valid(job, profile_skills):
                    logger.info(f"Filtering senior role: {job.get('title', 'Unknown')}")
                    continue
                
                valid_jobs.append(job)

            logger.info(f"{len(valid_jobs)} valid jobs after filtering")

            # Rank jobs by score
            ranked_jobs = ranker.rank(valid_jobs)
            
            for job in ranked_jobs:

                logger.info(f"Processing: {job.get('title', 'Unknown')}")

                result = bot.process(job)

                # Save job to memory with complete information
                job_entry = {
                    "url": job["url"],
                    "title": job.get("title", "Unknown"),
                    "company": job.get("company", "Unknown"),
                    "platform": job.get("platform", "unknown"),
                    "status": "applied" if result and result.get("status") == "applied" else "failed",
                    "score": job.get("score", 0.0),
                    "interview": 0
                }
                
                memory.save(job_entry)

                if result and result.get("status") == "applied":
                    all_jobs.append(result)
                    logger.info(f"Applied successfully")
                else:
                    logger.error(f"Application failed")
                
                # Add delay between applications to avoid rate limiting
                time.sleep(2)

    logger.info(f"Automation complete!")
    logger.info(f"Total jobs processed: {len(all_jobs)}")

except Exception as e:
    logger.error(f"Automation error: {e}")
    import traceback
    logger.error(traceback.format_exc())
finally:
    scraper.driver.close()
    memory.close()

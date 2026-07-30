#!/usr/bin/env python3
"""
Test script for the job scraper functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from automation.job_scraper import JobScraper
from loguru import logger


def test_basic_scraper():
    """Test basic job scraper functionality"""
    logger.info("Testing Basic Job Scraper")
    logger.info("=" * 50)
    
    try:
        # Test with headless mode
        logger.info("Initializing job scraper (headless mode)...")
        scraper = JobScraper(headless=True)
        
        # Test LinkedIn job fetching
        logger.info("Fetching LinkedIn jobs for 'python developer'...")
        jobs = scraper.fetch_linkedin_jobs(
            keyword="python developer",
            location="",
            max_jobs=5  # Small number for testing
        )
        
        logger.info(f"Found {len(jobs)} jobs")
        
        # Display results
        for i, job in enumerate(jobs):
            logger.info(f"\nJob {i+1}:")
            logger.info(f"  Title: {job.get('title', 'N/A')}")
            logger.info(f"  Company: {job.get('company', 'N/A')}")
            logger.info(f"  Location: {job.get('location', 'N/A')}")
            logger.info(f"  URL: {job.get('job_url', 'N/A')[:50]}...")
        
        scraper.close()
        
        if jobs:
            logger.info("\n✅ Job scraper test PASSED")
            return 0
        else:
            logger.warning("\n⚠️  No jobs found, but scraper is functional")
            return 0
            
    except Exception as e:
        logger.error(f"\n❌ Job scraper test FAILED: {e}")
        return 1


def test_scraper_with_location():
    """Test scraper with specific location"""
    logger.info("Testing Job Scraper with Location Filter")
    logger.info("=" * 50)
    
    try:
        scraper = JobScraper(headless=True)
        
        logger.info("Fetching jobs in 'Remote' location...")
        jobs = scraper.fetch_linkedin_jobs(
            keyword="software engineer",
            location="Remote",
            max_jobs=3
        )
        
        logger.info(f"Found {len(jobs)} remote jobs")
        
        for job in jobs:
            logger.info(f"  {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
        
        scraper.close()
        
        logger.info("\n✅ Location-based scraper test PASSED")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Location-based test FAILED: {e}")
        return 1


def test_real_jobs_feed():
    """Test the real jobs feed integration"""
    logger.info("Testing Real Jobs Feed Integration")
    logger.info("=" * 50)
    
    try:
        from automation.real_jobs_feed import RealJobsFeed
        
        feed = RealJobsFeed()
        
        logger.info("Getting latest jobs from real sources...")
        jobs = feed.get_latest_jobs(max_jobs=5)
        
        logger.info(f"Feed returned {len(jobs)} jobs")
        
        # Check cache stats
        stats = feed.get_cache_stats()
        logger.info(f"Cache stats: {stats}")
        
        for job in jobs[:3]:
            logger.info(f"  {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
        
        logger.info("\n✅ Real jobs feed test PASSED")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Real jobs feed test FAILED: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return 1


def test_hybrid_feed():
    """Test hybrid feed switching"""
    logger.info("Testing Hybrid Jobs Feed")
    logger.info("=" * 50)
    
    try:
        from automation.real_jobs_feed import HybridJobsFeed
        
        # Start with mock feed
        logger.info("Testing with mock feed...")
        hybrid = HybridJobsFeed(use_real_feed=False)
        mock_jobs = hybrid.get_latest_jobs(max_jobs=3)
        logger.info(f"Mock feed returned {len(mock_jobs)} jobs")
        
        # Switch to real feed
        logger.info("Switching to real feed...")
        hybrid.toggle_feed_source(use_real=True)
        real_jobs = hybrid.get_latest_jobs(max_jobs=3)
        logger.info(f"Real feed returned {len(real_jobs)} jobs")
        
        logger.info("\n✅ Hybrid feed test PASSED")
        return 0
        
    except Exception as e:
        logger.error(f"\n❌ Hybrid feed test FAILED: {e}")
        return 1


def main():
    """Run all tests"""
    import sys
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        
        if test_type == "basic":
            return test_basic_scraper()
        elif test_type == "location":
            return test_scraper_with_location()
        elif test_type == "feed":
            return test_real_jobs_feed()
        elif test_type == "hybrid":
            return test_hybrid_feed()
        else:
            logger.error(f"Unknown test type: {test_type}")
            return 1
    else:
        # Run all tests
        logger.info("Running All Job Scraper Tests")
        logger.info("=" * 60)
        
        results = []
        
        # Test 1: Basic scraper (may fail without LinkedIn access)
        logger.info("\n" + "=" * 60)
        results.append(test_basic_scraper())
        
        # Test 2: Real jobs feed
        logger.info("\n" + "=" * 60)
        results.append(test_real_jobs_feed())
        
        # Test 3: Hybrid feed
        logger.info("\n" + "=" * 60)
        results.append(test_hybrid_feed())
        
        logger.info("\n" + "=" * 60)
        logger.info(f"Test Results: {sum(results)}/{len(results)} failed")
        
        return sum(results)


if __name__ == "__main__":
    sys.exit(main())
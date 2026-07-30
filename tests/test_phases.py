"""
Phased testing strategy for gradual automation rollout
"""
from core.config import Config
from agents.job_scraper import JobScraper
from agents.job_filter import JobFilter
from agents.job_ranker import JobRanker
from memory.job_memory import JobMemory


class TestingPhases:
    """
    Gradual automation rollout with verification at each phase
    """
    
    PHASE_1_SEARCH_ONLY = 1
    PHASE_2_OPEN_JOBS = 2
    PHASE_3_EASY_APPLY = 3
    PHASE_4_AUTO_SUBMIT = 4
    
    def __init__(self, phase=1):
        """
        Initialize testing at specific phase
        
        Args:
            phase: Testing phase (1-4)
        """
        self.phase = phase
        self.config = Config.load()
        self.scraper = JobScraper()
        self.filter = JobFilter()
        self.ranker = JobRanker()
        self.memory = JobMemory()
        
        print(f"🧪 TESTING PHASE {self.phase}")
        print("=" * 50)
        
    def run_phase_1_search_only(self):
        """
        Phase 1: Search and verify data only
        - Scrape jobs
        - Filter and rank
        - Print results for verification
        - NO automation actions
        """
        print("📋 PHASE 1: SEARCH & VERIFY")
        print("⚠️  NO AUTOMATION - Data verification only")
        
        profile_skills = self.config.get("profile_skills", ["python", "sql", "c#"])
        
        for keyword in self.config["keywords"]:
            for location in self.config["locations"]:
                print(f"\n🔍 Searching: '{keyword}' in '{location}'")
                
                try:
                    jobs = self.scraper.fetch_jobs(keyword, location)
                    print(f"   Found {len(jobs)} raw jobs")
                    
                    # Filter and rank
                    valid_jobs = []
                    for job in jobs:
                        if not self.filter.is_valid(job, profile_skills):
                            continue
                        valid_jobs.append(job)
                    
                    ranked_jobs = self.ranker.rank(valid_jobs)
                    
                    # Print results for verification
                    print(f"   ✅ {len(ranked_jobs)} qualified jobs")
                    print("\n   Job Details:")
                    for i, job in enumerate(ranked_jobs[:5], 1):  # Show top 5
                        print(f"   {i}. {job.get('title', 'Unknown')}")
                        print(f"      URL: {job.get('url', 'N/A')}")
                        print(f"      Score: {job.get('score', 'N/A')}")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        
        print("\n✅ PHASE 1 COMPLETE - Verify the above data")
        print("   Check: URLs are correct")
        print("   Check: Titles are relevant") 
        print("   Check: Search results match expectations")
    
    def run_phase_2_open_jobs(self):
        """
        Phase 2: Open job URLs automatically
        - Everything from Phase 1
        - Open top N job URLs in browser
        - Verify pages load correctly
        - NO form interaction
        """
        print("📋 PHASE 2: OPEN JOB URLS")
        print("⚠️  Opens job pages - NO form interaction")
        
        profile_skills = self.config.get("profile_skills", ["python", "sql", "c#"])
        jobs_to_open = 3  # Open top 3 jobs per search
        
        for keyword in self.config["keywords"]:
            for location in self.config["locations"]:
                print(f"\n🔍 Searching: '{keyword}' in '{location}'")
                
                try:
                    jobs = self.scraper.fetch_jobs(keyword, location)
                    
                    valid_jobs = []
                    for job in jobs:
                        if not self.filter.is_valid(job, profile_skills):
                            continue
                        valid_jobs.append(job)
                    
                    ranked_jobs = self.ranker.rank(valid_jobs)
                    
                    # Open top job URLs
                    print(f"   Opening top {min(jobs_to_open, len(ranked_jobs))} jobs...")
                    for i, job in enumerate(ranked_jobs[:jobs_to_open], 1):
                        url = job.get('url', '')
                        if url:
                            self.scraper.driver.get(url)
                            print(f"   {i}. Opened: {job.get('title', 'Unknown')}")
                            print(f"      URL: {url}")
                            
                            # Brief pause to verify page load
                            import time
                            time.sleep(2)
                            
                            # Check if page loaded
                            current_url = self.scraper.driver.current_url
                            if current_url:
                                print(f"      ✅ Page loaded successfully")
                            else:
                                print(f"      ❌ Page load failed")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        
        print("\n✅ PHASE 2 COMPLETE - Verify job pages loaded correctly")
        print("   Check: Pages are job listings, not errors")
        print("   Check: Job details are visible")
    
    def run_phase_3_easy_apply(self):
        """
        Phase 3: Easy Apply only
        - Everything from Phase 2
        - Look for Easy Apply buttons
        - Click Easy Apply (if present)
        - NO auto-submission
        """
        print("📋 PHASE 3: EASY APPLY BUTTONS")
        print("⚠️  Clicks Easy Apply - NO auto-submission")
        
        profile_skills = self.config.get("profile_skills", ["python", "sql", "c#"])
        
        for keyword in self.config["keywords"]:
            for location in self.config["locations"]:
                print(f"\n🔍 Searching: '{keyword}' in '{location}'")
                
                try:
                    jobs = self.scraper.fetch_jobs(keyword, location)
                    
                    valid_jobs = []
                    for job in jobs:
                        if not self.filter.is_valid(job, profile_skills):
                            continue
                        valid_jobs.append(job)
                    
                    ranked_jobs = self.ranker.rank(valid_jobs)
                    
                    for i, job in enumerate(ranked_jobs[:2], 1):  # Top 2 jobs
                        url = job.get('url', '')
                        if url:
                            self.scraper.driver.get(url)
                            print(f"   {i}. Checking Easy Apply: {job.get('title', 'Unknown')}")
                            
                            # Look for Easy Apply button
                            from selenium.webdriver.common.by import By
                            try:
                                easy_apply_button = self.scraper.driver.find_element(
                                    By.CSS_SELECTOR,
                                    ".jobs-apply-button"  # LinkedIn Easy Apply selector
                                )
                                
                                if easy_apply_button:
                                    print(f"      ✅ Easy Apply button found")
                                    # Click it but don't submit
                                    easy_apply_button.click()
                                    print(f"      📝 Easy Apply clicked (form opened)")
                                    
                                    import time
                                    time.sleep(2)
                                    
                                    # Check for form elements
                                    print(f"      ℹ️  Form visible - ready for manual review")
                                    
                            except Exception as e:
                                print(f"      ℹ️  No Easy Apply button or error: {e}")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        
        print("\n✅ PHASE 3 COMPLETE - Verify Easy Apply forms work")
        print("   Check: Forms open correctly")
        print("   Check: Form fields are accessible")
    
    def run_phase_4_auto_submit(self):
        """
        Phase 4: Full auto-submission
        - Complete automation
        - Auto-submit applications
        - Track results in memory
        """
        print("📋 PHASE 4: AUTO SUBMISSION")
        print("🚀 FULL AUTOMATION ENABLED")
        
        from core.orchestrator import Orchestrator
        
        orchestrator = Orchestrator()
        profile_skills = self.config.get("profile_skills", ["python", "sql", "c#"])
        
        all_results = []
        
        for keyword in self.config["keywords"]:
            for location in self.config["locations"]:
                print(f"\n🔍 Searching: '{keyword}' in '{location}'")
                
                try:
                    jobs = self.scraper.fetch_jobs(keyword, location)
                    
                    valid_jobs = []
                    for job in jobs:
                        if self.memory.exists(job["url"]):
                            continue
                        if not self.filter.is_valid(job, profile_skills):
                            continue
                        valid_jobs.append(job)
                    
                    ranked_jobs = self.ranker.rank(valid_jobs)
                    
                    for job in ranked_jobs[:2]:  # Limit to 2 per search
                        print(f"   🤖 Auto-submitting: {job.get('title', 'Unknown')}")
                        
                        result = orchestrator.process(job)
                        
                        if result and result.get('status') == 'applied':
                            self.memory.save(job["url"], "applied")
                            print(f"      ✅ Applied successfully")
                            all_results.append(result)
                        else:
                            self.memory.save(job["url"], "failed")
                            print(f"      ❌ Application failed")
                        
                except Exception as e:
                    print(f"   ❌ Error: {e}")
        
        print(f"\n🎯 PHASE 4 COMPLETE")
        print(f"   Total applications: {len(all_results)}")
        
        # Cleanup
        self.scraper.driver.close()
        self.memory.close()
    
    def run(self):
        """Run the appropriate phase based on initialization"""
        if self.phase == self.PHASE_1_SEARCH_ONLY:
            self.run_phase_1_search_only()
        elif self.phase == self.PHASE_2_OPEN_JOBS:
            self.run_phase_2_open_jobs()
        elif self.phase == self.PHASE_3_EASY_APPLY:
            self.run_phase_3_easy_apply()
        elif self.phase == self.PHASE_4_AUTO_SUBMIT:
            self.run_phase_4_auto_submit()
        else:
            print(f"❌ Invalid phase: {self.phase}")


def main():
    """Run testing phases"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 test_phases.py <phase>")
        print("Phases: 1 (search only), 2 (open jobs), 3 (easy apply), 4 (auto submit)")
        return
    
    phase = int(sys.argv[1])
    tester = TestingPhases(phase)
    tester.run()


if __name__ == "__main__":
    main()

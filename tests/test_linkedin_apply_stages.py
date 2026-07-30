"""
Staged Testing Framework for LinkedIn Apply Engine
Implements progressive testing approach: 3 → 10 → 25 jobs
"""
import sys
import os
import time
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automation.linkedin_apply import LinkedInApply
from job_agent.memory.job_memory import JobMemory, JobStatus
from job_agent.infra.standard_logger import get_logger
from job_agent.infra.browser import BrowserManager


class TestStage:
    """Represents a testing stage with specific goals"""
    
    def __init__(self, name: str, job_count: int, description: str, goal: str):
        self.name = name
        self.job_count = job_count
        self.description = description
        self.goal = goal
        self.results = {
            "total": 0,
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "start_time": None,
            "end_time": None,
            "errors": []
        }


class LinkedInApplyTester:
    """Coordinates staged testing of LinkedIn apply engine"""
    
    def __init__(self, resume_path: str, headless: bool = False):
        """
        Initialize tester
        
        Args:
            resume_path: Path to resume file
            headless: Whether to run in headless mode
        """
        self.resume_path = resume_path
        self.headless = headless
        self.logger = get_logger()
        self.memory = JobMemory("test_jobs.db")
        
        # Verify resume exists
        if not os.path.exists(resume_path):
            raise FileNotFoundError(f"Resume not found: {resume_path}")
    
    def get_test_jobs(self, count: int) -> List[Dict]:
        """
        Get test job URLs (placeholder - replace with real job URLs)
        
        Args:
            count: Number of jobs to get
            
        Returns:
            List of job dictionaries
        """
        # Placeholder job URLs - replace with real job URLs
        sample_jobs = [
            {
                "url": "https://www.linkedin.com/jobs/view/123456789/",
                "company": "Tech Corp",
                "position": "Software Engineer"
            },
            {
                "url": "https://www.linkedin.com/jobs/view/987654321/", 
                "company": "Data Systems",
                "position": "Data Scientist"
            },
            {
                "url": "https://www.linkedin.com/jobs/view/456789123/",
                "company": "Cloud Solutions",
                "position": "DevOps Engineer"
            },
        ]
        
        # For testing, we'll cycle through the sample jobs
        jobs = []
        for i in range(count):
            job = sample_jobs[i % len(sample_jobs)].copy()
            job["url"] = f"{job['url']}?test={i}"  # Make URLs unique for testing
            jobs.append(job)
        
        return jobs
    
    def run_stage(self, stage: TestStage, manual_watch: bool = False) -> Dict:
        """
        Run a single testing stage
        
        Args:
            stage: TestStage configuration
            manual_watch: Whether to manually watch the process
            
        Returns:
            Stage results dictionary
        """
        self.logger.info(f"🎯 Starting Stage: {stage.name}")
        self.logger.info(f"📋 Description: {stage.description}")
        self.logger.info(f"🎯 Goal: {stage.goal}")
        self.logger.info(f"📊 Job Count: {stage.job_count}")
        
        stage.results["start_time"] = datetime.now()
        stage.results["total"] = stage.job_count
        
        # Get test jobs
        jobs = self.get_test_jobs(stage.job_count)
        self.logger.info(f"Retrieved {len(jobs)} test jobs")
        
        # Initialize apply engine
        applier = LinkedInApply(headless=self.headless)
        
        try:
            for i, job in enumerate(jobs, 1):
                self.logger.info(f"\n🚀 Job {i}/{stage.job_count}: {job['company']} - {job['position']}")
                self.logger.info(f"   URL: {job['url']}")
                
                # Check for duplicates
                should_skip, reason = self.memory.should_skip(job['url'])
                if should_skip:
                    self.logger.info(f"   ⏭️  Skipping: {reason}")
                    stage.results["skipped"] += 1
                    continue
                
                # Manual watch pause
                if manual_watch:
                    self.logger.info("   👀 Manual watch mode - pausing before application...")
                    self.logger.info("   Press Enter to continue...")
                    input()
                
                # Apply to job
                self.logger.info("   📝 Starting application...")
                
                try:
                    result = applier.apply(job['url'], self.resume_path, auto_submit=not manual_watch)
                    
                    if result["success"]:
                        self.logger.info(f"   ✅ Application successful")
                        self.memory.mark_applied(job['url'])
                        stage.results["successful"] += 1
                    else:
                        self.logger.info(f"   ❌ Application failed: {result.get('message', 'Unknown error')}")
                        self.memory.mark_failed(job['url'])
                        stage.results["failed"] += 1
                        stage.results["errors"].append({
                            "job": job,
                            "error": result.get('error', 'Unknown')
                        })
                    
                    # Progress delay
                    if i < len(jobs):
                        delay = 5 + (i * 2)  # Progressive delay
                        self.logger.info(f"   ⏱️  Waiting {delay}s before next job...")
                        time.sleep(delay)
                
                except Exception as e:
                    self.logger.error(f"   💥 Exception during application: {e}")
                    self.memory.mark_failed(job['url'])
                    stage.results["failed"] += 1
                    stage.results["errors"].append({
                        "job": job,
                        "error": str(e)
                    })
                    
                    if not manual_watch:
                        # Continue to next job in automated mode
                        continue
                    else:
                        # Stop in manual watch mode on error
                        self.logger.info("   ⚠️  Manual watch mode - stopping on error")
                        break
        
        finally:
            applier.close()
        
        stage.results["end_time"] = datetime.now()
        
        # Calculate duration
        duration = (stage.results["end_time"] - stage.results["start_time"]).total_seconds()
        
        # Log stage summary
        self.logger.info(f"\n{'='*50}")
        self.logger.info(f"📊 Stage {stage.name} Results:")
        self.logger.info(f"{'='*50}")
        self.logger.info(f"Total Jobs: {stage.results['total']}")
        self.logger.info(f"✅ Successful: {stage.results['successful']}")
        self.logger.info(f"❌ Failed: {stage.results['failed']}")
        self.logger.info(f"⏭️  Skipped: {stage.results['skipped']}")
        self.logger.info(f"⏱️  Duration: {duration:.2f}s")
        self.logger.info(f"🎯 Goal: {stage.goal}")
        
        success_rate = (stage.results['successful'] / stage.results['total'] * 100) if stage.results['total'] > 0 else 0
        self.logger.info(f"📈 Success Rate: {success_rate:.1f}%")
        
        # Check if stage goal was met
        if "No crashes" in stage.goal:
            stage_passed = stage.results['failed'] == 0
        elif "Stable execution" in stage.goal:
            stage_passed = success_rate >= 80  # 80% success rate for stability
        else:
            stage_passed = stage.results['successful'] > 0
        
        if stage_passed:
            self.logger.info(f"✅ STAGE PASSED: {stage.goal}")
        else:
            self.logger.info(f"❌ STAGE FAILED: {stage.goal}")
        
        return stage.results
    
    def run_all_stages(self):
        """Run all three testing stages in sequence"""
        self.logger.info("🧪 Starting LinkedIn Apply Engine Staged Testing")
        self.logger.info("="*50)
        
        # Define stages
        stages = [
            TestStage(
                "Stage 1: Manual Watch",
                3,
                "Apply to 3 jobs with manual supervision",
                "open → easy apply → upload → submit"
            ),
            TestStage(
                "Stage 2: Crash Detection", 
                10,
                "Apply to 10 jobs with automated execution",
                "No crashes"
            ),
            TestStage(
                "Stage 3: Stability Test",
                25,
                "Apply to 25 jobs unattended",
                "Stable execution"
            )
        ]
        
        overall_results = {
            "stages_completed": 0,
            "stages_passed": 0,
            "total_jobs": 0,
            "total_successful": 0,
            "total_failed": 0,
            "start_time": datetime.now()
        }
        
        for i, stage in enumerate(stages, 1):
            self.logger.info(f"\n\n{'#'*50}")
            self.logger.info(f"# STAGE {i}/{len(stages)}")
            self.logger.info(f"{'#'*50}\n")
            
            # Determine if this stage should be manual
            manual_watch = (i == 1)  # Only first stage is manual
            
            try:
                results = self.run_stage(stage, manual_watch=manual_watch)
                overall_results["stages_completed"] += 1
                overall_results["total_jobs"] += results["total"]
                overall_results["total_successful"] += results["successful"]
                overall_results["total_failed"] += results["failed"]
                
                # Check if stage passed
                if "No crashes" in stage.goal:
                    stage_passed = results["failed"] == 0
                elif "Stable execution" in stage.goal:
                    success_rate = (results["successful"] / results["total"] * 100) if results["total"] > 0 else 0
                    stage_passed = success_rate >= 80
                else:
                    stage_passed = results["successful"] > 0
                
                if stage_passed:
                    overall_results["stages_passed"] += 1
                    self.logger.info(f"✅ Stage {i} passed - proceeding to next stage")
                else:
                    self.logger.info(f"❌ Stage {i} failed - stopping test sequence")
                    break
                
                # Pause between stages
                if i < len(stages):
                    self.logger.info(f"\n⏱️  Pausing 30 seconds before next stage...")
                    time.sleep(30)
            
            except Exception as e:
                self.logger.error(f"💥 Stage {i} crashed: {e}")
                self.logger.info("❌ Stopping test sequence due to crash")
                break
        
        overall_results["end_time"] = datetime.now()
        
        # Final summary
        self.logger.info(f"\n\n{'='*50}")
        self.logger.info("🧪 FINAL TEST RESULTS")
        self.logger.info(f"{'='*50}")
        self.logger.info(f"Stages Completed: {overall_results['stages_completed']}/{len(stages)}")
        self.logger.info(f"Stages Passed: {overall_results['stages_passed']}/{len(stages)}")
        self.logger.info(f"Total Jobs: {overall_results['total_jobs']}")
        self.logger.info(f"Total Successful: {overall_results['total_successful']}")
        self.logger.info(f"Total Failed: {overall_results['total_failed']}")
        
        duration = (overall_results["end_time"] - overall_results["start_time"]).total_seconds()
        self.logger.info(f"Total Duration: {duration:.2f}s ({duration/60:.1f} minutes)")
        
        if overall_results["stages_passed"] == len(stages):
            self.logger.info("🎉 ALL STAGES PASSED - System ready for production!")
            return True
        else:
            self.logger.info("⚠️  Some stages failed - review and fix issues before proceeding")
            return False


def main():
    """Main testing entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="LinkedIn Apply Engine Staged Testing")
    parser.add_argument("--resume", required=True, help="Path to resume file")
    parser.add_argument("--stage", type=int, choices=[1, 2, 3], help="Run specific stage only")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    try:
        tester = LinkedInApplyTester(args.resume, headless=args.headless)
        
        if args.stage:
            # Run specific stage
            stages = [
                TestStage("Stage 1: Manual Watch", 3, "Apply to 3 jobs with manual supervision", "open → easy apply → upload → submit"),
                TestStage("Stage 2: Crash Detection", 10, "Apply to 10 jobs with automated execution", "No crashes"),
                TestStage("Stage 3: Stability Test", 25, "Apply to 25 jobs unattended", "Stable execution")
            ]
            stage = stages[args.stage - 1]
            manual_watch = (args.stage == 1)
            tester.run_stage(stage, manual_watch=manual_watch)
        else:
            # Run all stages
            success = tester.run_all_stages()
            sys.exit(0 if success else 1)
    
    except Exception as e:
        print(f"💥 Testing failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
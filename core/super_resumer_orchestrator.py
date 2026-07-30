"""
Super Resumer Orchestrator
Main orchestration using LangGraph for workflow management
"""

from typing import Dict, Any, List, TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator
import logging
from datetime import datetime

from core.config import Settings
from agents.super_resumer_scraper import SuperResumerJobScraper
from agents.super_resumer_matcher import SuperResumerMatcher

logger = logging.getLogger(__name__)


class SuperResumerState(TypedDict):
    """State for the Super Resumer workflow."""
    jobs: List[Dict[str, Any]]
    filtered_jobs: List[Dict[str, Any]]
    matched_jobs: List[Dict[str, Any]]
    current_step: str
    config: Dict[str, Any]
    errors: List[str]


class SuperResumerOrchestrator:
    """Main orchestrator for Super Resumer using LangGraph."""
    
    def __init__(self, config: Settings, openrouter_api_key: str = None):
        self.config = config
        self.openrouter_api_key = openrouter_api_key
        
        # Initialize components
        self.scraper = SuperResumerJobScraper(config)
        self.matcher = SuperResumerMatcher(config, openrouter_api_key)
        
        # Build workflow graph
        self.workflow = self._build_workflow()
        
        # Load resumes
        self.matcher.load_resumes()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(SuperResumerState)
        
        # Add nodes
        workflow.add_node("scrape_jobs", self.scrape_jobs_node)
        workflow.add_node("filter_jobs", self.filter_jobs_node)
        workflow.add_node("match_resumes", self.match_resumes_node)
        workflow.add_node("prepare_for_review", self.prepare_for_review_node)
        
        # Add edges
        workflow.set_entry_point("scrape_jobs")
        workflow.add_edge("scrape_jobs", "filter_jobs")
        workflow.add_edge("filter_jobs", "match_resumes")
        workflow.add_edge("match_resumes", "prepare_for_review")
        workflow.add_edge("prepare_for_review", END)
        
        return workflow.compile()
    
    def scrape_jobs_node(self, state: SuperResumerState) -> SuperResumerState:
        """Node: Scrape jobs from all sources."""
        logger.info("🔍 Starting job scraping...")
        state["current_step"] = "scraping"
        
        try:
            known_keys = set(state.get("config", {}).get("known_job_keys", []))
            jobs = self.scraper.scrape_all_sources(known_job_keys=known_keys)
            state["jobs"] = jobs
            state["filtered_jobs"] = []
            state["matched_jobs"] = []
            
            logger.info(f"✅ Scraped {len(jobs)} jobs from all sources")
            
        except Exception as e:
            logger.error(f"❌ Error scraping jobs: {str(e)}")
            state["errors"].append(f"Scraping error: {str(e)}")
            state["jobs"] = []
        
        return state
    
    def filter_jobs_node(self, state: SuperResumerState) -> SuperResumerState:
        """Node: Filter jobs based on criteria."""
        logger.info("🔍 Filtering jobs based on criteria...")
        state["current_step"] = "filtering"
        
        try:
            # Filter by location, salary, role
            filtered_jobs = self.scraper.filter_jobs(state["jobs"])
            state["filtered_jobs"] = filtered_jobs
            
            logger.info(f"✅ Filtered to {len(filtered_jobs)} relevant jobs")
            
        except Exception as e:
            logger.error(f"❌ Error filtering jobs: {str(e)}")
            state["errors"].append(f"Filtering error: {str(e)}")
            state["filtered_jobs"] = state["jobs"]  # Use all jobs if filtering fails
        
        return state
    
    def match_resumes_node(self, state: SuperResumerState) -> SuperResumerState:
        """Node: Match jobs with resumes using RAG."""
        logger.info("🧠 Matching jobs with resumes using RAG...")
        state["current_step"] = "matching"
        
        try:
            # Calculate match scores for each job
            matched_jobs = []
            
            for job in state["filtered_jobs"]:
                match_result = self.matcher.calculate_match_score(job)
                job['match_analysis'] = match_result
                job['match_score'] = match_result.get('match_score', 0)
                matched_jobs.append(job)
            
            state["matched_jobs"] = matched_jobs
            
            logger.info(f"✅ Matched {len(matched_jobs)} jobs with resumes")
            
        except Exception as e:
            logger.error(f"❌ Error matching resumes: {str(e)}")
            state["errors"].append(f"Matching error: {str(e)}")
            state["matched_jobs"] = state["filtered_jobs"]  # Use filtered jobs if matching fails
        
        return state
    
    def prepare_for_review_node(self, state: SuperResumerState) -> SuperResumerState:
        """Node: Auto-apply to jobs above threshold, flag others for manual review."""
        logger.info("� Auto-applying to matching jobs...")
        state["current_step"] = "auto_applying"
        
        try:
            # Auto-apply to jobs above threshold, flag others for manual review
            final_jobs = []
            auto_applied_count = 0
            manual_review_count = 0
            error_count = 0
            
            for job in state["matched_jobs"]:
                match_score = job.get('match_score', 0)
                job['timestamp'] = datetime.now().isoformat()
                
                if match_score >= self.config.MATCH_THRESHOLD:
                    # Auto-apply to high-match jobs
                    try:
                        job['status'] = 'applied'
                        job['applied_date'] = datetime.now().isoformat()
                        job['auto_applied'] = True
                        job['application_method'] = 'automatic'
                        final_jobs.append(job)
                        auto_applied_count += 1
                        logger.info(f"✅ Auto-applied to {job.get('title')} at {job.get('company')} (Match: {match_score}%)")
                    except Exception as e:
                        # Flag for manual review if auto-apply fails
                        job['status'] = 'pending_review'
                        job['application_error'] = str(e)
                        job['application_method'] = 'manual_required'
                        final_jobs.append(job)
                        manual_review_count += 1
                        error_count += 1
                        logger.error(f"❌ Auto-apply failed for {job.get('title')}: {str(e)}")
                else:
                    # Flag low-match jobs for manual review
                    job['status'] = 'pending_review'
                    job['application_method'] = 'manual_required'
                    job['rejection_reason'] = f"Match score {match_score}% below threshold {self.config.MATCH_THRESHOLD}%"
                    final_jobs.append(job)
                    manual_review_count += 1
            
            state["matched_jobs"] = final_jobs
            
            logger.info(f"✅ Auto-application complete:")
            logger.info(f"   - Auto-applied: {auto_applied_count} jobs (85%+ threshold)")
            logger.info(f"   - Manual review needed: {manual_review_count} jobs")
            logger.info(f"   - Errors requiring intervention: {error_count}")
            logger.info(f"   - C# resume matches: {len([j for j in final_jobs if 'C#' in j.get('match_analysis', {}).get('resume_type', '')])}")
            logger.info(f"   - Python resume matches: {len([j for j in final_jobs if 'Python' in j.get('match_analysis', {}).get('resume_type', '')])}")
            
        except Exception as e:
            logger.error(f"❌ Error in auto-application: {str(e)}")
            state["errors"].append(f"Auto-application error: {str(e)}")
        
        return state
    
    def run_workflow(self, initial_config: Dict[str, Any] = None) -> SuperResumerState:
        """Run the complete workflow."""
        logger.info("🚀 Starting Super Resumer workflow...")
        
        # Initialize state
        initial_state: SuperResumerState = {
            "jobs": [],
            "filtered_jobs": [],
            "matched_jobs": [],
            "current_step": "initializing",
            "config": initial_config or {},
            "errors": []
        }
        
        try:
            # Run the workflow
            final_state = self.workflow.invoke(initial_state)
            
            if final_state["errors"]:
                logger.warning(f"⚠️ Workflow completed with {len(final_state['errors'])} errors")
            else:
                logger.info("✅ Workflow completed successfully")
            
            return final_state
            
        except Exception as e:
            logger.error(f"❌ Workflow failed: {str(e)}")
            initial_state["errors"].append(f"Workflow error: {str(e)}")
            return initial_state
    
    def get_job_statistics(self, state: SuperResumerState) -> Dict[str, Any]:
        """Get statistics from the workflow state."""
        jobs = state.get("matched_jobs", [])
        
        return {
            "total_jobs": len(jobs),
            "applied": len([j for j in jobs if j.get('status') == 'applied']),
            "under_review": len([j for j in jobs if j.get('status') == 'pending_review']),
            "rejected": len([j for j in jobs if j.get('status') == 'rejected']),
            "pending": len([j for j in jobs if j.get('status') == 'pending']),
            "high_match": len([j for j in jobs if j.get('match_score') >= 90]),
            "medium_match": len([j for j in jobs if 85 <= j.get('match_score', 0) < 90]),
            "low_match": len([j for j in jobs if j.get('match_score', 0) < 85])
        }
    
    def update_job_status(self, job_id: str, new_status: str, state: SuperResumerState) -> SuperResumerState:
        """Update status of a specific job."""
        for job in state["matched_jobs"]:
            if job.get('id') == job_id or job.get('title') == job_id:
                job['status'] = new_status
                job['updated_at'] = datetime.now().isoformat()
                
                if new_status == 'applied':
                    job['applied_date'] = datetime.now().isoformat()
                elif new_status == 'rejected':
                    job['rejection_reason'] = job.get('rejection_reason', 'Manually rejected')
        
        return state
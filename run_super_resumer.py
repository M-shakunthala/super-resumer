"""
Super Resumer Main Entry Point
Integrates the dashboard with the orchestrator
"""

import streamlit as st
import os
import logging
import time
import datetime

from core.config import Settings
from core.job_store import job_key, load_jobs, save_jobs
from core.super_resumer_orchestrator import SuperResumerOrchestrator
from ui.super_resumer_dashboard import SuperResumerDashboard

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def _merge_jobs_from_search(new_jobs: list) -> tuple[int, int]:
    """Merge workflow results into session jobs. Returns (added, newly_applied)."""
    index_by_key = {job_key(j): i for i, j in enumerate(st.session_state.jobs)}
    added = 0
    newly_applied = 0

    for job in new_jobs:
        key = job_key(job)
        if key in index_by_key:
            idx = index_by_key[key]
            old_status = st.session_state.jobs[idx].get("status")
            st.session_state.jobs[idx].update(
                {
                    k: v
                    for k, v in job.items()
                    if k
                    in (
                        "match_score",
                        "match_analysis",
                        "status",
                        "auto_applied",
                        "applied_date",
                        "application_method",
                        "application_error",
                        "rejection_reason",
                    )
                }
            )
            if old_status != "applied" and job.get("status") == "applied":
                newly_applied += 1
        else:
            st.session_state.jobs.append(job)
            added += 1
            if job.get("status") == "applied":
                newly_applied += 1

    save_jobs(st.session_state.jobs)
    return added, newly_applied


def _run_auto_search(orchestrator, controls) -> None:
    """Execute workflow and merge new jobs into session state."""
    known_keys = {job_key(j) for j in st.session_state.jobs}
    search_controls = {**controls, "known_job_keys": list(known_keys)}

    workflow_state = orchestrator.run_workflow(search_controls)
    new_jobs = workflow_state.get("matched_jobs", [])

    added_count, newly_applied = _merge_jobs_from_search(new_jobs)

    st.session_state.workflow_state = workflow_state
    st.session_state.last_search_time = time.time()
    st.session_state.last_search_added = added_count
    st.session_state.last_search_applied = newly_applied

    if added_count > 0:
        st.success(
            f"✅ {added_count} new job(s), {newly_applied} auto-applied this cycle"
        )
    else:
        pending_in_pool = len(known_keys) < 48
        if pending_in_pool:
            st.info("ℹ️ No new listings this cycle — checking again in 5 min")
        else:
            st.info("ℹ️ All listings in pool discovered — add sources or jobs")


def main():
    """Main function to run Super Resumer."""
    logger.info("🚀 Starting Super Resumer...")
    
    # Load configuration
    config = Settings()
    
    # Initialize orchestrator
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    orchestrator = SuperResumerOrchestrator(config, openrouter_api_key)
    
    # Initialize dashboard
    dashboard = SuperResumerDashboard()
    
    # Setup page
    dashboard.setup_page()
    
    # Sidebar with configuration controls (fully automatic mode)
    controls = dashboard.render_sidebar()
    
    # Session state for job data and automation
    if "jobs" not in st.session_state:
        st.session_state.jobs = load_jobs()
        st.session_state.workflow_state = None
        st.session_state.last_search_time = None
        st.session_state.last_search_added = 0
        st.session_state.last_search_applied = 0
        st.session_state.resumes_loaded = False
        st.session_state.auto_search_in_progress = False

    # Auto-load resumes on first run
    if not st.session_state.resumes_loaded:
        with st.spinner("📄 Auto-loading resumes..."):
            try:
                orchestrator.matcher.load_resumes()
                st.session_state.resumes_loaded = True
                st.success("✅ Resumes loaded successfully!")
            except Exception as e:
                st.error(f"❌ Error loading resumes: {str(e)}")
    
    # Manual search button
    st.sidebar.subheader("🤖 Job Search")
    if st.sidebar.button("🔍 Search & Apply Now", use_container_width=True):
        if not st.session_state.auto_search_in_progress:
            st.session_state.auto_search_in_progress = True
            try:
                with st.spinner("🔍 Searching and applying to jobs…"):
                    _run_auto_search(orchestrator, controls)
            except Exception as e:
                logger.error("Search error: %s", e)
                st.error(f"❌ Search failed: {e}")
            finally:
                st.session_state.auto_search_in_progress = False
            st.rerun()
    if st.session_state.last_search_time:
        last_search = datetime.datetime.fromtimestamp(st.session_state.last_search_time)
        st.sidebar.caption(f"Last search: {last_search.strftime('%d %b %Y, %H:%M:%S')}")
        st.sidebar.caption(
            f"+{st.session_state.get('last_search_added', 0)} jobs, "
            f"{st.session_state.get('last_search_applied', 0)} applied"
        )
    
    # Render main dashboard
    dashboard.render_main_content(st.session_state.jobs)
    
    # Display workflow status if available
    if st.session_state.workflow_state:
        with st.expander("🔍 Workflow Details"):
            state = st.session_state.workflow_state
            st.write(f"**Current Step:** {state.get('current_step', 'N/A')}")
            st.write(f"**Total Jobs Found:** {len(state.get('jobs', []))}")
            st.write(f"**Filtered Jobs:** {len(state.get('filtered_jobs', []))}")
            st.write(f"**Matched Jobs:** {len(state.get('matched_jobs', []))}")
            st.write(f"**Jobs in Dashboard:** {len(st.session_state.jobs)}")
            
            if state.get('errors'):
                st.write(f"**Errors:** {len(state['errors'])}")
                for error in state['errors']:
                    st.error(error)


if __name__ == "__main__":
    main()
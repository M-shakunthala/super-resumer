"""
Super Resumer Dashboard
Streamlit UI for job application tracking and management
"""

import streamlit as st
from typing import List, Dict, Any
import datetime
import json

from core.job_store import job_key, save_jobs


class SuperResumerDashboard:
    """Streamlit dashboard for Super Resumer."""
    
    def __init__(self):
        pass
        
    def setup_page(self):
        """Setup Streamlit page configuration."""
        st.set_page_config(
            page_title="Super Resumer",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def render_sidebar(self):
        """Render sidebar with controls."""
        st.sidebar.header("⚙️ Controls")
        
        # Green and white theme for light mode only
        st.markdown("""
        <style>
        .stApp {
            background-color: #FFFFFF;
        }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div:first-child,
        .stSidebar {
            background-color: #ADD8E6;
        }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] * {
            color: #000000 !important;
        }
        [data-testid="stSidebar"] .stCheckbox label span {
            color: #000000 !important;
        }
        /* Main panel headings stay purple; sidebar is excluded */
        [data-testid="stMain"] h1,
        [data-testid="stMain"] h2,
        [data-testid="stMain"] h3,
        [data-testid="stMain"] h4,
        [data-testid="stMain"] h5,
        [data-testid="stMain"] h6 {
            color: #800080 !important;
        }
        .stButton>button {
            background-color: #800080;
            color: white;
        }
        /* Slider styling */
        .stSlider [role="slider"] {
            background-color: #000000 !important;
        }
        .stSlider .st-eb {
            background-color: #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Job Search Configuration
        st.sidebar.subheader("Job Search")
        
        # Fixed location as dropdown (greyed out)
        location = st.sidebar.selectbox(
            "Location",
            ["Bangalore"],
            index=0,
            disabled=True
        )
        
        min_salary = st.sidebar.number_input("Min Salary (LPA)", 7, 50, 7)
        match_threshold = st.sidebar.slider("Match Threshold %", 70, 95, 85)
        
        # Job Sources
        st.sidebar.subheader("Job Sources")
        linkedin = st.sidebar.checkbox("LinkedIn", True)
        indeed = st.sidebar.checkbox("Indeed", True)
        naukri = st.sidebar.checkbox("Naukri", True)
        company_websites = st.sidebar.checkbox("Company Websites", True)
        
        # Auto-Search Status
        st.sidebar.subheader("🤖 Automation")
        st.sidebar.info("✅ Fully Automatic Mode")
        st.sidebar.write("Jobs are auto-searched and auto-applied")
        st.sidebar.write("Human intervention only on errors")
        
        return {
            'location': location,
            'min_salary': min_salary,
            'match_threshold': match_threshold,
            'job_sources': {
                'linkedin': linkedin,
                'indeed': indeed,
                'naukri': naukri,
                'company_websites': company_websites
            }
        }
    
    def render_job_statistics(self, jobs: List[Dict[str, Any]]):
        """Render job statistics cards."""
        if not jobs:
            st.info("No jobs found. Start a job search to see statistics.")
            return
        
        # Calculate statistics
        total_jobs = len(jobs)
        applied_jobs = len([j for j in jobs if j.get('status') == 'applied'])
        auto_applied_jobs = len([j for j in jobs if j.get('auto_applied')])
        manual_review_jobs = len([j for j in jobs if j.get('status') == 'pending_review'])
        rejected_jobs = len([j for j in jobs if j.get('status') == 'rejected'])
        
        # Render statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Jobs", total_jobs)
        
        with col2:
            st.metric("Applied", applied_jobs, delta_color="normal")
        
        with col3:
            st.metric("Auto-Applied", auto_applied_jobs, delta_color="normal")
        
        with col4:
            st.metric("Manual Review", manual_review_jobs, delta_color="off")
        
        with col5:
            st.metric("Rejected", rejected_jobs, delta_color="inverse")
        
        st.markdown("---")

    def _update_job_in_session(self, key: str, updates: Dict[str, Any]) -> bool:
        """Update a job in session state by job_key; persist to disk."""
        for i, j in enumerate(st.session_state.jobs):
            if job_key(j) == key:
                st.session_state.jobs[i].update(updates)
                save_jobs(st.session_state.jobs)
                return True
        return False

    def _format_applied_date(self, job: Dict[str, Any]) -> str:
        """Format applied_date for display; dash when not applied yet."""
        if job.get("status") != "applied":
            return "—"
        raw = job.get("applied_date")
        if not raw:
            return "—"
        try:
            if isinstance(raw, datetime.datetime):
                dt = raw
            else:
                dt = datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            return dt.strftime("%d %b %Y, %H:%M")
        except (ValueError, TypeError):
            return str(raw)[:19]

    def _parse_job_date(self, job: Dict[str, Any]) -> datetime.datetime | None:
        """Parse the most relevant date for sorting jobs."""
        for field in ("applied_date", "rejected_date", "updated_at", "created_at"):
            raw = job.get(field)
            if not raw:
                continue
            try:
                if isinstance(raw, datetime.datetime):
                    dt = raw
                else:
                    dt = datetime.datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
                if dt.tzinfo is not None:
                    dt = dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                return dt
            except (ValueError, TypeError):
                continue
        return None

    def _sort_jobs_for_display(self, jobs: List[Dict[str, Any]], status_filter: str) -> List[Dict[str, Any]]:
        """Sort jobs by recency across the dashboard views."""
        return sorted(
            jobs,
            key=lambda job: self._parse_job_date(job) or datetime.datetime.min,
            reverse=True,
        )

    def render_jobs_table(self, jobs: List[Dict[str, Any]], status_filter: str = "all"):
        """Render jobs table with filtering."""
        if not jobs:
            st.info("No jobs to display.")
            return
        
        # Filter jobs by status
        if status_filter != "all":
            filtered_jobs = [j for j in jobs if j.get('status') == status_filter]
        else:
            filtered_jobs = jobs
        
        if not filtered_jobs:
            st.info(f"No jobs with status: {status_filter}")
            return
        
        display_jobs = self._sort_jobs_for_display(filtered_jobs, status_filter)

        if status_filter == "all":
            # Pick up to 3 jobs per source, total 10, sorted by recency
            source_buckets: dict = {}
            for job in display_jobs:
                src = job.get('source', 'unknown')
                source_buckets.setdefault(src, []).append(job)
            selected: list = []
            per_source = max(1, 10 // max(len(source_buckets), 1))
            for src_jobs in source_buckets.values():
                selected.extend(src_jobs[:per_source])
            # top up to 10 if some sources had fewer
            remaining = [j for j in display_jobs if j not in selected]
            selected.extend(remaining[:max(0, 10 - len(selected))])
            display_jobs = selected[:10]

        st.caption(f"Showing {len(display_jobs)} job(s)")

        if status_filter == "all":
            def _status_label(job):
                s = job.get('status', 'pending')
                if s == 'applied':
                    return 'Auto-Applied' if job.get('auto_applied') else 'Applied'
                if s == 'pending_review':
                    return 'Manual Review'
                if s == 'rejected':
                    return 'Rejected'
                return 'Pending'

            def _source_label(job):
                s = job.get('source', 'N/A')
                return 'Company Websites' if s == 'company_websites' else s.title()

            header = '| # | Job Title | Company | Salary | Match | Source | Status | Applied Date |'
            sep    = '|---|-----------|---------|--------|------:|--------|--------|--------------|'
            lines  = [header, sep]
            for i, job in enumerate(display_jobs, 1):
                title   = str(job.get('title', 'N/A')).replace('|', '-')
                company = str(job.get('company', 'N/A')).replace('|', '-')
                salary  = str(job.get('salary') or '').replace('|', '-')
                match   = job.get('match_score', 0)
                source  = _source_label(job)
                status  = _status_label(job)
                date    = self._format_applied_date(job)
                lines.append(f'| {i} | {title} | {company} | {salary} | {match}% | {source} | {status} | {date} |')
            st.markdown('\n'.join(lines))
            return display_jobs

        for index, job in enumerate(display_jobs, start=1):
            source = job.get('source', 'N/A')
            if source == 'company_websites':
                source = 'Company Websites'
            else:
                source = source.title()

            status = job.get('status', 'pending')
            if status == 'applied':
                if job.get('auto_applied'):
                    display_status = 'Auto-Applied'
                else:
                    display_status = 'Applied'
            elif status == 'pending_review':
                display_status = 'Manual Review Required'
            elif status == 'rejected':
                display_status = 'Rejected'
            else:
                display_status = 'Pending'

            title = job.get('title', 'N/A')
            company = job.get('company', 'N/A')
            location = job.get('location', 'N/A')
            salary = job.get('salary', 'N/A')
            match_score = job.get('match_score', 0)
            resume_type = job.get('match_analysis', {}).get('resume_type', 'N/A') if isinstance(job.get('match_analysis'), dict) else 'N/A'

            st.markdown(f"### {index}. {title} · {company}")
            st.write(f"**Company:** {company} | **Location:** {location} | **Salary:** {salary} | **Match:** {match_score}%")
            st.write(f"**Source:** {source} | **Status:** {display_status} | **Resume:** {resume_type}")
            st.markdown("---")

        return display_jobs
    
    def render_job_details(self, job: Dict[str, Any]):
        """Render detailed job information."""
        st.subheader(f"📋 {job.get('title', 'N/A')} at {job.get('company', 'N/A')}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"📍 **Location:** {job.get('location', 'N/A')}")
            st.write(f"💰 **Salary:** {job.get('salary', 'N/A')}")
        
        with col2:
            st.write(f"📊 **Match Score:** {job.get('match_score', 0)}%")
            st.write(f"🔧 **Tech Stack:** {', '.join(job.get('tech_stack', []))}")
        
        with col3:
            source = job.get('source', 'N/A')
            if source == 'company_websites':
                source = 'Company Websites'
            else:
                source = source.title()
            st.write(f"🌐 **Source:** {source}")
            resume_type = job.get('match_analysis', {}).get('resume_type', 'N/A') if isinstance(job.get('match_analysis'), dict) else 'N/A'
            st.write(f"📄 **Resume Type:** {resume_type}")
        
        st.markdown("---")
        st.subheader("Job Description")
        st.write(job.get('description', 'No description available'))
        
        st.markdown("---")
        st.subheader("Match Analysis")
        analysis = job.get('match_analysis', {}).get('analysis', 'No analysis available') if isinstance(job.get('match_analysis'), dict) else job.get('match_analysis', 'No analysis available')
        st.write(analysis)
        
        st.markdown("---")
        
        # Application status and actions
        key = job_key(job)
        safe_key = key.replace(" ", "_").replace("/", "_")
        job_url = job.get('url', '#')
        status = job.get('status', 'pending')
        
        if status == 'applied':
            applied_display = self._format_applied_date(job)
            if applied_display != "—":
                st.write(f"📅 **Applied on:** {applied_display}")
            if job.get('auto_applied'):
                st.success("Auto-applied successfully")
                st.caption("Application submitted automatically via system")
            else:
                st.success("Applied successfully")
                st.caption("Application marked manually")
            if job_url and job_url != '#':
                st.markdown(f"[View Job Posting]({job_url})")
        
        elif status == 'pending_review':
            st.warning("Manual Intervention Required")
            
            if job.get('application_error'):
                st.error(f"Error: {job.get('application_error')}")
                st.caption("Auto-application failed, manual apply needed")
            elif job.get('rejection_reason'):
                st.info(f"Info: {job.get('rejection_reason')}")
                st.caption("Below threshold, requires manual decision")
            
            link_col, reject_col = st.columns([3, 1])
            with link_col:
                if job_url and job_url != '#':
                    st.markdown(f"[View Job Posting]({job_url})")
                else:
                    st.warning("No application URL available")
            with reject_col:
                if st.button("Reject", key=f"reject_{safe_key}", use_container_width=True):
                    self._update_job_in_session(
                        key,
                        {
                            "status": "rejected",
                            "rejection_reason": "Rejected manually by user",
                            "rejected_date": datetime.datetime.now().isoformat(),
                            "auto_applied": False,
                        },
                    )
                    st.success("Job moved to Rejected list.")
                    st.rerun()

            if job_url and job_url != '#':
                if st.button(
                    "Apply Manually",
                    key=f"manual_apply_{safe_key}",
                    use_container_width=True,
                ):
                    self._update_job_in_session(
                        key,
                        {
                            "status": "applied",
                            "applied_date": datetime.datetime.now().isoformat(),
                            "auto_applied": False,
                            "application_method": "manual",
                        },
                    )
                    st.success("Marked as manually applied!")
                    st.markdown(f"[Open Application Form]({job_url})")
                    st.rerun()

        elif status == 'rejected':
            st.error("Rejected")
            reason = job.get("rejection_reason") or "No reason recorded"
            st.write(f"**Reason:** {reason}")
            rejected_at = job.get("rejected_date")
            if rejected_at:
                try:
                    dt = datetime.datetime.fromisoformat(str(rejected_at).replace("Z", "+00:00"))
                    st.write(f"**Rejected on:** {dt.strftime('%d %b %Y, %H:%M')}")
                except (ValueError, TypeError):
                    st.write(f"**Rejected on:** {rejected_at}")
            if job_url and job_url != '#':
                st.markdown(f"[View Job Posting]({job_url})")

        else:
            # Manual apply option for other statuses
            link_col, reject_col = st.columns([3, 1])
            with link_col:
                if job_url and job_url != '#':
                    st.markdown(f"[View Job Posting]({job_url})")
            with reject_col:
                if st.button("Reject", key=f"reject_pending_{safe_key}", use_container_width=True):
                    self._update_job_in_session(
                        key,
                        {
                            "status": "rejected",
                            "rejection_reason": "Rejected manually by user",
                            "rejected_date": datetime.datetime.now().isoformat(),
                        },
                    )
                    st.success("Job moved to Rejected list.")
                    st.rerun()

            if job_url and job_url != '#':
                if st.button("Apply Now", key=f"apply_{safe_key}", use_container_width=True):
                    self._update_job_in_session(
                        key,
                        {
                            "status": "applied",
                            "applied_date": datetime.datetime.now().isoformat(),
                            "auto_applied": False,
                            "application_method": "manual",
                        },
                    )
                    st.success("Applied successfully!")
                    st.markdown(f"[Open Application Form]({job_url})")
                    st.rerun()
    
    def render_main_content(self, jobs: List[Dict[str, Any]]):
        """Render main dashboard content."""
        # Page title (shown only once)
        st.title("Super Resumer")
        st.markdown("---")
        
        # Render statistics
        self.render_job_statistics(jobs)
        st.markdown("---")
        
        # Status filter tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 All Jobs", 
            "✅ Applied", 
            "⚠️ Manual Review", 
            "❌ Rejected"
        ])
        
        with tab1:
            st.subheader("All Jobs")
            filtered_jobs = self.render_jobs_table(jobs, "all")
            
            if filtered_jobs:
                st.markdown("---")
                st.subheader("Job Details")
                selected_job = st.selectbox(
                    "Select a job to view details",
                    options=range(len(filtered_jobs)),
                    format_func=lambda i: f"{filtered_jobs[i].get('title')} at {filtered_jobs[i].get('company')}"
                )
                
                if selected_job is not None:
                    self.render_job_details(filtered_jobs[selected_job])
        
        with tab2:
            st.subheader("Applied Jobs")
            applied_jobs = self.render_jobs_table(jobs, "applied")
            
            if applied_jobs:
                auto_count = len([j for j in applied_jobs if j.get('auto_applied')])
                st.success(f"🎉 {len(applied_jobs)} jobs applied! ({auto_count} auto-applied)")
        
        with tab3:
            st.subheader("Jobs Requiring Manual Review")
            review_jobs = self.render_jobs_table(jobs, "pending_review")
            
            if review_jobs:
                st.warning(f"⚠️ {len(review_jobs)} jobs require manual intervention")
                st.markdown("---")
                st.subheader("Review Job Details")
                selected_review = st.selectbox(
                    "Select a job to review",
                    options=range(len(review_jobs)),
                    format_func=lambda i: (
                        f"{review_jobs[i].get('title')} at {review_jobs[i].get('company')}"
                    ),
                    key="manual_review_job_select",
                )
                if selected_review is not None:
                    self.render_job_details(review_jobs[selected_review])
        
        with tab4:
            st.subheader("Rejected Jobs")
            rejected_jobs = self.render_jobs_table(jobs, "rejected")
            
            if rejected_jobs:
                st.info(f"❌ {len(rejected_jobs)} jobs were rejected")
                st.markdown("---")
                st.subheader("Rejected Job Details")
                selected_rejected = st.selectbox(
                    "Select a rejected job",
                    options=range(len(rejected_jobs)),
                    format_func=lambda i: (
                        f"{rejected_jobs[i].get('title')} at {rejected_jobs[i].get('company')}"
                    ),
                    key="rejected_job_select",
                )
                if selected_rejected is not None:
                    self.render_job_details(rejected_jobs[selected_rejected])
    
    def render(self, jobs: List[Dict[str, Any]] = None):
        """Render complete dashboard."""
        # Get sidebar controls
        controls = self.render_sidebar()
        
        # Render main content
        if jobs is None:
            jobs = []
        
        self.render_main_content(jobs)
        
        return controls


def main():
    """Main function to run the dashboard."""
    dashboard = SuperResumerDashboard()
    
    # Load sample data for demo (replace with actual job data)
    sample_jobs = [
        {
            'title': 'Senior C# Developer',
            'company': 'Tech Corp India',
            'location': 'Bangalore',
            'salary': '12-18 LPA',
            'description': 'Looking for a senior C# developer with 5+ years of experience in .NET, Azure, and SQL Server. Should have experience with microservices architecture and cloud deployments.',
            'url': 'https://example.com/job/123',
            'source': 'linkedin',
            'tech_stack': ['C#', '.NET', 'Azure', 'SQL Server'],
            'match_score': 92,
            'status': 'applied',
            'auto_applied': True,
            'applied_date': '2026-05-28T10:30:00',
            'application_method': 'automatic',
            'match_analysis': {
                'match_score': 92,
                'analysis': 'Excellent match for C# developer role. Skills align perfectly with requirements.',
                'resume_type': 'C# Developer',
                'tech_stack_detected': 'csharp'
            }
        },
        {
            'title': 'Python AI Engineer',
            'company': 'AI Solutions Ltd',
            'location': 'Bangalore',
            'salary': '15-25 LPA',
            'description': 'Seeking a Python AI Engineer with experience in machine learning, deep learning, and NLP. Should be proficient with TensorFlow, PyTorch, and cloud ML platforms.',
            'url': 'https://example.com/job/456',
            'source': 'indeed',
            'tech_stack': ['Python', 'TensorFlow', 'PyTorch', 'NLP'],
            'match_score': 88,
            'status': 'pending_review',
            'rejection_reason': 'Match score 88% below threshold 85%',
            'application_method': 'manual_required',
            'match_analysis': {
                'match_score': 88,
                'analysis': 'Strong match for Python AI role. Experience with ML frameworks aligns well with requirements.',
                'resume_type': 'Python AI Developer',
                'tech_stack_detected': 'python_ai'
            }
        }
    ]
    
    # Render dashboard
    controls = dashboard.render(sample_jobs)


if __name__ == "__main__":
    main()
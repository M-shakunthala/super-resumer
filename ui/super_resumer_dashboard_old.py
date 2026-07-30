"""
Super Resumer Dashboard
Streamlit UI for job application tracking and management
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any
import datetime
import json


class SuperResumerDashboard:
    """Streamlit dashboard for Super Resumer."""
    
    def __init__(self):
        self.setup_page()
        
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
        
        # Job Search Configuration
        st.sidebar.subheader("Job Search")
        
        # Fixed location as dropdown (greyed out)
        location = st.sidebar.selectbox(
            "Location",
            ["Bangalore"],
            index=0,
            disabled=True
        )
        st.caption("Location is fixed to Bangalore")
        
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
        reviewed_jobs = len([j for j in jobs if j.get('status') == 'pending_review'])
        rejected_jobs = len([j for j in jobs if j.get('status') == 'rejected'])
        pending_jobs = len([j for j in jobs if j.get('status') == 'pending'])
        
        # Render statistics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total Jobs", total_jobs)
        
        with col2:
            st.metric("Applied", applied_jobs, delta_color="normal")
        
        with col3:
            st.metric("Under Review", reviewed_jobs, delta_color="off")
        
        with col4:
            st.metric("Rejected", rejected_jobs, delta_color="inverse")
        
        with col5:
            st.metric("Pending", pending_jobs, delta_color="normal")
        
        st.markdown("---")
    
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
        
        # Create DataFrame
        df_data = []
        for job in filtered_jobs:
            # Format source name
            source = job.get('source', 'N/A')
            if source == 'company_websites':
                source = 'Company Websites'
            else:
                source = source.title()
            
            # Custom status display
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
            
            df_data.append({
                'Title': job.get('title', 'N/A'),
                'Company': job.get('company', 'N/A'),
                'Location': job.get('location', 'N/A'),
                'Salary': job.get('salary', 'N/A'),
                'Match Score': f"{job.get('match_score', 0)}%",
                'Source': source,
                'Status': display_status,
                'Resume': job.get('match_analysis', {}).get('resume_type', 'N/A') if isinstance(job.get('match_analysis'), dict) else 'N/A'
            })
        
        df = pd.DataFrame(df_data)
        
        # Display table
        st.dataframe(
            df,
            width='stretch',
            hide_index=True,
            column_config={
                "Title": st.column_config.TextColumn("Job Title", width="medium"),
                "Company": st.column_config.TextColumn("Company", width="medium"),
                "Match Score": st.column_config.TextColumn("Match %", width="small"),
                "Source": st.column_config.TextColumn("Source", width="small"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Resume": st.column_config.TextColumn("Resume Used", width="medium"),
            }
        )
        
        return filtered_jobs
    
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
            st.write(f"🌐 **Source:** {job.get('source', 'N/A').title()}")
            st.write(f"📄 **Resume Type:** {job.get('match_analysis', {}).get('resume_type', 'N/A')}")
        
        st.markdown("---")
        st.subheader("Job Description")
        st.write(job.get('description', 'No description available'))
        
        st.markdown("---")
        st.subheader("Match Analysis")
        st.write(job.get('match_analysis', {}).get('analysis', 'No analysis available'))
        
        st.markdown("---")
        
        # Automatic apply button - marks as applied and opens job link
        job_id = f"{job.get('title')}_{job.get('company')}"
        job_url = job.get('url', '#')
        
        # Format source name
        source = job.get('source', 'N/A')
        if source == 'company_websites':
            source = 'Company Websites'
        else:
            source = source.title()
        
        # Get resume type
        resume_type = job.get('match_analysis', {}).get('resume_type', 'N/A') if isinstance(job.get('match_analysis'), dict) else 'N/A'
        
        # Format tech stack
        tech_stack = job.get('tech_stack', [])
        if isinstance(tech_stack, list):
            tech_stack_display = ', '.join(tech_stack)
        else:
            tech_stack_display = tech_stack
        
        with col3:
            st.write(f"🌐 **Source:** {source}")
            st.write(f"📄 **Resume Used:** {resume_type}")
        
        st.markdown("---")
        st.subheader("Job Description")
        st.write(job.get('description', 'No description available'))
        
        st.markdown("---")
        st.subheader("Match Analysis")
        analysis = job.get('match_analysis', {}).get('analysis', 'No analysis available') if isinstance(job.get('match_analysis'), dict) else job.get('match_analysis', 'No analysis available')
        st.write(analysis)
        
        st.markdown("---")
        
        # Job application link
        if job_url and job_url != '#':
            st.markdown(f"### � [Apply to this Job]({job_url}){{:target='_blank'}}")
            st.caption("Click the link above to apply directly on the job site")
        else:
            st.warning("🔗 No application URL available for this job")
    
    def render_main_content(self, jobs: List[Dict[str, Any]]):
        """Render main dashboard content."""
        # Page title (shown only once)
        st.title("Super Resumer")
        st.markdown("---")
        
        # Render statistics
        self.render_job_statistics(jobs)
        
        # Status filter tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🔍 All Jobs", 
            "✅ Applied", 
            "👀 Under Review", 
            "❌ Rejected", 
            "⏳ Pending"
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
                st.success(f"🎉 You've applied to {len(applied_jobs)} jobs!")
        
        with tab3:
            st.subheader("Jobs Under Review")
            review_jobs = self.render_jobs_table(jobs, "pending_review")
            
            if review_jobs:
                st.info(f"👀 {len(review_jobs)} jobs are under your review")
        
        with tab4:
            st.subheader("Rejected Jobs")
            rejected_jobs = self.render_jobs_table(jobs, "rejected")
            
            if rejected_jobs:
                st.warning(f"❌ {len(rejected_jobs)} jobs were rejected")
        
        with tab5:
            st.subheader("Pending Jobs")
            pending_jobs = self.render_jobs_table(jobs, "pending")
            
            if pending_jobs:
                st.info(f"⏳ {len(pending_jobs)} jobs are pending action")
    
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
            'status': 'pending_review',
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
            'status': 'pending',
            'match_analysis': {
                'match_score': 88,
                'analysis': 'Strong match for Python AI role. Experience with ML frameworks aligns well with requirements.',
                'resume_type': 'Python AI Developer',
                'tech_stack_detected': 'python_ai'
            }
        },
        {
            'title': 'Full Stack Developer',
            'company': 'StartupXYZ',
            'location': 'Bangalore',
            'salary': '8-12 LPA',
            'description': 'Full stack developer needed for web application development. Experience with React, Node.js, and MongoDB required.',
            'url': 'https://example.com/job/789',
            'source': 'naukri',
            'tech_stack': ['React', 'Node.js', 'MongoDB'],
            'match_score': 45,
            'status': 'rejected',
            'rejection_reason': 'Match score 45% below threshold 85%',
            'match_analysis': {
                'match_score': 45,
                'analysis': 'Poor match - tech stack mismatch with C#/Python AI specialization.',
                'resume_type': 'Python AI Developer (default)',
                'tech_stack_detected': 'ambiguous'
            }
        }
    ]
    
    # Render dashboard
    controls = dashboard.render(sample_jobs)
    
    # Handle button actions
    if controls['search_jobs']:
        st.info("🔍 Job search initiated... (Connect to actual scraper)")
    
    if controls['load_resumes']:
        st.info("📄 Loading resumes... (Connect to actual resume loader)")


if __name__ == "__main__":
    main()
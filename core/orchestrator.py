"""
Smart orchestrator for intelligent job processing workflow
"""
import random
import os
from agents.resume_optimizer import ResumeOptimizer
from agents.pdf_builder import PDFBuilder
from resumes.resume_loader import ResumeLoader
from core.config import Config


class Orchestrator:
    """
    Smart job processor with AI-powered resume optimization and PDF generation
    Implements the complete intelligent workflow for job applications
    """
    
    def __init__(self):
        """Initialize orchestrator with all components"""
        self.config = Config.load()
        
        # Initialize components
        try:
            self.optimizer = ResumeOptimizer()
            self.has_optimizer = True
        except ValueError:
            print("⚠️  Resume optimizer not available (API key not set)")
            self.optimizer = None
            self.has_optimizer = False
        
        self.pdf_builder = PDFBuilder()
        
        # Load base resume
        self.resume_loader = ResumeLoader()
        try:
            self.base_resume = self.resume_loader.load_base_resume()
            print(f"✅ Base resume loaded ({len(self.base_resume)} characters)")
        except Exception as e:
            print(f"❌ Error loading base resume: {e}")
            self.base_resume = None
        
        # Check automation mode
        testing_config = self.config.get('testing', {})
        self.automation_enabled = testing_config.get('current_phase', 1) >= 4
        self.dry_run = testing_config.get('dry_run', True)

    def process(self, job):
        """
        Process a job application with intelligent workflow
        
        Args:
            job: Job dictionary with title, url, description, company, etc.
            
        Returns:
            Result dictionary with application status and generated files
        """
        if not self.base_resume:
            return {
                "job": job,
                "status": "failed",
                "error": "Base resume not loaded",
                "timestamp": self._get_timestamp()
            }
        
        result = {
            "job": job,
            "timestamp": self._get_timestamp(),
            "steps": []
        }
        
        try:
            # Step 1: Optimize resume for job
            result["steps"].append("Resume optimization")
            tailored_resume = self._optimize_resume(job, result)
            
            # Step 2: Generate PDF
            result["steps"].append("PDF generation")
            pdf_path = self._generate_pdf(tailored_resume, job, result)
            
            # Step 3: Apply for job (if automation enabled)
            if self.automation_enabled and not self.dry_run:
                result["steps"].append("Job application")
                apply_result = self._apply_job(job, pdf_path, result)
                result["status"] = apply_result["status"]
                result["pdf_path"] = pdf_path
            else:
                # Dry run mode - don't actually apply
                result["status"] = "ready"
                result["pdf_path"] = pdf_path
                result["message"] = "Resume ready for manual application (dry run mode)"
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            print(f"❌ Processing error: {e}")
        
        return result
    
    def _optimize_resume(self, job, result):
        """Optimize resume for specific job"""
        job_description = job.get('description', '')
        if not job_description:
            print("⚠️  No job description found, using base resume")
            return self.base_resume
        
        if self.has_optimizer and self.optimizer:
            try:
                tailored = self.optimizer.tailor(self.base_resume, job_description)
                print(f"✅ Resume optimized for {job.get('title', 'Unknown')}")
                return tailored
            except Exception as e:
                print(f"⚠️  Optimization failed, using base resume: {e}")
                return self.base_resume
        else:
            print("📝 Using base resume (optimizer not available)")
            return self.base_resume
    
    def _generate_pdf(self, resume_text, job, result):
        """Generate PDF from tailored resume"""
        company_name = job.get('company', 'Unknown')
        job_title = job.get('title', 'Unknown')
        
        try:
            # Sanitize company name for filename
            safe_company = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"resume_{safe_company.replace(' ', '_').lower()}.pdf"
            
            pdf_path = self.pdf_builder.build(resume_text, filename, company_name)
            print(f"✅ PDF generated: {filename}")
            result["pdf_generated"] = True
            
            return pdf_path
            
        except Exception as e:
            print(f"❌ PDF generation failed: {e}")
            result["pdf_generated"] = False
            raise
    
    def _apply_job(self, job, pdf_path, result):
        """Apply for job with generated PDF using platform-specific handler"""
        from core.apply_engine import ApplyEngine
        
        if self.dry_run:
            return {
                "status": "ready",
                "message": f"Ready to apply with PDF: {pdf_path} (dry run mode)",
                "platform": "unknown"
            }
        
        try:
            engine = ApplyEngine()
            engine.apply(job["url"], pdf_path)
            
            return {
                "status": "applied",
                "platform": "detected",
                "pdf_path": pdf_path
            }
            
        except Exception as e:
            print(f"❌ Application error: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "pdf_path": pdf_path
            }
    
    def process_step1_optimize_only(self, job):
        """
        Step 1: Optimize resume only (testing phase)
        
        Returns optimized resume text for manual review
        """
        if not self.base_resume:
            return {"error": "Base resume not loaded"}
        
        result = {
            "job": job,
            "step": "optimize_only",
            "timestamp": self._get_timestamp()
        }
        
        job_description = job.get('description', '')
        if not job_description:
            result["error"] = "No job description found"
            return result
        
        if self.has_optimizer and self.optimizer:
            try:
                tailored = self.optimizer.tailor(self.base_resume, job_description)
                result["optimized_resume"] = tailored
                result["status"] = "optimized"
                print(f"✅ Resume optimized for review")
                return result
            except Exception as e:
                result["error"] = str(e)
                return result
        else:
            result["error"] = "Optimizer not available"
            return result
    
    def process_step2_generate_pdf_only(self, job, resume_text=None):
        """
        Step 2: Generate PDF only (testing phase)
        
        Returns PDF path for manual review
        """
        if not resume_text and not self.base_resume:
            return {"error": "No resume text available"}
        
        resume_to_use = resume_text or self.base_resume
        company_name = job.get('company', 'Unknown')
        
        try:
            safe_company = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).strip()
            filename = f"resume_{safe_company.replace(' ', '_').lower()}.pdf"
            
            pdf_path = self.pdf_builder.build(resume_to_use, filename, company_name)
            
            result = {
                "job": job,
                "step": "generate_pdf_only",
                "pdf_path": pdf_path,
                "filename": filename,
                "status": "pdf_generated",
                "timestamp": self._get_timestamp()
            }
            
            print(f"✅ PDF generated for manual review: {filename}")
            return result
            
        except Exception as e:
            return {"error": str(e), "status": "failed"}
    
    def get_status(self):
        """Get orchestrator status and configuration"""
        return {
            "optimizer_available": self.has_optimizer,
            "automation_enabled": self.automation_enabled,
            "dry_run": self.dry_run,
            "base_resume_loaded": self.base_resume is not None,
            "pdf_builder_ready": True
        }
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

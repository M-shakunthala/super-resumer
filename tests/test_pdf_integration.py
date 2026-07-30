"""
Complete PDF generation integration workflow
"""
from resumes.resume_loader import ResumeLoader
from agents.resume_optimizer import ResumeOptimizer
from agents.pdf_builder import PDFBuilder
from pathlib import Path
import os


def demonstrate_complete_workflow():
    """Demonstrate complete workflow from text to PDF"""
    print("🚀 COMPLETE PDF GENERATION WORKFLOW")
    print("=" * 60)
    
    # Initialize components
    loader = ResumeLoader()
    builder = PDFBuilder()
    
    # Try to initialize optimizer (optional)
    try:
        optimizer = ResumeOptimizer()
        use_ai = True
    except ValueError:
        print("⚠️  AI optimizer not available (API key not set)")
        print("   Using base resume for PDF generation")
        optimizer = None
        use_ai = False
    
    # Sample job applications
    job_applications = [
        {
            "company": "Google",
            "title": "Python Backend Developer",
            "description": """
            We are looking for a Python Backend Developer for our cloud infrastructure.
            
            Requirements:
            - Strong Python development skills
            - SQL database expertise
            - REST API development
            - Docker and Kubernetes experience
            - Cloud platform experience (GCP preferred)
            
            Join our world-class engineering team!
            """
        },
        {
            "company": "Amazon",
            "title": "Software Engineer - Backend Services",
            "description": """
            Software Engineer needed for our e-commerce backend systems.
            
            Must have:
            - Python backend development
            - SQL database experience
            - API design and development
            - Distributed systems knowledge
            
            Preferred:
            - AWS cloud experience
            - Microservices architecture
            - High-scale systems experience
            
            Build systems that serve millions of customers.
            """
        },
        {
            "company": "Microsoft",
            "title": "Python Developer - Azure Services",
            "description": """
            Python Developer for our Azure cloud platform team.
            
            Requirements:
            - Python programming expertise
            - Cloud platform experience
            - REST API development
            - Database design skills
            
            Nice to have:
            - Azure specific experience
            - DevOps knowledge
            - Container deployment skills
            
            Work on cutting-edge cloud solutions.
            """
        }
    ]
    
    print(f"\n📋 Processing {len(job_applications)} job applications")
    print("-" * 60)
    
    # Load base resume
    try:
        base_resume = loader.load_base_resume()
        print(f"✅ Base resume loaded ({len(base_resume)} characters)")
    except:
        print("❌ Error loading base resume")
        return False
    
    generated_pdfs = []
    
    for i, job in enumerate(job_applications, 1):
        print(f"\n📄 Job {i}: {job['company']} - {job['title']}")
        print("-" * 60)
        
        # Step 1: Optimize resume for this job
        print("🤖 Step 1: Optimizing resume for job...")
        try:
            if optimizer and use_ai:
                optimized_resume = optimizer.tailor(base_resume, job['description'])
                print(f"   ✅ Resume optimized using AI")
            else:
                print(f"   🎭 Using base resume (AI not available)")
                optimized_resume = base_resume
        except Exception as e:
            print(f"   ⚠️  Using base resume (optimization error: {e})")
            optimized_resume = base_resume
        
        # Step 2: Generate PDF
        print("📄 Step 2: Generating company-specific PDF...")
        try:
            company_safe = job['company'].lower().replace(' ', '_')
            filename = f"resume_{company_safe}.pdf"
            output_path = builder.build(optimized_resume, filename, job['company'])
            
            if Path(output_path).exists():
                file_size = Path(output_path).stat().st_size
                print(f"   ✅ PDF generated: {Path(output_path).name}")
                print(f"   📊 File size: {file_size} bytes")
                generated_pdfs.append(output_path)
            else:
                print(f"   ❌ PDF generation failed")
                
        except Exception as e:
            print(f"   ❌ Error generating PDF: {e}")
    
    print("\n" + "=" * 60)
    print("✅ WORKFLOW COMPLETE")
    print(f"\n📁 Generated {len(generated_pdfs)} PDF files:")
    
    for pdf_path in generated_pdfs:
        print(f"   • {Path(pdf_path).name}")
    
    print(f"\n📁 Output directory: {builder.output_dir}")
    
    print("\n💡 Workflow Benefits:")
    print("   1. 📄 Load base resume from text file")
    print("   2. 🎯 Optimize for each specific job")
    print("   3. 📄 Generate company-specific PDF")
    print("   4. 🏢 Organize by company name")
    print("   5. 📊 Professional format for applications")
    print("   6. ✅ ATS-compatible layout")
    
    return True


def demonstrate_pdf_features():
    """Demonstrate advanced PDF builder features"""
    print("\n🎯 ADVANCED PDF BUILDER FEATURES")
    print("=" * 60)
    
    builder = PDFBuilder()
    loader = ResumeLoader()
    
    # Load resume
    try:
        resume_text = loader.load_base_resume()
        sections = loader.get_resume_sections()
    except:
        resume_text = "Sample resume content"
        sections = {"header": "Sample", "skills": "Python, SQL"}
    
    # Feature 1: Company-specific filenames
    print("\n📄 Feature 1: Company-specific filenames")
    companies = ["Google", "Amazon AWS", "Microsoft Azure"]
    for company in companies:
        pdf_path = builder.get_pdf_path(company)
        print(f"   {company} → {Path(pdf_path).name}")
    
    # Feature 2: Section-based building
    print("\n📄 Feature 2: Building from sections")
    try:
        output_path = builder.build_from_sections(sections, "sections_test.pdf")
        print(f"   ✅ Built from {len(sections)} sections")
        print(f"   📁 {Path(output_path).name}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Feature 3: Multiple PDF generation
    print("\n📄 Feature 3: Batch PDF generation")
    variants = {
        "TechCorp": resume_text,
        "DataInc": resume_text,
        "CloudSys": resume_text
    }
    
    try:
        generated = builder.build_multiple(variants, "batch_resume")
        print(f"   ✅ Generated {len(generated)} PDFs in batch:")
        for pdf in generated:
            print(f"      • {Path(pdf).name}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Feature 4: Existence checking
    print("\n📄 Feature 4: PDF existence checking")
    print(f"   resume_google.pdf exists: {builder.pdf_exists('Google')}")
    print(f"   resume_apple.pdf exists: {builder.pdf_exists('Apple')}")
    
    # Feature 5: Custom styling info
    print("\n📄 Feature 5: PDF configuration")
    print(f"   Page size: {builder.page_size}")
    print(f"   Output directory: {builder.output_dir}")
    print(f"   Margins configured: {len(builder.margins)} sides")


def demonstrate_text_to_pdf_benefits():
    """Demonstrate benefits of text-to-PDF workflow"""
    print("\n💡 TEXT-TO-PDF WORKFLOW BENEFITS")
    print("=" * 60)
    
    print("\n🔄 Workflow Process:")
    print("   1. 📝 Base Resume (Text)")
    print("      • Easy to edit")
    print("      • AI-friendly")
    print("      • Version control friendly")
    print()
    print("   2. 🤖 AI Optimization (Text)")
    print("      • Job-specific tailoring")
    print("      • ATS optimization")
    print("      • Keyword enhancement")
    print()
    print("   3. 📄 PDF Generation (Final)")
    print("      • Professional format")
    print("      • ATS-compatible")
    print("      • Company-specific versions")
    
    print("\n✅ Key Advantages:")
    print("   • Edit in text (AI-optimized)")
    print("   • Deliver in PDF (professional)")
    print("   • Best of both worlds")
    print("   • Workflow efficiency")
    print("   • Consistent quality")
    
    print("\n🎯 Use Cases:")
    print("   • Job applications to different companies")
    print("   • Tailored resumes for specific roles")
    print("   • A/B testing different resume versions")
    print("   • Maintaining multiple career targets")


if __name__ == "__main__":
    success = demonstrate_complete_workflow()
    if success:
        demonstrate_pdf_features()
        demonstrate_text_to_pdf_benefits()
    
    # Cleanup test PDFs
    try:
        import shutil
        if Path("resumes/pdfs").exists():
            shutil.rmtree("resumes/pdfs")
            print("\n🧹 Cleaned up test PDF files")
    except:
        pass
    
    exit(0 if success else 1)

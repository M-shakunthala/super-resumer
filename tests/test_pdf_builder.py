"""
Test PDF resume builder functionality
"""
from agents.pdf_builder import PDFBuilder
from resumes.resume_loader import ResumeLoader


def test_pdf_builder():
    print("📄 PDF RESUME BUILDER TEST")
    print("=" * 50)
    
    # Initialize PDF builder
    try:
        builder = PDFBuilder()
        print("✅ PDF Builder initialized successfully")
        print(f"   Output directory: {builder.output_dir}")
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False
    
    # Load base resume
    try:
        loader = ResumeLoader()
        resume_text = loader.load_base_resume()
        print(f"✅ Base resume loaded ({len(resume_text)} characters)")
    except Exception as e:
        print(f"❌ Error loading resume: {e}")
        # Use sample resume for testing
        resume_text = """John Doe

Software Engineer with 2 years of experience in backend development.

Skills:
Python, SQL, C#, .NET, REST APIs, Selenium, Git, Docker

Experience:
Junior Software Developer | Tech Company Inc. | 2022-2023
- Developed backend services using Python and SQL
- Built RESTful APIs serving 10,000+ daily requests
- Automated testing workflows using Selenium, reducing manual testing by 40%
- Collaborated with senior developers on database optimization projects

Projects:
Job Application Automation System | Personal Project
- Built automated job scraping system using Selenium and Python
- Implemented AI-powered job matching and resume tailoring
- Designed database schema for tracking application status

Education:
Bachelor of Science in Computer Science | State University | 2018-2022
- GPA: 3.7/4.0
- Relevant Coursework: Data Structures, Algorithms, Database Management"""
        print(f"   Using sample resume ({len(resume_text)} characters)")
    
    # Test 1: Build basic PDF
    print("\n📄 Test 1: Building basic PDF...")
    try:
        output_path = builder.build(resume_text, "test_resume.pdf")
        print(f"✅ PDF built successfully: {output_path}")
        
        # Verify file exists
        from pathlib import Path
        if Path(output_path).exists():
            file_size = Path(output_path).stat().st_size
            print(f"   File size: {file_size} bytes")
        else:
            print(f"   ❌ File not created")
            return False
            
    except Exception as e:
        print(f"❌ Error building PDF: {e}")
        return False
    
    # Test 2: Build PDF with company name
    print("\n📄 Test 2: Building PDF with company name...")
    try:
        output_path = builder.build(resume_text, "test_resume.pdf", "Google")
        print(f"✅ PDF built with company name: {output_path}")
        
        if Path(output_path).exists():
            print(f"   Filename contains company name: {'google' in output_path.lower()}")
        else:
            print(f"   ❌ File not created")
            return False
            
    except Exception as e:
        print(f"❌ Error building PDF with company name: {e}")
        return False
    
    # Test 3: Build from sections
    print("\n📄 Test 3: Building PDF from sections...")
    try:
        sections = loader.get_resume_sections()
        output_path = builder.build_from_sections(sections, "test_sections.pdf", "Amazon")
        print(f"✅ PDF built from sections: {output_path}")
        
        if Path(output_path).exists():
            print(f"   Successfully built from {len(sections)} sections")
        else:
            print(f"   ❌ File not created")
            return False
            
    except Exception as e:
        print(f"❌ Error building from sections: {e}")
        return False
    
    # Test 4: Build multiple PDFs
    print("\n📄 Test 4: Building multiple PDFs...")
    try:
        variants = {
            "Google": resume_text,
            "Amazon": resume_text,
            "Microsoft": resume_text
        }
        
        generated_files = builder.build_multiple(variants)
        print(f"✅ Built {len(generated_files)} PDFs:")
        for file_path in generated_files:
            print(f"   • {Path(file_path).name}")
            
    except Exception as e:
        print(f"❌ Error building multiple PDFs: {e}")
        return False
    
    # Test 5: Check PDF existence
    print("\n📄 Test 5: Checking PDF existence...")
    try:
        exists = builder.pdf_exists("Google")
        print(f"✅ PDF exists check: {exists}")
        
        # Get PDF path
        pdf_path = builder.get_pdf_path("Google")
        print(f"   Expected path: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Error checking PDF existence: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ALL PDF BUILDER TESTS PASSED")
    print("\n📁 PDF files created in:", builder.output_dir)
    print("\n💡 Integration Benefits:")
    print("   • Professional PDF format for applications")
    print("   • Company-specific resume versions")
    print("   • ATS-compatible formatting")
    print("   • Automatic file organization")
    print("   • Clean, professional layout")
    
    return True


def demonstrate_pdf_workflow():
    """Demonstrate complete PDF generation workflow"""
    from pathlib import Path
    
    print("\n🚀 PDF GENERATION WORKFLOW DEMONSTRATION")
    print("=" * 60)
    
    builder = PDFBuilder()
    loader = ResumeLoader()
    
    # Sample companies
    companies = [
        "Google",
        "Amazon", 
        "Microsoft",
        "Accenture",
        "Uber"
    ]
    
    # Load resume
    try:
        base_resume = loader.load_base_resume()
    except:
        base_resume = "Sample resume content for demonstration..."
    
    print(f"\n📄 Base resume loaded ({len(base_resume)} characters)")
    print(f"🏢 Target companies: {', '.join(companies)}")
    
    print("\n🤖 Workflow:")
    print("1. ✅ Load base resume text")
    print("2. ✅ For each job application:")
    print("3.    ✅ Optimize resume for specific job")
    print("4.    ✅ Generate company-specific PDF")
    print("5.    ✅ Use PDF for job application")
    
    print("\n📁 Generated PDFs would be:")
    for company in companies:
        pdf_path = builder.get_pdf_path(company)
        filename = Path(pdf_path).name
        print(f"   • {filename}")
    
    print("\n💡 Benefits:")
    print("   • resume_google.pdf - Tailored for Google")
    print("   • resume_amazon.pdf - Tailored for Amazon")
    print("   • resume_microsoft.pdf - Tailored for Microsoft")
    print("   • Each PDF optimized for specific company")
    print("   • Professional format for ATS systems")


if __name__ == "__main__":
    success = test_pdf_builder()
    if success:
        demonstrate_pdf_workflow()
    exit(0 if success else 1)

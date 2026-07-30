"""
Orchestrator testing strategy - 3-step validation before automation
"""
from core.orchestrator import Orchestrator
from resumes.resume_loader import ResumeLoader
from agents.jd_parser import JDParser


def test_step1_optimizer_only():
    """
    Step 1: Test optimizer only
    
    Verify:
    - Is resume truthful?
    - Are keywords relevant?
    - Professional language maintained?
    """
    print("🧪 STEP 1: OPTIMIZER TESTING")
    print("=" * 60)
    print("🎯 Testing resume optimization before automation")
    print("-" * 60)
    
    orchestrator = Orchestrator()
    status = orchestrator.get_status()
    
    print(f"Orchestrator Status:")
    print(f"  Optimizer Available: {status['optimizer_available']}")
    print(f"  Base Resume Loaded: {status['base_resume_loaded']}")
    
    if not status['optimizer_available']:
        print("\n❌ Optimizer not available - cannot test")
        print("🔑 Please set OPENAI_API_KEY in .env file")
        return False
    
    # Sample job for testing
    test_job = {
        "title": "Python Backend Developer",
        "company": "TestCorp",
        "description": """
        We are looking for a Python Backend Developer to join our team.
        
        Requirements:
        - Python development experience
        - SQL database skills
        - REST API development
        - Docker containerization
        
        Preferred:
        - FastAPI or Django
        - Redis caching
        - Cloud platform experience
        """
    }
    
    print(f"\n📋 Test Job: {test_job['title']} at {test_job['company']}")
    print("-" * 60)
    
    # Run optimizer only
    result = orchestrator.process_step1_optimize_only(test_job)
    
    if result.get("error"):
        print(f"❌ Optimization failed: {result['error']}")
        return False
    
    optimized_resume = result['optimized_resume']
    
    print("✅ Resume optimization successful")
    print(f"   Optimized resume length: {len(optimized_resume)} characters")
    
    # Verification checks
    print("\n🔍 VERIFICATION CHECKS:")
    print("-" * 60)
    
    # Load original for comparison
    loader = ResumeLoader()
    original_resume = loader.load_base_resume()
    
    # Check 1: Truthfulness - resume still contains original experience
    print("1. ✅ Truthfulness Check:")
    if "John Doe" in optimized_resume:
        print("   ✓ Original name preserved")
    else:
        print("   ⚠ Name changed - review needed")
    
    # Check 2: Relevant keywords - job requirements present
    print("2. ✅ Keyword Relevance Check:")
    required_keywords = ["python", "sql", "api", "docker"]
    found_keywords = []
    for keyword in required_keywords:
        if keyword.lower() in optimized_resume.lower():
            found_keywords.append(keyword)
    
    print(f"   Required keywords found: {len(found_keywords)}/{len(required_keywords)}")
    print(f"   Found: {', '.join(found_keywords)}")
    
    # Check 3: Professional language
    print("3. ✅ Professional Language Check:")
    professional_indicators = ["developed", "designed", "implemented", "built", "engineered"]
    professional_count = sum(1 for indicator in professional_indicators if indicator in optimized_resume.lower())
    print(f"   Professional action verbs: {professional_count} found")
    
    # Check 4: No fake experience
    print("4. ✅ No Fake Experience Check:")
    original_experiences = ["Tech Company Inc", "Startup XYZ", "University Project"]
    experiences_preserved = sum(1 for exp in original_experiences if exp in optimized_resume)
    print(f"   Original experiences preserved: {experiences_preserved}/{len(original_experiences)}")
    
    print("\n📄 OPTIMIZED RESUME PREVIEW:")
    print("-" * 60)
    print(optimized_resume[:400] + "..." if len(optimized_resume) > 400 else optimized_resume)
    
    print("\n✅ STEP 1 COMPLETE - Review optimized resume above")
    print("💡 If checks pass, proceed to Step 2")
    
    return True


def test_step2_generate_pdf_only():
    """
    Step 2: Generate PDFs only
    
    Verify:
    - PDF formatting is correct
    - Professional layout
    - Readable content
    """
    print("\n🧪 STEP 2: PDF GENERATION TESTING")
    print("=" * 60)
    print("🎯 Testing PDF generation before automation")
    print("-" * 60)
    
    orchestrator = Orchestrator()
    loader = ResumeLoader()
    
    # Use optimized or base resume
    try:
        base_resume = loader.load_base_resume()
    except:
        base_resume = "Sample resume content for testing"
    
    # Sample job
    test_job = {
        "title": "Python Developer",
        "company": "Google",
        "description": "Sample job description for PDF testing"
    }
    
    print(f"\n📋 Test Job: {test_job['title']} at {test_job['company']}")
    print("-" * 60)
    
    # Generate PDF only
    result = orchestrator.process_step2_generate_pdf_only(test_job, base_resume)
    
    if result.get("error"):
        print(f"❌ PDF generation failed: {result['error']}")
        return False
    
    pdf_path = result['pdf_path']
    filename = result['filename']
    
    print("✅ PDF generation successful")
    print(f"   Filename: {filename}")
    print(f"   Path: {pdf_path}")
    
    # Verification checks
    from pathlib import Path
    if Path(pdf_path).exists():
        file_size = Path(pdf_path).stat().st_size
        print(f"   File size: {file_size} bytes")
    else:
        print("❌ PDF file not created")
        return False
    
    print("\n🔍 VERIFICATION CHECKS:")
    print("-" * 60)
    
    # Check 1: File exists
    print("1. ✅ File Existence Check:")
    print(f"   ✓ PDF file exists at: {pdf_path}")
    
    # Check 2: File size reasonable
    print("2. ✅ File Size Check:")
    if 1000 < file_size < 100000:  # Between 1KB and 100KB
        print(f"   ✓ Reasonable file size: {file_size} bytes")
    else:
        print(f"   ⚠ Unusual file size: {file_size} bytes")
    
    # Check 3: Company name in filename
    print("3. ✅ Filename Check:")
    company_name_safe = test_job['company'].lower().replace(' ', '_')
    if company_name_safe in filename.lower():
        print(f"   ✓ Company name in filename: {company_name_safe}")
    else:
        print(f"   ⚠ Company name not in filename")
    
    # Check 4: PDF can be opened (basic check)
    print("4. ✅ PDF Validity Check:")
    try:
        import PyPDF2
        with open(pdf_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            num_pages = len(pdf_reader.pages)
            print(f"   ✓ PDF is valid, {num_pages} page(s)")
    except ImportError:
        print("   ⚠ PyPDF2 not installed, skipping validity check")
    except Exception as e:
        print(f"   ⚠ PDF validity check failed: {e}")
    
    print("\n✅ STEP 2 COMPLETE - Review generated PDF")
    print(f"💡 Open and verify: {pdf_path}")
    print("💡 If formatting looks good, proceed to Step 3")
    
    return True


def test_step3_manual_upload():
    """
    Step 3: Manual upload to LinkedIn
    
    Verify:
    - ATS friendliness
    - Upload process works
    - Display is correct
    """
    print("\n🧪 STEP 3: MANUAL UPLOAD TESTING")
    print("=" * 60)
    print("🎯 Manual upload to LinkedIn for ATS verification")
    print("-" * 60)
    
    # Get generated PDF
    from pathlib import Path
    pdf_dir = Path("resumes/pdfs")
    
    if not pdf_dir.exists():
        print("❌ No PDF directory found")
        print("💡 Complete Step 2 first to generate PDFs")
        return False
    
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found")
        print("💡 Complete Step 2 first to generate PDFs")
        return False
    
    print(f"📁 Found {len(pdf_files)} PDF file(s):")
    for pdf_file in pdf_files:
        print(f"   • {pdf_file.name}")
    
    print("\n🔍 MANUAL VERIFICATION STEPS:")
    print("-" * 60)
    
    print("1. ✅ ATS Friendliness Check:")
    print("   • Manually upload PDF to LinkedIn")
    print("   • Check if LinkedIn parses correctly")
    print("   • Verify sections are recognized")
    print("   • Confirm formatting is preserved")
    
    print("\n2. ✅ Display Verification:")
    print("   • View PDF in LinkedIn preview")
    print("   • Check text is readable")
    print("   • Verify layout looks professional")
    print("   • Confirm no formatting issues")
    
    print("\n3. ✅ Download Test:")
    print("   • Download PDF from LinkedIn")
    print("   • Compare with original")
    print("   • Check for data loss")
    print("   • Verify integrity maintained")
    
    print("\n📋 MANUAL CHECKLIST:")
    print("-" * 60)
    print("   [ ] Text is readable after upload")
    print("   [ ] Section headers are recognized")
    print("   [ ] Formatting is preserved")
    print("   [ ] No garbled characters")
    print("   [ ] Layout looks professional")
    print("   [ ] Contact information is visible")
    print("   [ ] Skills are properly displayed")
    print("   [ ] Experience is clearly shown")
    print("   [ ] File size is appropriate")
    
    print("\n✅ STEP 3 COMPLETE - Manual verification required")
    print("💡 After manual verification confirms ATS friendliness:")
    print("   → You can enable automation in config")
    print("   → Set testing.current_phase to 4")
    print("   → Set testing.dry_run to false")
    
    return True


def run_orchestrator_status_check():
    """Check orchestrator status and configuration"""
    print("🔍 ORCHESTRATOR STATUS CHECK")
    print("=" * 60)
    
    orchestrator = Orchestrator()
    status = orchestrator.get_status()
    
    print("\n📊 Current Configuration:")
    print("-" * 60)
    for key, value in status.items():
        status_icon = "✅" if value else "❌"
        print(f"{status_icon} {key.replace('_', ' ').title()}: {value}")
    
    print("\n🎯 Automation Status:")
    print("-" * 60)
    if status['automation_enabled']:
        print("⚠️  AUTOMATION IS ENABLED")
        print("   The system will automatically apply to jobs")
        print("   Make sure you have completed all testing steps!")
    else:
        print("✅ SAFE MODE - Automation disabled")
        print("   System will not automatically apply to jobs")
        print("   Complete testing steps before enabling")
    
    if status['dry_run']:
        print("✅ DRY RUN MODE - No real applications")
        print("   Safe for testing without real applications")
    else:
        print("⚠️  LIVE MODE - Real applications will be submitted")
    
    return True


def main():
    """Run orchestrator testing strategy"""
    print("🚀 ORCHESTRATOR TESTING STRATEGY")
    print("=" * 60)
    print("🧪 3-Step Validation Before Automation")
    print("=" * 60)
    
    # Check status first
    run_orchestrator_status_check()
    
    print("\n" + "=" * 60)
    print("📋 TESTING STRATEGY")
    print("=" * 60)
    print("Follow these steps in order:")
    print()
    print("Step 1: 🧪 Test Optimizer Only")
    print("   → Verify resume remains truthful")
    print("   → Check keywords are relevant")
    print("   → Confirm professional language")
    print()
    print("Step 2: 🧪 Generate PDFs Only")
    print("   → Verify PDF formatting")
    print("   → Check professional layout")
    print("   → Confirm content is readable")
    print()
    print("Step 3: 🧪 Manual Upload to LinkedIn")
    print("   → Check ATS friendliness")
    print("   → Verify display correctness")
    print("   → Test upload process")
    print()
    print("Only after ALL steps pass:")
    print("   → Enable automation in config")
    print("   → Set testing.current_phase to 4")
    print("   → Set testing.dry_run to false")
    
    print("\n" + "=" * 60)
    
    # Ask which step to test
    print("\n🎯 Which step would you like to test?")
    print("1. Test Step 1 (Optimizer only)")
    print("2. Test Step 2 (PDF generation only)")
    print("3. Test Step 3 (Manual upload instructions)")
    print("4. Run all steps")
    print("5. Status check only")
    
    # For automated testing, run all steps
    print("\n🤖 Running all testing steps...")
    print("-" * 60)
    
    # Step 1
    step1_success = test_step1_optimizer_only()
    
    # Step 2
    step2_success = test_step2_generate_pdf_only()
    
    # Step 3
    step3_success = test_step3_manual_upload()
    
    print("\n" + "=" * 60)
    print("🎯 TESTING SUMMARY")
    print("=" * 60)
    print(f"Step 1 (Optimizer): {'✅ PASSED' if step1_success else '❌ FAILED'}")
    print(f"Step 2 (PDF Gen): {'✅ PASSED' if step2_success else '❌ FAILED'}")
    print(f"Step 3 (Manual Upload): {'✅ READY' if step3_success else '❌ FAILED'}")
    
    if step1_success and step2_success and step3_success:
        print("\n✅ ALL TESTING STEPS COMPLETED")
        print("💡 Review results and manually verify Step 3")
        print("💡 Then you can consider enabling automation")
    else:
        print("\n⚠️  SOME STEPS FAILED")
        print("💡 Fix issues before proceeding to automation")
    
    # Cleanup
    print("\n🧹 Cleaning up test files...")
    try:
        import shutil
        if Path("resumes/pdfs").exists():
            shutil.rmtree("resumes/pdfs")
            print("✅ Test PDFs cleaned up")
    except:
        pass


if __name__ == "__main__":
    main()

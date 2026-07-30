# 📄 PDF Resume Builder

## 🎯 Purpose
Professional PDF generation from text resumes, creating company-specific resume versions for job applications.

## 🚀 What It Does

Converts text resumes into professional PDF format with company-specific filenames:

**Input:**
```text
John Doe
Software Engineer with 2 years of experience...
```

**Output:**
```
resume_google.pdf     # Tailored for Google
resume_amazon.pdf    # Tailored for Amazon  
resume_microsoft.pdf # Tailored for Microsoft
```

## 📁 Files Created

- `agents/pdf_builder.py` - PDF generation with reportlab
- `test_pdf_builder.py` - Basic PDF builder functionality test
- `test_pdf_integration.py` - Complete workflow integration test

## 🔧 Configuration

Updated `config/job_search.yaml` with PDF settings:

```yaml
pdf:
  output_dir: "resumes/pdfs"
  page_size: "letter"
  margins:
    top: 0.75
    bottom: 0.75
    left: 0.75
    right: 0.75
```

## 💻 Usage

### Basic Usage
```python
from agents.pdf_builder import PDFBuilder
from resumes.resume_loader import ResumeLoader

# Load resume
loader = ResumeLoader()
resume_text = loader.load_base_resume()

# Generate PDF
builder = PDFBuilder()
pdf_path = builder.build(resume_text, "my_resume.pdf")
```

### Company-Specific PDFs
```python
# Generate PDF with company name in filename
pdf_path = builder.build(resume_text, "resume.pdf", "Google")
# Output: resume_google.pdf
```

### Build from Sections
```python
# Build PDF from structured resume sections
sections = loader.get_resume_sections()
pdf_path = builder.build_from_sections(sections, "resume.pdf", "Amazon")
```

### Batch Generation
```python
# Generate multiple PDFs at once
variants = {
    "Google": google_resume_text,
    "Amazon": amazon_resume_text,
    "Microsoft": microsoft_resume_text
}

generated = builder.build_multiple(variants)
# Returns: ['resume_google.pdf', 'resume_amazon.pdf', 'resume_microsoft.pdf']
```

## 🧪 Testing

### Basic Test
```bash
python3 test_pdf_builder.py
```

### Integration Test
```bash
python3 test_pdf_integration.py
```

### Expected Output
```
📄 PDF RESUME BUILDER TEST
==================================================
✅ PDF Builder initialized successfully
✅ Base resume loaded (2270 characters)
📄 Test 1: Building basic PDF... ✅ PDF built successfully
📄 Test 2: Building PDF with company name... ✅ PDF built with company name
📄 Test 3: Building PDF from sections... ✅ PDF built from sections
📄 Test 4: Building multiple PDFs... ✅ Built 3 PDFs
📄 Test 5: Checking PDF existence... ✅ PDF exists check: True
```

## 🔍 How It Works

1. **Text Parsing**: Splits resume text into lines and paragraphs
2. **Header Detection**: Identifies section headers automatically
3. **Style Application**: Applies professional styling to content
4. **PDF Construction**: Builds PDF document with proper formatting
5. **File Organization**: Saves with company-specific naming

## 🎨 PDF Features

### Professional Formatting
- Clean, professional layout
- Standard page sizes (Letter, A4)
- Proper margins and spacing
- Consistent typography

### Smart Header Detection
- Automatically identifies section headers
- Applies different styles to headers vs body text
- Supports common resume section names

### Company-Specific Naming
- `resume_google.pdf` for Google applications
- `resume_amazon.pdf` for Amazon applications
- `resume_microsoft.pdf` for Microsoft applications
- Sanitized filenames for cross-platform compatibility

### Batch Processing
- Generate multiple PDFs at once
- Efficient processing for many applications
- Consistent formatting across all versions

## 🚀 Integration Workflow

```python
# 1. Load base resume
loader = ResumeLoader()
base_resume = loader.load_base_resume()

# 2. Optimize for specific job (optional)
optimizer = ResumeOptimizer()
optimized = optimizer.tailor(base_resume, job_description)

# 3. Generate company-specific PDF
builder = PDFBuilder()
pdf_path = builder.build(optimized, "resume.pdf", "Google")

# 4. Use PDF for job application
submit_application(job_url, pdf_path)
```

## 📊 Benefits

### 1. Professional Format
- Industry-standard PDF format
- ATS-compatible layout
- Consistent styling
- Clean typography

### 2. Company-Specific Versions
- Each company gets tailored version
- Organized by company name
- Easy to track which resume for which job
- No confusion between versions

### 3. Workflow Efficiency
- Automatic generation
- Batch processing support
- No manual PDF creation
- Consistent quality

### 4. Text-to-PDF Workflow
- Edit in text (AI-optimized)
- Deliver in PDF (professional)
- Best of both worlds
- Flexible workflow

## 🔒 Features

### Custom Fonts Support
- Drop custom fonts in `resumes/fonts/`
- Automatically registers available fonts
- Professional typography options

### Page Size Options
- Letter size (default)
- A4 size
- Configurable margins
- Standard dimensions

### File Management
- Automatic directory creation
- Company-specific naming
- Existence checking
- Batch cleanup options

## 💡 Best Practices

### For Resume Content
- **Clean structure**: Clear section headers
- **Consistent formatting**: Standard layout
- **Professional content**: Industry-standard terminology
- **Complete information**: Full resume details

### For PDF Generation
- **Company-specific naming**: Use company names for tracking
- **Batch processing**: Generate multiple versions at once
- **Organized storage**: Keep PDFs in dedicated directory
- **Version tracking**: Track which version for which job

### For Integration
- **Text editing**: Edit in text format (AI-friendly)
- **PDF delivery**: Generate PDF for final delivery
- **Quality control**: Review PDFs before submission
- **Backup management**: Keep original text versions

## 📈 Performance Metrics

- **Speed**: <1 second per PDF generation
- **File Size**: ~4KB per typical resume
- **Quality**: Professional formatting
- **Reliability**: Graceful error handling

## 🎯 Example Use Cases

### Use Case 1: Multiple Job Applications
```python
jobs = fetch_jobs("Python Developer")

for job in jobs:
    company_name = extract_company(job['url'])
    optimized = optimize_resume(base_resume, job['description'])
    pdf_path = builder.build(optimized, "resume.pdf", company_name)
    apply_with_pdf(job['url'], pdf_path)
```

### Use Case 2: A/B Testing
```python
# Generate different versions
version_a = optimize_resume(base_resume, job_desc, style="professional")
version_b = optimize_resume(base_resume, job_desc, style="creative")

pdf_a = builder.build(version_a, "resume_professional.pdf")
pdf_b = builder.build(version_b, "resume_creative.pdf")
```

### Use Case 3: Career Transition
```python
# Tailored versions for different industries
tech_resume = optimize_for_tech(base_resume)
finance_resume = optimize_for_finance(base_resume)

pdf_tech = builder.build(tech_resume, "resume_tech.pdf")
pdf_finance = builder.build(finance_resume, "resume_finance.pdf")
```

## 🔮 Future Enhancements

- [ ] Custom resume templates
- [] Color scheme options
- [] Cover letter integration
- [ ] Multiple page layouts
- [] Image/photo support
- [ ] Digital signature support
- [ ] PDF encryption options

## 📝 Notes

- Uses reportlab for PDF generation
- Professional formatting built-in
- Company-specific automatic naming
- Batch processing support
- ATS-compatible output
- Cross-platform compatible

## 🛠️ Setup Requirements

1. **Dependencies**: `reportlab` package installed
2. **Configuration**: PDF settings in `config/job_search.yaml`
3. **Resume**: Text resume in `resumes/base_resume.txt`
4. **Directory**: Output directory automatically created

## 🎯 Complete Workflow

```
Base Resume (Text) → AI Optimization → Company-Specific Text → PDF Generation → Application
        ↓                  ↓                    ↓                  ↓              ↓
    Easy to Edit       Job-Tailored      Organized by      Professional    Submit with
   AI-Friendly        Enhanced           Company           Format         Correct PDF
```

## 📁 File Organization

```
resumes/
├── base_resume.txt              # Original text resume
├── tailored/                     # AI-optimized text versions
│   ├── google.txt
│   ├── amazon.txt
│   └── microsoft.txt
└── pdfs/                        # Generated PDF files
    ├── resume_google.pdf
    ├── resume_amazon.pdf
    └── resume_microsoft.pdf
```

---

**The PDF builder creates professional company-specific resumes for job applications!** 📄

# Super Resumer - User Guide

## 🎯 Overview

Super Resumer is a personalized AI-powered job application system designed for your C# and Python AI job search in Bangalore with 7+ LPA salary requirement.

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd "/Users/shaku/Desktop/AI_PROJECTS_SHAKU/Super resumer"
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env` file:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key  # Optional fallback
```

### 3. Add Your Resumes

Place your resumes in the `resumes/` folder:
- `csharp_developer.pdf` - Your C# developer resume
- `python_ai_developer.pdf` - Your Python AI developer resume

Or update the text placeholders:
- `csharp_developer.txt` - Update with your C# experience
- `python_ai_developer.txt` - Update with your Python AI experience

### 4. Run the Application

```bash
streamlit run run_super_resumer.py
```

The dashboard will open at `http://localhost:8501`

## 🔧 Configuration

### Job Search Settings

Edit `core/config.py` to customize:

```python
# Location and Salary
LOCATION = "Bangalore"
MIN_SALARY_LPA = 7

# Target Roles
TARGET_ROLES = [
    "Software Developer", 
    "C# Developer", 
    "Python AI Developer", 
    "AI Engineer"
]

# Match Threshold
MATCH_THRESHOLD = 85  # 85% required
```

### Job Sources

Configure which sources to scrape:
- LinkedIn (requires credentials)
- Indeed
- Naukri
- Company websites

## 🎮 How It Works

### Workflow

1. **Job Discovery**: Scrapes jobs from configured sources
2. **Filtering**: Filters by location (Bangalore), salary (7+ LPA), and roles
3. **AI Matching**: Uses RAG to match job descriptions with your resumes
4. **Resume Selection**: Automatically selects C# or Python AI resume based on tech stack
5. **Manual Review**: You review matched jobs and decide to apply

### Resume Selection Logic

- **C# Roles**: Jobs requiring C#, .NET, ASP.NET skills
- **Python AI Roles**: Jobs requiring Python, ML, AI, NLP skills
- **Match Score**: Must be 85% or higher to proceed to review

## 📊 Dashboard Features

### Status Categories

- **🔍 All Jobs**: Complete job listing
- **✅ Applied**: Jobs you've applied to
- **👀 Under Review**: Jobs pending your decision
- **❌ Rejected**: Jobs that didn't match criteria
- **⏳ Pending**: Jobs awaiting action

### Job Actions

For each job, you can:
- **✅ Mark as Applied**: Record that you've applied
- **👀 Under Review**: Keep under consideration
- **❌ Reject**: Remove from consideration
- **🔗 Apply Now**: Open the job application link

### Statistics Dashboard

Real-time statistics show:
- Total jobs found
- Jobs applied
- Under review
- Rejected
- Pending action

## 🤖 AI Features

### RAG-Based Matching

- Uses LangChain for semantic search
- Matches job descriptions with your resume content
- Provides detailed match analysis
- Scores from 0-100%

### Tech Stack Detection

Automatically detects:
- C#/.NET roles → Uses C# resume
- Python/AI roles → Uses Python AI resume
- Mixed roles → Uses best matching resume

### OpenRouter Integration

- Uses OpenRouter API for AI processing
- Falls back to OpenAI if needed
- Configurable model selection

## 🔍 Job Sources

### Currently Supported

- **LinkedIn**: Manual entry or API (requires credentials)
- **Indeed**: Basic scraping
- **Naukri**: Basic scraping
- **Company Websites**: Configurable target companies

### Adding New Sources

To add new job sources:
1. Extend `SuperResumerJobScraper` class
2. Add scraping logic in `agents/super_resumer_scraper.py`
3. Update configuration in `core/config.py`

## 📝 Resume Management

### Resume Requirements

- **C# Resume**: Focus on .NET, C#, Azure, SQL Server
- **Python AI Resume**: Focus on Python, ML, AI, NLP, frameworks
- **Format**: PDF or TXT supported
- **Content**: Detailed skills, experience, projects

### Updating Resumes

1. Update resume files in `resumes/` folder
2. Click "Load Resumes" in dashboard sidebar
3. System will re-index with new content

## ⚠️ Important Notes

### Manual Application Workflow

This system uses **manual application**:
- System finds and matches jobs
- You review and apply manually
- You track application status
- No automated applications (for safety)

### Rate Limiting

- Respects website rate limits
- Delays between requests
- Human-like browsing patterns

### Data Privacy

- Your resume data stays local
- Job data stored locally
- No external data sharing
- Secure credential handling

## 🐛 Troubleshooting

### Common Issues

**API Key Not Working**
- Check OpenRouter API key is valid
- Ensure sufficient credits
- Try OpenAI fallback

**Resume Not Loading**
- Check file path in config
- Ensure file is readable
- Try .txt format instead of .pdf

**No Jobs Found**
- Check job sources are enabled
- Verify location and salary filters
- Check internet connection

**Matching Score Low**
- Ensure resume content is detailed
- Update resume with relevant skills
- Adjust match threshold in config

## 🎯 Best Practices

### For Best Results

1. **Detailed Resumes**: Include specific skills and technologies
2. **Regular Updates**: Keep resumes current with latest skills
3. **Target Roles**: Configure specific roles you're interested in
4. **Regular Searches**: Run searches weekly for new opportunities
5. **Prompt Action**: Review and apply to matched jobs quickly

### Job Search Strategy

1. Start with broad search criteria
2. Review high-match jobs first
3. Customize applications for each role
4. Track application status in dashboard
5. Follow up on applications

## 🔮 Future Enhancements

Planned features:
- Automated application with approval
- Email notifications for new jobs
- Application status tracking
- Interview scheduling integration
- Salary negotiation assistance
- Cover letter generation

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review logs in `logs/` directory
- Verify configuration settings
- Ensure all dependencies are installed

## 🎉 Success Tips

1. **Keep Resumes Updated**: Regular update skills and experience
2. **Broaden Search**: Don't limit to exact role matches
3. **Apply Promptly**: Good jobs get filled quickly
4. **Customize Applications**: Tailor each application
5. **Follow Up**: Don't hesitate to follow up on applications

---

**Happy Job Hunting! 🚀**
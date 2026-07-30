# AI Job Agent

An intelligent AI-powered job application system that automates:

- Job discovery
- Resume tailoring
- ATS optimization
- Multi-platform applications
- AI-generated responses
- Dashboard analytics

## 🚀 Super Resumer Mode

**Personalized version for C# and Python AI roles in Bangalore**

- **Dual Resume System**: Automatically selects C# or Python AI resume based on job requirements
- **85% Match Threshold**: Strict matching using RAG and LangChain
- **Manual Workflow**: System finds jobs → You review and apply
- **Bangalore Focus**: 7+ LPA salary requirement
- **Multi-Source**: LinkedIn, Indeed, Naukri, company websites

**Quick Start for Super Resumer:**

```bash
pip install -r requirements.txt
# Add your OpenRouter API key to .env
streamlit run run_super_resumer.py
```

See [Super Resumer Guide](docs/SUPER_RESUMER_GUIDE.md) for detailed setup.

## Features

### Job Discovery

Automatically discovers jobs from:

- LinkedIn
- Workday
- Greenhouse
- Lever

### Resume Intelligence

- ATS-friendly resume tailoring
- Job-specific optimization
- AI keyword enhancement

### Automation

- Auto-fill applications
- Session persistence
- Retry system
- Duplicate prevention

### Dashboard

- Job tracking
- Application analytics
- Interview tracking
- Error monitoring

## Tech Stack

Python  
Selenium  
OpenAI API  
SQLite  
Streamlit  
Docker

## Architecture

Job Scraper
↓
AI Matcher
↓
Resume Optimizer
↓
Apply Engine
↓
Dashboard

## Setup

pip install -r requirements.txt

streamlit run ui/dashboard.py

## Screenshots

_Note: Screenshots need to be taken. See `screenshots/QUICK_START_SCREENSHOTS.md` for instructions._

### Dashboard Overview

![Dashboard Overview](screenshots/dashboard_overview.png)

### Job Tracking

![Job Tracking](screenshots/job_tracking_table.png)

### Resume Tailoring

![Resume Tailoring](screenshots/resume_tailoring_example.png)

### Application Log

![Application Log](screenshots/successful_apply_log.png)

### Architecture

![Architecture](screenshots/architecture_diagram.png)

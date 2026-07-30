# 🤖 AI Job Application Bot - Scheduler System

## 📋 Overview

The Background Job Scheduler enables automatic, continuous job application processing. It runs 24/7, constantly checking for new jobs and applying to those that match your profile.

## 🚀 Quick Start

### 1. Configuration

Set up your `.env` file:

```bash
OPENAI_API_KEY=your_actual_openai_key_here
SCHEDULER_INTERVAL_MINUTES=5
ENABLE_AI_MATCHING=true
MATCH_THRESHOLD=0.85
```

### 2. Run the Bot

```bash
# Run the main bot (continuous operation)
python run_bot.py

# Or run tests
python test_scheduler.py              # Single cycle test
python test_scheduler.py continuous   # Continuous test
```

## 📁 Files Created

### Core Scheduler Files:
- **`scheduler.py`** - Basic scheduler (simple version)
- **`scheduler_enhanced.py`** - Enhanced scheduler with logging & error handling
- **`run_bot.py`** - Main entry point for production use

### Testing & Mock Data:
- **`mock_jobs_feed.py`** - Mock job feed for testing (replace with real scraping)
- **`test_scheduler.py`** - Scheduler testing scripts

### Enhanced Orchestrator:
- **`automation/orchestrator.py`** - Updated with AI-powered matching

## 🔧 How It Works

### 1. Continuous Operation
```
┌─────────────────────────────────────┐
│  Scheduler checks for new jobs      │
│         (every 5 minutes)          │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Jobs Feed returns latest jobs      │
│  (LinkedIn, Indeed, etc.)           │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│  Orchestrator processes each job    │
│  - AI matching (semantic + keyword) │
│  - Threshold filtering              │
│  - AI answer generation             │
│  - Automated application            │
└──────────────┬──────────────────────┘
               │
               ▼
        ┌──────────────┐
        │  Sleep 5 min │
        └──────┬───────┘
               │
               └──────────┘
```

### 2. AI-Powered Matching

The enhanced orchestrator now uses:

1. **Keyword Matching** (`JobMatcher`)
   - Extracts skills from job description
   - Matches against user's skills
   - Calculates compatibility score

2. **Semantic Matching** (`SemanticMatcher`)
   - Uses OpenAI embeddings
   - Understands context and meaning
   - Detects subtle similarities

3. **Combined Scoring**
   - 70% semantic similarity
   - 30% keyword matching
   - Configurable threshold (default 0.85)

## 🔌 Integration Options

### Replace Mock Feed with Real Data

Edit `mock_jobs_feed.py` or create your own feed:

```python
class RealJobsFeed:
    def get_latest_jobs(self):
        # Scrape LinkedIn Jobs
        # Call Indeed API
        # Monitor company career pages
        # Return list of job dictionaries
        return jobs
```

### Job Dictionary Format:
```python
{
    "role": "Senior Python Developer",
    "company": "Tech Corp",
    "salary": "$120k",
    "location": "Remote",
    "job_url": "https://linkedin.com/jobs/123",
    "description": "Full job description text...",
    "match_score": 0.85  # Optional, will be calculated by AI
}
```

## ⚙️ Configuration Options

### Environment Variables:
- `SCHEDULER_INTERVAL_MINUTES` - Check interval (default: 5)
- `ENABLE_AI_MATCHING` - Use AI matching (default: true)
- `MATCH_THRESHOLD` - Minimum match score (default: 0.85)
- `USE_SEMANTIC_MATCHING` - Enable semantic matching (default: true)

### Scheduler Modes:

**Continuous Mode** (Production):
```bash
python run_bot.py
# Runs indefinitely, checking jobs every 5 minutes
```

**Single Cycle Mode** (Testing):
```python
scheduler.run_single_cycle(jobs_feed)
# Processes jobs once and exits
```

## 📊 Monitoring & Logging

The enhanced scheduler includes:
- ✅ Detailed logging with `loguru`
- ✅ Error handling and recovery
- ✅ Job processing statistics
- ✅ Timestamp-based tracking

### Log Output:
```
2024-05-25 14:55:00 | INFO | Checking for new jobs...
2024-05-25 14:55:01 | INFO | Found 3 new jobs to process
2024-05-25 14:55:02 | INFO | Processing job: Senior Python Developer
2024-05-25 14:55:03 | INFO | Keyword score: 0.80, Semantic score: 0.90, Combined: 0.87
2024-05-25 14:55:04 | INFO | Applying to: Senior Python Developer (match: 0.87)
2024-05-25 14:55:05 | INFO | Successfully applied to: Senior Python Developer
```

## 🛠️ Troubleshooting

### Common Issues:

**Bot not applying to jobs:**
- Check `MATCH_THRESHOLD` in .env
- Verify your profile skills are set
- Ensure job descriptions are being fetched

**Scheduler not running:**
- Check Python dependencies: `pip install -r requirements.txt`
- Verify OPENAI_API_KEY is set
- Check logs for specific errors

**High API costs:**
- Increase `SCHEDULER_INTERVAL_MINUTES`
- Disable semantic matching if not needed
- Use keyword matching only

## 🚦 Next Steps

1. **Replace Mock Feed** - Implement real job scraping
2. **Configure Thresholds** - Tune match scores for your needs
3. **Set Up Monitoring** - Add alerts for failures
4. **Deploy** - Run on server/cloud for 24/7 operation

## 🎯 Current Status

✅ **Part 5 Complete:**
- ✅ Background job scheduler created
- ✅ Enhanced orchestrator with AI matching
- ✅ Semantic + keyword matching
- ✅ Continuous operation support
- ✅ Error handling & logging
- ✅ Configuration management

🤖 **Your AI Job Application Bot is now ready for automatic operation!**
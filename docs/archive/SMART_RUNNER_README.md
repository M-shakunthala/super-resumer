# 🚀 Smart Job Search Automation System

An intelligent job search automation system that coordinates multiple components for efficient job hunting.

## 📁 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CONFIGURATION                            │
│                  config/job_search.yaml                      │
└────────────────────────┬────────────────────────────────────┘
                         │
    ┌────────────────────┼────────────────────┐
    │                    │                    │
┌───▼────┐        ┌──────▼──────┐     ┌──────▼──────┐
│SCRAPER │        │  FILTER     │     │   RANKER    │
│LinkedIn│───────▶│ Experience  │────▶│   Score     │
│Jobs    │        │ Level       │     │   Sort      │
└───┬────┘        └──────┬──────┘     └──────┬──────┘
    │                    │                    │
    │                    │                    │
    └────────────────────┼────────────────────┘
                         │
                    ┌────▼────┐
                    │ MEMORY  │
                    │ Duplicate│
                    │ Tracking │
                    └────┬────┘
                         │
                    ┌────▼────┐
                    │ORCHESTRA│
                    │  TOR    │
                    │Process  │
                    └─────────┘
```

## 🔧 Components

### 1. **Config System** (`core/config.py`)
- Loads job search parameters from YAML
- Centralized configuration management
- Easy to modify without code changes

### 2. **Job Scraper** (`agents/job_scraper.py`) 
- Fetches real jobs from LinkedIn
- Browser automation with Selenium
- Session persistence for login state

### 3. **Job Filter** (`agents/job_filter.py`)
- Filters senior-level roles
- Configurable blacklist
- Experience-appropriate jobs only

### 4. **Job Ranker** (`agents/job_ranker.py`)
- Prioritizes jobs by match score
- Filters below threshold
- Limits to top N jobs

### 5. **Job Memory** (`memory/job_memory.py`)
- SQLite database for tracking
- Duplicate detection
- Status management

### 6. **Orchestrator** (`core/orchestrator.py`)
- Coordinates job processing workflow
- Simulates AI-powered processing
- Status tracking and reporting

## 📋 Configuration (`config/job_search.yaml`)

```yaml
keywords:
  - "Python Developer"
  - "Backend Developer" 
  - "Software Engineer"

locations:
  - "Bengaluru"
  - "Remote"

profile_skills:
  - "python"
  - "sql"
  - "c#"

title_blacklist:
  - "senior"
  - "lead"
  - "architect"
  - "manager"

ranking:
  min_score_threshold: 0.5
  max_ranked_jobs: 20
```

## 🚀 Usage

### Basic Usage
```bash
python3 run.py
```

### Simulation Mode
```bash
python3 test_run_simulation.py
```

### Component Testing
```bash
# Test individual components
python3 test_job_filter.py
python3 test_job_ranker.py
python3 test_full_pipeline.py
```

## 🔍 Workflow

1. **Load Configuration** - Read search parameters from YAML
2. **Initialize Components** - Set up scraper, filter, ranker, memory, orchestrator
3. **Iterate Search Combinations** - For each keyword × location:
   - **Scrape Jobs** - Fetch from LinkedIn
   - **Check Duplicates** - Skip already processed jobs
   - **Filter Experience** - Remove senior/lead roles
   - **Rank by Score** - Prioritize best matches
   - **Process Jobs** - Run through orchestrator
   - **Track Status** - Save results to memory
4. **Report Results** - Summary of processed jobs
5. **Cleanup** - Close browser and database connections

## 🎯 Key Features

### ✅ Intelligent Filtering
- No more senior role applications when you're entry-level
- Configurable blacklist for role types
- Skills-based matching

### ✅ Smart Ranking  
- Best jobs first based on match score
- Configurable minimum score threshold
- Limits to prevent overwhelming results

### ✅ Duplicate Prevention
- SQLite database tracking
- Never apply to the same job twice
- Status history for each job

### ✅ Config-Driven
- Change search parameters without code
- Easy A/B testing of different strategies
- Profile skills in one place

### ✅ Progress Tracking
- Real-time console output
- Success/failure tracking
- Memory statistics

## 📊 Test Results

```
🚀 SIMULATING intelligent job search automation...
Keywords: ['Python Developer', 'Backend Developer', 'Software Engineer']
Locations: ['Bengaluru', 'Remote']
Profile Skills: ['python', 'sql', 'c#']

🔍 Searching: 'Python Developer' in 'Bengaluru'
   Found 8 raw jobs
   ❌ Filtering senior role: Senior Python Developer
   ✅ 5 valid jobs after filtering
   🤖 Processing: Backend Developer (score: 0.9)
   ✅ Applied successfully

🎯 Simulation complete!
Total jobs processed: 5
Successful applications: 5
```

## 🛠️ Future Enhancements

- [ ] Real AI-powered job matching
- [ ] Automatic resume tailoring
- [ ] Email notifications
- [ ] Scheduler integration
- [ ] Multiple job board support
- [ ] Advanced analytics dashboard

## 🔒 Safety Features

- Browser session persistence
- Duplicate job detection  
- Experience level filtering
- Status tracking and retry logic
- Graceful error handling

## 📝 Notes

- **Browser**: Uses Chrome with session persistence
- **Database**: SQLite for job tracking
- **Configuration**: YAML for easy modification
- **Logging**: Console output for monitoring

This system transforms job hunting from manual to intelligent automation! 🎯

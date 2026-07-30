# Testing Quick Reference

## Stage 1: Manual Watch (3 Jobs)
```bash
python3 run_stage1.py /path/to/resume.pdf
```
**Goal**: Validate flow: open → apply → upload → submit
**Success**: 3/3 jobs, 0 crashes, manual validation complete
**Time**: ~15 minutes

## Stage 2: Crash Detection (10 Jobs)
```bash
python3 run_stage2.py /path/to/resume.pdf
```
**Goal**: No crashes during automated execution
**Success**: 10/10 processed, 0 crashes
**Time**: ~30 minutes

## Stage 3: Stability Test (25 Jobs)
```bash
python3 run_stage3.py /path/to/resume.pdf
```
**Goal**: Stable unattended execution
**Success**: ≥20/25 successful (80%), 0 crashes
**Time**: ~60 minutes

## All Stages (Sequential)
```bash
python3 test_linkedin_apply_stages.py --resume /path/to/resume.pdf
```

## Before Testing
1. ✅ Resume ready (PDF format)
2. ✅ Real LinkedIn job URLs in code
3. ✅ LinkedIn account logged in
4. ✅ Enough time for stage completion

## During Testing
- Monitor console output
- Watch logs in `logs/` directory
- Check `test_jobs.db` for status
- Note any errors or issues

## After Testing
- Review success metrics
- Check logs for issues
- Fix any problems found
- Only proceed if stage passes

## Files Created
- `test_linkedin_apply_stages.py` - Main framework
- `run_stage1.py` - Stage 1 script
- `run_stage2.py` - Stage 2 script
- `run_stage3.py` - Stage 3 script
- `logs/job_agent.log` - All activity
- `logs/errors_job_agent.log` - Errors only
- `test_jobs.db` - Job status database

## Success Criteria Summary
| Stage | Jobs | Success Rate | Crashes |
|-------|------|--------------|---------|
| 1     | 3    | 100% (3/3)   | 0       |
| 2     | 10   | N/A          | 0       |
| 3     | 25   | ≥80% (20+)   | 0       |

## Quick Troubleshooting
- **Stage 1 fails**: Check selectors, resume path, form filling
- **Stage 2 crashes**: Improve error handling, add retries
- **Stage 3 unstable**: Check session persistence, resource management

## Production Readiness
Only after ALL stages pass:
- ✅ Success rate ≥80% in Stage 3
- ✅ Zero crashes across all stages
- ✅ Stable resource usage
- ✅ Comprehensive error handling

**Remember**: Don't skip stages. Each validates critical functionality.

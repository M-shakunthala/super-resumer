from scheduler_enhanced import Scheduler
from mock_jobs_feed import MockJobsFeed


def test_scheduler_basic():
    """Test the basic scheduler with mock jobs"""
    print("Testing Basic Scheduler...")
    print("=" * 50)
    
    # Create a mock jobs feed
    jobs_feed = MockJobsFeed()
    
    # Create scheduler with 1-minute intervals for testing
    scheduler = Scheduler(check_interval_minutes=1)
    
    # Run a single cycle for testing
    scheduler.run_single_cycle(jobs_feed)


def test_scheduler_continuous():
    """Test continuous scheduler (runs until interrupted)"""
    print("Testing Continuous Scheduler...")
    print("=" * 50)
    print("Press Ctrl+C to stop the scheduler")
    print()
    
    # Create a mock jobs feed
    jobs_feed = MockJobsFeed()
    
    # Create scheduler with 2-minute intervals
    scheduler = Scheduler(check_interval_minutes=2)
    
    # Run continuously
    scheduler.run_continuously(jobs_feed)


def test_scheduler_basic_original():
    """Test the original simple scheduler"""
    from scheduler import Scheduler as BasicScheduler
    
    print("Testing Original Basic Scheduler...")
    print("=" * 50)
    
    # Create a mock jobs feed
    jobs_feed = MockJobsFeed()
    
    # Create basic scheduler
    scheduler = BasicScheduler()
    
    # Note: This will run indefinitely, so we'll modify it for testing
    # In production, use: scheduler.run_continuously(jobs_feed)
    print("Original scheduler created successfully")
    print("To run continuously: scheduler.run_continuously(jobs_feed)")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "continuous":
        test_scheduler_continuous()
    elif len(sys.argv) > 1 and sys.argv[1] == "original":
        test_scheduler_basic_original()
    else:
        test_scheduler_basic()

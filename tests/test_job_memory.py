#!/usr/bin/env python3
"""
Test script for upgraded job memory system
Validates duplicate filtering and status management
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_agent.memory.job_memory import (
    JobMemory, 
    JobStatus, 
    check_duplicate, 
    record_application
)


def test_job_memory_initialization():
    """Test that JobMemory can be initialized"""
    try:
        memory = JobMemory(":memory:")  # Use in-memory database for testing
        if memory is None:
            print("❌ JobMemory initialization failed - returned None")
            return False
        
        print("✅ JobMemory initialization successful")
        return True
    except Exception as e:
        print(f"❌ JobMemory initialization test failed: {e}")
        return False


def test_database_schema():
    """Test that database schema is created correctly"""
    try:
        memory = JobMemory(":memory:")
        
        # Check that table exists
        cur = memory.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='jobs'"
        )
        if cur.fetchone() is None:
            print("❌ Jobs table not created")
            return False
        
        # Check table structure
        cur = memory.conn.execute("PRAGMA table_info(jobs)")
        columns = [row['name'] for row in cur.fetchall()]
        
        required_columns = ['url', 'status', 'first_seen', 'last_updated', 'retry_count', 'company', 'position']
        for col in required_columns:
            if col not in columns:
                print(f"❌ Missing required column: {col}")
                return False
        
        print("✅ Database schema created correctly")
        return True
    except Exception as e:
        print(f"❌ Database schema test failed: {e}")
        return False


def test_save_and_exists():
    """Test save and exists functionality"""
    try:
        memory = JobMemory(":memory:")
        
        # Initially should not exist
        if memory.exists("https://example.com/job1"):
            print("❌ Job exists before saving")
            return False
        
        # Save job
        memory.save("https://example.com/job1")
        
        # Now should exist
        if not memory.exists("https://example.com/job1"):
            print("❌ Job doesn't exist after saving")
            return False
        
        print("✅ Save and exists functionality works")
        return True
    except Exception as e:
        print(f"❌ Save and exists test failed: {e}")
        return False


def test_status_management():
    """Test status management"""
    try:
        memory = JobMemory(":memory:")
        
        # Test different statuses
        memory.save("https://example.com/job1", JobStatus.APPLIED.value)
        status = memory.get_status("https://example.com/job1")
        if status != JobStatus.APPLIED.value:
            print(f"❌ Status mismatch: expected {JobStatus.APPLIED.value}, got {status}")
            return False
        
        # Test mark methods
        memory.mark_failed("https://example.com/job2")
        if memory.get_status("https://example.com/job2") != JobStatus.FAILED.value:
            print("❌ mark_failed failed")
            return False
        
        memory.mark_skipped("https://example.com/job3")
        if memory.get_status("https://example.com/job3") != JobStatus.SKIPPED.value:
            print("❌ mark_skipped failed")
            return False
        
        print("✅ Status management works")
        return True
    except Exception as e:
        print(f"❌ Status management test failed: {e}")
        return False


def test_should_skip_logic():
    """Test duplicate filtering logic"""
    try:
        memory = JobMemory(":memory:")
        
        # New job should not be skipped
        should_skip, reason = memory.should_skip("https://example.com/new")
        if should_skip:
            print(f"❌ New job incorrectly marked for skip: {reason}")
            return False
        
        # Applied job should be skipped
        memory.mark_applied("https://example.com/applied")
        should_skip, reason = memory.should_skip("https://example.com/applied")
        if not should_skip or reason != "Already applied":
            print(f"❌ Applied job not skipped correctly: {reason}")
            return False
        
        # Skipped job should be skipped
        memory.mark_skipped("https://example.com/skipped")
        should_skip, reason = memory.should_skip("https://example.com/skipped")
        if not should_skip or reason != "Previously skipped":
            print(f"❌ Skipped job not skipped correctly: {reason}")
            return False
        
        # Failed job with low retry count should not be skipped
        memory.mark_failed("https://example.com/failed")
        should_skip, reason = memory.should_skip("https://example.com/failed")
        if should_skip:
            print(f"❌ Failed job incorrectly marked for skip: {reason}")
            return False
        
        # Failed job with high retry count should be skipped
        for i in range(4):  # Exceed retry limit
            memory.mark_failed("https://example.com/failed_many")
        
        should_skip, reason = memory.should_skip("https://example.com/failed_many")
        if not should_skip or "giving up" not in reason:
            print(f"❌ Failed job with many retries not skipped: {reason}")
            return False
        
        print("✅ Duplicate filtering logic works correctly")
        return True
    except Exception as e:
        print(f"❌ Duplicate filtering logic test failed: {e}")
        return False


def test_get_jobs_by_status():
    """Test filtering jobs by status"""
    try:
        memory = JobMemory(":memory:")
        
        # Add jobs with different statuses
        memory.save("https://example.com/job1", JobStatus.APPLIED.value)
        memory.save("https://example.com/job2", JobStatus.FAILED.value)
        memory.save("https://example.com/job3", JobStatus.APPLIED.value)
        
        applied_jobs = memory.get_jobs_by_status(JobStatus.APPLIED.value)
        if len(applied_jobs) != 2:
            print(f"❌ Expected 2 applied jobs, got {len(applied_jobs)}")
            return False
        
        failed_jobs = memory.get_jobs_by_status(JobStatus.FAILED.value)
        if len(failed_jobs) != 1:
            print(f"❌ Expected 1 failed job, got {len(failed_jobs)}")
            return False
        
        print("✅ Get jobs by status works")
        return True
    except Exception as e:
        print(f"❌ Get jobs by status test failed: {e}")
        return False


def test_get_stats():
    """Test statistics functionality"""
    try:
        memory = JobMemory(":memory:")
        
        # Add some jobs
        memory.save("https://example.com/job1", JobStatus.NEW.value)
        memory.save("https://example.com/job2", JobStatus.APPLIED.value)
        memory.save("https://example.com/job3", JobStatus.FAILED.value)
        
        stats = memory.get_stats()
        
        if stats['total'] != 3:
            print(f"❌ Expected total 3, got {stats['total']}")
            return False
        
        if stats[JobStatus.NEW.value] != 1:
            print(f"❌ Expected 1 new job, got {stats[JobStatus.NEW.value]}")
            return False
        
        if stats[JobStatus.APPLIED.value] != 1:
            print(f"❌ Expected 1 applied job, got {stats[JobStatus.APPLIED.value]}")
            return False
        
        print("✅ Statistics functionality works")
        return True
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False


def test_convenience_functions():
    """Test convenience functions"""
    try:
        # Use temporary database file
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".db") as tmp:
            db_path = tmp.name
        
        try:
            # Test check_duplicate
            should_skip, reason = check_duplicate("https://example.com/test", db_path)
            if should_skip:
                print(f"❌ New job marked as duplicate: {reason}")
                return False
            
            # Test record_application
            record_application("https://example.com/test", True, db_path)
            
            # Check that it's now marked as applied
            should_skip, reason = check_duplicate("https://example.com/test", db_path)
            if not should_skip or "already applied" not in reason.lower():
                print(f"❌ Applied job not marked as duplicate: {reason}")
                return False
            
            print("✅ Convenience functions work")
            return True
        finally:
            # Cleanup temp file
            import os
            if os.path.exists(db_path):
                os.remove(db_path)
    
    except Exception as e:
        print(f"❌ Convenience functions test failed: {e}")
        return False


def test_context_manager():
    """Test context manager functionality"""
    try:
        with JobMemory(":memory:") as memory:
            memory.save("https://example.com/test")
            if not memory.exists("https://example.com/test"):
                print("❌ Context manager save failed")
                return False
        
        # Connection should be closed now
        print("✅ Context manager works")
        return True
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing Upgraded Job Memory System")
    print("=" * 50)
    
    tests = [
        test_job_memory_initialization,
        test_database_schema,
        test_save_and_exists,
        test_status_management,
        test_should_skip_logic,
        test_get_jobs_by_status,
        test_get_stats,
        test_convenience_functions,
        test_context_manager,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("=" * 50)
    print(f"Test Results: {sum(results)}/{len(results)} passed")
    print("=" * 50)
    
    if all(results):
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

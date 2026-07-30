#!/usr/bin/env python3
"""
Test script for standard logging system
Validates implementation and features
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_agent.infra.standard_logger import (
    get_logger,
    setup_logging,
    info,
    error,
    warning,
    debug,
    critical,
    OperationTimer
)


def test_logger_import():
    """Test that logger can be imported"""
    try:
        from job_agent.infra.standard_logger import get_logger, setup_logging
        print("✅ Standard logger import successful")
        return True
    except ImportError as e:
        print(f"❌ Standard logger import failed: {e}")
        return False


def test_logger_initialization():
    """Test that logger can be initialized"""
    try:
        logger = get_logger()
        if logger is None:
            print("❌ Logger initialization failed - returned None")
            return False
        
        if not hasattr(logger, 'logger'):
            print("❌ Logger missing logger attribute")
            return False
        
        print("✅ Logger initialization successful")
        return True
    except Exception as e:
        print(f"❌ Logger initialization test failed: {e}")
        return False


def test_basic_logging_methods():
    """Test basic logging methods"""
    try:
        logger = get_logger()
        
        # Test all basic methods
        logger.info("Test info message")
        logger.error("Test error message")
        logger.warning("Test warning message")
        logger.debug("Test debug message")
        logger.critical("Test critical message")
        
        print("✅ Basic logging methods work")
        return True
    except Exception as e:
        print(f"❌ Basic logging methods test failed: {e}")
        return False


def test_convenience_functions():
    """Test convenience functions"""
    try:
        info("Convenience info")
        error("Convenience error")
        warning("Convenience warning")
        debug("Convenience debug")
        critical("Convenience critical")
        
        print("✅ Convenience functions work")
        return True
    except Exception as e:
        print(f"❌ Convenience functions test failed: {e}")
        return False


def test_specialized_logging_methods():
    """Test specialized logging methods"""
    try:
        logger = get_logger()
        
        logger.log_application("Google", "Software Engineer", True)
        logger.log_application("Facebook", "Data Scientist", False)
        logger.log_scraping("LinkedIn", 25)
        logger.log_login("LinkedIn", True)
        
        print("✅ Specialized logging methods work")
        return True
    except Exception as e:
        print(f"❌ Specialized logging methods test failed: {e}")
        return False


def test_structured_logging():
    """Test structured logging"""
    try:
        logger = get_logger()
        
        logger.log_structured("info", {"job": "Engineer", "company": "Tech Corp"})
        logger.log_structured("error", {"error": "Timeout", "url": "https://example.com"})
        
        print("✅ Structured logging works")
        return True
    except Exception as e:
        print(f"❌ Structured logging test failed: {e}")
        return False


def test_timer_functionality():
    """Test operation timer"""
    try:
        logger = get_logger()
        
        import time
        with logger.start_timer("Test Operation"):
            time.sleep(0.5)
        
        print("✅ Timer functionality works")
        return True
    except Exception as e:
        print(f"❌ Timer functionality test failed: {e}")
        return False


def test_log_file_creation():
    """Test that log files are created"""
    try:
        logger = get_logger()
        log_files = logger.get_log_files()
        
        if len(log_files) == 0:
            print("❌ No log files created")
            return False
        
        # Check that files actually exist
        for log_file in log_files:
            if not os.path.exists(log_file):
                print(f"❌ Log file does not exist: {log_file}")
                return False
        
        print(f"✅ Log files created: {len(log_files)} files")
        return True
    except Exception as e:
        print(f"❌ Log file creation test failed: {e}")
        return False


def test_log_level_setting():
    """Test changing log level"""
    try:
        import logging
        logger = get_logger()
        
        # Change to debug level
        logger.set_level(logging.DEBUG)
        logger.debug("Debug message after level change")
        
        # Change back to info level
        logger.set_level(logging.INFO)
        
        print("✅ Log level setting works")
        return True
    except Exception as e:
        print(f"❌ Log level setting test failed: {e}")
        return False


def test_context_manager():
    """Test OperationTimer context manager"""
    try:
        logger = get_logger()
        
        import time
        with logger.start_timer("Context Test"):
            time.sleep(0.3)
        
        print("✅ Context manager works")
        return True
    except Exception as e:
        print(f"❌ Context manager test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing Standard Logging System")
    print("=" * 50)
    
    tests = [
        test_logger_import,
        test_logger_initialization,
        test_basic_logging_methods,
        test_convenience_functions,
        test_specialized_logging_methods,
        test_structured_logging,
        test_timer_functionality,
        test_log_file_creation,
        test_log_level_setting,
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
        print(f"\n📝 Log files created in: logs/")
        print(f"   - job_agent.log (all logs)")
        print(f"   - errors_job_agent.log (errors only)")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

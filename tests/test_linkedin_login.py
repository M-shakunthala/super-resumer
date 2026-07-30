#!/usr/bin/env python3
"""
Test script for LinkedIn login persistence checker
Demonstrates usage and validates implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automation.linkedin_login import LinkedInLogin, check_linkedin_login_status, get_linkedin_session_info


def test_linkedin_login_import():
    """Test that LinkedInLogin can be imported"""
    try:
        from automation.linkedin_login import LinkedInLogin
        print("✅ LinkedInLogin import successful")
        return True
    except ImportError as e:
        print(f"❌ LinkedInLogin import failed: {e}")
        return False


def test_linkedin_login_methods():
    """Test that LinkedInLogin has all required methods"""
    try:
        methods = [
            'is_logged_in',
            'get_login_status_details',
            'wait_for_login',
            'check_session_validity',
            'ensure_logged_in',
        ]
        
        for method in methods:
            if not hasattr(LinkedInLogin, method):
                print(f"❌ LinkedInLogin missing method: {method}")
                return False
        
        print(f"✅ LinkedInLogin has all {len(methods)} required methods")
        return True
    except Exception as e:
        print(f"❌ LinkedInLogin methods test failed: {e}")
        return False


def test_convenience_functions():
    """Test that convenience functions are available"""
    try:
        from automation.linkedin_login import check_linkedin_login_status, get_linkedin_session_info
        
        if not callable(check_linkedin_login_status):
            print("❌ check_linkedin_login_status not callable")
            return False
        
        if not callable(get_linkedin_session_info):
            print("❌ get_linkedin_session_info not callable")
            return False
        
        print("✅ Convenience functions available and callable")
        return True
    except Exception as e:
        print(f"❌ Convenience functions test failed: {e}")
        return False


def test_linkedin_login_initialization():
    """Test that LinkedInLogin can be instantiated"""
    try:
        checker = LinkedInLogin()
        
        # Check that it has the expected attributes
        if not hasattr(checker, 'login_url'):
            print("❌ LinkedInLogin missing login_url attribute")
            return False
        
        if not hasattr(checker, 'login_check_selectors'):
            print("❌ LinkedInLogin missing login_check_selectors attribute")
            return False
        
        # Check that selectors are properly configured
        if len(checker.login_check_selectors) == 0:
            print("❌ LinkedInLogin has no login check selectors")
            return False
        
        print(f"✅ LinkedInLogin initialization successful with {len(checker.login_check_selectors)} selectors")
        return True
    except Exception as e:
        print(f"❌ LinkedInLogin initialization test failed: {e}")
        return False


def test_browser_manager_integration():
    """Test that BrowserManager has LinkedIn login methods"""
    try:
        from job_agent.infra.browser import BrowserManager
        
        methods = [
            'check_linkedin_login',
            'ensure_linkedin_session',
        ]
        
        for method in methods:
            if not hasattr(BrowserManager, method):
                print(f"❌ BrowserManager missing method: {method}")
                return False
        
        print("✅ BrowserManager LinkedIn login integration successful")
        return True
    except Exception as e:
        print(f"❌ BrowserManager integration test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing LinkedIn Login Persistence Checker")
    print("=" * 50)
    
    tests = [
        test_linkedin_login_import,
        test_linkedin_login_methods,
        test_convenience_functions,
        test_linkedin_login_initialization,
        test_browser_manager_integration,
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

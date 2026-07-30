#!/usr/bin/env python3
"""
Test script for SafeActions functionality
This demonstrates the usage and validates the implementation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from job_agent.infra.safe_actions import SafeActions
from job_agent.infra.waits import Waits
from job_agent.infra.browser import BrowserManager


def test_safe_actions_import():
    """Test that SafeActions can be imported"""
    try:
        from job_agent.infra.safe_actions import SafeActions
        print("✅ SafeActions import successful")
        return True
    except ImportError as e:
        print(f"❌ SafeActions import failed: {e}")
        return False


def test_waits_import():
    """Test that Waits can be imported"""
    try:
        from job_agent.infra.waits import Waits
        print("✅ Waits import successful")
        return True
    except ImportError as e:
        print(f"❌ Waits import failed: {e}")
        return False


def test_browser_manager_integration():
    """Test that BrowserManager has safe actions integrated"""
    try:
        from job_agent.infra.browser import BrowserManager
        
        # Check that safe action methods are available
        methods = [
            'safe_click',
            'safe_send_keys', 
            'safe_hover',
            'safe_double_click',
            'safe_get_text',
            'safe_get_attribute'
        ]
        
        for method in methods:
            if not hasattr(BrowserManager, method):
                print(f"❌ BrowserManager missing method: {method}")
                return False
        
        print("✅ BrowserManager safe actions integration successful")
        return True
    except Exception as e:
        print(f"❌ BrowserManager integration test failed: {e}")
        return False


def test_safe_actions_methods():
    """Test that SafeActions has all required methods"""
    try:
        methods = [
            'safe_click',
            'safe_send_keys',
            'safe_select_by_text',
            'safe_select_by_value',
            'safe_select_by_index',
            'safe_hover',
            'safe_double_click',
            'safe_right_click',
            'safe_drag_and_drop',
            'safe_get_text',
            'safe_get_attribute',
            'safe_is_displayed',
            'safe_is_enabled'
        ]
        
        for method in methods:
            if not hasattr(SafeActions, method):
                print(f"❌ SafeActions missing method: {method}")
                return False
        
        print(f"✅ SafeActions has all {len(methods)} required methods")
        return True
    except Exception as e:
        print(f"❌ SafeActions methods test failed: {e}")
        return False


def test_waits_methods():
    """Test that Waits has all required methods"""
    try:
        methods = [
            'clickable',
            'visible',
            'present',
            'text_present',
            'title_contains',
            'url_contains',
            'frame_available',
            'staleness',
            'all_visible',
            'any_visible',
            'page_loaded',
            'ajax_complete'
        ]
        
        for method in methods:
            if not hasattr(Waits, method):
                print(f"❌ Waits missing method: {method}")
                return False
        
        print(f"✅ Waits has all {len(methods)} required methods")
        return True
    except Exception as e:
        print(f"❌ Waits methods test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing Safe Actions Implementation")
    print("=" * 50)
    
    tests = [
        test_safe_actions_import,
        test_waits_import,
        test_browser_manager_integration,
        test_safe_actions_methods,
        test_waits_methods
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

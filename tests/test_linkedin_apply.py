#!/usr/bin/env python3
"""
Test script for improved LinkedIn Apply Engine
Validates implementation and available methods
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from automation.linkedin_apply import LinkedInApply


def test_linkedin_apply_import():
    """Test that LinkedInApply can be imported"""
    try:
        from automation.linkedin_apply import LinkedInApply
        print("✅ LinkedInApply import successful")
        return True
    except ImportError as e:
        print(f"❌ LinkedInApply import failed: {e}")
        return False


def test_linkedin_apply_methods():
    """Test that LinkedInApply has all required methods"""
    try:
        methods = [
            '__init__',
            '_get_driver',
            '_ensure_logged_in',
            '_find_easy_apply_button',
            '_fill_form_fields',
            '_upload_resume',
            '_submit_application',
            'apply',
            'apply_batch',
            'close',
        ]
        
        for method in methods:
            if not hasattr(LinkedInApply, method):
                print(f"❌ LinkedInApply missing method: {method}")
                return False
        
        print(f"✅ LinkedInApply has all {len(methods)} required methods")
        return True
    except Exception as e:
        print(f"❌ LinkedInApply methods test failed: {e}")
        return False


def test_linkedin_apply_initialization():
    """Test that LinkedInApply can be instantiated"""
    try:
        # Test with headless=False (default)
        apply_engine = LinkedInApply(headless=False)
        
        # Check that it has the expected attributes
        if not hasattr(apply_engine, 'browser_manager'):
            print("❌ LinkedInApply missing browser_manager attribute")
            return False
        
        if not hasattr(apply_engine, 'login_checker'):
            print("❌ LinkedInApply missing login_checker attribute")
            return False
        
        print("✅ LinkedInApply initialization successful")
        return True
    except Exception as e:
        print(f"❌ LinkedInApply initialization test failed: {e}")
        return False


def test_infrastructure_integration():
    """Test that infrastructure modules are properly integrated"""
    try:
        from automation.linkedin_apply import (
            BrowserManager,
            Waits,
            SafeActions,
            LinkedInLogin,
            FormFiller
        )
        
        print("✅ All infrastructure modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Infrastructure import failed: {e}")
        return False


def test_selector_arrays():
    """Test that selector arrays are properly defined"""
    try:
        apply_engine = LinkedInApply(headless=False)
        
        # Access private method to check selectors
        import inspect
        
        # Check easy apply selectors
        easy_apply_method = apply_engine._find_easy_apply_button
        source = inspect.getsource(easy_apply_method)
        
        if "easy_apply_selectors" in source and len(source) > 100:
            print("✅ Easy apply selectors properly defined")
        else:
            print("❌ Easy apply selectors not properly defined")
            return False
        
        # Check upload selectors
        upload_method = apply_engine._upload_resume
        source = inspect.getsource(upload_method)
        
        if "upload_selectors" in source and len(source) > 100:
            print("✅ Upload selectors properly defined")
        else:
            print("❌ Upload selectors not properly defined")
            return False
        
        # Check submit selectors
        submit_method = apply_engine._submit_application
        source = inspect.getsource(submit_method)
        
        if "submit_selectors" in source and len(source) > 100:
            print("✅ Submit selectors properly defined")
        else:
            print("❌ Submit selectors not properly defined")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Selector arrays test failed: {e}")
        return False


def test_apply_return_structure():
    """Test that apply method returns proper structure"""
    try:
        import inspect
        
        apply_engine = LinkedInApply(headless=False)
        apply_method = apply_engine.apply
        source = inspect.getsource(apply_method)
        
        # Check for result dictionary structure
        result_keys = [
            '"success"',
            '"job_url"',
            '"resume_uploaded"',
            '"form_filled"',
            '"submitted"',
            '"error"',
            '"message"'
        ]
        
        for key in result_keys:
            if key not in source:
                print(f"❌ Result missing key: {key}")
                return False
        
        print("✅ Apply method returns proper result structure")
        return True
    except Exception as e:
        print(f"❌ Apply return structure test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 50)
    print("Testing Improved LinkedIn Apply Engine")
    print("=" * 50)
    
    tests = [
        test_linkedin_apply_import,
        test_linkedin_apply_methods,
        test_linkedin_apply_initialization,
        test_infrastructure_integration,
        test_selector_arrays,
        test_apply_return_structure,
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

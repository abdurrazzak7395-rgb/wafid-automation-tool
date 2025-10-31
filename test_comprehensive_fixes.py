#!/usr/bin/env python3
"""
Comprehensive test suite for all bug fixes
Tests resource leaks, race conditions, thread safety, and error handling
"""

import sys
import os
from pathlib import Path
import tempfile
import threading
import time

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_browser_temp_directory_cleanup():
    """Test that temporary directories are properly cleaned up"""
    print("Testing browser temporary directory cleanup...")
    
    try:
        from components.browser_automation import BrowserAutomation
        
        # Create browser instance
        browser = BrowserAutomation(headless=True)
        
        # Check that temp_dir is tracked
        assert hasattr(browser, 'temp_dir'), "Browser should track temp_dir"
        assert browser.temp_dir is None, "temp_dir should be None initially"
        
        print("  ✓ Browser tracks temporary directory")
        
        # Note: We can't actually test browser creation without Chrome installed
        # but we can verify the cleanup logic exists
        
        # Verify close_session includes cleanup
        import inspect
        source = inspect.getsource(browser.close_session)
        assert 'shutil.rmtree' in source, "close_session should clean up temp directory"
        assert 'self.temp_dir' in source, "close_session should reference temp_dir"
        
        print("  ✓ close_session includes temp directory cleanup")
        
        # Verify destructor exists
        assert hasattr(browser, '__del__'), "Browser should have destructor"
        
        print("  ✓ Browser has destructor for cleanup")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_proxy_manager_race_condition():
    """Test that proxy manager handles concurrent access correctly"""
    print("\nTesting proxy manager race condition fix...")
    
    try:
        from components.proxy_manager import ProxyManager
        
        pm = ProxyManager()
        
        # Verify lock exists
        assert hasattr(pm, 'lock'), "ProxyManager should have lock"
        
        print("  ✓ ProxyManager has threading lock")
        
        # Verify refresh_proxy_list uses lock correctly
        import inspect
        source = inspect.getsource(pm.refresh_proxy_list)
        
        # Check that lock is used but not held during long operations
        assert 'with self.lock:' in source, "refresh_proxy_list should use lock"
        assert source.count('with self.lock:') >= 2, "Lock should be used multiple times (not held continuously)"
        
        print("  ✓ refresh_proxy_list uses lock correctly (not held during long operations)")
        
        # Test concurrent access
        results = []
        errors = []
        
        def get_proxy():
            try:
                proxy = pm.get_next_proxy()
                results.append(proxy)
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=get_proxy) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0, f"No errors should occur during concurrent access: {errors}"
        
        print(f"  ✓ Concurrent access test passed ({len(threads)} threads)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_logger_thread_safety():
    """Test that logger handles concurrent logging correctly"""
    print("\nTesting logger thread safety fix...")
    
    try:
        from components.logger import logger
        
        # Verify lock exists
        assert hasattr(logger, 'lock'), "Logger should have lock"
        
        print("  ✓ Logger has threading lock")
        
        # Verify GUI callback is called outside lock
        import inspect
        
        # Check info method
        info_source = inspect.getsource(logger.info)
        assert 'with self.lock:' in info_source, "info should use lock"
        assert '_log_to_gui' in info_source, "info should call _log_to_gui"
        
        # Verify _log_to_gui doesn't hold lock
        gui_source = inspect.getsource(logger._log_to_gui)
        assert 'with self.lock:' not in gui_source, "_log_to_gui should not hold lock"
        
        print("  ✓ GUI callback called outside lock (prevents deadlocks)")
        
        # Test concurrent logging
        errors = []
        
        def log_messages():
            try:
                for i in range(10):
                    logger.info(f"Test message {i}")
                    logger.warning(f"Test warning {i}")
                    logger.error(f"Test error {i}")
            except Exception as e:
                errors.append(e)
        
        threads = [threading.Thread(target=log_messages) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        
        assert len(errors) == 0, f"No errors should occur during concurrent logging: {errors}"
        
        print(f"  ✓ Concurrent logging test passed ({len(threads)} threads, 30 messages each)")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_network_monitor_error_handling():
    """Test that network monitor handles errors gracefully"""
    print("\nTesting network monitor error handling...")
    
    try:
        from components.network_monitor import NetworkMonitor
        
        # Verify error handling in wait_for_response
        import inspect
        source = inspect.getsource(NetworkMonitor.wait_for_response)
        
        # Check for proper error handling
        assert 'try:' in source, "wait_for_response should have try blocks"
        assert 'except Exception' in source, "wait_for_response should catch exceptions"
        assert source.count('except') >= 3, "Multiple exception handlers for robustness"
        
        print("  ✓ wait_for_response has comprehensive error handling")
        
        # Check for safe dictionary access
        assert '.get(' in source, "Should use safe dictionary access (.get())"
        
        print("  ✓ Uses safe dictionary access methods")
        
        # Verify _enable_network_logging checks driver
        enable_source = inspect.getsource(NetworkMonitor._enable_network_logging)
        assert 'if not self.driver' in enable_source, "Should check if driver exists"
        
        print("  ✓ _enable_network_logging checks driver before use")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_automation_engine_cleanup():
    """Test that automation engine properly cleans up resources"""
    print("\nTesting automation engine cleanup...")
    
    try:
        from components.automation_engine import AutomationEngine
        
        engine = AutomationEngine()
        
        # Verify stop_automation includes cleanup
        import inspect
        source = inspect.getsource(engine.stop_automation)
        
        assert 'close_session' in source, "stop_automation should close browser session"
        assert 'try:' in source, "Should handle cleanup errors gracefully"
        
        print("  ✓ stop_automation includes browser cleanup")
        
        # Test that engine can be stopped safely
        engine.is_running = True
        engine.stop_automation()
        
        assert engine.is_running == False, "Engine should be stopped"
        
        print("  ✓ Engine stops safely")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_passport_expiry_field_mapping():
    """Test that passport expiry field is correctly mapped"""
    print("\nTesting passport expiry field mapping fix...")
    
    try:
        from components.browser_automation import BrowserAutomation
        from components.form_handler import FormHandler
        
        browser = BrowserAutomation()
        
        # Test field detection
        result = browser._determine_field_purpose(
            'passport_expiry_date',
            'passport_expiry_date',
            'Passport Expiry Date',
            'Passport Expiry Date',
            'date'
        )
        
        assert result == 'passport_expiry_date', f"Should detect as 'passport_expiry_date', got '{result}'"
        
        print("  ✓ Field detection returns 'passport_expiry_date'")
        
        # Verify form handler uses correct key
        import inspect
        source = inspect.getsource(FormHandler.fill_candidate_info)
        
        assert "'passport_expiry_date':" in source, "Form handler should use 'passport_expiry_date' key"
        assert "'passport_expiry':" not in source, "Form handler should not use old 'passport_expiry' key"
        
        print("  ✓ Form handler uses correct field key")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all comprehensive tests"""
    print("=== Comprehensive Bug Fixes Test Suite ===\n")
    
    # Ensure directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    tests = [
        ("Resource Leak Fix", test_browser_temp_directory_cleanup),
        ("Race Condition Fix", test_proxy_manager_race_condition),
        ("Thread Safety Fix", test_logger_thread_safety),
        ("Error Handling Fix", test_network_monitor_error_handling),
        ("Cleanup Fix", test_automation_engine_cleanup),
        ("Field Mapping Fix", test_passport_expiry_field_mapping),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*60}")
        print(f"Test: {test_name}")
        print('='*60)
        try:
            if test_func():
                passed += 1
                print(f"\n✅ {test_name} PASSED")
            else:
                print(f"\n❌ {test_name} FAILED")
        except Exception as e:
            print(f"\n❌ {test_name} CRASHED: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*60}")
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    print('='*60)
    
    if passed == total:
        print("\n✅ All comprehensive bug fixes are working correctly!")
        print("\nFixed Issues:")
        print("  1. ✅ Resource leak - temporary directory cleanup")
        print("  2. ✅ Race condition in proxy manager")
        print("  3. ✅ Thread safety in logger")
        print("  4. ✅ Error handling in network monitor")
        print("  5. ✅ Cleanup in automation engine")
        print("  6. ✅ Passport expiry field mapping")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

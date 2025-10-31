#!/usr/bin/env python3
"""
Test suite for URL configuration functionality
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

def test_url_validation():
    """Test URL validation logic"""
    print("Testing URL validation...")
    
    try:
        from components.automation_engine import AutomationEngine
        
        engine = AutomationEngine()
        
        # Test valid URLs
        valid_urls = [
            "https://wafid.com/book-appointment",
            "http://localhost:8000/booking",
            "https://booking.example.com/appointments",
            "https://medical-center.org/book",
        ]
        
        for url in valid_urls:
            result = engine.set_booking_url(url)
            if result:
                print(f"  ✓ Valid URL accepted: {url}")
            else:
                print(f"  ✗ Valid URL rejected: {url}")
                return False
        
        # Test invalid URLs
        invalid_urls = [
            "",  # Empty
            "wafid.com/book",  # Missing protocol
            "ftp://wafid.com/book",  # Wrong protocol
            "https://",  # Missing domain
            "https:// wafid.com",  # Space in URL
            "not a url",  # Invalid format
        ]
        
        for url in invalid_urls:
            result = engine.set_booking_url(url)
            if not result:
                print(f"  ✓ Invalid URL rejected: '{url}'")
            else:
                print(f"  ✗ Invalid URL accepted: '{url}'")
                return False
        
        print(f"\n✅ URL validation test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_loading():
    """Test configuration loading from config.json"""
    print("\nTesting configuration loading...")
    
    try:
        from components.automation_engine import AutomationEngine
        import json
        import tempfile
        
        # Create a temporary config file
        config_data = {
            "automation": {
                "booking_url": "https://test-booking.com/appointments",
                "max_retries": 50
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_file = f.name
            json.dump(config_data, f)
        
        try:
            # Initialize engine with custom config
            engine = AutomationEngine(config_file=config_file)
            
            # Verify URL was loaded
            if engine.booking_url == "https://test-booking.com/appointments":
                print(f"  ✓ URL loaded from config: {engine.booking_url}")
            else:
                print(f"  ✗ URL not loaded correctly: {engine.booking_url}")
                return False
            
            # Verify max_retries was loaded
            if engine.max_retries == 50:
                print(f"  ✓ max_retries loaded from config: {engine.max_retries}")
            else:
                print(f"  ✗ max_retries not loaded correctly: {engine.max_retries}")
                return False
            
            print(f"\n✅ Configuration loading test passed")
            return True
            
        finally:
            # Clean up temp file
            os.unlink(config_file)
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_default_url():
    """Test that default URL is used when config is missing"""
    print("\nTesting default URL fallback...")
    
    try:
        from components.automation_engine import AutomationEngine
        
        # Initialize with non-existent config file
        engine = AutomationEngine(config_file="nonexistent_config.json")
        
        # Should fall back to default URL
        if engine.booking_url == "https://wafid.com/book-appointment":
            print(f"  ✓ Default URL used: {engine.booking_url}")
        else:
            print(f"  ✗ Unexpected URL: {engine.booking_url}")
            return False
        
        print(f"\n✅ Default URL fallback test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_url_update():
    """Test runtime URL updates"""
    print("\nTesting runtime URL updates...")
    
    try:
        from components.automation_engine import AutomationEngine
        
        engine = AutomationEngine()
        
        initial_url = engine.booking_url
        print(f"  Initial URL: {initial_url}")
        
        # Update URL
        new_url = "https://new-booking-site.com/appointments"
        if engine.set_booking_url(new_url):
            print(f"  ✓ URL updated successfully")
        else:
            print(f"  ✗ URL update failed")
            return False
        
        # Verify update
        if engine.booking_url == new_url:
            print(f"  ✓ URL verified: {engine.booking_url}")
        else:
            print(f"  ✗ URL not updated: {engine.booking_url}")
            return False
        
        print(f"\n✅ Runtime URL update test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_url_whitespace_handling():
    """Test that URLs with whitespace are handled correctly"""
    print("\nTesting whitespace handling...")
    
    try:
        from components.automation_engine import AutomationEngine
        
        engine = AutomationEngine()
        
        # URL with leading/trailing whitespace
        url_with_whitespace = "  https://wafid.com/book-appointment  "
        if engine.set_booking_url(url_with_whitespace):
            if engine.booking_url == "https://wafid.com/book-appointment":
                print(f"  ✓ Whitespace trimmed correctly")
            else:
                print(f"  ✗ Whitespace not trimmed: '{engine.booking_url}'")
                return False
        else:
            print(f"  ✗ Valid URL with whitespace rejected")
            return False
        
        # URL with internal whitespace (should be rejected)
        url_with_internal_space = "https://wafid .com/book"
        if not engine.set_booking_url(url_with_internal_space):
            print(f"  ✓ URL with internal spaces rejected")
        else:
            print(f"  ✗ URL with internal spaces accepted")
            return False
        
        print(f"\n✅ Whitespace handling test passed")
        return True
        
    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all URL configuration tests"""
    print("=== URL Configuration Test Suite ===\n")
    
    # Ensure directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    tests = [
        ("URL Validation", test_url_validation),
        ("Config Loading", test_config_loading),
        ("Default URL Fallback", test_default_url),
        ("Runtime URL Update", test_url_update),
        ("Whitespace Handling", test_url_whitespace_handling),
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
        print("\n✅ All URL configuration tests passed!")
        print("\nURL Configuration Features:")
        print("  1. ✅ URL validation (protocol, format, domain)")
        print("  2. ✅ Config file loading")
        print("  3. ✅ Default URL fallback")
        print("  4. ✅ Runtime URL updates")
        print("  5. ✅ Whitespace handling")
        return True
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

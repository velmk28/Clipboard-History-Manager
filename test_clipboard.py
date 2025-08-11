#!/usr/bin/env python3
"""
Simple test script to verify clipboard functionality
"""

import pyperclip
import time

def test_clipboard():
    """Test basic clipboard operations"""
    print("Testing clipboard functionality...")
    
    # Test 1: Write to clipboard
    test_text = "Hello from Clipboard Manager Test! 🧪"
    print(f"Writing to clipboard: {test_text}")
    pyperclip.copy(test_text)
    
    # Wait a moment
    time.sleep(1)
    
    # Test 2: Read from clipboard
    read_text = pyperclip.paste()
    print(f"Read from clipboard: {read_text}")
    
    # Test 3: Verify
    if read_text == test_text:
        print("✅ Clipboard test PASSED!")
        return True
    else:
        print("❌ Clipboard test FAILED!")
        print(f"Expected: {test_text}")
        print(f"Got: {read_text}")
        return False

def test_multiple_copies():
    """Test multiple clipboard operations"""
    print("\nTesting multiple clipboard operations...")
    
    test_items = [
        "First clipboard item",
        "Second clipboard item with numbers: 12345",
        "https://www.example.com",
        "Multi-line\nclipboard\ncontent"
    ]
    
    for i, item in enumerate(test_items, 1):
        print(f"Copying item {i}: {item[:30]}...")
        pyperclip.copy(item)
        time.sleep(0.5)
        
        # Verify
        read_item = pyperclip.paste()
        if read_item == item:
            print(f"  ✅ Item {i} copied successfully")
        else:
            print(f"  ❌ Item {i} failed")
            return False
    
    print("✅ Multiple clipboard test PASSED!")
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("CLIPBOARD FUNCTIONALITY TEST")
    print("=" * 50)
    
    try:
        # Test basic functionality
        basic_test = test_clipboard()
        
        if basic_test:
            # Test multiple operations
            multiple_test = test_multiple_copies()
            
            if multiple_test:
                print("\n🎉 All tests PASSED! Clipboard is working correctly.")
                print("You can now run the main application: python clipboard_manager.py")
            else:
                print("\n❌ Multiple clipboard test failed.")
        else:
            print("\n❌ Basic clipboard test failed.")
            
    except ImportError:
        print("❌ pyperclip module not found!")
        print("Please install it with: pip install pyperclip")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    input("Press Enter to exit...")

#!/usr/bin/env python3
"""
Demo script for Clipboard History Manager
Simulates various clipboard operations to showcase features
"""

import pyperclip
import time
import random

def demo_clipboard_operations():
    """Demonstrate various clipboard operations"""
    print("🎬 Clipboard History Manager Demo")
    print("=" * 50)
    print("This demo will copy various types of content to your clipboard.")
    print("Open the Clipboard History Manager to see them appear in real-time!")
    print("=" * 50)
    
    demo_items = [
        ("Simple text", "Hello, this is a simple text message!"),
        ("URL", "https://www.example.com"),
        ("Number", "12345"),
        ("Multi-line text", "This is a\nmulti-line\nclipboard item"),
        ("Long text", "This is a much longer piece of text that demonstrates how the clipboard manager handles content of varying lengths. It should be automatically categorized as 'Text' type."),
        ("Email", "user@example.com"),
        ("Code snippet", "def hello_world():\n    print('Hello, World!')"),
        ("Phone number", "+1-555-123-4567"),
        ("Date", "2024-01-15"),
        ("Emoji text", "🚀 🎉 ✨ Amazing clipboard content! 🎯 🏆")
    ]
    
    print("Starting demo in 3 seconds...")
    for i in range(3, 0, -1):
        print(f"  {i}...")
        time.sleep(1)
    
    print("\n🎯 Demo started! Copying items to clipboard...")
    print("=" * 50)
    
    for i, (description, content) in enumerate(demo_items, 1):
        print(f"📋 Item {i}: {description}")
        print(f"   Content: {content[:50]}{'...' if len(content) > 50 else ''}")
        
        # Copy to clipboard
        pyperclip.copy(content)
        
        # Wait a bit
        time.sleep(2)
        
        # Verify it was copied
        current_clipboard = pyperclip.paste()
        if current_clipboard == content:
            print(f"   ✅ Successfully copied to clipboard")
        else:
            print(f"   ❌ Failed to copy to clipboard")
        
        print()
    
    print("🎉 Demo completed!")
    print("=" * 50)
    print("Check your Clipboard History Manager to see all the items!")
    print("Try searching, filtering, and copying items back to clipboard.")
    print("=" * 50)

def interactive_demo():
    """Interactive demo mode"""
    print("\n🎮 Interactive Demo Mode")
    print("=" * 50)
    print("You can now manually copy items to see them appear in the manager.")
    print("Commands:")
    print("  'quit' - Exit demo")
    print("  'status' - Show current clipboard content")
    print("  'help' - Show this help")
    print("=" * 50)
    
    while True:
        try:
            command = input("\nEnter command (or just copy something): ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'status':
                current = pyperclip.paste()
                print(f"Current clipboard: {current[:100]}{'...' if len(current) > 100 else ''}")
            elif command == 'help':
                print("Commands: quit, status, help")
            elif command:
                print("Unknown command. Type 'help' for available commands.")
            else:
                # Check if clipboard changed
                current = pyperclip.paste()
                if current:
                    print(f"📋 Clipboard updated: {current[:100]}{'...' if len(current) > 100 else ''}")
                
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")
            

def main():
    """Main demo function"""
    print("Welcome to the Clipboard History Manager Demo!")
    print("=" * 60)
    
    # Check if pyperclip is available
    try:
        import pyperclip
    except ImportError:
        print("❌ pyperclip not found. Please install it first:")
        print("pip install pyperclip")
        return
    
    print("Choose demo mode:")
    print("1. Automatic demo (copy various items automatically)")
    print("2. Interactive demo (you control the clipboard)")
    print("3. Exit")
    
    
    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                demo_clipboard_operations()
                break
            elif choice == '2':
                interactive_demo()
                break
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n\nDemo interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            

if __name__ == "__main__":
    main()

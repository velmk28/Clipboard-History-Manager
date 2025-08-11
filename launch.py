#!/usr/bin/env python3
"""
Clipboard History Manager Launcher
Provides a nice startup experience and error handling
"""

import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    try:
        import tkinter
    except ImportError:
        missing_deps.append("tkinter (should be included with Python)")
    
    try:
        import pyperclip
    except ImportError:
        missing_deps.append("pyperclip")
    
    return missing_deps

def install_dependencies():
    """Install missing dependencies"""
    try:
        print("Installing missing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("Failed to install dependencies automatically.")
        return False

def show_error_dialog(title, message):
    """Show error dialog"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror(title, message)
    root.destroy()

def main():
    """Main launcher function"""
    print("=" * 50)
    print("📋 Clipboard History Manager Launcher")
    print("=" * 50)
    
    # Check dependencies
    missing_deps = check_dependencies()
    
    if missing_deps:
        print(f"Missing dependencies: {', '.join(missing_deps)}")
        
        if "pyperclip" in missing_deps:
            print("\nAttempting to install pyperclip...")
            if install_dependencies():
                print("Retrying dependency check...")
                missing_deps = check_dependencies()
            else:
                print("\nPlease install dependencies manually:")
                print("pip install pyperclip")
                input("Press Enter to exit...")
                return
        
        if missing_deps:
            error_msg = f"Missing dependencies: {', '.join(missing_deps)}\n\nPlease install them manually."
            show_error_dialog("Missing Dependencies", error_msg)
            return
    
    print("✅ All dependencies available!")
    print("🚀 Starting Clipboard History Manager...")
    print("=" * 50)
    
    try:
        # Import and run the main application
        from clipboard_manager import main as run_app
        run_app()
    except Exception as e:
        error_msg = f"Failed to start application:\n{str(e)}"
        print(f"❌ {error_msg}")
        show_error_dialog("Application Error", error_msg)

if __name__ == "__main__":
    main()

#!/bin/bash

echo "Starting Clipboard History Manager..."
echo ""
echo "If this is your first time running the app, you may need to install dependencies:"
echo "pip install -r requirements.txt"
echo ""

# Check if Python is available
if command -v python3 &> /dev/null; then
    python3 clipboard_manager.py
elif command -v python &> /dev/null; then
    python clipboard_manager.py
else
    echo "Error: Python not found. Please install Python 3.6 or higher."
    exit 1
fi

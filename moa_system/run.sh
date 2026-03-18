#!/bin/bash

# MOA & Legal Opinion Tracking System - Startup Script
# This script runs the application on Unix-like systems

echo "Starting MOA & Legal Opinion Tracking System..."
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Failed to start the application."
    echo ""
    echo "Make sure:"
    echo "1. Python 3.8 or higher is installed"
    echo "2. Dependencies are installed: pip install -r requirements.txt"
    echo "3. You're running this script from the moa_system folder"
    echo ""
    read -p "Press Enter to exit..."
fi

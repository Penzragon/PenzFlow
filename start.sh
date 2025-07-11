#!/bin/bash

# PenzFlow ERP & SFA System Startup Script

echo "🏢 Starting PenzFlow ERP & SFA System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Start the application
echo "Starting Streamlit application..."
echo "Access your ERP system at: http://localhost:8501"
echo ""
echo "Default login credentials:"
echo "  Admin: username: admin, password: admin123"
echo "  Demo:  username: demo,  password: demo"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run src/main.py

#!/bin/bash

# SARA Web Interface Startup Script

echo "============================================"
echo "🌐 SARA Web Interface Startup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "✅ Python 3 detected"

# Install requirements if they don't exist
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found"
    exit 1
fi

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
mkdir -p uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

echo "📁 Directory structure created"

# Check if sara.py exists
if [ ! -f "sara.py" ]; then
    echo "⚠️  Warning: sara.py not found. Some features may not work properly."
    echo "   Please ensure you're in the SARA directory and the original files are present."
fi

echo ""
echo "🚀 Starting SARA Web Interface..."
echo "📍 Web interface will be available at: http://localhost:5000"
echo ""
echo "⚠️  WARNING: This tool is for educational purposes only!"
echo "   The author is not responsible for any misuse."
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask application
python3 app.py
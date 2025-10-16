#!/bin/bash

echo "🚀 Starting AIDA Demo Setup (Flask Only)..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python nu este instalat!"
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd aida-backend
pip install -r requirements.txt

echo "✅ Setup complet!"
echo ""
echo "🎯 Pentru a rula demo-ul:"
echo "1. python app.py"
echo "2. Deschide index.html în browser"
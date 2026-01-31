#!/bin/bash
# iOS Test Automator - Streamlit UI Launcher

set -e

echo "🚀 iOS Test Automator - Streamlit UI"
echo "===================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Check if backend is running
echo "🔍 Checking backend status..."
BACKEND_URL="http://localhost:8000"
if curl -s "${BACKEND_URL}/health" > /dev/null 2>&1; then
    echo "✅ Backend is running"
else
    echo "⚠️  Backend is not running!"
    echo ""
    echo "Please start the backend first:"
    echo "  cd ../python-backend"
    echo "  source venv/bin/activate"
    echo "  python main.py"
    echo ""
    read -p "Press Enter to continue anyway, or Ctrl+C to exit..."
fi

echo ""
echo "🌐 Starting Streamlit UI..."
echo "   URL: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run Streamlit
streamlit run app.py

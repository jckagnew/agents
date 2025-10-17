#!/bin/bash
# Job Search Assistant - Easy Startup Script

echo "🎯 Starting Job Search Assistant..."
echo "=================================="

# Change to the correct directory
cd "$(dirname "$0")"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the job-search-assistant directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run 'uv sync' first"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../.venv/bin/activate

# Install/update the package
echo "📦 Installing/updating package..."
uv run pip install -e . > /dev/null 2>&1

# Start the server
echo "🚀 Starting server on http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=================================="

# Start the server
uv run uvicorn src.job_search_assistant.api.main:app --reload --host 127.0.0.1 --port 8000

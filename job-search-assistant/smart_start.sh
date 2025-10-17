#!/bin/bash
# Smart Job Search Assistant Launcher with Resilience

echo "🎯 Job Search Assistant - Smart Launcher"
echo "========================================"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "📁 Working directory: $(pwd)"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Not in job-search-assistant directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "💡 Run: cd /Users/jackagnew/projects/agents && uv sync"
    exit 1
fi

# Check for port conflicts
echo "🔍 Checking for port conflicts..."
if command -v lsof >/dev/null 2>&1; then
    if lsof -i :8000 >/dev/null 2>&1; then
        echo "⚠️  Port 8000 is in use. Finding alternative port..."
        for port in 8001 8002 8003 8004 8005; do
            if ! lsof -i :$port >/dev/null 2>&1; then
                echo "✅ Found available port: $port"
                PORT=$port
                break
            fi
        done
        if [ -z "$PORT" ]; then
            echo "❌ No available ports found. Please close some applications."
            exit 1
        fi
    else
        echo "✅ Port 8000 is available"
        PORT=8000
    fi
else
    echo "⚠️  lsof not available, assuming port 8000 is free"
    PORT=8000
fi

# Install/update package
echo "📦 Installing/updating package..."
uv run pip install -e . > /dev/null 2>&1

# Start the server
echo "🚀 Starting server on port $PORT..."
echo "📚 API Documentation: http://localhost:$PORT/docs"
echo "❤️  Health Check: http://localhost:$PORT/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"

# Start the server
uv run python -m uvicorn src.job_search_assistant.api.main:app --reload --host 127.0.0.1 --port $PORT

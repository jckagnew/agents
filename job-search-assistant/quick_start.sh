#!/bin/bash
# Quick Start Script for Job Search Assistant

echo "🎯 Job Search Assistant - Quick Start"
echo "====================================="

# Change to the job-search-assistant directory
cd "$(dirname "$0")"

echo "🚀 Starting server..."
echo "📚 API Documentation will open at: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "====================================="

# Start the server
uv run python -m uvicorn src.job_search_assistant.api.main:app --reload --host 127.0.0.1 --port 8000

#!/bin/bash
# Job Search Assistant Setup Script

set -e

echo "🚀 Setting up Job Search Assistant..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3.11+ is required but not installed."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 3.11+ is required. Found: $PYTHON_VERSION"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
python3 -m pip install --upgrade pip
pip install -e ".[dev]"

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
npm install

# Install pre-commit hooks
echo "🔧 Setting up pre-commit hooks..."
pre-commit install

# Install Playwright browsers
echo "🎭 Installing Playwright browsers..."
npx playwright install

# Set up environment variables
echo "🔐 Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file from .env.example"
    echo "⚠️  Please update .env with your API keys and configuration"
fi

# Set up database
echo "🗄️  Setting up database..."
python3 -c "
from src.services.database import engine
from src.models.job_opportunity import Base
Base.metadata.create_all(bind=engine)
print('✅ Database tables created')
"

# Run initial tests
echo "🧪 Running initial tests..."
pytest tests/unit -v

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Update .env with your API keys"
echo "2. Run 'python main.py' to start the job search"
echo "3. Run 'npm run dev' to start the frontend"
echo "4. Run 'pytest' to run all tests"
echo ""
echo "📚 Documentation:"
echo "- README.md - Project overview"
echo "- DEVELOPMENT_PLAN.md - Development phases"
echo "- docs/ - Detailed documentation"

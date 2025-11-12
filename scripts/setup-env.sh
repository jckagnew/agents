#!/bin/bash

# ===================================================================
# Environment Setup Script
# Creates master .env file from template
# ===================================================================

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"
EXAMPLE_FILE="$ROOT_DIR/.env.example"

echo "🔧 Environment Setup for Design-First Software Factory"
echo "======================================================"
echo ""

# Check if .env already exists
if [ -f "$ENV_FILE" ]; then
    echo "⚠️  Master .env file already exists at: $ENV_FILE"
    echo ""
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "✅ Keeping existing .env file"
        exit 0
    fi
fi

# Check if .env.example exists
if [ ! -f "$EXAMPLE_FILE" ]; then
    echo "❌ Error: .env.example not found at: $EXAMPLE_FILE"
    exit 1
fi

# Copy template
echo "📋 Copying .env.example to .env..."
cp "$EXAMPLE_FILE" "$ENV_FILE"

echo "✅ Created master .env file at: $ENV_FILE"
echo ""
echo "📝 Next steps:"
echo ""
echo "1. Edit the .env file and add your real credentials:"
echo "   nano $ENV_FILE"
echo ""
echo "2. Required credentials to fill in:"
echo "   - SUPABASE_URL (from design-factory-admin project)"
echo "   - SUPABASE_ANON_KEY (from design-factory-admin project)"
echo "   - SUPABASE_SERVICE_ROLE_KEY (from design-factory-admin project)"
echo "   - REDIS_URL (from Redis provider)"
echo "   - OPENAI_API_KEY (from OpenAI)"
echo "   - ANTHROPIC_API_KEY (from Anthropic)"
echo "   - GOOGLE_AI_API_KEY (from Google AI)"
echo ""
echo "3. This ONE .env file is used by:"
echo "   ✓ Factory (apps/factory/)"
echo "   ✓ Admin Console (apps/admin-console/)"
echo "   ✓ All deployment scripts"
echo ""
echo "💡 Tip: Store these credentials securely in your password manager!"
echo ""
echo "🔒 Security Note: .env file is gitignored - never commit credentials!"
echo ""

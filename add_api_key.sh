#!/bin/bash

# Simple script to add API keys to the .env file

echo "🔑 Add API Key to Design Decision Team"
echo "======================================"
echo ""
echo "Which API key do you want to add?"
echo "1. Unsplash"
echo "2. Pexels"
echo "3. Stability AI"
echo "4. Exit"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📸 Adding Unsplash API Key..."
        read -p "Enter your Unsplash API key: " unsplash_key
        if [ ! -z "$unsplash_key" ]; then
            sed -i '' "s/UNSPLASH_API_KEY=your_unsplash_api_key_here/UNSPLASH_API_KEY=$unsplash_key/" .env
            echo "✅ Unsplash API key added!"
        else
            echo "❌ No key provided"
        fi
        ;;
    2)
        echo ""
        echo "📷 Adding Pexels API Key..."
        read -p "Enter your Pexels API key: " pexels_key
        if [ ! -z "$pexels_key" ]; then
            sed -i '' "s/PEXELS_API_KEY=your_pexels_api_key_here/PEXELS_API_KEY=$pexels_key/" .env
            echo "✅ Pexels API key added!"
        else
            echo "❌ No key provided"
        fi
        ;;
    3)
        echo ""
        echo "🤖 Adding Stability AI API Key..."
        read -p "Enter your Stability AI API key: " stability_key
        if [ ! -z "$stability_key" ]; then
            sed -i '' "s/STABILITY_API_KEY=your_stability_api_key_here/STABILITY_API_KEY=$stability_key/" .env
            echo "✅ Stability AI API key added!"
        else
            echo "❌ No key provided"
        fi
        ;;
    4)
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice"
        ;;
esac

echo ""
echo "🧪 Testing updated API keys..."
python3 test_api_keys.py

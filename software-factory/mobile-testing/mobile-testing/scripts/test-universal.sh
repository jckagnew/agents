#!/bin/bash

# Universal Testing Script for Software Factory
set -e

echo "🌐 Starting Universal App Testing..."

# Function to test web version
test_web() {
    echo "Testing Web version..."
    cd ../../generated-apps/weight-tracker-nextjs
    npm run dev -- --port 3003 &
    WEB_PID=$!
    
    # Wait for web server to start
    sleep 5
    
    # Test web version
    if curl -s http://localhost:3003 > /dev/null; then
        echo "✅ Web version is running at http://localhost:3003"
    else
        echo "❌ Web version failed to start"
    fi
}

# Function to test Android
test_android() {
    echo "Testing Android version..."
    if command -v $ANDROID_HOME/emulator/emulator &> /dev/null; then
        ./test-android.sh
    else
        echo "⚠️  Android SDK not found. Skipping Android test."
    fi
}

# Function to test iOS
test_ios() {
    echo "Testing iOS version..."
    if command -v xcrun &> /dev/null; then
        ./test-ios.sh
    else
        echo "⚠️  Xcode not found. Skipping iOS test."
    fi
}

# Run tests based on arguments
case "${1:-all}" in
    "web")
        test_web
        ;;
    "android")
        test_android
        ;;
    "ios")
        test_ios
        ;;
    "all")
        test_web
        test_android
        test_ios
        ;;
    *)
        echo "Usage: $0 [web|android|ios|all]"
        exit 1
        ;;
esac

echo "🎉 Universal testing completed!"

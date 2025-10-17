#!/bin/bash

# iOS Testing Script for Software Factory
set -e

echo "🍎 Starting iOS Testing..."

# Check if iOS Simulator is running
if ! pgrep -f "Simulator" > /dev/null; then
    echo "Starting iOS Simulator..."
    
    # List available simulators
    xcrun simctl list devices
    
    # Start iPhone 15 Pro simulator
    xcrun simctl boot "iPhone 15 Pro"
    open -a Simulator
    
    echo "iOS Simulator started successfully!"
else
    echo "iOS Simulator is already running"
fi

# Install and run the app
echo "Installing app on iOS device..."
cd ../../generated-apps/weight-tracker-nextjs

# For Expo apps
if [ -f "app.json" ] || [ -f "expo.json" ]; then
    echo "Starting Expo app on iOS..."
    npx expo start --ios
else
    echo "Starting React Native app on iOS..."
    npx react-native run-ios
fi

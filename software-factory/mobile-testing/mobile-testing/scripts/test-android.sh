#!/bin/bash

# Android Testing Script for Software Factory
set -e

echo "🤖 Starting Android Testing..."

# Check if Android emulator is running
if ! pgrep -f "emulator" > /dev/null; then
    echo "Starting Android emulator..."
    
    # List available AVDs
    $ANDROID_HOME/emulator/emulator -list-avds
    
    # Start emulator (you may need to adjust the AVD name)
    $ANDROID_HOME/emulator/emulator -avd SoftwareFactory_Android -no-audio -no-window &
    
    # Wait for emulator to start
    echo "Waiting for emulator to start..."
    $ANDROID_HOME/platform-tools/adb wait-for-device
    
    echo "Android emulator started successfully!"
else
    echo "Android emulator is already running"
fi

# Install and run the app
echo "Installing app on Android device..."
cd ../../generated-apps/weight-tracker-nextjs

# For Expo apps
if [ -f "app.json" ] || [ -f "expo.json" ]; then
    echo "Starting Expo app on Android..."
    npx expo start --android
else
    echo "Starting React Native app on Android..."
    npx react-native run-android
fi

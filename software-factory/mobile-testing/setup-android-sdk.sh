#!/bin/bash

# Android SDK Setup Script for Software Factory
# This script helps configure Android Studio and SDK

set -e

echo "🤖 Setting up Android SDK for Software Factory..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Android Studio is installed
if [ ! -d "/Applications/Android Studio.app" ]; then
    print_error "Android Studio not found. Please install it first."
    print_status "Download from: https://developer.android.com/studio"
    exit 1
fi

print_success "Android Studio found!"

# Find Android SDK location
print_status "Looking for Android SDK..."

# Common SDK locations
SDK_LOCATIONS=(
    "$HOME/Library/Android/sdk"
    "$HOME/Android/Sdk"
    "/usr/local/android-sdk"
    "/opt/android-sdk"
)

ANDROID_SDK_PATH=""

for location in "${SDK_LOCATIONS[@]}"; do
    if [ -d "$location" ]; then
        ANDROID_SDK_PATH="$location"
        print_success "Found Android SDK at: $ANDROID_SDK_PATH"
        break
    fi
done

if [ -z "$ANDROID_SDK_PATH" ]; then
    print_warning "Android SDK not found in common locations."
    print_status "Please configure Android Studio first:"
    echo ""
    print_status "1. Open Android Studio"
    print_status "2. Go to Tools → SDK Manager"
    print_status "3. Install Android SDK (it will be installed to ~/Library/Android/sdk)"
    print_status "4. Run this script again"
    echo ""
    print_status "Opening Android Studio for you..."
    open "/Applications/Android Studio.app"
    exit 1
fi

# Set environment variables
print_status "Setting up environment variables..."

# Add to shell profile
SHELL_PROFILE=""
if [ -f "$HOME/.zshrc" ]; then
    SHELL_PROFILE="$HOME/.zshrc"
elif [ -f "$HOME/.bash_profile" ]; then
    SHELL_PROFILE="$HOME/.bash_profile"
elif [ -f "$HOME/.bashrc" ]; then
    SHELL_PROFILE="$HOME/.bashrc"
else
    SHELL_PROFILE="$HOME/.zshrc"
    touch "$SHELL_PROFILE"
fi

# Check if already configured
if ! grep -q "ANDROID_HOME" "$SHELL_PROFILE"; then
    print_status "Adding Android SDK environment variables to $SHELL_PROFILE"
    
    cat >> "$SHELL_PROFILE" << EOF

# Android SDK Environment Variables
export ANDROID_HOME=$ANDROID_SDK_PATH
export PATH=\$PATH:\$ANDROID_HOME/emulator
export PATH=\$PATH:\$ANDROID_HOME/tools
export PATH=\$PATH:\$ANDROID_HOME/tools/bin
export PATH=\$PATH:\$ANDROID_HOME/platform-tools
EOF
    
    print_success "Environment variables added to $SHELL_PROFILE"
else
    print_success "Environment variables already configured"
fi

# Apply environment variables for current session
export ANDROID_HOME="$ANDROID_SDK_PATH"
export PATH="$PATH:$ANDROID_HOME/emulator"
export PATH="$PATH:$ANDROID_HOME/tools"
export PATH="$PATH:$ANDROID_HOME/tools/bin"
export PATH="$PATH:$ANDROID_HOME/platform-tools"

print_success "Environment variables set for current session"

# Check if SDK tools are available
print_status "Checking Android SDK tools..."

if [ -f "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" ]; then
    SDKMANAGER="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
elif [ -f "$ANDROID_HOME/tools/bin/sdkmanager" ]; then
    SDKMANAGER="$ANDROID_HOME/tools/bin/sdkmanager"
else
    print_warning "SDK Manager not found. Installing command line tools..."
    
    # Download command line tools
    print_status "Downloading Android command line tools..."
    cd /tmp
    curl -O https://dl.google.com/android/repository/commandlinetools-mac-11076708_latest.zip
    unzip -q commandlinetools-mac-11076708_latest.zip
    
    # Install command line tools
    mkdir -p "$ANDROID_HOME/cmdline-tools"
    mv cmdline-tools "$ANDROID_HOME/cmdline-tools/latest"
    
    SDKMANAGER="$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager"
    
    print_success "Command line tools installed"
fi

# Install required SDK components
print_status "Installing required Android SDK components..."

# Accept licenses
yes | $SDKMANAGER --licenses > /dev/null 2>&1 || true

# Install Android 13 (API 33)
print_status "Installing Android 13 (API 33)..."
$SDKMANAGER "platforms;android-33" > /dev/null 2>&1 || true

# Install build tools
print_status "Installing build tools..."
$SDKMANAGER "build-tools;33.0.0" > /dev/null 2>&1 || true

# Install system image
print_status "Installing Android 13 system image..."
$SDKMANAGER "system-images;android-33;google_apis;x86_64" > /dev/null 2>&1 || true

# Install emulator
print_status "Installing Android emulator..."
$SDKMANAGER "emulator" > /dev/null 2>&1 || true

print_success "Android SDK components installed"

# Create AVD
print_status "Creating Android Virtual Device..."

# Check if AVD already exists
if [ -f "$ANDROID_HOME/avd/SoftwareFactory_Android.avd/config.ini" ]; then
    print_success "AVD already exists: SoftwareFactory_Android"
else
    print_status "Creating AVD: SoftwareFactory_Android"
    echo "no" | $ANDROID_HOME/cmdline-tools/latest/bin/avdmanager create avd \
        -n "SoftwareFactory_Android" \
        -k "system-images;android-33;google_apis;x86_64" \
        --force > /dev/null 2>&1 || true
    
    print_success "AVD created: SoftwareFactory_Android"
fi

# Test setup
print_status "Testing Android setup..."

if command -v adb &> /dev/null; then
    ADB_VERSION=$(adb version | head -1)
    print_success "✅ ADB: $ADB_VERSION"
else
    print_warning "⚠️  ADB: Not available"
fi

if command -v emulator &> /dev/null; then
    print_success "✅ Emulator: Available"
    print_status "Available AVDs:"
    emulator -list-avds
else
    print_warning "⚠️  Emulator: Not available"
fi

print_success "🎉 Android SDK setup completed!"
print_status "Next steps:"
print_status "1. Restart your terminal or run: source ~/.zshrc"
print_status "2. Test Android setup: ./test-universal-app.sh android"
print_status "3. Test all platforms: ./test-universal-app.sh all"

echo ""
print_status "Your Software Factory can now test Android apps! 🤖"

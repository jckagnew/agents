#!/bin/bash

# Mobile Development Environment Setup Script
# Sets up React Native, Expo, and mobile testing tools

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${YELLOW}✨ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    log_error "This script is designed for macOS. Mobile development requires macOS for iOS development."
    exit 1
fi

log_info "Setting up mobile development environment..."

# 1. Install Node.js (if not already installed)
if ! command -v node &> /dev/null; then
    log_info "Installing Node.js via Homebrew..."
    brew install node
else
    log_info "Node.js already installed: $(node --version)"
fi

# 2. Install React Native CLI
log_info "Installing React Native CLI..."
npm install -g @react-native-community/cli

# 3. Install Expo CLI
log_info "Installing Expo CLI..."
npm install -g @expo/cli

# 4. Install Flutter (optional, for cross-platform development)
log_info "Installing Flutter..."
if ! command -v flutter &> /dev/null; then
    brew install --cask flutter
    log_success "Flutter installed successfully"
else
    log_info "Flutter already installed: $(flutter --version | head -n 1)"
fi

# 5. Install Android Studio (if not already installed)
if [ ! -d "/Applications/Android Studio.app" ]; then
    log_info "Installing Android Studio..."
    brew install --cask android-studio
    log_success "Android Studio installed. Please complete the setup wizard manually."
    log_info "After setup, run: flutter doctor --android-licenses"
else
    log_info "Android Studio already installed"
fi

# 6. Install Xcode Command Line Tools (for iOS development)
log_info "Installing Xcode Command Line Tools..."
xcode-select --install 2>/dev/null || log_info "Xcode Command Line Tools already installed"

# 7. Install mobile testing tools
log_info "Installing mobile testing tools..."

# Appium
npm install -g appium
npm install -g @appium/doctor

# Detox (for React Native)
npm install -g detox-cli

# 8. Install additional mobile development tools
log_info "Installing additional mobile development tools..."

# CocoaPods (for iOS)
if ! command -v pod &> /dev/null; then
    sudo gem install cocoapods
    log_success "CocoaPods installed"
else
    log_info "CocoaPods already installed: $(pod --version)"
fi

# Fastlane (for mobile deployment)
if ! command -v fastlane &> /dev/null; then
    sudo gem install fastlane -NV
    log_success "Fastlane installed"
else
    log_info "Fastlane already installed: $(fastlane --version | head -n 1)"
fi

# 9. Create mobile project templates
log_info "Creating mobile project templates..."

# Create Expo template
if [ ! -d "templates/mobile/expo" ]; then
    mkdir -p templates/mobile/expo
    log_success "Expo template directory created"
fi

# Create React Native template
if [ ! -d "templates/mobile/react-native" ]; then
    mkdir -p templates/mobile/react-native
    log_success "React Native template directory created"
fi

# 10. Verify installations
log_info "Verifying mobile development setup..."

# Check Node.js
if command -v node &> /dev/null; then
    log_success "Node.js: $(node --version)"
else
    log_error "Node.js not found"
fi

# Check React Native CLI
if command -v react-native &> /dev/null; then
    log_success "React Native CLI: $(react-native --version | head -n 1)"
else
    log_error "React Native CLI not found"
fi

# Check Expo CLI
if command -v expo &> /dev/null; then
    log_success "Expo CLI: $(expo --version | head -n 1)"
else
    log_error "Expo CLI not found"
fi

# Check Flutter
if command -v flutter &> /dev/null; then
    log_success "Flutter: $(flutter --version | head -n 1)"
else
    log_error "Flutter not found"
fi

# Check Android Studio
if [ -d "/Applications/Android Studio.app" ]; then
    log_success "Android Studio: Installed"
else
    log_error "Android Studio not found"
fi

# Check Xcode
if command -v xcodebuild &> /dev/null; then
    log_success "Xcode: $(xcodebuild -version | head -n 1)"
else
    log_error "Xcode not found"
fi

log_success "Mobile development environment setup completed!"
log_info "Next steps:"
log_info "1. Complete Android Studio setup wizard"
log_info "2. Run 'flutter doctor' to check Flutter setup"
log_info "3. Run 'appium-doctor' to check Appium setup"
log_info "4. Create a new mobile project using the templates"
log_info "5. Test on iOS Simulator and Android Emulator"

log_info "Mobile development templates available in:"
log_info "- templates/mobile/expo/ (Expo/React Native)"
log_info "- templates/mobile/react-native/ (Pure React Native)"
log_info "- templates/mobile/native/ (Native iOS/Android)"

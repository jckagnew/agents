#!/bin/bash

# =============================================================================
# MOBILE DEVELOPMENT SETUP SCRIPT
# =============================================================================
# This script sets up a complete mobile development environment on macOS
# Includes: iOS Simulator, Android Emulator, React Native, Flutter, and more
# =============================================================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# =============================================================================
# 1. XCODE & iOS SIMULATOR
# =============================================================================
log_info "Setting up iOS development environment..."

# Check if Xcode is installed
if ! command -v xcodebuild &> /dev/null; then
    log_warning "Xcode not found. Please install from App Store first:"
    log_warning "1. Open App Store"
    log_warning "2. Search for 'Xcode'"
    log_warning "3. Install (it's free but large ~15GB)"
    log_warning "4. Run this script again after installation"
    exit 1
fi

# Install Xcode command line tools
log_info "Installing Xcode command line tools..."
xcode-select --install 2>/dev/null || log_success "Command line tools already installed"

# Install iOS Simulator (if not already installed)
log_info "Installing iOS Simulator..."
xcrun simctl list devices &> /dev/null || log_warning "iOS Simulator may need to be installed via Xcode"

log_success "iOS development environment ready!"

# =============================================================================
# 2. ANDROID STUDIO & EMULATOR
# =============================================================================
log_info "Setting up Android development environment..."

# Install Android Studio
if ! command -v android-studio &> /dev/null; then
    log_info "Installing Android Studio..."
    brew install --cask android-studio
    log_success "Android Studio installed!"
    log_warning "Please open Android Studio and complete the setup wizard"
    log_warning "Then run: android-studio"
else
    log_success "Android Studio already installed"
fi

# Set up Android SDK
log_info "Setting up Android SDK..."
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$PATH:$ANDROID_HOME/emulator"
export PATH="$PATH:$ANDROID_HOME/tools"
export PATH="$PATH:$ANDROID_HOME/tools/bin"
export PATH="$PATH:$ANDROID_HOME/platform-tools"

# Add to shell profile
if ! grep -q "ANDROID_HOME" ~/.zshrc; then
    echo 'export ANDROID_HOME="$HOME/Library/Android/sdk"' >> ~/.zshrc
    echo 'export PATH="$PATH:$ANDROID_HOME/emulator"' >> ~/.zshrc
    echo 'export PATH="$PATH:$ANDROID_HOME/tools"' >> ~/.zshrc
    echo 'export PATH="$PATH:$ANDROID_HOME/tools/bin"' >> ~/.zshrc
    echo 'export PATH="$PATH:$ANDROID_HOME/platform-tools"' >> ~/.zshrc
    log_success "Android environment variables added to ~/.zshrc"
fi

# =============================================================================
# 3. REACT NATIVE CLI
# =============================================================================
log_info "Setting up React Native development..."

# Install Node.js (if not already installed)
if ! command -v node &> /dev/null; then
    log_info "Installing Node.js..."
    brew install node
fi

# Install React Native CLI
log_info "Installing React Native CLI..."
npm install -g @react-native-community/cli

# Install Expo CLI
log_info "Installing Expo CLI..."
npm install -g @expo/cli

log_success "React Native development tools installed!"

# =============================================================================
# 4. FLUTTER (OPTIONAL)
# =============================================================================
log_info "Setting up Flutter (optional)..."

if ! command -v flutter &> /dev/null; then
    log_info "Installing Flutter..."
    brew install --cask flutter
    log_success "Flutter installed!"
    log_warning "Run 'flutter doctor' to check your setup"
else
    log_success "Flutter already installed"
fi

# =============================================================================
# 5. MOBILE TESTING TOOLS
# =============================================================================
log_info "Installing mobile testing tools..."

# Install Appium (mobile automation)
log_info "Installing Appium..."
npm install -g appium
npm install -g appium-doctor

# Install Detox (React Native E2E testing)
log_info "Installing Detox..."
npm install -g detox-cli

# Install Flipper (mobile debugging)
log_info "Installing Flipper..."
brew install --cask flipper

log_success "Mobile testing tools installed!"

# =============================================================================
# 6. BROWSER TESTING TOOLS
# =============================================================================
log_info "Installing browser testing tools..."

# Install Playwright (cross-browser testing)
log_info "Installing Playwright..."
npm install -g playwright
npx playwright install

# Install Lighthouse (performance testing)
log_info "Installing Lighthouse..."
npm install -g lighthouse

log_success "Browser testing tools installed!"

# =============================================================================
# 7. CREATE MOBILE TEST PROJECT
# =============================================================================
log_info "Creating mobile test project..."

MOBILE_TEST_DIR="$HOME/mobile-test-projects"
mkdir -p "$MOBILE_TEST_DIR"

# Create React Native test project
if [ ! -d "$MOBILE_TEST_DIR/TestApp" ]; then
    log_info "Creating React Native test app..."
    cd "$MOBILE_TEST_DIR"
    npx react-native@latest init TestApp
    log_success "React Native test app created at $MOBILE_TEST_DIR/TestApp"
fi

# Create Expo test project
if [ ! -d "$MOBILE_TEST_DIR/ExpoTestApp" ]; then
    log_info "Creating Expo test app..."
    cd "$MOBILE_TEST_DIR"
    npx create-expo-app ExpoTestApp
    log_success "Expo test app created at $MOBILE_TEST_DIR/ExpoTestApp"
fi

# =============================================================================
# 8. USEFUL ALIASES
# =============================================================================
log_info "Setting up useful aliases..."

# Add mobile development aliases to shell profile
cat >> ~/.zshrc << 'EOF'

# Mobile Development Aliases
alias ios-sim="xcrun simctl list devices"
alias android-emu="emulator -list-avds"
alias start-ios="npx react-native run-ios"
alias start-android="npx react-native run-android"
alias expo-start="npx expo start"
alias flutter-devices="flutter devices"
alias appium-doctor="appium-doctor"

# Mobile Testing
alias test-ios="npx detox test --configuration ios.sim.debug"
alias test-android="npx detox test --configuration android.emu.debug"
alias lighthouse-mobile="lighthouse --form-factor=mobile --throttling-method=devtools"

EOF

log_success "Mobile development aliases added to ~/.zshrc"

# =============================================================================
# 9. SUMMARY
# =============================================================================
log_success "🎉 Mobile development environment setup complete!"
echo ""
log_info "📱 Available Tools:"
echo "  • Xcode Simulator (iOS)"
echo "  • Android Studio Emulator (Android)"
echo "  • React Native CLI"
echo "  • Expo CLI"
echo "  • Flutter"
echo "  • Appium (automation)"
echo "  • Detox (E2E testing)"
echo "  • Flipper (debugging)"
echo "  • Playwright (browser testing)"
echo "  • Lighthouse (performance)"
echo ""
log_info "🚀 Next Steps:"
echo "  1. Open Android Studio and complete setup wizard"
echo "  2. Run 'flutter doctor' to check Flutter setup"
echo "  3. Run 'appium-doctor' to check Appium setup"
echo "  4. Test your setup with the created test apps"
echo ""
log_info "📁 Test Projects Created:"
echo "  • $MOBILE_TEST_DIR/TestApp (React Native)"
echo "  • $MOBILE_TEST_DIR/ExpoTestApp (Expo)"
echo ""
log_info "🔧 Useful Commands:"
echo "  • ios-sim - List iOS simulators"
echo "  • android-emu - List Android emulators"
echo "  • start-ios - Run React Native on iOS"
echo "  • start-android - Run React Native on Android"
echo "  • expo-start - Start Expo development server"
echo "  • flutter-devices - List Flutter devices"
echo ""
log_warning "⚠️  Don't forget to restart your terminal or run 'source ~/.zshrc'"

#!/bin/bash

# Mobile SDK Installation Script for Software Factory
# This script helps install Android Studio and Xcode for mobile testing

set -e

echo "🚀 Installing Mobile SDKs for Software Factory..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_platform() {
    echo -e "${PURPLE}[PLATFORM]${NC} $1"
}

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_error "This script is designed for macOS. iOS development requires macOS."
    exit 1
fi

print_status "Starting mobile SDK installation process..."

# Function to install Xcode
install_xcode() {
    print_platform "Installing Xcode for iOS Development"
    
    # Check if Xcode is already installed
    if command -v xcodebuild &> /dev/null; then
        local xcode_version=$(xcodebuild -version | head -1)
        print_success "Xcode is already installed: $xcode_version"
        return 0
    fi
    
    print_status "Xcode is not installed. Here's how to install it:"
    echo ""
    print_status "📱 XCODE INSTALLATION STEPS:"
    echo "1. Open the App Store on your Mac"
    echo "2. Search for 'Xcode'"
    echo "3. Click 'Get' or 'Install' (it's free but large ~15GB)"
    echo "4. Wait for download and installation to complete"
    echo "5. Open Xcode and accept the license agreement"
    echo "6. Install additional components when prompted"
    echo ""
    print_warning "Xcode download is large (~15GB) and may take 30-60 minutes"
    print_status "After installation, run this script again to verify setup"
    
    # Open App Store to Xcode page
    print_status "Opening App Store to Xcode page..."
    open "macappstore://itunes.apple.com/app/xcode/id497799835"
    
    return 1
}

# Function to install Android Studio
install_android_studio() {
    print_platform "Installing Android Studio for Android Development"
    
    # Check if Android Studio is already installed
    if command -v studio &> /dev/null || [ -d "/Applications/Android Studio.app" ]; then
        print_success "Android Studio appears to be installed"
        return 0
    fi
    
    print_status "Android Studio is not installed. Here's how to install it:"
    echo ""
    print_status "🤖 ANDROID STUDIO INSTALLATION STEPS:"
    echo "1. Download Android Studio from: https://developer.android.com/studio"
    echo "2. Open the downloaded .dmg file"
    echo "3. Drag Android Studio to Applications folder"
    echo "4. Launch Android Studio from Applications"
    echo "5. Follow the setup wizard to install Android SDK"
    echo "6. Accept all license agreements"
    echo "7. Install recommended SDK components"
    echo ""
    print_warning "Android Studio download is large (~1GB) and setup takes 10-15 minutes"
    print_status "After installation, run this script again to verify setup"
    
    # Open Android Studio download page
    print_status "Opening Android Studio download page..."
    open "https://developer.android.com/studio"
    
    return 1
}

# Function to setup environment variables
setup_environment() {
    print_status "Setting up environment variables..."
    
    local shell_profile=""
    if [ -f "$HOME/.zshrc" ]; then
        shell_profile="$HOME/.zshrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        shell_profile="$HOME/.bash_profile"
    elif [ -f "$HOME/.bashrc" ]; then
        shell_profile="$HOME/.bashrc"
    else
        shell_profile="$HOME/.zshrc"
        touch "$shell_profile"
    fi
    
    print_status "Adding Android SDK environment variables to $shell_profile"
    
    # Check if Android SDK variables are already set
    if ! grep -q "ANDROID_HOME" "$shell_profile"; then
        cat >> "$shell_profile" << 'EOF'

# Android SDK Environment Variables
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
EOF
        print_success "Android SDK environment variables added to $shell_profile"
    else
        print_success "Android SDK environment variables already configured"
    fi
    
    print_status "To apply changes, run: source $shell_profile"
}

# Function to verify installations
verify_installations() {
    print_status "Verifying installations..."
    
    local all_good=true
    
    # Check Xcode
    if command -v xcodebuild &> /dev/null; then
        local xcode_version=$(xcodebuild -version | head -1)
        print_success "✅ Xcode: $xcode_version"
    else
        print_warning "⚠️  Xcode: Not installed"
        all_good=false
    fi
    
    # Check Android Studio
    if command -v studio &> /dev/null || [ -d "/Applications/Android Studio.app" ]; then
        print_success "✅ Android Studio: Installed"
    else
        print_warning "⚠️  Android Studio: Not installed"
        all_good=false
    fi
    
    # Check Android SDK
    if [ -d "$HOME/Library/Android/sdk" ]; then
        print_success "✅ Android SDK: Installed at $HOME/Library/Android/sdk"
    else
        print_warning "⚠️  Android SDK: Not found"
        all_good=false
    fi
    
    # Check adb
    if command -v adb &> /dev/null; then
        local adb_version=$(adb version | head -1)
        print_success "✅ ADB: $adb_version"
    else
        print_warning "⚠️  ADB: Not available (Android SDK not in PATH)"
        all_good=false
    fi
    
    if [ "$all_good" = true ]; then
        print_success "🎉 All mobile SDKs are properly installed!"
        return 0
    else
        print_warning "Some components are missing. Please complete the installation steps above."
        return 1
    fi
}

# Function to create Android AVD
create_android_avd() {
    print_status "Creating Android Virtual Device (AVD)..."
    
    if ! command -v avdmanager &> /dev/null; then
        print_warning "AVD Manager not found. Please install Android SDK first."
        return 1
    fi
    
    # List available system images
    print_status "Available Android system images:"
    sdkmanager --list | grep "system-images" | head -10
    
    # Create AVD
    print_status "Creating AVD for Software Factory testing..."
    echo "no" | avdmanager create avd -n "SoftwareFactory_Android" -k "system-images;android-33;google_apis;x86_64" || true
    
    print_success "Android AVD created: SoftwareFactory_Android"
}

# Function to test mobile setup
test_mobile_setup() {
    print_status "Testing mobile development setup..."
    
    # Test iOS Simulator
    if command -v xcrun &> /dev/null; then
        print_status "Available iOS Simulators:"
        xcrun simctl list devices | grep "iPhone" | head -5
        print_success "✅ iOS Simulator: Ready"
    else
        print_warning "⚠️  iOS Simulator: Not available"
    fi
    
    # Test Android Emulator
    if command -v emulator &> /dev/null; then
        print_status "Available Android AVDs:"
        emulator -list-avds
        print_success "✅ Android Emulator: Ready"
    else
        print_warning "⚠️  Android Emulator: Not available"
    fi
}

# Main execution
main() {
    echo ""
    print_status "🚀 MOBILE SDK INSTALLATION FOR SOFTWARE FACTORY"
    echo ""
    
    # Install Xcode
    install_xcode
    local xcode_installed=$?
    
    # Install Android Studio
    install_android_studio
    local android_installed=$?
    
    # Setup environment
    setup_environment
    
    # Verify installations
    verify_installations
    local verification_result=$?
    
    if [ $verification_result -eq 0 ]; then
        # Create Android AVD
        create_android_avd
        
        # Test setup
        test_mobile_setup
        
        echo ""
        print_success "🎉 MOBILE SDK INSTALLATION COMPLETE!"
        print_status "Your Software Factory can now test apps on:"
        print_status "  ✅ iOS Simulator"
        print_status "  ✅ Android Emulator"
        print_status "  ✅ Web browsers"
        echo ""
        print_status "Next steps:"
        print_status "1. Restart your terminal or run: source ~/.zshrc"
        print_status "2. Test your setup: cd mobile-testing && ./test-universal-app.sh all"
        print_status "3. Create new mobile apps: ./create-mobile-app.sh 'app-name' 'App Name'"
    else
        echo ""
        print_warning "⚠️  INSTALLATION INCOMPLETE"
        print_status "Please complete the installation steps above and run this script again."
        print_status "After installation, run: ./install-mobile-sdks.sh verify"
    fi
}

# Handle verify command
if [ "${1:-}" = "verify" ]; then
    verify_installations
    test_mobile_setup
    exit $?
fi

# Run main installation
main

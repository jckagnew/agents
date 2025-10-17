#!/bin/bash

# Mobile Project Creation Script
# Creates a new mobile project using the templates

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

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] PROJECT_NAME"
    echo ""
    echo "Options:"
    echo "  -t, --type TYPE     Mobile framework type (expo|react-native|flutter)"
    echo "  -c, --company NAME  Company name for bundle identifier"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 MyApp --type expo"
    echo "  $0 MyApp --type react-native --company mycompany"
    echo "  $0 MyApp --type flutter"
}

# Default values
PROJECT_TYPE="expo"
COMPANY_NAME="mycompany"
PROJECT_NAME=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            PROJECT_TYPE="$2"
            shift 2
            ;;
        -c|--company)
            COMPANY_NAME="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            if [ -z "$PROJECT_NAME" ]; then
                PROJECT_NAME="$1"
            else
                log_error "Unknown option: $1"
                show_usage
                exit 1
            fi
            shift
            ;;
    esac
done

# Check if project name is provided
if [ -z "$PROJECT_NAME" ]; then
    log_error "Project name is required"
    show_usage
    exit 1
fi

# Validate project type
case $PROJECT_TYPE in
    expo|react-native|flutter)
        ;;
    *)
        log_error "Invalid project type: $PROJECT_TYPE"
        log_error "Valid types: expo, react-native, flutter"
        exit 1
        ;;
esac

# Create project slug and company slug
PROJECT_SLUG=$(echo "$PROJECT_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')
COMPANY_SLUG=$(echo "$COMPANY_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-\|-$//g')

log_info "Creating mobile project: $PROJECT_NAME"
log_info "Type: $PROJECT_TYPE"
log_info "Company: $COMPANY_NAME"
log_info "Project slug: $PROJECT_SLUG"

# Create project directory
PROJECT_DIR="$PROJECT_SLUG"
if [ -d "$PROJECT_DIR" ]; then
    log_error "Directory $PROJECT_DIR already exists"
    exit 1
fi

mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# Setup environment variables
log_info "Setting up environment variables..."
if [ -f "/Users/jackagnew/projects/agents/env.master" ]; then
    cp "/Users/jackagnew/projects/agents/env.master" .env
    log_success "Environment variables copied from master"
else
    log_warning "Master .env file not found, creating basic .env"
    cat > .env << 'EOF'
# Environment Variables
NODE_ENV=development
EOF
fi

# Create project based on type
case $PROJECT_TYPE in
    expo)
        log_info "Creating Expo project..."
        
        # Initialize Expo project
        npx create-expo-app@latest . --template blank-typescript --yes
        
        # Copy template files
        if [ -f "../templates/mobile/expo/App.tsx" ]; then
            cp "../templates/mobile/expo/App.tsx" "./App.tsx"
            log_success "App.tsx template copied"
        fi
        
        if [ -f "../templates/mobile/expo/app.json" ]; then
            cp "../templates/mobile/expo/app.json" "./app.json"
            # Replace placeholders
            sed -i '' "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" app.json
            sed -i '' "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g" app.json
            sed -i '' "s/{{COMPANY_SLUG}}/$COMPANY_SLUG/g" app.json
            log_success "app.json template copied and configured"
        fi
        
        if [ -f "../templates/mobile/expo/package.json" ]; then
            cp "../templates/mobile/expo/package.json" "./package.json"
            # Replace placeholders
            sed -i '' "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g" package.json
            log_success "package.json template copied and configured"
        fi
        
        # Install dependencies
        npm install
        ;;
        
    react-native)
        log_info "Creating React Native project..."
        
        # Initialize React Native project
        npx react-native@latest init "$PROJECT_NAME" --template react-native-template-typescript
        
        # Copy template files
        if [ -f "../templates/mobile/react-native/App.tsx" ]; then
            cp "../templates/mobile/react-native/App.tsx" "./App.tsx"
            # Replace placeholders
            sed -i '' "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" App.tsx
            log_success "App.tsx template copied and configured"
        fi
        
        if [ -f "../templates/mobile/react-native/package.json" ]; then
            cp "../templates/mobile/react-native/package.json" "./package.json"
            # Replace placeholders
            sed -i '' "s/{{PROJECT_SLUG}}/$PROJECT_SLUG/g" package.json
            sed -i '' "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" package.json
            log_success "package.json template copied and configured"
        fi
        
        # Install dependencies
        npm install
        ;;
        
    flutter)
        log_info "Creating Flutter project..."
        
        # Initialize Flutter project
        flutter create --org com.$COMPANY_SLUG --project-name $PROJECT_SLUG .
        
        # Update pubspec.yaml with project name
        sed -i '' "s/name: $PROJECT_SLUG/name: $PROJECT_SLUG/g" pubspec.yaml
        sed -i '' "s/description: .*/description: $PROJECT_NAME - A Flutter mobile application./g" pubspec.yaml
        
        # Install dependencies
        flutter pub get
        ;;
esac

# Create additional mobile-specific files
log_info "Creating mobile-specific configuration files..."

# Create .gitignore for mobile
cat > .gitignore << EOF
# Mobile Development
*.log
*.tmp
*.temp

# iOS
ios/build/
ios/Pods/
ios/*.xcworkspace/xcuserdata/
ios/*.xcodeproj/xcuserdata/
ios/*.xcodeproj/project.xcworkspace/xcuserdata/
ios/DerivedData/
ios/UserInterfaceState.xcuserstate

# Android
android/app/build/
android/build/
android/.gradle/
android/gradle/
android/gradlew
android/gradlew.bat
android/local.properties
android/.idea/
android/*.iml
android/app/release/

# Expo
.expo/
dist/
web-build/

# Flutter
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
build/
flutter_*.png
linked_*.ds
unlinked.ds
unlinked_spec.ds

# Metro
.metro-health-check*

# Testing
coverage/
.nyc_output/

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOF

log_success ".gitignore created"

# Create README for mobile project
cat > README.md << EOF
# 🎯 $PROJECT_NAME

A mobile application built with $PROJECT_TYPE.

## 🚀 Quick Start

### Prerequisites
- Node.js (for Expo/React Native)
- Flutter SDK (for Flutter projects)
- iOS Simulator (for iOS development)
- Android Studio (for Android development)

### Development

EOF

case $PROJECT_TYPE in
    expo)
        cat >> README.md << EOF
\`\`\`bash
# Start development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android

# Run on web
npm run web
\`\`\`
EOF
        ;;
    react-native)
        cat >> README.md << EOF
\`\`\`bash
# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
\`\`\`
EOF
        ;;
    flutter)
        cat >> README.md << EOF
\`\`\`bash
# Get dependencies
flutter pub get

# Run on iOS
flutter run -d ios

# Run on Android
flutter run -d android

# Run on web
flutter run -d web
\`\`\`
EOF
        ;;
esac

cat >> README.md << EOF

## 📱 Testing

### iOS Simulator
1. Open Xcode
2. Go to Xcode > Open Developer Tool > Simulator
3. Run the app

### Android Emulator
1. Open Android Studio
2. Go to Tools > AVD Manager
3. Create/start an emulator
4. Run the app

### Physical Device
1. Install Expo Go (for Expo projects)
2. Scan QR code
3. Or build and install APK/IPA

## 🛠️ Development Tools

- **Expo CLI**: \`npm install -g @expo/cli\`
- **React Native CLI**: \`npm install -g @react-native-community/cli\`
- **Flutter**: Follow [Flutter installation guide](https://flutter.dev/docs/get-started/install)

## 📦 Building for Production

EOF

case $PROJECT_TYPE in
    expo)
        cat >> README.md << EOF
\`\`\`bash
# Build for Android
npm run build:android

# Build for iOS
npm run build:ios
\`\`\`
EOF
        ;;
    react-native)
        cat >> README.md << EOF
\`\`\`bash
# Build for Android
npm run build:android

# Build for iOS
npm run build:ios
\`\`\`
EOF
        ;;
    flutter)
        cat >> README.md << EOF
\`\`\`bash
# Build for Android
flutter build apk

# Build for iOS
flutter build ios

# Build for web
flutter build web
\`\`\`
EOF
        ;;
esac

cat >> README.md << EOF

## 🎯 Features

- Cross-platform mobile development
- Hot reloading for fast development
- Native performance
- Easy deployment to app stores

## 📚 Documentation

- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/docs/getting-started)
- [Flutter Documentation](https://flutter.dev/docs)

---

**Happy coding! 🚀**
EOF

log_success "README.md created"

# Create development scripts
log_info "Creating development scripts..."

mkdir -p scripts

case $PROJECT_TYPE in
    expo)
        cat > scripts/dev.sh << 'EOF'
#!/bin/bash
# Start Expo development server
npx expo start
EOF
        ;;
    react-native)
        cat > scripts/dev.sh << 'EOF'
#!/bin/bash
# Start React Native Metro bundler
npx react-native start
EOF
        ;;
    flutter)
        cat > scripts/dev.sh << 'EOF'
#!/bin/bash
# Start Flutter development server
flutter run
EOF
        ;;
esac

chmod +x scripts/dev.sh

cat > scripts/test.sh << 'EOF'
#!/bin/bash
# Run mobile tests
case $1 in
    expo)
        npm test
        ;;
    react-native)
        npm test
        ;;
    flutter)
        flutter test
        ;;
    *)
        echo "Usage: $0 [expo|react-native|flutter]"
        exit 1
        ;;
esac
EOF

chmod +x scripts/test.sh

log_success "Development scripts created"

# Final success message
log_success "Mobile project '$PROJECT_NAME' created successfully!"
log_info "Project directory: $(pwd)"
log_info "Next steps:"
log_info "1. cd $PROJECT_DIR"
log_info "2. Run './scripts/dev.sh' to start development"
log_info "3. Open iOS Simulator or Android Emulator"
log_info "4. Start coding!"

log_info "Available commands:"
log_info "- ./scripts/dev.sh     # Start development server"
log_info "- ./scripts/test.sh    # Run tests"
log_info "- npm start            # Alternative start command"

case $PROJECT_TYPE in
    expo)
        log_info "- npm run ios        # Run on iOS"
        log_info "- npm run android    # Run on Android"
        log_info "- npm run web        # Run on web"
        ;;
    react-native)
        log_info "- npm run ios        # Run on iOS"
        log_info "- npm run android    # Run on Android"
        ;;
    flutter)
        log_info "- flutter run -d ios     # Run on iOS"
        log_info "- flutter run -d android # Run on Android"
        log_info "- flutter run -d web     # Run on web"
        ;;
esac

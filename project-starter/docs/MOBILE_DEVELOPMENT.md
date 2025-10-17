# 📱 Mobile Development Guide

This guide covers mobile development capabilities included in the project starter template.

## 🚀 Quick Start

### 1. Setup Mobile Development Environment
```bash
# Run the mobile setup script
./scripts/setup-mobile.sh
```

### 2. Create a Mobile Project
```bash
# Create an Expo project
./scripts/create-mobile-project.sh MyApp --type expo

# Create a React Native project
./scripts/create-mobile-project.sh MyApp --type react-native --company mycompany

# Create a Flutter project
./scripts/create-mobile-project.sh MyApp --type flutter
```

## 📋 What's Included

### Mobile Development Tools
- **React Native CLI** - Pure React Native development
- **Expo CLI** - Expo/React Native with managed workflow
- **Flutter SDK** - Cross-platform development
- **Android Studio** - Android development and emulation
- **Xcode Command Line Tools** - iOS development
- **CocoaPods** - iOS dependency management
- **Fastlane** - Mobile deployment automation

### Testing Tools
- **Appium** - Cross-platform mobile testing
- **Detox** - React Native testing framework
- **Flutter Test** - Flutter testing framework

### Project Templates
- **Expo Template** - Ready-to-use Expo project structure
- **React Native Template** - Pure React Native with TypeScript
- **Flutter Template** - Flutter project with best practices

## 🛠️ Development Workflow

### Expo Development
```bash
# Start development server
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android

# Run on web
npm run web
```

### React Native Development
```bash
# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android
```

### Flutter Development
```bash
# Get dependencies
flutter pub get

# Run on iOS
flutter run -d ios

# Run on Android
flutter run -d android

# Run on web
flutter run -d web
```

## 📱 Testing

### iOS Testing
1. **iOS Simulator** (macOS only)
   - Open Xcode
   - Go to Xcode > Open Developer Tool > Simulator
   - Run your app

2. **Physical Device**
   - Install Expo Go (for Expo projects)
   - Scan QR code
   - Or build and install IPA

### Android Testing
1. **Android Emulator**
   - Open Android Studio
   - Go to Tools > AVD Manager
   - Create/start an emulator
   - Run your app

2. **Physical Device**
   - Enable Developer Options
   - Enable USB Debugging
   - Connect device and run

### Cross-Platform Testing
- **Appium** - Automated testing across platforms
- **Detox** - React Native specific testing
- **Flutter Test** - Flutter unit and widget tests

## 🏗️ Building for Production

### Expo
```bash
# Build for Android
npm run build:android

# Build for iOS
npm run build:ios
```

### React Native
```bash
# Build for Android
npm run build:android

# Build for iOS
npm run build:ios
```

### Flutter
```bash
# Build for Android
flutter build apk

# Build for iOS
flutter build ios

# Build for web
flutter build web
```

## 📦 App Store Deployment

### iOS App Store
1. **Apple Developer Account** - Required for distribution
2. **Xcode** - Build and upload
3. **App Store Connect** - Manage app metadata
4. **TestFlight** - Beta testing

### Google Play Store
1. **Google Play Console** - Manage app
2. **Android Studio** - Build APK/AAB
3. **Play Console** - Upload and publish

### Automated Deployment
- **Fastlane** - Automate build and deployment
- **GitHub Actions** - CI/CD for mobile apps
- **Expo EAS** - Managed deployment for Expo apps

## 🔧 Configuration

### Environment Variables
```bash
# Mobile-specific environment variables
EXPO_PUBLIC_API_URL=https://api.example.com
REACT_NATIVE_API_URL=https://api.example.com
FLUTTER_API_URL=https://api.example.com
```

### Platform-Specific Code
- **React Native** - Platform.OS checks
- **Flutter** - Platform.isIOS, Platform.isAndroid
- **Expo** - Platform.select()

### Native Modules
- **React Native** - Native modules for platform features
- **Flutter** - Platform channels for native code
- **Expo** - Expo modules for managed workflow

## 📚 Best Practices

### Performance
- **Image Optimization** - Use appropriate formats and sizes
- **Bundle Size** - Minimize JavaScript bundle
- **Memory Management** - Avoid memory leaks
- **Lazy Loading** - Load components on demand

### User Experience
- **Responsive Design** - Adapt to different screen sizes
- **Touch Interactions** - Optimize for touch
- **Loading States** - Provide feedback during operations
- **Error Handling** - Graceful error recovery

### Security
- **API Keys** - Store securely, never in code
- **Data Encryption** - Encrypt sensitive data
- **Certificate Pinning** - Secure API communications
- **Code Obfuscation** - Protect intellectual property

## 🐛 Debugging

### Development Tools
- **React Native Debugger** - Debug React Native apps
- **Flipper** - Mobile development platform
- **Chrome DevTools** - Debug JavaScript
- **Xcode Debugger** - Debug iOS apps
- **Android Studio Debugger** - Debug Android apps

### Common Issues
- **Metro Bundler** - Clear cache and restart
- **iOS Simulator** - Reset simulator
- **Android Emulator** - Wipe data and restart
- **Dependencies** - Clear node_modules and reinstall

## 📖 Resources

### Documentation
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Documentation](https://reactnative.dev/docs/getting-started)
- [Flutter Documentation](https://flutter.dev/docs)

### Tools
- [React Native Debugger](https://github.com/jhen0409/react-native-debugger)
- [Flipper](https://fbflipper.com/)
- [Appium](https://appium.io/)

### Communities
- [React Native Community](https://github.com/react-native-community)
- [Expo Community](https://forums.expo.dev/)
- [Flutter Community](https://flutter.dev/community)

## 🎯 Project Templates

### Expo Template Features
- TypeScript support
- Navigation setup
- State management
- API integration
- Testing framework

### React Native Template Features
- TypeScript configuration
- Navigation setup
- State management (Redux/Context)
- Native modules
- Testing framework

### Flutter Template Features
- Dart language
- Material Design
- State management (Provider/Riverpod)
- Platform channels
- Testing framework

---

**Happy mobile development! 📱🚀**

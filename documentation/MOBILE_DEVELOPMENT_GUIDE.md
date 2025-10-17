# 📱 Mobile Development & Testing Guide

## 🚀 Quick Setup

Run the setup script to install everything:
```bash
./setup-mobile-dev.sh
```

## 📱 **iOS Testing (Free)**

### Xcode Simulator
```bash
# List available simulators
ios-sim

# Open specific simulator
xcrun simctl boot "iPhone 15 Pro"
open -a Simulator

# Install app on simulator
xcrun simctl install booted /path/to/app.app
```

### Available iOS Simulators
- iPhone 15 Pro (iOS 17.0)
- iPhone 14 Pro (iOS 16.0)
- iPhone 13 Pro (iOS 15.0)
- iPad Pro (12.9-inch) (iOS 17.0)
- iPad Air (iOS 17.0)

## 🤖 **Android Testing (Free)**

### Android Studio Emulator
```bash
# List available emulators
android-emu

# Start specific emulator
emulator -avd Pixel_7_API_34

# Install APK
adb install app.apk
```

### Create New Android Emulator
1. Open Android Studio
2. Tools → AVD Manager
3. Create Virtual Device
4. Choose device (Pixel 7, Samsung Galaxy, etc.)
5. Select API level (Android 14, 13, 12, etc.)

## 🌐 **Cross-Platform Testing**

### React Native
```bash
# Create new project
npx react-native@latest init MyApp

# Run on iOS
start-ios

# Run on Android
start-android

# Run on both
npx react-native run-ios && npx react-native run-android
```

### Expo (Easiest for Web Developers)
```bash
# Create new project
npx create-expo-app MyApp

# Start development server
expo-start

# Install Expo Go app on your phone
# Scan QR code to test on real device
```

### Flutter
```bash
# Create new project
flutter create my_app

# List available devices
flutter-devices

# Run on specific device
flutter run -d "iPhone 15 Pro"
flutter run -d "Pixel_7_API_34"
```

## 🧪 **Testing Tools**

### Appium (Mobile Automation)
```bash
# Check setup
appium-doctor

# Start Appium server
appium

# Run tests
npm test
```

### Detox (React Native E2E)
```bash
# Setup Detox
detox init

# Run E2E tests
test-ios
test-android
```

### Playwright (Cross-Browser)
```bash
# Install browsers
npx playwright install

# Run tests
npx playwright test

# Test mobile viewport
npx playwright test --config=playwright.config.mobile.js
```

## 📊 **Performance Testing**

### Lighthouse (Web Performance)
```bash
# Test mobile performance
lighthouse-mobile https://your-app.com

# Test with throttling
lighthouse --form-factor=mobile --throttling-method=devtools https://your-app.com
```

### Flipper (Mobile Debugging)
```bash
# Start Flipper
flipper

# Connect your app to Flipper for debugging
```

## 🔧 **Useful Commands**

### Device Management
```bash
# List all connected devices
adb devices

# Restart ADB server
adb kill-server && adb start-server

# Clear app data
adb shell pm clear com.yourapp.package
```

### iOS Simulator
```bash
# Reset simulator
xcrun simctl erase all

# Take screenshot
xcrun simctl io booted screenshot screenshot.png

# Record video
xcrun simctl io booted recordVideo video.mov
```

## 📱 **Testing Your Job Search Assistant**

### 1. Browser Testing
```bash
# Test responsive design
npx playwright test --config=playwright.config.mobile.js

# Test specific viewport
npx playwright test --viewport-size=375,812
```

### 2. Mobile App Testing
```bash
# Create React Native version
npx react-native@latest init JobSearchApp

# Or create Expo version
npx create-expo-app JobSearchApp
```

### 3. Real Device Testing
```bash
# Find your IP
ifconfig | grep "inet " | grep -v 127.0.0.1

# Test on phone: http://[YOUR_IP]:3000/admin
```

## 🎯 **Recommended Testing Workflow**

1. **Development**: Use browser dev tools for quick testing
2. **iOS Testing**: Use Xcode Simulator for iOS-specific features
3. **Android Testing**: Use Android Studio Emulator for Android features
4. **Real Device**: Use Expo Go app for real device testing
5. **Production**: Use BrowserStack for comprehensive testing

## 💡 **Pro Tips**

- **Start with Expo** if you're new to mobile development
- **Use React Native** for more control and native features
- **Test on real devices** regularly, not just simulators
- **Use Flipper** for debugging network requests and state
- **Set up CI/CD** with GitHub Actions for automated testing
- **Monitor performance** with Lighthouse and Flipper

## 🚨 **Troubleshooting**

### Common Issues
```bash
# Metro bundler issues
npx react-native start --reset-cache

# Android build issues
cd android && ./gradlew clean

# iOS build issues
cd ios && xcodebuild clean
```

### Reset Everything
```bash
# Reset React Native
npx react-native clean

# Reset Expo
expo r -c

# Reset Flutter
flutter clean
```

## 📚 **Resources**

- [React Native Docs](https://reactnative.dev/)
- [Expo Docs](https://docs.expo.dev/)
- [Flutter Docs](https://flutter.dev/docs)
- [Appium Docs](http://appium.io/docs/)
- [Playwright Docs](https://playwright.dev/)
- [Flipper Docs](https://fbflipper.com/)

---

**Happy Mobile Development!** 🚀📱

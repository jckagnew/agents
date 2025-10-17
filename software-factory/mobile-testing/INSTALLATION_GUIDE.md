# 📱 Mobile SDK Installation Guide for Software Factory

## 🎯 **Current Status:**
- ✅ **Android Studio**: Installed
- ⚠️ **Android SDK**: Needs configuration
- ⚠️ **Xcode**: Needs installation
- ✅ **Web Testing**: Working perfectly

---

## 🍎 **Step 1: Install Xcode (iOS Development)**

### **Download and Install Xcode:**
1. **Open App Store** (I've opened it for you)
2. **Search for "Xcode"**
3. **Click "Get" or "Install"** (Free, but ~15GB download)
4. **Wait for download** (30-60 minutes depending on internet speed)
5. **Open Xcode** and accept license agreement
6. **Install additional components** when prompted

### **After Xcode Installation:**
```bash
# Verify Xcode installation
xcodebuild -version

# Install iOS Simulator (if not already installed)
sudo xcode-select --install
```

---

## 🤖 **Step 2: Configure Android Studio (Android Development)**

### **Android Studio is already installed! Now configure the SDK:**

1. **Android Studio should be opening now**
2. **If it's your first time:**
   - Follow the setup wizard
   - Choose "Standard" installation
   - Accept all license agreements
   - Let it download Android SDK components

3. **If Android Studio is already configured:**
   - Go to **Tools → SDK Manager**
   - Install **Android 13 (API 33)** or latest
   - Install **Android SDK Build-Tools**
   - Install **Android Emulator**

### **Configure Environment Variables:**
```bash
# Add to your ~/.zshrc file (already done by our script)
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools

# Apply changes
source ~/.zshrc
```

---

## 🚀 **Step 3: Test Your Setup**

### **After both installations are complete:**

```bash
# Navigate to mobile testing directory
cd software-factory/mobile-testing

# Verify installations
./install-mobile-sdks.sh verify

# Test all platforms
./test-universal-app.sh all
```

---

## 📱 **Step 4: Create Android Virtual Device (AVD)**

### **In Android Studio:**
1. **Open AVD Manager**: Tools → AVD Manager
2. **Create Virtual Device**: Click "Create Virtual Device"
3. **Choose Device**: Select "Pixel 7" or similar
4. **Choose System Image**: Select "Android 13 (API 33)"
5. **Configure AVD**: Name it "SoftwareFactory_Android"
6. **Finish**: Click "Finish"

### **Or use command line:**
```bash
# List available system images
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --list | grep "system-images"

# Install Android 13 system image
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager "system-images;android-33;google_apis;x86_64"

# Create AVD
$ANDROID_HOME/cmdline-tools/latest/bin/avdmanager create avd -n "SoftwareFactory_Android" -k "system-images;android-33;google_apis;x86_64"
```

---

## 🎯 **Step 5: Test iOS Simulator**

### **After Xcode installation:**
```bash
# List available simulators
xcrun simctl list devices

# Boot iPhone 15 Pro simulator
xcrun simctl boot "iPhone 15 Pro"

# Open Simulator app
open -a Simulator
```

---

## ✅ **Verification Checklist**

### **After installation, verify everything works:**

- [ ] **Xcode installed**: `xcodebuild -version` shows version
- [ ] **Android Studio installed**: Can open from Applications
- [ ] **Android SDK configured**: `echo $ANDROID_HOME` shows path
- [ ] **ADB available**: `adb version` shows version
- [ ] **iOS Simulator**: `xcrun simctl list devices` shows devices
- [ ] **Android Emulator**: `emulator -list-avds` shows AVDs

### **Test your Weight Tracker app:**
```bash
# Test web version (should work now)
./test-universal-app.sh web

# Test Android version (after SDK setup)
./test-universal-app.sh android

# Test iOS version (after Xcode installation)
./test-universal-app.sh ios

# Test all platforms
./test-universal-app.sh all
```

---

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **Android SDK not found:**
```bash
# Find Android SDK location
find /Users -name "Android" -type d 2>/dev/null | grep -i sdk

# Set ANDROID_HOME manually
export ANDROID_HOME=/path/to/android/sdk
```

#### **Xcode command line tools:**
```bash
# Reset Xcode path
sudo xcode-select --reset

# Set Xcode path
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
```

#### **Permission issues:**
```bash
# Fix Android SDK permissions
sudo chown -R $(whoami) $ANDROID_HOME
```

---

## 🎉 **Expected Results**

### **After successful installation:**
- ✅ **Web App**: http://localhost:3003 (working now)
- ✅ **Android App**: Running on emulator
- ✅ **iOS App**: Running on simulator
- ✅ **Universal Testing**: All platforms working

### **Your Software Factory will have:**
- **Complete mobile testing environment**
- **Universal app development capabilities**
- **Production-ready app generation**
- **Cross-platform testing automation**

---

## 📞 **Need Help?**

If you encounter issues:
1. Check the troubleshooting section above
2. Run `./install-mobile-sdks.sh verify` to check status
3. Check the logs in `mobile-testing/logs/`
4. Ensure all downloads completed successfully

**🎯 Once both Xcode and Android SDK are properly installed, your Software Factory will have complete universal app testing capabilities!**

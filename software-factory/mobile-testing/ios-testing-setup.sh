#!/bin/bash

# iOS Testing Setup Script
# Configures iOS Simulator and testing environment

echo "🍎 Setting up iOS Testing Environment..."

# Check if Xcode is installed
if [ ! -d "/Applications/Xcode.app" ]; then
    echo "❌ Xcode not found. Please install Xcode from the App Store."
    exit 1
fi

echo "✅ Xcode found at /Applications/Xcode.app"

# Accept Xcode license if needed
echo "📋 Accepting Xcode license..."
sudo xcodebuild -license accept

# Install iOS Simulator if not already installed
echo "📱 Checking iOS Simulator..."
if ! xcrun simctl list devices > /dev/null 2>&1; then
    echo "Installing iOS Simulator..."
    xcodebuild -downloadPlatform iOS
fi

# List available simulators
echo "📱 Available iOS Simulators:"
xcrun simctl list devices available | grep "iPhone\|iPad"

# Create a test iOS app for verification
echo "🧪 Creating test iOS app..."
mkdir -p ios-test-app
cd ios-test-app

# Create a simple React Native test app
cat > package.json << 'EOF'
{
  "name": "ios-test-app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "ios": "react-native run-ios",
    "android": "react-native run-android",
    "start": "react-native start"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.72.0"
  }
}
EOF

# Create a simple test component
cat > App.js << 'EOF'
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

const App = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>iOS Test App</Text>
      <Text style={styles.subtitle}>Testing iOS Simulator</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f0f0f0',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
  },
});

export default App;
EOF

echo "✅ iOS test app created"

# Create iOS testing verification script
cat > verify-ios.sh << 'EOF'
#!/bin/bash

echo "🍎 Verifying iOS Testing Setup..."

# Check if simulator is running
if pgrep -f "Simulator" > /dev/null; then
    echo "✅ iOS Simulator is running"
else
    echo "❌ iOS Simulator is not running"
    echo "Starting iOS Simulator..."
    open -a Simulator
    sleep 5
fi

# Check available devices
echo "📱 Available iOS devices:"
xcrun simctl list devices available | grep "iPhone\|iPad" | head -5

# Test simulator functionality
echo "🧪 Testing simulator functionality..."
xcrun simctl list devices | grep "Booted" || echo "No devices currently booted"

echo "✅ iOS testing setup complete"
EOF

chmod +x verify-ios.sh

echo "✅ iOS testing setup complete!"
echo "Run './verify-ios.sh' to verify the setup"

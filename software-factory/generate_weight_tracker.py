#!/usr/bin/env python3
"""
Generate Universal Weight Tracker App
Based on the workflow screens provided
"""

import os
import json
import shutil
from typing import Dict, Any, List

def generate_weight_tracker_app():
    """Generate a universal Weight Tracker app"""
    
    print("🚀 Generating Universal Weight Tracker App...")
    
    # App configuration
    app_name = "Weight Tracker Pro"
    app_description = "Privacy-first weight tracking with body composition analysis and advanced analytics"
    bundle_id = "com.weighttrackerpro.app"
    version = "1.0.0"
    features = ["Dashboard", "Log Entry", "History", "Analytics", "Settings", "Paywall"]
    
    # Create output directory
    app_path = f"generated-apps/{app_name.lower().replace(' ', '-')}"
    os.makedirs(app_path, exist_ok=True)
    
    # Create directory structure
    dirs = [
        "src/screens",
        "src/components", 
        "src/navigation",
        "src/services",
        "src/hooks",
        "src/utils",
        "src/types",
        "web",
        "mobile",
        "shared",
        ".github/workflows",
        "assets"
    ]
    
    for dir_path in dirs:
        os.makedirs(os.path.join(app_path, dir_path), exist_ok=True)
    
    # Generate package.json
    package_json = {
        "name": app_name.lower().replace(" ", "-"),
        "version": version,
        "description": app_description,
        "main": "index.js",
        "scripts": {
            "start": "expo start",
            "ios": "expo start --ios",
            "android": "expo start --android",
            "web": "expo start --web",
            "build:ios": "expo build:ios",
            "build:android": "expo build:android",
            "build:web": "next build",
            "test:all": "jest",
            "lint": "eslint . --ext .js,.jsx,.ts,.tsx"
        },
        "dependencies": {
            "@expo/vector-icons": "^14.0.0",
            "@react-navigation/bottom-tabs": "^6.5.11",
            "@react-navigation/native": "^6.1.9",
            "@react-navigation/stack": "^6.3.20",
            "expo": "~50.0.0",
            "expo-constants": "~15.4.0",
            "expo-font": "~11.10.0",
            "expo-linking": "~6.2.0",
            "expo-router": "~3.4.0",
            "expo-splash-screen": "~0.26.0",
            "expo-status-bar": "~1.11.0",
            "expo-web-browser": "~12.8.0",
            "next": "14.0.0",
            "react": "18.2.0",
            "react-dom": "18.2.0",
            "react-native": "0.73.0",
            "react-native-gesture-handler": "~2.14.0",
            "react-native-reanimated": "~3.6.0",
            "react-native-safe-area-context": "4.8.0",
            "react-native-screens": "~3.29.0",
            "react-native-svg": "14.1.0",
            "react-native-web": "~0.19.6",
            "zustand": "^4.4.7"
        },
        "devDependencies": {
            "@babel/core": "^7.20.0",
            "@types/jest": "^29.5.8",
            "@types/react": "~18.2.45",
            "@types/react-native": "~0.73.0",
            "@typescript-eslint/eslint-plugin": "^6.13.0",
            "@typescript-eslint/parser": "^6.13.0",
            "eslint": "^8.54.0",
            "eslint-config-expo": "^7.0.0",
            "jest": "^29.2.1",
            "jest-expo": "~50.0.0",
            "react-test-renderer": "18.2.0",
            "typescript": "^5.1.3"
        },
        "private": True
    }
    
    with open(os.path.join(app_path, "package.json"), 'w') as f:
        json.dump(package_json, f, indent=2)
    
    # Generate expo.json
    expo_json = {
        "expo": {
            "name": app_name,
            "slug": app_name.lower().replace(" ", "-"),
            "version": version,
            "orientation": "portrait",
            "icon": "./assets/icon.png",
            "userInterfaceStyle": "light",
            "splash": {
                "image": "./assets/splash.png",
                "resizeMode": "contain",
                "backgroundColor": "#ffffff"
            },
            "assetBundlePatterns": ["**/*"],
            "ios": {
                "supportsTablet": True,
                "bundleIdentifier": bundle_id
            },
            "android": {
                "adaptiveIcon": {
                    "foregroundImage": "./assets/adaptive-icon.png",
                    "backgroundColor": "#ffffff"
                },
                "package": bundle_id
            },
            "web": {
                "favicon": "./assets/favicon.png",
                "bundler": "metro"
            },
            "plugins": [
                "expo-router",
                [
                    "expo-build-properties",
                    {
                        "ios": {"newArchEnabled": True},
                        "android": {"newArchEnabled": True}
                    }
                ]
            ],
            "experiments": {
                "typedRoutes": True
            }
        }
    }
    
    with open(os.path.join(app_path, "expo.json"), 'w') as f:
        json.dump(expo_json, f, indent=2)
    
    # Generate App.tsx
    app_tsx_content = f'''/**
 * {app_name}
 * {app_description}
 * Universal app for iOS, Android, and Web
 */

import React from 'react';
import {{ Platform }} from 'react-native';
import {{ NavigationContainer }} from '@react-navigation/native';
import {{ createStackNavigator }} from '@react-navigation/stack';
import {{ createBottomTabNavigator }} from '@react-navigation/bottom-tabs';
import {{ StatusBar }} from 'expo-status-bar';
import {{ Ionicons }} from '@expo/vector-icons';

// Screens
import {{ DashboardScreen }} from './src/screens/DashboardScreen';
import {{ LogEntryScreen }} from './src/screens/LogEntryScreen';
import {{ HistoryScreen }} from './src/screens/HistoryScreen';
import {{ AnalyticsScreen }} from './src/screens/AnalyticsScreen';
import {{ SettingsScreen }} from './src/screens/SettingsScreen';
import {{ PaywallScreen }} from './src/screens/PaywallScreen';

// Types
type RootStackParamList = {{
  MainTabs: undefined;
  LogEntry: {{ date: string }};
  Paywall: undefined;
}};

type TabParamList = {{
  Dashboard: undefined;
  History: undefined;
  Analytics: undefined;
  Settings: undefined;
}};

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

// Tab Navigator Component
const MainTabNavigator = () => {{
  return (
    <Tab.Navigator
      screenOptions={{{{ route }}) => ({{
        tabBarIcon: ({{ focused, color, size }}) => {{
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Dashboard') {{
            iconName = focused ? 'home' : 'home-outline';
          }} else if (route.name === 'History') {{
            iconName = focused ? 'time' : 'time-outline';
          }} else if (route.name === 'Analytics') {{
            iconName = focused ? 'analytics' : 'analytics-outline';
          }} else if (route.name === 'Settings') {{
            iconName = focused ? 'settings' : 'settings-outline';
          }} else {{
            iconName = 'help-outline';
          }}

          return <Ionicons name={{iconName}} size={{size}} color={{color}} />;
        }},
        tabBarActiveTintColor: '#2196F3',
        tabBarInactiveTintColor: '#666',
        tabBarStyle: {{
          backgroundColor: '#fff',
          borderTopWidth: 1,
          borderTopColor: '#e0e0e0',
          paddingBottom: Platform.OS === 'ios' ? 20 : 5,
          paddingTop: 5,
          height: Platform.OS === 'ios' ? 85 : 60,
        }},
        tabBarLabelStyle: {{
          fontSize: 12,
          fontWeight: '600',
        }},
        headerStyle: {{
          backgroundColor: '#2196F3',
          elevation: 0,
          shadowOpacity: 0,
        }},
        headerTintColor: '#fff',
        headerTitleStyle: {{
          fontWeight: 'bold',
          fontSize: 18,
        }},
      }})}
    >
      <Tab.Screen
        name="Dashboard"
        component={{DashboardScreen}}
        options={{
          title: 'Weight Tracker',
          headerShown: false,
        }}
      />
      <Tab.Screen
        name="History"
        component={{HistoryScreen}}
        options={{
          title: 'History',
        }}
      />
      <Tab.Screen
        name="Analytics"
        component={{AnalyticsScreen}}
        options={{
          title: 'Analytics',
        }}
      />
      <Tab.Screen
        name="Settings"
        component={{SettingsScreen}}
        options={{
          title: 'Settings',
        }}
      />
    </Tab.Navigator>
  );
}};

export default function App() {{
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator
        initialRouteName="MainTabs"
        screenOptions={{
          headerStyle: {{
            backgroundColor: '#2196F3',
          }},
          headerTintColor: '#fff',
          headerTitleStyle: {{
            fontWeight: 'bold',
          }},
        }}
      >
        <Stack.Screen
          name="MainTabs"
          component={{MainTabNavigator}}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="LogEntry"
          component={{LogEntryScreen}}
          options={{
            title: 'Log Entry',
            headerBackTitleVisible: false,
          }}
        />
        <Stack.Screen
          name="Paywall"
          component={{PaywallScreen}}
          options={{
            title: 'Upgrade to Pro',
            headerBackTitleVisible: false,
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}};
'''
    
    with open(os.path.join(app_path, "App.tsx"), 'w') as f:
        f.write(app_tsx_content)
    
    # Generate screen components
    for feature in features:
        screen_name = feature.title().replace(' ', '')
        screen_content = generate_screen_component(feature, app_name, app_description)
        screen_filename = f"{screen_name}Screen.tsx"
        with open(os.path.join(app_path, "src", "screens", screen_filename), 'w') as f:
            f.write(screen_content)
    
    # Generate README
    readme_content = f'''# {app_name}

{app_description}

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run start

# Run on specific platforms
npm run ios      # iOS Simulator
npm run android  # Android Emulator
npm run web      # Web Browser
```

## 📱 Platforms

- ✅ **iOS**: Native app with App Store deployment
- ✅ **Android**: Native app with Google Play deployment
- ✅ **Web**: Progressive Web App (PWA)

## ✨ Features

{chr(10).join([f"- {feature}" for feature in features])}

## 🏗️ Architecture

This is a universal app built with:
- **React Native + Expo** for mobile platforms
- **Next.js + React Native Web** for web platform
- **TypeScript** for type safety
- **React Navigation** for universal navigation
- **Zustand** for state management

## 📦 Deployment

```bash
# Build for all platforms
npm run build:all

# Deploy to app stores
npm run deploy:mobile

# Deploy to web
npm run deploy:web
```

## 🧪 Testing

```bash
# Run all tests
npm run test:all

# Platform-specific tests
npm run test:ios
npm run test:android
npm run test:web
```

## 📚 Documentation

- [React Native Docs](https://reactnative.dev/)
- [Expo Docs](https://docs.expo.dev/)
- [React Navigation](https://reactnavigation.org/)
- [Next.js Docs](https://nextjs.org/docs)

## 🔧 Development

This app follows the workflow screens provided:
1. **Dashboard**: Main overview with weight tracking
2. **Log Entry**: Add/update daily measurements
3. **History**: View past entries
4. **Analytics**: Charts and insights
5. **Settings**: App configuration
6. **Paywall**: Pro upgrade flow

## 📄 License

Private - All rights reserved
'''
    
    with open(os.path.join(app_path, "README.md"), 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Universal Weight Tracker app generated successfully!")
    print(f"📁 Location: {app_path}")
    print(f"📱 Platforms: iOS, Android, Web")
    print(f"✨ Features: {', '.join(features)}")
    print("\n🚀 Next Steps:")
    print(f"  1. Navigate to the app directory: cd {app_path}")
    print("  2. Install dependencies: npm install")
    print("  3. Start development server: npm run start")
    print("  4. Run on iOS: npm run ios")
    print("  5. Run on Android: npm run android")
    print("  6. Run on Web: npm run web")
    
    return {
        "success": True,
        "app_path": app_path,
        "platforms": ["ios", "android", "web"],
        "features": features
    }

def generate_screen_component(feature: str, app_name: str, app_description: str) -> str:
    """Generate a screen component"""
    screen_name = feature.title().replace(' ', '')
    
    # Special handling for specific screens
    if feature.lower() == "dashboard":
        return f'''/**
 * {app_name} - {feature.title()} Screen
 * Main dashboard with weight tracking overview
 */

import React from 'react';
import {{
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Platform,
  Dimensions,
}} from 'react-native';
import {{ Ionicons }} from '@expo/vector-icons';

const {{ width: screenWidth }} = Dimensions.get('window');

interface {screen_name}ScreenProps {{
  navigation: any;
}}

export const {screen_name}Screen: React.FC<{screen_name}ScreenProps> = ({{ navigation }}) => {{
  return (
    <ScrollView style={{styles.container}}>
      <View style={{styles.header}}>
        <View style={{styles.headerContent}}>
          <Text style={{styles.title}}>Weight Tracker</Text>
          <Text style={{styles.subtitle}}>Privacy-first tracking</Text>
        </View>
        <TouchableOpacity
          style={{styles.settingsButton}}
          onPress={{() => navigation.navigate('Settings')}}
        >
          <Ionicons name="settings-outline" size={24} color="white" />
        </TouchableOpacity>
      </View>

      <View style={{styles.summaryCard}}>
        <Text style={{styles.cardTitle}}>Today's Summary</Text>
        <View style={{styles.summaryContent}}>
          <Text style={{styles.weightText}}>185.2 lbs</Text>
          <Text style={{styles.bfText}}>Navy BF%: 15.2%</Text>
          <Text style={{styles.smoothedText}}>7-day avg: 185.8 lbs</Text>
          <Text style={{styles.changeText}}>-0.3%</Text>
        </View>
      </View>

      <View style={{styles.chartCard}}>
        <Text style={{styles.cardTitle}}>Weight Trend (Last 30 Days)</Text>
        <View style={{styles.chartPlaceholder}}>
          <Text style={{styles.chartText}}>📊 Weight Chart</Text>
          <Text style={{styles.chartSubtext}}>Pro: Unlock smoothing controls</Text>
        </View>
      </View>

      <View style={{styles.actionButtons}}>
        <TouchableOpacity 
          style={{styles.primaryButton}} 
          onPress={{() => navigation.navigate('LogEntry', {{ date: new Date().toISOString().split('T')[0] }})}}
        >
          <Ionicons name="add-circle" size={24} color="white" style={{styles.buttonIcon}} />
          <Text style={{styles.buttonText}}>Log Entry</Text>
        </TouchableOpacity>

        <View style={{styles.secondaryButtons}}>
          <TouchableOpacity
            style={{styles.secondaryButton}}
            onPress={{() => navigation.navigate('History')}}
          >
            <Ionicons name="time-outline" size={20} color="#2196F3" style={{styles.buttonIcon}} />
            <Text style={{styles.secondaryButtonText}}>History</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={{styles.secondaryButton}}
            onPress={{() => navigation.navigate('Analytics')}}
          >
            <Ionicons name="analytics-outline" size={20} color="#2196F3" style={{styles.buttonIcon}} />
            <Text style={{styles.secondaryButtonText}}>Analytics</Text>
          </TouchableOpacity>
        </View>
      </View>
    </ScrollView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#f5f5f5',
  }},
  header: {{
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#2196F3',
  }},
  headerContent: {{
    flex: 1,
  }},
  title: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  }},
  subtitle: {{
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  }},
  settingsButton: {{
    padding: 8,
  }},
  summaryCard: {{
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 2 }},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  }},
  cardTitle: {{
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  }},
  summaryContent: {{
    alignItems: 'center',
  }},
  weightText: {{
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
    marginBottom: 8,
  }},
  bfText: {{
    fontSize: 16,
    color: '#666',
    marginBottom: 4,
  }},
  smoothedText: {{
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  }},
  changeText: {{
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
  }},
  chartCard: {{
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 2 }},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  }},
  chartPlaceholder: {{
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  }},
  chartText: {{
    fontSize: 18,
    color: '#666',
  }},
  chartSubtext: {{
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    fontStyle: 'italic',
  }},
  actionButtons: {{
    margin: 16,
    gap: 12,
  }},
  primaryButton: {{
    backgroundColor: '#2196F3',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 2 }},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  }},
  buttonIcon: {{
    marginRight: 8,
  }},
  buttonText: {{
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  }},
  secondaryButtons: {{
    flexDirection: 'row',
    gap: 12,
  }},
  secondaryButton: {{
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#2196F3',
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 1 }},
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  }},
  secondaryButtonText: {{
    color: '#2196F3',
    fontSize: 16,
    fontWeight: 'bold',
  }},
}});
'''
    
    elif feature.lower() == "log entry":
        return f'''/**
 * {app_name} - {feature.title()} Screen
 * Log daily weight and body measurements
 */

import React, {{ useState }} from 'react';
import {{
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Platform,
  Alert,
}} from 'react-native';
import {{ Ionicons }} from '@expo/vector-icons';

interface {screen_name}ScreenProps {{
  navigation: any;
  route: {{
    params: {{
      date: string;
    }};
  }};
}}

export const {screen_name}Screen: React.FC<{screen_name}ScreenProps> = ({{ navigation, route }}) => {{
  const {{ date }} = route.params;
  const [weight, setWeight] = useState('');
  const [neck, setNeck] = useState('');
  const [upperWaist, setUpperWaist] = useState('');
  const [lowerWaist, setLowerWaist] = useState('');
  const [hips, setHips] = useState('');
  const [notes, setNotes] = useState('');

  const handleSave = () => {{
    if (!weight || !neck || !upperWaist || !lowerWaist || !hips) {{
      Alert.alert('Missing Data', 'Please fill in all required measurements.');
      return;
    }}
    
    // Save logic here
    Alert.alert('Success', 'Entry saved successfully!');
    navigation.goBack();
  }};

  return (
    <ScrollView style={{styles.container}}>
      <View style={{styles.header}}>
        <Text style={{styles.title}}>Log Entry</Text>
        <Text style={{styles.date}}>{{new Date(date).toLocaleDateString()}}</Text>
      </View>

      <View style={{styles.form}}>
        <View style={{styles.inputGroup}}>
          <Text style={{styles.label}}>Weight (lbs)</Text>
          <TextInput
            style={{styles.input}}
            value={{weight}}
            onChangeText={{setWeight}}
            keyboardType="numeric"
            placeholder="185.2"
            accessibilityLabel="Weight input"
            accessibilityHint="Enter your weight in pounds"
          />
        </View>

        <View style={{styles.inputGroup}}>
          <Text style={{styles.label}}>Neck (inches)</Text>
          <TextInput
            style={{styles.input}}
            value={{neck}}
            onChangeText={{setNeck}}
            keyboardType="numeric"
            placeholder="15.5"
            accessibilityLabel="Neck measurement input"
            accessibilityHint="Enter your neck measurement in inches"
          />
        </View>

        <View style={{styles.inputGroup}}>
          <Text style={{styles.label}}>Upper Waist (inches)</Text>
          <TextInput
            style={{styles.input}}
            value={{upperWaist}}
            onChangeText={{setUpperWaist}}
            keyboardType="numeric"
            placeholder="32.0"
            accessibilityLabel="Upper waist measurement input"
            accessibilityHint="Enter your upper waist measurement in inches"
          />
        </View>

        <View style={{styles.inputGroup}}>
          <Text style={{styles.label}}>Lower Waist (inches)</Text>
          <TextInput
            style={{styles.input}}
            value={{lowerWaist}}
            onChangeText={{setLowerWaist}}
            keyboardType="numeric"
            placeholder="34.5"
            accessibilityLabel="Lower waist measurement input"
            accessibilityHint="Enter your lower waist measurement in inches"
          />
        </View>

        <View style={{styles.inputGroup}}>
          <Text style={{styles.label}}>Hips (inches)</Text>
          <TextInput
            style={{styles.input}}
            value={{hips}}
            onChangeText={{setHips}}
            keyboardType="numeric"
            placeholder="38.0"
            accessibilityLabel="Hips measurement input"
            accessibilityHint="Enter your hips measurement in inches"
          />
        </View>

        <View style={{styles.inputGroup}}>
          <Text style={{styles.label}}>Notes (optional)</Text>
          <TextInput
            style={{[styles.input, styles.textArea]}}
            value={{notes}}
            onChangeText={{setNotes}}
            multiline
            numberOfLines={3}
            placeholder="Any additional notes..."
            accessibilityLabel="Notes input"
            accessibilityHint="Enter any additional notes about your entry"
          />
        </View>
      </View>

      <View style={{styles.actions}}>
        <TouchableOpacity style={{styles.cancelButton}} onPress={{() => navigation.goBack()}}>
          <Text style={{styles.cancelButtonText}}>Cancel</Text>
        </TouchableOpacity>
        
        <TouchableOpacity style={{styles.saveButton}} onPress={{handleSave}}>
          <Ionicons name="checkmark" size={20} color="white" style={{styles.buttonIcon}} />
          <Text style={{styles.saveButtonText}}>Save Entry</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#f5f5f5',
  }},
  header: {{
    padding: 20,
    backgroundColor: '#2196F3',
    alignItems: 'center',
  }},
  title: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  }},
  date: {{
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  }},
  form: {{
    padding: 20,
  }},
  inputGroup: {{
    marginBottom: 20,
  }},
  label: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  }},
  input: {{
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: 'white',
  }},
  textArea: {{
    height: 80,
    textAlignVertical: 'top',
  }},
  actions: {{
    flexDirection: 'row',
    padding: 20,
    gap: 12,
  }},
  cancelButton: {{
    flex: 1,
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#ddd',
    backgroundColor: 'white',
  }},
  cancelButtonText: {{
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  }},
  saveButton: {{
    flex: 1,
    backgroundColor: '#2196F3',
    padding: 16,
    borderRadius: 8,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
  }},
  saveButtonText: {{
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  }},
  buttonIcon: {{
    marginRight: 8,
  }},
}});
'''
    
    else:
        # Generic screen for other features
        return f'''/**
 * {app_name} - {feature.title()} Screen
 * {app_description}
 */

import React from 'react';
import {{
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Platform,
}} from 'react-native';
import {{ Ionicons }} from '@expo/vector-icons';

interface {screen_name}ScreenProps {{
  navigation: any;
}}

export const {screen_name}Screen: React.FC<{screen_name}ScreenProps> = ({{ navigation }}) => {{
  return (
    <ScrollView style={{styles.container}}>
      <View style={{styles.header}}>
        <Text style={{styles.title}}>{feature.title()}</Text>
        <Text style={{styles.subtitle}}>{app_description}</Text>
      </View>

      <View style={{styles.content}}>
        <Text style={{styles.description}}>
          This is the {feature.lower()} screen for {app_name}.
          Platform: {{Platform.OS}}
        </Text>

        <TouchableOpacity style={{styles.button}}>
          <Ionicons name="add-circle" size={24} color="white" style={{styles.buttonIcon}} />
          <Text style={{styles.buttonText}}>Add {feature.title()}</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    backgroundColor: '#f5f5f5',
  }},
  header: {{
    padding: 20,
    backgroundColor: '#2196F3',
  }},
  title: {{
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  }},
  subtitle: {{
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  }},
  content: {{
    padding: 20,
  }},
  description: {{
    fontSize: 16,
    color: '#333',
    marginBottom: 20,
  }},
  button: {{
    backgroundColor: '#2196F3',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: {{ width: 0, height: 2 }},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  }},
  buttonIcon: {{
    marginRight: 8,
  }},
  buttonText: {{
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  }},
}});
'''

if __name__ == "__main__":
    generate_weight_tracker_app()

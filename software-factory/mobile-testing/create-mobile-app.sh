#!/bin/bash

# Create Mobile App Script for Software Factory
# This script creates a React Native version of any app for mobile testing

set -e

echo "📱 Creating Mobile App for Software Factory Testing..."

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

# Get app name from argument or use default
APP_NAME=${1:-"weight-tracker-mobile"}
APP_DISPLAY_NAME=${2:-"Weight Tracker Mobile"}

print_status "Creating mobile app: $APP_NAME"

# Create mobile app directory
MOBILE_APP_DIR="mobile-apps/$APP_NAME"
mkdir -p "$MOBILE_APP_DIR"

# Initialize React Native project
print_status "Initializing React Native project..."
cd "$MOBILE_APP_DIR"

# Create package.json
cat > package.json << EOF
{
  "name": "$APP_NAME",
  "version": "1.0.0",
  "description": "$APP_DISPLAY_NAME - Universal Mobile App",
  "main": "index.js",
  "scripts": {
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "start": "react-native start",
    "test": "jest",
    "lint": "eslint .",
    "web": "expo start --web"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.73.2",
    "@react-navigation/native": "^6.1.9",
    "@react-navigation/stack": "^6.3.20",
    "@react-navigation/bottom-tabs": "^6.5.11",
    "react-native-screens": "~3.29.0",
    "react-native-safe-area-context": "4.8.2",
    "react-native-gesture-handler": "~2.14.0",
    "react-native-vector-icons": "^10.0.3",
    "react-native-chart-kit": "^6.12.0",
    "react-native-svg": "13.14.0",
    "expo": "~50.0.5",
    "expo-status-bar": "~1.11.1",
    "@expo/vector-icons": "^14.0.0"
  },
  "devDependencies": {
    "@babel/core": "^7.20.0",
    "@babel/preset-env": "^7.20.0",
    "@babel/runtime": "^7.20.0",
    "@react-native/eslint-config": "^0.73.1",
    "@react-native/metro-config": "^0.73.2",
    "@react-native/typescript-config": "^0.73.1",
    "@types/react": "^18.2.6",
    "@types/react-test-renderer": "^18.0.0",
    "babel-jest": "^29.6.3",
    "eslint": "^8.19.0",
    "jest": "^29.6.3",
    "metro-react-native-babel-preset": "0.77.0",
    "prettier": "^2.8.8",
    "react-test-renderer": "18.2.0",
    "typescript": "5.0.4"
  },
  "engines": {
    "node": ">=18"
  }
}
EOF

# Create app.json for Expo
cat > app.json << EOF
{
  "expo": {
    "name": "$APP_DISPLAY_NAME",
    "slug": "$APP_NAME",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "light",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#2196F3"
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.softwarefactory.$APP_NAME"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#FFFFFF"
      },
      "package": "com.softwarefactory.$APP_NAME"
    },
    "web": {
      "favicon": "./assets/favicon.png",
      "bundler": "metro"
    }
  }
}
EOF

# Create index.js
cat > index.js << 'EOF'
import { AppRegistry } from 'react-native';
import App from './src/App';
import { name as appName } from './package.json';

AppRegistry.registerComponent(appName, () => App);
EOF

# Create src directory structure
mkdir -p src/{components,screens,context,utils,assets}

# Create App.tsx
cat > src/App.tsx << 'EOF'
import React, { useState } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';

// Context
import { WeightProvider } from './context/WeightContext';

// Screens
import DashboardScreen from './screens/DashboardScreen';
import HistoryScreen from './screens/HistoryScreen';
import LogEntryScreen from './screens/LogEntryScreen';
import AnalyticsScreen from './screens/AnalyticsScreen';
import SettingsScreen from './screens/SettingsScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function MainTabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'History') {
            iconName = focused ? 'time' : 'time-outline';
          } else if (route.name === 'Analytics') {
            iconName = focused ? 'analytics' : 'analytics-outline';
          } else if (route.name === 'Settings') {
            iconName = focused ? 'settings' : 'settings-outline';
          } else {
            iconName = 'help-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#2196F3',
        tabBarInactiveTintColor: '#666',
        headerStyle: {
          backgroundColor: '#2196F3',
        },
        headerTintColor: '#fff',
        headerTitleStyle: {
          fontWeight: 'bold',
        },
      })}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen}
        options={{ title: 'Weight Tracker' }}
      />
      <Tab.Screen 
        name="History" 
        component={HistoryScreen}
        options={{ title: 'History' }}
      />
      <Tab.Screen 
        name="Analytics" 
        component={AnalyticsScreen}
        options={{ title: 'Analytics' }}
      />
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen}
        options={{ title: 'Settings' }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <WeightProvider>
      <NavigationContainer>
        <StatusBar style="light" />
        <Stack.Navigator
          screenOptions={{
            headerStyle: {
              backgroundColor: '#2196F3',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
          }}
        >
          <Stack.Screen
            name="MainTabs"
            component={MainTabNavigator}
            options={{ headerShown: false }}
          />
          <Stack.Screen
            name="LogEntry"
            component={LogEntryScreen}
            options={{
              title: 'Log Entry',
              headerBackTitleVisible: false,
            }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </WeightProvider>
  );
}
EOF

# Create WeightContext
cat > src/context/WeightContext.tsx << 'EOF'
import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface WeightEntry {
  id: string;
  date: string;
  weight: number;
  bodyFat: number;
  notes?: string;
}

interface WeightContextType {
  entries: WeightEntry[];
  addEntry: (entry: Omit<WeightEntry, 'id'>) => void;
  updateEntry: (id: string, entry: Partial<WeightEntry>) => void;
  deleteEntry: (id: string) => void;
  currentWeight: number;
  currentBodyFat: number;
  goalWeight: number;
  setGoalWeight: (weight: number) => void;
}

const WeightContext = createContext<WeightContextType | undefined>(undefined);

export const useWeight = () => {
  const context = useContext(WeightContext);
  if (!context) {
    throw new Error('useWeight must be used within a WeightProvider');
  }
  return context;
};

// Sample data
const initialEntries: WeightEntry[] = [
  { id: '1', date: '2025-09-15', weight: 185.2, bodyFat: 15.2 },
  { id: '2', date: '2025-09-16', weight: 184.8, bodyFat: 15.1 },
  { id: '3', date: '2025-09-17', weight: 184.5, bodyFat: 15.0 },
  { id: '4', date: '2025-09-18', weight: 184.2, bodyFat: 14.9 },
  { id: '5', date: '2025-09-19', weight: 183.9, bodyFat: 14.8 },
  { id: '6', date: '2025-09-20', weight: 183.6, bodyFat: 14.7 },
  { id: '7', date: '2025-09-21', weight: 183.3, bodyFat: 14.6 },
  { id: '8', date: '2025-09-22', weight: 183.0, bodyFat: 14.5 },
  { id: '9', date: '2025-09-23', weight: 182.7, bodyFat: 14.4 },
  { id: '10', date: '2025-09-24', weight: 182.4, bodyFat: 14.3 },
  { id: '11', date: '2025-09-25', weight: 182.1, bodyFat: 14.2 },
  { id: '12', date: '2025-09-26', weight: 181.8, bodyFat: 14.1 },
  { id: '13', date: '2025-09-27', weight: 181.5, bodyFat: 14.0 },
  { id: '14', date: '2025-09-28', weight: 181.2, bodyFat: 13.9 },
  { id: '15', date: '2025-09-29', weight: 180.9, bodyFat: 13.8 },
  { id: '16', date: '2025-09-30', weight: 180.6, bodyFat: 13.7 },
  { id: '17', date: '2025-10-01', weight: 180.3, bodyFat: 13.6 },
  { id: '18', date: '2025-10-02', weight: 180.0, bodyFat: 13.5 },
  { id: '19', date: '2025-10-03', weight: 179.7, bodyFat: 13.4 },
  { id: '20', date: '2025-10-04', weight: 179.4, bodyFat: 13.3 },
  { id: '21', date: '2025-10-05', weight: 179.1, bodyFat: 13.2 },
  { id: '22', date: '2025-10-06', weight: 178.8, bodyFat: 13.1 },
  { id: '23', date: '2025-10-07', weight: 178.5, bodyFat: 13.0 },
  { id: '24', date: '2025-10-08', weight: 178.2, bodyFat: 12.9 },
  { id: '25', date: '2025-10-09', weight: 178.4, bodyFat: 12.8 },
  { id: '26', date: '2025-10-10', weight: 178.1, bodyFat: 12.7 },
  { id: '27', date: '2025-10-11', weight: 177.8, bodyFat: 12.6 },
  { id: '28', date: '2025-10-12', weight: 177.5, bodyFat: 12.5 },
  { id: '29', date: '2025-10-13', weight: 177.2, bodyFat: 12.4 },
  { id: '30', date: '2025-10-14', weight: 178.4, bodyFat: 12.8 },
];

export const WeightProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [entries, setEntries] = useState<WeightEntry[]>(initialEntries);
  const [goalWeight, setGoalWeight] = useState(175.0);

  const addEntry = (entry: Omit<WeightEntry, 'id'>) => {
    const newEntry: WeightEntry = {
      ...entry,
      id: Date.now().toString(),
    };
    setEntries(prev => [...prev, newEntry].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()));
  };

  const updateEntry = (id: string, updatedEntry: Partial<WeightEntry>) => {
    setEntries(prev => prev.map(entry => 
      entry.id === id ? { ...entry, ...updatedEntry } : entry
    ));
  };

  const deleteEntry = (id: string) => {
    setEntries(prev => prev.filter(entry => entry.id !== id));
  };

  const currentWeight = entries[entries.length - 1]?.weight || 0;
  const currentBodyFat = entries[entries.length - 1]?.bodyFat || 0;

  const value: WeightContextType = {
    entries,
    addEntry,
    updateEntry,
    deleteEntry,
    currentWeight,
    currentBodyFat,
    goalWeight,
    setGoalWeight,
  };

  return (
    <WeightContext.Provider value={value}>
      {children}
    </WeightContext.Provider>
  );
};
EOF

# Create Dashboard Screen
cat > src/screens/DashboardScreen.tsx << 'EOF'
import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Platform,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useWeight } from '../context/WeightContext';

const { width: screenWidth } = Dimensions.get('window');

export default function DashboardScreen({ navigation }: any) {
  const { entries, currentWeight, currentBodyFat, goalWeight } = useWeight();
  
  // Calculate metrics
  const startWeight = entries[0]?.weight || 0;
  const totalLoss = startWeight - currentWeight;
  const weekAvg = entries.slice(-7).reduce((sum, entry) => sum + entry.weight, 0) / Math.min(7, entries.length);
  const weeklyLoss = totalLoss / Math.max(1, Math.floor(entries.length / 7));
  const remainingToGoal = currentWeight - goalWeight;
  const progressPercentage = Math.min(100, ((startWeight - currentWeight) / (startWeight - goalWeight)) * 100);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.title}>Weight Tracker Pro</Text>
          <Text style={styles.subtitle}>Privacy-first tracking</Text>
        </View>
        <TouchableOpacity
          style={styles.settingsButton}
          onPress={() => navigation.navigate('Settings')}
        >
          <Ionicons name="settings-outline" size={24} color="white" />
        </TouchableOpacity>
      </View>

      <View style={styles.summaryCard}>
        <Text style={styles.cardTitle}>Today's Summary</Text>
        <View style={styles.summaryContent}>
          <Text style={styles.weightText}>{currentWeight} lbs</Text>
          <Text style={styles.bfText}>Navy BF%: {currentBodyFat}%</Text>
          <Text style={styles.smoothedText}>7-day avg: {weekAvg.toFixed(1)} lbs</Text>
          <Text style={styles.changeText}>-{weeklyLoss.toFixed(1)}% this week</Text>
        </View>
      </View>

      <View style={styles.chartCard}>
        <Text style={styles.cardTitle}>Weight Trend (Last 30 Days)</Text>
        <View style={styles.chartPlaceholder}>
          <Ionicons name="stats-chart-outline" size={48} color="#999" />
          <Text style={styles.chartText}>Weight Chart</Text>
          <Text style={styles.chartSubtext}>Pro: Unlock smoothing controls</Text>
          <Text style={styles.chartData}>
            Start: {startWeight} lbs → Current: {currentWeight} lbs
          </Text>
          <Text style={styles.chartData}>
            Average weekly loss: {weeklyLoss.toFixed(1)} lbs
          </Text>
        </View>
      </View>

      <View style={styles.actionButtons}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation.navigate('LogEntry')}
        >
          <Ionicons name="add-circle" size={24} color="white" style={styles.buttonIcon} />
          <Text style={styles.buttonText}>Log Entry</Text>
        </TouchableOpacity>

        <View style={styles.secondaryButtons}>
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('History')}
          >
            <Ionicons name="time-outline" size={20} color="#2196F3" style={styles.buttonIcon} />
            <Text style={styles.secondaryButtonText}>History</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Analytics')}
          >
            <Ionicons name="analytics-outline" size={20} color="#2196F3" style={styles.buttonIcon} />
            <Text style={styles.secondaryButtonText}>Analytics</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.progressCard}>
        <Text style={styles.cardTitle}>12-Week Progress</Text>
        <View style={styles.progressGrid}>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{totalLoss.toFixed(1)} lbs</Text>
            <Text style={styles.progressLabel}>Total Lost</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{weeklyLoss.toFixed(1)} lbs</Text>
            <Text style={styles.progressLabel}>Per Week</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{(15.2 - currentBodyFat).toFixed(1)}%</Text>
            <Text style={styles.progressLabel}>BF Reduction</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{Math.ceil(remainingToGoal / weeklyLoss)}</Text>
            <Text style={styles.progressLabel}>Days to Goal</Text>
          </View>
        </View>
        <View style={styles.progressBar}>
          <View 
            style={[styles.progressFill, { width: `${progressPercentage}%` }]}
          />
        </View>
        <Text style={styles.progressText}>
          {Math.round(progressPercentage)}% to goal
        </Text>
      </View>

      <View style={styles.platformCard}>
        <Text style={styles.cardTitle}>Universal App Demo</Text>
        <Text style={styles.platformText}>
          This sophisticated Weight Tracker app runs natively on:
        </Text>
        <View style={styles.platformBadges}>
          <View style={styles.platformBadge}>
            <Ionicons name="logo-apple" size={16} color="#007AFF" />
            <Text style={styles.platformBadgeText}>iOS</Text>
          </View>
          <View style={styles.platformBadge}>
            <Ionicons name="logo-android" size={16} color="#3DDC84" />
            <Text style={styles.platformBadgeText}>Android</Text>
          </View>
          <View style={styles.platformBadge}>
            <Ionicons name="globe-outline" size={16} color="#2196F3" />
            <Text style={styles.platformBadgeText}>Web</Text>
          </View>
        </View>
        <Text style={styles.platformSubtext}>
          Single codebase • Native performance • Consistent UX
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#2196F3',
  },
  headerContent: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  subtitle: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  },
  settingsButton: {
    padding: 8,
  },
  summaryCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  },
  summaryContent: {
    alignItems: 'center',
  },
  weightText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
    marginBottom: 8,
  },
  bfText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 4,
  },
  smoothedText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  changeText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  chartCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  chartPlaceholder: {
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  chartText: {
    fontSize: 18,
    color: '#666',
    marginTop: 8,
  },
  chartSubtext: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    fontStyle: 'italic',
  },
  chartData: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    textAlign: 'center',
  },
  actionButtons: {
    margin: 16,
    gap: 12,
  },
  primaryButton: {
    backgroundColor: '#2196F3',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  buttonIcon: {
    marginRight: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  secondaryButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  secondaryButton: {
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
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  secondaryButtonText: {
    color: '#2196F3',
    fontSize: 16,
    fontWeight: 'bold',
  },
  progressCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  progressGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  progressItem: {
    width: '48%',
    alignItems: 'center',
    marginBottom: 16,
  },
  progressValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  progressLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2196F3',
    borderRadius: 4,
  },
  progressText: {
    textAlign: 'center',
    color: '#666',
    fontSize: 14,
  },
  platformCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  platformText: {
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
  },
  platformBadges: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
  },
  platformBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f8ff',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    gap: 4,
  },
  platformBadgeText: {
    color: '#2196F3',
    fontSize: 12,
    fontWeight: '600',
  },
  platformSubtext: {
    color: '#999',
    fontSize: 12,
  },
});
EOF

# Create placeholder screens
for screen in HistoryScreen LogEntryScreen AnalyticsScreen SettingsScreen; do
  cat > "src/screens/${screen}.tsx" << EOF
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

export default function ${screen}({ navigation }: any) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>${screen}</Text>
      <Text style={styles.subtitle}>This screen is ready for implementation</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
});
EOF
done

# Create metro.config.js
cat > metro.config.js << 'EOF'
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

module.exports = config;
EOF

# Create babel.config.js
cat > babel.config.js << 'EOF'
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
  };
};
EOF

# Create tsconfig.json
cat > tsconfig.json << 'EOF'
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true
  }
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# OSX
#
.DS_Store

# Xcode
#
build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata
*.xccheckout
*.moved-aside
DerivedData
*.hmap
*.ipa
*.xcuserstate
project.xcworkspace

# Android/IntelliJ
#
build/
.idea
.gradle
local.properties
*.iml
*.hprof
.cxx/
*.keystore
!debug.keystore

# node.js
#
node_modules/
npm-debug.log
yarn-error.log

# BUCK
buck-out/
\.buckd/
*.keystore
!debug.keystore

# fastlane
#
# It is recommended to not store the screenshots in the git repo. Instead, use fastlane to re-generate the
# screenshots whenever they are needed.
# For more information about the recommended setup visit:
# https://docs.fastlane.tools/best-practices/source-control/

*/fastlane/report.xml
*/fastlane/Preview.html
*/fastlane/screenshots
*/fastlane/test_output

# Bundle artifacts
*.jsbundle

# CocoaPods
/ios/Pods/

# Expo
.expo/
dist/
web-build/

# Temporary files created by Metro to check the health of the file watcher
.metro-health-check*
EOF

print_success "Mobile app created successfully!"
print_status "App location: $MOBILE_APP_DIR"
print_status "Next steps:"
print_status "1. cd $MOBILE_APP_DIR"
print_status "2. npm install"
print_status "3. npx expo start"
print_status "4. Test on Android: npx expo start --android"
print_status "5. Test on iOS: npx expo start --ios"

cd ../..

print_success "🎉 Mobile App Creation Complete!"
print_status "Your Software Factory can now create mobile apps for testing!"

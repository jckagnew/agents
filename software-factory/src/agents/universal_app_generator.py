"""
Universal App Generator Agent
Creates native mobile (iOS/Android) and web versions by default
"""

import os
import json
import shutil
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum
import asyncio

class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"
    ALL = "all"

@dataclass
class AppConfig:
    name: str
    description: str
    bundle_id: str
    version: str
    platforms: List[Platform]
    features: List[str]
    ui_theme: str
    navigation_type: str

class UniversalAppGenerator:
    """Generates universal apps for iOS, Android, and Web"""
    
    def __init__(self):
        self.template_path = "templates/universal-app-template"
        self.output_path = "generated-apps"
        
    async def generate_app(self, config: AppConfig) -> Dict[str, Any]:
        """Generate a universal app with the given configuration"""
        
        print(f"🚀 Generating universal app: {config.name}")
        print(f"📱 Platforms: {[p.value for p in config.platforms]}")
        print(f"✨ Features: {config.features}")
        
        # Create output directory
        app_path = os.path.join(self.output_path, config.name.lower().replace(" ", "-"))
        os.makedirs(app_path, exist_ok=True)
        
        # Copy template
        await self._copy_template(app_path)
        
        # Generate platform-specific configurations
        await self._generate_platform_configs(app_path, config)
        
        # Generate app-specific code
        await self._generate_app_code(app_path, config)
        
        # Generate deployment configurations
        await self._generate_deployment_configs(app_path, config)
        
        # Generate CI/CD pipeline
        await self._generate_cicd_pipeline(app_path, config)
        
        print(f"✅ Universal app generated successfully!")
        print(f"📁 Location: {app_path}")
        
        return {
            "success": True,
            "app_path": app_path,
            "platforms": [p.value for p in config.platforms],
            "features": config.features,
            "next_steps": self._get_next_steps(app_path, config)
        }
    
    async def _copy_template(self, app_path: str):
        """Copy the universal app template"""
        if os.path.exists(self.template_path):
            shutil.copytree(self.template_path, app_path, dirs_exist_ok=True)
        else:
            raise FileNotFoundError(f"Template not found: {self.template_path}")
    
    async def _generate_platform_configs(self, app_path: str, config: AppConfig):
        """Generate platform-specific configuration files"""
        
        # Update package.json
        package_json_path = os.path.join(app_path, "package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
            
            package_data["name"] = config.name.lower().replace(" ", "-")
            package_data["description"] = config.description
            package_data["version"] = config.version
            
            with open(package_json_path, 'w') as f:
                json.dump(package_data, f, indent=2)
        
        # Update expo.json
        expo_json_path = os.path.join(app_path, "expo.json")
        if os.path.exists(expo_json_path):
            with open(expo_json_path, 'r') as f:
                expo_data = json.load(f)
            
            expo_data["expo"]["name"] = config.name
            expo_data["expo"]["slug"] = config.name.lower().replace(" ", "-")
            expo_data["expo"]["version"] = config.version
            expo_data["expo"]["ios"]["bundleIdentifier"] = config.bundle_id
            expo_data["expo"]["android"]["package"] = config.bundle_id
            
            with open(expo_json_path, 'w') as f:
                json.dump(expo_data, f, indent=2)
    
    async def _generate_app_code(self, app_path: str, config: AppConfig):
        """Generate app-specific code based on features"""
        
        # Generate main App.tsx
        app_tsx_content = self._generate_app_tsx(config)
        with open(os.path.join(app_path, "App.tsx"), 'w') as f:
            f.write(app_tsx_content)
        
        # Generate screens based on features
        screens_path = os.path.join(app_path, "src", "screens")
        os.makedirs(screens_path, exist_ok=True)
        
        for feature in config.features:
            screen_content = self._generate_screen_component(feature, config)
            screen_filename = f"{feature.title().replace(' ', '')}Screen.tsx"
            with open(os.path.join(screens_path, screen_filename), 'w') as f:
                f.write(screen_content)
    
    async def _generate_deployment_configs(self, app_path: str, config: AppConfig):
        """Generate deployment configurations for all platforms"""
        
        # Generate Docker configuration for web
        dockerfile_content = self._generate_dockerfile(config)
        with open(os.path.join(app_path, "Dockerfile"), 'w') as f:
            f.write(dockerfile_content)
        
        # Generate docker-compose for local development
        docker_compose_content = self._generate_docker_compose(config)
        with open(os.path.join(app_path, "docker-compose.yml"), 'w') as f:
            f.write(docker_compose_content)
        
        # Generate deployment scripts
        deploy_script_content = self._generate_deploy_script(config)
        with open(os.path.join(app_path, "deploy.sh"), 'w') as f:
            f.write(deploy_script_content)
        os.chmod(os.path.join(app_path, "deploy.sh"), 0o755)
    
    async def _generate_cicd_pipeline(self, app_path: str, config: AppConfig):
        """Generate CI/CD pipeline for automated deployment"""
        
        github_workflows_path = os.path.join(app_path, ".github", "workflows")
        os.makedirs(github_workflows_path, exist_ok=True)
        
        # Generate main CI/CD workflow
        workflow_content = self._generate_github_workflow(config)
        with open(os.path.join(github_workflows_path, "universal-app.yml"), 'w') as f:
            f.write(workflow_content)
    
    def _generate_app_tsx(self, config: AppConfig) -> str:
        """Generate the main App.tsx file"""
        screen_imports = self._generate_screen_imports(config.features)
        tab_types = self._generate_tab_types(config.features)
        tab_icons = self._generate_tab_icons(config.features)
        tab_screens = self._generate_tab_screens(config.features)
        
        return f'''/**
 * {config.name}
 * {config.description}
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
{screen_imports}

// Types
type RootStackParamList = {{
  MainTabs: undefined;
  Modal: undefined;
}};

type TabParamList = {{
{tab_types}
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

{tab_icons}

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
{tab_screens}
    </Tab.Navigator>
  );
}};

export default function App() {{
  return (
    <NavigationContainer>
      <StatusBar style="light" />
      <Stack.Navigator
        initialRouteName="MainTabs"
        screenOptions={{{
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
          component={{{MainTabNavigator}}}
          options={{{{{ headerShown: false }}}}}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
}};
'''
    
    def _generate_screen_imports(self, features: List[str]) -> str:
        """Generate screen imports"""
        imports = []
        for feature in features:
            screen_name = feature.title().replace(' ', '')
            imports.append(f"import {{ {screen_name}Screen }} from './src/screens/{screen_name}Screen';")
        return '\n'.join(imports)
    
    def _generate_tab_types(self, features: List[str]) -> str:
        """Generate tab types"""
        types = []
        for feature in features:
            screen_name = feature.title().replace(' ', '')
            types.append(f"  {screen_name}: undefined;")
        return '\n'.join(types)
    
    def _generate_tab_icons(self, features: List[str]) -> str:
        """Generate tab icons"""
        icons = []
        icon_map = {
            'dashboard': 'home',
            'profile': 'person',
            'settings': 'settings',
            'analytics': 'analytics',
            'notifications': 'notifications',
            'chat': 'chatbubbles',
            'calendar': 'calendar',
            'files': 'folder',
            'search': 'search',
            'help': 'help-circle'
        }
        
        for i, feature in enumerate(features):
            screen_name = feature.title().replace(' ', '')
            icon_name = icon_map.get(feature.lower(), 'help-circle')
            if i == 0:
                icons.append(f"          if (route.name === '{screen_name}') {{")
            else:
                icons.append(f"          }} else if (route.name === '{screen_name}') {{")
            icons.append(f"            iconName = focused ? '{icon_name}' : '{icon_name}-outline';")
        
        icons.append("          } else {")
        icons.append("            iconName = 'help-outline';")
        icons.append("          }")
        
        return '\n'.join(icons)
    
    def _generate_tab_screens(self, features: List[str]) -> str:
        """Generate tab screens"""
        screens = []
        for feature in features:
            screen_name = feature.title().replace(' ', '')
            screens.append(f'''      <Tab.Screen
        name="{screen_name}"
        component={{{screen_name}Screen}}
        options={{
          title: "{feature.title()}",
        }}
      />''')
        return '\n'.join(screens)
    
    def _generate_screen_component(self, feature: str, config: AppConfig) -> str:
        """Generate a screen component"""
        screen_name = feature.title().replace(' ', '')
        return f'''/**
 * {config.name} - {feature.title()} Screen
 * {config.description}
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
        <Text style={{styles.subtitle}}>{config.description}</Text>
      </View>

      <View style={{styles.content}}>
        <Text style={{styles.description}}>
          This is the {feature.lower()} screen for {config.name}.
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
    
    def _generate_dockerfile(self, config: AppConfig) -> str:
        """Generate Dockerfile for web deployment"""
        return f'''# {config.name} - Web Deployment
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build the app
RUN npm run build:web

# Expose port
EXPOSE 3000

# Start the app
CMD ["npm", "run", "start:web"]
'''
    
    def _generate_docker_compose(self, config: AppConfig) -> str:
        """Generate docker-compose.yml for local development"""
        return f'''version: '3.8'

services:
  {config.name.lower().replace(" ", "-")}-web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run dev:web

  {config.name.lower().replace(" ", "-")}-mobile:
    build: .
    ports:
      - "8081:8081"
    environment:
      - EXPO_DEVTOOLS_LISTEN_ADDRESS=0.0.0.0
    volumes:
      - .:/app
      - /app/node_modules
    command: npm run start
'''
    
    def _generate_deploy_script(self, config: AppConfig) -> str:
        """Generate deployment script"""
        return f'''#!/bin/bash
# {config.name} - Deployment Script

set -e

echo "🚀 Deploying {config.name}..."

# Build for all platforms
echo "📱 Building for iOS..."
npm run build:ios

echo "🤖 Building for Android..."
npm run build:android

echo "🌐 Building for Web..."
npm run build:web

# Deploy to platforms
echo "📱 Deploying to App Store..."
npm run deploy:ios

echo "🤖 Deploying to Google Play..."
npm run deploy:android

echo "🌐 Deploying to Web..."
npm run deploy:web

echo "✅ Deployment complete!"
'''
    
    def _generate_github_workflow(self, config: AppConfig) -> str:
        """Generate GitHub Actions workflow"""
        return f'''name: {config.name} CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:all
      
      - name: Run linting
        run: npm run lint
      
      - name: Type check
        run: npm run type-check

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Build iOS
        run: npm run build:ios
      
      - name: Build Android
        run: npm run build:android
      
      - name: Build Web
        run: npm run build:web
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: {config.name.lower().replace(" ", "-")}-builds
          path: |
            build/
            dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: {config.name.lower().replace(" ", "-")}-builds
      
      - name: Deploy to Web
        run: npm run deploy:web
      
      - name: Deploy to App Stores
        run: npm run deploy:mobile
'''
    
    def _get_next_steps(self, app_path: str, config: AppConfig) -> List[str]:
        """Get next steps for the generated app"""
        return [
            f"1. Navigate to the app directory: cd {app_path}",
            "2. Install dependencies: npm install",
            "3. Start development server: npm run start",
            "4. Run on iOS: npm run ios",
            "5. Run on Android: npm run android", 
            "6. Run on Web: npm run web",
            "7. Run tests: npm run test:all",
            "8. Deploy: npm run deploy:all"
        ]

# Example usage
async def main():
    generator = UniversalAppGenerator()
    
    config = AppConfig(
        name="Weight Tracker Pro",
        description="Advanced weight tracking with body composition analysis",
        bundle_id="com.yourcompany.weighttrackerpro",
        version="1.0.0",
        platforms=[Platform.IOS, Platform.ANDROID, Platform.WEB],
        features=["Dashboard", "Analytics", "Settings", "Profile"],
        ui_theme="modern",
        navigation_type="tabs"
    )
    
    result = await generator.generate_app(config)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

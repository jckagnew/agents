import { Tabs } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { Pressable } from 'react-native';
import { useAuth } from '@/contexts/AuthContext';

export default function TabsLayout() {
  const { signOut } = useAuth();

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#8E8E93',
        headerStyle: {
          backgroundColor: '#f8f8f8',
        },
        headerTintColor: '#000',
        headerShadowVisible: false,
      }}
    >
      <Tabs.Screen
        name="customers"
        options={{
          title: 'Customers',
          tabBarIcon: ({ color, size }) => (
            <Feather name="users" size={size} color={color} />
          ),
          headerRight: () => (
            <Pressable onPress={signOut} style={{ marginRight: 16 }}>
              <Feather name="log-out" size={24} color="#007AFF" />
            </Pressable>
          ),
        }}
      />
      <Tabs.Screen
        name="projects"
        options={{
          title: 'Projects',
          tabBarIcon: ({ color, size }) => (
            <Feather name="folder" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="settings"
        options={{
          title: 'Settings',
          tabBarIcon: ({ color, size }) => (
            <Feather name="settings" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}

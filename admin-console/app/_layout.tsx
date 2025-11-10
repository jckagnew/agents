import { useEffect } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import { ActivityIndicator, View } from 'react-native';

function RootLayoutNav() {
  const { isAdmin, loading } = useAuth();
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (loading) return;

    const inAuthGroup = segments[0] === '(tabs)';

    if (!isAdmin && inAuthGroup) {
      // Redirect to login if not admin
      router.replace('/login');
    } else if (isAdmin && !inAuthGroup) {
      // Redirect to app if admin
      router.replace('/(tabs)/customers');
    }
  }, [isAdmin, loading, segments]);

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="login" />
      <Stack.Screen name="(tabs)" />
    </Stack>
  );
}

export default function RootLayout() {
  return (
    <AuthProvider>
      <RootLayoutNav />
    </AuthProvider>
  );
}

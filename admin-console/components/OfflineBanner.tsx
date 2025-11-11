import { View, Text, StyleSheet } from 'react-native';
import { Feather } from '@expo/vector-icons';
import { useNetworkStatus } from '@/hooks/useNetworkStatus';

export function OfflineBanner() {
  const { isOffline } = useNetworkStatus();

  if (!isOffline) {
    return null;
  }

  return (
    <View style={styles.banner}>
      <Feather name="wifi-off" size={16} color="#fff" />
      <Text style={styles.text}>You are offline</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  banner: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
    backgroundColor: '#FF9500',
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  text: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },
});

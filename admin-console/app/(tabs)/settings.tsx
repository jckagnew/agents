import { View, Text, StyleSheet, Pressable, Alert } from 'react-native';
import { Feather } from '@expo/vector-icons';
import { useAuth } from '@/contexts/AuthContext';

export default function SettingsScreen() {
  const { user, adminUser, signOut } = useAuth();

  const handleSignOut = async () => {
    Alert.alert('Sign Out', 'Are you sure you want to sign out?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Sign Out',
        style: 'destructive',
        onPress: async () => {
          await signOut();
        },
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>

        <View style={styles.card}>
          <View style={styles.row}>
            <Feather name="user" size={20} color="#8E8E93" />
            <View style={styles.rowContent}>
              <Text style={styles.label}>Name</Text>
              <Text style={styles.value}>{adminUser?.full_name}</Text>
            </View>
          </View>

          <View style={styles.divider} />

          <View style={styles.row}>
            <Feather name="mail" size={20} color="#8E8E93" />
            <View style={styles.rowContent}>
              <Text style={styles.label}>Email</Text>
              <Text style={styles.value}>{adminUser?.email}</Text>
            </View>
          </View>

          <View style={styles.divider} />

          <View style={styles.row}>
            <Feather name="shield" size={20} color="#8E8E93" />
            <View style={styles.rowContent}>
              <Text style={styles.label}>Role</Text>
              <Text style={styles.value}>
                {adminUser?.role.replace('_', ' ').toUpperCase()}
              </Text>
            </View>
          </View>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>App Info</Text>

        <View style={styles.card}>
          <View style={styles.row}>
            <Feather name="info" size={20} color="#8E8E93" />
            <View style={styles.rowContent}>
              <Text style={styles.label}>Version</Text>
              <Text style={styles.value}>1.0.0</Text>
            </View>
          </View>

          <View style={styles.divider} />

          <View style={styles.row}>
            <Feather name="code" size={20} color="#8E8E93" />
            <View style={styles.rowContent}>
              <Text style={styles.label}>Tech Stack</Text>
              <Text style={styles.value}>Expo + React Native</Text>
            </View>
          </View>
        </View>
      </View>

      <Pressable style={styles.signOutButton} onPress={handleSignOut}>
        <Feather name="log-out" size={20} color="#FF3B30" />
        <Text style={styles.signOutText}>Sign Out</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  section: {
    marginTop: 24,
    paddingHorizontal: 16,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#8E8E93',
    textTransform: 'uppercase',
    marginBottom: 8,
    paddingHorizontal: 4,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
    overflow: 'hidden',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    gap: 12,
  },
  rowContent: {
    flex: 1,
  },
  label: {
    fontSize: 14,
    color: '#8E8E93',
    marginBottom: 2,
  },
  value: {
    fontSize: 16,
    color: '#1a1a1a',
    fontWeight: '500',
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E5EA',
    marginLeft: 48,
  },
  signOutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    marginHorizontal: 16,
    marginTop: 32,
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#FF3B30',
    gap: 8,
  },
  signOutText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FF3B30',
  },
});

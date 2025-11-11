import { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  ActivityIndicator,
  Pressable,
  TextInput,
  Alert,
} from 'react-native';
import { useLocalSearchParams, useRouter, Stack } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { supabase } from '@/lib/supabase';

interface Customer {
  id: string;
  full_name: string;
  email: string;
  phone: string | null;
  company_name: string | null;
  subscription_status: string;
  subscription_tier: string | null;
  mrr: number;
  status: string;
  tags: string[] | null;
  source: string | null;
  created_at: string;
}

export default function CustomerDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [saving, setSaving] = useState(false);

  // Form state
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [subscriptionStatus, setSubscriptionStatus] = useState('none');
  const [subscriptionTier, setSubscriptionTier] = useState('');
  const [customerStatus, setCustomerStatus] = useState('active');
  const [source, setSource] = useState('');

  useEffect(() => {
    if (id) {
      fetchCustomer();
    }
  }, [id]);

  const fetchCustomer = async () => {
    try {
      const { data, error } = await supabase
        .from('customers')
        .select('*')
        .eq('id', id)
        .single();

      if (error) {
        console.error('Error fetching customer:', error);
        Alert.alert('Error', 'Failed to load customer');
        router.back();
      } else {
        setCustomer(data);
        // Initialize form state
        setFullName(data.full_name);
        setEmail(data.email);
        setPhone(data.phone || '');
        setCompanyName(data.company_name || '');
        setSubscriptionStatus(data.subscription_status);
        setSubscriptionTier(data.subscription_tier || '');
        setCustomerStatus(data.status);
        setSource(data.source || '');
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    // Validation
    if (!fullName.trim()) {
      Alert.alert('Validation Error', 'Full name is required');
      return;
    }
    if (!email.trim() || !email.includes('@')) {
      Alert.alert('Validation Error', 'Valid email is required');
      return;
    }

    setSaving(true);
    try {
      const { data, error } = await supabase
        .from('customers')
        .update({
          full_name: fullName.trim(),
          email: email.trim().toLowerCase(),
          phone: phone.trim() || null,
          company_name: companyName.trim() || null,
          subscription_status: subscriptionStatus,
          subscription_tier: subscriptionTier || null,
          status: customerStatus,
          source: source || null,
        })
        .eq('id', id)
        .select()
        .single();

      if (error) {
        console.error('Error updating customer:', error);
        Alert.alert('Error', error.message);
      } else {
        setCustomer(data);
        setEditing(false);
        Alert.alert('Success', 'Customer updated successfully');
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'An unexpected error occurred');
    } finally {
      setSaving(false);
    }
  };

  const handleCancel = () => {
    if (!customer) return;

    // Reset form to original values
    setFullName(customer.full_name);
    setEmail(customer.email);
    setPhone(customer.phone || '');
    setCompanyName(customer.company_name || '');
    setSubscriptionStatus(customer.subscription_status);
    setSubscriptionTier(customer.subscription_tier || '');
    setCustomerStatus(customer.status);
    setSource(customer.source || '');
    setEditing(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return '#34C759';
      case 'trial':
        return '#FF9500';
      case 'past_due':
        return '#FF3B30';
      case 'cancelled':
        return '#8E8E93';
      default:
        return '#8E8E93';
    }
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  if (!customer) {
    return (
      <View style={styles.centerContainer}>
        <Text>Customer not found</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: editing ? 'Edit Customer' : customer.full_name,
          headerShown: true,
          headerRight: () =>
            editing ? null : (
              <Pressable onPress={() => setEditing(true)}>
                <Feather name="edit-2" size={20} color="#007AFF" />
              </Pressable>
            ),
        }}
      />
      <ScrollView style={styles.container}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Contact Information</Text>
          <View style={styles.card}>
            <View style={styles.field}>
              <Text style={styles.label}>Full Name *</Text>
              {editing ? (
                <TextInput
                  style={styles.input}
                  value={fullName}
                  onChangeText={setFullName}
                  placeholder="John Doe"
                />
              ) : (
                <Text style={styles.value}>{customer.full_name}</Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>Email *</Text>
              {editing ? (
                <TextInput
                  style={styles.input}
                  value={email}
                  onChangeText={setEmail}
                  placeholder="john@example.com"
                  keyboardType="email-address"
                  autoCapitalize="none"
                />
              ) : (
                <Text style={[styles.value, styles.emailText]}>
                  {customer.email}
                </Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>Phone</Text>
              {editing ? (
                <TextInput
                  style={styles.input}
                  value={phone}
                  onChangeText={setPhone}
                  placeholder="+1-555-0123"
                  keyboardType="phone-pad"
                />
              ) : (
                <Text style={styles.value}>{customer.phone || '—'}</Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>Company</Text>
              {editing ? (
                <TextInput
                  style={styles.input}
                  value={companyName}
                  onChangeText={setCompanyName}
                  placeholder="Acme Corp"
                />
              ) : (
                <Text style={styles.value}>{customer.company_name || '—'}</Text>
              )}
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Subscription</Text>
          <View style={styles.card}>
            <View style={styles.field}>
              <Text style={styles.label}>Status</Text>
              {editing ? (
                <View style={styles.pickerContainer}>
                  {['none', 'trial', 'active', 'cancelled', 'past_due'].map(
                    (status) => (
                      <Pressable
                        key={status}
                        style={[
                          styles.pickerOption,
                          subscriptionStatus === status &&
                            styles.pickerOptionSelected,
                        ]}
                        onPress={() => setSubscriptionStatus(status)}
                      >
                        <Text
                          style={[
                            styles.pickerOptionText,
                            subscriptionStatus === status &&
                              styles.pickerOptionTextSelected,
                          ]}
                        >
                          {status.replace('_', ' ').toUpperCase()}
                        </Text>
                      </Pressable>
                    )
                  )}
                </View>
              ) : (
                <View style={styles.row}>
                  <View
                    style={[
                      styles.statusBadge,
                      { backgroundColor: getStatusColor(customer.subscription_status) },
                    ]}
                  >
                    <Text style={styles.statusText}>
                      {customer.subscription_status.replace('_', ' ').toUpperCase()}
                    </Text>
                  </View>
                </View>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>Tier</Text>
              {editing ? (
                <TextInput
                  style={styles.input}
                  value={subscriptionTier}
                  onChangeText={setSubscriptionTier}
                  placeholder="express, concierge, etc."
                />
              ) : (
                <Text style={styles.value}>
                  {customer.subscription_tier || '—'}
                </Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>MRR</Text>
              <Text style={styles.value}>${customer.mrr.toFixed(2)}/mo</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Account</Text>
          <View style={styles.card}>
            <View style={styles.field}>
              <Text style={styles.label}>Status</Text>
              {editing ? (
                <View style={styles.pickerContainer}>
                  {['active', 'paused', 'cancelled'].map((status) => (
                    <Pressable
                      key={status}
                      style={[
                        styles.pickerOption,
                        customerStatus === status && styles.pickerOptionSelected,
                      ]}
                      onPress={() => setCustomerStatus(status)}
                    >
                      <Text
                        style={[
                          styles.pickerOptionText,
                          customerStatus === status &&
                            styles.pickerOptionTextSelected,
                        ]}
                      >
                        {status.toUpperCase()}
                      </Text>
                    </Pressable>
                  ))}
                </View>
              ) : (
                <Text style={styles.value}>
                  {customer.status.toUpperCase()}
                </Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>Source</Text>
              {editing ? (
                <TextInput
                  style={styles.input}
                  value={source}
                  onChangeText={setSource}
                  placeholder="website, referral, agency"
                />
              ) : (
                <Text style={styles.value}>{customer.source || '—'}</Text>
              )}
            </View>

            <View style={styles.divider} />

            <View style={styles.field}>
              <Text style={styles.label}>Created</Text>
              <Text style={styles.value}>
                {new Date(customer.created_at).toLocaleDateString()}
              </Text>
            </View>
          </View>
        </View>

        {!editing && (
          <View style={styles.section}>
            <Pressable
              style={styles.invoicesButton}
              onPress={() => router.push(`/customer/${id}/invoices`)}
            >
              <Feather name="file-text" size={20} color="#007AFF" />
              <Text style={styles.invoicesButtonText}>View Invoices</Text>
              <Feather name="chevron-right" size={20} color="#8E8E93" />
            </Pressable>
          </View>
        )}

        {editing && (
          <View style={styles.buttonContainer}>
            <Pressable
              style={[styles.button, styles.cancelButton]}
              onPress={handleCancel}
              disabled={saving}
            >
              <Text style={styles.cancelButtonText}>Cancel</Text>
            </Pressable>
            <Pressable
              style={[styles.button, styles.saveButton, saving && styles.buttonDisabled]}
              onPress={handleSave}
              disabled={saving}
            >
              {saving ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.saveButtonText}>Save Changes</Text>
              )}
            </Pressable>
          </View>
        )}
      </ScrollView>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
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
  field: {
    padding: 16,
  },
  label: {
    fontSize: 14,
    color: '#8E8E93',
    marginBottom: 4,
  },
  value: {
    fontSize: 16,
    color: '#1a1a1a',
    fontWeight: '500',
  },
  emailText: {
    color: '#007AFF',
  },
  input: {
    fontSize: 16,
    color: '#1a1a1a',
    fontWeight: '500',
    borderBottomWidth: 1,
    borderBottomColor: '#007AFF',
    paddingVertical: 4,
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E5EA',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
    color: '#fff',
  },
  pickerContainer: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginTop: 8,
  },
  pickerOption: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 6,
    backgroundColor: '#f5f5f5',
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  pickerOptionSelected: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  pickerOptionText: {
    fontSize: 12,
    color: '#1a1a1a',
  },
  pickerOptionTextSelected: {
    color: '#fff',
    fontWeight: '600',
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: 12,
    padding: 16,
    paddingBottom: 32,
  },
  button: {
    flex: 1,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  cancelButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
  },
  saveButton: {
    backgroundColor: '#007AFF',
  },
  saveButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#fff',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  invoicesButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  invoicesButtonText: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
    marginLeft: 12,
  },
});

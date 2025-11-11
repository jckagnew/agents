import { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TextInput,
  Pressable,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  Modal,
  FlatList,
} from 'react-native';
import { useRouter, Stack } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { supabase } from '@/lib/supabase';

interface Customer {
  id: string;
  full_name: string;
  email: string;
  company_name: string | null;
}

export default function NewProjectScreen() {
  const router = useRouter();
  const [saving, setSaving] = useState(false);
  const [showCustomerPicker, setShowCustomerPicker] = useState(false);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loadingCustomers, setLoadingCustomers] = useState(false);

  // Form state
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [customerId, setCustomerId] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);
  const [productType, setProductType] = useState<string>('express');
  const [pricingTier, setPricingTier] = useState('');
  const [estimatedDeliveryDate, setEstimatedDeliveryDate] = useState('');

  // Validation errors
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    setLoadingCustomers(true);
    try {
      const { data, error } = await supabase
        .from('customers')
        .select('id, full_name, email, company_name')
        .eq('status', 'active')
        .order('full_name');

      if (error) {
        console.error('Error fetching customers:', error);
      } else {
        setCustomers(data || []);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoadingCustomers(false);
    }
  };

  const selectCustomer = (customer: Customer) => {
    setSelectedCustomer(customer);
    setCustomerId(customer.id);
    setShowCustomerPicker(false);
    if (errors.customerId) {
      setErrors({ ...errors, customerId: '' });
    }
  };

  const validateForm = () => {
    const newErrors: { [key: string]: string } = {};

    if (!name.trim()) {
      newErrors.name = 'Project name is required';
    }

    if (!customerId) {
      newErrors.customerId = 'Customer is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSave = async () => {
    if (!validateForm()) {
      Alert.alert('Validation Error', 'Please fix the errors and try again');
      return;
    }

    setSaving(true);
    try {
      const { data, error } = await supabase
        .from('projects')
        .insert({
          name: name.trim(),
          description: description.trim() || null,
          customer_id: customerId,
          product_type: productType,
          pricing_tier: pricingTier.trim() || null,
          status: 'INTAKE',
          estimated_delivery_date: estimatedDeliveryDate || null,
        })
        .select()
        .single();

      if (error) {
        console.error('Error creating project:', error);
        Alert.alert('Error', error.message);
      } else {
        Alert.alert('Success', 'Project created successfully', [
          {
            text: 'OK',
            onPress: () => router.replace(`/project/${data.id}`),
          },
        ]);
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'An unexpected error occurred');
    } finally {
      setSaving(false);
    }
  };

  return (
    <>
      <Stack.Screen
        options={{
          title: 'New Project',
          headerShown: true,
          headerLeft: () => (
            <Pressable onPress={() => router.back()} style={{ marginRight: 16 }}>
              <Feather name="x" size={24} color="#000" />
            </Pressable>
          ),
        }}
      />
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.container}
      >
        <ScrollView style={styles.content}>
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Project Information</Text>
            <View style={styles.card}>
              <View style={styles.field}>
                <Text style={styles.label}>
                  Project Name <Text style={styles.required}>*</Text>
                </Text>
                <TextInput
                  style={[styles.input, errors.name && styles.inputError]}
                  value={name}
                  onChangeText={(text) => {
                    setName(text);
                    if (errors.name) {
                      setErrors({ ...errors, name: '' });
                    }
                  }}
                  placeholder="E-commerce Platform"
                  autoFocus
                />
                {errors.name && (
                  <Text style={styles.errorText}>{errors.name}</Text>
                )}
              </View>

              <View style={styles.divider} />

              <View style={styles.field}>
                <Text style={styles.label}>Description</Text>
                <TextInput
                  style={[styles.input, styles.textArea]}
                  value={description}
                  onChangeText={setDescription}
                  placeholder="Project description..."
                  multiline
                  numberOfLines={4}
                  textAlignVertical="top"
                />
              </View>

              <View style={styles.divider} />

              <View style={styles.field}>
                <Text style={styles.label}>
                  Customer <Text style={styles.required}>*</Text>
                </Text>
                <Pressable
                  style={[
                    styles.pickerButton,
                    errors.customerId && styles.inputError,
                  ]}
                  onPress={() => setShowCustomerPicker(true)}
                >
                  {selectedCustomer ? (
                    <View>
                      <Text style={styles.pickerButtonText}>
                        {selectedCustomer.full_name}
                      </Text>
                      <Text style={styles.pickerButtonSubtext}>
                        {selectedCustomer.email}
                      </Text>
                    </View>
                  ) : (
                    <Text style={styles.pickerButtonPlaceholder}>
                      Select customer
                    </Text>
                  )}
                  <Feather name="chevron-down" size={20} color="#8E8E93" />
                </Pressable>
                {errors.customerId && (
                  <Text style={styles.errorText}>{errors.customerId}</Text>
                )}
              </View>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Product Details</Text>
            <View style={styles.card}>
              <View style={styles.field}>
                <Text style={styles.label}>Product Type</Text>
                <View style={styles.productTypeOptions}>
                  {[
                    { value: 'express', icon: 'zap', label: 'Express' },
                    { value: 'concierge', icon: 'briefcase', label: 'Concierge' },
                    {
                      value: 'website_refresh',
                      icon: 'refresh-cw',
                      label: 'Website Refresh',
                    },
                  ].map((type) => (
                    <Pressable
                      key={type.value}
                      style={[
                        styles.productTypeOption,
                        productType === type.value &&
                          styles.productTypeOptionSelected,
                      ]}
                      onPress={() => setProductType(type.value)}
                    >
                      <Feather
                        name={type.icon as any}
                        size={20}
                        color={productType === type.value ? '#fff' : '#007AFF'}
                      />
                      <Text
                        style={[
                          styles.productTypeText,
                          productType === type.value &&
                            styles.productTypeTextSelected,
                        ]}
                      >
                        {type.label}
                      </Text>
                    </Pressable>
                  ))}
                </View>
              </View>

              <View style={styles.divider} />

              <View style={styles.field}>
                <Text style={styles.label}>Pricing Tier</Text>
                <TextInput
                  style={styles.input}
                  value={pricingTier}
                  onChangeText={setPricingTier}
                  placeholder="basic, standard, premium"
                />
                <Text style={styles.hint}>Optional</Text>
              </View>

              <View style={styles.divider} />

              <View style={styles.field}>
                <Text style={styles.label}>Estimated Delivery Date</Text>
                <TextInput
                  style={styles.input}
                  value={estimatedDeliveryDate}
                  onChangeText={setEstimatedDeliveryDate}
                  placeholder="YYYY-MM-DD"
                />
                <Text style={styles.hint}>
                  Format: YYYY-MM-DD (e.g., 2025-12-31)
                </Text>
              </View>
            </View>
          </View>

          <View style={styles.infoBox}>
            <Feather name="info" size={16} color="#007AFF" />
            <Text style={styles.infoText}>
              Project status will be set to "INTAKE" by default. You can update it
              in the project details once created.
            </Text>
          </View>
        </ScrollView>

        <View style={styles.footer}>
          <Pressable
            style={[styles.button, styles.cancelButton]}
            onPress={() => router.back()}
            disabled={saving}
          >
            <Text style={styles.cancelButtonText}>Cancel</Text>
          </Pressable>
          <Pressable
            style={[
              styles.button,
              styles.saveButton,
              saving && styles.buttonDisabled,
            ]}
            onPress={handleSave}
            disabled={saving}
          >
            {saving ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text style={styles.saveButtonText}>Create Project</Text>
            )}
          </Pressable>
        </View>
      </KeyboardAvoidingView>

      {/* Customer Picker Modal */}
      <Modal
        visible={showCustomerPicker}
        animationType="slide"
        presentationStyle="pageSheet"
        onRequestClose={() => setShowCustomerPicker(false)}
      >
        <View style={styles.modalContainer}>
          <View style={styles.modalHeader}>
            <Text style={styles.modalTitle}>Select Customer</Text>
            <Pressable onPress={() => setShowCustomerPicker(false)}>
              <Feather name="x" size={24} color="#000" />
            </Pressable>
          </View>
          {loadingCustomers ? (
            <View style={styles.centerContainer}>
              <ActivityIndicator size="large" color="#007AFF" />
            </View>
          ) : (
            <FlatList
              data={customers}
              keyExtractor={(item) => item.id}
              renderItem={({ item }) => (
                <Pressable
                  style={styles.customerItem}
                  onPress={() => selectCustomer(item)}
                >
                  <View style={styles.customerItemContent}>
                    <Text style={styles.customerItemName}>{item.full_name}</Text>
                    <Text style={styles.customerItemEmail}>{item.email}</Text>
                    {item.company_name && (
                      <Text style={styles.customerItemCompany}>
                        {item.company_name}
                      </Text>
                    )}
                  </View>
                  {customerId === item.id && (
                    <Feather name="check" size={20} color="#007AFF" />
                  )}
                </Pressable>
              )}
              ListEmptyComponent={
                <View style={styles.emptyContainer}>
                  <Feather name="users" size={48} color="#8E8E93" />
                  <Text style={styles.emptyText}>No customers found</Text>
                </View>
              }
            />
          )}
        </View>
      </Modal>
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  content: {
    flex: 1,
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
    color: '#1a1a1a',
    fontWeight: '500',
    marginBottom: 8,
  },
  required: {
    color: '#FF3B30',
  },
  input: {
    fontSize: 16,
    color: '#1a1a1a',
    borderWidth: 1,
    borderColor: '#E5E5EA',
    borderRadius: 8,
    padding: 12,
    backgroundColor: '#fff',
  },
  inputError: {
    borderColor: '#FF3B30',
  },
  textArea: {
    minHeight: 100,
    textAlignVertical: 'top',
  },
  errorText: {
    fontSize: 12,
    color: '#FF3B30',
    marginTop: 4,
  },
  hint: {
    fontSize: 12,
    color: '#8E8E93',
    marginTop: 4,
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E5EA',
  },
  pickerButton: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#E5E5EA',
    borderRadius: 8,
    padding: 12,
    backgroundColor: '#fff',
  },
  pickerButtonText: {
    fontSize: 16,
    color: '#1a1a1a',
    fontWeight: '500',
  },
  pickerButtonSubtext: {
    fontSize: 13,
    color: '#8E8E93',
    marginTop: 2,
  },
  pickerButtonPlaceholder: {
    fontSize: 16,
    color: '#8E8E93',
  },
  productTypeOptions: {
    gap: 12,
  },
  productTypeOption: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
    padding: 16,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#007AFF',
    backgroundColor: '#fff',
  },
  productTypeOptionSelected: {
    backgroundColor: '#007AFF',
  },
  productTypeText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#007AFF',
  },
  productTypeTextSelected: {
    color: '#fff',
  },
  infoBox: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: 8,
    backgroundColor: '#E3F2FD',
    padding: 12,
    borderRadius: 8,
    margin: 16,
  },
  infoText: {
    flex: 1,
    fontSize: 13,
    color: '#007AFF',
    lineHeight: 18,
  },
  footer: {
    flexDirection: 'row',
    gap: 12,
    padding: 16,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#E5E5EA',
  },
  button: {
    flex: 1,
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  cancelButton: {
    backgroundColor: '#f5f5f5',
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
  modalContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  customerItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  customerItemContent: {
    flex: 1,
  },
  customerItemName: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1a1a1a',
    marginBottom: 2,
  },
  customerItemEmail: {
    fontSize: 14,
    color: '#007AFF',
    marginBottom: 2,
  },
  customerItemCompany: {
    fontSize: 13,
    color: '#8E8E93',
  },
  emptyContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 16,
    color: '#8E8E93',
    marginTop: 12,
  },
});

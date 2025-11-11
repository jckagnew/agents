import { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Pressable,
  TextInput,
  RefreshControl,
} from 'react-native';
import { Feather } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { supabase } from '@/lib/supabase';
import { ListSkeleton } from '@/components/SkeletonLoader';
import { useErrorHandler, getErrorMessage } from '@/hooks/useErrorHandler';

interface Customer {
  id: string;
  full_name: string;
  email: string;
  company_name: string | null;
  subscription_status: string;
  subscription_tier: string | null;
  mrr: number;
  status: string;
  created_at: string;
  projects?: { count: number }[];
}

export default function CustomersScreen() {
  const router = useRouter();
  const { handleError } = useErrorHandler();
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState('');

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    try {
      const { data, error } = await supabase
        .from('customers')
        .select('*, projects(count)')
        .order('created_at', { ascending: false });

      if (error) {
        handleError(error, { customMessage: getErrorMessage(error) });
      } else {
        setCustomers(data || []);
      }
    } catch (error) {
      handleError(error, { customMessage: 'Failed to load customers' });
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchCustomers();
  };

  const filteredCustomers = customers.filter(
    (customer) =>
      customer.full_name.toLowerCase().includes(search.toLowerCase()) ||
      customer.email.toLowerCase().includes(search.toLowerCase()) ||
      (customer.company_name &&
        customer.company_name.toLowerCase().includes(search.toLowerCase()))
  );

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

  const renderCustomer = ({ item }: { item: Customer }) => {
    const projectCount = item.projects?.[0]?.count || 0;

    return (
      <Pressable
        style={styles.card}
        onPress={() => router.push(`/customer/${item.id}`)}
      >
        <View style={styles.cardHeader}>
          <View style={styles.customerInfo}>
            <Text style={styles.customerName}>{item.full_name}</Text>
            {item.company_name && (
              <Text style={styles.companyName}>{item.company_name}</Text>
            )}
          </View>
          <View
            style={[
              styles.statusBadge,
              { backgroundColor: getStatusColor(item.subscription_status) },
            ]}
          >
            <Text style={styles.statusText}>
              {item.subscription_status.replace('_', ' ').toUpperCase()}
            </Text>
          </View>
        </View>

        <Text style={styles.email}>{item.email}</Text>

        <View style={styles.cardFooter}>
          <View style={styles.stat}>
            <Feather name="folder" size={14} color="#8E8E93" />
            <Text style={styles.statText}>
              {projectCount} {projectCount === 1 ? 'project' : 'projects'}
            </Text>
          </View>
          {item.mrr > 0 && (
            <View style={styles.stat}>
              <Feather name="dollar-sign" size={14} color="#8E8E93" />
              <Text style={styles.statText}>${item.mrr.toFixed(0)}/mo</Text>
            </View>
          )}
          {item.subscription_tier && (
            <View style={styles.stat}>
              <Feather name="tag" size={14} color="#8E8E93" />
              <Text style={styles.statText}>{item.subscription_tier}</Text>
            </View>
          )}
        </View>
      </Pressable>
    );
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <View style={styles.searchContainer}>
          <Feather
            name="search"
            size={20}
            color="#8E8E93"
            style={styles.searchIcon}
          />
          <TextInput
            style={styles.searchInput}
            placeholder="Search customers..."
            editable={false}
          />
        </View>
        <ListSkeleton count={5} type="customer" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.searchContainer}>
        <Feather
          name="search"
          size={20}
          color="#8E8E93"
          style={styles.searchIcon}
        />
        <TextInput
          style={styles.searchInput}
          placeholder="Search customers..."
          value={search}
          onChangeText={setSearch}
        />
      </View>

      <FlatList
        data={filteredCustomers}
        renderItem={renderCustomer}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Feather name="users" size={48} color="#8E8E93" />
            <Text style={styles.emptyText}>No customers found</Text>
          </View>
        }
      />

      <Pressable
        style={styles.fab}
        onPress={() => router.push('/customer/new')}
      >
        <Feather name="plus" size={24} color="#fff" />
      </Pressable>
    </View>
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
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    margin: 16,
    borderRadius: 12,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    padding: 12,
    fontSize: 16,
  },
  listContent: {
    paddingHorizontal: 16,
    paddingBottom: 80,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 8,
  },
  customerInfo: {
    flex: 1,
  },
  customerName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  companyName: {
    fontSize: 14,
    color: '#8E8E93',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  statusText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#fff',
  },
  email: {
    fontSize: 14,
    color: '#007AFF',
    marginBottom: 12,
  },
  cardFooter: {
    flexDirection: 'row',
    gap: 16,
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  statText: {
    fontSize: 12,
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
  fab: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#007AFF',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
    elevation: 8,
  },
});

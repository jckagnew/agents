import { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { useLocalSearchParams, Stack } from 'expo-router';
import { Feather } from '@expo/vector-icons';
import { supabase } from '@/lib/supabase';

interface Invoice {
  id: string;
  amount: number;
  currency: string;
  status: string;
  product_type: string | null;
  due_date: string | null;
  paid_at: string | null;
  created_at: string;
  line_items: any[];
}

export default function CustomerInvoicesScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    if (id) {
      fetchInvoices();
    }
  }, [id]);

  const fetchInvoices = async () => {
    try {
      const { data, error } = await supabase
        .from('invoices')
        .select('*')
        .eq('customer_id', id)
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching invoices:', error);
      } else {
        setInvoices(data || []);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchInvoices();
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'paid':
        return '#34C759';
      case 'sent':
        return '#007AFF';
      case 'draft':
        return '#8E8E93';
      case 'failed':
        return '#FF3B30';
      case 'refunded':
        return '#FF9500';
      default:
        return '#8E8E93';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'paid':
        return 'check-circle';
      case 'sent':
        return 'send';
      case 'draft':
        return 'file-text';
      case 'failed':
        return 'x-circle';
      case 'refunded':
        return 'rotate-ccw';
      default:
        return 'file';
    }
  };

  const renderInvoice = ({ item }: { item: Invoice }) => (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <View style={styles.invoiceInfo}>
          <View style={styles.amountRow}>
            <Text style={styles.amount}>
              ${item.amount.toFixed(2)} {item.currency}
            </Text>
            <View
              style={[
                styles.statusBadge,
                { backgroundColor: getStatusColor(item.status) },
              ]}
            >
              <Feather
                name={getStatusIcon(item.status) as any}
                size={10}
                color="#fff"
              />
              <Text style={styles.statusText}>
                {item.status.toUpperCase()}
              </Text>
            </View>
          </View>
          {item.product_type && (
            <Text style={styles.productType}>
              {item.product_type.replace('_', ' ')}
            </Text>
          )}
        </View>
      </View>

      {item.line_items && item.line_items.length > 0 && (
        <View style={styles.lineItems}>
          {item.line_items.map((lineItem: any, index: number) => (
            <View key={index} style={styles.lineItem}>
              <Text style={styles.lineItemDescription}>
                {lineItem.description}
              </Text>
              <Text style={styles.lineItemAmount}>
                ${lineItem.amount?.toFixed(2)}
              </Text>
            </View>
          ))}
        </View>
      )}

      <View style={styles.cardFooter}>
        <View style={styles.stat}>
          <Feather name="calendar" size={14} color="#8E8E93" />
          <Text style={styles.statText}>
            Created: {new Date(item.created_at).toLocaleDateString()}
          </Text>
        </View>
        {item.due_date && (
          <View style={styles.stat}>
            <Feather name="clock" size={14} color="#8E8E93" />
            <Text style={styles.statText}>
              Due: {new Date(item.due_date).toLocaleDateString()}
            </Text>
          </View>
        )}
        {item.paid_at && (
          <View style={styles.stat}>
            <Feather name="check" size={14} color="#34C759" />
            <Text style={styles.statText}>
              Paid: {new Date(item.paid_at).toLocaleDateString()}
            </Text>
          </View>
        )}
      </View>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  const totalAmount = invoices.reduce((sum, inv) => sum + inv.amount, 0);
  const paidAmount = invoices
    .filter((inv) => inv.status === 'paid')
    .reduce((sum, inv) => sum + inv.amount, 0);

  return (
    <>
      <Stack.Screen
        options={{
          title: 'Invoices',
          headerShown: true,
        }}
      />
      <View style={styles.container}>
        {invoices.length > 0 && (
          <View style={styles.summary}>
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Total</Text>
              <Text style={styles.summaryValue}>${totalAmount.toFixed(2)}</Text>
            </View>
            <View style={styles.summaryDivider} />
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Paid</Text>
              <Text style={[styles.summaryValue, { color: '#34C759' }]}>
                ${paidAmount.toFixed(2)}
              </Text>
            </View>
            <View style={styles.summaryDivider} />
            <View style={styles.summaryItem}>
              <Text style={styles.summaryLabel}>Outstanding</Text>
              <Text style={[styles.summaryValue, { color: '#FF9500' }]}>
                ${(totalAmount - paidAmount).toFixed(2)}
              </Text>
            </View>
          </View>
        )}

        <FlatList
          data={invoices}
          renderItem={renderInvoice}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Feather name="file-text" size={48} color="#8E8E93" />
              <Text style={styles.emptyText}>No invoices yet</Text>
            </View>
          }
        />
      </View>
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
  summary: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  summaryItem: {
    flex: 1,
    alignItems: 'center',
  },
  summaryLabel: {
    fontSize: 12,
    color: '#8E8E93',
    marginBottom: 4,
  },
  summaryValue: {
    fontSize: 18,
    fontWeight: '700',
    color: '#1a1a1a',
  },
  summaryDivider: {
    width: 1,
    backgroundColor: '#E5E5EA',
    marginHorizontal: 8,
  },
  listContent: {
    paddingHorizontal: 16,
    paddingVertical: 16,
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
    marginBottom: 12,
  },
  invoiceInfo: {
    gap: 6,
  },
  amountRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  amount: {
    fontSize: 22,
    fontWeight: '700',
    color: '#1a1a1a',
  },
  statusBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  statusText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#fff',
  },
  productType: {
    fontSize: 14,
    color: '#8E8E93',
    textTransform: 'capitalize',
  },
  lineItems: {
    gap: 8,
    marginBottom: 12,
    paddingTop: 12,
    borderTopWidth: 1,
    borderTopColor: '#E5E5EA',
  },
  lineItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  lineItemDescription: {
    flex: 1,
    fontSize: 14,
    color: '#1a1a1a',
  },
  lineItemAmount: {
    fontSize: 14,
    fontWeight: '600',
    color: '#1a1a1a',
  },
  cardFooter: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
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
});

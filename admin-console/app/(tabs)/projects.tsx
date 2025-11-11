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

interface Project {
  id: string;
  name: string;
  description: string | null;
  status: string;
  product_type: string;
  visual_qa_score: number | null;
  estimated_delivery_date: string | null;
  created_at: string;
  customer: {
    id: string;
    full_name: string;
    company_name: string | null;
  };
}

export default function ProjectsScreen() {
  const router = useRouter();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState<string>('all');

  useEffect(() => {
    fetchProjects();
  }, [filter]);

  const fetchProjects = async () => {
    try {
      let query = supabase
        .from('projects')
        .select(`
          *,
          customer:customers(id, full_name, company_name)
        `)
        .order('created_at', { ascending: false });

      if (filter !== 'all') {
        query = query.eq('status', filter);
      }

      const { data, error } = await query;

      if (error) {
        console.error('Error fetching projects:', error);
      } else {
        setProjects(data || []);
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
    fetchProjects();
  };

  const filteredProjects = projects.filter((project) =>
    project.name.toLowerCase().includes(search.toLowerCase())
  );

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETE':
        return '#34C759';
      case 'QA':
        return '#32ADE6';
      case 'DEV':
        return '#007AFF';
      case 'DESIGN':
        return '#AF52DE';
      case 'INTAKE':
        return '#FF9500';
      default:
        return '#8E8E93';
    }
  };

  const getProductTypeIcon = (productType: string) => {
    switch (productType) {
      case 'express':
        return 'zap';
      case 'concierge':
        return 'briefcase';
      case 'website_refresh':
        return 'refresh-cw';
      default:
        return 'folder';
    }
  };

  const renderProject = ({ item }: { item: Project }) => (
    <Pressable
      style={styles.card}
      onPress={() => router.push(`/project/${item.id}`)}
    >
      <View style={styles.cardHeader}>
        <View style={styles.projectInfo}>
          <View style={styles.nameRow}>
            <Feather
              name={getProductTypeIcon(item.product_type) as any}
              size={16}
              color="#8E8E93"
            />
            <Text style={styles.projectName}>{item.name}</Text>
          </View>
          <Text style={styles.customerName}>
            {item.customer.full_name}
            {item.customer.company_name && ` • ${item.customer.company_name}`}
          </Text>
        </View>
        <View
          style={[
            styles.statusBadge,
            { backgroundColor: getStatusColor(item.status) },
          ]}
        >
          <Text style={styles.statusText}>{item.status}</Text>
        </View>
      </View>

      {item.description && (
        <Text style={styles.description} numberOfLines={2}>
          {item.description}
        </Text>
      )}

      <View style={styles.cardFooter}>
        <View style={styles.stat}>
          <Feather name="package" size={14} color="#8E8E93" />
          <Text style={styles.statText}>
            {item.product_type.replace('_', ' ')}
          </Text>
        </View>
        {item.visual_qa_score && (
          <View style={styles.stat}>
            <Feather name="check-circle" size={14} color="#34C759" />
            <Text style={styles.statText}>{item.visual_qa_score.toFixed(1)}%</Text>
          </View>
        )}
        {item.estimated_delivery_date && (
          <View style={styles.stat}>
            <Feather name="calendar" size={14} color="#8E8E93" />
            <Text style={styles.statText}>
              {new Date(item.estimated_delivery_date).toLocaleDateString()}
            </Text>
          </View>
        )}
      </View>
    </Pressable>
  );

  const filters = [
    { label: 'All', value: 'all' },
    { label: 'Intake', value: 'INTAKE' },
    { label: 'Design', value: 'DESIGN' },
    { label: 'Dev', value: 'DEV' },
    { label: 'QA', value: 'QA' },
    { label: 'Complete', value: 'COMPLETE' },
  ];

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
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
          placeholder="Search projects..."
          value={search}
          onChangeText={setSearch}
        />
      </View>

      <View style={styles.filterContainer}>
        {filters.map((f) => (
          <Pressable
            key={f.value}
            style={[
              styles.filterChip,
              filter === f.value && styles.filterChipActive,
            ]}
            onPress={() => setFilter(f.value)}
          >
            <Text
              style={[
                styles.filterText,
                filter === f.value && styles.filterTextActive,
              ]}
            >
              {f.label}
            </Text>
          </Pressable>
        ))}
      </View>

      <FlatList
        data={filteredProjects}
        renderItem={renderProject}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.listContent}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Feather name="folder" size={48} color="#8E8E93" />
            <Text style={styles.emptyText}>No projects found</Text>
          </View>
        }
      />

      <Pressable
        style={styles.fab}
        onPress={() => router.push('/project/new')}
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
    marginHorizontal: 16,
    marginTop: 16,
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
  filterContainer: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    paddingVertical: 12,
    gap: 8,
  },
  filterChip: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 16,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  filterChipActive: {
    backgroundColor: '#007AFF',
    borderColor: '#007AFF',
  },
  filterText: {
    fontSize: 14,
    color: '#8E8E93',
  },
  filterTextActive: {
    color: '#fff',
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
  projectInfo: {
    flex: 1,
  },
  nameRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
    marginBottom: 4,
  },
  projectName: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    flex: 1,
  },
  customerName: {
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
  description: {
    fontSize: 14,
    color: '#666',
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

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
import { useAuth } from '@/contexts/AuthContext';

interface Project {
  id: string;
  name: string;
  description: string | null;
  status: string;
  product_type: string;
  pricing_tier: string | null;
  visual_qa_score: number | null;
  estimated_delivery_date: string | null;
  actual_delivery_date: string | null;
  design_upload_url: string | null;
  final_code_url: string | null;
  created_at: string;
  customer: {
    id: string;
    full_name: string;
    email: string;
    company_name: string | null;
  };
}

interface ProjectNote {
  id: string;
  content: string;
  author_type: string;
  note_type: string;
  visibility: string;
  created_at: string;
  author_id: string;
}

export default function ProjectDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const router = useRouter();
  const { user } = useAuth();
  const [project, setProject] = useState<Project | null>(null);
  const [notes, setNotes] = useState<ProjectNote[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingNotes, setLoadingNotes] = useState(true);
  const [newNote, setNewNote] = useState('');
  const [addingNote, setAddingNote] = useState(false);
  const [showNoteInput, setShowNoteInput] = useState(false);

  useEffect(() => {
    if (id) {
      fetchProject();
      fetchNotes();
    }
  }, [id]);

  const fetchProject = async () => {
    try {
      const { data, error } = await supabase
        .from('projects')
        .select(`
          *,
          customer:customers(id, full_name, email, company_name)
        `)
        .eq('id', id)
        .single();

      if (error) {
        console.error('Error fetching project:', error);
        Alert.alert('Error', 'Failed to load project');
        router.back();
      } else {
        setProject(data);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchNotes = async () => {
    try {
      const { data, error } = await supabase
        .from('project_notes')
        .select('*')
        .eq('project_id', id)
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching notes:', error);
      } else {
        setNotes(data || []);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoadingNotes(false);
    }
  };

  const handleAddNote = async () => {
    if (!newNote.trim()) {
      Alert.alert('Validation Error', 'Note content is required');
      return;
    }

    setAddingNote(true);
    try {
      const { data, error } = await supabase
        .from('project_notes')
        .insert({
          project_id: id,
          author_id: user?.id,
          author_type: 'admin',
          content: newNote.trim(),
          note_type: 'general',
          visibility: 'internal',
        })
        .select()
        .single();

      if (error) {
        console.error('Error adding note:', error);
        Alert.alert('Error', error.message);
      } else {
        setNotes([data, ...notes]);
        setNewNote('');
        setShowNoteInput(false);
      }
    } catch (error) {
      console.error('Error:', error);
      Alert.alert('Error', 'An unexpected error occurred');
    } finally {
      setAddingNote(false);
    }
  };

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

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  if (!project) {
    return (
      <View style={styles.centerContainer}>
        <Text>Project not found</Text>
      </View>
    );
  }

  return (
    <>
      <Stack.Screen
        options={{
          title: project.name,
          headerShown: true,
        }}
      />
      <ScrollView style={styles.container}>
        {/* Project Header */}
        <View style={styles.header}>
          <View style={styles.headerRow}>
            <View style={styles.headerLeft}>
              <Feather
                name={getProductTypeIcon(project.product_type) as any}
                size={24}
                color="#007AFF"
              />
              <View style={styles.headerText}>
                <Text style={styles.projectName}>{project.name}</Text>
                <Pressable
                  onPress={() => router.push(`/customer/${project.customer.id}`)}
                >
                  <Text style={styles.customerLink}>
                    {project.customer.full_name}
                    {project.customer.company_name &&
                      ` • ${project.customer.company_name}`}
                  </Text>
                </Pressable>
              </View>
            </View>
            <View
              style={[
                styles.statusBadge,
                { backgroundColor: getStatusColor(project.status) },
              ]}
            >
              <Text style={styles.statusText}>{project.status}</Text>
            </View>
          </View>

          {project.description && (
            <Text style={styles.description}>{project.description}</Text>
          )}
        </View>

        {/* Project Details */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Project Details</Text>
          <View style={styles.card}>
            <View style={styles.field}>
              <Text style={styles.label}>Product Type</Text>
              <Text style={styles.value}>
                {project.product_type.replace('_', ' ').toUpperCase()}
              </Text>
            </View>

            {project.pricing_tier && (
              <>
                <View style={styles.divider} />
                <View style={styles.field}>
                  <Text style={styles.label}>Pricing Tier</Text>
                  <Text style={styles.value}>{project.pricing_tier}</Text>
                </View>
              </>
            )}

            {project.visual_qa_score && (
              <>
                <View style={styles.divider} />
                <View style={styles.field}>
                  <Text style={styles.label}>Visual QA Score</Text>
                  <View style={styles.row}>
                    <Feather name="check-circle" size={16} color="#34C759" />
                    <Text style={styles.value}>
                      {project.visual_qa_score.toFixed(1)}%
                    </Text>
                  </View>
                </View>
              </>
            )}

            {project.estimated_delivery_date && (
              <>
                <View style={styles.divider} />
                <View style={styles.field}>
                  <Text style={styles.label}>Estimated Delivery</Text>
                  <Text style={styles.value}>
                    {new Date(project.estimated_delivery_date).toLocaleDateString()}
                  </Text>
                </View>
              </>
            )}

            {project.actual_delivery_date && (
              <>
                <View style={styles.divider} />
                <View style={styles.field}>
                  <Text style={styles.label}>Actual Delivery</Text>
                  <Text style={styles.value}>
                    {new Date(project.actual_delivery_date).toLocaleDateString()}
                  </Text>
                </View>
              </>
            )}

            <View style={styles.divider} />
            <View style={styles.field}>
              <Text style={styles.label}>Created</Text>
              <Text style={styles.value}>
                {new Date(project.created_at).toLocaleDateString()}
              </Text>
            </View>
          </View>
        </View>

        {/* Files */}
        {(project.design_upload_url || project.final_code_url) && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Files</Text>
            <View style={styles.card}>
              {project.design_upload_url && (
                <View style={styles.field}>
                  <Text style={styles.label}>Design Upload</Text>
                  <Text style={styles.linkText} numberOfLines={1}>
                    {project.design_upload_url}
                  </Text>
                </View>
              )}
              {project.design_upload_url && project.final_code_url && (
                <View style={styles.divider} />
              )}
              {project.final_code_url && (
                <View style={styles.field}>
                  <Text style={styles.label}>Final Code</Text>
                  <Text style={styles.linkText} numberOfLines={1}>
                    {project.final_code_url}
                  </Text>
                </View>
              )}
            </View>
          </View>
        )}

        {/* Notes Timeline */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Notes Timeline</Text>
            <Pressable
              style={styles.addButton}
              onPress={() => setShowNoteInput(true)}
            >
              <Feather name="plus" size={16} color="#007AFF" />
              <Text style={styles.addButtonText}>Add Note</Text>
            </Pressable>
          </View>

          {showNoteInput && (
            <View style={styles.noteInputCard}>
              <TextInput
                style={styles.noteInput}
                value={newNote}
                onChangeText={setNewNote}
                placeholder="Add a note..."
                multiline
                numberOfLines={4}
                textAlignVertical="top"
              />
              <View style={styles.noteInputActions}>
                <Pressable
                  style={styles.noteInputCancel}
                  onPress={() => {
                    setNewNote('');
                    setShowNoteInput(false);
                  }}
                  disabled={addingNote}
                >
                  <Text style={styles.noteInputCancelText}>Cancel</Text>
                </Pressable>
                <Pressable
                  style={[
                    styles.noteInputSave,
                    addingNote && styles.buttonDisabled,
                  ]}
                  onPress={handleAddNote}
                  disabled={addingNote}
                >
                  {addingNote ? (
                    <ActivityIndicator color="#fff" size="small" />
                  ) : (
                    <Text style={styles.noteInputSaveText}>Add Note</Text>
                  )}
                </Pressable>
              </View>
            </View>
          )}

          {loadingNotes ? (
            <View style={styles.centerContainer}>
              <ActivityIndicator color="#007AFF" />
            </View>
          ) : notes.length === 0 ? (
            <View style={styles.emptyNotes}>
              <Feather name="message-square" size={32} color="#8E8E93" />
              <Text style={styles.emptyNotesText}>No notes yet</Text>
            </View>
          ) : (
            <View style={styles.timeline}>
              {notes.map((note, index) => (
                <View key={note.id} style={styles.timelineItem}>
                  <View style={styles.timelineDot} />
                  {index < notes.length - 1 && <View style={styles.timelineLine} />}
                  <View style={styles.noteCard}>
                    <View style={styles.noteHeader}>
                      <View style={styles.noteHeaderLeft}>
                        <Feather
                          name={
                            note.author_type === 'admin' ? 'shield' : 'user'
                          }
                          size={14}
                          color="#8E8E93"
                        />
                        <Text style={styles.noteAuthor}>
                          {note.author_type === 'admin' ? 'Admin' : 'Customer'}
                        </Text>
                        {note.visibility === 'customer' && (
                          <View style={styles.visibilityBadge}>
                            <Text style={styles.visibilityText}>
                              Customer Visible
                            </Text>
                          </View>
                        )}
                      </View>
                      <Text style={styles.noteDate}>
                        {new Date(note.created_at).toLocaleDateString()}
                      </Text>
                    </View>
                    <Text style={styles.noteContent}>{note.content}</Text>
                  </View>
                </View>
              ))}
            </View>
          )}
        </View>

        <View style={{ height: 32 }} />
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
    padding: 20,
  },
  header: {
    backgroundColor: '#fff',
    padding: 16,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E5EA',
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 12,
  },
  headerLeft: {
    flex: 1,
    flexDirection: 'row',
    gap: 12,
    alignItems: 'flex-start',
  },
  headerText: {
    flex: 1,
  },
  projectName: {
    fontSize: 22,
    fontWeight: '700',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  customerLink: {
    fontSize: 14,
    color: '#007AFF',
  },
  statusBadge: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  statusText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#fff',
  },
  description: {
    fontSize: 15,
    color: '#666',
    lineHeight: 21,
  },
  section: {
    marginTop: 24,
    paddingHorizontal: 16,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: '#8E8E93',
    textTransform: 'uppercase',
    paddingHorizontal: 4,
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  addButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#007AFF',
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
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  divider: {
    height: 1,
    backgroundColor: '#E5E5EA',
  },
  linkText: {
    fontSize: 14,
    color: '#007AFF',
  },
  noteInputCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
    padding: 12,
    marginBottom: 16,
  },
  noteInput: {
    fontSize: 15,
    color: '#1a1a1a',
    minHeight: 80,
    marginBottom: 12,
  },
  noteInputActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 8,
  },
  noteInputCancel: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  noteInputCancelText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#8E8E93',
  },
  noteInputSave: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
    backgroundColor: '#007AFF',
  },
  noteInputSaveText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#fff',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  emptyNotes: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 40,
  },
  emptyNotesText: {
    fontSize: 14,
    color: '#8E8E93',
    marginTop: 8,
  },
  timeline: {
    position: 'relative',
  },
  timelineItem: {
    position: 'relative',
    paddingLeft: 32,
    marginBottom: 16,
  },
  timelineDot: {
    position: 'absolute',
    left: 0,
    top: 8,
    width: 12,
    height: 12,
    borderRadius: 6,
    backgroundColor: '#007AFF',
    borderWidth: 2,
    borderColor: '#fff',
  },
  timelineLine: {
    position: 'absolute',
    left: 5,
    top: 20,
    width: 2,
    height: '100%',
    backgroundColor: '#E5E5EA',
  },
  noteCard: {
    backgroundColor: '#fff',
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
    padding: 12,
  },
  noteHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  noteHeaderLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  noteAuthor: {
    fontSize: 13,
    fontWeight: '600',
    color: '#1a1a1a',
  },
  visibilityBadge: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 4,
  },
  visibilityText: {
    fontSize: 10,
    fontWeight: '600',
    color: '#fff',
  },
  noteDate: {
    fontSize: 12,
    color: '#8E8E93',
  },
  noteContent: {
    fontSize: 14,
    color: '#1a1a1a',
    lineHeight: 20,
  },
});

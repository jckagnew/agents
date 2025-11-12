/**
 * Stitch Upload Screen
 * Allows users to upload HTML exports from Stitch for each screen
 * Shows generated Stitch prompts and tracks approval status
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
  Platform,
} from 'react-native';
import * as DocumentPicker from 'expo-document-picker';
import { ScreenMapping, StitchDesign, ProjectWithDetails } from '../types/project';

interface StitchUploadScreenProps {
  projectId: string;
  onComplete: () => void;
}

interface ScreenUploadState {
  screenMappingId: string;
  screenName: string;
  stateVariation?: string;
  uploaded: boolean;
  approved: boolean;
  designId?: string;
}

export default function StitchUploadScreen({
  projectId,
  onComplete,
}: StitchUploadScreenProps) {
  const [project, setProject] = useState<ProjectWithDetails | null>(null);
  const [uploadStates, setUploadStates] = useState<ScreenUploadState[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedScreen, setSelectedScreen] = useState<string | null>(null);
  const [uploadingScreen, setUploadingScreen] = useState<string | null>(null);

  useEffect(() => {
    loadProject();
  }, [projectId]);

  const loadProject = async () => {
    try {
      setIsLoading(true);
      // TODO: Replace with actual Supabase service call
      // const supabase = getSupabaseService();
      // const projectData = await supabase.getProjectWithDetails(projectId);
      // setProject(projectData);

      // For now, create mock upload states from screen mappings
      // const states = projectData.screen_mappings?.flatMap((mapping) => {
      //   return mapping.state_variations.map((variation) => ({
      //     screenMappingId: mapping.id,
      //     screenName: mapping.screen_name,
      //     stateVariation: variation !== 'default' ? variation : undefined,
      //     uploaded: false,
      //     approved: false,
      //   }));
      // }) || [];
      // setUploadStates(states);
    } catch (error) {
      console.error('Error loading project:', error);
      Alert.alert('Error', 'Failed to load project details');
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadHTML = async (screenState: ScreenUploadState) => {
    try {
      setUploadingScreen(`${screenState.screenName}-${screenState.stateVariation}`);

      // Pick HTML file
      const result = await DocumentPicker.getDocumentAsync({
        type: 'text/html',
        copyToCacheDirectory: true,
      });

      if (result.canceled) {
        setUploadingScreen(null);
        return;
      }

      // Read file content
      const file = result.assets[0];
      const htmlContent = await readFileAsText(file.uri);

      // Upload to Supabase
      // TODO: Replace with actual service call
      // const supabase = getSupabaseService();
      // const designId = await supabase.uploadStitchDesign(
      //   projectId,
      //   screenState.screenMappingId,
      //   screenState.screenName,
      //   htmlContent,
      //   screenState.stateVariation
      // );

      // Update upload state
      setUploadStates((prev) =>
        prev.map((state) =>
          state.screenMappingId === screenState.screenMappingId &&
          state.stateVariation === screenState.stateVariation
            ? { ...state, uploaded: true /* designId */ }
            : state
        )
      );

      Alert.alert('Success', `${screenState.screenName} HTML uploaded successfully`);
    } catch (error) {
      console.error('Error uploading HTML:', error);
      Alert.alert('Error', 'Failed to upload HTML file');
    } finally {
      setUploadingScreen(null);
    }
  };

  const readFileAsText = async (uri: string): Promise<string> => {
    // For web, use fetch
    if (Platform.OS === 'web') {
      const response = await fetch(uri);
      return await response.text();
    }

    // For native, use FileSystem
    const FileSystem = await import('expo-file-system');
    return await FileSystem.default.readAsStringAsync(uri);
  };

  const handleApproveDesign = async (screenState: ScreenUploadState) => {
    if (!screenState.designId) return;

    try {
      // TODO: Replace with actual service call
      // const supabase = getSupabaseService();
      // await supabase.approveStitchDesign(screenState.designId);

      // Update state
      setUploadStates((prev) =>
        prev.map((state) =>
          state.designId === screenState.designId ? { ...state, approved: true } : state
        )
      );

      Alert.alert('Success', 'Design approved');
    } catch (error) {
      console.error('Error approving design:', error);
      Alert.alert('Error', 'Failed to approve design');
    }
  };

  const handleGenerateCode = async () => {
    const allApproved = uploadStates.every((state) => state.approved);

    if (!allApproved) {
      Alert.alert(
        'Incomplete',
        'Please upload and approve all screen designs before generating code'
      );
      return;
    }

    try {
      // TODO: Replace with actual service call
      // const supabase = getSupabaseService();
      // const jobId = await supabase.generateCodeFromStitchDesigns(projectId);

      Alert.alert(
        'Code Generation Started',
        'Your code is being generated. You will be notified when it\'s ready.',
        [{ text: 'OK', onPress: onComplete }]
      );
    } catch (error) {
      console.error('Error generating code:', error);
      Alert.alert('Error', 'Failed to start code generation');
    }
  };

  const getScreenPrompt = (screenName: string): string => {
    const mapping = project?.screen_mappings?.find((m) => m.screen_name === screenName);
    return mapping?.stitch_prompt || 'No prompt available';
  };

  const renderScreenCard = (screenState: ScreenUploadState) => {
    const key = `${screenState.screenName}-${screenState.stateVariation || 'default'}`;
    const isSelected = selectedScreen === key;
    const isUploading = uploadingScreen === key;

    return (
      <View key={key} style={styles.screenCard}>
        <TouchableOpacity
          style={styles.screenHeader}
          onPress={() => setSelectedScreen(isSelected ? null : key)}
        >
          <View style={styles.screenTitleContainer}>
            <Text style={styles.screenName}>{screenState.screenName}</Text>
            {screenState.stateVariation && (
              <Text style={styles.screenVariation}>({screenState.stateVariation})</Text>
            )}
          </View>

          <View style={styles.screenStatus}>
            {screenState.approved && (
              <View style={styles.statusBadge}>
                <Text style={styles.statusText}>✓ Approved</Text>
              </View>
            )}
            {screenState.uploaded && !screenState.approved && (
              <View style={[styles.statusBadge, styles.statusBadgeWarning]}>
                <Text style={styles.statusText}>Pending Approval</Text>
              </View>
            )}
            {!screenState.uploaded && (
              <View style={[styles.statusBadge, styles.statusBadgeError]}>
                <Text style={styles.statusText}>Not Uploaded</Text>
              </View>
            )}
          </View>
        </TouchableOpacity>

        {isSelected && (
          <View style={styles.screenDetails}>
            <Text style={styles.promptLabel}>Stitch Prompt:</Text>
            <ScrollView style={styles.promptScroll} nestedScrollEnabled>
              <Text style={styles.promptText}>
                {getScreenPrompt(screenState.screenName)}
              </Text>
            </ScrollView>

            <View style={styles.actionButtons}>
              {!screenState.uploaded ? (
                <TouchableOpacity
                  style={[styles.uploadButton, isUploading && styles.buttonDisabled]}
                  onPress={() => handleUploadHTML(screenState)}
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <ActivityIndicator color="#fff" />
                  ) : (
                    <Text style={styles.uploadButtonText}>Upload HTML</Text>
                  )}
                </TouchableOpacity>
              ) : (
                <>
                  <TouchableOpacity
                    style={styles.reuploadButton}
                    onPress={() => handleUploadHTML(screenState)}
                  >
                    <Text style={styles.reuploadButtonText}>Re-upload</Text>
                  </TouchableOpacity>

                  {!screenState.approved && (
                    <TouchableOpacity
                      style={styles.approveButton}
                      onPress={() => handleApproveDesign(screenState)}
                    >
                      <Text style={styles.approveButtonText}>Approve Design</Text>
                    </TouchableOpacity>
                  )}
                </>
              )}
            </View>
          </View>
        )}
      </View>
    );
  };

  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#3498db" />
        <Text style={styles.loadingText}>Loading project details...</Text>
      </View>
    );
  }

  const uploadedCount = uploadStates.filter((s) => s.uploaded).length;
  const approvedCount = uploadStates.filter((s) => s.approved).length;
  const totalCount = uploadStates.length;

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scrollView} contentContainerStyle={styles.contentContainer}>
        <Text style={styles.title}>Upload Stitch Designs</Text>
        <Text style={styles.subtitle}>
          Upload the HTML exports from Stitch for each screen and state variation
        </Text>

        <View style={styles.progressCard}>
          <Text style={styles.progressTitle}>Progress</Text>
          <View style={styles.progressRow}>
            <Text style={styles.progressLabel}>Uploaded:</Text>
            <Text style={styles.progressValue}>
              {uploadedCount} / {totalCount}
            </Text>
          </View>
          <View style={styles.progressRow}>
            <Text style={styles.progressLabel}>Approved:</Text>
            <Text style={styles.progressValue}>
              {approvedCount} / {totalCount}
            </Text>
          </View>
          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressBarFill,
                { width: `${(approvedCount / totalCount) * 100}%` },
              ]}
            />
          </View>
        </View>

        <View style={styles.screensSection}>
          <Text style={styles.sectionTitle}>Screens</Text>
          {uploadStates.map((state) => renderScreenCard(state))}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        <TouchableOpacity
          style={[
            styles.generateButton,
            approvedCount !== totalCount && styles.generateButtonDisabled,
          ]}
          onPress={handleGenerateCode}
          disabled={approvedCount !== totalCount}
        >
          <Text style={styles.generateButtonText}>
            {approvedCount === totalCount
              ? 'Generate Code'
              : `Approve All Designs (${approvedCount}/${totalCount})`}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  scrollView: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 100,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: '#666',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#000',
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    marginBottom: 24,
  },
  progressCard: {
    backgroundColor: '#f8f9fa',
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
  },
  progressTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#000',
  },
  progressRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  progressLabel: {
    fontSize: 14,
    color: '#666',
  },
  progressValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#000',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginTop: 8,
    overflow: 'hidden',
  },
  progressBarFill: {
    height: '100%',
    backgroundColor: '#3498db',
    borderRadius: 4,
  },
  screensSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 16,
    color: '#000',
  },
  screenCard: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    marginBottom: 12,
    overflow: 'hidden',
  },
  screenHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#fff',
  },
  screenTitleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  screenName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000',
  },
  screenVariation: {
    fontSize: 14,
    color: '#666',
    marginLeft: 8,
  },
  screenStatus: {
    marginLeft: 12,
  },
  statusBadge: {
    backgroundColor: '#27ae60',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  statusBadgeWarning: {
    backgroundColor: '#f39c12',
  },
  statusBadgeError: {
    backgroundColor: '#95a5a6',
  },
  statusText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
  screenDetails: {
    padding: 16,
    backgroundColor: '#f8f9fa',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
  },
  promptLabel: {
    fontSize: 14,
    fontWeight: '600',
    marginBottom: 8,
    color: '#000',
  },
  promptScroll: {
    maxHeight: 150,
    backgroundColor: '#fff',
    borderRadius: 8,
    padding: 12,
    marginBottom: 16,
  },
  promptText: {
    fontSize: 14,
    color: '#333',
    lineHeight: 20,
  },
  actionButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  uploadButton: {
    flex: 1,
    backgroundColor: '#3498db',
    borderRadius: 8,
    padding: 14,
    alignItems: 'center',
  },
  uploadButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  reuploadButton: {
    flex: 1,
    backgroundColor: '#95a5a6',
    borderRadius: 8,
    padding: 14,
    alignItems: 'center',
  },
  reuploadButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  approveButton: {
    flex: 1,
    backgroundColor: '#27ae60',
    borderRadius: 8,
    padding: 14,
    alignItems: 'center',
  },
  approveButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  buttonDisabled: {
    backgroundColor: '#95a5a6',
  },
  footer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: '#fff',
    borderTopWidth: 1,
    borderTopColor: '#ddd',
    padding: 20,
  },
  generateButton: {
    backgroundColor: '#27ae60',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
  },
  generateButtonDisabled: {
    backgroundColor: '#95a5a6',
  },
  generateButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});

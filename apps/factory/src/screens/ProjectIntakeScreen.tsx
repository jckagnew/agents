/**
 * Enhanced Project Intake Screen
 * Supports inspiration websites (max 3, 1 lockable as brand guideline)
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Alert,
  Platform,
} from 'react-native';
import { InspirationWebsite, ProjectIntake, ServiceTier } from '../types/project';

interface ProjectIntakeScreenProps {
  onSubmit: (intake: ProjectIntake) => Promise<void>;
}

export default function ProjectIntakeScreen({ onSubmit }: ProjectIntakeScreenProps) {
  const [appName, setAppName] = useState('');
  const [appConcept, setAppConcept] = useState('');
  const [serviceTier, setServiceTier] = useState<ServiceTier>('concierge');
  const [inspirationWebsites, setInspirationWebsites] = useState<InspirationWebsite[]>([]);
  const [targetAudience, setTargetAudience] = useState('');
  const [designPreferences, setDesignPreferences] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const addInspirationWebsite = () => {
    if (inspirationWebsites.length >= 3) {
      Alert.alert('Maximum Reached', 'You can add up to 3 inspiration websites.');
      return;
    }

    setInspirationWebsites([
      ...inspirationWebsites,
      { url: '', locked: false, notes: '' },
    ]);
  };

  const removeInspirationWebsite = (index: number) => {
    setInspirationWebsites(inspirationWebsites.filter((_, i) => i !== index));
  };

  const updateInspirationWebsite = (
    index: number,
    field: keyof InspirationWebsite,
    value: any
  ) => {
    const updated = [...inspirationWebsites];
    updated[index] = { ...updated[index], [field]: value };
    setInspirationWebsites(updated);
  };

  const toggleLocked = (index: number) => {
    // Only one can be locked at a time
    const updated = inspirationWebsites.map((site, i) => ({
      ...site,
      locked: i === index ? !site.locked : false,
    }));
    setInspirationWebsites(updated);
  };

  const validateForm = (): boolean => {
    if (!appName.trim()) {
      Alert.alert('Validation Error', 'Please enter an app name.');
      return false;
    }

    if (!appConcept.trim()) {
      Alert.alert('Validation Error', 'Please describe your app concept.');
      return false;
    }

    // Validate inspiration websites
    for (const site of inspirationWebsites) {
      if (site.url && !isValidUrl(site.url)) {
        Alert.alert('Validation Error', `Invalid URL: ${site.url}`);
        return false;
      }
    }

    return true;
  };

  const isValidUrl = (url: string): boolean => {
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setIsSubmitting(true);

    try {
      const intake: ProjectIntake = {
        appName,
        appConcept,
        serviceTier,
        inspirationWebsites: inspirationWebsites.filter((site) => site.url.trim()),
        targetAudience: targetAudience.trim() || undefined,
        designPreferences: designPreferences.trim() || undefined,
      };

      await onSubmit(intake);

      // Success - form will be cleared by parent component navigation
    } catch (error) {
      Alert.alert('Error', 'Failed to submit project intake. Please try again.');
      console.error('Project intake submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      <Text style={styles.title}>Create Your App</Text>
      <Text style={styles.subtitle}>
        Let's start with the basics and some design inspiration
      </Text>

      {/* App Name */}
      <View style={styles.section}>
        <Text style={styles.label}>
          App Name <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={styles.input}
          value={appName}
          onChangeText={setAppName}
          placeholder="e.g., FitTracker Pro"
          placeholderTextColor="#999"
        />
      </View>

      {/* App Concept */}
      <View style={styles.section}>
        <Text style={styles.label}>
          App Concept <Text style={styles.required}>*</Text>
        </Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={appConcept}
          onChangeText={setAppConcept}
          placeholder="Describe your app idea in a few sentences..."
          placeholderTextColor="#999"
          multiline
          numberOfLines={4}
          textAlignVertical="top"
        />
      </View>

      {/* Service Tier */}
      <View style={styles.section}>
        <Text style={styles.label}>Service Tier</Text>
        <View style={styles.tierContainer}>
          <TouchableOpacity
            style={[
              styles.tierButton,
              serviceTier === 'express' && styles.tierButtonActive,
            ]}
            onPress={() => setServiceTier('express')}
          >
            <Text
              style={[
                styles.tierButtonText,
                serviceTier === 'express' && styles.tierButtonTextActive,
              ]}
            >
              Express
            </Text>
            <Text style={styles.tierDescription}>Fully automated</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.tierButton,
              serviceTier === 'concierge' && styles.tierButtonActive,
            ]}
            onPress={() => setServiceTier('concierge')}
          >
            <Text
              style={[
                styles.tierButtonText,
                serviceTier === 'concierge' && styles.tierButtonTextActive,
              ]}
            >
              Concierge
            </Text>
            <Text style={styles.tierDescription}>Collaborative design</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[
              styles.tierButton,
              serviceTier === 'premium' && styles.tierButtonActive,
            ]}
            onPress={() => setServiceTier('premium')}
          >
            <Text
              style={[
                styles.tierButtonText,
                serviceTier === 'premium' && styles.tierButtonTextActive,
              ]}
            >
              Premium
            </Text>
            <Text style={styles.tierDescription}>Professional design</Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Inspiration Websites */}
      <View style={styles.section}>
        <Text style={styles.label}>Inspiration Websites</Text>
        <Text style={styles.helperText}>
          Add up to 3 websites for design inspiration. Lock one as a brand guideline.
        </Text>

        {inspirationWebsites.map((site, index) => (
          <View key={index} style={styles.websiteCard}>
            <View style={styles.websiteHeader}>
              <Text style={styles.websiteNumber}>Website {index + 1}</Text>
              <TouchableOpacity
                onPress={() => removeInspirationWebsite(index)}
                style={styles.removeButton}
              >
                <Text style={styles.removeButtonText}>Remove</Text>
              </TouchableOpacity>
            </View>

            <TextInput
              style={styles.input}
              value={site.url}
              onChangeText={(text) => updateInspirationWebsite(index, 'url', text)}
              placeholder="https://example.com"
              placeholderTextColor="#999"
              keyboardType="url"
              autoCapitalize="none"
            />

            <TextInput
              style={[styles.input, styles.textArea]}
              value={site.notes}
              onChangeText={(text) => updateInspirationWebsite(index, 'notes', text)}
              placeholder="What do you like about this design?"
              placeholderTextColor="#999"
              multiline
              numberOfLines={2}
              textAlignVertical="top"
            />

            <TouchableOpacity
              style={styles.lockButton}
              onPress={() => toggleLocked(index)}
            >
              <View style={[styles.checkbox, site.locked && styles.checkboxChecked]}>
                {site.locked && <Text style={styles.checkmark}>✓</Text>}
              </View>
              <Text style={styles.lockButtonText}>
                Lock as brand guideline (must follow exactly)
              </Text>
            </TouchableOpacity>
          </View>
        ))}

        {inspirationWebsites.length < 3 && (
          <TouchableOpacity
            style={styles.addButton}
            onPress={addInspirationWebsite}
          >
            <Text style={styles.addButtonText}>+ Add Inspiration Website</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Optional: Target Audience */}
      <View style={styles.section}>
        <Text style={styles.label}>Target Audience (Optional)</Text>
        <TextInput
          style={styles.input}
          value={targetAudience}
          onChangeText={setTargetAudience}
          placeholder="e.g., Fitness enthusiasts aged 25-40"
          placeholderTextColor="#999"
        />
      </View>

      {/* Optional: Design Preferences */}
      <View style={styles.section}>
        <Text style={styles.label}>Design Preferences (Optional)</Text>
        <TextInput
          style={[styles.input, styles.textArea]}
          value={designPreferences}
          onChangeText={setDesignPreferences}
          placeholder="Any specific design preferences or requirements?"
          placeholderTextColor="#999"
          multiline
          numberOfLines={3}
          textAlignVertical="top"
        />
      </View>

      {/* Submit Button */}
      <TouchableOpacity
        style={[styles.submitButton, isSubmitting && styles.submitButtonDisabled]}
        onPress={handleSubmit}
        disabled={isSubmitting}
      >
        <Text style={styles.submitButtonText}>
          {isSubmitting ? 'Creating Project...' : 'Start Project'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 40,
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
  section: {
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#000',
  },
  required: {
    color: '#e74c3c',
  },
  helperText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 12,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
    backgroundColor: '#fff',
    color: '#000',
  },
  textArea: {
    minHeight: 80,
    paddingTop: 12,
  },
  tierContainer: {
    flexDirection: 'row',
    gap: 12,
  },
  tierButton: {
    flex: 1,
    borderWidth: 2,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    alignItems: 'center',
  },
  tierButtonActive: {
    borderColor: '#3498db',
    backgroundColor: '#e3f2fd',
  },
  tierButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  tierButtonTextActive: {
    color: '#3498db',
  },
  tierDescription: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
  },
  websiteCard: {
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
  },
  websiteHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  websiteNumber: {
    fontSize: 14,
    fontWeight: '600',
    color: '#000',
  },
  removeButton: {
    padding: 4,
  },
  removeButtonText: {
    color: '#e74c3c',
    fontSize: 14,
    fontWeight: '600',
  },
  lockButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderWidth: 2,
    borderColor: '#ddd',
    borderRadius: 4,
    marginRight: 8,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
  },
  checkboxChecked: {
    backgroundColor: '#3498db',
    borderColor: '#3498db',
  },
  checkmark: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
  },
  lockButtonText: {
    fontSize: 14,
    color: '#666',
    flex: 1,
  },
  addButton: {
    borderWidth: 2,
    borderColor: '#3498db',
    borderRadius: 8,
    borderStyle: 'dashed',
    padding: 16,
    alignItems: 'center',
  },
  addButtonText: {
    color: '#3498db',
    fontSize: 16,
    fontWeight: '600',
  },
  submitButton: {
    backgroundColor: '#3498db',
    borderRadius: 8,
    padding: 16,
    alignItems: 'center',
    marginTop: 8,
  },
  submitButtonDisabled: {
    backgroundColor: '#95a5a6',
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});

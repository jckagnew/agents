/**
 * Weight Tracker - Settings Screen
 * User preferences and app configuration
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Switch,
  Alert,
  Linking,
} from 'react-native';
import { useWeightTrackerStore, useSettings, useGatingFlags } from '../store';
import { ScreenHeader } from '../components';
import { theme } from '../theme';

interface SettingsScreenProps {
  navigation: any;
}

export const SettingsScreen: React.FC<SettingsScreenProps> = ({ navigation }) => {
  const { settings, updateSettings, clearAllData } = useWeightTrackerStore();
  const gatingFlags = useGatingFlags();
  const [isLoading, setIsLoading] = useState(false);

  const handleUnitChange = (type: 'weight' | 'length', value: string) => {
    updateSettings({
      ...settings,
      [`unit_${type}`]: value,
    });
  };

  const handleTargetChange = (field: string, value: number) => {
    updateSettings({
      ...settings,
      [field]: value,
    });
  };

  const handleClearData = () => {
    Alert.alert(
      'Clear All Data',
      'This will permanently delete all your weight tracking data. This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear Data',
          style: 'destructive',
          onPress: async () => {
            setIsLoading(true);
            try {
              await clearAllData();
              Alert.alert('Success', 'All data has been cleared.');
            } catch (error) {
              Alert.alert('Error', 'Failed to clear data. Please try again.');
            } finally {
              setIsLoading(false);
            }
          },
        },
      ]
    );
  };

  const handleExportData = () => {
    Alert.alert(
      'Export Data',
      'Data export feature coming soon! This will allow you to download your weight tracking data.',
      [{ text: 'OK' }]
    );
  };

  const handlePrivacyPolicy = () => {
    Linking.openURL('https://example.com/privacy-policy');
  };

  const handleTermsOfService = () => {
    Linking.openURL('https://example.com/terms-of-service');
  };

  const handleContactSupport = () => {
    Linking.openURL('mailto:support@example.com');
  };

  return (
    <ScrollView style={styles.container}>
      <ScreenHeader
        title="Settings"
        subtitle="Customize your experience"
        leftIcon="arrow-back"
        onPressLeft={() => navigation.goBack()}
        leftIconAccessibilityLabel="Back to dashboard"
        containerStyle={styles.header}
      />

      {/* Units Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Units</Text>
        
        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Weight Unit</Text>
          <View style={styles.unitButtons}>
            {['lb', 'kg', 'st'].map((unit) => (
              <TouchableOpacity
                key={unit}
                style={[
                  styles.unitButton,
                  settings.unit_weight === unit && styles.unitButtonActive,
                ]}
                onPress={() => handleUnitChange('weight', unit)}
              >
                <Text
                  style={[
                    styles.unitButtonText,
                    settings.unit_weight === unit && styles.unitButtonTextActive,
                  ]}
                >
                  {unit.toUpperCase()}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Length Unit</Text>
          <View style={styles.unitButtons}>
            {['in', 'cm'].map((unit) => (
              <TouchableOpacity
                key={unit}
                style={[
                  styles.unitButton,
                  settings.unit_length === unit && styles.unitButtonActive,
                ]}
                onPress={() => handleUnitChange('length', unit)}
              >
                <Text
                  style={[
                    styles.unitButtonText,
                    settings.unit_length === unit && styles.unitButtonTextActive,
                  ]}
                >
                  {unit.toUpperCase()}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>
      </View>

      {/* Goals Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Goals</Text>
        
        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Target Body Fat %</Text>
          <View style={styles.goalInput}>
            <TouchableOpacity
              style={styles.goalButton}
              onPress={() => {
                Alert.prompt(
                  'Target Body Fat %',
                  'Enter your target body fat percentage',
                  [
                    { text: 'Cancel', style: 'cancel' },
                    {
                      text: 'Save',
                      onPress: (text) => {
                        const value = parseFloat(text || '0');
                        if (!isNaN(value) && value > 0 && value < 100) {
                          handleTargetChange('target_bf_percent', value);
                        } else {
                          Alert.alert('Invalid Input', 'Please enter a valid percentage between 0 and 100.');
                        }
                      },
                    },
                  ],
                  'plain-text',
                  settings.target_bf_percent.toString()
                );
              }}
            >
              <Text style={styles.goalButtonText}>
                {settings.target_bf_percent}%
              </Text>
            </TouchableOpacity>
          </View>
        </View>

        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Height</Text>
          <View style={styles.goalInput}>
            <TouchableOpacity
              style={styles.goalButton}
              onPress={() => {
                Alert.prompt(
                  'Height',
                  `Enter your height in ${settings.unit_length}`,
                  [
                    { text: 'Cancel', style: 'cancel' },
                    {
                      text: 'Save',
                      onPress: (text) => {
                        const value = parseFloat(text || '0');
                        if (!isNaN(value) && value > 0) {
                          // Convert to inches for storage
                          const heightIn = settings.unit_length === 'cm' 
                            ? value / 2.54 
                            : value;
                          handleTargetChange('height_in', heightIn);
                        } else {
                          Alert.alert('Invalid Input', 'Please enter a valid height.');
                        }
                      },
                    },
                  ],
                  'plain-text',
                  (settings.unit_length === 'cm' 
                    ? (settings.height_in * 2.54).toFixed(1)
                    : settings.height_in.toFixed(1)
                  )
                );
              }}
            >
              <Text style={styles.goalButtonText}>
                {settings.unit_length === 'cm' 
                  ? `${(settings.height_in * 2.54).toFixed(1)} cm`
                  : `${settings.height_in.toFixed(1)} in`
                }
              </Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>

      {/* Data Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Data</Text>
        
        <TouchableOpacity
          style={styles.settingItem}
          onPress={handleExportData}
        >
          <Text style={styles.settingLabel}>Export Data</Text>
          <Text style={styles.settingValue}>Coming Soon</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.settingItem}
          onPress={handleClearData}
        >
          <Text style={[styles.settingLabel, styles.dangerText]}>Clear All Data</Text>
          <Text style={styles.settingValue}>⚠️</Text>
        </TouchableOpacity>
      </View>

      {/* Account Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Account</Text>
        
        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Plan</Text>
          <View style={styles.planContainer}>
            <Text
              style={[
                styles.planText,
                { color: settings.plan === 'pro' ? theme.colors.success : theme.colors.textSecondary },
              ]}
            >
              {settings.plan === 'pro' ? 'Pro' : 'Free'}
            </Text>
            {settings.plan === 'free' && (
              <TouchableOpacity
                style={styles.upgradeButton}
                onPress={() => navigation.navigate('Paywall')}
              >
                <Text style={styles.upgradeButtonText}>Upgrade</Text>
              </TouchableOpacity>
            )}
          </View>
        </View>
      </View>

      {/* Support Section */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Support</Text>
        
        <TouchableOpacity
          style={styles.settingItem}
          onPress={handleContactSupport}
        >
          <Text style={styles.settingLabel}>Contact Support</Text>
          <Text style={styles.settingValue}>→</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.settingItem}
          onPress={handlePrivacyPolicy}
        >
          <Text style={styles.settingLabel}>Privacy Policy</Text>
          <Text style={styles.settingValue}>→</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.settingItem}
          onPress={handleTermsOfService}
        >
          <Text style={styles.settingLabel}>Terms of Service</Text>
          <Text style={styles.settingValue}>→</Text>
        </TouchableOpacity>
      </View>

      {/* App Info */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>App</Text>
        
        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Version</Text>
          <Text style={styles.settingValue}>1.0.0</Text>
        </View>

        <View style={styles.settingItem}>
          <Text style={styles.settingLabel}>Build</Text>
          <Text style={styles.settingValue}>1</Text>
        </View>
      </View>

      {/* Loading Overlay */}
      {isLoading && (
        <View style={styles.loadingOverlay}>
          <Text style={styles.loadingText}>Processing...</Text>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
  },
  section: {
    margin: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    ...theme.shadows.sm,
  },
  sectionTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    marginBottom: theme.spacing.md,
    paddingHorizontal: theme.spacing.lg,
    paddingTop: theme.spacing.lg,
    color: theme.colors.textPrimary,
  },
  settingItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.borderLight,
  },
  settingLabel: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textPrimary,
  },
  settingValue: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textSecondary,
  },
  unitButtons: {
    flexDirection: 'row',
    gap: theme.spacing.sm,
  },
  unitButton: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.full,
    borderWidth: 1,
    borderColor: theme.colors.border,
    backgroundColor: theme.colors.surface,
  },
  unitButtonActive: {
    backgroundColor: theme.colors.primary,
    borderColor: theme.colors.primary,
  },
  unitButtonText: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.body,
    fontWeight: '600',
    color: theme.colors.textSecondary,
  },
  unitButtonTextActive: {
    color: theme.colors.textInverse,
  },
  goalInput: {
    flex: 1,
    alignItems: 'flex-end',
  },
  goalButton: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.lg,
    backgroundColor: theme.colors.tintBlue,
  },
  goalButtonText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.primary,
  },
  planContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: theme.spacing.sm,
  },
  planText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.label,
    fontWeight: '600',
  },
  upgradeButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.lg,
  },
  upgradeButtonText: {
    color: theme.colors.textInverse,
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.label,
    fontWeight: '600',
  },
  dangerText: {
    color: theme.colors.error,
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: theme.colors.textInverse,
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.label,
    fontWeight: '600',
  },
});

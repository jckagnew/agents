/**
 * Weight Tracker - Log Entry Screen
 * Multi-step modal for entering daily measurements
 * Redesigned with Google-inspired design system
 */

import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  KeyboardAvoidingView,
  Platform,
  Dimensions,
  Modal,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useWeightTrackerStore, useSettings, useGatingFlags, useRecordForDate } from '../store';
import { DailyRecord } from '../types';
import { convertWeightToLb, convertLengthToIn, isWeightOutlier } from '../utils/calculations';
import { Button, ProgressDots, Toast, ScreenHeader } from '../components';
import { theme } from '../theme';

const { width: screenWidth } = Dimensions.get('window');

interface LogEntryProps {
  navigation: any;
  route: {
    params: {
      date: string;
    };
  };
}

export const LogEntryScreen: React.FC<LogEntryProps> = ({ navigation, route }) => {
  const { date } = route.params;
  const { saveRecord, getLastRecord } = useWeightTrackerStore();
  const settings = useSettings();
  const gatingFlags = useGatingFlags();
  const existingRecord = useRecordForDate(date);

  // Multi-step state
  const [currentStep, setCurrentStep] = useState(1);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState<'success' | 'error'>('success');

  // Form data
  const [weight, setWeight] = useState('');
  const [neck, setNeck] = useState('');
  const [upperWaist, setUpperWaist] = useState('');
  const [lowerWaist, setLowerWaist] = useState('');
  const [hips, setHips] = useState('');
  const [notes, setNotes] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const totalSteps = 3;

  useEffect(() => {
    if (existingRecord) {
      // Convert from canonical units to display units
      setWeight(convertWeightFromLb(existingRecord.weight_lb, settings.unit_weight).toString());
      setNeck(convertLengthFromIn(existingRecord.neck_in, settings.unit_length).toString());
      setUpperWaist(convertLengthFromIn(existingRecord.upper_waist_in, settings.unit_length).toString());
      setLowerWaist(convertLengthFromIn(existingRecord.lower_waist_in, settings.unit_length).toString());
      setHips(convertLengthFromIn(existingRecord.hips_in, settings.unit_length).toString());
      setNotes(existingRecord.notes);
    }
  }, [existingRecord, settings]);

  const convertWeightFromLb = (weightLb: number, unit: 'lb' | 'kg' | 'st'): number => {
    switch (unit) {
      case 'lb': return weightLb;
      case 'kg': return weightLb / 2.20462;
      case 'st': return weightLb / 14;
      default: return weightLb;
    }
  };

  const convertLengthFromIn = (lengthIn: number, unit: 'in' | 'cm'): number => {
    switch (unit) {
      case 'in': return lengthIn;
      case 'cm': return lengthIn * 2.54;
      default: return lengthIn;
    }
  };

  const validateInputs = (): boolean => {
    if (!weight || !neck || !upperWaist || !lowerWaist || !hips) {
      Alert.alert('Missing Data', 'Please fill in all required measurements.');
      return false;
    }

    const weightNum = parseFloat(weight);
    const neckNum = parseFloat(neck);
    const upperWaistNum = parseFloat(upperWaist);
    const lowerWaistNum = parseFloat(lowerWaist);
    const hipsNum = parseFloat(hips);

    if (isNaN(weightNum) || weightNum <= 0) {
      Alert.alert('Invalid Weight', 'Please enter a valid weight.');
      return false;
    }

    if (isNaN(neckNum) || neckNum <= 0) {
      Alert.alert('Invalid Neck', 'Please enter a valid neck measurement.');
      return false;
    }

    if (isNaN(upperWaistNum) || upperWaistNum <= 0) {
      Alert.alert('Invalid Upper Waist', 'Please enter a valid upper waist measurement.');
      return false;
    }

    if (isNaN(lowerWaistNum) || lowerWaistNum <= 0) {
      Alert.alert('Invalid Lower Waist', 'Please enter a valid lower waist measurement.');
      return false;
    }

    if (isNaN(hipsNum) || hipsNum <= 0) {
      Alert.alert('Invalid Hips', 'Please enter a valid hip measurement.');
      return false;
    }

    // Check for logical measurements
    if (lowerWaistNum <= neckNum) {
      Alert.alert('Invalid Measurements', 'Lower waist should be larger than neck measurement.');
      return false;
    }

    if (hipsNum <= lowerWaistNum) {
      Alert.alert('Invalid Measurements', 'Hips should be larger than lower waist measurement.');
      return false;
    }

    return true;
  };

  const handleSave = async () => {
    if (!validateInputs()) return;

    setIsLoading(true);

    try {
      // Step 3: Data Input & Storage - Convert to canonical units
      const weightLb = convertWeightToLb(parseFloat(weight), settings.unit_weight);
      const neckIn = convertLengthToIn(parseFloat(neck), settings.unit_length);
      const upperWaistIn = convertLengthToIn(parseFloat(upperWaist), settings.unit_length);
      const lowerWaistIn = convertLengthToIn(parseFloat(lowerWaist), settings.unit_length);
      const hipsIn = convertLengthToIn(parseFloat(hips), settings.unit_length);

      // Step 3: Pre-Save Checks - Check for outliers (> 5 lbs in 24h)
      const lastRecord = getLastRecord();
      const isOutlier = isWeightOutlier(weightLb, lastRecord);

      if (isOutlier) {
        // Step 3: UI: Show > 5 lbs in 24h? prompt
        Alert.alert(
          'Weight Outlier Detected',
          `Your weight change (${Math.abs(weightLb - (lastRecord?.weight_lb || 0)).toFixed(1)} ${settings.unit_weight}) is more than 5 ${settings.unit_weight}. Is this correct?`,
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Yes, Save', onPress: () => saveRecordData(weightLb, neckIn, upperWaistIn, lowerWaistIn, hipsIn, true) },
          ]
        );
        return;
      }

      // Step 3: DB: Save/Update: Convert Canonical Units (lb, in)
      await saveRecordData(weightLb, neckIn, upperWaistIn, lowerWaistIn, hipsIn, false);
    } catch (error) {
      Alert.alert('Error', 'Failed to save record. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const saveRecordData = async (
    weightLb: number,
    neckIn: number,
    upperWaistIn: number,
    lowerWaistIn: number,
    hipsIn: number,
    isOutlier: boolean
  ) => {
    // Step 3: DB: Save/Update: Convert Canonical Units (lb, in)
    const record: DailyRecord = {
      date,
      weight_lb: weightLb,
      height_in: settings.height_in, // Use from settings
      neck_in: neckIn,
      upper_waist_in: upperWaistIn,
      lower_waist_in: lowerWaistIn,
      hips_in: hipsIn,
      notes: notes.trim(),
      flags: {
        outlier_weight: isOutlier,
        duplicate: false,
      },
      tags: [],
    };

    // Step 3: DB: Save/Update Record SQUIZE DB
    await saveRecord(record);
    
    // Step 4: Post-Save Calculations - Process & Calculate Metrics
    // This happens automatically in the store when saveRecord is called
    
    // Step 5: Final UI Update - Display Updated Dashboard
    Alert.alert('Success', 'Record saved successfully!', [
      { text: 'OK', onPress: () => navigation.goBack() },
    ]);
  };

  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const nextStep = () => {
    if (currentStep < totalSteps) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const showToastMessage = (message: string, type: 'success' | 'error' = 'success') => {
    setToastMessage(message);
    setToastType(type);
    setShowToast(true);
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>Weight Measurement</Text>
            <Text style={styles.stepDescription}>
              Enter your current weight to track your progress
            </Text>
            <View style={styles.inputGroup}>
              <Text style={styles.label}>Weight ({settings.unit_weight}) *</Text>
              <TextInput
                style={styles.input}
                value={weight}
                onChangeText={setWeight}
                placeholder={`Enter weight in ${settings.unit_weight}`}
                keyboardType="numeric"
                autoFocus
                accessibilityLabel={`Weight in ${settings.unit_weight}`}
                accessibilityHint="Enter your current weight"
              />
            </View>
          </View>
        );
      
      case 2:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>Body Measurements</Text>
            <Text style={styles.stepDescription}>
              Enter your body measurements for accurate body fat calculation
            </Text>
            
            <View style={styles.measurementsGrid}>
              <View style={styles.inputGroup}>
                <Text style={styles.label}>Neck ({settings.unit_length}) *</Text>
                <TextInput
                  style={styles.input}
                  value={neck}
                  onChangeText={setNeck}
                  placeholder={`Neck in ${settings.unit_length}`}
                  keyboardType="numeric"
                />
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>Upper Waist ({settings.unit_length}) *</Text>
                <TextInput
                  style={styles.input}
                  value={upperWaist}
                  onChangeText={setUpperWaist}
                  placeholder={`Upper waist in ${settings.unit_length}`}
                  keyboardType="numeric"
                />
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>Lower Waist ({settings.unit_length}) *</Text>
                <TextInput
                  style={styles.input}
                  value={lowerWaist}
                  onChangeText={setLowerWaist}
                  placeholder={`Lower waist in ${settings.unit_length}`}
                  keyboardType="numeric"
                />
              </View>

              <View style={styles.inputGroup}>
                <Text style={styles.label}>Hips ({settings.unit_length}) *</Text>
                <TextInput
                  style={styles.input}
                  value={hips}
                  onChangeText={setHips}
                  placeholder={`Hips in ${settings.unit_length}`}
                  keyboardType="numeric"
                />
              </View>
            </View>
          </View>
        );
      
      case 3:
        return (
          <View style={styles.stepContent}>
            <Text style={styles.stepTitle}>Additional Notes</Text>
            <Text style={styles.stepDescription}>
              Add any notes about today's measurements (optional)
            </Text>
            <View style={styles.inputGroup}>
              <TextInput
                style={[styles.input, styles.notesInput]}
                value={notes}
                onChangeText={setNotes}
                placeholder="Add any notes about today's measurements..."
                multiline
                numberOfLines={3}
              />
            </View>
          </View>
        );
      
      default:
        return null;
    }
  };

  return (
    <View style={styles.container}>
      {/* Main Content */}
      <ScrollView style={styles.scrollView}>
        <ScreenHeader
          title="Log Entry"
          subtitle={formatDate(date)}
          leftIcon="arrow-back"
          onPressLeft={() => navigation.goBack()}
          leftIconAccessibilityLabel="Back to previous screen"
          containerStyle={styles.header}
        >
          {existingRecord ? (
            <Text style={styles.existingText}>Updating existing entry</Text>
          ) : null}
        </ScreenHeader>

        {/* Quick Entry Button */}
        <View style={styles.quickEntrySection}>
          <Button
            title={existingRecord ? 'Update Entry' : 'Start Log Entry'}
            onPress={() => setIsModalVisible(true)}
            icon="add-circle"
            fullWidth
            size="lg"
          />
        </View>

        {/* Gating Information */}
        {!gatingFlags.allowMultipleEntriesPerDay && (
          <View style={styles.gatingInfo}>
            <Ionicons name="information-circle" size={20} color={theme.colors.warning} style={styles.gatingIcon} />
            <Text style={styles.gatingText}>
              Free Plan: One entry per day. Replace existing entry to update.
            </Text>
            <Button
              title="Upgrade to Pro"
              onPress={() => navigation.navigate('Paywall')}
              variant="outline"
              size="sm"
              style={styles.upgradeButton}
            />
          </View>
        )}
      </ScrollView>

      {/* Multi-Step Modal */}
      <Modal
        visible={isModalVisible}
        animationType="slide"
        presentationStyle="pageSheet"
        onRequestClose={() => setIsModalVisible(false)}
      >
        <KeyboardAvoidingView
          style={styles.modalContainer}
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        >
          {/* Modal Header */}
          <View style={styles.modalHeader}>
            <View style={styles.modalHeaderContent}>
              <Text style={styles.modalTitle}>
                {existingRecord ? 'Update Entry' : 'Log Entry'}
              </Text>
              <Text style={styles.modalSubtitle}>{formatDate(date)}</Text>
            </View>
            <TouchableOpacity
              style={styles.modalCloseButton}
              onPress={() => setIsModalVisible(false)}
            >
              <Ionicons name="close" size={24} color={theme.colors.textPrimary} />
            </TouchableOpacity>
          </View>

          {/* Progress Dots */}
          <View style={styles.progressSection}>
            <ProgressDots currentStep={currentStep} totalSteps={totalSteps} />
          </View>

          {/* Step Content */}
          <ScrollView style={styles.modalContent}>
            {renderStepContent()}
          </ScrollView>

          {/* Modal Actions */}
          <View style={styles.modalActions}>
            {currentStep > 1 && (
              <Button
                title="Back"
                onPress={prevStep}
                variant="outline"
                style={styles.modalButton}
              />
            )}
            
            {currentStep < totalSteps ? (
              <Button
                title="Next"
                onPress={nextStep}
                style={styles.modalButton}
              />
            ) : (
              <Button
                title={isLoading ? 'Saving...' : existingRecord ? 'Update Entry' : 'Save Entry'}
                onPress={handleSave}
                loading={isLoading}
                disabled={isLoading}
                style={styles.modalButton}
              />
            )}
          </View>
        </KeyboardAvoidingView>
      </Modal>

      {/* Toast Notification */}
      <Toast
        message={toastMessage}
        type={toastType}
        visible={showToast}
        onHide={() => setShowToast(false)}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  scrollView: {
    flex: 1,
  },
  header: {
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
  },
  existingText: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.secondary,
    marginTop: theme.spacing.xs,
  },
  quickEntrySection: {
    padding: theme.spacing.lg,
  },
  gatingInfo: {
    margin: theme.spacing.lg,
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.tintYellow,
    borderRadius: theme.borderRadius.lg,
    borderLeftWidth: 4,
    borderLeftColor: theme.colors.warning,
    flexDirection: 'row',
    alignItems: 'center',
  },
  gatingIcon: {
    marginRight: theme.spacing.sm,
  },
  gatingText: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.warning,
    flex: 1,
    marginRight: theme.spacing.sm,
  },
  upgradeButton: {
    flexShrink: 0,
  },
  // Modal styles
  modalContainer: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  modalHeaderContent: {
    flex: 1,
  },
  modalTitle: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
  },
  modalSubtitle: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
  modalCloseButton: {
    padding: theme.spacing.sm,
  },
  progressSection: {
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
  },
  modalContent: {
    flex: 1,
    padding: theme.spacing.lg,
  },
  stepContent: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    ...theme.shadows.md,
  },
  stepTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.sm,
  },
  stepDescription: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.lg,
  },
  measurementsGrid: {
    gap: theme.spacing.md,
  },
  inputGroup: {
    marginBottom: theme.spacing.md,
  },
  label: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.sm,
  },
  input: {
    ...theme.components.input,
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
  },
  notesInput: {
    height: 80,
    textAlignVertical: 'top',
  },
  modalActions: {
    flexDirection: 'row',
    padding: theme.spacing.lg,
    gap: theme.spacing.md,
    backgroundColor: theme.colors.surface,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
  },
  modalButton: {
    flex: 1,
  },
});

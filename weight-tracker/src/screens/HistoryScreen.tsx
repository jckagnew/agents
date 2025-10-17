/**
 * Weight Tracker - History Screen
 * Display historical weight and measurement data
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  FlatList,
  RefreshControl,
} from 'react-native';
import { useWeightTrackerStore, useSettings } from '../store';
import { DailyRecord } from '../types';
import { ScreenHeader } from '../components';
import { theme } from '../theme';

interface HistoryScreenProps {
  navigation: any;
}

export const HistoryScreen: React.FC<HistoryScreenProps> = ({ navigation }) => {
  const { records, isLoading, error, initializeApp } = useWeightTrackerStore();
  const settings = useSettings();
  const [refreshing, setRefreshing] = useState(false);
  const entrySummary = `${records.length} ${records.length === 1 ? 'entry' : 'entries'}`;

  useEffect(() => {
    initializeApp();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    await initializeApp();
    setRefreshing(false);
  };

  const formatDate = (dateStr: string): string => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const formatWeight = (weightLb: number): string => {
    switch (settings.unit_weight) {
      case 'kg':
        return `${(weightLb / 2.20462).toFixed(1)} kg`;
      case 'st':
        return `${(weightLb / 14).toFixed(1)} st`;
      default:
        return `${weightLb.toFixed(1)} lb`;
    }
  };

  const formatLength = (lengthIn: number): string => {
    switch (settings.unit_length) {
      case 'cm':
        return `${(lengthIn * 2.54).toFixed(1)} cm`;
      default:
        return `${lengthIn.toFixed(1)} in`;
    }
  };

  const renderRecord = ({ item }: { item: DailyRecord }) => (
    <TouchableOpacity
      style={styles.recordCard}
      onPress={() => navigation.navigate('LogEntry', { date: item.date })}
    >
      <View style={styles.recordHeader}>
        <Text style={styles.recordDate}>{formatDate(item.date)}</Text>
        <Text style={styles.recordWeight}>{formatWeight(item.weight_lb)}</Text>
      </View>
      
      <View style={styles.recordDetails}>
        <View style={styles.measurementRow}>
          <Text style={styles.measurementLabel}>Neck:</Text>
          <Text style={styles.measurementValue}>{formatLength(item.neck_in)}</Text>
        </View>
        <View style={styles.measurementRow}>
          <Text style={styles.measurementLabel}>Upper Waist:</Text>
          <Text style={styles.measurementValue}>{formatLength(item.upper_waist_in)}</Text>
        </View>
        <View style={styles.measurementRow}>
          <Text style={styles.measurementLabel}>Lower Waist:</Text>
          <Text style={styles.measurementValue}>{formatLength(item.lower_waist_in)}</Text>
        </View>
        <View style={styles.measurementRow}>
          <Text style={styles.measurementLabel}>Hips:</Text>
          <Text style={styles.measurementValue}>{formatLength(item.hips_in)}</Text>
        </View>
      </View>

      {item.notes && (
        <View style={styles.notesContainer}>
          <Text style={styles.notesText}>{item.notes}</Text>
        </View>
      )}

      {item.flags.outlier_weight && (
        <View style={styles.outlierFlag}>
          <Text style={styles.outlierText}>⚠️ Outlier</Text>
        </View>
      )}
    </TouchableOpacity>
  );

  if (isLoading) {
    return (
      <View style={styles.container}>
        <ScreenHeader
          title="Weight History"
          subtitle="Loading entries..."
          leftIcon="arrow-back"
          onPressLeft={() => navigation.goBack()}
          leftIconAccessibilityLabel="Back to dashboard"
          containerStyle={styles.header}
        />
        <View style={styles.centerContent}>
          <Text style={styles.loadingText}>Loading history...</Text>
        </View>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <ScreenHeader
          title="Weight History"
          subtitle="Something went wrong"
          leftIcon="arrow-back"
          onPressLeft={() => navigation.goBack()}
          leftIconAccessibilityLabel="Back to dashboard"
          containerStyle={styles.header}
        />
        <View style={styles.centerContent}>
          <Text style={styles.errorText}>Error: {error}</Text>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScreenHeader
        title="Weight History"
        subtitle={entrySummary}
        leftIcon="arrow-back"
        onPressLeft={() => navigation.goBack()}
        leftIconAccessibilityLabel="Back to dashboard"
        containerStyle={styles.header}
      />

      {records.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyTitle}>No entries yet</Text>
          <Text style={styles.emptySubtitle}>
            Start tracking your weight and measurements
          </Text>
          <TouchableOpacity
            style={styles.addButton}
            onPress={() => navigation.navigate('LogEntry', { date: new Date().toISOString().split('T')[0] })}
          >
            <Text style={styles.addButtonText}>Add First Entry</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={records.slice().reverse()} // Show newest first
          renderItem={renderRecord}
          keyExtractor={(item) => item.date}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
          contentContainerStyle={styles.listContainer}
          showsVerticalScrollIndicator={false}
        />
      )}
    </View>
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
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing['4xl'],
  },
  listContainer: {
    padding: theme.spacing.lg,
  },
  recordCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    marginBottom: theme.spacing.md,
    ...theme.shadows.sm,
  },
  recordHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  recordDate: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    fontWeight: '600',
    color: theme.colors.textPrimary,
  },
  recordWeight: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.primary,
  },
  recordDetails: {
    marginBottom: theme.spacing.sm,
  },
  measurementRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: theme.spacing.xs,
  },
  measurementLabel: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
  },
  measurementValue: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textPrimary,
  },
  notesContainer: {
    marginTop: theme.spacing.sm,
    paddingTop: theme.spacing.sm,
    borderTopWidth: 1,
    borderTopColor: theme.colors.borderLight,
  },
  notesText: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    fontStyle: 'italic',
  },
  outlierFlag: {
    position: 'absolute',
    top: theme.spacing.sm,
    right: theme.spacing.sm,
    backgroundColor: theme.colors.warning,
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.lg,
  },
  outlierText: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textInverse,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing['4xl'],
  },
  emptyTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.sm,
  },
  emptySubtitle: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginBottom: theme.spacing.xl,
  },
  addButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing['3xl'],
    paddingVertical: theme.spacing.md,
    borderRadius: theme.borderRadius.xl,
    ...theme.shadows.sm,
  },
  addButtonText: {
    color: theme.colors.textInverse,
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.label,
    fontWeight: '600',
  },
  loadingText: {
    fontSize: theme.typography.fontSize.bodyLg,
    fontFamily: theme.typography.fontFamily.body,
    textAlign: 'center',
    color: theme.colors.textSecondary,
  },
  errorText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    textAlign: 'center',
    color: theme.colors.error,
  },
});

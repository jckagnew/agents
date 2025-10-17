/**
 * Weight Tracker - Dashboard Screen
 * Main screen showing today's summary, charts, and metrics
 * Redesigned with Google-inspired design system
 */

import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useWeightTrackerStore, useCurrentMetrics, useSettings, useGatingFlags } from '../store';
import { DailyRecord } from '../types';
import { MetricCard, Button, TrendChart, ScreenHeader } from '../components';
import { theme } from '../theme';

const { width: screenWidth } = Dimensions.get('window');

interface DashboardProps {
  navigation: any;
}

export const DashboardScreen: React.FC<DashboardProps> = ({ navigation }) => {
  const { initializeApp, records, isLoading, error } = useWeightTrackerStore();
  const currentMetrics = useCurrentMetrics();
  const settings = useSettings();
  const gatingFlags = useGatingFlags();

  useEffect(() => {
    initializeApp();
  }, []);

  const today = new Date().toISOString().split('T')[0];
  const todayRecord = records.find(r => r.date === today);

  // Prepare chart data (last 30 days)
  const chartData = records
    .slice(-30)
    .map(record => ({
      x: new Date(record.date),
      y: record.weight_lb,
    }));

  // Calculate smoothed data for ghost overlay (Pro teaser)
  const smoothedData = records
    .slice(-30)
    .map(record => {
      // Simple 7-day average calculation
      const recordIndex = records.findIndex(r => r.date === record.date);
      if (recordIndex < 6) return null;
      
      const window = records.slice(recordIndex - 6, recordIndex + 1);
      const avg = window.reduce((sum, r) => sum + r.weight_lb, 0) / window.length;
      
      return {
        x: new Date(record.date),
        y: avg,
      };
    })
    .filter(Boolean);

  const handleLogEntry = () => {
    // Follow the process flow from the diagram
    if (todayRecord && !gatingFlags.allowMultipleEntriesPerDay) {
      // Step 2: Pre-Save Checks - Decision: 'Replace/...' Prompt
      Alert.alert(
        'Entry Exists',
        'You already have an entry for today. Would you like to replace it?',
        [
          { text: 'Cancel', style: 'cancel' },
          { 
            text: 'Replace', 
            onPress: () => navigation.navigate('LogEntry', { date: today }) 
          },
        ]
      );
    } else {
      // Step 1: Entry Initiation - User Taps 'Add/Today's Entry'
      navigation.navigate('LogEntry', { date: today });
    }
  };

  const handleUpgrade = () => {
    navigation.navigate('Paywall');
  };

  const handleHomePress = () => {
    initializeApp();
  };

  if (isLoading) {
    return (
      <View style={styles.container}>
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Error: {error}</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.container}>
      <ScreenHeader
        title="Weight Tracker"
        subtitle="Privacy-first tracking"
        leftIcon="home-outline"
        rightIcon="settings-outline"
        onPressLeft={handleHomePress}
        onPressRight={() => navigation.navigate('Settings')}
        leftIconAccessibilityLabel="Refresh dashboard"
        rightIconAccessibilityLabel="Open settings"
      />

      {/* Metrics Grid */}
      <View style={styles.metricsGrid}>
        {/* Today's Weight */}
        <MetricCard
          title="Today's Weight"
          value={todayRecord ? `${todayRecord.weight_lb.toFixed(1)} ${settings.unit_weight}` : 'No entry'}
          subtitle={currentMetrics?.smoothed_weight_7d ? `7-day avg: ${currentMetrics.smoothed_weight_7d.toFixed(1)} ${settings.unit_weight}` : undefined}
          delta={currentMetrics?.percent_change !== null ? {
            value: `${currentMetrics.percent_change.toFixed(1)}%`,
            isPositive: currentMetrics.percent_change < 0
          } : undefined}
          icon="scale-outline"
          tintColor="blue"
          onPress={handleLogEntry}
        />

        {/* Body Fat Percentage */}
        {currentMetrics?.navy_bf_percent && (
          <MetricCard
            title="Body Fat %"
            value={`${currentMetrics.navy_bf_percent}%`}
            subtitle="Navy method"
            icon="body-outline"
            tintColor="green"
          />
        )}

        {/* Waist-to-Hip Ratio */}
        {currentMetrics && (
          <MetricCard
            title="Waist-to-Hip Ratio"
            value={currentMetrics.whr.toFixed(2)}
            subtitle={currentMetrics.whr_category}
            icon="resize-outline"
            tintColor="yellow"
          />
        )}

        {/* Goal Progress */}
        <MetricCard
          title="Goal Progress"
          value={`${currentMetrics?.navy_bf_percent || 0}%`}
          subtitle={`Target: ${settings.target_bf_percent}%`}
          icon="flag-outline"
          tintColor="green"
        />
      </View>

      {/* Weight Trend Chart */}
      <View style={styles.chartSection}>
        <TrendChart
          data={chartData}
          goalLine={undefined} // No goal line for now, could be calculated from target_bf_percent
          title="Weight Trend (Last 30 Days)"
          subtitle="Track your progress over time"
        />
        {!gatingFlags.allowSmoothingChange && smoothedData.length > 0 && (
          <Text style={styles.teaserText}>
            Pro: Unlock smoothing controls and trend analysis
          </Text>
        )}
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <Button
          title={todayRecord ? 'Update Entry' : 'Log Entry'}
          onPress={handleLogEntry}
          icon="add-circle"
          fullWidth
          style={styles.primaryAction}
        />
        
        <View style={styles.secondaryActions}>
          <Button
            title="History"
            onPress={() => navigation.navigate('History')}
            variant="secondary"
            icon="time-outline"
            style={styles.secondaryButton}
          />
          
          <Button
            title="Reports"
            onPress={() => navigation.navigate('Reporting')}
            variant="secondary"
            icon="analytics-outline"
            style={styles.secondaryButton}
          />
        </View>
      </View>

      {/* Pro Upgrade Teaser */}
      {settings.plan === 'free' && (
        <TouchableOpacity style={styles.upgradeCard} onPress={handleUpgrade}>
          <View style={styles.upgradeContent}>
            <Ionicons name="star" size={24} color="white" style={styles.upgradeIcon} />
            <View style={styles.upgradeText}>
              <Text style={styles.upgradeTitle}>Unlock Pro Features</Text>
              <Text style={styles.upgradeDescription}>
                Get advanced analytics, custom smoothing, WHR trends, and more
              </Text>
            </View>
          </View>
        </TouchableOpacity>
      )}
    </ScrollView>
  );
};

function getCategoryColor(category: 'Low' | 'Moderate' | 'High'): string {
  switch (category) {
    case 'Low': return '#4CAF50';
    case 'Moderate': return '#FF9800';
    case 'High': return '#F44336';
    default: return '#666';
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  metricsGrid: {
    padding: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  chartSection: {
    margin: theme.spacing.lg,
  },
  teaserText: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginTop: theme.spacing.sm,
    fontStyle: 'italic',
  },
  actionButtons: {
    padding: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  primaryAction: {
    marginBottom: theme.spacing.sm,
  },
  secondaryActions: {
    flexDirection: 'row',
    gap: theme.spacing.md,
  },
  secondaryButton: {
    flex: 1,
  },
  upgradeCard: {
    margin: theme.spacing.lg,
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.secondary,
    borderRadius: theme.borderRadius.xl,
    ...theme.shadows.md,
  },
  upgradeContent: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  upgradeIcon: {
    marginRight: theme.spacing.md,
  },
  upgradeText: {
    flex: 1,
  },
  upgradeTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textInverse,
    marginBottom: theme.spacing.xs,
  },
  upgradeDescription: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: 'rgba(255, 255, 255, 0.9)',
  },
  loadingText: {
    fontSize: theme.typography.fontSize.bodyLg,
    fontFamily: theme.typography.fontFamily.body,
    textAlign: 'center',
    marginTop: theme.spacing['4xl'],
    color: theme.colors.textSecondary,
  },
  errorText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    textAlign: 'center',
    marginTop: theme.spacing['4xl'],
    color: theme.colors.error,
  },
});

/**
 * Weight Tracker - Reporting Screen
 * Display analytics and insights from weight tracking data
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { VictoryChart, VictoryLine, VictoryArea, VictoryAxis, VictoryBar } from 'victory-native';
import { useWeightTrackerStore, useCurrentMetrics, useSettings, useGatingFlags } from '../store';
import { ScreenHeader } from '../components';
import { theme } from '../theme';

interface ReportingScreenProps {
  navigation: any;
}

const { width: screenWidth } = Dimensions.get('window');

export const ReportingScreen: React.FC<ReportingScreenProps> = ({ navigation }) => {
  const { records, isLoading, error, initializeApp } = useWeightTrackerStore();
  const currentMetrics = useCurrentMetrics();
  const settings = useSettings();
  const gatingFlags = useGatingFlags();

  useEffect(() => {
    initializeApp();
  }, []);

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

  // Prepare chart data (last 30 days)
  const chartData = records
    .slice(-30)
    .map((record, index) => ({
      x: index,
      y: record.weight_lb,
      date: record.date,
    }));

  // Calculate 7-day moving average
  const smoothedData = records
    .slice(-30)
    .map((record, index) => {
      if (index < 6) return null;
      
      const window = records.slice(-30).slice(index - 6, index + 1);
      const avg = window.reduce((sum, r) => sum + r.weight_lb, 0) / window.length;
      
      return {
        x: index,
        y: avg,
        date: record.date,
      };
    })
    .filter(Boolean);

  // Calculate weekly averages for bar chart
  const weeklyData = [];
  for (let i = 0; i < records.length; i += 7) {
    const weekRecords = records.slice(i, i + 7);
    if (weekRecords.length > 0) {
      const avgWeight = weekRecords.reduce((sum, r) => sum + r.weight_lb, 0) / weekRecords.length;
      weeklyData.push({
        x: Math.floor(i / 7) + 1,
        y: avgWeight,
        week: `Week ${Math.floor(i / 7) + 1}`,
      });
    }
  }

  const getTrendDirection = (): 'up' | 'down' | 'stable' => {
    if (records.length < 2) return 'stable';
    
    const recent = records.slice(-7);
    const older = records.slice(-14, -7);
    
    if (recent.length === 0 || older.length === 0) return 'stable';
    
    const recentAvg = recent.reduce((sum, r) => sum + r.weight_lb, 0) / recent.length;
    const olderAvg = older.reduce((sum, r) => sum + r.weight_lb, 0) / older.length;
    
    const change = recentAvg - olderAvg;
    
    if (Math.abs(change) < 0.5) return 'stable';
    return change > 0 ? 'up' : 'down';
  };

  const getTrendColor = (): string => {
    const trend = getTrendDirection();
    switch (trend) {
      case 'up': return theme.colors.error;
      case 'down': return theme.colors.success;
      default: return theme.colors.textSecondary;
    }
  };

  const getTrendIcon = (): string => {
    const trend = getTrendDirection();
    switch (trend) {
      case 'up': return '📈';
      case 'down': return '📉';
      default: return '➡️';
    }
  };

  const renderHeader = () => (
    <ScreenHeader
      title="Analytics"
      subtitle="Track your progress and trends"
      leftIcon="arrow-back"
      onPressLeft={() => navigation.goBack()}
      leftIconAccessibilityLabel="Back to dashboard"
      containerStyle={styles.header}
    />
  );

  if (isLoading) {
    return (
      <View style={styles.container}>
        {renderHeader()}
        <View style={styles.centerContent}>
          <Text style={styles.loadingText}>Loading reports...</Text>
        </View>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        {renderHeader()}
        <View style={styles.centerContent}>
          <Text style={styles.errorText}>Error: {error}</Text>
        </View>
      </View>
    );
  }

  if (records.length === 0) {
    return (
      <View style={styles.container}>
        {renderHeader()}
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyTitle}>No data to analyze</Text>
          <Text style={styles.emptySubtitle}>
            Start logging entries to see your progress
          </Text>
          <TouchableOpacity
            style={styles.addButton}
            onPress={() => navigation.navigate('LogEntry', { date: new Date().toISOString().split('T')[0] })}
          >
            <Text style={styles.addButtonText}>Add First Entry</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {renderHeader()}
      <ScrollView contentContainerStyle={styles.scrollContent}>

      {/* Key Metrics */}
      <View style={styles.metricsCard}>
        <Text style={styles.cardTitle}>Key Metrics</Text>
        
        <View style={styles.metricsGrid}>
          <View style={styles.metricItem}>
            <Text style={styles.metricValue}>
              {formatWeight(records[records.length - 1]?.weight_lb || 0)}
            </Text>
            <Text style={styles.metricLabel}>Current Weight</Text>
          </View>
          
          <View style={styles.metricItem}>
            <Text style={[styles.metricValue, { color: getTrendColor() }]}>
              {getTrendIcon()} {Math.abs(currentMetrics?.percent_change || 0).toFixed(1)}%
            </Text>
            <Text style={styles.metricLabel}>7-Day Change</Text>
          </View>
          
          <View style={styles.metricItem}>
            <Text style={styles.metricValue}>
              {records.length}
            </Text>
            <Text style={styles.metricLabel}>Total Entries</Text>
          </View>
          
          <View style={styles.metricItem}>
            <Text style={styles.metricValue}>
              {currentMetrics?.navy_bf_percent?.toFixed(1) || '--'}%
            </Text>
            <Text style={styles.metricLabel}>Body Fat %</Text>
          </View>
        </View>
      </View>

      {/* Weight Trend Chart */}
      <View style={styles.chartCard}>
        <Text style={styles.cardTitle}>Weight Trend (Last 30 Days)</Text>
        {chartData.length > 0 ? (
          <View style={styles.chartContainer}>
            <VictoryChart
              height={200}
              width={screenWidth - 32}
              padding={{ left: 50, right: 20, top: 20, bottom: 40 }}
            >
              <VictoryAxis
                dependentAxis
                tickFormat={(x) => `${x.toFixed(0)}`}
                style={{
                  axis: { stroke: theme.colors.textSecondary },
                  tickLabels: { fontSize: 12, fill: theme.colors.textSecondary },
                }}
              />
              <VictoryAxis
                tickFormat={(x) => {
                  const dataPoint = chartData[x];
                  if (!dataPoint) return '';
                  const date = new Date(dataPoint.date);
                  return `${date.getMonth() + 1}/${date.getDate()}`;
                }}
                style={{
                  axis: { stroke: '#666' },
                  tickLabels: { fontSize: 12, fill: '#666' },
                }}
              />
              <VictoryArea
                data={chartData}
                style={{
                  data: { fill: theme.colors.chartPrimary, fillOpacity: 0.3 },
                }}
              />
              <VictoryLine
                data={chartData}
                style={{
                  data: { stroke: theme.colors.chartPrimary, strokeWidth: 3 },
                }}
              />
              {/* Pro teaser: Smoothed line */}
              {!gatingFlags.allowSmoothingChange && smoothedData.length > 0 && (
                <VictoryLine
                  data={smoothedData}
                  style={{
                    data: {
                      stroke: theme.colors.textSecondary,
                      strokeWidth: 2,
                      strokeDasharray: '5,5',
                      opacity: 0.7,
                    },
                  }}
                />
              )}
            </VictoryChart>
            {!gatingFlags.allowSmoothingChange && (
              <Text style={styles.teaserText}>
                Pro: Unlock smoothing controls and advanced analytics
              </Text>
            )}
          </View>
        ) : (
          <Text style={styles.noDataText}>No data to display</Text>
        )}
      </View>

      {/* Weekly Progress */}
      {weeklyData.length > 0 && (
        <View style={styles.chartCard}>
          <Text style={styles.cardTitle}>Weekly Averages</Text>
          <View style={styles.chartContainer}>
            <VictoryChart
              height={200}
              width={screenWidth - 32}
              padding={{ left: 50, right: 20, top: 20, bottom: 40 }}
            >
              <VictoryAxis
                dependentAxis
                tickFormat={(x) => `${x.toFixed(0)}`}
                style={{
                  axis: { stroke: theme.colors.textSecondary },
                  tickLabels: { fontSize: 12, fill: theme.colors.textSecondary },
                }}
              />
              <VictoryAxis
                tickFormat={(x) => `W${x}`}
                style={{
                  axis: { stroke: theme.colors.textSecondary },
                  tickLabels: { fontSize: 12, fill: theme.colors.textSecondary },
                }}
              />
              <VictoryBar
                data={weeklyData}
                style={{
                  data: { fill: theme.colors.success, fillOpacity: 0.8 },
                }}
              />
            </VictoryChart>
          </View>
        </View>
      )}

      {/* WHR Analysis */}
      {currentMetrics && (
        <View style={styles.whrCard}>
          <Text style={styles.cardTitle}>Waist-to-Hip Ratio Analysis</Text>
          <View style={styles.whrContent}>
            <View style={styles.whrMetric}>
              <Text style={styles.whrValue}>
                {currentMetrics.whr.toFixed(2)}
              </Text>
              <Text style={styles.whrLabel}>Current WHR</Text>
            </View>
            <View style={[
              styles.categoryPill,
              { backgroundColor: getCategoryColor(currentMetrics.whr_category) }
            ]}>
              <Text style={styles.categoryText}>
                {currentMetrics.whr_category}
              </Text>
            </View>
          </View>
          {!gatingFlags.allowWHRTrend && (
            <Text style={styles.teaserText}>
              Pro: Unlock WHR trend analysis and health insights
            </Text>
          )}
        </View>
      )}

      {/* Pro Upgrade */}
      {settings.plan === 'free' && (
        <TouchableOpacity
          style={styles.upgradeCard}
          onPress={() => navigation.navigate('Paywall')}
        >
          <Text style={styles.upgradeTitle}>Unlock Advanced Analytics</Text>
          <Text style={styles.upgradeText}>
            Get detailed insights, trend analysis, and personalized recommendations
          </Text>
        </TouchableOpacity>
      )}
      </ScrollView>
    </View>
  );
};

function getCategoryColor(category: 'Low' | 'Moderate' | 'High'): string {
  switch (category) {
    case 'Low': return theme.colors.success;
    case 'Moderate': return theme.colors.warning;
    case 'High': return theme.colors.error;
    default: return theme.colors.textSecondary;
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
  },
  scrollContent: {
    paddingBottom: theme.spacing['4xl'],
  },
  centerContent: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing['4xl'],
  },
  metricsCard: {
    margin: theme.spacing.lg,
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    ...theme.shadows.sm,
  },
  cardTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    marginBottom: theme.spacing.md,
    color: theme.colors.textPrimary,
  },
  metricsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  metricItem: {
    width: '48%',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  metricValue: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.primary,
    marginBottom: theme.spacing.xs,
  },
  metricLabel: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
  chartCard: {
    margin: theme.spacing.lg,
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    ...theme.shadows.sm,
  },
  chartContainer: {
    alignItems: 'center',
  },
  teaserText: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    marginTop: theme.spacing.sm,
    fontStyle: 'italic',
  },
  noDataText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    fontStyle: 'italic',
  },
  whrCard: {
    margin: theme.spacing.lg,
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    ...theme.shadows.sm,
  },
  whrContent: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  whrMetric: {
    alignItems: 'center',
  },
  whrValue: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
  },
  whrLabel: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
  },
  categoryPill: {
    paddingHorizontal: theme.spacing.lg,
    paddingVertical: theme.spacing.sm,
    borderRadius: theme.borderRadius.full,
  },
  categoryText: {
    color: theme.colors.textInverse,
    fontFamily: theme.typography.fontFamily.label,
    fontSize: theme.typography.fontSize.body,
    fontWeight: '600',
  },
  upgradeCard: {
    margin: theme.spacing.lg,
    padding: theme.spacing.xl,
    backgroundColor: theme.colors.warning,
    borderRadius: theme.borderRadius.xl,
    alignItems: 'center',
  },
  upgradeTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textInverse,
    marginBottom: theme.spacing.sm,
  },
  upgradeText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textInverse,
    textAlign: 'center',
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

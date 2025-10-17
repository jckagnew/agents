import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Platform,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useWeight } from '../context/WeightContext';

const { width: screenWidth } = Dimensions.get('window');

export default function DashboardScreen({ navigation }: any) {
  const { entries, currentWeight, currentBodyFat, goalWeight } = useWeight();
  
  // Calculate metrics
  const startWeight = entries[0]?.weight || 0;
  const totalLoss = startWeight - currentWeight;
  const weekAvg = entries.slice(-7).reduce((sum, entry) => sum + entry.weight, 0) / Math.min(7, entries.length);
  const weeklyLoss = totalLoss / Math.max(1, Math.floor(entries.length / 7));
  const remainingToGoal = currentWeight - goalWeight;
  const progressPercentage = Math.min(100, ((startWeight - currentWeight) / (startWeight - goalWeight)) * 100);

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.headerContent}>
          <Text style={styles.title}>Weight Tracker Pro</Text>
          <Text style={styles.subtitle}>Privacy-first tracking</Text>
        </View>
        <TouchableOpacity
          style={styles.settingsButton}
          onPress={() => navigation.navigate('Settings')}
        >
          <Ionicons name="settings-outline" size={24} color="white" />
        </TouchableOpacity>
      </View>

      <View style={styles.summaryCard}>
        <Text style={styles.cardTitle}>Today's Summary</Text>
        <View style={styles.summaryContent}>
          <Text style={styles.weightText}>{currentWeight} lbs</Text>
          <Text style={styles.bfText}>Navy BF%: {currentBodyFat}%</Text>
          <Text style={styles.smoothedText}>7-day avg: {weekAvg.toFixed(1)} lbs</Text>
          <Text style={styles.changeText}>-{weeklyLoss.toFixed(1)}% this week</Text>
        </View>
      </View>

      <View style={styles.chartCard}>
        <Text style={styles.cardTitle}>Weight Trend (Last 30 Days)</Text>
        <View style={styles.chartPlaceholder}>
          <Ionicons name="stats-chart-outline" size={48} color="#999" />
          <Text style={styles.chartText}>Weight Chart</Text>
          <Text style={styles.chartSubtext}>Pro: Unlock smoothing controls</Text>
          <Text style={styles.chartData}>
            Start: {startWeight} lbs → Current: {currentWeight} lbs
          </Text>
          <Text style={styles.chartData}>
            Average weekly loss: {weeklyLoss.toFixed(1)} lbs
          </Text>
        </View>
      </View>

      <View style={styles.actionButtons}>
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation.navigate('LogEntry')}
        >
          <Ionicons name="add-circle" size={24} color="white" style={styles.buttonIcon} />
          <Text style={styles.buttonText}>Log Entry</Text>
        </TouchableOpacity>

        <View style={styles.secondaryButtons}>
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('History')}
          >
            <Ionicons name="time-outline" size={20} color="#2196F3" style={styles.buttonIcon} />
            <Text style={styles.secondaryButtonText}>History</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => navigation.navigate('Analytics')}
          >
            <Ionicons name="analytics-outline" size={20} color="#2196F3" style={styles.buttonIcon} />
            <Text style={styles.secondaryButtonText}>Analytics</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.progressCard}>
        <Text style={styles.cardTitle}>12-Week Progress</Text>
        <View style={styles.progressGrid}>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{totalLoss.toFixed(1)} lbs</Text>
            <Text style={styles.progressLabel}>Total Lost</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{weeklyLoss.toFixed(1)} lbs</Text>
            <Text style={styles.progressLabel}>Per Week</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{(15.2 - currentBodyFat).toFixed(1)}%</Text>
            <Text style={styles.progressLabel}>BF Reduction</Text>
          </View>
          <View style={styles.progressItem}>
            <Text style={styles.progressValue}>{Math.ceil(remainingToGoal / weeklyLoss)}</Text>
            <Text style={styles.progressLabel}>Days to Goal</Text>
          </View>
        </View>
        <View style={styles.progressBar}>
          <View 
            style={[styles.progressFill, { width: `${progressPercentage}%` }]}
          />
        </View>
        <Text style={styles.progressText}>
          {Math.round(progressPercentage)}% to goal
        </Text>
      </View>

      <View style={styles.platformCard}>
        <Text style={styles.cardTitle}>Universal App Demo</Text>
        <Text style={styles.platformText}>
          This sophisticated Weight Tracker app runs natively on:
        </Text>
        <View style={styles.platformBadges}>
          <View style={styles.platformBadge}>
            <Ionicons name="logo-apple" size={16} color="#007AFF" />
            <Text style={styles.platformBadgeText}>iOS</Text>
          </View>
          <View style={styles.platformBadge}>
            <Ionicons name="logo-android" size={16} color="#3DDC84" />
            <Text style={styles.platformBadgeText}>Android</Text>
          </View>
          <View style={styles.platformBadge}>
            <Ionicons name="globe-outline" size={16} color="#2196F3" />
            <Text style={styles.platformBadgeText}>Web</Text>
          </View>
        </View>
        <Text style={styles.platformSubtext}>
          Single codebase • Native performance • Consistent UX
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#2196F3',
  },
  headerContent: {
    flex: 1,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  subtitle: {
    fontSize: 14,
    color: 'rgba(255, 255, 255, 0.8)',
    marginTop: 4,
  },
  settingsButton: {
    padding: 8,
  },
  summaryCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#333',
  },
  summaryContent: {
    alignItems: 'center',
  },
  weightText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
    marginBottom: 8,
  },
  bfText: {
    fontSize: 16,
    color: '#666',
    marginBottom: 4,
  },
  smoothedText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
  },
  changeText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#4CAF50',
  },
  chartCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  chartPlaceholder: {
    height: 200,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  chartText: {
    fontSize: 18,
    color: '#666',
    marginTop: 8,
  },
  chartSubtext: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    fontStyle: 'italic',
  },
  chartData: {
    fontSize: 12,
    color: '#999',
    marginTop: 4,
    textAlign: 'center',
  },
  actionButtons: {
    margin: 16,
    gap: 12,
  },
  primaryButton: {
    backgroundColor: '#2196F3',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  buttonIcon: {
    marginRight: 8,
  },
  buttonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
  },
  secondaryButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  secondaryButton: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#2196F3',
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 1,
  },
  secondaryButtonText: {
    color: '#2196F3',
    fontSize: 16,
    fontWeight: 'bold',
  },
  progressCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  progressGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  progressItem: {
    width: '48%',
    alignItems: 'center',
    marginBottom: 16,
  },
  progressValue: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#2196F3',
  },
  progressLabel: {
    fontSize: 12,
    color: '#666',
    marginTop: 4,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#e0e0e0',
    borderRadius: 4,
    marginBottom: 8,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#2196F3',
    borderRadius: 4,
  },
  progressText: {
    textAlign: 'center',
    color: '#666',
    fontSize: 14,
  },
  platformCard: {
    margin: 16,
    padding: 16,
    backgroundColor: 'white',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  platformText: {
    color: '#666',
    marginBottom: 12,
    lineHeight: 20,
  },
  platformBadges: {
    flexDirection: 'row',
    gap: 8,
    marginBottom: 12,
  },
  platformBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f0f8ff',
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 20,
    gap: 4,
  },
  platformBadgeText: {
    color: '#2196F3',
    fontSize: 12,
    fontWeight: '600',
  },
  platformSubtext: {
    color: '#999',
    fontSize: 12,
  },
});

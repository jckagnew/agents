/**
 * Weight Tracker - State Management with Zustand
 * Manages application state including records, settings, and UI state
 */

import { create } from 'zustand';
import { DailyRecord, Settings, CalculatedMetrics, GatingFlags, DEFAULT_SETTINGS } from '../types';
import { databaseService } from '../services/database';
import { calculateAllMetrics, isWeightOutlier } from '../utils/calculations';

interface WeightTrackerState {
  // Data
  records: DailyRecord[];
  settings: Settings;
  currentMetrics: CalculatedMetrics | null;
  
  // UI State
  isLoading: boolean;
  error: string | null;
  selectedDate: string;
  
  // Actions
  initializeApp: () => Promise<void>;
  loadRecords: () => Promise<void>;
  loadSettings: () => Promise<void>;
  saveRecord: (record: DailyRecord) => Promise<void>;
  updateSettings: (settings: Partial<Settings>) => Promise<void>;
  deleteRecord: (date: string) => Promise<void>;
  setSelectedDate: (date: string) => void;
  clearError: () => void;
  
  // Computed values
  getGatingFlags: () => GatingFlags;
  getRecordForDate: (date: string) => DailyRecord | null;
  hasRecordForDate: (date: string) => boolean;
  getLastRecord: () => DailyRecord | null;
  getRecordsInRange: (startDate: string, endDate: string) => DailyRecord[];
}

export const useWeightTrackerStore = create<WeightTrackerState>((set, get) => ({
  // Initial state
  records: [],
  settings: DEFAULT_SETTINGS,
  currentMetrics: null,
  isLoading: false,
  error: null,
  selectedDate: new Date().toISOString().split('T')[0],

  // Actions
  initializeApp: async () => {
    set({ isLoading: true, error: null });
    
    try {
      await databaseService.initialize();
      await Promise.all([
        get().loadRecords(),
        get().loadSettings(),
      ]);
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to initialize app' });
    } finally {
      set({ isLoading: false });
    }
  },

  loadRecords: async () => {
    try {
      const records = await databaseService.getAllDailyRecords();
      set({ records });
      
      // Calculate current metrics for today
      const today = new Date().toISOString().split('T')[0];
      const todayRecord = records.find(r => r.date === today);
      if (todayRecord) {
        const metrics = calculateAllMetrics(todayRecord, get().settings, records);
        set({ currentMetrics: metrics });
      }
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to load records' });
    }
  },

  loadSettings: async () => {
    try {
      const settings = await databaseService.getSettings();
      if (settings) {
        set({ settings });
      }
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to load settings' });
    }
  },

  saveRecord: async (record: DailyRecord) => {
    set({ isLoading: true, error: null });
    
    try {
      // Check for outliers
      const lastRecord = get().getLastRecord();
      const isOutlier = isWeightOutlier(record.weight_lb, lastRecord);
      
      if (isOutlier) {
        record.flags.outlier_weight = true;
      }
      
      await databaseService.insertDailyRecord(record);
      
      // Reload records to get updated data
      await get().loadRecords();
      
      // Update current metrics if this is today's record
      const today = new Date().toISOString().split('T')[0];
      if (record.date === today) {
        const metrics = calculateAllMetrics(record, get().settings, get().records);
        set({ currentMetrics: metrics });
      }
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to save record' });
    } finally {
      set({ isLoading: false });
    }
  },

  updateSettings: async (newSettings: Partial<Settings>) => {
    set({ isLoading: true, error: null });
    
    try {
      const updatedSettings = { ...get().settings, ...newSettings };
      await databaseService.saveSettings(updatedSettings);
      set({ settings: updatedSettings });
      
      // Recalculate current metrics with new settings
      const today = new Date().toISOString().split('T')[0];
      const todayRecord = get().records.find(r => r.date === today);
      if (todayRecord) {
        const metrics = calculateAllMetrics(todayRecord, updatedSettings, get().records);
        set({ currentMetrics: metrics });
      }
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to update settings' });
    } finally {
      set({ isLoading: false });
    }
  },

  deleteRecord: async (date: string) => {
    set({ isLoading: true, error: null });
    
    try {
      await databaseService.deleteDailyRecord(date);
      await get().loadRecords();
      
      // Update current metrics if we deleted today's record
      const today = new Date().toISOString().split('T')[0];
      if (date === today) {
        set({ currentMetrics: null });
      }
    } catch (error) {
      set({ error: error instanceof Error ? error.message : 'Failed to delete record' });
    } finally {
      set({ isLoading: false });
    }
  },

  setSelectedDate: (date: string) => {
    set({ selectedDate: date });
  },

  clearError: () => {
    set({ error: null });
  },

  // Computed values
  getGatingFlags: (): GatingFlags => {
    const { plan } = get().settings;
    
    return {
      allowMultipleEntriesPerDay: plan === 'pro',
      allowCustomBF: plan === 'pro',
      allowWHRTrend: plan === 'pro',
      allowGoalMoving: plan === 'pro',
      allowSmoothingChange: plan === 'pro',
      maxSavedCustomRanges: plan === 'pro' ? Infinity : 1,
      allowPhotoJournal: plan === 'pro',
      allowExport: plan === 'pro',
    };
  },

  getRecordForDate: (date: string): DailyRecord | null => {
    return get().records.find(r => r.date === date) || null;
  },

  hasRecordForDate: (date: string): boolean => {
    return get().records.some(r => r.date === date);
  },

  getLastRecord: (): DailyRecord | null => {
    const { records } = get();
    if (records.length === 0) return null;
    
    return records[records.length - 1];
  },

  getRecordsInRange: (startDate: string, endDate: string): DailyRecord[] => {
    return get().records.filter(r => r.date >= startDate && r.date <= endDate);
  },
}));

// Selectors for specific data
export const useRecords = () => useWeightTrackerStore(state => state.records);
export const useSettings = () => useWeightTrackerStore(state => state.settings);
export const useCurrentMetrics = () => useWeightTrackerStore(state => state.currentMetrics);
export const useIsLoading = () => useWeightTrackerStore(state => state.isLoading);
export const useError = () => useWeightTrackerStore(state => state.error);
export const useSelectedDate = () => useWeightTrackerStore(state => state.selectedDate);

// Action selectors
export const useActions = () => useWeightTrackerStore(state => ({
  initializeApp: state.initializeApp,
  loadRecords: state.loadRecords,
  loadSettings: state.loadSettings,
  saveRecord: state.saveRecord,
  updateSettings: state.updateSettings,
  deleteRecord: state.deleteRecord,
  setSelectedDate: state.setSelectedDate,
  clearError: state.clearError,
}));

// Computed selectors
export const useGatingFlags = () => useWeightTrackerStore(state => state.getGatingFlags());
export const useHasRecordForDate = (date: string) => useWeightTrackerStore(state => state.hasRecordForDate(date));
export const useRecordForDate = (date: string) => useWeightTrackerStore(state => state.getRecordForDate(date));
export const useLastRecord = () => useWeightTrackerStore(state => state.getLastRecord());
export const useRecordsInRange = (startDate: string, endDate: string) => 
  useWeightTrackerStore(state => state.getRecordsInRange(startDate, endDate));

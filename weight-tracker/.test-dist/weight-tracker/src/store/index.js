"use strict";
/**
 * Weight Tracker - State Management with Zustand
 * Manages application state including records, settings, and UI state
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.useRecordsInRange = exports.useLastRecord = exports.useRecordForDate = exports.useHasRecordForDate = exports.useGatingFlags = exports.useActions = exports.useSelectedDate = exports.useError = exports.useIsLoading = exports.useCurrentMetrics = exports.useSettings = exports.useRecords = exports.useWeightTrackerStore = void 0;
const zustand_1 = require("zustand");
const types_1 = require("../types");
const database_1 = require("../services/database");
const calculations_1 = require("../utils/calculations");
exports.useWeightTrackerStore = (0, zustand_1.create)((set, get) => ({
    // Initial state
    records: [],
    settings: types_1.DEFAULT_SETTINGS,
    currentMetrics: null,
    isLoading: false,
    error: null,
    selectedDate: new Date().toISOString().split('T')[0],
    // Actions
    initializeApp: async () => {
        set({ isLoading: true, error: null });
        try {
            await database_1.databaseService.initialize();
            await Promise.all([
                get().loadRecords(),
                get().loadSettings(),
            ]);
        }
        catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to initialize app' });
        }
        finally {
            set({ isLoading: false });
        }
    },
    loadRecords: async () => {
        try {
            const records = await database_1.databaseService.getAllDailyRecords();
            set({ records });
            // Calculate current metrics for today
            const today = new Date().toISOString().split('T')[0];
            const todayRecord = records.find(r => r.date === today);
            if (todayRecord) {
                const metrics = (0, calculations_1.calculateAllMetrics)(todayRecord, get().settings, records);
                set({ currentMetrics: metrics });
            }
        }
        catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to load records' });
        }
    },
    loadSettings: async () => {
        try {
            const settings = await database_1.databaseService.getSettings();
            if (settings) {
                set({ settings });
            }
        }
        catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to load settings' });
        }
    },
    saveRecord: async (record) => {
        set({ isLoading: true, error: null });
        try {
            // Check for outliers
            const lastRecord = get().getLastRecord();
            const isOutlier = (0, calculations_1.isWeightOutlier)(record.weight_lb, lastRecord);
            if (isOutlier) {
                record.flags.outlier_weight = true;
            }
            await database_1.databaseService.insertDailyRecord(record);
            // Reload records to get updated data
            await get().loadRecords();
            // Update current metrics if this is today's record
            const today = new Date().toISOString().split('T')[0];
            if (record.date === today) {
                const metrics = (0, calculations_1.calculateAllMetrics)(record, get().settings, get().records);
                set({ currentMetrics: metrics });
            }
        }
        catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to save record' });
        }
        finally {
            set({ isLoading: false });
        }
    },
    updateSettings: async (newSettings) => {
        set({ isLoading: true, error: null });
        try {
            const updatedSettings = { ...get().settings, ...newSettings };
            await database_1.databaseService.saveSettings(updatedSettings);
            set({ settings: updatedSettings });
            // Recalculate current metrics with new settings
            const today = new Date().toISOString().split('T')[0];
            const todayRecord = get().records.find(r => r.date === today);
            if (todayRecord) {
                const metrics = (0, calculations_1.calculateAllMetrics)(todayRecord, updatedSettings, get().records);
                set({ currentMetrics: metrics });
            }
        }
        catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to update settings' });
        }
        finally {
            set({ isLoading: false });
        }
    },
    deleteRecord: async (date) => {
        set({ isLoading: true, error: null });
        try {
            await database_1.databaseService.deleteDailyRecord(date);
            await get().loadRecords();
            // Update current metrics if we deleted today's record
            const today = new Date().toISOString().split('T')[0];
            if (date === today) {
                set({ currentMetrics: null });
            }
        }
        catch (error) {
            set({ error: error instanceof Error ? error.message : 'Failed to delete record' });
        }
        finally {
            set({ isLoading: false });
        }
    },
    setSelectedDate: (date) => {
        set({ selectedDate: date });
    },
    clearError: () => {
        set({ error: null });
    },
    // Computed values
    getGatingFlags: () => {
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
    getRecordForDate: (date) => {
        return get().records.find(r => r.date === date) || null;
    },
    hasRecordForDate: (date) => {
        return get().records.some(r => r.date === date);
    },
    getLastRecord: () => {
        const { records } = get();
        if (records.length === 0)
            return null;
        return records[records.length - 1];
    },
    getRecordsInRange: (startDate, endDate) => {
        return get().records.filter(r => r.date >= startDate && r.date <= endDate);
    },
}));
// Selectors for specific data
const useRecords = () => (0, exports.useWeightTrackerStore)(state => state.records);
exports.useRecords = useRecords;
const useSettings = () => (0, exports.useWeightTrackerStore)(state => state.settings);
exports.useSettings = useSettings;
const useCurrentMetrics = () => (0, exports.useWeightTrackerStore)(state => state.currentMetrics);
exports.useCurrentMetrics = useCurrentMetrics;
const useIsLoading = () => (0, exports.useWeightTrackerStore)(state => state.isLoading);
exports.useIsLoading = useIsLoading;
const useError = () => (0, exports.useWeightTrackerStore)(state => state.error);
exports.useError = useError;
const useSelectedDate = () => (0, exports.useWeightTrackerStore)(state => state.selectedDate);
exports.useSelectedDate = useSelectedDate;
// Action selectors
const useActions = () => (0, exports.useWeightTrackerStore)(state => ({
    initializeApp: state.initializeApp,
    loadRecords: state.loadRecords,
    loadSettings: state.loadSettings,
    saveRecord: state.saveRecord,
    updateSettings: state.updateSettings,
    deleteRecord: state.deleteRecord,
    setSelectedDate: state.setSelectedDate,
    clearError: state.clearError,
}));
exports.useActions = useActions;
// Computed selectors
const useGatingFlags = () => (0, exports.useWeightTrackerStore)(state => state.getGatingFlags());
exports.useGatingFlags = useGatingFlags;
const useHasRecordForDate = (date) => (0, exports.useWeightTrackerStore)(state => state.hasRecordForDate(date));
exports.useHasRecordForDate = useHasRecordForDate;
const useRecordForDate = (date) => (0, exports.useWeightTrackerStore)(state => state.getRecordForDate(date));
exports.useRecordForDate = useRecordForDate;
const useLastRecord = () => (0, exports.useWeightTrackerStore)(state => state.getLastRecord());
exports.useLastRecord = useLastRecord;
const useRecordsInRange = (startDate, endDate) => (0, exports.useWeightTrackerStore)(state => state.getRecordsInRange(startDate, endDate));
exports.useRecordsInRange = useRecordsInRange;

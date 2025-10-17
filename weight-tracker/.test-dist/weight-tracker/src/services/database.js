"use strict";
/**
 * Weight Tracker - Database Schema and Operations
 * SQLite database for storing daily records
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.databaseService = exports.DatabaseService = void 0;
const SQLite = __importStar(require("expo-sqlite"));
const DB_NAME = 'weight_tracker.db';
class DatabaseService {
    constructor() {
        this.db = null;
    }
    async initialize() {
        try {
            this.db = await SQLite.openDatabaseAsync(DB_NAME);
            await this.createTables();
        }
        catch (error) {
            console.error('Failed to initialize database:', error);
            throw error;
        }
    }
    async createTables() {
        if (!this.db)
            throw new Error('Database not initialized');
        // Create daily_records table
        await this.db.execAsync(`
      CREATE TABLE IF NOT EXISTS daily_records (
        date TEXT PRIMARY KEY,
        weight_lb REAL NOT NULL,
        height_in REAL NOT NULL,
        neck_in REAL NOT NULL,
        upper_waist_in REAL NOT NULL,
        lower_waist_in REAL NOT NULL,
        hips_in REAL NOT NULL,
        notes TEXT DEFAULT '',
        outlier_weight INTEGER DEFAULT 0,
        duplicate INTEGER DEFAULT 0,
        tags TEXT DEFAULT '[]',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
        // Create settings table
        await this.db.execAsync(`
      CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `);
        // Create indexes for better performance
        await this.db.execAsync(`
      CREATE INDEX IF NOT EXISTS idx_daily_records_date ON daily_records(date)
    `);
    }
    // Daily Records Operations
    async insertDailyRecord(record) {
        if (!this.db)
            throw new Error('Database not initialized');
        await this.db.runAsync(`INSERT OR REPLACE INTO daily_records 
       (date, weight_lb, height_in, neck_in, upper_waist_in, lower_waist_in, hips_in, notes, outlier_weight, duplicate, tags)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`, [
            record.date,
            record.weight_lb,
            record.height_in,
            record.neck_in,
            record.upper_waist_in,
            record.lower_waist_in,
            record.hips_in,
            record.notes,
            record.flags.outlier_weight ? 1 : 0,
            record.flags.duplicate ? 1 : 0,
            JSON.stringify(record.tags),
        ]);
    }
    async getDailyRecord(date) {
        if (!this.db)
            throw new Error('Database not initialized');
        const result = await this.db.getFirstAsync(`SELECT * FROM daily_records WHERE date = ?`, [date]);
        if (!result)
            return null;
        return this.mapRowToDailyRecord(result);
    }
    async getAllDailyRecords() {
        if (!this.db)
            throw new Error('Database not initialized');
        const results = await this.db.getAllAsync(`SELECT * FROM daily_records ORDER BY date ASC`);
        return results.map(row => this.mapRowToDailyRecord(row));
    }
    async getDailyRecordsInRange(startDate, endDate) {
        if (!this.db)
            throw new Error('Database not initialized');
        const results = await this.db.getAllAsync(`SELECT * FROM daily_records 
       WHERE date >= ? AND date <= ? 
       ORDER BY date ASC`, [startDate, endDate]);
        return results.map(row => this.mapRowToDailyRecord(row));
    }
    async deleteDailyRecord(date) {
        if (!this.db)
            throw new Error('Database not initialized');
        await this.db.runAsync(`DELETE FROM daily_records WHERE date = ?`, [date]);
    }
    async getLastDailyRecord() {
        if (!this.db)
            throw new Error('Database not initialized');
        const result = await this.db.getFirstAsync(`SELECT * FROM daily_records ORDER BY date DESC LIMIT 1`);
        if (!result)
            return null;
        return this.mapRowToDailyRecord(result);
    }
    async hasRecordForDate(date) {
        if (!this.db)
            throw new Error('Database not initialized');
        const result = await this.db.getFirstAsync(`SELECT 1 FROM daily_records WHERE date = ?`, [date]);
        return result !== null;
    }
    // Settings Operations
    async saveSettings(settings) {
        if (!this.db)
            throw new Error('Database not initialized');
        const settingsJson = JSON.stringify(settings);
        await this.db.runAsync(`INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)`, ['settings', settingsJson]);
    }
    async getSettings() {
        if (!this.db)
            throw new Error('Database not initialized');
        const result = await this.db.getFirstAsync(`SELECT value FROM settings WHERE key = ?`, ['settings']);
        if (!result)
            return null;
        return JSON.parse(result.value);
    }
    // Utility Methods
    mapRowToDailyRecord(row) {
        return {
            date: row.date,
            weight_lb: row.weight_lb,
            height_in: row.height_in,
            neck_in: row.neck_in,
            upper_waist_in: row.upper_waist_in,
            lower_waist_in: row.lower_waist_in,
            hips_in: row.hips_in,
            notes: row.notes || '',
            flags: {
                outlier_weight: Boolean(row.outlier_weight),
                duplicate: Boolean(row.duplicate),
            },
            tags: JSON.parse(row.tags || '[]'),
        };
    }
    // Database Management
    async clearAllData() {
        if (!this.db)
            throw new Error('Database not initialized');
        await this.db.execAsync(`DELETE FROM daily_records`);
        await this.db.execAsync(`DELETE FROM settings`);
    }
    async close() {
        if (this.db) {
            await this.db.closeAsync();
            this.db = null;
        }
    }
    // Statistics
    async getRecordCount() {
        if (!this.db)
            throw new Error('Database not initialized');
        const result = await this.db.getFirstAsync(`SELECT COUNT(*) as count FROM daily_records`);
        return result.count;
    }
    async getDateRange() {
        if (!this.db)
            throw new Error('Database not initialized');
        const result = await this.db.getFirstAsync(`SELECT MIN(date) as minDate, MAX(date) as maxDate FROM daily_records`);
        return {
            minDate: result.minDate,
            maxDate: result.maxDate,
        };
    }
}
exports.DatabaseService = DatabaseService;
// Singleton instance
exports.databaseService = new DatabaseService();

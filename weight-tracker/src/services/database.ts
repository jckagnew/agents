/**
 * Weight Tracker - Database Schema and Operations
 * SQLite database for storing daily records
 */

import * as SQLite from 'expo-sqlite';
import { DailyRecord, Settings } from '../types';

const DB_NAME = 'weight_tracker.db';

export class DatabaseService {
  private db: SQLite.SQLiteDatabase | null = null;

  async initialize(): Promise<void> {
    try {
      this.db = await SQLite.openDatabaseAsync(DB_NAME);
      await this.createTables();
    } catch (error) {
      console.error('Failed to initialize database:', error);
      throw error;
    }
  }

  private async createTables(): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

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
  async insertDailyRecord(record: DailyRecord): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    await this.db.runAsync(
      `INSERT OR REPLACE INTO daily_records 
       (date, weight_lb, height_in, neck_in, upper_waist_in, lower_waist_in, hips_in, notes, outlier_weight, duplicate, tags)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
      [
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
      ]
    );
  }

  async getDailyRecord(date: string): Promise<DailyRecord | null> {
    if (!this.db) throw new Error('Database not initialized');

    const result = await this.db.getFirstAsync(
      `SELECT * FROM daily_records WHERE date = ?`,
      [date]
    );

    if (!result) return null;

    return this.mapRowToDailyRecord(result as any);
  }

  async getAllDailyRecords(): Promise<DailyRecord[]> {
    if (!this.db) throw new Error('Database not initialized');

    const results = await this.db.getAllAsync(
      `SELECT * FROM daily_records ORDER BY date ASC`
    );

    return results.map(row => this.mapRowToDailyRecord(row as any));
  }

  async getDailyRecordsInRange(startDate: string, endDate: string): Promise<DailyRecord[]> {
    if (!this.db) throw new Error('Database not initialized');

    const results = await this.db.getAllAsync(
      `SELECT * FROM daily_records 
       WHERE date >= ? AND date <= ? 
       ORDER BY date ASC`,
      [startDate, endDate]
    );

    return results.map(row => this.mapRowToDailyRecord(row as any));
  }

  async deleteDailyRecord(date: string): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    await this.db.runAsync(
      `DELETE FROM daily_records WHERE date = ?`,
      [date]
    );
  }

  async getLastDailyRecord(): Promise<DailyRecord | null> {
    if (!this.db) throw new Error('Database not initialized');

    const result = await this.db.getFirstAsync(
      `SELECT * FROM daily_records ORDER BY date DESC LIMIT 1`
    );

    if (!result) return null;

    return this.mapRowToDailyRecord(result as any);
  }

  async hasRecordForDate(date: string): Promise<boolean> {
    if (!this.db) throw new Error('Database not initialized');

    const result = await this.db.getFirstAsync(
      `SELECT 1 FROM daily_records WHERE date = ?`,
      [date]
    );

    return result !== null;
  }

  // Settings Operations
  async saveSettings(settings: Settings): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    const settingsJson = JSON.stringify(settings);
    await this.db.runAsync(
      `INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)`,
      ['settings', settingsJson]
    );
  }

  async getSettings(): Promise<Settings | null> {
    if (!this.db) throw new Error('Database not initialized');

    const result = await this.db.getFirstAsync(
      `SELECT value FROM settings WHERE key = ?`,
      ['settings']
    );

    if (!result) return null;

    return JSON.parse((result as any).value);
  }

  // Utility Methods
  private mapRowToDailyRecord(row: any): DailyRecord {
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
  async clearAllData(): Promise<void> {
    if (!this.db) throw new Error('Database not initialized');

    await this.db.execAsync(`DELETE FROM daily_records`);
    await this.db.execAsync(`DELETE FROM settings`);
  }

  async close(): Promise<void> {
    if (this.db) {
      await this.db.closeAsync();
      this.db = null;
    }
  }

  // Statistics
  async getRecordCount(): Promise<number> {
    if (!this.db) throw new Error('Database not initialized');

    const result = await this.db.getFirstAsync(
      `SELECT COUNT(*) as count FROM daily_records`
    );

    return (result as any).count;
  }

  async getDateRange(): Promise<{ minDate: string | null; maxDate: string | null }> {
    if (!this.db) throw new Error('Database not initialized');

    const result = await this.db.getFirstAsync(
      `SELECT MIN(date) as minDate, MAX(date) as maxDate FROM daily_records`
    );

    return {
      minDate: (result as any).minDate,
      maxDate: (result as any).maxDate,
    };
  }
}

// Singleton instance
export const databaseService = new DatabaseService();

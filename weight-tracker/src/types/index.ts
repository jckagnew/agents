/**
 * Weight Tracker - Data Model and Types
 * Privacy-first weight tracker with trend clarity over daily noise
 */

export interface DailyRecord {
  date: string; // "YYYY-MM-DD"
  weight_lb: number;
  height_in: number; // Read from Settings, ignored if present in daily record
  neck_in: number;
  upper_waist_in: number;
  lower_waist_in: number;
  hips_in: number;
  notes: string;
  flags: {
    outlier_weight: boolean;
    duplicate: boolean;
  };
  tags: string[];
}

export interface Settings {
  plan: "free" | "pro";
  sex_for_formula: "male" | "female";
  height_in: number;
  unit_weight: "lb" | "kg" | "st";
  unit_length: "in" | "cm";
  target_bf_percent: number;
  smoothing_method: "7D_min4";
  tz_mode: "auto" | "manual";
  tz_manual: string;
}

export interface GatingFlags {
  allowMultipleEntriesPerDay: boolean;
  allowCustomBF: boolean;
  allowWHRTrend: boolean;
  allowGoalMoving: boolean;
  allowSmoothingChange: boolean;
  maxSavedCustomRanges: number;
  allowPhotoJournal: boolean;
  allowExport: boolean;
}

export interface CalculatedMetrics {
  navy_bf_percent: number | null;
  fat_mass_lb: number | null;
  lean_mass_lb: number | null;
  whr: number;
  whr_category: "Low" | "Moderate" | "High";
  smoothed_weight_7d: number | null;
  percent_change: number | null;
}

export interface TestFixture {
  date: string;
  weight_lb: number;
  neck_in: number;
  lower_waist_in: number;
  upper_waist_in: number;
  hips_in: number;
  navy_bf_percent: number;
  fat_lb: number;
  lean_lb: number;
  whr: number;
  weight_7d_sma: number | null;
  percent_change_smoothed: number | null;
}

// Unit conversion constants
export const UNIT_CONSTANTS = {
  KG_TO_LB: 2.20462,
  STONE_TO_LB: 14,
  IN_TO_CM: 2.54,
} as const;

// Default settings
export const DEFAULT_SETTINGS: Settings = {
  plan: "free",
  sex_for_formula: "male",
  height_in: 69,
  unit_weight: "lb",
  unit_length: "in",
  target_bf_percent: 20,
  smoothing_method: "7D_min4",
  tz_mode: "auto",
  tz_manual: "America/Chicago",
};

// Test fixtures for validation
export const TEST_FIXTURES: TestFixture[] = [
  {
    date: "2025-08-01",
    weight_lb: 270.4,
    neck_in: 17.0,
    lower_waist_in: 47.0,
    upper_waist_in: 45.0,
    hips_in: 48.5,
    navy_bf_percent: 35.0,
    fat_lb: 94.6,
    lean_lb: 175.8,
    whr: 0.97,
    weight_7d_sma: null,
    percent_change_smoothed: null,
  },
  {
    date: "2025-08-02",
    weight_lb: 270.1,
    neck_in: 16.9,
    lower_waist_in: 46.8,
    upper_waist_in: 44.9,
    hips_in: 48.5,
    navy_bf_percent: 34.9,
    fat_lb: 94.3,
    lean_lb: 175.8,
    whr: 0.96,
    weight_7d_sma: null,
    percent_change_smoothed: null,
  },
  {
    date: "2025-08-03",
    weight_lb: 269.9,
    neck_in: 17.0,
    lower_waist_in: 46.7,
    upper_waist_in: 44.8,
    hips_in: 48.4,
    navy_bf_percent: 34.6,
    fat_lb: 93.4,
    lean_lb: 176.5,
    whr: 0.96,
    weight_7d_sma: null,
    percent_change_smoothed: null,
  },
  {
    date: "2025-08-04",
    weight_lb: 269.4,
    neck_in: 16.9,
    lower_waist_in: 46.6,
    upper_waist_in: 44.6,
    hips_in: 48.4,
    navy_bf_percent: 34.6,
    fat_lb: 93.2,
    lean_lb: 176.2,
    whr: 0.96,
    weight_7d_sma: 269.9,
    percent_change_smoothed: 0.0,
  },
  {
    date: "2025-08-05",
    weight_lb: 269.6,
    neck_in: 16.8,
    lower_waist_in: 46.5,
    upper_waist_in: 44.7,
    hips_in: 48.3,
    navy_bf_percent: 34.6,
    fat_lb: 93.3,
    lean_lb: 176.3,
    whr: 0.96,
    weight_7d_sma: 269.9,
    percent_change_smoothed: -0.0,
  },
  {
    date: "2025-08-06",
    weight_lb: 268.9,
    neck_in: 16.8,
    lower_waist_in: 46.5,
    upper_waist_in: 44.5,
    hips_in: 48.3,
    navy_bf_percent: 34.6,
    fat_lb: 93.0,
    lean_lb: 175.9,
    whr: 0.96,
    weight_7d_sma: 269.7,
    percent_change_smoothed: -0.1,
  },
  {
    date: "2025-08-07",
    weight_lb: 268.4,
    neck_in: 16.8,
    lower_waist_in: 46.3,
    upper_waist_in: 44.4,
    hips_in: 48.2,
    navy_bf_percent: 34.4,
    fat_lb: 92.3,
    lean_lb: 176.1,
    whr: 0.96,
    weight_7d_sma: 269.5,
    percent_change_smoothed: -0.2,
  },
  {
    date: "2025-08-08",
    weight_lb: 268.2,
    neck_in: 16.7,
    lower_waist_in: 46.2,
    upper_waist_in: 44.3,
    hips_in: 48.1,
    navy_bf_percent: 34.4,
    fat_lb: 92.3,
    lean_lb: 175.9,
    whr: 0.96,
    weight_7d_sma: 269.2,
    percent_change_smoothed: -0.3,
  },
  {
    date: "2025-08-09",
    weight_lb: 267.9,
    neck_in: 16.7,
    lower_waist_in: 46.1,
    upper_waist_in: 44.2,
    hips_in: 48.1,
    navy_bf_percent: 34.3,
    fat_lb: 91.9,
    lean_lb: 176.0,
    whr: 0.96,
    weight_7d_sma: 268.9,
    percent_change_smoothed: -0.4,
  },
  {
    date: "2025-08-10",
    weight_lb: 267.5,
    neck_in: 16.7,
    lower_waist_in: 46.0,
    upper_waist_in: 44.0,
    hips_in: 48.0,
    navy_bf_percent: 34.1,
    fat_lb: 91.2,
    lean_lb: 176.3,
    whr: 0.96,
    weight_7d_sma: 268.6,
    percent_change_smoothed: -0.5,
  },
];

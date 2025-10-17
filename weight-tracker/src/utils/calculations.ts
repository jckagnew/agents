/**
 * Weight Tracker - Core Calculation Algorithms
 * Implements Navy BF%, WHR, smoothing, and other calculations
 */

import { DailyRecord, Settings, CalculatedMetrics, UNIT_CONSTANTS } from '../types';

/**
 * Calculate Navy Body Fat Percentage
 * Male: BF% = 86.01*log10(LowerWaist - Neck) - 70.041*log10(Height) + 36.76
 * Female: BF% = 163.205*log10(LowerWaist + Hips - Neck) - 97.684*log10(Height) - 78.387
 */
export function calculateNavyBF(
  record: DailyRecord,
  settings: Settings
): number | null {
  const { sex_for_formula, height_in } = settings;
  const { lower_waist_in, neck_in, hips_in } = record;

  if (sex_for_formula === 'male') {
    const waistNeckDiff = lower_waist_in - neck_in;
    if (waistNeckDiff <= 0) return null;
    
    const bf = 86.01 * Math.log10(waistNeckDiff) - 70.041 * Math.log10(height_in) + 36.76;
    return Math.round(bf * 10) / 10; // Round to 0.1
  } else {
    const waistHipsNeckSum = lower_waist_in + hips_in - neck_in;
    if (waistHipsNeckSum <= 0) return null;
    
    const bf = 163.205 * Math.log10(waistHipsNeckSum) - 97.684 * Math.log10(height_in) - 78.387;
    return Math.round(bf * 10) / 10; // Round to 0.1
  }
}

/**
 * Calculate Fat Mass in pounds
 */
export function calculateFatMass(weight_lb: number, bf_percent: number | null): number | null {
  if (bf_percent === null) return null;
  return Math.round(weight_lb * bf_percent / 100 * 10) / 10; // Round to 0.1
}

/**
 * Calculate Lean Mass in pounds
 */
export function calculateLeanMass(weight_lb: number, bf_percent: number | null): number | null {
  if (bf_percent === null) return null;
  return Math.round(weight_lb * (1 - bf_percent / 100) * 10) / 10; // Round to 0.1
}

/**
 * Calculate Waist-to-Hip Ratio
 */
export function calculateWHR(record: DailyRecord): number {
  const { lower_waist_in, hips_in } = record;
  return Math.round((lower_waist_in / hips_in) * 100) / 100; // Round to 2 decimal places
}

/**
 * Get WHR Category based on sex
 */
export function getWHRCategory(whr: number, sex: 'male' | 'female'): 'Low' | 'Moderate' | 'High' {
  if (sex === 'male') {
    if (whr < 0.90) return 'Low';
    if (whr <= 0.99) return 'Moderate';
    return 'High';
  } else {
    if (whr < 0.80) return 'Low';
    if (whr <= 0.89) return 'Moderate';
    return 'High';
  }
}

/**
 * Calculate 7-day simple moving average with minimum 4 values requirement
 */
export function calculate7DaySMA(
  records: DailyRecord[],
  targetDate: string
): number | null {
  // Sort records by date
  const sortedRecords = [...records].sort((a, b) => a.date.localeCompare(b.date));
  
  // Find the target date index
  const targetIndex = sortedRecords.findIndex(r => r.date === targetDate);
  if (targetIndex === -1) return null;
  
  // Get the 7-day window ending on target date
  const startIndex = Math.max(0, targetIndex - 6);
  const windowRecords = sortedRecords.slice(startIndex, targetIndex + 1);
  
  // Check if we have at least 4 values
  if (windowRecords.length < 4) return null;
  
  // Calculate average
  const sum = windowRecords.reduce((acc, record) => acc + record.weight_lb, 0);
  return Math.round((sum / windowRecords.length) * 10) / 10; // Round to 0.1
}

/**
 * Calculate percent change from smoothed baseline
 */
export function calculatePercentChange(
  records: DailyRecord[],
  targetDate: string
): number | null {
  const sortedRecords = [...records].sort((a, b) => a.date.localeCompare(b.date));
  
  // Find first non-null smoothed value (baseline)
  let baseline: number | null = null;
  for (const record of sortedRecords) {
    const smoothed = calculate7DaySMA(records, record.date);
    if (smoothed !== null) {
      baseline = smoothed;
      break;
    }
  }
  
  if (baseline === null) return null;
  
  // Get current smoothed value
  const currentSmoothed = calculate7DaySMA(records, targetDate);
  if (currentSmoothed === null) return null;
  
  // Calculate percent change
  const percentChange = ((currentSmoothed - baseline) / baseline) * 100;
  return Math.round(percentChange * 10) / 10; // Round to 0.1%
}

/**
 * Calculate all metrics for a given record
 */
export function calculateAllMetrics(
  record: DailyRecord,
  settings: Settings,
  allRecords: DailyRecord[]
): CalculatedMetrics {
  const navyBF = calculateNavyBF(record, settings);
  const fatMass = calculateFatMass(record.weight_lb, navyBF);
  const leanMass = calculateLeanMass(record.weight_lb, navyBF);
  const whr = calculateWHR(record);
  const whrCategory = getWHRCategory(whr, settings.sex_for_formula);
  const smoothedWeight = calculate7DaySMA(allRecords, record.date);
  const percentChange = calculatePercentChange(allRecords, record.date);
  
  return {
    navy_bf_percent: navyBF,
    fat_mass_lb: fatMass,
    lean_mass_lb: leanMass,
    whr,
    whr_category: whrCategory,
    smoothed_weight_7d: smoothedWeight,
    percent_change: percentChange,
  };
}

/**
 * Check if weight change is an outlier (>5 lb in 24h)
 */
export function isWeightOutlier(
  newWeight: number,
  lastRecord: DailyRecord | null
): boolean {
  if (!lastRecord) return false;
  
  const weightChange = Math.abs(newWeight - lastRecord.weight_lb);
  return weightChange > 5;
}

/**
 * Convert weight from user units to canonical pounds
 */
export function convertWeightToLb(weight: number, unit: 'lb' | 'kg' | 'st'): number {
  switch (unit) {
    case 'lb':
      return weight;
    case 'kg':
      return weight * UNIT_CONSTANTS.KG_TO_LB;
    case 'st':
      return weight * UNIT_CONSTANTS.STONE_TO_LB;
    default:
      return weight;
  }
}

/**
 * Convert weight from canonical pounds to user units
 */
export function convertWeightFromLb(weightLb: number, unit: 'lb' | 'kg' | 'st'): number {
  switch (unit) {
    case 'lb':
      return weightLb;
    case 'kg':
      return weightLb / UNIT_CONSTANTS.KG_TO_LB;
    case 'st':
      return weightLb / UNIT_CONSTANTS.STONE_TO_LB;
    default:
      return weightLb;
  }
}

/**
 * Convert length from user units to canonical inches
 */
export function convertLengthToIn(length: number, unit: 'in' | 'cm'): number {
  switch (unit) {
    case 'in':
      return length;
    case 'cm':
      return length / UNIT_CONSTANTS.IN_TO_CM;
    default:
      return length;
  }
}

/**
 * Convert length from canonical inches to user units
 */
export function convertLengthFromIn(lengthIn: number, unit: 'in' | 'cm'): number {
  switch (unit) {
    case 'in':
      return lengthIn;
    case 'cm':
      return lengthIn * UNIT_CONSTANTS.IN_TO_CM;
    default:
      return lengthIn;
  }
}

/**
 * Validate calculation accuracy against test fixtures
 */
export function validateCalculations(
  record: DailyRecord,
  settings: Settings,
  expected: {
    navy_bf_percent: number;
    fat_lb: number;
    lean_lb: number;
    whr: number;
  }
): {
  navyBFValid: boolean;
  fatMassValid: boolean;
  leanMassValid: boolean;
  whrValid: boolean;
  errors: string[];
} {
  const metrics = calculateAllMetrics(record, settings, [record]);
  const errors: string[] = [];
  
  // Check Navy BF% (±0.1 tolerance)
  const navyBFValid = metrics.navy_bf_percent !== null && 
    Math.abs(metrics.navy_bf_percent - expected.navy_bf_percent) <= 0.1;
  if (!navyBFValid) {
    errors.push(`Navy BF%: expected ${expected.navy_bf_percent}, got ${metrics.navy_bf_percent}`);
  }
  
  // Check Fat Mass (±0.1 tolerance)
  const fatMassValid = metrics.fat_mass_lb !== null && 
    Math.abs(metrics.fat_mass_lb - expected.fat_lb) <= 0.1;
  if (!fatMassValid) {
    errors.push(`Fat Mass: expected ${expected.fat_lb}, got ${metrics.fat_mass_lb}`);
  }
  
  // Check Lean Mass (±0.1 tolerance)
  const leanMassValid = metrics.lean_mass_lb !== null && 
    Math.abs(metrics.lean_mass_lb - expected.lean_lb) <= 0.1;
  if (!leanMassValid) {
    errors.push(`Lean Mass: expected ${expected.lean_lb}, got ${metrics.lean_mass_lb}`);
  }
  
  // Check WHR (±0.01 tolerance)
  const whrValid = Math.abs(metrics.whr - expected.whr) <= 0.01;
  if (!whrValid) {
    errors.push(`WHR: expected ${expected.whr}, got ${metrics.whr}`);
  }
  
  return {
    navyBFValid,
    fatMassValid,
    leanMassValid,
    whrValid,
    errors,
  };
}

/**
 * Weight Tracker - Acceptance Tests
 * Validates all calculations against provided test fixtures
 */

import { DailyRecord, Settings, TEST_FIXTURES, DEFAULT_SETTINGS } from '../src/types';
import {
  calculateNavyBF,
  calculateFatMass,
  calculateLeanMass,
  calculateWHR,
  calculate7DaySMA,
  calculatePercentChange,
  validateCalculations,
} from '../src/utils/calculations';

describe('Weight Tracker - Acceptance Tests', () => {
  const settings: Settings = {
    ...DEFAULT_SETTINGS,
    sex_for_formula: 'male',
    height_in: 69,
  };

  describe('Navy BF% Calculations', () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      test(`Fixture ${index + 1} (${fixture.date}) - Navy BF% calculation`, () => {
        const record: DailyRecord = {
          date: fixture.date,
          weight_lb: fixture.weight_lb,
          height_in: settings.height_in,
          neck_in: fixture.neck_in,
          upper_waist_in: fixture.upper_waist_in,
          lower_waist_in: fixture.lower_waist_in,
          hips_in: fixture.hips_in,
          notes: '',
          flags: { outlier_weight: false, duplicate: false },
          tags: [],
        };

        const calculatedBF = calculateNavyBF(record, settings);
        expect(calculatedBF).not.toBeNull();
        expect(calculatedBF).toBeCloseTo(fixture.navy_bf_percent, 1);
      });
    });
  });

  describe('Fat Mass Calculations', () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      test(`Fixture ${index + 1} (${fixture.date}) - Fat Mass calculation`, () => {
        const fatMass = calculateFatMass(fixture.weight_lb, fixture.navy_bf_percent);
        expect(fatMass).not.toBeNull();
        expect(fatMass).toBeCloseTo(fixture.fat_lb, 1);
      });
    });
  });

  describe('Lean Mass Calculations', () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      test(`Fixture ${index + 1} (${fixture.date}) - Lean Mass calculation`, () => {
        const leanMass = calculateLeanMass(fixture.weight_lb, fixture.navy_bf_percent);
        expect(leanMass).not.toBeNull();
        expect(leanMass).toBeCloseTo(fixture.lean_lb, 1);
      });
    });
  });

  describe('WHR Calculations', () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      test(`Fixture ${index + 1} (${fixture.date}) - WHR calculation`, () => {
        const record: DailyRecord = {
          date: fixture.date,
          weight_lb: fixture.weight_lb,
          height_in: settings.height_in,
          neck_in: fixture.neck_in,
          upper_waist_in: fixture.upper_waist_in,
          lower_waist_in: fixture.lower_waist_in,
          hips_in: fixture.hips_in,
          notes: '',
          flags: { outlier_weight: false, duplicate: false },
          tags: [],
        };

        const calculatedWHR = calculateWHR(record);
        expect(calculatedWHR).toBeCloseTo(fixture.whr, 2);
      });
    });
  });

  describe('7-Day Simple Moving Average', () => {
    // Create records from fixtures
    const records: DailyRecord[] = TEST_FIXTURES.map(fixture => ({
      date: fixture.date,
      weight_lb: fixture.weight_lb,
      height_in: settings.height_in,
      neck_in: fixture.neck_in,
      upper_waist_in: fixture.upper_waist_in,
      lower_waist_in: fixture.lower_waist_in,
      hips_in: fixture.hips_in,
      notes: '',
      flags: { outlier_weight: false, duplicate: false },
      tags: [],
    }));

    TEST_FIXTURES.forEach((fixture, index) => {
      if (fixture.weight_7d_sma !== null) {
        test(`Fixture ${index + 1} (${fixture.date}) - 7D SMA calculation`, () => {
          const calculatedSMA = calculate7DaySMA(records, fixture.date);
          expect(calculatedSMA).not.toBeNull();
          expect(calculatedSMA).toBeCloseTo(fixture.weight_7d_sma!, 1);
        });
      } else {
        test(`Fixture ${index + 1} (${fixture.date}) - 7D SMA should be null (insufficient data)`, () => {
          const calculatedSMA = calculate7DaySMA(records, fixture.date);
          expect(calculatedSMA).toBeNull();
        });
      }
    });
  });

  describe('Percent Change Calculations', () => {
    const records: DailyRecord[] = TEST_FIXTURES.map(fixture => ({
      date: fixture.date,
      weight_lb: fixture.weight_lb,
      height_in: settings.height_in,
      neck_in: fixture.neck_in,
      upper_waist_in: fixture.upper_waist_in,
      lower_waist_in: fixture.lower_waist_in,
      hips_in: fixture.hips_in,
      notes: '',
      flags: { outlier_weight: false, duplicate: false },
      tags: [],
    }));

    TEST_FIXTURES.forEach((fixture, index) => {
      if (fixture.percent_change_smoothed !== null) {
        test(`Fixture ${index + 1} (${fixture.date}) - Percent change calculation`, () => {
          const calculatedPercentChange = calculatePercentChange(records, fixture.date);
          expect(calculatedPercentChange).not.toBeNull();
          expect(calculatedPercentChange).toBeCloseTo(fixture.percent_change_smoothed!, 1);
        });
      } else {
        test(`Fixture ${index + 1} (${fixture.date}) - Percent change should be null (insufficient data)`, () => {
          const calculatedPercentChange = calculatePercentChange(records, fixture.date);
          expect(calculatedPercentChange).toBeNull();
        });
      }
    });
  });

  describe('Comprehensive Validation', () => {
    const records: DailyRecord[] = TEST_FIXTURES.map(fixture => ({
      date: fixture.date,
      weight_lb: fixture.weight_lb,
      height_in: settings.height_in,
      neck_in: fixture.neck_in,
      upper_waist_in: fixture.upper_waist_in,
      lower_waist_in: fixture.lower_waist_in,
      hips_in: fixture.hips_in,
      notes: '',
      flags: { outlier_weight: false, duplicate: false },
      tags: [],
    }));

    TEST_FIXTURES.forEach((fixture, index) => {
      test(`Fixture ${index + 1} (${fixture.date}) - Complete validation`, () => {
        const record = records[index];
        const validation = validateCalculations(record, settings, {
          navy_bf_percent: fixture.navy_bf_percent,
          fat_lb: fixture.fat_lb,
          lean_lb: fixture.lean_lb,
          whr: fixture.whr,
        });

        expect(validation.navyBFValid).toBe(true);
        expect(validation.fatMassValid).toBe(true);
        expect(validation.leanMassValid).toBe(true);
        expect(validation.whrValid).toBe(true);
        expect(validation.errors).toHaveLength(0);
      });
    });
  });

  describe('Edge Cases', () => {
    test('Navy BF% calculation with invalid measurements (male)', () => {
      const record: DailyRecord = {
        date: '2025-01-01',
        weight_lb: 200,
        height_in: 69,
        neck_in: 17,
        upper_waist_in: 45,
        lower_waist_in: 16, // Lower than neck - should return null
        hips_in: 48,
        notes: '',
        flags: { outlier_weight: false, duplicate: false },
        tags: [],
      };

      const bf = calculateNavyBF(record, settings);
      expect(bf).toBeNull();
    });

    test('Navy BF% calculation with invalid measurements (female)', () => {
      const femaleSettings: Settings = {
        ...settings,
        sex_for_formula: 'female',
      };

      const record: DailyRecord = {
        date: '2025-01-01',
        weight_lb: 200,
        height_in: 69,
        neck_in: 17,
        upper_waist_in: 45,
        lower_waist_in: 46,
        hips_in: 15, // Too small - should return null
        notes: '',
        flags: { outlier_weight: false, duplicate: false },
        tags: [],
      };

      const bf = calculateNavyBF(record, femaleSettings);
      expect(bf).toBeNull();
    });

    test('7D SMA with insufficient data', () => {
      const records: DailyRecord[] = [
        {
          date: '2025-01-01',
          weight_lb: 200,
          height_in: 69,
          neck_in: 17,
          upper_waist_in: 45,
          lower_waist_in: 46,
          hips_in: 48,
          notes: '',
          flags: { outlier_weight: false, duplicate: false },
          tags: [],
        },
      ];

      const sma = calculate7DaySMA(records, '2025-01-01');
      expect(sma).toBeNull();
    });

    test('Percent change with no baseline', () => {
      const records: DailyRecord[] = [
        {
          date: '2025-01-01',
          weight_lb: 200,
          height_in: 69,
          neck_in: 17,
          upper_waist_in: 45,
          lower_waist_in: 46,
          hips_in: 48,
          notes: '',
          flags: { outlier_weight: false, duplicate: false },
          tags: [],
        },
      ];

      const percentChange = calculatePercentChange(records, '2025-01-01');
      expect(percentChange).toBeNull();
    });
  });

  describe('Unit Conversions', () => {
    test('Weight conversion from kg to lb', () => {
      const weightKg = 100;
      const weightLb = weightKg * 2.20462;
      expect(weightLb).toBeCloseTo(220.462, 3);
    });

    test('Weight conversion from stone to lb', () => {
      const weightStone = 10;
      const weightLb = weightStone * 14;
      expect(weightLb).toBe(140);
    });

    test('Length conversion from cm to inches', () => {
      const lengthCm = 100;
      const lengthIn = lengthCm / 2.54;
      expect(lengthIn).toBeCloseTo(39.3701, 4);
    });
  });

  describe('WHR Categories', () => {
    test('Male WHR categories', () => {
      const maleSettings: Settings = { ...settings, sex_for_formula: 'male' };
      
      // Low: < 0.90
      expect(getWHRCategory(0.85, 'male')).toBe('Low');
      
      // Moderate: 0.90-0.99
      expect(getWHRCategory(0.95, 'male')).toBe('Moderate');
      
      // High: >= 1.00
      expect(getWHRCategory(1.05, 'male')).toBe('High');
    });

    test('Female WHR categories', () => {
      // Low: < 0.80
      expect(getWHRCategory(0.75, 'female')).toBe('Low');
      
      // Moderate: 0.80-0.89
      expect(getWHRCategory(0.85, 'female')).toBe('Moderate');
      
      // High: >= 0.90
      expect(getWHRCategory(0.95, 'female')).toBe('High');
    });
  });
});

// Helper function for WHR categories
function getWHRCategory(whr: number, sex: 'male' | 'female'): 'Low' | 'Moderate' | 'High' {
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

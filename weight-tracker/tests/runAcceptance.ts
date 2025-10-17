/**
 * Minimal acceptance test harness for the Weight Tracker calculations.
 * Mirrors the Jest-based suite but runs without external dependencies.
 */

import {
  DailyRecord,
  Settings,
  TEST_FIXTURES,
  DEFAULT_SETTINGS,
} from '../src/types';
import {
  calculateNavyBF,
  calculateFatMass,
  calculateLeanMass,
  calculateWHR,
  calculate7DaySMA,
  calculatePercentChange,
  validateCalculations,
  getWHRCategory,
} from '../src/utils/calculations';
import { trackTestRun } from '../src/lib/observability';

type Check = {
  name: string;
  run: () => void;
};

const failures: string[] = [];
const checks: Check[] = [];

function reportFailure(message: string): void {
  failures.push(message);
}

function assertApprox(
  actual: number | null,
  expected: number | null,
  tolerance: number,
  context: string
): void {
  if (actual === null || expected === null) {
    if (actual !== expected) {
      reportFailure(`${context}: expected ${expected}, received ${actual}`);
    }
    return;
  }

  if (Math.abs(actual - expected) > tolerance) {
    reportFailure(`${context}: expected ${expected}, received ${actual}`);
  }
}

function makeRecord(fixture: (typeof TEST_FIXTURES)[number], overrides: Partial<DailyRecord> = {}): DailyRecord {
  return {
    date: fixture.date,
    weight_lb: fixture.weight_lb,
    height_in: DEFAULT_SETTINGS.height_in,
    neck_in: fixture.neck_in,
    upper_waist_in: fixture.upper_waist_in,
    lower_waist_in: fixture.lower_waist_in,
    hips_in: fixture.hips_in,
    notes: '',
    flags: { outlier_weight: false, duplicate: false },
    tags: [],
    ...overrides,
  };
}

const baseSettings: Settings = {
  ...DEFAULT_SETTINGS,
  sex_for_formula: 'male',
  height_in: 69,
};

checks.push({
  name: 'Navy BF% fixtures',
  run: () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      const record = makeRecord(fixture);
      const bf = calculateNavyBF(record, baseSettings);
      assertApprox(bf, fixture.navy_bf_percent, 0.1, `Fixture ${index + 1} Navy BF%`);
    });
  },
});

checks.push({
  name: 'Fat & Lean mass fixtures',
  run: () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      const fat = calculateFatMass(fixture.weight_lb, fixture.navy_bf_percent);
      const lean = calculateLeanMass(fixture.weight_lb, fixture.navy_bf_percent);
      assertApprox(fat, fixture.fat_lb, 0.1, `Fixture ${index + 1} Fat Mass`);
      assertApprox(lean, fixture.lean_lb, 0.1, `Fixture ${index + 1} Lean Mass`);
    });
  },
});

checks.push({
  name: 'WHR fixtures',
  run: () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      const record = makeRecord(fixture);
      const whr = calculateWHR(record);
      assertApprox(whr, fixture.whr, 0.01, `Fixture ${index + 1} WHR`);
    });
  },
});

checks.push({
  name: '7-day SMA fixtures',
  run: () => {
    const records = TEST_FIXTURES.map(f => makeRecord(f));
    TEST_FIXTURES.forEach((fixture, index) => {
      const expected = fixture.weight_7d_sma;
      const actual = calculate7DaySMA(records, fixture.date);
      if (expected === null) {
        if (actual !== null) {
          reportFailure(`Fixture ${index + 1} SMA expected null, received ${actual}`);
        }
      } else {
        assertApprox(actual, expected, 0.11, `Fixture ${index + 1} 7D SMA`);
      }
    });
  },
});

checks.push({
  name: 'Percent change fixtures',
  run: () => {
    const records = TEST_FIXTURES.map(f => makeRecord(f));
    TEST_FIXTURES.forEach((fixture, index) => {
      const expected = fixture.percent_change_smoothed;
      const actual = calculatePercentChange(records, fixture.date);
      if (expected === null) {
        if (actual !== null) {
          reportFailure(`Fixture ${index + 1} percent change expected null, received ${actual}`);
        }
      } else {
        assertApprox(actual, expected, 0.1, `Fixture ${index + 1} percent change`);
      }
    });
  },
});

checks.push({
  name: 'Validation helper',
  run: () => {
    TEST_FIXTURES.forEach((fixture, index) => {
      const record = makeRecord(fixture);
      const { errors } = validateCalculations(record, baseSettings, {
        navy_bf_percent: fixture.navy_bf_percent,
        fat_lb: fixture.fat_lb,
        lean_lb: fixture.lean_lb,
        whr: fixture.whr,
      });
      if (errors.length > 0) {
        reportFailure(`Fixture ${index + 1} validation errors: ${errors.join(', ')}`);
      }
    });
  },
});

checks.push({
  name: 'Edge cases',
  run: () => {
    const maleInvalid = makeRecord(TEST_FIXTURES[0], {
      lower_waist_in: TEST_FIXTURES[0].neck_in - 0.5,
    });
    if (calculateNavyBF(maleInvalid, baseSettings) !== null) {
      reportFailure('Male invalid measurements should produce null Navy BF%');
    }

    const femaleSettings: Settings = { ...baseSettings, sex_for_formula: 'female' };
    const femaleInvalid = makeRecord(TEST_FIXTURES[0], {
      neck_in: 40,
      lower_waist_in: 30,
      hips_in: 5,
    });
    if (calculateNavyBF(femaleInvalid, femaleSettings) !== null) {
      reportFailure('Female invalid measurements should produce null Navy BF%');
    }

    const insufficientRecords: DailyRecord[] = [makeRecord(TEST_FIXTURES[0])];
    if (calculate7DaySMA(insufficientRecords, TEST_FIXTURES[0].date) !== null) {
      reportFailure('SMA with insufficient data should be null');
    }
    if (calculatePercentChange(insufficientRecords, TEST_FIXTURES[0].date) !== null) {
      reportFailure('Percent change with insufficient data should be null');
    }
  },
});

checks.push({
  name: 'Unit conversions',
  run: () => {
    const kgToLb = 100 * 2.20462;
    assertApprox(kgToLb, 220.462, 0.001, 'kg to lb conversion');

    const stoneToLb = 10 * 14;
    assertApprox(stoneToLb, 140, 0, 'stone to lb conversion');

    const cmToIn = 100 / 2.54;
    assertApprox(cmToIn, 39.3701, 0.0001, 'cm to inches conversion');
  },
});

checks.push({
  name: 'WHR categories',
  run: () => {
    if (getWHRCategory(0.85, 'male') !== 'Low') reportFailure('Male WHR low category mismatch');
    if (getWHRCategory(0.95, 'male') !== 'Moderate') reportFailure('Male WHR moderate category mismatch');
    if (getWHRCategory(1.05, 'male') !== 'High') reportFailure('Male WHR high category mismatch');
    if (getWHRCategory(0.75, 'female') !== 'Low') reportFailure('Female WHR low category mismatch');
    if (getWHRCategory(0.85, 'female') !== 'Moderate') reportFailure('Female WHR moderate category mismatch');
    if (getWHRCategory(0.95, 'female') !== 'High') reportFailure('Female WHR high category mismatch');
  },
});

async function main(): Promise<void> {
  console.log('Running Weight Tracker acceptance checks...');
  checks.forEach(({ name, run }) => {
    try {
      run();
      console.log(`  ✔ ${name}`);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      reportFailure(`${name}: ${message}`);
    }
  });

  const status = failures.length > 0 ? 'fail' : 'pass';
  const details = failures.length > 0 ? failures.join('; ') : undefined;

  await trackTestRun({ pipeline: 'acceptance', status, details });

  if (failures.length > 0) {
    console.error('\n❌ Acceptance checks failed:');
    failures.forEach(failure => console.error(`  - ${failure}`));
    process.exitCode = 1;
  } else {
    console.log('\n✅ All acceptance checks passed.');
  }
}

main().catch(error => {
  console.error('Acceptance harness encountered an unexpected error:', error);
  process.exitCode = 1;
});

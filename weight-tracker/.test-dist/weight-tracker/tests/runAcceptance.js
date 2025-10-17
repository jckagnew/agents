"use strict";
/**
 * Minimal acceptance test harness for the Weight Tracker calculations.
 * Mirrors the Jest-based suite but runs without external dependencies.
 */
Object.defineProperty(exports, "__esModule", { value: true });
const types_1 = require("../src/types");
const calculations_1 = require("../src/utils/calculations");
const observability_1 = require("../src/lib/observability");
const failures = [];
const checks = [];
function reportFailure(message) {
    failures.push(message);
}
function assertApprox(actual, expected, tolerance, context) {
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
function makeRecord(fixture, overrides = {}) {
    return {
        date: fixture.date,
        weight_lb: fixture.weight_lb,
        height_in: types_1.DEFAULT_SETTINGS.height_in,
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
const baseSettings = {
    ...types_1.DEFAULT_SETTINGS,
    sex_for_formula: 'male',
    height_in: 69,
};
checks.push({
    name: 'Navy BF% fixtures',
    run: () => {
        types_1.TEST_FIXTURES.forEach((fixture, index) => {
            const record = makeRecord(fixture);
            const bf = (0, calculations_1.calculateNavyBF)(record, baseSettings);
            assertApprox(bf, fixture.navy_bf_percent, 0.1, `Fixture ${index + 1} Navy BF%`);
        });
    },
});
checks.push({
    name: 'Fat & Lean mass fixtures',
    run: () => {
        types_1.TEST_FIXTURES.forEach((fixture, index) => {
            const fat = (0, calculations_1.calculateFatMass)(fixture.weight_lb, fixture.navy_bf_percent);
            const lean = (0, calculations_1.calculateLeanMass)(fixture.weight_lb, fixture.navy_bf_percent);
            assertApprox(fat, fixture.fat_lb, 0.1, `Fixture ${index + 1} Fat Mass`);
            assertApprox(lean, fixture.lean_lb, 0.1, `Fixture ${index + 1} Lean Mass`);
        });
    },
});
checks.push({
    name: 'WHR fixtures',
    run: () => {
        types_1.TEST_FIXTURES.forEach((fixture, index) => {
            const record = makeRecord(fixture);
            const whr = (0, calculations_1.calculateWHR)(record);
            assertApprox(whr, fixture.whr, 0.01, `Fixture ${index + 1} WHR`);
        });
    },
});
checks.push({
    name: '7-day SMA fixtures',
    run: () => {
        const records = types_1.TEST_FIXTURES.map(f => makeRecord(f));
        types_1.TEST_FIXTURES.forEach((fixture, index) => {
            const expected = fixture.weight_7d_sma;
            const actual = (0, calculations_1.calculate7DaySMA)(records, fixture.date);
            if (expected === null) {
                if (actual !== null) {
                    reportFailure(`Fixture ${index + 1} SMA expected null, received ${actual}`);
                }
            }
            else {
                assertApprox(actual, expected, 0.11, `Fixture ${index + 1} 7D SMA`);
            }
        });
    },
});
checks.push({
    name: 'Percent change fixtures',
    run: () => {
        const records = types_1.TEST_FIXTURES.map(f => makeRecord(f));
        types_1.TEST_FIXTURES.forEach((fixture, index) => {
            const expected = fixture.percent_change_smoothed;
            const actual = (0, calculations_1.calculatePercentChange)(records, fixture.date);
            if (expected === null) {
                if (actual !== null) {
                    reportFailure(`Fixture ${index + 1} percent change expected null, received ${actual}`);
                }
            }
            else {
                assertApprox(actual, expected, 0.1, `Fixture ${index + 1} percent change`);
            }
        });
    },
});
checks.push({
    name: 'Validation helper',
    run: () => {
        types_1.TEST_FIXTURES.forEach((fixture, index) => {
            const record = makeRecord(fixture);
            const { errors } = (0, calculations_1.validateCalculations)(record, baseSettings, {
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
        const maleInvalid = makeRecord(types_1.TEST_FIXTURES[0], {
            lower_waist_in: types_1.TEST_FIXTURES[0].neck_in - 0.5,
        });
        if ((0, calculations_1.calculateNavyBF)(maleInvalid, baseSettings) !== null) {
            reportFailure('Male invalid measurements should produce null Navy BF%');
        }
        const femaleSettings = { ...baseSettings, sex_for_formula: 'female' };
        const femaleInvalid = makeRecord(types_1.TEST_FIXTURES[0], {
            neck_in: 40,
            lower_waist_in: 30,
            hips_in: 5,
        });
        if ((0, calculations_1.calculateNavyBF)(femaleInvalid, femaleSettings) !== null) {
            reportFailure('Female invalid measurements should produce null Navy BF%');
        }
        const insufficientRecords = [makeRecord(types_1.TEST_FIXTURES[0])];
        if ((0, calculations_1.calculate7DaySMA)(insufficientRecords, types_1.TEST_FIXTURES[0].date) !== null) {
            reportFailure('SMA with insufficient data should be null');
        }
        if ((0, calculations_1.calculatePercentChange)(insufficientRecords, types_1.TEST_FIXTURES[0].date) !== null) {
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
        if ((0, calculations_1.getWHRCategory)(0.85, 'male') !== 'Low')
            reportFailure('Male WHR low category mismatch');
        if ((0, calculations_1.getWHRCategory)(0.95, 'male') !== 'Moderate')
            reportFailure('Male WHR moderate category mismatch');
        if ((0, calculations_1.getWHRCategory)(1.05, 'male') !== 'High')
            reportFailure('Male WHR high category mismatch');
        if ((0, calculations_1.getWHRCategory)(0.75, 'female') !== 'Low')
            reportFailure('Female WHR low category mismatch');
        if ((0, calculations_1.getWHRCategory)(0.85, 'female') !== 'Moderate')
            reportFailure('Female WHR moderate category mismatch');
        if ((0, calculations_1.getWHRCategory)(0.95, 'female') !== 'High')
            reportFailure('Female WHR high category mismatch');
    },
});
async function main() {
    console.log('Running Weight Tracker acceptance checks...');
    checks.forEach(({ name, run }) => {
        try {
            run();
            console.log(`  ✔ ${name}`);
        }
        catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            reportFailure(`${name}: ${message}`);
        }
    });
    const status = failures.length > 0 ? 'fail' : 'pass';
    const details = failures.length > 0 ? failures.join('; ') : undefined;
    await (0, observability_1.trackTestRun)({ pipeline: 'acceptance', status, details });
    if (failures.length > 0) {
        console.error('\n❌ Acceptance checks failed:');
        failures.forEach(failure => console.error(`  - ${failure}`));
        process.exitCode = 1;
    }
    else {
        console.log('\n✅ All acceptance checks passed.');
    }
}
main().catch(error => {
    console.error('Acceptance harness encountered an unexpected error:', error);
    process.exitCode = 1;
});

#!/usr/bin/env node

/**
 * Parking Validation Script
 * Validates parking entries for required fields and data quality
 */

const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  parkingDir: '.claude/idea-to-design/test-gen/parking',
  requiredFields: [
    'title',
    'description', 
    'opportunity_driver',
    'estimated_value',
    'confidence',
    'metadata'
  ],
  metadataFields: [
    'created_date',
    'created_by',
    'status'
  ]
};

// Validation functions
function validateParkingEntry(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(content);
    
    const errors = [];
    const warnings = [];
    
    // Check required fields
    for (const field of CONFIG.requiredFields) {
      if (!data[field]) {
        errors.push(`Missing required field: ${field}`);
      }
    }
    
    // Check metadata fields
    if (data.metadata) {
      for (const field of CONFIG.metadataFields) {
        if (!data.metadata[field]) {
          errors.push(`Missing required metadata field: ${field}`);
        }
      }
    }
    
    // Validate value ranges
    if (data.estimated_value !== undefined) {
      if (typeof data.estimated_value !== 'number' || data.estimated_value < 1 || data.estimated_value > 10) {
        errors.push('estimated_value must be a number between 1 and 10');
      }
    }
    
    if (data.confidence !== undefined) {
      if (typeof data.confidence !== 'number' || data.confidence < 0 || data.confidence > 1) {
        errors.push('confidence must be a number between 0 and 1');
      }
    }
    
    // Check for reasonable values
    if (data.estimated_value && data.estimated_value > 8 && data.confidence && data.confidence < 0.5) {
      warnings.push('High value estimate with low confidence - consider gathering more data');
    }
    
    if (data.estimated_value && data.estimated_value < 4 && data.confidence && data.confidence > 0.8) {
      warnings.push('Low value estimate with high confidence - consider if this feature is worth pursuing');
    }
    
    return {
      file: path.basename(filePath),
      valid: errors.length === 0,
      errors,
      warnings,
      data
    };
    
  } catch (error) {
    return {
      file: path.basename(filePath),
      valid: false,
      errors: [`JSON parse error: ${error.message}`],
      warnings: [],
      data: null
    };
  }
}

// Main validation function
function validateAllParkingEntries() {
  console.log('🅿️  Parking Validation Report');
  console.log('============================');
  
  if (!fs.existsSync(CONFIG.parkingDir)) {
    console.log('❌ Parking directory not found:', CONFIG.parkingDir);
    return false;
  }
  
  const files = fs.readdirSync(CONFIG.parkingDir)
    .filter(file => file.endsWith('.json'))
    .filter(file => file !== 'parking-template.json');
  
  if (files.length === 0) {
    console.log('ℹ️  No parking entries found to validate');
    return true;
  }
  
  console.log(`📁 Found ${files.length} parking entries to validate\n`);
  
  let validCount = 0;
  let totalErrors = 0;
  let totalWarnings = 0;
  
  for (const file of files) {
    const filePath = path.join(CONFIG.parkingDir, file);
    const result = validateParkingEntry(filePath);
    
    if (result.valid) {
      console.log(`✅ ${result.file} - Valid`);
      validCount++;
    } else {
      console.log(`❌ ${result.file} - Invalid`);
    }
    
    if (result.errors.length > 0) {
      totalErrors += result.errors.length;
      result.errors.forEach(error => {
        console.log(`   Error: ${error}`);
      });
    }
    
    if (result.warnings.length > 0) {
      totalWarnings += result.warnings.length;
      result.warnings.forEach(warning => {
        console.log(`   Warning: ${warning}`);
      });
    }
    
    console.log('');
  }
  
  // Summary
  console.log('📊 Validation Summary');
  console.log('====================');
  console.log(`Total entries: ${files.length}`);
  console.log(`Valid entries: ${validCount}`);
  console.log(`Invalid entries: ${files.length - validCount}`);
  console.log(`Total errors: ${totalErrors}`);
  console.log(`Total warnings: ${totalWarnings}`);
  
  if (totalErrors > 0) {
    console.log('\n❌ Validation failed - please fix errors before proceeding');
    return false;
  } else {
    console.log('\n✅ All parking entries are valid');
    return true;
  }
}

// Command line interface
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    // Validate all entries
    const success = validateAllParkingEntries();
    process.exit(success ? 0 : 1);
  } else {
    // Validate specific files
    for (const file of args) {
      const filePath = path.resolve(file);
      if (!fs.existsSync(filePath)) {
        console.log(`❌ File not found: ${file}`);
        continue;
      }
      
      const result = validateParkingEntry(filePath);
      
      if (result.valid) {
        console.log(`✅ ${result.file} - Valid`);
      } else {
        console.log(`❌ ${result.file} - Invalid`);
        result.errors.forEach(error => {
          console.log(`   Error: ${error}`);
        });
      }
      
      result.warnings.forEach(warning => {
        console.log(`   Warning: ${warning}`);
      });
    }
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { validateParkingEntry, validateAllParkingEntries };

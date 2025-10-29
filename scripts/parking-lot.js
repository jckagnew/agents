#!/usr/bin/env node

/**
 * Future-Feature Parking Lot Script
 *
 * Purpose: Capture and manage long-horizon or exploratory ideas without cluttering the active backlog
 *
 * Usage:
 *   node scripts/parking-lot.js --session-dir .claude/idea-to-design/session-123
 *   node scripts/parking-lot.js --session-dir SESSION_DIR --source ideas.md
 *   node scripts/parking-lot.js --session-dir SESSION_DIR --merge --dry-run
 *   node scripts/parking-lot.js --session-dir SESSION_DIR --fail-on-duplicate
 *   node scripts/parking-lot.js --session-dir SESSION_DIR --generate-report
 *
 * Features:
 * - Ingest ideas from multiple sources (JSON, Markdown, AI outputs)
 * - Deduplicate entries by title similarity
 * - Generate prioritization reports (Impact vs Effort vs Confidence)
 * - Identify promotion-ready items for active backlog
 * - Integrate with backlog sync for "future" flagged items
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// CLI ARGUMENT PARSING
// ============================================================================

const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index !== -1 && args[index + 1] ? args[index + 1] : null;
};

const sessionDir = getArg('--session-dir') || '.claude/idea-to-design/parking-test';
const sourceFile = getArg('--source');
const dryRun = args.includes('--dry-run');
const merge = args.includes('--merge');
const failOnDuplicate = args.includes('--fail-on-duplicate');
const generateReport = args.includes('--generate-report');

console.log('🅿️  Future-Feature Parking Lot');
console.log('================================');
console.log(`   Session: ${sessionDir}`);
console.log(`   Source: ${sourceFile || 'None (using template)'}`);
console.log(`   Dry Run: ${dryRun ? 'Yes' : 'No'}`);
console.log(`   Merge Mode: ${merge ? 'Yes' : 'No'}`);
console.log(`   Fail on Duplicate: ${failOnDuplicate ? 'Yes' : 'No'}`);
console.log(`   Generate Report: ${generateReport ? 'Yes' : 'No'}\n`);

// Ensure output directory exists
const parkingDir = path.join(sessionDir, 'parking');
if (!fs.existsSync(parkingDir) && !dryRun) {
  fs.mkdirSync(parkingDir, { recursive: true });
}

// ============================================================================
// IDEA SCHEMA AND VALIDATION
// ============================================================================

/**
 * Parking lot idea schema:
 * {
 *   id: string (auto-generated UUID)
 *   title: string (required, unique)
 *   description: string (required)
 *   drivers: string[] (business drivers, user needs)
 *   estimatedValue: number (1-10, business value)
 *   estimatedEffort: number (1-10, implementation complexity)
 *   confidence: number (0.0-1.0, certainty in estimates)
 *   dependencies: string[] (other features, technical requirements)
 *   targetPhase: string (when this should be considered)
 *   theme: string (category/domain)
 *   source: string (where this idea came from)
 *   status: 'parked' | 'ready' | 'promoted' | 'archived'
 *   createdAt: ISO timestamp
 *   updatedAt: ISO timestamp
 * }
 */

function validateIdea(idea) {
  const errors = [];

  if (!idea.title || typeof idea.title !== 'string' || idea.title.trim().length === 0) {
    errors.push('Title is required and must be a non-empty string');
  }

  if (!idea.description || typeof idea.description !== 'string' || idea.description.trim().length === 0) {
    errors.push('Description is required and must be a non-empty string');
  }

  if (idea.estimatedValue !== undefined) {
    if (typeof idea.estimatedValue !== 'number' || idea.estimatedValue < 1 || idea.estimatedValue > 10) {
      errors.push('estimatedValue must be a number between 1 and 10');
    }
  }

  if (idea.estimatedEffort !== undefined) {
    if (typeof idea.estimatedEffort !== 'number' || idea.estimatedEffort < 1 || idea.estimatedEffort > 10) {
      errors.push('estimatedEffort must be a number between 1 and 10');
    }
  }

  if (idea.confidence !== undefined) {
    if (typeof idea.confidence !== 'number' || idea.confidence < 0 || idea.confidence > 1) {
      errors.push('confidence must be a number between 0.0 and 1.0');
    }
  }

  return errors;
}

/**
 * Normalize idea to standard schema
 */
function normalizeIdea(rawIdea) {
  return {
    id: rawIdea.id || generateId(),
    title: rawIdea.title?.trim() || '',
    description: rawIdea.description?.trim() || '',
    drivers: Array.isArray(rawIdea.drivers) ? rawIdea.drivers : [],
    estimatedValue: rawIdea.estimatedValue || 5,
    estimatedEffort: rawIdea.estimatedEffort || 5,
    confidence: rawIdea.confidence !== undefined ? rawIdea.confidence : 0.5,
    dependencies: Array.isArray(rawIdea.dependencies) ? rawIdea.dependencies : [],
    targetPhase: rawIdea.targetPhase || 'post-mvp',
    theme: rawIdea.theme || 'uncategorized',
    source: rawIdea.source || 'manual',
    status: rawIdea.status || 'parked',
    createdAt: rawIdea.createdAt || new Date().toISOString(),
    updatedAt: new Date().toISOString()
  };
}

/**
 * Generate unique ID
 */
function generateId() {
  return `idea-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// ============================================================================
// SIMILARITY AND DEDUPLICATION
// ============================================================================

/**
 * Calculate similarity between two strings (0.0 to 1.0)
 * Using simple token-based similarity
 */
function calculateSimilarity(str1, str2) {
  const tokens1 = str1.toLowerCase().split(/\W+/).filter(t => t.length > 2);
  const tokens2 = str2.toLowerCase().split(/\W+/).filter(t => t.length > 2);

  const set1 = new Set(tokens1);
  const set2 = new Set(tokens2);

  const intersection = new Set([...set1].filter(t => set2.has(t)));
  const union = new Set([...set1, ...set2]);

  if (union.size === 0) return 0;
  return intersection.size / union.size;
}

/**
 * Find duplicate ideas based on title similarity
 */
function findDuplicates(newIdea, existingIdeas, threshold = 0.7) {
  const duplicates = [];

  for (const existing of existingIdeas) {
    const similarity = calculateSimilarity(newIdea.title, existing.title);
    if (similarity >= threshold) {
      duplicates.push({
        idea: existing,
        similarity
      });
    }
  }

  return duplicates.sort((a, b) => b.similarity - a.similarity);
}

/**
 * Deduplicate ideas array
 */
function deduplicateIdeas(ideas) {
  const unique = [];
  const seen = new Set();

  for (const idea of ideas) {
    const normalized = idea.title.toLowerCase().trim();
    if (!seen.has(normalized)) {
      seen.add(normalized);
      unique.push(idea);
    }
  }

  return unique;
}

// ============================================================================
// SOURCE PARSERS
// ============================================================================

/**
 * Parse ideas from JSON file
 */
function parseJsonSource(filePath) {
  console.log(`📄 Parsing JSON source: ${filePath}\n`);

  const content = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(content);

  // Handle both single idea and array of ideas
  const rawIdeas = Array.isArray(data) ? data : [data];

  const ideas = [];
  const errors = [];

  rawIdeas.forEach((raw, index) => {
    const validationErrors = validateIdea(raw);
    if (validationErrors.length > 0) {
      errors.push({
        index,
        idea: raw,
        errors: validationErrors
      });
    } else {
      ideas.push(normalizeIdea(raw));
    }
  });

  if (errors.length > 0) {
    console.log('⚠️  Validation errors:\n');
    errors.forEach(err => {
      console.log(`   Idea ${err.index}: ${err.idea.title || 'Untitled'}`);
      err.errors.forEach(e => console.log(`      - ${e}`));
    });
    console.log('');
  }

  console.log(`   ✅ Parsed ${ideas.length} valid ideas`);
  if (errors.length > 0) {
    console.log(`   ⚠️  Skipped ${errors.length} invalid ideas\n`);
  }

  return ideas;
}

/**
 * Parse ideas from Markdown file
 * Expects format:
 * ## Idea Title
 * Description text
 * - Drivers: driver1, driver2
 * - Value: 8
 * - Effort: 6
 * - Confidence: 0.7
 */
function parseMarkdownSource(filePath) {
  console.log(`📄 Parsing Markdown source: ${filePath}\n`);

  const content = fs.readFileSync(filePath, 'utf8');
  const ideas = [];

  // Split by ## headers
  const sections = content.split(/^## /m).filter(s => s.trim());

  sections.forEach(section => {
    const lines = section.split('\n');
    const title = lines[0].trim();

    let description = '';
    const drivers = [];
    let value = 5;
    let effort = 5;
    let confidence = 0.5;
    let theme = 'uncategorized';

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();

      if (line.startsWith('- Drivers:') || line.startsWith('- drivers:')) {
        const driverText = line.replace(/^- [Dd]rivers:\s*/, '');
        drivers.push(...driverText.split(',').map(d => d.trim()));
      } else if (line.startsWith('- Value:') || line.startsWith('- value:')) {
        value = parseInt(line.replace(/^- [Vv]alue:\s*/, '')) || 5;
      } else if (line.startsWith('- Effort:') || line.startsWith('- effort:')) {
        effort = parseInt(line.replace(/^- [Ee]ffort:\s*/, '')) || 5;
      } else if (line.startsWith('- Confidence:') || line.startsWith('- confidence:')) {
        confidence = parseFloat(line.replace(/^- [Cc]onfidence:\s*/, '')) || 0.5;
      } else if (line.startsWith('- Theme:') || line.startsWith('- theme:')) {
        theme = line.replace(/^- [Tt]heme:\s*/, '').trim();
      } else if (line && !line.startsWith('- ')) {
        description += (description ? ' ' : '') + line;
      }
    }

    if (title && description) {
      ideas.push(normalizeIdea({
        title,
        description,
        drivers,
        estimatedValue: value,
        estimatedEffort: effort,
        confidence,
        theme,
        source: 'markdown'
      }));
    }
  });

  console.log(`   ✅ Parsed ${ideas.length} ideas from Markdown\n`);
  return ideas;
}

/**
 * Parse ideas from AI Studio output
 * Expects JSON or structured text format
 */
function parseAIStudioSource(filePath) {
  console.log(`🤖 Parsing AI Studio output: ${filePath}\n`);

  const content = fs.readFileSync(filePath, 'utf8');

  // Try to parse as JSON first
  try {
    const data = JSON.parse(content);
    if (data.ideas && Array.isArray(data.ideas)) {
      return data.ideas.map(normalizeIdea);
    }
  } catch (e) {
    // Not JSON, try markdown format
    return parseMarkdownSource(filePath);
  }

  console.log('   ⚠️  Could not parse AI Studio output\n');
  return [];
}

// ============================================================================
// PARKING LOT MANAGEMENT
// ============================================================================

/**
 * Load existing parking lot
 */
function loadParkingLot() {
  const files = fs.existsSync(parkingDir)
    ? fs.readdirSync(parkingDir).filter(f => f.startsWith('parking-lot-') && f.endsWith('.json'))
    : [];

  if (files.length === 0) {
    return { ideas: [], files: [] };
  }

  // Load all parking lot files
  const allIdeas = [];
  files.forEach(file => {
    const filePath = path.join(parkingDir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (data.ideas && Array.isArray(data.ideas)) {
      allIdeas.push(...data.ideas);
    }
  });

  return {
    ideas: deduplicateIdeas(allIdeas),
    files
  };
}

/**
 * Save parking lot
 */
function saveParkingLot(ideas) {
  if (dryRun) {
    console.log('🔍 Dry run: Would save parking lot with ideas:\n');
    ideas.forEach((idea, i) => {
      console.log(`   ${i + 1}. ${idea.title} (Value: ${idea.estimatedValue}, Effort: ${idea.estimatedEffort}, Confidence: ${idea.confidence})`);
    });
    console.log('');
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `parking-lot-${timestamp}.json`;
  const filepath = path.join(parkingDir, filename);

  const data = {
    version: '1.0',
    timestamp: new Date().toISOString(),
    totalIdeas: ideas.length,
    ideas
  };

  fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
  console.log(`💾 Saved parking lot: ${filepath}\n`);

  return filepath;
}

// ============================================================================
// PRIORITIZATION AND REPORTING
// ============================================================================

/**
 * Calculate ROI score
 */
function calculateROI(idea) {
  // ROI = Value / Effort, weighted by confidence
  const rawROI = idea.estimatedValue / idea.estimatedEffort;
  return rawROI * idea.confidence;
}

/**
 * Determine if idea is ready for promotion
 */
function isPromotionReady(idea) {
  // Ready if: high confidence (≥0.6) AND high value (≥7)
  return idea.confidence >= 0.6 && idea.estimatedValue >= 7;
}

/**
 * Group ideas by theme
 */
function groupByTheme(ideas) {
  const grouped = {};

  ideas.forEach(idea => {
    const theme = idea.theme || 'uncategorized';
    if (!grouped[theme]) {
      grouped[theme] = [];
    }
    grouped[theme].push(idea);
  });

  return grouped;
}

/**
 * Generate prioritization report
 */
function generatePrioritizationReport(ideas) {
  console.log('📊 Generating prioritization report...\n');

  // Calculate ROI for all ideas
  const ideasWithROI = ideas.map(idea => ({
    ...idea,
    roi: calculateROI(idea),
    promotionReady: isPromotionReady(idea)
  }));

  // Sort by ROI
  const sorted = [...ideasWithROI].sort((a, b) => b.roi - a.roi);

  // Group by theme
  const byTheme = groupByTheme(ideasWithROI);

  // Generate report
  let report = `# Future Feature Parking Lot - Prioritization Report

**Generated**: ${new Date().toISOString()}
**Total Ideas**: ${ideas.length}
**Ready for Promotion**: ${sorted.filter(i => i.promotionReady).length}

---

## Executive Summary

### Top Priority Ideas (by ROI)

| Rank | Title | Value | Effort | Confidence | ROI | Ready? |
|------|-------|-------|--------|------------|-----|--------|
`;

  sorted.slice(0, 10).forEach((idea, index) => {
    const readyIcon = idea.promotionReady ? '✅' : '⏸️';
    report += `| ${index + 1} | ${idea.title} | ${idea.estimatedValue} | ${idea.estimatedEffort} | ${(idea.confidence * 100).toFixed(0)}% | ${idea.roi.toFixed(2)} | ${readyIcon} |\n`;
  });

  report += '\n---\n\n## Ideas by Theme\n\n';

  Object.entries(byTheme).forEach(([theme, themeIdeas]) => {
    const avgValue = (themeIdeas.reduce((sum, i) => sum + i.estimatedValue, 0) / themeIdeas.length).toFixed(1);
    const avgEffort = (themeIdeas.reduce((sum, i) => sum + i.estimatedEffort, 0) / themeIdeas.length).toFixed(1);
    const avgConfidence = (themeIdeas.reduce((sum, i) => sum + i.confidence, 0) / themeIdeas.length * 100).toFixed(0);

    report += `### ${theme} (${themeIdeas.length} ideas)\n\n`;
    report += `**Avg Value**: ${avgValue} | **Avg Effort**: ${avgEffort} | **Avg Confidence**: ${avgConfidence}%\n\n`;

    themeIdeas.sort((a, b) => b.roi - a.roi).forEach(idea => {
      const readyTag = idea.promotionReady ? ' **[READY]**' : '';
      report += `#### ${idea.title}${readyTag}\n\n`;
      report += `${idea.description}\n\n`;
      report += `- **Value**: ${idea.estimatedValue}/10\n`;
      report += `- **Effort**: ${idea.estimatedEffort}/10\n`;
      report += `- **Confidence**: ${(idea.confidence * 100).toFixed(0)}%\n`;
      report += `- **ROI**: ${idea.roi.toFixed(2)}\n`;
      if (idea.drivers.length > 0) {
        report += `- **Drivers**: ${idea.drivers.join(', ')}\n`;
      }
      if (idea.dependencies.length > 0) {
        report += `- **Dependencies**: ${idea.dependencies.join(', ')}\n`;
      }
      report += `- **Target Phase**: ${idea.targetPhase}\n`;
      report += `- **Status**: ${idea.status}\n`;
      report += '\n';
    });

    report += '\n';
  });

  report += '---\n\n## Promotion-Ready Ideas\n\n';

  const promotionReady = sorted.filter(i => i.promotionReady);

  if (promotionReady.length === 0) {
    report += '*No ideas currently meet promotion criteria (Confidence ≥ 60% AND Value ≥ 7)*\n\n';
  } else {
    report += `The following ${promotionReady.length} ideas are ready to be promoted to the active backlog:\n\n`;

    promotionReady.forEach((idea, index) => {
      report += `${index + 1}. **${idea.title}**\n`;
      report += `   - Value: ${idea.estimatedValue}/10\n`;
      report += `   - Effort: ${idea.estimatedEffort}/10\n`;
      report += `   - Confidence: ${(idea.confidence * 100).toFixed(0)}%\n`;
      report += `   - ROI: ${idea.roi.toFixed(2)}\n`;
      report += '\n';
    });
  }

  report += '---\n\n## Impact vs Effort Matrix\n\n';
  report += '```\n';
  report += 'High Impact │                    \n';
  report += '     10     │                    \n';
  report += '            │                    \n';
  report += '      7     │  QUICK WINS   │  STRATEGIC\n';
  report += '            │                │            \n';
  report += '      5     ├─────────────────┼────────────\n';
  report += '            │                │            \n';
  report += '      3     │  FILL INS     │  MAJOR     \n';
  report += '            │                │  PROJECTS  \n';
  report += ' Low Impact │                    \n';
  report += '      0     └────────────────────────────\n';
  report += '                0      5      10\n';
  report += '              Low    Medium   High\n';
  report += '                   Effort\n';
  report += '```\n\n';

  // Categorize ideas into quadrants
  const quickWins = sorted.filter(i => i.estimatedValue >= 7 && i.estimatedEffort <= 5);
  const strategic = sorted.filter(i => i.estimatedValue >= 7 && i.estimatedEffort > 5);
  const fillIns = sorted.filter(i => i.estimatedValue < 7 && i.estimatedEffort <= 5);
  const majorProjects = sorted.filter(i => i.estimatedValue < 7 && i.estimatedEffort > 5);

  report += `**Quick Wins** (High Value, Low Effort): ${quickWins.length}\n`;
  quickWins.slice(0, 5).forEach(i => report += `  - ${i.title}\n`);
  report += '\n';

  report += `**Strategic** (High Value, High Effort): ${strategic.length}\n`;
  strategic.slice(0, 5).forEach(i => report += `  - ${i.title}\n`);
  report += '\n';

  report += `**Fill-Ins** (Low Value, Low Effort): ${fillIns.length}\n`;
  fillIns.slice(0, 5).forEach(i => report += `  - ${i.title}\n`);
  report += '\n';

  report += `**Major Projects** (Low Value, High Effort): ${majorProjects.length}\n`;
  majorProjects.slice(0, 5).forEach(i => report += `  - ${i.title}\n`);
  report += '\n';

  report += '---\n\n## Next Steps\n\n';
  report += '1. Review promotion-ready ideas with stakeholders\n';
  report += '2. Move approved ideas to active backlog using backlog sync\n';
  report += '3. Update confidence scores for uncertain ideas\n';
  report += '4. Archive ideas that are no longer relevant\n';
  report += '5. Continue to park new exploratory ideas here\n';

  return report;
}

/**
 * Save prioritization report
 */
function savePrioritizationReport(ideas) {
  const report = generatePrioritizationReport(ideas);

  if (dryRun) {
    console.log('🔍 Dry run: Generated report preview:\n');
    console.log(report.substring(0, 500) + '...\n');
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `parking-summary-${timestamp}.md`;
  const filepath = path.join(parkingDir, filename);

  fs.writeFileSync(filepath, report);
  console.log(`📊 Saved prioritization report: ${filepath}\n`);

  return filepath;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  console.log('🚀 Starting parking lot processing...\n');

  // Load existing parking lot
  const existing = loadParkingLot();
  console.log(`📦 Loaded ${existing.ideas.length} existing ideas from ${existing.files.length} files\n`);

  let newIdeas = [];

  // Parse source if provided
  if (sourceFile) {
    const ext = path.extname(sourceFile).toLowerCase();

    if (ext === '.json') {
      newIdeas = parseJsonSource(sourceFile);
    } else if (ext === '.md' || ext === '.markdown') {
      newIdeas = parseMarkdownSource(sourceFile);
    } else if (ext === '.txt' && sourceFile.includes('ai-studio')) {
      newIdeas = parseAIStudioSource(sourceFile);
    } else {
      console.error(`❌ Unsupported file format: ${ext}`);
      process.exit(1);
    }
  }

  // Check for duplicates
  const duplicates = [];
  newIdeas.forEach(newIdea => {
    const dups = findDuplicates(newIdea, existing.ideas);
    if (dups.length > 0) {
      duplicates.push({
        newIdea,
        matches: dups
      });
    }
  });

  if (duplicates.length > 0) {
    console.log('⚠️  Found potential duplicates:\n');
    duplicates.forEach(dup => {
      console.log(`   New: "${dup.newIdea.title}"`);
      dup.matches.forEach(match => {
        console.log(`      Similar to: "${match.idea.title}" (${(match.similarity * 100).toFixed(0)}% match)`);
      });
    });
    console.log('');

    if (failOnDuplicate) {
      console.error('❌ Exiting due to duplicate detection (--fail-on-duplicate)\n');
      process.exit(1);
    }
  }

  // Merge or replace
  let finalIdeas;
  if (merge) {
    console.log('🔀 Merging new ideas with existing...\n');
    finalIdeas = deduplicateIdeas([...existing.ideas, ...newIdeas]);
  } else if (newIdeas.length > 0) {
    console.log('🔄 Replacing existing ideas with new...\n');
    finalIdeas = newIdeas;
  } else {
    finalIdeas = existing.ideas;
  }

  console.log(`✅ Final count: ${finalIdeas.length} ideas\n`);

  // Save parking lot
  const savedFile = saveParkingLot(finalIdeas);

  // Generate report if requested or if we have ideas
  if (generateReport || finalIdeas.length > 0) {
    const reportFile = savePrioritizationReport(finalIdeas);

    // Show promotion-ready summary
    const promotionReady = finalIdeas.filter(isPromotionReady);
    if (promotionReady.length > 0) {
      console.log('🎯 Promotion-Ready Ideas:\n');
      promotionReady.forEach((idea, i) => {
        const roi = calculateROI(idea);
        console.log(`   ${i + 1}. ${idea.title}`);
        console.log(`      Value: ${idea.estimatedValue}/10, Effort: ${idea.estimatedEffort}/10, Confidence: ${(idea.confidence * 100).toFixed(0)}%, ROI: ${roi.toFixed(2)}`);
      });
      console.log('');
      console.log('💡 These ideas are ready to be promoted to the active backlog!\n');
    }
  }

  // Summary
  console.log('='.repeat(60));
  console.log('📊 Parking Lot Summary');
  console.log('='.repeat(60));
  console.log(`Total Ideas: ${finalIdeas.length}`);
  console.log(`New Ideas: ${newIdeas.length}`);
  console.log(`Duplicates Found: ${duplicates.length}`);
  console.log(`Promotion Ready: ${finalIdeas.filter(isPromotionReady).length}`);
  console.log('');

  const byTheme = groupByTheme(finalIdeas);
  console.log('Ideas by Theme:');
  Object.entries(byTheme).forEach(([theme, ideas]) => {
    console.log(`  - ${theme}: ${ideas.length}`);
  });
  console.log('='.repeat(60));

  console.log('\n✅ Parking lot processing complete!');
  console.log('\nNext steps:');
  console.log('  1. Review parking-summary-*.md report');
  console.log('  2. Update confidence scores for uncertain ideas');
  console.log('  3. Promote ready ideas to active backlog');
  console.log('  4. Archive or remove obsolete ideas\n');
}

// Run main function
main().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});

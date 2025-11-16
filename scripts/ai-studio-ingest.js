#!/usr/bin/env node

/**
 * AI Studio Ingestion Script
 *
 * Purpose: Convert Google AI Studio exports into structured parking-lot entries
 *
 * Usage:
 *   node scripts/ai-studio-ingest.js --session-dir SESSION_DIR --source file.json
 *   node scripts/ai-studio-ingest.js --session-dir SESSION_DIR --source file.md --auto-tag
 *   node scripts/ai-studio-ingest.js --session-dir SESSION_DIR --source file.json --confidence-threshold 0.7
 *   node scripts/ai-studio-ingest.js --session-dir SESSION_DIR --source file.json --dry-run
 *
 * Features:
 * - Parse AI Studio JSON and Markdown exports
 * - Convert to parking lot schema
 * - Auto-tag based on content analysis
 * - Generate ingestion summary reports
 * - Maintain audit trail
 * - Respect deduplication and ROI workflows
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

const sessionDir = getArg('--session-dir') || '.claude/idea-to-design/ai-studio-test';
const sourceFile = getArg('--source');
const dryRun = args.includes('--dry-run');
const autoTag = args.includes('--auto-tag');
const confidenceThreshold = parseFloat(getArg('--confidence-threshold') || '0.6');

if (!sourceFile) {
  console.error('❌ Missing required argument: --source');
  console.error('Usage: node scripts/ai-studio-ingest.js --session-dir DIR --source FILE [--dry-run] [--auto-tag] [--confidence-threshold 0.7]');
  process.exit(1);
}

console.log('🤖 AI Studio Ingestion');
console.log('======================');
console.log(`   Session: ${sessionDir}`);
console.log(`   Source: ${sourceFile}`);
console.log(`   Dry Run: ${dryRun ? 'Yes' : 'No'}`);
console.log(`   Auto-Tag: ${autoTag ? 'Yes' : 'No'}`);
console.log(`   Confidence Threshold: ${confidenceThreshold}\n`);

// Ensure output directory exists
const parkingDir = path.join(sessionDir, 'parking');
if (!fs.existsSync(parkingDir) && !dryRun) {
  fs.mkdirSync(parkingDir, { recursive: true });
}

// ============================================================================
// AI STUDIO FORMAT PARSERS
// ============================================================================

/**
 * Expected AI Studio JSON format:
 * {
 *   "title": "Feature Name",
 *   "summary": "Brief description",
 *   "findings": "Detailed analysis",
 *   "feasibility": "High|Medium|Low" or number,
 *   "cost": "High|Medium|Low" or number,
 *   "confidence": 0.0-1.0 or "High|Medium|Low",
 *   "opportunity_driver": ["Driver 1", "Driver 2"],
 *   "dependencies": ["Dep 1", "Dep 2"],
 *   "timeframe": "Q1|Q2|MVP|Post-MVP|Exploratory",
 *   "next_steps": "Actions to take",
 *   "tags": ["tag1", "tag2"]
 * }
 */

/**
 * Parse AI Studio JSON export
 */
function parseAIStudioJSON(filePath) {
  console.log(`📄 Parsing AI Studio JSON: ${filePath}\n`);

  const content = fs.readFileSync(filePath, 'utf8');
  const data = JSON.parse(content);

  // Handle both single object and array of objects
  const items = Array.isArray(data) ? data : [data];

  const parsedIdeas = [];

  items.forEach((item, index) => {
    try {
      const idea = convertAIStudioToIdea(item);
      parsedIdeas.push(idea);
    } catch (error) {
      console.error(`   ⚠️  Error parsing item ${index}: ${error.message}`);
    }
  });

  console.log(`   ✅ Parsed ${parsedIdeas.length} ideas from AI Studio JSON\n`);
  return parsedIdeas;
}

/**
 * Parse AI Studio Markdown export
 * Expected format:
 * # Feature Title
 * ## Summary
 * Description text
 * ## Feasibility: High
 * ## Cost: Medium
 * ## Confidence: 0.8
 * ## Drivers
 * - Driver 1
 * - Driver 2
 */
function parseAIStudioMarkdown(filePath) {
  console.log(`📄 Parsing AI Studio Markdown: ${filePath}\n`);

  const content = fs.readFileSync(filePath, 'utf8');
  const ideas = [];

  // Split by top-level headers
  const sections = content.split(/^# /m).filter(s => s.trim());

  sections.forEach(section => {
    const lines = section.split('\n');
    const title = lines[0].trim();

    let summary = '';
    let findings = '';
    let feasibility = 'Medium';
    let cost = 'Medium';
    let confidence = 0.5;
    const drivers = [];
    const dependencies = [];
    let timeframe = 'post-mvp';
    let nextSteps = '';
    const tags = [];

    let currentSection = '';

    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();

      if (line.startsWith('## ')) {
        currentSection = line.replace(/^## /, '').toLowerCase();
        continue;
      }

      if (line.startsWith('- ')) {
        const item = line.replace(/^- /, '');
        if (currentSection.includes('driver')) {
          drivers.push(item);
        } else if (currentSection.includes('depend')) {
          dependencies.push(item);
        } else if (currentSection.includes('tag')) {
          tags.push(item);
        }
      } else if (line) {
        if (currentSection.includes('summary')) {
          summary += (summary ? ' ' : '') + line;
        } else if (currentSection.includes('finding')) {
          findings += (findings ? ' ' : '') + line;
        } else if (currentSection.includes('feasibility')) {
          feasibility = line.split(':')[1]?.trim() || line;
        } else if (currentSection.includes('cost') || currentSection.includes('effort')) {
          cost = line.split(':')[1]?.trim() || line;
        } else if (currentSection.includes('confidence')) {
          const confidenceText = line.split(':')[1]?.trim() || line;
          confidence = parseConfidence(confidenceText);
        } else if (currentSection.includes('timeframe') || currentSection.includes('timeline')) {
          timeframe = line.split(':')[1]?.trim() || line;
        } else if (currentSection.includes('next') || currentSection.includes('step')) {
          nextSteps += (nextSteps ? ' ' : '') + line;
        }
      }
    }

    if (title && summary) {
      const item = {
        title,
        summary,
        findings,
        feasibility,
        cost,
        confidence,
        opportunity_driver: drivers,
        dependencies,
        timeframe,
        next_steps: nextSteps,
        tags
      };

      ideas.push(convertAIStudioToIdea(item));
    }
  });

  console.log(`   ✅ Parsed ${ideas.length} ideas from AI Studio Markdown\n`);
  return ideas;
}

// ============================================================================
// CONVERSION & MAPPING
// ============================================================================

/**
 * Convert AI Studio item to parking lot idea schema
 */
function convertAIStudioToIdea(aiStudioItem) {
  const title = aiStudioItem.title || aiStudioItem.name || 'Untitled Idea';
  const description = aiStudioItem.summary || aiStudioItem.description || '';

  // Extract or construct drivers
  let drivers = [];
  if (Array.isArray(aiStudioItem.opportunity_driver)) {
    drivers = aiStudioItem.opportunity_driver;
  } else if (typeof aiStudioItem.opportunity_driver === 'string') {
    drivers = [aiStudioItem.opportunity_driver];
  } else if (aiStudioItem.drivers) {
    drivers = Array.isArray(aiStudioItem.drivers) ? aiStudioItem.drivers : [aiStudioItem.drivers];
  }

  // Map feasibility to value (1-10)
  const estimatedValue = mapToValue(aiStudioItem.feasibility || aiStudioItem.value);

  // Map cost/effort to effort (1-10)
  const estimatedEffort = mapToEffort(aiStudioItem.cost || aiStudioItem.effort);

  // Parse confidence (0.0-1.0)
  const confidence = parseConfidence(aiStudioItem.confidence);

  // Extract dependencies
  let dependencies = [];
  if (Array.isArray(aiStudioItem.dependencies)) {
    dependencies = aiStudioItem.dependencies;
  } else if (typeof aiStudioItem.dependencies === 'string') {
    dependencies = [aiStudioItem.dependencies];
  }

  // Map timeframe to target phase
  const targetPhase = mapTimeframeToPhase(aiStudioItem.timeframe || aiStudioItem.timeline);

  // Determine theme from tags or content
  let theme = 'uncategorized';
  if (aiStudioItem.tags && aiStudioItem.tags.length > 0) {
    theme = aiStudioItem.tags[0].toLowerCase();
  } else if (autoTag) {
    theme = detectTheme(title, description);
  }

  // Construct parking lot idea
  const idea = {
    id: generateId(),
    title,
    description: description + (aiStudioItem.findings ? `\n\n**Findings**: ${aiStudioItem.findings}` : ''),
    drivers,
    estimatedValue,
    estimatedEffort,
    confidence,
    dependencies,
    targetPhase,
    theme,
    source: 'ai-studio',
    status: 'parked',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
    metadata: {
      aiStudio: {
        nextSteps: aiStudioItem.next_steps || '',
        originalTags: aiStudioItem.tags || []
      }
    }
  };

  return idea;
}

/**
 * Map feasibility/value text to numeric value (1-10)
 */
function mapToValue(value) {
  if (typeof value === 'number') {
    return Math.max(1, Math.min(10, Math.round(value)));
  }

  const text = String(value || '').toLowerCase();

  if (text.includes('very high') || text.includes('critical')) return 10;
  if (text.includes('high')) return 9;
  if (text.includes('medium-high') || text.includes('significant')) return 7;
  if (text.includes('medium')) return 6;
  if (text.includes('medium-low') || text.includes('moderate')) return 4;
  if (text.includes('low')) return 3;
  if (text.includes('very low') || text.includes('minimal')) return 1;

  return 5; // Default medium
}

/**
 * Map cost/effort text to numeric effort (1-10)
 */
function mapToEffort(effort) {
  if (typeof effort === 'number') {
    return Math.max(1, Math.min(10, Math.round(effort)));
  }

  const text = String(effort || '').toLowerCase();

  if (text.includes('very high') || text.includes('major')) return 10;
  if (text.includes('high')) return 8;
  if (text.includes('medium-high') || text.includes('significant')) return 7;
  if (text.includes('medium')) return 5;
  if (text.includes('medium-low') || text.includes('moderate')) return 4;
  if (text.includes('low')) return 3;
  if (text.includes('very low') || text.includes('trivial')) return 1;

  return 5; // Default medium
}

/**
 * Parse confidence value (0.0-1.0)
 */
function parseConfidence(confidence) {
  if (typeof confidence === 'number') {
    return Math.max(0, Math.min(1, confidence));
  }

  const text = String(confidence || '').toLowerCase();

  if (text.includes('very high') || text.includes('certain')) return 0.9;
  if (text.includes('high')) return 0.8;
  if (text.includes('medium-high')) return 0.7;
  if (text.includes('medium')) return 0.5;
  if (text.includes('medium-low')) return 0.4;
  if (text.includes('low')) return 0.3;
  if (text.includes('very low') || text.includes('uncertain')) return 0.2;

  return 0.5; // Default medium
}

/**
 * Map timeframe to target phase
 */
function mapTimeframeToPhase(timeframe) {
  const text = String(timeframe || '').toLowerCase();

  if (text.includes('mvp') || text.includes('immediate') || text.includes('q1')) return 'mvp';
  if (text.includes('post-mvp') || text.includes('q2')) return 'post-mvp';
  if (text.includes('v2') || text.includes('q3') || text.includes('q4')) return 'v2';
  if (text.includes('future') || text.includes('long-term')) return 'future';
  if (text.includes('exploratory') || text.includes('research')) return 'exploratory';

  return 'post-mvp'; // Default
}

/**
 * Auto-detect theme from title and description
 */
function detectTheme(title, description) {
  const text = (title + ' ' + description).toLowerCase();

  const themePatterns = {
    'user-experience': ['ux', 'ui', 'interface', 'usability', 'design', 'user', 'experience'],
    'performance': ['performance', 'speed', 'optimization', 'fast', 'latency', 'cache'],
    'security': ['security', 'auth', 'encryption', 'vulnerability', 'privacy', 'compliance'],
    'analytics': ['analytics', 'metrics', 'tracking', 'data', 'insights', 'reporting'],
    'infrastructure': ['infrastructure', 'deployment', 'devops', 'scaling', 'reliability'],
    'business': ['revenue', 'pricing', 'sales', 'marketing', 'growth', 'monetization'],
    'developer-experience': ['developer', 'dx', 'api', 'sdk', 'tooling', 'documentation']
  };

  for (const [theme, keywords] of Object.entries(themePatterns)) {
    if (keywords.some(keyword => text.includes(keyword))) {
      return theme;
    }
  }

  return 'uncategorized';
}

/**
 * Generate unique ID
 */
function generateId() {
  return `ai-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// ============================================================================
// DEDUPLICATION
// ============================================================================

/**
 * Load existing parking lot
 */
function loadExistingParkingLot() {
  const files = fs.existsSync(parkingDir)
    ? fs.readdirSync(parkingDir).filter(f => f.startsWith('parking-lot-') && f.endsWith('.json'))
    : [];

  const allIdeas = [];
  files.forEach(file => {
    const filePath = path.join(parkingDir, file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (data.ideas && Array.isArray(data.ideas)) {
      allIdeas.push(...data.ideas);
    }
  });

  return allIdeas;
}

/**
 * Check for duplicates using simple title matching
 */
function findDuplicates(newIdeas, existingIdeas) {
  const duplicates = [];

  newIdeas.forEach(newIdea => {
    const existingMatch = existingIdeas.find(existing =>
      existing.title.toLowerCase() === newIdea.title.toLowerCase()
    );

    if (existingMatch) {
      duplicates.push({
        newIdea,
        existingIdea: existingMatch
      });
    }
  });

  return duplicates;
}

// ============================================================================
// PROMOTION DETECTION
// ============================================================================

/**
 * Check if idea meets promotion criteria
 */
function isPromotionReady(idea, threshold = 0.6) {
  return idea.confidence >= threshold && idea.estimatedValue >= 7;
}

/**
 * Calculate ROI
 */
function calculateROI(idea) {
  return (idea.estimatedValue / idea.estimatedEffort) * idea.confidence;
}

// ============================================================================
// STORAGE
// ============================================================================

/**
 * Save ideas to parking lot
 */
function saveToParkingLot(ideas) {
  if (dryRun) {
    console.log('🔍 Dry run: Would save the following ideas:\n');
    ideas.forEach((idea, i) => {
      const roi = calculateROI(idea);
      const ready = isPromotionReady(idea, confidenceThreshold) ? '✅' : '⏸️';
      console.log(`   ${i + 1}. ${idea.title} ${ready}`);
      console.log(`      Value: ${idea.estimatedValue}, Effort: ${idea.estimatedEffort}, Confidence: ${(idea.confidence * 100).toFixed(0)}%, ROI: ${roi.toFixed(2)}`);
    });
    console.log('');
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `parking-lot-${timestamp}.json`;
  const filepath = path.join(parkingDir, filename);

  // Merge with existing ideas
  const existingIdeas = loadExistingParkingLot();
  const allIdeas = [...existingIdeas, ...ideas];

  const data = {
    version: '1.0',
    timestamp: new Date().toISOString(),
    source: 'ai-studio',
    totalIdeas: allIdeas.length,
    ideas: allIdeas
  };

  fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
  console.log(`💾 Saved to parking lot: ${filepath}\n`);

  return filepath;
}

// ============================================================================
// REPORTING
// ============================================================================

/**
 * Generate AI Studio ingestion summary
 */
function generateIngestionSummary(ideas, duplicates) {
  const promotionReady = ideas.filter(i => isPromotionReady(i, confidenceThreshold));
  const ideasWithROI = ideas.map(i => ({ ...i, roi: calculateROI(i) })).sort((a, b) => b.roi - a.roi);

  let report = `# AI Studio Ingestion Summary

**Generated**: ${new Date().toISOString()}
**Source**: ${sourceFile}
**Total Ideas Ingested**: ${ideas.length}
**Duplicates Found**: ${duplicates.length}
**Promotion-Ready Ideas**: ${promotionReady.length}
**Confidence Threshold**: ${confidenceThreshold}

---

## Ingestion Results

`;

  ideasWithROI.forEach((idea, index) => {
    const readyTag = isPromotionReady(idea, confidenceThreshold) ? ' **[READY FOR PROMOTION]**' : '';
    report += `### ${index + 1}. ${idea.title}${readyTag}\n\n`;
    report += `${idea.description}\n\n`;
    report += `- **Value**: ${idea.estimatedValue}/10\n`;
    report += `- **Effort**: ${idea.estimatedEffort}/10\n`;
    report += `- **Confidence**: ${(idea.confidence * 100).toFixed(0)}%\n`;
    report += `- **ROI**: ${idea.roi.toFixed(2)}\n`;
    report += `- **Theme**: ${idea.theme}\n`;
    report += `- **Target Phase**: ${idea.targetPhase}\n`;

    if (idea.drivers.length > 0) {
      report += `- **Drivers**: ${idea.drivers.join(', ')}\n`;
    }

    if (idea.dependencies.length > 0) {
      report += `- **Dependencies**: ${idea.dependencies.join(', ')}\n`;
    }

    if (idea.metadata?.aiStudio?.nextSteps) {
      report += `- **Next Steps**: ${idea.metadata.aiStudio.nextSteps}\n`;
    }

    report += '\n';
  });

  if (duplicates.length > 0) {
    report += '---\n\n## Duplicate Detection\n\n';
    report += `Found ${duplicates.length} potential duplicates:\n\n`;

    duplicates.forEach((dup, i) => {
      report += `${i + 1}. **${dup.newIdea.title}**\n`;
      report += `   - Matches existing: "${dup.existingIdea.title}"\n`;
      report += `   - New idea was merged with existing parking lot\n\n`;
    });
  }

  if (promotionReady.length > 0) {
    report += '---\n\n## Promotion-Ready Ideas\n\n';
    report += `The following ${promotionReady.length} ideas meet promotion criteria (Confidence ≥ ${confidenceThreshold} AND Value ≥ 7):\n\n`;

    promotionReady.forEach((idea, i) => {
      const roi = calculateROI(idea);
      report += `${i + 1}. **${idea.title}**\n`;
      report += `   - Value: ${idea.estimatedValue}/10\n`;
      report += `   - Effort: ${idea.estimatedEffort}/10\n`;
      report += `   - Confidence: ${(idea.confidence * 100).toFixed(0)}%\n`;
      report += `   - ROI: ${roi.toFixed(2)}\n`;
      report += `   - **Action**: Review with stakeholders and promote to active backlog\n\n`;
    });
  }

  report += '---\n\n## Next Steps\n\n';
  report += '1. Review all ingested ideas in the parking lot\n';
  report += '2. Validate promotion-ready ideas with stakeholders\n';
  report += '3. Run `npm run parking:report` to generate full prioritization report\n';
  report += '4. Promote approved ideas to active backlog using backlog sync\n';

  return report;
}

/**
 * Save ingestion summary
 */
function saveIngestionSummary(ideas, duplicates) {
  const report = generateIngestionSummary(ideas, duplicates);

  if (dryRun) {
    console.log('🔍 Dry run: Generated summary preview:\n');
    console.log(report.substring(0, 500) + '...\n');
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `ai-studio-summary-${timestamp}.md`;
  const filepath = path.join(parkingDir, filename);

  fs.writeFileSync(filepath, report);
  console.log(`📊 Saved ingestion summary: ${filepath}\n`);

  return filepath;
}

/**
 * Create audit log
 */
function createAuditLog(ideas, duplicates, parkingFile, summaryFile) {
  if (dryRun) {
    return null;
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `audit-${timestamp}.json`;
  const filepath = path.join(parkingDir, filename);

  const auditData = {
    timestamp: new Date().toISOString(),
    source: 'ai-studio',
    sourceFile,
    totalIdeas: ideas.length,
    duplicates: duplicates.length,
    promotionReady: ideas.filter(i => isPromotionReady(i, confidenceThreshold)).length,
    confidenceThreshold,
    parkingFile,
    summaryFile,
    ideas: ideas.map(i => ({
      id: i.id,
      title: i.title,
      value: i.estimatedValue,
      effort: i.estimatedEffort,
      confidence: i.confidence,
      roi: calculateROI(i),
      promotionReady: isPromotionReady(i, confidenceThreshold)
    }))
  };

  fs.writeFileSync(filepath, JSON.stringify(auditData, null, 2));
  console.log(`📋 Audit log created: ${filepath}\n`);

  return filepath;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  console.log('🚀 Starting AI Studio ingestion...\n');

  // Verify source file exists
  if (!fs.existsSync(sourceFile)) {
    console.error(`❌ Source file not found: ${sourceFile}`);
    process.exit(1);
  }

  // Parse source file based on extension
  const ext = path.extname(sourceFile).toLowerCase();
  let ideas = [];

  if (ext === '.json') {
    ideas = parseAIStudioJSON(sourceFile);
  } else if (ext === '.md' || ext === '.markdown') {
    ideas = parseAIStudioMarkdown(sourceFile);
  } else {
    console.error(`❌ Unsupported file format: ${ext}`);
    console.error('   Supported formats: .json, .md, .markdown');
    process.exit(1);
  }

  if (ideas.length === 0) {
    console.log('✅ No ideas found in source file. Nothing to ingest.');
    return;
  }

  console.log(`📊 Ingested ${ideas.length} ideas from AI Studio\n`);

  // Check for duplicates
  const existingIdeas = loadExistingParkingLot();
  const duplicates = findDuplicates(ideas, existingIdeas);

  if (duplicates.length > 0) {
    console.log(`⚠️  Found ${duplicates.length} potential duplicates:\n`);
    duplicates.forEach(dup => {
      console.log(`   "${dup.newIdea.title}" matches existing "${dup.existingIdea.title}"`);
    });
    console.log('\n   Note: Duplicates will be merged with existing parking lot\n');
  }

  // Show promotion-ready summary
  const promotionReady = ideas.filter(i => isPromotionReady(i, confidenceThreshold));
  if (promotionReady.length > 0) {
    console.log(`🎯 ${promotionReady.length} ideas meet promotion criteria:\n`);
    promotionReady.forEach((idea, i) => {
      const roi = calculateROI(idea);
      console.log(`   ${i + 1}. ${idea.title}`);
      console.log(`      Value: ${idea.estimatedValue}/10, Effort: ${idea.estimatedEffort}/10, Confidence: ${(idea.confidence * 100).toFixed(0)}%, ROI: ${roi.toFixed(2)}`);
    });
    console.log('');
  }

  // Save to parking lot
  const parkingFile = saveToParkingLot(ideas);

  // Generate summary report
  const summaryFile = saveIngestionSummary(ideas, duplicates);

  // Create audit log
  const auditFile = createAuditLog(ideas, duplicates, parkingFile, summaryFile);

  // Final summary
  console.log('='.repeat(60));
  console.log('📊 AI Studio Ingestion Summary');
  console.log('='.repeat(60));
  console.log(`Source File:      ${sourceFile}`);
  console.log(`Ideas Ingested:   ${ideas.length}`);
  console.log(`Duplicates:       ${duplicates.length}`);
  console.log(`Promotion Ready:  ${promotionReady.length}`);
  console.log(`Mode:             ${dryRun ? 'DRY RUN' : 'LIVE'}`);
  console.log('='.repeat(60));

  if (dryRun) {
    console.log('\n💡 Tip: Run without --dry-run to save ideas to parking lot');
  } else {
    console.log('\n✅ AI Studio ingestion complete!');
    console.log('\nNext steps:');
    console.log('  1. Review ai-studio-summary-*.md');
    console.log('  2. Run: npm run parking:report');
    console.log('  3. Promote ready ideas to active backlog');
  }
}

// Run main function
main().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});

#!/usr/bin/env node

/**
 * Backlog Sync Module
 *
 * Purpose: Automatically sync backlog items from documentation generation to issue tracker.
 * Extracts future features, nice-to-haves, and audit findings from PRD/Architecture/UX docs
 * and creates structured backlog entries.
 *
 * Usage:
 *   node scripts/backlog-sync.js \
 *     --session-dir .claude/idea-to-design/session-X \
 *     [--dry-run]
 *
 * Features:
 * - Extracts backlog items from PRD, architecture, and UX documentation
 * - Pushes to MCP issue tracker (GitHub, Linear, Jira, etc.)
 * - Maintains audit trail of synced items
 * - Supports dry-run mode for testing
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ============================================================================
// CLI ARGUMENT PARSING
// ============================================================================

const args = process.argv.slice(2);
const getArg = (flag) => {
  const index = args.indexOf(flag);
  return index !== -1 && args[index + 1] ? args[index + 1] : null;
};

const sessionDir = getArg('--session-dir');
const dryRun = args.includes('--dry-run');
const inputFile = getArg('--input');

if (!sessionDir && !inputFile) {
  console.error('❌ Missing required argument');
  console.error('Usage: node scripts/backlog-sync.js --session-dir <path> [--dry-run]');
  console.error('   OR: node scripts/backlog-sync.js --input <backlog-input.json> [--dry-run]');
  process.exit(1);
}

console.log('📋 Backlog Sync Module');
console.log(`   Session: ${sessionDir || 'N/A'}`);
console.log(`   Input File: ${inputFile || 'N/A'}`);
console.log(`   Mode: ${dryRun ? 'DRY RUN' : 'LIVE'}\n`);

// ============================================================================
// BACKLOG EXTRACTION FUNCTIONS
// ============================================================================

/**
 * Extract nice-to-have features from PRD
 */
function extractPRDBacklog(prdDir) {
  const backlogItems = [];

  // Check acceptance criteria for nice-to-have features
  const criteriaFile = path.join(prdDir, '03-acceptance-criteria.md');
  if (!fs.existsSync(criteriaFile)) {
    console.warn('⚠️  Acceptance criteria file not found');
    return backlogItems;
  }

  const content = fs.readFileSync(criteriaFile, 'utf8');

  // Extract nice-to-have features
  const niceToHaveSection = content.match(/## Nice-to-Have Features \(Post-MVP\)([\s\S]*?)(?=##|$)/);

  if (niceToHaveSection) {
    const features = niceToHaveSection[1].match(/### \d+\. (.+?)\n([\s\S]*?)(?=###|\n##|$)/g);

    if (features) {
      features.forEach(feature => {
        const titleMatch = feature.match(/### \d+\. (.+)/);
        const userStoryMatch = feature.match(/\*\*User Story\*\*: (.+)/);
        const descMatch = feature.match(/\*\*Description\*\*: (.+)/);

        if (titleMatch) {
          backlogItems.push({
            title: titleMatch[1],
            description: descMatch ? descMatch[1] : (userStoryMatch ? userStoryMatch[1] : ''),
            priority: 'P2',
            source: 'PRD (Nice-to-Have)',
            labels: ['enhancement', 'post-mvp'],
            status: 'backlog'
          });
        }
      });
    }
  }

  // Also check for future considerations
  const futureMatches = content.match(/\*\*Future.*?\*\*:?\s*(.+?)(?=\n\n|\n\*\*|$)/gi);
  if (futureMatches) {
    futureMatches.forEach(match => {
      const description = match.replace(/\*\*Future.*?\*\*:?\s*/i, '').trim();
      if (description && description.length > 10) {
        backlogItems.push({
          title: `Future Enhancement: ${description.slice(0, 60)}${description.length > 60 ? '...' : ''}`,
          description: description,
          priority: 'P3',
          source: 'PRD (Future Consideration)',
          labels: ['future', 'enhancement'],
          status: 'backlog'
        });
      }
    });
  }

  return backlogItems;
}

/**
 * Extract future work from architecture docs
 */
function extractArchitectureBacklog(architectureDir) {
  const backlogItems = [];

  if (!fs.existsSync(architectureDir)) {
    console.warn('⚠️  Architecture directory not found');
    return backlogItems;
  }

  const archFiles = [
    'architecture-tech-stack.md',
    'architecture-services.md',
    'architecture-data-model.md',
    'architecture-api.md',
    'architecture-deployment.md'
  ];

  archFiles.forEach(fileName => {
    const filePath = path.join(architectureDir, fileName);
    if (!fs.existsSync(filePath)) return;

    const content = fs.readFileSync(filePath, 'utf8');

    // Extract "Future Consideration" sections
    const futureMatches = content.match(/### Future Consideration\n([\s\S]*?)(?=\n###|\n##|$)/g);
    if (futureMatches) {
      futureMatches.forEach(section => {
        const lines = section.split('\n').filter(l => l.trim());

        // Look for subsections or bullet points
        const items = section.match(/####\s+(.+?)\n([\s\S]*?)(?=\n####|\n###|$)/g);
        if (items) {
          items.forEach(item => {
            const titleMatch = item.match(/####\s+(.+)/);
            const purposeMatch = item.match(/\*\*Purpose\*\*:\s*(.+)/);

            if (titleMatch) {
              backlogItems.push({
                title: `[Architecture] ${titleMatch[1]}`,
                description: purposeMatch ? purposeMatch[1] : item.replace(/####\s+.+\n/, '').trim().slice(0, 200),
                priority: 'P2',
                source: `Architecture (${fileName})`,
                labels: ['architecture', 'future'],
                status: 'backlog'
              });
            }
          });
        }
      });
    }

    // Extract "If API Added Later" sections
    const apiLaterMatches = content.match(/\*\*If API Added Later\*\*:([\s\S]*?)(?=\n##|\n---|$)/);
    if (apiLaterMatches) {
      backlogItems.push({
        title: '[Architecture] Backend API Implementation',
        description: 'Add backend API for cloud sync and multi-device support. ' + apiLaterMatches[1].trim().slice(0, 200),
        priority: 'P2',
        source: `Architecture (${fileName})`,
        labels: ['backend', 'api', 'future'],
        status: 'backlog'
      });
    }

    // Extract migration paths
    const migrationMatches = content.match(/\*\*Migration Path\*\*:([\s\S]*?)(?=\n##|\n---|$)/);
    if (migrationMatches) {
      backlogItems.push({
        title: '[Architecture] Migration to Production Infrastructure',
        description: migrationMatches[1].trim().slice(0, 200),
        priority: 'P3',
        source: `Architecture (${fileName})`,
        labels: ['infrastructure', 'scaling'],
        status: 'backlog'
      });
    }
  });

  return backlogItems;
}

/**
 * Extract future work from UX docs
 */
function extractUXBacklog(uxDir) {
  const backlogItems = [];

  if (!fs.existsSync(uxDir)) {
    console.warn('⚠️  UX directory not found');
    return backlogItems;
  }

  const uxFiles = fs.readdirSync(uxDir).filter(f => f.endsWith('.md'));

  uxFiles.forEach(fileName => {
    const filePath = path.join(uxDir, fileName);
    const content = fs.readFileSync(filePath, 'utf8');

    // Extract future features from UX flows
    const futureMatches = content.match(/\*\*Future\*\*:([\s\S]*?)(?=\n\*\*|\n##|$)/gi);
    if (futureMatches) {
      futureMatches.forEach(match => {
        const description = match.replace(/\*\*Future\*\*:/i, '').trim();
        if (description.length > 10) {
          backlogItems.push({
            title: `[UX] ${description.slice(0, 60)}${description.length > 60 ? '...' : ''}`,
            description: description,
            priority: 'P2',
            source: `UX (${fileName})`,
            labels: ['ux', 'enhancement'],
            status: 'backlog'
          });
        }
      });
    }

    // Extract command palette mentions (common future feature)
    if (content.includes('Command palette (future)')) {
      backlogItems.push({
        title: '[UX] Implement Command Palette',
        description: 'Add keyboard-driven command palette for power users (Cmd+K)',
        priority: 'P2',
        source: `UX (${fileName})`,
        labels: ['ux', 'keyboard-shortcuts', 'power-users'],
        status: 'backlog'
      });
    }
  });

  return backlogItems;
}

/**
 * Extract issues from respect_spec audit
 */
function extractAuditBacklog(sessionDir) {
  const backlogItems = [];
  const reportPath = path.join(sessionDir, 'respect-spec-report.json');

  if (!fs.existsSync(reportPath)) {
    console.warn('⚠️  Respect-spec report not found');
    return backlogItems;
  }

  const report = JSON.parse(fs.readFileSync(reportPath, 'utf8'));

  // Extract architecture issues
  if (report.validations?.architecture?.issues) {
    report.validations.architecture.issues.forEach(issue => {
      backlogItems.push({
        title: `[Audit] Architecture: ${issue}`,
        description: `Issue found during spec compliance audit: ${issue}`,
        priority: 'P1',
        source: 'Spec Compliance Audit',
        labels: ['bug', 'audit', 'architecture'],
        status: 'todo'
      });
    });
  }

  // Extract UX issues
  if (report.validations?.ux?.issues) {
    report.validations.ux.issues.forEach(issue => {
      backlogItems.push({
        title: `[Audit] UX: ${issue}`,
        description: `Issue found during spec compliance audit: ${issue}`,
        priority: 'P1',
        source: 'Spec Compliance Audit',
        labels: ['bug', 'audit', 'ux'],
        status: 'todo'
      });
    });
  }

  return backlogItems;
}

// ============================================================================
// BACKLOG STORAGE
// ============================================================================

/**
 * Save backlog items to local storage before syncing
 */
function saveBacklogLocally(sessionDir, backlogItems) {
  const backlogDir = path.join(sessionDir, 'backlog');

  if (!fs.existsSync(backlogDir)) {
    fs.mkdirSync(backlogDir, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const backlogFile = path.join(backlogDir, `backlog-${timestamp}.json`);

  const backlogData = {
    timestamp: new Date().toISOString(),
    totalItems: backlogItems.length,
    items: backlogItems,
    metadata: {
      sessionDir: sessionDir,
      generatedBy: 'backlog-sync.js',
      version: '1.0.0'
    }
  };

  fs.writeFileSync(backlogFile, JSON.stringify(backlogData, null, 2));

  console.log(`✅ Backlog saved locally: ${backlogFile}`);
  return backlogFile;
}

// ============================================================================
// ISSUE TRACKER INTEGRATION
// ============================================================================

/**
 * Check if GitHub CLI is available
 */
function isGitHubCLIAvailable() {
  try {
    execSync('gh --version', { stdio: 'ignore' });
    return true;
  } catch (error) {
    return false;
  }
}

/**
 * Get current GitHub repository
 */
function getCurrentRepo() {
  try {
    const remote = execSync('git remote get-url origin', { encoding: 'utf8' }).trim();
    const match = remote.match(/github\.com[:/](.+?)\/(.+?)(\.git)?$/);
    if (match) {
      return `${match[1]}/${match[2].replace('.git', '')}`;
    }
  } catch (error) {
    // Not a git repo or no origin
  }
  return null;
}

/**
 * Push backlog items to GitHub Issues
 */
async function pushToGitHub(backlogItems, dryRun = false) {
  if (!isGitHubCLIAvailable()) {
    console.warn('⚠️  GitHub CLI (gh) not available. Skipping GitHub sync.');
    console.warn('   Install: https://cli.github.com/');
    return { success: false, synced: [], failed: [] };
  }

  const repo = getCurrentRepo();
  if (!repo) {
    console.warn('⚠️  Not a GitHub repository. Skipping GitHub sync.');
    return { success: false, synced: [], failed: [] };
  }

  console.log(`📤 Syncing to GitHub: ${repo}\n`);

  const synced = [];
  const failed = [];

  for (const item of backlogItems) {
    try {
      const labels = item.labels.join(',');
      const body = `${item.description}\n\n---\n**Source**: ${item.source}\n**Priority**: ${item.priority}`;

      if (dryRun) {
        console.log(`[DRY RUN] Would create issue: ${item.title}`);
        console.log(`   Labels: ${labels}`);
        console.log(`   Priority: ${item.priority}\n`);
        synced.push({ ...item, issueNumber: 'DRY_RUN' });
      } else {
        const command = `gh issue create --repo ${repo} --title "${item.title.replace(/"/g, '\\"')}" --body "${body.replace(/"/g, '\\"')}" --label "${labels}"`;
        const output = execSync(command, { encoding: 'utf8' });
        const issueUrl = output.trim();
        const issueNumber = issueUrl.match(/\/(\d+)$/)?.[1];

        console.log(`✅ Created issue #${issueNumber}: ${item.title}`);
        synced.push({ ...item, issueNumber, issueUrl });
      }
    } catch (error) {
      console.error(`❌ Failed to create issue: ${item.title}`);
      console.error(`   Error: ${error.message}`);
      failed.push({ ...item, error: error.message });
    }
  }

  return { success: true, synced, failed };
}

/**
 * Main issue tracker sync (supports multiple backends)
 */
async function syncToIssueTracker(backlogItems, dryRun = false) {
  console.log('\n📤 Syncing to Issue Tracker...\n');

  // Try GitHub first
  const githubResult = await pushToGitHub(backlogItems, dryRun);

  if (githubResult.success) {
    return githubResult;
  }

  // Could add other integrations here (Linear, Jira, etc.)
  console.warn('⚠️  No issue tracker integration available.');
  console.warn('   Items saved locally but not synced to tracker.');

  return { success: false, synced: [], failed: backlogItems };
}

// ============================================================================
// AUDIT LOGGING
// ============================================================================

/**
 * Create audit log of sync operation
 */
function createAuditLog(sessionDir, syncResult, backlogFile) {
  const backlogDir = path.join(sessionDir, 'backlog');
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const auditFile = path.join(backlogDir, `audit-${timestamp}.json`);

  const auditData = {
    timestamp: new Date().toISOString(),
    backlogFile: backlogFile,
    totalItems: syncResult.synced.length + syncResult.failed.length,
    syncedItems: syncResult.synced.length,
    failedItems: syncResult.failed.length,
    synced: syncResult.synced.map(item => ({
      title: item.title,
      issueNumber: item.issueNumber,
      issueUrl: item.issueUrl,
      source: item.source,
      priority: item.priority
    })),
    failed: syncResult.failed.map(item => ({
      title: item.title,
      source: item.source,
      error: item.error
    }))
  };

  fs.writeFileSync(auditFile, JSON.stringify(auditData, null, 2));

  console.log(`\n✅ Audit log created: ${auditFile}`);
  return auditFile;
}

// ============================================================================
// PARKING LOT INTEGRATION
// ============================================================================

/**
 * Determine if an item should be parked instead of added to active backlog
 * Criteria for parking:
 * - Labeled as "future", "exploratory", or "research"
 * - Priority is P3 or lower
 * - Description contains keywords like "consider", "explore", "investigate"
 */
function shouldParkItem(item) {
  // Check labels
  const parkingLabels = ['future', 'exploratory', 'research', 'post-mvp', 'nice-to-have'];
  if (item.labels && item.labels.some(label => parkingLabels.includes(label))) {
    return true;
  }

  // Check priority (P3 or lower = park it)
  if (item.priority === 'P3' || item.priority === 'P4') {
    return true;
  }

  // Check description keywords
  const exploratoryKeywords = ['explore', 'consider', 'investigate', 'research', 'future', 'long-term', 'experimental'];
  const description = (item.description || '').toLowerCase();
  if (exploratoryKeywords.some(keyword => description.includes(keyword))) {
    return true;
  }

  return false;
}

/**
 * Route backlog items to either active backlog or parking lot
 */
function routeToParkingLot(backlogItems) {
  const activeBacklog = [];
  const parkedIdeas = [];

  backlogItems.forEach(item => {
    if (shouldParkItem(item)) {
      // Convert backlog item to parking lot idea format
      parkedIdeas.push({
        title: item.title,
        description: item.description || '',
        drivers: [item.source || 'backlog-sync'],
        estimatedValue: item.priority === 'P1' ? 9 : item.priority === 'P2' ? 7 : 5,
        estimatedEffort: 5, // Default middle value
        confidence: 0.4, // Low confidence for exploratory items
        dependencies: [],
        targetPhase: 'post-mvp',
        theme: item.labels && item.labels[0] ? item.labels[0] : 'uncategorized',
        source: 'backlog-sync',
        status: 'parked'
      });
    } else {
      activeBacklog.push(item);
    }
  });

  return { activeBacklog, parkedIdeas };
}

/**
 * Save ideas to parking lot
 */
function saveToParkingLot(sessionDir, parkedIdeas) {
  const parkingDir = path.join(sessionDir, 'parking');

  if (!fs.existsSync(parkingDir)) {
    fs.mkdirSync(parkingDir, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const filename = `parking-lot-${timestamp}.json`;
  const filepath = path.join(parkingDir, filename);

  const data = {
    version: '1.0',
    timestamp: new Date().toISOString(),
    source: 'backlog-sync',
    totalIdeas: parkedIdeas.length,
    ideas: parkedIdeas
  };

  fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
  console.log(`   💾 Saved to: ${filepath}`);

  return filepath;
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  let backlogItems = [];

  // Load from input file or extract from session
  if (inputFile) {
    if (!fs.existsSync(inputFile)) {
      console.error(`❌ Input file not found: ${inputFile}`);
      process.exit(1);
    }

    const inputData = JSON.parse(fs.readFileSync(inputFile, 'utf8'));
    backlogItems = inputData.items || [];
    console.log(`📥 Loaded ${backlogItems.length} items from input file\n`);
  } else {
    console.log('🔍 Extracting backlog items from documentation...\n');

    const prdDir = path.join(sessionDir, 'prd');
    const architectureDir = path.join(sessionDir, 'architecture');
    const uxDir = path.join(sessionDir, 'ux');

    // Extract from each source
    console.log('📄 Scanning PRD documents...');
    const prdItems = extractPRDBacklog(prdDir);
    console.log(`   Found ${prdItems.length} items\n`);

    console.log('🏗️  Scanning architecture documents...');
    const archItems = extractArchitectureBacklog(architectureDir);
    console.log(`   Found ${archItems.length} items\n`);

    console.log('🎨 Scanning UX documents...');
    const uxItems = extractUXBacklog(uxDir);
    console.log(`   Found ${uxItems.length} items\n`);

    console.log('📊 Scanning audit reports...');
    const auditItems = extractAuditBacklog(sessionDir);
    console.log(`   Found ${auditItems.length} items\n`);

    backlogItems = [...prdItems, ...archItems, ...uxItems, ...auditItems];

    // Deduplicate items by title
    const seen = new Set();
    backlogItems = backlogItems.filter(item => {
      if (seen.has(item.title)) {
        return false;
      }
      seen.add(item.title);
      return true;
    });

    console.log(`🔄 After deduplication: ${backlogItems.length} unique items\n`);

    // Route exploratory/future items to parking lot
    const { activeBacklog, parkedIdeas } = routeToParkingLot(backlogItems);

    if (parkedIdeas.length > 0) {
      console.log(`🅿️  Routing ${parkedIdeas.length} exploratory/future items to parking lot...\n`);
      saveToParkingLot(sessionDir, parkedIdeas);
      console.log(`✅ Parked ${parkedIdeas.length} items for future consideration\n`);
    }

    // Continue with only active backlog items
    backlogItems = activeBacklog;
    console.log(`📋 ${backlogItems.length} items remaining for active backlog\n`);
  }

  if (backlogItems.length === 0) {
    console.log('✅ No backlog items found. Nothing to sync.');
    return;
  }

  console.log(`📋 Total backlog items: ${backlogItems.length}\n`);

  // Save locally
  const backlogFile = saveBacklogLocally(sessionDir || path.dirname(inputFile), backlogItems);

  // Sync to issue tracker
  const syncResult = await syncToIssueTracker(backlogItems, dryRun);

  // Create audit log
  const auditFile = createAuditLog(sessionDir || path.dirname(inputFile), syncResult, backlogFile);

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 Backlog Sync Summary');
  console.log('='.repeat(60));
  console.log(`Total Items:     ${backlogItems.length}`);
  console.log(`Synced:          ${syncResult.synced.length} ✅`);
  console.log(`Failed:          ${syncResult.failed.length} ❌`);
  console.log(`Mode:            ${dryRun ? 'DRY RUN' : 'LIVE'}`);
  console.log('='.repeat(60));

  if (dryRun) {
    console.log('\n💡 Tip: Run without --dry-run to actually create issues');
  }

  if (syncResult.failed.length > 0) {
    console.log('\n⚠️  Some items failed to sync. Check audit log for details.');
    process.exit(1);
  }
}

// Run main function
main().catch(error => {
  console.error('❌ Fatal error:', error);
  process.exit(1);
});

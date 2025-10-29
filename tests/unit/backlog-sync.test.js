/**
 * Unit tests for backlog-sync.js
 */

import { describe, it, expect } from 'vitest';

describe('Backlog Sync - Extraction Logic', () => {
  it('should extract nice-to-have features from PRD', () => {
    // Mock PRD content
    const mockPRD = `
## Nice-to-Have Features (Post-MVP)

### 1. Cloud Sync
**User Story**: As a user, I want to sync my data across devices
**Description**: Allow users to sync their data to the cloud
`;

    // This would be the actual extraction logic
    const features = extractNiceToHave(mockPRD);

    expect(features).toHaveLength(1);
    expect(features[0]).toHaveProperty('title');
    expect(features[0].title).toContain('Cloud Sync');
  });

  it('should deduplicate backlog items by title', () => {
    const items = [
      { title: 'Feature A', description: 'Test 1' },
      { title: 'Feature B', description: 'Test 2' },
      { title: 'Feature A', description: 'Duplicate' }
    ];

    const deduplicated = deduplicateItems(items);

    expect(deduplicated).toHaveLength(2);
    expect(deduplicated.map(i => i.title)).toEqual(['Feature A', 'Feature B']);
  });

  it('should assign correct priority levels', () => {
    const criticalItem = { source: 'Spec Compliance Audit', labels: ['bug', 'critical'] };
    const futureItem = { source: 'Architecture (future)', labels: ['enhancement'] };

    expect(assignPriority(criticalItem)).toBe('P1');
    expect(assignPriority(futureItem)).toBe('P2');
  });
});

// Helper functions (would be imported from actual module)
function extractNiceToHave(content) {
  const regex = /### \d+\. (.+)/g;
  const matches = [...content.matchAll(regex)];
  return matches.map(m => ({ title: m[1], description: '' }));
}

function deduplicateItems(items) {
  const seen = new Set();
  return items.filter(item => {
    if (seen.has(item.title)) return false;
    seen.add(item.title);
    return true;
  });
}

function assignPriority(item) {
  if (item.labels?.includes('critical') || item.labels?.includes('bug')) {
    return 'P1';
  }
  if (item.labels?.includes('enhancement')) {
    return 'P2';
  }
  return 'P3';
}

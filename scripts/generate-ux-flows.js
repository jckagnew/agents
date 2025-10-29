#!/usr/bin/env node

/**
 * UX Flow Documentation Generator
 *
 * Purpose: Given a requirements JSON (same input used by generate-prd.js and generate-architecture.js),
 * produce comprehensive UX flow documentation including:
 * 1. Screen map with navigation structure (Mermaid diagrams)
 * 2. Key states and transitions
 * 3. User interaction patterns
 * 4. Accessibility flows
 *
 * Usage:
 *   node scripts/generate-ux-flows.js \
 *     --requirements path/to/requirements.json \
 *     --output-dir path/to/output
 */

const fs = require('fs');
const path = require('path');

// Parse CLI arguments
const args = process.argv.slice(2);
const requirementsPath = args[args.indexOf('--requirements') + 1];
const outputDir = args[args.indexOf('--output-dir') + 1];

if (!requirementsPath || !outputDir) {
  console.error('❌ Missing required arguments');
  console.error('Usage: node scripts/generate-ux-flows.js --requirements <path> --output-dir <path>');
  process.exit(1);
}

// Load requirements
const requirements = JSON.parse(fs.readFileSync(requirementsPath, 'utf8'));
const appName = requirements.app_name;
const appType = requirements.app_type;
const extractFeatures = req => {
  if (!req) return [];
  if (Array.isArray(req)) return req;
  if (req.must_have) return req.must_have;
  if (req.must_have_features) return req.must_have_features;
  if (req.features && Array.isArray(req.features)) return req.features;
  return [];
};

const features = extractFeatures(requirements.features) || extractFeatures(requirements.must_have_features) || [];

console.log('🎨 Generating UX Flow Documentation...');
console.log(`   App: ${appName}\n`);

// Ensure output directory exists
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

/**
 * Generate Screen Map with Navigation Structure
 */
function generateScreenMap(requirements) {
  const appName = requirements.app_name;
  const features = extractFeatures(requirements.features) || extractFeatures(requirements.must_have_features) || [];

  // Detect core screens based on features
  const screens = {
    dashboard: true,
    logging: features.some(f => f.toLowerCase().includes('log') || f.toLowerCase().includes('track')),
    goals: features.some(f => f.toLowerCase().includes('goal')),
    progress: features.some(f => f.toLowerCase().includes('progress') || f.toLowerCase().includes('analytics')),
    settings: true,
    history: features.some(f => f.toLowerCase().includes('history') || f.toLowerCase().includes('log'))
  };

  return `# Screen Map & Navigation

## Overview

${appName} follows a **single-page application (SPA)** architecture with client-side routing. The navigation structure prioritizes quick access to core features with minimal clicks.

**Navigation Pattern**: Hub-and-spoke (Dashboard as central hub)

---

## Screen Hierarchy

\`\`\`mermaid
graph TB
    Start([App Launch]) --> Dashboard[Dashboard Screen]

    Dashboard --> Log[Quick Log Entry]
    Dashboard --> Goals[Goals Screen]
    Dashboard --> Progress[Progress Screen]
    Dashboard --> History[History Screen]
    Dashboard --> Settings[Settings Screen]

    Log --> Dashboard
    Goals --> GoalDetail[Goal Detail]
    GoalDetail --> Goals
    Progress --> Dashboard
    History --> EntryDetail[Entry Detail]
    EntryDetail --> History
    Settings --> Dashboard

    style Dashboard fill:#2196F3,color:#fff
    style Log fill:#4CAF50,color:#fff
    style Goals fill:#FF9800,color:#fff
    style Progress fill:#9C27B0,color:#fff
\`\`\`

---

## Screen Inventory

### 1. Dashboard (Home Screen)
**Route**: \`/\`
**Purpose**: Central hub for all app functionality

**Components**:
- Quick stats summary (today's progress)
- Quick log button (primary CTA)
- Recent entries list (last 5)
- Goal progress rings
- Navigation menu

**Navigation**:
- → Quick Log (modal/slide-up)
- → Goals (link)
- → Progress (link)
- → History (link)
- → Settings (menu)

**Empty State**:
- Welcome message
- "Set your first goal" CTA
- "Log your first entry" CTA

---

${screens.logging ? `### 2. Quick Log Entry
**Route**: \`/log\` (or modal overlay)
**Purpose**: Fast data entry for daily tracking

**Components**:
- Numeric input (with increment/decrement buttons)
- Unit selector (ml/oz for water)
- Timestamp picker (defaults to now)
- Notes field (optional)
- Save button (primary)
- Cancel button (secondary)

**Interaction Flow**:
1. User taps "Log Entry" on dashboard
2. Modal slides up from bottom
3. Focus on numeric input
4. User enters value (keyboard or +/- buttons)
5. Tap "Save"
6. Success toast → return to dashboard

**Validation**:
- Value must be > 0
- Value must be < 10000 (sanity check)
- Timestamp cannot be future

**Keyboard Shortcuts**:
- \`Cmd+N\` - Open quick log
- \`Enter\` - Save
- \`Esc\` - Cancel

---

` : ''}

${screens.goals ? `### 3. Goals Screen
**Route**: \`/goals\`
**Purpose**: View and manage daily/weekly goals

**Components**:
- Active goals list
- Goal progress bars
- "Add Goal" button
- Goal cards (editable inline)

**Goal Card**:
- Goal name
- Target value + unit
- Current progress (%)
- Progress bar (visual)
- Edit/Delete actions

**Interaction Flow**:
1. View list of goals
2. Tap "Add Goal"
3. Enter goal details (name, target, frequency)
4. Save → goal appears in list
5. Dashboard updates with new goal

**Empty State**:
- "No goals yet" message
- "Create your first goal" CTA
- Suggested goals (e.g., "Drink 2L daily")

---

` : ''}

${screens.progress ? `### 4. Progress Screen
**Route**: \`/progress\`
**Purpose**: Visualize trends and analytics

**Components**:
- Date range selector (7d, 30d, 90d, All)
- Chart (line or bar chart)
- Streak counter
- Best day badge
- Average statistics

**Chart Types**:
- **Line Chart**: Trend over time
- **Bar Chart**: Daily comparison
- **Heatmap**: Calendar view with intensity

**Metrics Displayed**:
- Total entries logged
- Current streak (consecutive days)
- Longest streak
- Average daily value
- Goal completion rate

**Interactions**:
- Tap chart bar → view entries for that day
- Swipe chart → change date range
- Tap "Share" → export screenshot

---

` : ''}

${screens.history ? `### 5. History Screen
**Route**: \`/history\`
**Purpose**: Browse and edit past entries

**Components**:
- Grouped list (by date)
- Search/filter bar
- Entry cards (swipeable)
- Pagination (infinite scroll)

**Entry Card**:
- Value + unit
- Timestamp
- Notes (if any)
- Edit/Delete actions (swipe left)

**Interactions**:
- Swipe left → Delete
- Tap entry → Edit modal
- Pull to refresh

**Search/Filter**:
- By date range
- By value range
- By notes keyword

**Empty State**:
- "No entries yet"
- "Log your first entry" CTA

---

` : ''}

### ${screens.history ? '6' : '5'}. Settings Screen
**Route**: \`/settings\`
**Purpose**: App configuration and preferences

**Sections**:
1. **Profile** (if auth exists)
   - Name, email, avatar

2. **Preferences**
   - Unit system (metric/imperial)
   - Default reminder time
   - Theme (light/dark/auto)
   - Language

3. **Data**
   - Export data (JSON)
   - Clear all data (with confirmation)
   - Import data (future)

4. **About**
   - Version number
   - Privacy policy link
   - Terms of service link
   - Contact support

**Interactions**:
- Toggle switches for boolean settings
- Dropdowns for selection
- Confirmation modals for destructive actions

---

## Navigation Patterns

### Primary Navigation
**Type**: Bottom Tab Bar (Mobile) / Sidebar (Desktop)

**Tabs**:
1. 🏠 Home (Dashboard)
2. 📊 Progress
3. ➕ Quick Log (center, emphasized)
4. 📅 History
5. ⚙️ Settings

**Desktop Adaptation**:
- Sidebar on left
- Always visible (not collapsed)
- Active state highlighted

### Secondary Navigation
**Type**: In-page navigation (breadcrumbs, back buttons)

**Patterns**:
- Modal overlays for quick actions (log entry)
- Slide-in panels for details (goal detail)
- Breadcrumbs for deep navigation

---

## Responsive Behavior

### Mobile (< 768px)
- Bottom tab navigation
- Full-screen modals
- Stacked cards
- Swipe gestures enabled

### Tablet (768px - 1024px)
- Side navigation (collapsible)
- Modal dialogs (not full-screen)
- 2-column layout where appropriate

### Desktop (> 1024px)
- Persistent sidebar
- Multi-column layouts
- Hover states
- Keyboard shortcuts

---

## Loading States

### Initial Load
\`\`\`
1. App shell appears instantly (cached)
2. Skeleton screens for content
3. Data loads from localStorage
4. UI hydrates with real data
\`\`\`

**Skeleton Pattern**:
- Pulsing gray boxes
- Match final layout dimensions
- No loading spinners (jarring)

### Navigation Transitions
\`\`\`
1. Instant route change (no spinner)
2. Optimistic UI updates
3. Smooth page transitions (fade/slide)
\`\`\`

**Duration**: 200ms (feels instant)

---

## Error States

### Network Errors
**Pattern**: Toast notification (dismissible)
**Message**: "You're offline. Changes saved locally."
**Action**: Dismiss or Auto-dismiss after 3s

### Validation Errors
**Pattern**: Inline error message (below input)
**Message**: Specific error (e.g., "Value must be greater than 0")
**Action**: User fixes input

### Critical Errors
**Pattern**: Full-screen error boundary
**Message**: "Something went wrong. Refresh to try again."
**Action**: Refresh button

---

## Accessibility Navigation

### Keyboard Navigation
- \`Tab\` - Move to next interactive element
- \`Shift+Tab\` - Move to previous element
- \`Enter\` or \`Space\` - Activate button/link
- \`Esc\` - Close modal/dialog
- \`Cmd+K\` - Command palette (future)

### Screen Reader Announcements
- Route changes: "Navigated to Progress screen"
- Actions: "Entry logged successfully"
- Errors: "Error: Invalid value entered"

### Focus Management
- Focus moves to modal when opened
- Focus returns to trigger when closed
- Focus visible indicator (outline)

---

## Deep Linking

**Pattern**: All screens accessible via URL

**Examples**:
- \`/\` → Dashboard
- \`/goals\` → Goals screen
- \`/goals/123\` → Goal detail
- \`/progress?range=30d\` → Progress (30 days)
- \`/settings\` → Settings

**Benefits**:
- Shareable links
- Browser back/forward
- Bookmarkable screens

---

## References

**Design System**:
- See \`architecture-tech-stack.md\` for UI framework
- See \`prd/01-personas.md\` for user needs

**Implementation**:
- React Router for navigation
- Framer Motion for transitions
- Radix UI for accessible components
`;
}

/**
 * Generate Key States & Transitions
 */
function generateStates(requirements) {
  const appName = requirements.app_name;
  const features = extractFeatures(requirements.features) || extractFeatures(requirements.must_have_features) || [];

  return `# Key States & Transitions

## Overview

${appName} uses **React state management** (Context API + localStorage) to handle application state. This document maps key states, transitions, and user interactions.

---

## State Architecture

### State Layers

\`\`\`mermaid
graph TB
    UI[UI Components] --> Local[Local Component State]
    UI --> Global[Global Context State]
    Global --> Storage[localStorage Persistence]

    Local -.Ephemeral.-> UI
    Global -.Persisted.-> Storage

    style Global fill:#2196F3,color:#fff
    style Storage fill:#4CAF50,color:#fff
\`\`\`

**Local State**: Temporary UI state (modal open, form inputs)
**Global State**: App-wide data (entries, goals, settings)
**Persistent State**: Synced to localStorage on change

---

## Core Data States

### Entries State
\`\`\`typescript
interface EntriesState {
  entries: Entry[];
  loading: boolean;
  error: string | null;
  lastSync: Date | null;
}

interface Entry {
  id: string;
  timestamp: Date;
  value: number;
  unit: string;
  notes?: string;
  goalId?: string;
}
\`\`\`

**Transitions**:
1. **Empty** → User logs first entry → **Has Data**
2. **Has Data** → User deletes all → **Empty**
3. **Synced** → User makes edit → **Pending Sync** (if backend exists)

---

### Goals State
\`\`\`typescript
interface GoalsState {
  goals: Goal[];
  activeGoalId: string | null;
  loading: boolean;
  error: string | null;
}

interface Goal {
  id: string;
  name: string;
  target: number;
  unit: string;
  frequency: 'daily' | 'weekly';
  isActive: boolean;
  createdAt: Date;
}
\`\`\`

**Transitions**:
1. **No Goals** → User creates goal → **Has Goals**
2. **Has Goals** → User achieves goal → **Goal Completed** (celebration)
3. **Active Goal** → User pauses → **Inactive Goal**

---

### Settings State
\`\`\`typescript
interface SettingsState {
  theme: 'light' | 'dark' | 'auto';
  unit: 'ml' | 'oz';
  notifications: boolean;
  reminderTime: string; // "09:00"
  language: string;
}
\`\`\`

**Transitions**:
- Settings update immediately (optimistic)
- Persisted to localStorage on change
- No loading states (instant)

---

## UI States

### Dashboard States

#### Empty State
**Trigger**: No entries logged yet
**UI**:
- Empty state illustration
- "Get started" message
- "Log your first entry" CTA
- "Set a goal" CTA

\`\`\`mermaid
stateDiagram-v2
    [*] --> Empty: First launch
    Empty --> HasData: Log first entry
    HasData --> Empty: Delete all data
    HasData --> HasData: Log more entries
\`\`\`

---

#### Has Data State
**Trigger**: At least 1 entry exists
**UI**:
- Quick stats cards
- Recent entries list
- Progress visualization
- Quick log button

**Sub-states**:
- **On Track**: Progress ≥ goal
- **Behind**: Progress < goal
- **No Goal Set**: Show suggestion to set goal

---

#### Loading State
**Trigger**: Initial data load (< 100ms usually)
**UI**:
- Skeleton screens
- Shimmer effect
- No spinner

---

#### Error State
**Trigger**: Data load fails (rare, localStorage should always work)
**UI**:
- Error message
- "Retry" button
- "Clear cache" option

---

### Quick Log States

\`\`\`mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: Tap "Log Entry"
    Open --> Entering: Focus input
    Entering --> Validating: Tap "Save"
    Validating --> Saving: Valid
    Validating --> Entering: Invalid (show error)
    Saving --> Success: Saved
    Success --> Closed: Auto-close
    Open --> Closed: Tap "Cancel" or Esc
\`\`\`

**State Details**:

1. **Closed**: Modal not visible
2. **Open**: Modal visible, input focused
3. **Entering**: User typing value
4. **Validating**: Check value > 0, < max
5. **Saving**: Write to localStorage
6. **Success**: Show toast, close modal

**Timing**:
- Open animation: 200ms
- Save duration: < 50ms (localStorage)
- Success toast: 2s
- Auto-close: After success

---

### Progress Chart States

\`\`\`mermaid
stateDiagram-v2
    [*] --> NoData: No entries
    NoData --> Loading: User logs data
    Loading --> Rendered: Data loaded
    Rendered --> Updating: New entry added
    Updating --> Rendered: Re-render
    Rendered --> Loading: Change date range
\`\`\`

**State Details**:

1. **No Data**: Empty state with CTA
2. **Loading**: Skeleton chart
3. **Rendered**: Chart with data
4. **Updating**: Smooth transition to new data

**Performance**:
- Debounce updates: 300ms
- Use React.memo to prevent unnecessary re-renders
- Virtualize long lists

---

## User Interaction Flows

### Flow 1: First-Time User Experience

\`\`\`mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Storage

    U->>A: Open app
    A->>S: Check for existing data
    S-->>A: No data found
    A->>U: Show empty state
    U->>A: Tap "Log first entry"
    A->>U: Open quick log modal
    U->>A: Enter value (500 ml)
    A->>A: Validate input
    A->>S: Save entry
    S-->>A: Success
    A->>U: Show success toast
    A->>U: Update dashboard (show entry)
    A->>U: Celebrate (confetti?)
\`\`\`

**Duration**: ~30 seconds
**Success Metric**: User completes first log

---

### Flow 2: Daily Logging (Returning User)

\`\`\`mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Storage

    U->>A: Open app
    A->>S: Load entries
    S-->>A: Return entries
    A->>U: Show dashboard (with data)
    U->>A: Tap "Quick Log"
    A->>U: Open modal (prefill today's date)
    U->>A: Tap "+250ml" quick button
    A->>S: Save entry
    S-->>A: Success
    A->>U: Close modal, update dashboard
    A->>U: Update streak counter
\`\`\`

**Duration**: ~5 seconds
**Success Metric**: Entry logged quickly

---

### Flow 3: Goal Achievement

\`\`\`mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Storage

    U->>A: Log entry (reaches goal)
    A->>A: Calculate progress
    A->>A: Detect goal achieved
    A->>U: Show celebration modal
    A->>U: Confetti animation
    A->>U: "Goal achieved!" message
    U->>A: Tap "Dismiss"
    A->>U: Return to dashboard
    A->>S: Log achievement
    S-->>A: Success
\`\`\`

**Duration**: ~3 seconds
**Success Metric**: User feels rewarded

---

### Flow 4: Editing Past Entry

\`\`\`mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant S as Storage

    U->>A: Navigate to History
    A->>S: Load all entries
    S-->>A: Return entries
    A->>U: Show grouped list
    U->>A: Swipe left on entry
    A->>U: Show Delete button
    U->>A: Tap "Edit" instead
    A->>U: Open edit modal (prefilled)
    U->>A: Change value
    A->>A: Validate
    A->>S: Update entry
    S-->>A: Success
    A->>U: Close modal
    A->>U: Update list (optimistic UI)
\`\`\`

**Duration**: ~10 seconds
**Success Metric**: Edit saves correctly

---

## Transition Animations

### Modal Transitions
**Open**: Slide up from bottom (mobile) or fade in (desktop)
**Close**: Slide down or fade out
**Duration**: 200ms
**Easing**: cubic-bezier(0.4, 0, 0.2, 1)

### Page Transitions
**Enter**: Fade in + slide right
**Exit**: Fade out
**Duration**: 150ms

### List Animations
**Add Item**: Slide in from top
**Remove Item**: Slide out + fade
**Reorder**: Smooth position change

### Success States
**Toast**: Slide in from top
**Confetti**: Particle burst (on goal achievement)
**Progress Bar**: Smooth fill animation

---

## Offline Behavior

### States
1. **Online**: Normal operation
2. **Offline**: All features work (local-first)
3. **Reconnecting**: If backend exists, sync pending changes

### Offline-First Strategy
**Principle**: App works 100% offline, sync is optional

**User Experience**:
- No "You're offline" error
- Data saves to localStorage immediately
- Sync icon shows pending changes (if backend)
- Auto-sync when online

---

## Error Recovery

### Validation Errors
**Strategy**: Prevent invalid states
**Example**: Disable "Save" until valid

### Storage Errors
**Strategy**: Graceful degradation
**Example**: If localStorage full, show warning + export option

### Unexpected Errors
**Strategy**: Error boundary
**Example**: Catch React errors, show fallback UI

---

## State Persistence

### localStorage Schema
\`\`\`json
{
  "hydrotrack_entries": [...],
  "hydrotrack_goals": [...],
  "hydrotrack_settings": {...},
  "hydrotrack_lastSync": "2025-10-24T12:00:00Z"
}
\`\`\`

### Sync Strategy
- Save on every mutation
- Debounced writes (100ms)
- Atomic updates (all-or-nothing)

---

## References

**State Management**:
- React Context API
- localStorage Web API
- React Router state

**PRD Cross-References**:
- See \`prd/03-acceptance-criteria.md\` for feature states
- See \`architecture-data-model.md\` for data schemas
`;
}

/**
 * Generate Interaction Patterns
 */
function generateInteractions(requirements) {
  const appName = requirements.app_name;

  return `# User Interaction Patterns

## Overview

${appName} follows **mobile-first interaction patterns** optimized for quick, frequent logging while maintaining full desktop functionality.

---

## Input Patterns

### Quick Value Entry
**Context**: Logging water intake

**Mobile**:
\`\`\`
┌─────────────────────┐
│  Log Water Intake   │
├─────────────────────┤
│                     │
│   [  -  ] 500 [ + ] │ ← Increment/decrement
│         ml          │
│                     │
│  ┌───┐ ┌───┐ ┌───┐ │
│  │250│ │500│ │750│ │ ← Quick buttons
│  └───┘ └───┘ └───┘ │
│                     │
│    [ Save Entry ]   │
│                     │
└─────────────────────┘
\`\`\`

**Desktop**:
- Number input with up/down arrows
- Keyboard input with validation
- Enter to submit

**Accessibility**:
- ARIA live region announces value changes
- Increment/decrement buttons labeled
- Keyboard shortcuts: Arrow up/down

---

### Date/Time Selection
**Context**: Editing entry timestamp

**Mobile**: Native date/time picker
**Desktop**: Custom calendar dropdown
**Default**: Current time

**Constraints**:
- Cannot select future dates
- Cannot select dates before app install

---

### Goal Setting
**Context**: Creating a new goal

**Pattern**: Multi-step form (inline, not wizard)

\`\`\`
1. Goal name (text input)
2. Target value (number + unit)
3. Frequency (radio: daily/weekly)
4. Start date (date picker)
\`\`\`

**Validation**:
- Real-time (on blur)
- Inline error messages
- Disable submit until valid

---

## Gesture Patterns (Mobile)

### Swipe Actions
**Context**: Entry cards in history

- **Swipe Left**: Reveal Delete button
- **Swipe Right**: Reveal Edit button
- **Threshold**: 50% of card width
- **Animation**: Smooth spring

### Pull to Refresh
**Context**: History list

- **Trigger**: Pull down from top
- **Threshold**: 80px
- **Feedback**: Loading spinner
- **Action**: Reload entries from localStorage

### Pinch to Zoom
**Context**: Charts (optional)

- **Action**: Zoom into chart
- **Feedback**: Scale animation
- **Reset**: Double-tap

---

## Feedback Patterns

### Success Feedback
**Pattern**: Toast notification (top-right)
**Duration**: 2-3 seconds
**Auto-dismiss**: Yes

**Examples**:
- ✅ "Entry logged successfully"
- ✅ "Goal created"
- ✅ "Settings saved"

### Error Feedback
**Pattern**: Inline error message (below input)
**Duration**: Persistent until fixed
**Auto-dismiss**: No

**Examples**:
- ❌ "Value must be greater than 0"
- ❌ "Goal name is required"

### Loading Feedback
**Pattern**: Skeleton screens (not spinners)
**Duration**: Until data loads
**Animation**: Shimmer effect

---

## Touch Targets

### Minimum Sizes
- **Buttons**: 44×44px (iOS HIG)
- **Input fields**: 48px height (Material Design)
- **List items**: 56px height

### Spacing
- **Between targets**: 8px minimum
- **Padding around text**: 12px minimum

### States
- **Default**: Base color
- **Hover**: Darken 10%
- **Active**: Darken 20%
- **Disabled**: 40% opacity

---

## Keyboard Shortcuts (Desktop)

### Global
- \`Cmd/Ctrl + N\` - New entry (quick log)
- \`Cmd/Ctrl + G\` - New goal
- \`Cmd/Ctrl + K\` - Command palette (future)
- \`/\` - Focus search

### Navigation
- \`Cmd/Ctrl + 1-5\` - Switch tabs
- \`Esc\` - Close modal/dialog
- \`Tab\` - Next field
- \`Shift + Tab\` - Previous field

### Actions
- \`Enter\` - Submit form / Save
- \`Cmd/Ctrl + S\` - Save (in forms)
- \`Cmd/Ctrl + Z\` - Undo delete (future)

---

## Confirmation Patterns

### Destructive Actions
**Pattern**: Modal dialog with explicit confirmation

**Example**: Delete all data
\`\`\`
┌────────────────────────────┐
│  Delete All Data?          │
├────────────────────────────┤
│  This cannot be undone.    │
│  Your entries will be      │
│  permanently deleted.      │
│                            │
│  [ Cancel ]  [ Delete All ]│
└────────────────────────────┘
\`\`\`

**Required**:
- Type "DELETE" to confirm (for critical actions)
- Red button color
- Focus on Cancel by default

### Non-Destructive Actions
**Pattern**: Inline confirmation or toast undo

**Example**: Delete single entry
- Action: Entry deleted immediately
- Feedback: Toast with "Undo" button (5s)
- Undo: Restores entry

---

## Empty States

### Pattern
\`\`\`
┌────────────────────────────┐
│          ┌───┐             │
│          │ 📊 │             │ ← Illustration
│          └───┘             │
│                            │
│   No entries yet           │ ← Message
│                            │
│   Track your first habit   │ ← Description
│   to see your progress     │
│                            │
│   [  Log Your First Day  ] │ ← CTA
└────────────────────────────┘
\`\`\`

**Elements**:
1. **Illustration**: Friendly, on-brand
2. **Message**: Short, clear
3. **Description**: Explain what happens next
4. **CTA**: Action-oriented button

---

## Loading Patterns

### Initial Load
**Pattern**: Skeleton screens

\`\`\`
┌────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓              │ ← Skeleton card
│  ▓▓▓▓▓▓                    │
│                            │
│  ▓▓▓▓▓▓▓▓▓▓▓▓              │
│  ▓▓▓▓▓▓                    │
└────────────────────────────┘
\`\`\`

### Infinite Scroll
**Pattern**: Loading indicator at bottom

\`\`\`
[Entry 1]
[Entry 2]
...
[Entry 20]
   ⏳ Loading more...
\`\`\`

### Optimistic UI
**Pattern**: Update UI immediately, rollback if fails

**Example**: Create goal
1. Add goal to list immediately
2. Show loading state on goal card
3. Persist to localStorage
4. If fails: Remove from list + show error

---

## Accessibility Patterns

### Focus Management
- Modal opens → Focus on first input
- Modal closes → Focus returns to trigger
- Form error → Focus on first error

### Screen Reader Announcements
- **Route change**: "Navigated to Progress screen"
- **Action success**: "Entry logged successfully"
- **Error**: "Error: Invalid value"
- **Loading**: "Loading entries"

### Keyboard Navigation
- All interactive elements focusable
- Visible focus indicator
- Logical tab order

### Color Contrast
- Text: 4.5:1 minimum (WCAG AA)
- Large text: 3:1 minimum
- Interactive elements: 3:1 minimum

---

## Responsive Patterns

### Mobile (<768px)
- Bottom sheet modals
- Full-width buttons
- Stacked layouts
- Touch-optimized

### Tablet (768-1024px)
- Split view (list + detail)
- Floating modals
- Hybrid navigation

### Desktop (>1024px)
- Sidebar navigation
- Multi-column layouts
- Hover states
- Keyboard shortcuts

---

## References

**Standards**:
- [iOS Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [Material Design](https://material.io/design)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)

**PRD Cross-References**:
- See \`prd/01-personas.md\` for user context
- See \`architecture-tech-stack.md\` for UI framework
`;
}

// Generate all UX documents
console.log('📄 Generating screen map...');
const screenMapContent = generateScreenMap(requirements);
const screenMapPath = path.join(outputDir, 'ux-screen-map.md');
fs.writeFileSync(screenMapPath, screenMapContent);
console.log('   ✅ ux-screen-map.md');

console.log('📄 Generating states & transitions...');
const statesContent = generateStates(requirements);
const statesPath = path.join(outputDir, 'ux-states.md');
fs.writeFileSync(statesPath, statesContent);
console.log('   ✅ ux-states.md');

console.log('📄 Generating interaction patterns...');
const interactionsContent = generateInteractions(requirements);
const interactionsPath = path.join(outputDir, 'ux-interactions.md');
fs.writeFileSync(interactionsPath, interactionsContent);
console.log('   ✅ ux-interactions.md');

console.log('\n✅ UX Flow Documentation generated!');
console.log(`📂 Output: ${outputDir}/\n`);
console.log('UX documentation complete (3 documents):');
console.log('  ✅ ux-screen-map.md');
console.log('  ✅ ux-states.md');
console.log('  ✅ ux-interactions.md');

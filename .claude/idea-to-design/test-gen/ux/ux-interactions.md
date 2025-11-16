# User Interaction Patterns

## Overview

HydroTrack follows **mobile-first interaction patterns** optimized for quick, frequent logging while maintaining full desktop functionality.

---

## Input Patterns

### Quick Value Entry
**Context**: Logging water intake

**Mobile**:
```
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
```

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

```
1. Goal name (text input)
2. Target value (number + unit)
3. Frequency (radio: daily/weekly)
4. Start date (date picker)
```

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
- `Cmd/Ctrl + N` - New entry (quick log)
- `Cmd/Ctrl + G` - New goal
- `Cmd/Ctrl + K` - Command palette (future)
- `/` - Focus search

### Navigation
- `Cmd/Ctrl + 1-5` - Switch tabs
- `Esc` - Close modal/dialog
- `Tab` - Next field
- `Shift + Tab` - Previous field

### Actions
- `Enter` - Submit form / Save
- `Cmd/Ctrl + S` - Save (in forms)
- `Cmd/Ctrl + Z` - Undo delete (future)

---

## Confirmation Patterns

### Destructive Actions
**Pattern**: Modal dialog with explicit confirmation

**Example**: Delete all data
```
┌────────────────────────────┐
│  Delete All Data?          │
├────────────────────────────┤
│  This cannot be undone.    │
│  Your entries will be      │
│  permanently deleted.      │
│                            │
│  [ Cancel ]  [ Delete All ]│
└────────────────────────────┘
```

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
```
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
```

**Elements**:
1. **Illustration**: Friendly, on-brand
2. **Message**: Short, clear
3. **Description**: Explain what happens next
4. **CTA**: Action-oriented button

---

## Loading Patterns

### Initial Load
**Pattern**: Skeleton screens

```
┌────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓              │ ← Skeleton card
│  ▓▓▓▓▓▓                    │
│                            │
│  ▓▓▓▓▓▓▓▓▓▓▓▓              │
│  ▓▓▓▓▓▓                    │
└────────────────────────────┘
```

### Infinite Scroll
**Pattern**: Loading indicator at bottom

```
[Entry 1]
[Entry 2]
...
[Entry 20]
   ⏳ Loading more...
```

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
- See `prd/01-personas.md` for user context
- See `architecture-tech-stack.md` for UI framework

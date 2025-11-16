# Weight Tracker Enhancement Sprint - Implementation Plan
**Partner Demo Preparation**

**Date**: October 25, 2025
**Sprint Goal**: Add Splash Screen → Login → Dashboard flow with authentication
**Coordinated with**: Gemini CLI (routing/analytics), Cursor AI (code edits)

---

## 📊 Current State Summary

### ✅ What We Have
- **Core App**: Fully functional Weight Tracker with 5 screens
  - DashboardScreen, HistoryScreen, LogEntryScreen, AnalyticsScreen, SettingsScreen
- **Design System**: PillButton, MetricCard components ready
- **Data Management**: WeightContext with full CRUD operations
- **Splash Prototypes**: 6 variations in `src/components/splash-prototypes/`
  - SplashScreenV1, V2, V3 (newer versions)
  - SplashScreen1, 2, 3 (older versions)
  - All rated 0.53/1.0 (mediocre - need improvement)
- **Navigation**: Screen-based routing via state in `page.tsx`
- **Tech Stack**: Next.js 14, React 18, TypeScript, Tailwind 4, Heroicons
- **Dependencies**: All installed, no missing packages

### ❌ What's Missing
- **AuthContext**: No authentication system
- **LoginScreen**: No login UI
- **UserIndicator**: No user identity display
- **SplashScreen**: No integrated splash (prototypes not connected)
- **Navigation Flow**: No splash → login → app routing
- **Session Management**: No persistent login state
- **User Data**: No user profile/preferences storage

### 🔍 Technical Debt Identified
- Splash prototypes have low quality scores (0.53/1.0)
- No localStorage/sessionStorage integration
- No error boundaries for auth failures
- No loading states for authentication

---

## 🎯 Implementation Plan

### PHASE 1: AuthContext Foundation (60 min)
**Priority**: P0 (Blocking)
**File**: `src/context/AuthContext.tsx` (NEW)

**Tasks**:
1. **Create AuthContext with TypeScript interfaces**
   ```typescript
   interface User {
     id: string;
     username: string;
     emoji: string;
     loginTime: number;
   }

   interface AuthContextType {
     isAuthenticated: boolean;
     user: User | null;
     login: (username: string, password: string) => Promise<boolean>;
     logout: () => void;
   }
   ```

2. **Implement localStorage session persistence**
   - Key: `weightTracker_session`
   - Store: `{ user, loginTime, expiresAt }`
   - Auto-logout after 24 hours

3. **Add demo credentials validation**
   - Username: `demo`
   - Password: `weighttracker2025`
   - In production: hash passwords, use Supabase Auth

4. **Error handling**
   - Invalid credentials message
   - Session expiry detection
   - Clear all data on logout

**Acceptance Criteria**:
- [ ] AuthContext exports useAuth hook
- [ ] login() validates credentials and sets session
- [ ] logout() clears localStorage and resets state
- [ ] Session persists across browser refreshes
- [ ] Auto-logout after 24 hours

**Testing**:
```bash
# Manual test in browser console
localStorage.setItem('weightTracker_session', JSON.stringify({
  user: { id: '1', username: 'demo', emoji: '🏃', loginTime: Date.now() },
  expiresAt: Date.now() + 86400000
}));
# Refresh page - should stay logged in
```

---

### PHASE 2: LoginScreen Component (45 min)
**Priority**: P0 (Blocking)
**File**: `src/components/LoginScreen.tsx` (NEW)

**Tasks**:
1. **Build login form UI**
   - Username input (text)
   - Password input (type="password")
   - "Remember Me" checkbox (optional)
   - "Login" PillButton (variant="primary")
   - Demo credentials hint box

2. **Integrate with AuthContext**
   - useAuth() hook
   - Call login() on form submit
   - Handle loading state
   - Display error messages

3. **Styling**
   - Match Weight Tracker design system
   - Use gradient background (red-to-green theme)
   - Center card layout (max-width 400px)
   - Mobile-responsive

4. **Accessibility**
   - Label all inputs
   - ARIA attributes
   - Keyboard navigation (Tab, Enter)
   - Focus management

**Acceptance Criteria**:
- [ ] Form submits on Enter key
- [ ] Loading spinner during authentication
- [ ] Error message for invalid credentials
- [ ] Success redirects to dashboard
- [ ] Demo credentials clearly displayed

**Design Specification**:
```tsx
<div style={{ background: 'linear-gradient(135deg, #dc2626, #22c55e)' }}>
  <div className="card">
    <h1>Welcome to Weight Tracker Pro</h1>
    <form onSubmit={handleLogin}>
      <input type="text" placeholder="Username" />
      <input type="password" placeholder="Password" />
      <PillButton type="submit" variant="primary">Login</PillButton>
    </form>
    <div className="demo-hint">
      Demo: username=demo, password=weighttracker2025
    </div>
  </div>
</div>
```

---

### PHASE 3: UserIndicator Component (30 min)
**Priority**: P1 (High)
**File**: `src/components/UserIndicator.tsx` (NEW)

**Tasks**:
1. **Create top-right user display**
   - Circular avatar with emoji
   - Username text (optional, toggle)
   - Dropdown menu on click

2. **Dropdown menu options**
   - "Profile" (placeholder, navigate to settings)
   - "Settings" (navigate to settings)
   - Divider
   - "Logout" (call logout, redirect to splash)

3. **State management**
   - useState for menu open/close
   - Click outside to close (useEffect + ref)
   - Conditional rendering (only show if authenticated)

4. **Styling**
   - Position: fixed top-right
   - z-index: 1000 (above other content)
   - Smooth dropdown animation
   - Match design system colors

**Acceptance Criteria**:
- [ ] Avatar shows user emoji
- [ ] Menu toggles on click
- [ ] Clicks outside close menu
- [ ] Logout clears session and redirects
- [ ] Only renders when authenticated

**Component Structure**:
```tsx
<div className="user-indicator">
  <button onClick={toggleMenu}>
    <span className="emoji">{user.emoji}</span>
    <span className="username">{user.username}</span>
  </button>
  {menuOpen && (
    <div className="dropdown-menu">
      <button onClick={() => navigate('settings')}>Settings</button>
      <button onClick={handleLogout}>Logout</button>
    </div>
  )}
</div>
```

---

### PHASE 4: SplashScreen Selection & Enhancement (45 min)
**Priority**: P1 (High)
**Decision Required**: Select best prototype OR create new splash

**Options**:

**Option A: Use Existing Prototype (Quick)**
- Select SplashScreenV3 (most recent)
- Add "Start Your Journey" PillButton
- Connect to navigation flow
- **Pros**: Fast, already built
- **Cons**: Low quality score (0.53)

**Option B: Create New Splash (Better Quality)**
- Build new SplashScreen.tsx from scratch
- Follow WEIGHT_TRACKER_ENHANCEMENT_PLAN.md design
- Animated "before/after" transformation
- **Pros**: Better quality, custom-tailored
- **Cons**: More time (45 min vs 15 min)

**Recommendation**: **Option B** - Create new splash for partner demo quality

**Tasks** (if Option B):
1. **Create SplashScreen.tsx**
   - Full-screen gradient background
   - Centered content area
   - Animated emoji transformation (🧑‍💼 → 🏃)
   - Compelling headline: "Transform Your Life, One Weigh-In at a Time"
   - "Start Your Journey" PillButton

2. **CSS Animation**
   ```css
   @keyframes transformation {
     0% { transform: scale(1) rotate(0deg); opacity: 1; }
     25% { transform: scale(1.1) rotate(2deg); opacity: 0.8; }
     50% { transform: scale(1.2) rotate(0deg); opacity: 0.3; }
     75% { transform: scale(1.1) rotate(-2deg); opacity: 0.8; }
     100% { transform: scale(1) rotate(0deg); opacity: 1; }
   }
   ```

3. **Character swap logic**
   - Emoji array: ['🧑‍💼', '🏃', '💪', '🎯']
   - Cycle every 3 seconds
   - Smooth crossfade transition

**Acceptance Criteria**:
- [ ] Smooth 3-second animation loop
- [ ] Compelling copy visible
- [ ] CTA button navigates to login
- [ ] Mobile-responsive layout
- [ ] Accessible (prefers-reduced-motion support)

---

### PHASE 5: Navigation Flow Integration (30 min)
**Priority**: P0 (Blocking)
**File**: `src/app/page.tsx` (MODIFIED)

**Tasks**:
1. **Add authentication state**
   ```typescript
   const [appState, setAppState] = useState<'splash' | 'login' | 'app'>('splash');
   ```

2. **Update routing logic**
   ```typescript
   const renderScreen = () => {
     if (!isAuthenticated && appState === 'splash') {
       return <SplashScreen onContinue={() => setAppState('login')} />;
     }
     if (!isAuthenticated && appState === 'login') {
       return <LoginScreen onLogin={() => setAppState('app')} />;
     }
     if (isAuthenticated) {
       return renderAuthenticatedScreens();
     }
   };
   ```

3. **Wrap app with AuthProvider**
   ```tsx
   <AuthProvider>
     <WeightProvider>
       {renderScreen()}
     </WeightProvider>
   </AuthProvider>
   ```

4. **Add session check on mount**
   ```typescript
   useEffect(() => {
     if (isAuthenticated) {
       setAppState('app');
     }
   }, [isAuthenticated]);
   ```

**Acceptance Criteria**:
- [ ] Fresh load shows splash screen
- [ ] Splash → Login → Dashboard flow works
- [ ] Authenticated users skip to dashboard
- [ ] Logout returns to splash screen
- [ ] No flicker on page load

---

### PHASE 6: Add UserIndicator to All Screens (20 min)
**Priority**: P1 (High)
**Files**: All 5 screen components (MODIFIED)

**Tasks**:
1. **Import UserIndicator and useAuth**
   ```typescript
   import { UserIndicator } from '../components/UserIndicator';
   import { useAuth } from '../context/AuthContext';
   ```

2. **Add to each screen's JSX**
   ```tsx
   const { isAuthenticated } = useAuth();

   return (
     <div className="screen-container">
       {isAuthenticated && <UserIndicator />}
       {/* existing screen content */}
     </div>
   );
   ```

**Files to Update**:
- `src/components/DashboardScreen.tsx`
- `src/components/HistoryScreen.tsx`
- `src/components/LogEntryScreen.tsx`
- `src/components/AnalyticsScreen.tsx`
- `src/components/SettingsScreen.tsx`

**Acceptance Criteria**:
- [ ] UserIndicator visible on all authenticated screens
- [ ] Consistent positioning across all screens
- [ ] No layout shift when indicator appears

---

### PHASE 7: Enhanced Logout in Settings (15 min)
**Priority**: P2 (Medium)
**File**: `src/components/SettingsScreen.tsx` (MODIFIED)

**Tasks**:
1. **Add logout button to settings**
   - Position: Bottom of settings page
   - Style: PillButton variant="danger" (red)
   - Confirmation: "Are you sure?" dialog

2. **Implement confirmation dialog**
   - Modal overlay with backdrop
   - "Cancel" and "Confirm Logout" buttons
   - Clear messaging: "Your data will be saved"

3. **Logout logic**
   - Call `logout()` from useAuth
   - Clear WeightContext data (optional - discuss)
   - Redirect to splash screen
   - Show success toast (optional)

**Acceptance Criteria**:
- [ ] Logout button visible in settings
- [ ] Confirmation dialog prevents accidental logout
- [ ] Successful logout redirects to splash
- [ ] Session cleared from localStorage

---

## 📋 Step-by-Step Coding Checklist for Cursor

### Pre-Flight Checks
- [ ] Confirm `npm install` completed successfully
- [ ] Verify `npm run dev` starts without errors
- [ ] Check all existing screens render correctly
- [ ] Confirm splash prototypes exist in `/src/components/splash-prototypes/`

### Phase 1: AuthContext (Estimated: 60 min)
1. [ ] Create file: `src/context/AuthContext.tsx`
2. [ ] Define TypeScript interfaces: User, AuthContextType
3. [ ] Implement AuthProvider component with useState hooks
4. [ ] Add localStorage integration (getItem/setItem)
5. [ ] Implement login() function with demo credential validation
6. [ ] Implement logout() function with localStorage.clear()
7. [ ] Add session expiry check (24-hour timeout)
8. [ ] Export useAuth custom hook
9. [ ] Test in browser console: login/logout/session persistence

### Phase 2: LoginScreen (Estimated: 45 min)
10. [ ] Create file: `src/components/LoginScreen.tsx`
11. [ ] Build form UI with username/password inputs
12. [ ] Add PillButton for submit
13. [ ] Integrate useAuth hook
14. [ ] Add form submission handler (preventDefault, call login)
15. [ ] Implement loading state (useState)
16. [ ] Add error message display (invalid credentials)
17. [ ] Style with gradient background matching Weight Tracker theme
18. [ ] Add demo credentials hint box
19. [ ] Test: Valid login → success, Invalid → error message

### Phase 3: UserIndicator (Estimated: 30 min)
20. [ ] Create file: `src/components/UserIndicator.tsx`
21. [ ] Build circular avatar with emoji
22. [ ] Add dropdown menu with Settings/Logout options
23. [ ] Implement menu toggle (useState)
24. [ ] Add click-outside-to-close logic (useEffect + ref)
25. [ ] Style with fixed position top-right
26. [ ] Connect logout button to useAuth().logout()
27. [ ] Test: Menu opens/closes, logout works

### Phase 4: SplashScreen (Estimated: 45 min)
**Option A (Quick - 15 min)**:
28a. [ ] Copy `SplashScreenV3.tsx` to `SplashScreen.tsx`
29a. [ ] Add "Start Your Journey" PillButton
30a. [ ] Connect button to onContinue prop

**Option B (Better Quality - 45 min)**:
28b. [ ] Create file: `src/components/SplashScreen.tsx`
29b. [ ] Add gradient background (red-to-green)
30b. [ ] Create centered content layout
31b. [ ] Add headline: "Transform Your Life, One Weigh-In at a Time"
32b. [ ] Implement animated emoji transformation (🧑‍💼 → 🏃)
33b. [ ] Add CSS keyframes for animation
34b. [ ] Add PillButton: "Start Your Journey"
35b. [ ] Test animation smoothness, responsive layout

### Phase 5: Navigation Flow (Estimated: 30 min)
36. [ ] Update `src/app/page.tsx`
37. [ ] Import AuthProvider from AuthContext
38. [ ] Wrap app with `<AuthProvider>`
39. [ ] Add appState useState: 'splash' | 'login' | 'app'
40. [ ] Implement renderScreen() routing logic
41. [ ] Add useEffect for session check on mount
42. [ ] Test flow: Splash → Login → Dashboard
43. [ ] Test: Refresh page while logged in → stays logged in

### Phase 6: Add UserIndicator to Screens (Estimated: 20 min)
44. [ ] Update `DashboardScreen.tsx` - import + render UserIndicator
45. [ ] Update `HistoryScreen.tsx` - import + render UserIndicator
46. [ ] Update `LogEntryScreen.tsx` - import + render UserIndicator
47. [ ] Update `AnalyticsScreen.tsx` - import + render UserIndicator
48. [ ] Update `SettingsScreen.tsx` - import + render UserIndicator
49. [ ] Test: UserIndicator appears on all screens

### Phase 7: Enhanced Logout (Estimated: 15 min)
50. [ ] Update `SettingsScreen.tsx`
51. [ ] Add logout button at bottom
52. [ ] Implement confirmation dialog modal
53. [ ] Connect logout to useAuth().logout()
54. [ ] Test: Logout from settings → redirects to splash

### Final Testing & Validation (Estimated: 30 min)
55. [ ] **Full Flow Test**: Splash → Login → Dashboard → Navigate all screens → Logout → Splash
56. [ ] **Session Persistence**: Login → Close browser → Reopen → Still logged in
57. [ ] **Error Handling**: Try invalid credentials → See error message
58. [ ] **Mobile Responsive**: Test on mobile viewport (DevTools)
59. [ ] **Accessibility**: Tab navigation, screen reader labels
60. [ ] **Performance**: Check animation FPS, no jank

---

## 🧪 Testing & Validation

### Manual Test Cases

**Test 1: Fresh User Journey**
1. Open app in incognito window
2. Verify splash screen appears
3. Click "Start Your Journey"
4. Verify login screen appears
5. Enter demo credentials
6. Verify dashboard appears
7. Navigate to all 5 screens
8. Verify UserIndicator visible on each
9. Click UserIndicator → Logout
10. Verify returns to splash screen

**Expected**: All steps pass without errors

**Test 2: Session Persistence**
1. Login with demo credentials
2. Navigate to analytics screen
3. Refresh browser (F5)
4. Verify still on analytics screen (authenticated)
5. Wait 24 hours (or modify timeout to 10 seconds for testing)
6. Refresh browser
7. Verify redirected to splash (session expired)

**Expected**: Session persists until expiry

**Test 3: Error Handling**
1. On login screen, enter invalid username
2. Click login
3. Verify error message appears
4. Enter valid username but invalid password
5. Click login
6. Verify error message appears
7. Enter valid credentials
8. Verify successful login

**Expected**: Clear error messages, no crashes

### Automated Tests (Optional - Future)
```javascript
// tests/e2e/auth-flow.spec.ts
describe('Authentication Flow', () => {
  it('should navigate from splash to dashboard', async () => {
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Transform Your Life');
    await page.click('button:has-text("Start Your Journey")');
    await expect(page.locator('h1')).toContainText('Welcome to Weight Tracker');
    await page.fill('input[type="text"]', 'demo');
    await page.fill('input[type="password"]', 'weighttracker2025');
    await page.click('button:has-text("Login")');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
});
```

---

## ⚠️ Risks / Dependencies

### BLOCKERS
1. **Gemini Routing Notes Pending**
   - **Impact**: Cannot deploy multi-DBA routing until domain config complete
   - **Mitigation**: Proceed with authentication on single domain
   - **Status**: ⏳ Waiting for Gemini research completion

2. **No Backend Authentication**
   - **Impact**: Demo credentials hardcoded, not production-ready
   - **Mitigation**: Document Supabase migration path
   - **Status**: ⚠️ Acceptable for partner demo, must upgrade for prod

### DEPENDENCIES
1. **Existing Design System**
   - **Status**: ✅ PillButton and MetricCard ready
   - **Risk**: Low

2. **localStorage Browser API**
   - **Status**: ✅ Supported in all modern browsers
   - **Risk**: Low (incognito mode may block, but acceptable)

3. **React Context API**
   - **Status**: ✅ Already using WeightContext successfully
   - **Risk**: Low

### RISKS
1. **Splash Screen Quality**
   - **Risk**: Existing prototypes rated 0.53/1.0 (low quality)
   - **Mitigation**: Create new splash from scratch (Phase 4 Option B)
   - **Decision**: Choose quality over speed for partner demo

2. **Animation Performance**
   - **Risk**: CSS animations may jank on low-end devices
   - **Mitigation**: Add `prefers-reduced-motion` support, use GPU-accelerated transforms
   - **Testing**: Test on mobile Chrome DevTools throttling

3. **Session Security**
   - **Risk**: localStorage vulnerable to XSS attacks
   - **Mitigation**: Acceptable for demo, document upgrade to httpOnly cookies + Supabase Auth
   - **Production Path**: Migrate to Supabase Auth before public launch

4. **Data Persistence Confusion**
   - **Risk**: Users expect weight data to persist per-user, but currently shared
   - **Mitigation**: Add clear messaging: "Demo mode - data is local only"
   - **Production Path**: Add user_id to WeightContext, store in Supabase

---

## 📝 Hand-off Notes for Cursor

### Commands to Run

**Start Development Server**:
```bash
cd software-factory/generated-apps/weight-tracker-nextjs
npm run dev
# Open http://localhost:3000
```

**Build for Production**:
```bash
npm run build
npm run start
```

**Run Visual Tests** (after implementation):
```bash
npm run test:visual
```

### Code Style Guidelines
- **TypeScript**: Use strict typing, no `any` types
- **React**: Functional components only, hooks for state
- **Styling**: CSS-in-JS with inline styles (matching existing pattern)
- **Naming**: PascalCase for components, camelCase for functions
- **Comments**: Add JSDoc comments for public functions

### File Locations
```
src/
├── context/
│   ├── AuthContext.tsx          [CREATE NEW]
│   └── WeightContext.tsx         [EXISTING]
├── components/
│   ├── SplashScreen.tsx         [CREATE NEW]
│   ├── LoginScreen.tsx          [CREATE NEW]
│   ├── UserIndicator.tsx        [CREATE NEW]
│   ├── DashboardScreen.tsx      [MODIFY - add UserIndicator]
│   ├── HistoryScreen.tsx        [MODIFY - add UserIndicator]
│   ├── LogEntryScreen.tsx       [MODIFY - add UserIndicator]
│   ├── AnalyticsScreen.tsx      [MODIFY - add UserIndicator]
│   └── SettingsScreen.tsx       [MODIFY - add UserIndicator + logout]
└── app/
    └── page.tsx                 [MODIFY - add auth routing]
```

### Design Tokens (Use Existing)
```typescript
// Colors (from current theme)
const colors = {
  red: '#dc2626',      // Start of progress gradient
  green: '#22c55e',    // End of progress gradient
  amber: '#f59e0b',    // Middle warning color
  gray: '#6b7280',     // Secondary text
  white: '#ffffff',    // Primary text
};

// Spacing
const spacing = {
  xs: '0.5rem',
  sm: '1rem',
  md: '1.5rem',
  lg: '2rem',
  xl: '3rem',
};

// Border radius (from PillButton)
const borderRadius = {
  pill: '9999px',
  card: '1rem',
};
```

### Critical Integration Points
1. **AuthContext must export useAuth hook** - Used by LoginScreen, UserIndicator, and page.tsx
2. **SplashScreen must accept onContinue prop** - Called when "Start Your Journey" clicked
3. **LoginScreen must accept onLogin prop** - Called after successful authentication
4. **UserIndicator must use fixed positioning** - z-index: 1000, top-right corner
5. **All screens must conditionally render UserIndicator** - Only when `isAuthenticated === true`

### Environment Variables (None Required for Demo)
```bash
# For future Supabase integration
# NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
# NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
```

### Debugging Tips
```javascript
// Check auth state in browser console
localStorage.getItem('weightTracker_session')

// Force logout
localStorage.removeItem('weightTracker_session')
window.location.reload()

// Check if authenticated
// In React DevTools, find AuthProvider and inspect context value
```

---

## ⏳ Status Update

**Current Phase**: Planning Complete ✅
**Next Action**: **WAITING FOR GEMINI** to complete domain routing + analytics research

**Ready for Cursor to Begin Coding**:
- ✅ Implementation plan finalized
- ✅ File structure defined
- ✅ Step-by-step checklist provided
- ✅ Testing strategy documented
- ✅ Risks identified and mitigated
- ⏳ Awaiting Gemini routing notes before deployment

**Estimated Total Implementation Time**: 4-5 hours
**Recommended Approach**: Implement in order (Phase 1 → Phase 7)
**Critical Path**: AuthContext → LoginScreen → Navigation Flow (Phases 1, 2, 5)

---

## 🚀 Quick Start for Cursor

**Step 1**: Create AuthContext
```bash
# Create new file
touch src/context/AuthContext.tsx
# Implement using checklist items 1-9
```

**Step 2**: Create LoginScreen
```bash
# Create new file
touch src/components/LoginScreen.tsx
# Implement using checklist items 10-19
```

**Step 3**: Test Basic Auth Flow
```bash
npm run dev
# Navigate to login → enter demo/weighttracker2025 → verify dashboard loads
```

**Step 4**: Continue with remaining phases
- Follow checklist items 20-54 in order
- Test after each phase completion
- Commit changes after each successful test

---

**End of Implementation Plan**
**Next Update**: After Gemini completes routing research
**Questions/Blockers**: Escalate to coordination chat

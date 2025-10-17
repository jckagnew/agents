# Weight Tracker - Architecture & Implementation Plan

## 🎯 Project Overview
**Privacy-first weight tracker** with trend clarity over daily noise. Free tier is genuinely useful; Pro unlocks deeper control and insights.

## 🏗️ Architecture Sketch

### **Tech Stack (P0)**
- **Framework**: React Native + Expo (TypeScript)
- **Storage**: SQLite (expo-sqlite) for records; MMKV for settings
- **Dates/TZ**: Luxon
- **Charts**: Victory Native
- **State**: Zustand
- **Tests**: Jest + React Testing Library
- **Lint/format**: ESLint + Prettier
- **Min OS**: iOS 14 / Android 8

### **Data Architecture**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SQLite DB     │    │   MMKV Store    │    │   Calculations  │
│                 │    │                 │    │                 │
│ Daily Records   │    │ Settings        │    │ Navy BF%        │
│ - date          │    │ - plan          │    │ WHR             │
│ - measurements  │    │ - preferences   │    │ Smoothing       │
│ - flags         │    │ - units         │    │ % Change        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **Smoothing Approach**
- **7D_min4**: Simple average of last 7 calendar days
- Requires ≥4 values, otherwise null
- Used for trend analysis and % change calculations

### **Gating Hooks**
```typescript
interface GatingFlags {
  allowMultipleEntriesPerDay: boolean;
  allowCustomBF: boolean;
  allowWHRTrend: boolean;
  allowGoalMoving: boolean;
  allowSmoothingChange: boolean;
  maxSavedCustomRanges: number;
  allowPhotoJournal: boolean;
  allowExport: boolean;
}
```

## 📅 Milestones & Timeline

### **P0 Development (4 weeks)**
- **Week 1**: Project setup, data model, core algorithms
- **Week 2**: P0 screens implementation
- **Week 3**: Gating system, testing, validation
- **Week 4**: Polish, acceptance tests, deployment prep

### **v1 Development (6 weeks)**
- **Weeks 5-6**: Pro features, advanced analytics
- **Weeks 7-8**: Photo journal, cloud sync
- **Weeks 9-10**: Advanced reporting, exports

## 💰 Pricing Structure

### **P0 (MVP)**
- **Fixed Bid**: $15,000
- **Deliverables**: Complete P0 functionality as specified
- **Timeline**: 4 weeks
- **Acceptance**: All acceptance tests pass

### **v1 (Full Feature)**
- **Fixed Bid**: $25,000
- **Deliverables**: All Pro features, advanced analytics
- **Timeline**: 6 weeks (after P0)
- **Acceptance**: Full feature parity with requirements

## ⚠️ Risk Assessment

### **High Risk**
- **Privacy Compliance**: On-device storage requirements
- **Math Accuracy**: Navy BF% calculations must match fixtures exactly
- **Timezone Handling**: Complex edge cases with device timezone

### **Medium Risk**
- **Performance**: SQLite queries with large datasets
- **Cross-platform**: iOS/Android compatibility
- **State Management**: Complex state with gating logic

### **Low Risk**
- **UI/UX**: Standard React Native patterns
- **Charts**: Victory Native is well-documented
- **Testing**: Standard testing frameworks

## 🔧 Tooling Choices

### **Development**
- **Repository**: Client's private repo (Day 1)
- **CI/CD**: GitHub Actions (Client's account)
- **Analytics**: Client's analytics account
- **Crash Reporting**: Client's crash reporting service

### **Build & Deploy**
- **iOS**: Client's Apple Developer account
- **Android**: Client's Google Play Console
- **Expo**: Client's Expo account
- **Least Privilege**: Minimal access required

## 🎯 Success Criteria

### **Technical**
- ✅ Daily logging loop feels fast, reliable, and private
- ✅ Numbers match test fixtures for Navy BF/Fat/Lean/Goal (±0.1)
- ✅ Free/Pro gates behave exactly as specified
- ✅ Teasers appear at the right moments

### **Business**
- ✅ Free tier is genuinely useful
- ✅ Pro tier provides clear value proposition
- ✅ Privacy-first approach maintained
- ✅ On-device compute requirements met

## 📊 Acceptance Tests

### **Math Parity**
- Navy BF% calculations match fixtures (±0.1)
- Fat Mass and Lean Mass calculations accurate
- WHR calculations and categories correct

### **Smoothing**
- 7D_min4 values match expected
- Percent change uses smoothed baseline
- Requires ≥4 values for smoothing

### **Gating**
- Free: one entry/day with Replace/Cancel prompt
- Free: smoothing control locked to 7D_min4
- Free: WHR shows snapshot only
- Free: static goal doesn't auto-change

### **Timezone**
- Local day boundary per device timezone
- Fallback to America/Chicago if timezone unavailable

## 🚀 Implementation Strategy

### **Phase 1: Foundation (Week 1)**
1. Project setup with Expo + TypeScript
2. SQLite database schema
3. MMKV settings store
4. Core calculation algorithms
5. Unit tests for calculations

### **Phase 2: Core Features (Week 2)**
1. Dashboard screen with charts
2. Log entry screen with validation
3. History screen with calendar view
4. Settings screen with preferences
5. Basic navigation

### **Phase 3: Gating & Polish (Week 3)**
1. Free/Pro gating system
2. Paywall/upgrade screens
3. Teaser implementations
4. Outlier detection
5. Timezone handling

### **Phase 4: Testing & Deploy (Week 4)**
1. Acceptance test implementation
2. Fixture validation
3. Performance optimization
4. Build configuration
5. Deployment preparation

## 💡 Key Assumptions

### **Technical**
- SQLite performance sufficient for expected data volume
- Victory Native charts meet visualization requirements
- Expo provides sufficient native functionality
- Device storage adequate for local data

### **Business**
- Free tier provides sufficient value for user retention
- Pro tier features justify subscription cost
- Privacy-first approach aligns with user expectations
- On-device compute meets performance requirements

### **User Experience**
- Daily logging workflow is intuitive
- Chart visualizations are clear and actionable
- Gating doesn't feel restrictive
- Teasers effectively drive upgrades

## 🔒 Privacy & Security

### **Data Protection**
- All data stored locally on device
- No cloud sync in P0
- Photos deleted immediately (unless Photo Journal enabled)
- EXIF data stripped from photos
- Encryption at rest for Photo Journal (Pro feature)

### **Compliance**
- No personal data transmitted to external services
- User controls all data retention
- Clear privacy policy and data handling
- GDPR/CCPA compliant by design

---

**This architecture provides a solid foundation for building a privacy-first, feature-rich weight tracking application that meets all specified requirements while maintaining flexibility for future enhancements.**

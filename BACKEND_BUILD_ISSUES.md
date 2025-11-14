# Backend Build Issues

**Date**: 2025-11-14
**Status**: ❌ Backend has TypeScript compilation errors
**Blocker**: Cannot deploy to Railway until build succeeds

---

## 🔍 Discovery

Attempted to build the backend for Railway deployment:
```bash
npm run build:backend  # Runs: tsc
```

**Result**: 30+ TypeScript compilation errors

---

## 📋 TypeScript Errors Summary

### 1. Missing getInstance() Static Methods
Multiple services are missing the singleton `getInstance()` method:
- `QuotaService` (used in server.ts, ai-agent-orchestrator)
- `ErrorRecoveryService` (used in ai-agent-orchestrator)

**Error Example**:
```
apps/factory/src/api/server.ts(35,35): error TS2339:
Property 'getInstance' does not exist on type 'typeof QuotaService'.
```

### 2. Missing SupabaseService Methods
The `SupabaseService` class is missing several methods that are being called:
- `createProject()`
- `updateProject()`
- `saveCodeArtifact()`
- `packageProjectAsZip()`

**Error Example**:
```
apps/factory/src/services/express-tier.service.ts(131,38): error TS2339:
Property 'createProject' does not exist on type 'SupabaseService'.
```

### 3. Anthropic SDK Type Issues
The Anthropic client doesn't have expected `.messages` property:
```
apps/factory/src/services/ai-agent-orchestrator.service.ts(452,48): error TS2339:
Property 'messages' does not exist on type 'Anthropic'.
```

### 4. Type Safety Issues
- Unknown type errors (need proper error typing)
- Null assignment issues
- Missing type exports (PRD, ConversationMessage)

---

## 🎯 Resolution Options

### Option 1: Fix TypeScript Errors (Recommended)
**Pros**: Production-ready, type-safe code
**Cons**: Takes time, requires understanding the codebase
**Estimated Time**: 2-4 hours

**Fix List**:
1. Add `getInstance()` static methods to QuotaService and ErrorRecoveryService
2. Implement missing SupabaseService methods
3. Fix Anthropic SDK usage (use proper API)
4. Add proper error typing
5. Export missing types from prd-generation.service
6. Fix null safety issues

### Option 2: Use ts-node for Development Deployment
**Pros**: Fast, can deploy immediately
**Cons**: Not production-optimized, slower startup
**Estimated Time**: 15 minutes

**Changes Needed**:
```json
// railway.json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm install"
  },
  "deploy": {
    "startCommand": "npm run api",
    "healthcheckPath": "/api/v1/health",
    "healthcheckTimeout": 100
  }
}
```

Update package.json:
```json
"api": "ts-node --transpile-only apps/factory/src/api/server.ts"
```

### Option 3: Disable Type Checking (Not Recommended)
**Pros**: Builds complete
**Cons**: Runtime errors likely, not production-safe

```json
// tsconfig.json
{
  "compilerOptions": {
    "noEmitOnError": false,
    "skipLibCheck": true
  }
}
```

---

## 🔧 Immediate Action Plan

### For Cursor (If You Want Quick Deployment):
Use Option 2 - Deploy with ts-node:

```bash
# 1. Update railway.json
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "npm install"
  },
  "deploy": {
    "startCommand": "npx ts-node apps/factory/src/api/server.ts",
    "healthcheckPath": "/api/v1/health",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF

# 2. Test locally
npm run api:dev
# Should start without compilation

# 3. Deploy to Railway
railway up
```

### For Claude (If You Want Production-Ready):
Fix the TypeScript errors systematically. Start with:

1. **Add getInstance() methods**:
   ```typescript
   // In quota.service.ts and error-recovery.service.ts
   private static instance: ThisServiceType;

   public static getInstance(): ThisServiceType {
     if (!ThisServiceType.instance) {
       ThisServiceType.instance = new ThisServiceType();
     }
     return ThisServiceType.instance;
   }
   ```

2. **Implement SupabaseService methods** or refactor services to not depend on them

3. **Fix Anthropic SDK usage**:
   ```typescript
   // Should be:
   const anthropic = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
   const response = await anthropic.messages.create({ ... });
   ```

---

## 📊 Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Dependencies | ✅ | npm install complete |
| Credentials | ✅ | All validated |
| TypeScript Config | ✅ | Created tsconfig.json |
| Backend Build | ❌ | **30+ compilation errors** |
| Railway Config | ✅ | Exists but expects compiled code |
| Deployment | ⏸️ | **Blocked until build succeeds** |

---

## 🚀 Recommendation

**For Fastest Deployment**:
- Use Option 2 (ts-node)
- Deploy to Railway immediately
- Fix TypeScript errors later as tech debt

**For Best Practice**:
- Use Option 1 (fix errors)
- Ensures production stability
- Takes more time upfront

---

## 📝 Next Steps

**If using ts-node approach**:
1. Update railway.json per Option 2
2. Test locally: `npm run api:dev`
3. Install Railway CLI: `npm install -g @railway/cli`
4. Deploy: `railway login && railway up`

**If fixing TypeScript errors**:
1. Start with QuotaService.getInstance()
2. Add ErrorRecoveryService.getInstance()
3. Review SupabaseService implementation
4. Fix Anthropic SDK usage
5. Build and test: `npm run build:backend && node dist/api/server.js`

---

**Decision Required**: Which approach do you want to take?

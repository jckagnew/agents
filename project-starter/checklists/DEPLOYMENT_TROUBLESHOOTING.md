# Deployment Troubleshooting Checklist - Software Factory

## 🎯 **Purpose**
This checklist helps diagnose and fix common deployment issues quickly and systematically.

## 🚨 **Emergency Checklist (5 minutes)**

### **Step 1: Verify Local Build**
```bash
# Test production build locally
npm run build
npm run start

# Check if app loads at http://localhost:3000
curl -I http://localhost:3000
```

**✅ Success**: App loads without errors
**❌ Failure**: Fix local issues first

### **Step 2: Check TypeScript**
```bash
# Run TypeScript check
npx tsc --noEmit

# Fix any errors
npm run lint -- --fix
```

**✅ Success**: No TypeScript errors
**❌ Failure**: Fix type definitions

### **Step 3: Verify Dependencies**
```bash
# Check for duplicate lockfiles
find . -name "package-lock.json" -not -path "./node_modules/*"

# Clean if needed
rm -rf node_modules package-lock.json
npm install
```

**✅ Success**: Single lockfile, clean install
**❌ Failure**: Clean dependencies

### **Step 4: Test Bundle Size**
```bash
# Analyze bundle
npm run build
npx @next/bundle-analyzer

# Check sizes
ls -la .next/static/chunks/
```

**✅ Success**: Bundle < 1MB
**❌ Failure**: Optimize imports

## 🔍 **Detailed Diagnosis (15 minutes)**

### **Issue: Build Timeouts**
**Symptoms**: Deployment fails with timeout
**Diagnosis**:
```bash
# Check bundle size
npm run build
du -sh .next/static/chunks/*

# Check for large dependencies
npm ls --depth=0
```

**Solutions**:
1. **Code Splitting**:
```typescript
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <div>Loading...</div>,
  ssr: false
});
```

2. **Lazy Loading**:
```typescript
const LazyComponent = lazy(() => import('./LazyComponent'));
```

3. **Remove Unused Dependencies**:
```bash
npx depcheck
npm uninstall unused-package
```

### **Issue: TypeScript Errors**
**Symptoms**: Build fails with TS errors
**Diagnosis**:
```bash
# Check specific errors
npx tsc --noEmit --pretty

# Check tsconfig
cat tsconfig.json
```

**Solutions**:
1. **Fix Type Definitions**:
```typescript
// Instead of empty interface
export interface Props extends React.HTMLAttributes<HTMLDivElement> {}

// Use type alias
export type Props = React.HTMLAttributes<HTMLDivElement>
```

2. **Add Missing Types**:
```bash
npm install @types/package-name
```

3. **Update tsconfig.json**:
```json
{
  "compilerOptions": {
    "strict": false,
    "noEmit": true,
    "skipLibCheck": true
  }
}
```

### **Issue: Memory Issues**
**Symptoms**: Build fails with OOM error
**Diagnosis**:
```bash
# Check memory usage
node --max-old-space-size=4096 node_modules/.bin/next build

# Check for memory leaks
npm run build 2>&1 | grep -i memory
```

**Solutions**:
1. **Optimize Components**:
```typescript
const OptimizedComponent = React.memo(({ data }) => {
  return <div>{/* render */}</div>;
});
```

2. **Implement Cleanup**:
```typescript
useEffect(() => {
  const timer = setInterval(() => {}, 1000);
  return () => clearInterval(timer);
}, []);
```

3. **Use Dynamic Imports**:
```typescript
const Component = dynamic(() => import('./Component'));
```

### **Issue: Dependency Conflicts**
**Symptoms**: Build fails with dependency errors
**Diagnosis**:
```bash
# Check for conflicts
npm ls

# Check peer dependencies
npm ls --depth=0
```

**Solutions**:
1. **Clean Install**:
```bash
rm -rf node_modules package-lock.json
npm install
```

2. **Resolve Conflicts**:
```bash
npm install --legacy-peer-deps
```

3. **Use Exact Versions**:
```json
{
  "dependencies": {
    "react": "18.2.0",
    "react-dom": "18.2.0"
  }
}
```

## 🛠️ **Advanced Troubleshooting (30 minutes)**

### **Issue: Vercel-Specific Errors**
**Symptoms**: Works locally, fails on Vercel
**Diagnosis**:
```bash
# Check Vercel logs
vercel logs

# Check environment variables
vercel env ls
```

**Solutions**:
1. **Environment Variables**:
```bash
# Set in Vercel dashboard
NEXT_PUBLIC_APP_URL=https://your-app.vercel.app
DATABASE_URL=your-db-url
```

2. **Vercel Configuration**:
```json
// vercel.json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "installCommand": "npm install"
}
```

3. **Node.js Version**:
```json
// package.json
{
  "engines": {
    "node": "18.x"
  }
}
```

### **Issue: Runtime Errors**
**Symptoms**: Builds successfully, fails at runtime
**Diagnosis**:
```bash
# Check browser console
# Check Vercel function logs
vercel logs --follow
```

**Solutions**:
1. **Error Boundaries**:
```typescript
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

2. **Progressive Enhancement**:
```typescript
const [isClient, setIsClient] = useState(false);

useEffect(() => {
  setIsClient(true);
}, []);

if (!isClient) return <Loading />;
```

3. **Proper Error Handling**:
```typescript
try {
  const data = await fetch('/api/data');
  if (!data.ok) throw new Error('Failed to fetch');
  return data.json();
} catch (error) {
  console.error('Error:', error);
  return null;
}
```

## 📊 **Performance Optimization**

### **Bundle Size Optimization**
```bash
# Analyze bundle
npm run build
npx @next/bundle-analyzer

# Target sizes
# Main bundle: < 500KB
# Page bundles: < 200KB
# Total JS: < 1MB
```

### **Build Time Optimization**
```bash
# Check build time
time npm run build

# Target: < 2 minutes
# Optimize with:
# - Code splitting
# - Tree shaking
# - Dynamic imports
```

### **Runtime Performance**
```bash
# Check Core Web Vitals
# - FCP: < 1.5s
# - LCP: < 2.5s
# - CLS: < 0.1
```

## 🚀 **Quick Fixes**

### **Fix 1: Simple Deployment**
```bash
# Deploy basic version first
git checkout -b simple-deployment
# Remove complex features temporarily
git add -A
git commit -m "Simple deployment test"
git push origin simple-deployment
```

### **Fix 2: Rollback Strategy**
```bash
# Quick rollback
git checkout previous-working-commit
git push origin main --force
```

### **Fix 3: Emergency Patch**
```bash
# Hot fix
git checkout -b hotfix
# Make minimal changes
git add -A
git commit -m "Hot fix"
git push origin hotfix
```

## 📋 **Prevention Checklist**

### **Before Every Deployment**
- [ ] Local production build works
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Bundle size optimized
- [ ] Dependencies cleaned
- [ ] Environment variables set
- [ ] Error boundaries implemented
- [ ] Progressive enhancement used

### **Weekly Maintenance**
- [ ] Update dependencies
- [ ] Check for security vulnerabilities
- [ ] Analyze bundle size
- [ ] Review performance metrics
- [ ] Test deployment pipeline

### **Monthly Review**
- [ ] Review deployment patterns
- [ ] Update troubleshooting guide
- [ ] Optimize build process
- [ ] Improve error handling
- [ ] Document new learnings

## 🎯 **Success Metrics**

### **Deployment Success Rate**
- **Target**: > 95%
- **Current**: Track and improve

### **Build Time**
- **Target**: < 2 minutes
- **Current**: Track and optimize

### **Bundle Size**
- **Target**: < 1MB total
- **Current**: Monitor and reduce

### **Error Rate**
- **Target**: < 1%
- **Current**: Track and fix

---

## 🎉 **Key Takeaway**

This checklist transforms deployment issues from blockers into learning opportunities. By following this systematic approach, your software factory becomes more reliable with each deployment.

**Remember: Every deployment issue is a chance to make the system smarter!** 🎯✨

# Railway Pilot Evaluation Runbook

## 🎯 **Objective**
Evaluate Railway as a deployment platform for our software factory stack and determine if it should replace our current GitHub Actions + Docker approach.

## 📋 **Pre-Flight Checklist**

### Prerequisites
- [ ] Railway account created
- [ ] Test project ready (weight-tracker-nextjs)
- [ ] Environment variables documented
- [ ] Baseline metrics captured (current deployment time, cost)

**Note**: This runbook requires manual Railway CLI installation as an opt-in step.

### Manual CLI Installation (Required)
```bash
# Install Railway CLI (manual opt-in step)
npm install -g @railway/cli

# Verify installation
railway --version
```

**Important**: Do not run this command without understanding the implications of global package installation.

### Environment Setup
```bash
# 1. Create pilot directory
mkdir railway-pilot
cd railway-pilot

# 2. Copy test project
cp -r ../software-factory/generated-apps/weight-tracker-nextjs ./weight-tracker-railway
cd weight-tracker-railway

# 3. Create Railway configuration
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "npm run start",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100
  }
}
EOF
```

## 🚀 **Deployment Process**

### Step 1: Initial Deployment

**Prerequisites**: Railway CLI must be installed manually before proceeding.

**Deployment Steps**:
```bash
# Login to Railway
railway login

# Create new project
railway project create weight-tracker-pilot

# Link project
railway link

# Set environment variables
railway variables set NODE_ENV=production
railway variables set PORT=3000

# Deploy
railway up
```

### Step 2: Verify Deployment
- [ ] Application accessible via Railway URL
- [ ] All routes working correctly
- [ ] Environment variables loaded
- [ ] Static assets served properly
- [ ] Database connections working (if applicable)

## 📊 **Evaluation Metrics**

### Performance Metrics
| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| Cold start time | < 10s | ___s | Time from deploy to first response |
| Response time | < 500ms | ___ms | Average response time |
| Memory usage | < 512MB | ___MB | Peak memory consumption |
| CPU usage | < 50% | ___% | Average CPU usage |

### Deployment Experience
| Criteria | Score (1-5) | Notes |
|----------|------------|-------|
| Setup simplicity | ___/5 | How easy was initial setup? |
| Configuration clarity | ___/5 | Were configs intuitive? |
| Error messages | ___/5 | Helpful debugging info? |
| Documentation quality | ___/5 | Clear and complete? |
| Integration ease | ___/5 | Works with our stack? |

### Cost Analysis
| Period | Usage | Cost | Notes |
|--------|-------|------|-------|
| Day 1 | ___ | $___ | Initial deployment |
| Week 1 | ___ | $___ | Light usage |
| Month 1 | ___ | $___ | Projected monthly cost |

### Comparison with Current Setup
| Aspect | Current (GitHub Actions) | Railway | Winner |
|--------|-------------------------|---------|--------|
| Setup time | ___ minutes | ___ minutes | |
| Deployment time | ___ minutes | ___ minutes | |
| Monthly cost | $___ | $___ | |
| Ease of use | ___/5 | ___/5 | |
| Debugging | ___/5 | ___/5 | |
| Scaling | ___/5 | ___/5 | |

## 🧪 **Testing Scenarios**

### Basic Functionality
- [ ] Homepage loads
- [ ] Navigation works
- [ ] Forms submit correctly
- [ ] API endpoints respond
- [ ] Error pages display

### Performance Testing
- [ ] Load test with 10 concurrent users
- [ ] Memory usage under load
- [ ] Response time degradation
- [ ] Recovery after load

### Edge Cases
- [ ] Invalid environment variables
- [ ] Database connection failures
- [ ] Large file uploads
- [ ] High memory usage

## 🔧 **Troubleshooting Guide**

### Common Issues
1. **Build Failures**
   - Check Node.js version compatibility
   - Verify package.json dependencies
   - Review build logs in Railway dashboard

2. **Environment Variables**
   - Ensure all required vars are set
   - Check variable names match code
   - Verify no typos in values

3. **Deployment Timeouts**
   - Increase healthcheck timeout
   - Check application startup time
   - Review resource limits

### Debugging Commands
```bash
# Check deployment status
railway status

# View logs
railway logs

# Connect to service
railway connect

# Check variables
railway variables
```

## 📈 **Success Criteria**

### Must Have
- [ ] Application deploys successfully
- [ ] All core functionality works
- [ ] Performance meets targets
- [ ] Cost is reasonable (<$50/month for pilot)

### Nice to Have
- [ ] Faster deployment than current setup
- [ ] Better debugging experience
- [ ] Easier configuration management
- [ ] Good documentation

### Deal Breakers
- [ ] Cannot deploy successfully
- [ ] Performance significantly worse
- [ ] Cost exceeds budget
- [ ] Poor developer experience

## 🎯 **Decision Framework**

### Adopt Railway If:
- ✅ All must-have criteria met
- ✅ At least 2 nice-to-have criteria met
- ✅ No deal-breakers encountered
- ✅ Cost is within budget
- ✅ Team prefers Railway over current setup

### Reject Railway If:
- ❌ Any deal-breaker encountered
- ❌ Cost exceeds budget significantly
- ❌ Performance significantly worse
- ❌ Team strongly prefers current setup

### Further Testing Needed If:
- ⚠️ Mixed results on must-have criteria
- ⚠️ Close call on cost/performance
- ⚠️ Team divided on preference

## 📝 **Final Report Template**

### Executive Summary
- **Recommendation**: [Adopt/Reject/Further Testing]
- **Key Benefits**: [List top 3 benefits]
- **Key Concerns**: [List top 3 concerns]
- **Next Steps**: [Specific actions]

### Detailed Findings
- **Performance**: [Summary of performance metrics]
- **Cost**: [Cost analysis and projections]
- **Developer Experience**: [Team feedback and observations]
- **Technical Issues**: [Problems encountered and solutions]

### Implementation Plan (if adopting)
- **Phase 1**: [Immediate actions]
- **Phase 2**: [Migration steps]
- **Phase 3**: [Full rollout]
- **Timeline**: [Expected completion date]

## 🔄 **Next Steps**

1. **Complete this runbook** for weight-tracker-nextjs
2. **Document findings** in the evaluation metrics
3. **Share results** with team for input
4. **Make decision** based on criteria
5. **Implement decision** or plan next steps

---

**Last Updated**: [Date]
**Evaluator**: [Name]
**Project**: weight-tracker-railway

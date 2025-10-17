# 🚀 Complete API Keys Setup - All Services

## 🎯 **Quick Setup Guide for All APIs**

Since you already have OpenAI API access, let's get all the other APIs set up quickly. Here are the direct links and steps:

### **1. Unsplash API (FREE) - Priority #1**

#### **Get API Key (2 minutes):**
1. **Go to**: [Unsplash Developers](https://unsplash.com/developers)
2. **Sign up/Login** to Unsplash (free account)
3. **Click**: "Your apps" → "New Application"
4. **Fill out form**:
   - **Application name**: `Design Decision Team`
   - **Description**: `AI-powered design automation for software factory`
   - **Website**: `https://github.com/yourusername` (or your website)
5. **Accept terms** and click "Create application"
6. **Copy "Access Key"** (starts with your access key)

#### **Add to Environment:**
```bash
UNSPLASH_API_KEY=your-access-key-here
```

### **2. Stability AI API (CHEAP) - Priority #2**

#### **Get API Key (3 minutes):**
1. **Go to**: [Stability AI Platform](https://platform.stability.ai/)
2. **Sign up/Login** (free account)
3. **Navigate to**: "API Keys"
4. **Click**: "Create API Key"
5. **Copy the key** (starts with `sk-`)
6. **Add $10 deposit** (minimum, pay-as-you-go)

#### **Add to Environment:**
```bash
STABILITY_API_KEY=sk-your-key-here
```

### **3. Pexels API (FREE) - Priority #3**

#### **Get API Key (2 minutes):**
1. **Go to**: [Pexels API](https://www.pexels.com/api/)
2. **Sign up/Login** (free account)
3. **Click**: "Request API Key"
4. **Fill out form**:
   - **Project name**: `Design Decision Team`
   - **Description**: `AI-powered design automation`
   - **Website**: Your website or GitHub
5. **Submit** and wait for approval (usually instant)
6. **Copy the key** (starts with your API key)

#### **Add to Environment:**
```bash
PEXELS_API_KEY=your-api-key-here
```

### **4. OpenAI API (You Already Have This)**

#### **If you need to find your key:**
1. **Go to**: [OpenAI Platform](https://platform.openai.com/)
2. **Navigate to**: "API Keys"
3. **Copy existing key** or create new one

#### **Add to Environment:**
```bash
OPENAI_API_KEY=sk-your-existing-key-here
```

## 🔧 **Quick Configuration**

### **Option 1: Manual Setup (Fastest)**
```bash
cd /Users/jackagnew/projects/agents/project-starter/templates/ai_agents/design_decision_team/

# Create .env file
cp env_template.txt .env

# Edit .env file with your keys
nano .env
```

### **Option 2: Direct Environment Setup**
```bash
# Set environment variables directly
export OPENAI_API_KEY="sk-your-openai-key"
export UNSPLASH_API_KEY="your-unsplash-key"
export STABILITY_API_KEY="sk-your-stability-key"
export PEXELS_API_KEY="your-pexels-key"
```

## 🧪 **Test All APIs**

Once you have the keys, test them:

```bash
cd /Users/jackagnew/projects/agents/project-starter/templates/ai_agents/design_decision_team/
python3 test_api_keys.py
```

## 💰 **Cost Summary**

| API | Cost | Setup Time | Best For |
|-----|------|------------|----------|
| **Unsplash** | FREE | 2 min | Stock photos |
| **Pexels** | FREE | 2 min | Additional stock photos |
| **OpenAI** | $0.040/image | Already have | Custom cartoon characters |
| **Stability AI** | $0.002/image | 3 min | Cost-effective generation |

**Total Setup Time**: ~7 minutes
**Monthly Cost**: $0-10 (depending on usage)

## 🎯 **Expected Results After Setup**

```bash
🔑 Testing Design Decision Team API Keys
==================================================

🧪 Testing OpenAI DALL-E 3...
✅ OpenAI DALL-E 3: API key format valid

🧪 Testing Unsplash...
✅ Unsplash: API working correctly

🧪 Testing Stability AI...
✅ Stability AI: API key format valid

🧪 Testing Pexels...
✅ Pexels: API working correctly

📊 API Keys Summary:
==============================
✅ Working APIs: 4
❌ Failed APIs: 0

💡 Recommendations:
✅ You have enough APIs configured for the Design Decision Team!
   The team can now generate images and make design decisions.
```

## 🚀 **Next Steps After Setup**

1. **Test Configuration**:
   ```bash
   python3 test_api_keys.py
   ```

2. **Test with Weight Tracker**:
   ```bash
   python3 test_weight_tracker_integration.py
   ```

3. **Generate Real Cartoon Characters**:
   ```bash
   python3 quick_start.py
   ```

## 🔗 **Direct Links for Quick Access**

- **Unsplash API**: https://unsplash.com/developers
- **Stability AI**: https://platform.stability.ai/
- **Pexels API**: https://www.pexels.com/api/
- **OpenAI Platform**: https://platform.openai.com/

---

**Once you have these 4 APIs configured, the Design Decision Team will be able to generate real cartoon characters and professional morphing animations for your weight tracker project!** 🎨🚀

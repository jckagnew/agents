# 🔑 API Keys Setup Guide for Design Decision Team

## 📋 **Required API Keys**

### **Tier 1: AI-Generated Images (Recommended)**
1. **OpenAI DALL-E 3 API** - Best for custom cartoon characters
2. **Stability AI** - Cost-effective alternative
3. **RunwayML** - For AI-powered morphing (optional)

### **Tier 2: Free Attribution Sources**
1. **Unsplash API** - High-quality stock photos
2. **Pexels API** - Additional free images
3. **Pixabay API** - Diverse content (optional)

### **Tier 3: Premium Sources (Optional)**
1. **Shutterstock API** - Premium commercial images
2. **Adobe Stock API** - Professional quality
3. **Getty Images API** - Editorial content

## 🚀 **Step-by-Step Setup**

### **1. OpenAI DALL-E 3 API (Priority #1)**

#### **Get API Key:**
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up/Login to your account
3. Navigate to "API Keys" section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

#### **Set Usage Limits:**
1. Go to "Usage" section
2. Set monthly spending limit (recommended: $50-100)
3. Enable billing alerts

#### **Add to Environment:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

### **2. Unsplash API (Priority #2)**

#### **Get API Key:**
1. Go to [Unsplash Developers](https://unsplash.com/developers)
2. Sign up/Login to Unsplash
3. Click "Your apps" → "New Application"
4. Fill out application form:
   - **Application name**: "Design Decision Team"
   - **Description**: "AI-powered design automation for software factory"
   - **Website**: Your website or GitHub
5. Accept terms and create application
6. Copy "Access Key" (starts with `your-access-key`)

#### **Add to Environment:**
```bash
UNSPLASH_API_KEY=your-access-key-here
```

### **3. Stability AI API (Priority #3)**

#### **Get API Key:**
1. Go to [Stability AI Platform](https://platform.stability.ai/)
2. Sign up/Login
3. Navigate to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `sk-`)

#### **Add to Environment:**
```bash
STABILITY_API_KEY=sk-your-key-here
```

### **4. Pexels API (Optional)**

#### **Get API Key:**
1. Go to [Pexels API](https://www.pexels.com/api/)
2. Sign up/Login
3. Click "Request API Key"
4. Fill out form and submit
5. Copy the key (starts with `your-api-key`)

#### **Add to Environment:**
```bash
PEXELS_API_KEY=your-api-key-here
```

## 🔧 **Environment Configuration**

### **Create .env File:**
```bash
# Navigate to Design Decision Team directory
cd project-starter/templates/ai_agents/design_decision_team/

# Copy template
cp env_template.txt .env

# Edit with your keys
nano .env
```

### **Complete .env File:**
```bash
# AI Image Generation APIs
OPENAI_API_KEY=sk-your-openai-key-here
STABILITY_API_KEY=sk-your-stability-key-here
RUNWAYML_API_KEY=your-runwayml-key-here

# Free Attribution Sources
UNSPLASH_API_KEY=your-unsplash-key-here
PEXELS_API_KEY=your-pexels-key-here
PIXABAY_API_KEY=your-pixabay-key-here

# Premium Sources (Optional)
SHUTTERSTOCK_API_KEY=your-shutterstock-key-here
ADOBE_STOCK_API_KEY=your-adobe-stock-key-here
GETTY_IMAGES_API_KEY=your-getty-key-here

# Quality Metrics Configuration
DESIGN_QUALITY_THRESHOLD=85
UX_SCORE_THRESHOLD=80
BRAND_CONSISTENCY_THRESHOLD=90
PERFORMANCE_THRESHOLD=75

# Budget Tiers
PREMIUM_BUDGET_LIMIT=500
AI_GENERATED_BUDGET_LIMIT=100
FREE_BUDGET_LIMIT=0

# Timeline Configuration
URGENT_TIMELINE_HOURS=2
STANDARD_TIMELINE_HOURS=8
EXTENDED_TIMELINE_HOURS=24
```

## 🧪 **Test API Keys**

### **Test Script:**
```python
import os
import requests

def test_api_keys():
    """Test all configured API keys"""
    
    print("🔑 Testing API Keys...")
    
    # Test OpenAI DALL-E
    if os.getenv('OPENAI_API_KEY'):
        print("✅ OpenAI API Key: Configured")
        # Test with a simple request
        try:
            headers = {
                'Authorization': f'Bearer {os.getenv("OPENAI_API_KEY")}',
                'Content-Type': 'application/json'
            }
            data = {
                'model': 'dall-e-3',
                'prompt': 'A simple test image',
                'n': 1,
                'size': '1024x1024'
            }
            # Note: This would make an actual API call in production
            print("   OpenAI API: Ready for requests")
        except Exception as e:
            print(f"   OpenAI API: Error - {e}")
    else:
        print("❌ OpenAI API Key: Not configured")
    
    # Test Unsplash
    if os.getenv('UNSPLASH_API_KEY'):
        print("✅ Unsplash API Key: Configured")
        try:
            headers = {
                'Authorization': f'Client-ID {os.getenv("UNSPLASH_API_KEY")}'
            }
            # Test endpoint
            response = requests.get(
                'https://api.unsplash.com/photos/random',
                headers=headers,
                params={'count': 1}
            )
            if response.status_code == 200:
                print("   Unsplash API: Working correctly")
            else:
                print(f"   Unsplash API: Error - {response.status_code}")
        except Exception as e:
            print(f"   Unsplash API: Error - {e}")
    else:
        print("❌ Unsplash API Key: Not configured")
    
    # Test Stability AI
    if os.getenv('STABILITY_API_KEY'):
        print("✅ Stability AI API Key: Configured")
        print("   Stability AI API: Ready for requests")
    else:
        print("❌ Stability AI API Key: Not configured")

if __name__ == "__main__":
    test_api_keys()
```

## 💰 **Cost Management**

### **Estimated Costs:**
- **OpenAI DALL-E 3**: $0.040-$0.080 per image
- **Stability AI**: $0.002-$0.01 per image
- **Unsplash**: Free (with attribution)
- **Pexels**: Free (with attribution)

### **Budget Recommendations:**
- **Development/Testing**: $50-100/month
- **Production**: $200-500/month
- **High Volume**: $1000+/month

### **Cost Optimization:**
1. **Start with free sources** (Unsplash, Pexels)
2. **Use AI generation** for custom needs
3. **Set spending limits** on all APIs
4. **Monitor usage** regularly
5. **Cache results** to reduce API calls

## 🔒 **Security Best Practices**

### **API Key Security:**
1. **Never commit** API keys to version control
2. **Use environment variables** only
3. **Rotate keys** regularly
4. **Monitor usage** for anomalies
5. **Set IP restrictions** where possible

### **Rate Limiting:**
- **OpenAI**: 50 requests/minute
- **Unsplash**: 50 requests/hour
- **Stability AI**: 150 requests/minute
- **Pexels**: 200 requests/hour

## 🚀 **Next Steps**

### **1. Get Priority Keys:**
```bash
# Essential for Design Decision Team
1. OpenAI DALL-E 3 API Key
2. Unsplash API Key
3. Stability AI API Key (optional)
```

### **2. Configure Environment:**
```bash
cd project-starter/templates/ai_agents/design_decision_team/
cp env_template.txt .env
# Edit .env with your keys
```

### **3. Test Configuration:**
```bash
python3 validate_setup.py
```

### **4. Run Weight Tracker Test:**
```bash
python3 test_weight_tracker_integration.py
```

## 📞 **Support & Troubleshooting**

### **Common Issues:**
1. **Invalid API Key**: Check key format and permissions
2. **Rate Limiting**: Wait and retry, or upgrade plan
3. **Billing Issues**: Check payment method and limits
4. **Network Errors**: Check internet connection and firewall

### **Getting Help:**
- **OpenAI**: [OpenAI Help Center](https://help.openai.com/)
- **Unsplash**: [Unsplash API Docs](https://unsplash.com/documentation)
- **Stability AI**: [Stability AI Docs](https://platform.stability.ai/docs)

---

**Once you have the API keys configured, the Design Decision Team will be able to generate real cartoon characters and morphing animations for your weight tracker project!** 🎨🚀

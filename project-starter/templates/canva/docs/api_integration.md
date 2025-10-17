# 🔌 Canva API Integration Guide

This guide covers how to integrate Canva's API with your AI-powered applications using the project starter templates.

## 🚀 Quick Start

### 1. Get Canva API Access

1. **Sign up for Canva Pro or Enterprise**
   - Visit [Canva for Work](https://www.canva.com/for-work/)
   - Choose the plan that fits your needs
   - Pro: $15/month per user
   - Enterprise: Custom pricing

2. **Enable API Access**
   - Go to your Canva account settings
   - Navigate to "API & Integrations"
   - Generate your API key
   - Note your Team ID and Brand Kit ID

3. **Configure Environment Variables**
   ```bash
   # Add to your .env file
   CANVA_API_KEY=your_canva_api_key_here
   CANVA_TEAM_ID=your_team_id_here
   CANVA_BRAND_KIT_ID=your_brand_kit_id_here
   CANVA_OUTPUT_DIR=./generated_designs
   ```

### 2. Install Dependencies

```bash
# Install required packages
pip install requests asyncio python-dotenv

# Or add to requirements.txt
echo "requests>=2.31.0" >> requirements.txt
echo "asyncio" >> requirements.txt
echo "python-dotenv>=1.0.0" >> requirements.txt
```

### 3. Basic Usage

```python
from canva_design_agent import CanvaDesignAgent, Platform, DesignFormat

# Initialize agent
agent = CanvaDesignAgent(
    api_key=os.getenv("CANVA_API_KEY"),
    team_id=os.getenv("CANVA_TEAM_ID"),
    brand_kit_id=os.getenv("CANVA_BRAND_KIT_ID")
)

# Generate designs
designs = await agent.generate_social_media_designs(
    platform=Platform.INSTAGRAM,
    content_type="post",
    content="Check out our new product!",
    quantity=3
)

# Download designs
files = await agent.batch_download(designs)
```

## 📚 API Reference

### CanvaDesignAgent

The main class for generating designs using Canva's API.

#### Constructor
```python
CanvaDesignAgent(
    api_key: str = None,
    team_id: str = None,
    brand_kit_id: str = None,
    output_dir: str = "./generated_designs"
)
```

#### Methods

##### `generate_social_media_designs()`
Generate social media designs for specific platforms.

```python
async def generate_social_media_designs(
    platform: Platform,
    content_type: str,
    content: str,
    quantity: int = 1,
    variations: List[str] = None,
    style: str = "modern"
) -> List[GeneratedDesign]
```

**Parameters:**
- `platform`: Target platform (INSTAGRAM, FACEBOOK, LINKEDIN, TWITTER)
- `content_type`: Type of content (post, story, cover, etc.)
- `content`: Text content for the design
- `quantity`: Number of designs to generate
- `variations`: List of variation types
- `style`: Design style preference

**Returns:** List of GeneratedDesign objects

##### `generate_marketing_assets()`
Generate marketing assets for a campaign.

```python
async def generate_marketing_assets(
    campaign_name: str,
    products: List[str],
    platforms: List[Platform],
    output_formats: List[DesignFormat] = None
) -> Dict[str, List[GeneratedDesign]]
```

**Parameters:**
- `campaign_name`: Name of the marketing campaign
- `products`: List of products to feature
- `platforms`: List of target platforms
- `output_formats`: Desired output formats

**Returns:** Dictionary mapping platform names to design lists

##### `generate_data_visualizations()`
Generate data visualization designs.

```python
async def generate_data_visualizations(
    data: Dict,
    chart_types: List[str],
    title: str = "Data Visualization"
) -> List[GeneratedDesign]
```

**Parameters:**
- `data`: Data to visualize
- `chart_types`: Types of charts to create
- `title`: Title for the visualization

**Returns:** List of GeneratedDesign objects

##### `download_design()`
Download a single design to local filesystem.

```python
async def download_design(
    design: GeneratedDesign,
    format: DesignFormat = None
) -> str
```

**Parameters:**
- `design`: GeneratedDesign object to download
- `format`: Desired output format

**Returns:** File path of downloaded design

##### `batch_download()`
Download multiple designs in batch.

```python
async def batch_download(
    designs: List[GeneratedDesign],
    format: DesignFormat = None
) -> List[str]
```

**Parameters:**
- `designs`: List of GeneratedDesign objects
- `format`: Desired output format

**Returns:** List of file paths

### Enums

#### Platform
```python
class Platform(Enum):
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    WEB = "web"
    PRINT = "print"
```

#### DesignFormat
```python
class DesignFormat(Enum):
    PNG = "png"
    PDF = "pdf"
    SVG = "svg"
    JPG = "jpg"
```

### Data Classes

#### GeneratedDesign
```python
@dataclass
class GeneratedDesign:
    design_id: str
    url: str
    format: DesignFormat
    platform: Platform
    dimensions: Dict
    file_size: int
    created_at: datetime
    metadata: Dict
```

#### DesignRequest
```python
@dataclass
class DesignRequest:
    content_type: str
    platform: Platform
    brand_guidelines: Dict
    content: str
    dimensions: Optional[Dict] = None
    style: Optional[str] = None
    quantity: int = 1
    variations: Optional[List[str]] = None
```

## 🔧 Configuration

### Brand Guidelines

Configure your brand guidelines in `config/brand_guidelines.json`:

```json
{
  "brand": {
    "name": "Your Company",
    "colors": {
      "primary": "#1a73e8",
      "secondary": "#34a853"
    },
    "typography": {
      "heading": "Roboto",
      "body": "Open Sans"
    }
  }
}
```

### Platform Specifications

Platform-specific design dimensions are automatically configured:

```python
platform_specs = {
    Platform.INSTAGRAM: {
        "post": {"width": 1080, "height": 1080},
        "story": {"width": 1080, "height": 1920}
    },
    Platform.FACEBOOK: {
        "post": {"width": 1200, "height": 630},
        "cover": {"width": 1200, "height": 315}
    }
}
```

## 🎯 Use Cases

### 1. Social Media Marketing

```python
# Generate Instagram posts
instagram_designs = await agent.generate_social_media_designs(
    platform=Platform.INSTAGRAM,
    content_type="post",
    content="New product launch! 🚀",
    quantity=5,
    variations=["product_showcase", "lifestyle", "testimonial"]
)

# Generate Facebook covers
facebook_covers = await agent.generate_social_media_designs(
    platform=Platform.FACEBOOK,
    content_type="cover",
    content="Welcome to our page!",
    quantity=2
)
```

### 2. Marketing Campaigns

```python
# Generate campaign assets
campaign_assets = await agent.generate_marketing_assets(
    campaign_name="Summer Sale 2024",
    products=["Product A", "Product B", "Product C"],
    platforms=[Platform.INSTAGRAM, Platform.FACEBOOK, Platform.LINKEDIN],
    output_formats=[DesignFormat.PNG, DesignFormat.PDF]
)
```

### 3. Data Visualization

```python
# Generate charts
sales_data = {
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "values": [100, 150, 200, 180]
}

charts = await agent.generate_data_visualizations(
    data=sales_data,
    chart_types=["bar", "line", "pie"],
    title="Quarterly Sales Report"
)
```

## 🚨 Error Handling

### Common Errors

1. **Invalid API Key**
   ```python
   try:
       agent = CanvaDesignAgent(api_key="invalid_key")
   except ValueError as e:
       print(f"API Key Error: {e}")
   ```

2. **Rate Limit Exceeded**
   ```python
   try:
       designs = await agent.generate_social_media_designs(...)
   except Exception as e:
       if "rate limit" in str(e).lower():
           print("Rate limit exceeded. Please wait and try again.")
       else:
           print(f"Error: {e}")
   ```

3. **Invalid Platform/Content Type**
   ```python
   try:
       designs = await agent.generate_social_media_designs(
           platform=Platform.INSTAGRAM,
           content_type="invalid_type"
       )
   except Exception as e:
       print(f"Invalid content type: {e}")
   ```

### Retry Logic

```python
import asyncio
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
                    await asyncio.sleep(delay * (2 ** attempt))
            return None
        return wrapper
    return decorator

# Usage
@retry_on_failure(max_retries=3, delay=2)
async def generate_designs_with_retry(agent, platform, content):
    return await agent.generate_social_media_designs(platform, "post", content)
```

## 📊 Performance Optimization

### Batch Processing

```python
# Process multiple campaigns in parallel
async def process_multiple_campaigns(campaigns):
    tasks = []
    for campaign in campaigns:
        task = agent.generate_marketing_assets(
            campaign_name=campaign["name"],
            products=campaign["products"],
            platforms=campaign["platforms"]
        )
        tasks.append(task)
    
    results = await asyncio.gather(*tasks)
    return results
```

### Caching

```python
import hashlib
import json

class CachedCanvaAgent(CanvaDesignAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}
    
    def _get_cache_key(self, request):
        """Generate cache key for request"""
        request_str = json.dumps(request.__dict__, sort_keys=True)
        return hashlib.md5(request_str.encode()).hexdigest()
    
    async def generate_social_media_designs(self, *args, **kwargs):
        # Check cache first
        cache_key = self._get_cache_key(DesignRequest(*args, **kwargs))
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Generate designs
        designs = await super().generate_social_media_designs(*args, **kwargs)
        
        # Cache results
        self.cache[cache_key] = designs
        return designs
```

## 🔒 Security Best Practices

### API Key Management

```python
# Use environment variables
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CANVA_API_KEY")
if not api_key:
    raise ValueError("CANVA_API_KEY not found in environment variables")
```

### Rate Limiting

```python
import asyncio
from asyncio import Semaphore

class RateLimitedCanvaAgent(CanvaDesignAgent):
    def __init__(self, *args, max_concurrent=5, **kwargs):
        super().__init__(*args, **kwargs)
        self.semaphore = Semaphore(max_concurrent)
    
    async def generate_social_media_designs(self, *args, **kwargs):
        async with self.semaphore:
            return await super().generate_social_media_designs(*args, **kwargs)
```

## 📈 Monitoring and Analytics

### Usage Tracking

```python
class MonitoredCanvaAgent(CanvaDesignAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usage_stats = {
            "designs_generated": 0,
            "api_calls": 0,
            "errors": 0
        }
    
    async def generate_social_media_designs(self, *args, **kwargs):
        self.usage_stats["api_calls"] += 1
        try:
            designs = await super().generate_social_media_designs(*args, **kwargs)
            self.usage_stats["designs_generated"] += len(designs)
            return designs
        except Exception as e:
            self.usage_stats["errors"] += 1
            raise e
    
    def get_usage_stats(self):
        return self.usage_stats.copy()
```

## 🚀 Advanced Features

### Custom Templates

```python
# Create custom design templates
custom_templates = {
    "product_showcase": {
        "layout": "centered",
        "elements": ["product_image", "title", "description", "cta_button"],
        "colors": ["primary", "secondary"],
        "fonts": ["heading", "body"]
    }
}

# Use custom templates
designs = await agent.generate_social_media_designs(
    platform=Platform.INSTAGRAM,
    content_type="post",
    content="New product!",
    style="product_showcase"
)
```

### Webhook Integration

```python
# Set up webhook for design completion notifications
webhook_url = "https://your-app.com/canva-webhook"

# Configure webhook
webhook_config = {
    "url": webhook_url,
    "events": ["design.completed", "design.failed"],
    "secret": "your_webhook_secret"
}
```

---

*This integration guide provides everything you need to leverage Canva's AI workflow capabilities in your applications.*


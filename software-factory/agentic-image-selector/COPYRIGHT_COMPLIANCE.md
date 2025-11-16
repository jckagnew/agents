# Copyright Compliance Guide

## 🛡️ Overview

This guide ensures that the Agentic Image Selector only uses images that are free for commercial use and properly licensed, avoiding copyright infringement and legal issues.

## ✅ Approved Image Sources

### **Primary Sources (Recommended)**
These repositories provide high-quality images with clear commercial use rights:

#### **Unsplash**
- **License**: Unsplash License (free for commercial use)
- **API**: Free tier (50 requests/hour)
- **Quality**: High-resolution, professional photos
- **Usage**: Commercial use allowed, no attribution required
- **Link**: https://unsplash.com/developers

#### **Pixabay**
- **License**: Pixabay License (free for commercial use)
- **API**: Free tier (5,000 requests/hour)
- **Quality**: Photos, illustrations, vectors
- **Usage**: Commercial use allowed, no attribution required
- **Link**: https://pixabay.com/api/docs/

#### **Pexels**
- **License**: Pexels License (free for commercial use)
- **API**: Free tier available
- **Quality**: High-quality stock photos and videos
- **Usage**: Commercial use allowed, no attribution required
- **Link**: https://www.pexels.com/api/

### **Secondary Sources (Backup)**
These sources are used as backup when primary sources don't have enough content:

#### **Freepik**
- **License**: Freepik Free License (with attribution)
- **API**: Limited free tier
- **Quality**: Vectors, illustrations, photos
- **Usage**: Commercial use with attribution required
- **Link**: https://www.freepik.com/

#### **OpenClipart**
- **License**: Public Domain
- **API**: No API (web scraping)
- **Quality**: Vector illustrations
- **Usage**: Public domain, no restrictions
- **Link**: https://openclipart.org/

## 🚫 Avoided Sources

### **Copyrighted Content**
- Stock photo sites requiring payment (Shutterstock, Getty Images, etc.)
- Social media images without explicit permission
- Branded content or logos
- Images with watermarks
- Content from news sites or blogs

### **Risky Sources**
- Google Images (mixed licensing)
- Pinterest (unknown licensing)
- Social media platforms (copyright unclear)
- News websites (editorial use only)

## 🔍 Validation Process

### **Automatic Validation**
The system automatically validates images using:

1. **Domain Checking**: Verifies URLs are from approved sources
2. **License Detection**: Scans descriptions for licensing keywords
3. **Accessibility Testing**: Ensures images are accessible and loadable
4. **Commercial Use Verification**: Confirms commercial use rights

### **Manual Review**
For critical projects, manually review:

1. **Image Attribution**: Ensure proper attribution if required
2. **License Terms**: Verify specific license requirements
3. **Usage Rights**: Confirm commercial use is allowed
4. **Model Releases**: Check if people in images have signed releases

## 📋 License Types

### **Free for Commercial Use**
- ✅ Unsplash License
- ✅ Pixabay License
- ✅ Pexels License
- ✅ Public Domain (CC0)

### **Attribution Required**
- ⚠️ Creative Commons BY (CC BY)
- ⚠️ Creative Commons BY-SA (CC BY-SA)
- ⚠️ Freepik Free License

### **Restricted Use**
- ❌ Editorial Use Only
- ❌ Personal Use Only
- ❌ Non-Commercial Use Only
- ❌ All Rights Reserved

## 🛠️ Implementation

### **Image Sourcing Priority**
1. **Primary**: Search open source repositories first
2. **Secondary**: Use MCP servers with open source filters
3. **Validation**: Verify licensing and accessibility
4. **Fallback**: Skip images that don't meet requirements

### **Code Implementation**
```python
# Check if image is from approved source
def is_open_source_image(url: str) -> bool:
    open_source_domains = [
        "unsplash.com",
        "pixabay.com", 
        "pexels.com",
        "freepik.com",
        "openclipart.org"
    ]
    return any(domain in url.lower() for domain in open_source_domains)

# Check for licensing keywords
def has_open_source_license(description: str) -> bool:
    license_keywords = [
        "creative commons",
        "public domain",
        "free to use",
        "commercial use",
        "no attribution required"
    ]
    return any(keyword in description.lower() for keyword in license_keywords)
```

## 📊 Compliance Reporting

### **Generated Reports**
The system generates compliance reports including:

- **Source Attribution**: Which repositories were used
- **License Information**: License type for each image
- **Validation Results**: Success/failure of validation checks
- **Commercial Use Confirmation**: Verification of commercial rights

### **Example Report**
```json
{
  "total_images": 50,
  "open_source_images": 45,
  "licensed_images": 5,
  "rejected_images": 0,
  "sources": {
    "unsplash": 25,
    "pixabay": 15,
    "pexels": 5
  },
  "compliance_status": "FULLY_COMPLIANT"
}
```

## ⚖️ Legal Disclaimer

### **Important Notes**
- This system prioritizes open source and free-to-use images
- Always verify licensing before commercial use
- Consider consulting legal counsel for high-stakes projects
- Keep records of image sources and licenses
- Be prepared to provide attribution if required

### **Risk Mitigation**
- Use only approved repositories
- Implement automatic validation
- Keep detailed logs of image sources
- Have a process for handling takedown requests
- Consider purchasing commercial licenses for critical projects

## 🔄 Updates and Maintenance

### **Regular Updates**
- Monitor for new open source repositories
- Update validation rules as needed
- Review and update approved sources list
- Test API endpoints regularly

### **Monitoring**
- Track image usage and licensing
- Monitor for copyright complaints
- Update compliance procedures
- Review legal requirements

---

**🛡️ Remember: When in doubt, err on the side of caution. It's better to use fewer images than to risk copyright infringement.**

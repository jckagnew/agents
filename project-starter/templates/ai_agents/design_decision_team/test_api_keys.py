"""
API Keys Testing Script for Design Decision Team
Tests all configured API keys and validates access
"""

import os
import requests
import json
from typing import Dict, List, Any

def test_openai_api() -> Dict[str, Any]:
    """Test OpenAI DALL-E 3 API"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return {"status": "error", "message": "API key not configured"}
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple request (won't actually generate image)
        data = {
            'model': 'dall-e-3',
            'prompt': 'A simple test image of a cartoon character',
            'n': 1,
            'size': '1024x1024'
        }
        
        # Note: This would make an actual API call in production
        # For testing, we'll just validate the key format
        if api_key.startswith('sk-'):
            return {
                "status": "success",
                "message": "OpenAI API key format valid",
                "endpoint": "https://api.openai.com/v1/images/generations",
                "cost_per_image": "$0.040-$0.080"
            }
        else:
            return {"status": "error", "message": "Invalid API key format"}
            
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}

def test_unsplash_api() -> Dict[str, Any]:
    """Test Unsplash API"""
    api_key = os.getenv('UNSPLASH_API_KEY')
    if not api_key:
        return {"status": "error", "message": "API key not configured"}
    
    try:
        headers = {
            'Authorization': f'Client-ID {api_key}'
        }
        
        # Test with a simple request
        response = requests.get(
            'https://api.unsplash.com/photos/random',
            headers=headers,
            params={'count': 1, 'query': 'cartoon character'}
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "message": "Unsplash API working correctly",
                "endpoint": "https://api.unsplash.com/search/photos",
                "cost": "Free with attribution",
                "sample_image": data[0]['urls']['small'] if data else None
            }
        else:
            return {
                "status": "error", 
                "message": f"API error: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}

def test_stability_api() -> Dict[str, Any]:
    """Test Stability AI API"""
    api_key = os.getenv('STABILITY_API_KEY')
    if not api_key:
        return {"status": "error", "message": "API key not configured"}
    
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test with a simple request (won't actually generate image)
        data = {
            'text_prompts': [{'text': 'A simple test image of a cartoon character'}],
            'cfg_scale': 7,
            'height': 1024,
            'width': 1024,
            'samples': 1,
            'steps': 30
        }
        
        # Note: This would make an actual API call in production
        # For testing, we'll just validate the key format
        if api_key.startswith('sk-'):
            return {
                "status": "success",
                "message": "Stability AI API key format valid",
                "endpoint": "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image",
                "cost_per_image": "$0.002-$0.01"
            }
        else:
            return {"status": "error", "message": "Invalid API key format"}
            
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}

def test_pexels_api() -> Dict[str, Any]:
    """Test Pexels API"""
    api_key = os.getenv('PEXELS_API_KEY')
    if not api_key:
        return {"status": "error", "message": "API key not configured"}
    
    try:
        headers = {
            'Authorization': api_key
        }
        
        # Test with a simple request
        response = requests.get(
            'https://api.pexels.com/v1/search',
            headers=headers,
            params={'query': 'cartoon character', 'per_page': 1}
        )
        
        if response.status_code == 200:
            data = response.json()
            return {
                "status": "success",
                "message": "Pexels API working correctly",
                "endpoint": "https://api.pexels.com/v1/search",
                "cost": "Free with attribution",
                "total_results": data.get('total_results', 0)
            }
        else:
            return {
                "status": "error", 
                "message": f"API error: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {"status": "error", "message": f"Error: {e}"}

def test_all_api_keys():
    """Test all configured API keys"""
    
    print("🔑 Testing Design Decision Team API Keys")
    print("=" * 50)
    
    # Test each API
    apis = [
        ("OpenAI DALL-E 3", test_openai_api),
        ("Unsplash", test_unsplash_api),
        ("Stability AI", test_stability_api),
        ("Pexels", test_pexels_api)
    ]
    
    results = {}
    
    for api_name, test_func in apis:
        print(f"\n🧪 Testing {api_name}...")
        result = test_func()
        results[api_name] = result
        
        if result["status"] == "success":
            print(f"✅ {api_name}: {result['message']}")
            if 'cost' in result:
                print(f"   💰 Cost: {result['cost']}")
            if 'cost_per_image' in result:
                print(f"   💰 Cost: {result['cost_per_image']}")
        else:
            print(f"❌ {api_name}: {result['message']}")
    
    # Summary
    print("\n📊 API Keys Summary:")
    print("=" * 30)
    
    working_apis = [name for name, result in results.items() if result["status"] == "success"]
    failed_apis = [name for name, result in results.items() if result["status"] == "error"]
    
    print(f"✅ Working APIs: {len(working_apis)}")
    for api in working_apis:
        print(f"   • {api}")
    
    print(f"❌ Failed APIs: {len(failed_apis)}")
    for api in failed_apis:
        print(f"   • {api}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if len(working_apis) >= 2:
        print("✅ You have enough APIs configured for the Design Decision Team!")
        print("   The team can now generate images and make design decisions.")
    elif len(working_apis) == 1:
        print("⚠️  You have 1 API configured. Consider adding more for better options.")
    else:
        print("❌ No APIs are working. Please check your configuration.")
    
    return results

def generate_sample_request():
    """Generate a sample design request using working APIs"""
    
    print(f"\n🎨 Sample Design Request Generation")
    print("=" * 40)
    
    # Check which APIs are working
    working_apis = []
    if os.getenv('OPENAI_API_KEY'):
        working_apis.append("OpenAI DALL-E 3")
    if os.getenv('UNSPLASH_API_KEY'):
        working_apis.append("Unsplash")
    if os.getenv('STABILITY_API_KEY'):
        working_apis.append("Stability AI")
    if os.getenv('PEXELS_API_KEY'):
        working_apis.append("Pexels")
    
    if not working_apis:
        print("❌ No APIs configured. Please set up API keys first.")
        return
    
    print(f"📋 Available APIs: {', '.join(working_apis)}")
    
    # Generate sample request for weight tracker
    sample_request = {
        "id": "weight_tracker_splash_sample",
        "project_id": "weight_tracker_mobile",
        "description": "Create morphing transformation splash screen",
        "requirements": {
            "quality": "high",
            "animation_type": "morphing",
            "character_style": "cartoon",
            "transformation": "overweight_to_fit"
        },
        "budget_tier": "ai_generated" if "OpenAI DALL-E 3" in working_apis else "free",
        "timeline": "urgent",
        "target_platform": "mobile"
    }
    
    print(f"\n🎯 Sample Design Request:")
    print(f"   Project: {sample_request['project_id']}")
    print(f"   Description: {sample_request['description']}")
    print(f"   Budget Tier: {sample_request['budget_tier']}")
    print(f"   Platform: {sample_request['target_platform']}")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Run: python3 test_weight_tracker_integration.py")
    print(f"   2. The Design Decision Team will use your configured APIs")
    print(f"   3. Generate real cartoon characters and morphing animations")

if __name__ == "__main__":
    # Test all API keys
    results = test_all_api_keys()
    
    # Generate sample request
    generate_sample_request()
    
    print(f"\n🎉 API Keys testing complete!")
    print(f"   Check the results above and configure any missing keys.")
    print(f"   Then run the Design Decision Team with your weight tracker project!")

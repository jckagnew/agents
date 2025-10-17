#!/usr/bin/env python3
"""Simple test script for the Job Search Assistant API."""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    print("�� Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_job_opportunities():
    """Test job opportunities endpoints."""
    print("\n🔍 Testing job opportunities...")
    
    # Test GET (list)
    try:
        response = requests.get(f"{BASE_URL}/api/job-opportunities/", timeout=5)
        print(f"✅ List job opportunities: {response.status_code}")
        opportunities = response.json()
        print(f"   Found {len(opportunities)} opportunities")
    except Exception as e:
        print(f"❌ List job opportunities failed: {e}")
        return False
    
    # Test POST (create)
    try:
        new_job = {
            "title": "Senior AI Sales Engineer",
            "company": "TechCorp Inc",
            "location": "San Francisco, CA",
            "remote_ok": True,
            "salary_min": 120000.0,
            "salary_max": 180000.0,
            "fit_score": 9.2,
            "description": "Looking for an experienced AI sales engineer to drive enterprise AI solutions.",
            "requirements": ["5+ years enterprise sales", "AI/ML experience", "Strong technical background"],
            "benefits": ["Health insurance", "Dental coverage", "401k matching", "Stock options", "Flexible work"]
        }
        
        response = requests.post(
            f"{BASE_URL}/api/job-opportunities/",
            json=new_job,
            timeout=5
        )
        print(f"✅ Create job opportunity: {response.status_code}")
        if response.status_code == 200:
            created_job = response.json()
            print(f"   Created job ID: {created_job.get('id')}")
            return created_job.get('id')
    except Exception as e:
        print(f"❌ Create job opportunity failed: {e}")
        return None

def main():
    """Run all tests."""
    print("🎯 JOB SEARCH ASSISTANT - API TEST")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("\n❌ Server is not running. Please start it with:")
        print("   uv run uvicorn src.job_search_assistant.api.main:app --reload --host 127.0.0.1 --port 8000")
        return
    
    # Test job opportunities
    test_job_opportunities()
    
    print("\n🎉 TEST COMPLETE!")
    print("\n🌐 Next steps:")
    print("   1. Open http://localhost:8000/docs in your browser")
    print("   2. Explore the interactive API documentation")
    print("   3. Try creating more job opportunities")
    print("   4. Test the search and filtering features")

if __name__ == "__main__":
    main()

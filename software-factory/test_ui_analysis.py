#!/usr/bin/env python3
"""
Test Script for UI Analysis Agent
This script demonstrates the UI Analysis Agent functionality.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import our UI analysis agent
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents.ui_analysis import UIAnalysisAgent, UIIssue, IssueCategory, SeverityLevel


async def test_ui_analysis_agent():
    """Test the UI Analysis Agent with sample HTML content"""
    print("🎨 Testing UI Analysis Agent...")
    print("=" * 50)
    
    agent = UIAnalysisAgent()
    
    # Create a sample HTML file with common UI issues
    sample_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Sample App with UI Issues</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                color: #666666;
                background-color: #f0f0f0;
            }
            .container {
                width: 1200px;
                margin: 0 auto;
            }
            .button {
                font-size: 10px;
                color: #999999;
                background-color: #eeeeee;
                padding: 5px;
            }
            .nav {
                display: flex;
                justify-content: space-between;
            }
            .nav ul {
                list-style: none;
                padding: 0;
            }
            .nav ul li {
                display: inline-block;
                margin-right: 20px;
            }
            .nav ul li ul {
                position: absolute;
                display: none;
            }
            .nav ul li:hover ul {
                display: block;
            }
            .nav ul li ul li {
                display: block;
                margin: 10px 0;
            }
            .nav ul li ul li ul {
                position: absolute;
                left: 100%;
                top: 0;
            }
            .nav ul li ul li:hover ul {
                display: block;
            }
            .content {
                margin: 20px 0;
            }
            .content h1 {
                font-size: 24px;
                color: #333333;
            }
            .content p {
                font-size: 12px;
                line-height: 1.2;
                max-width: none;
            }
            .form-group {
                margin: 10px 0;
            }
            .form-group input {
                width: 300px;
                padding: 8px;
                border: 1px solid #cccccc;
            }
            .form-group label {
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }
            .image-container {
                text-align: center;
                margin: 20px 0;
            }
            .image-container img {
                max-width: 100%;
                height: auto;
            }
            .cta-button {
                background-color: #007bff;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                font-size: 16px;
                cursor: pointer;
            }
            .cta-button:hover {
                background-color: #0056b3;
            }
            .cta-button:focus {
                outline: none;
            }
            .success-message {
                color: green;
                font-weight: bold;
            }
            .error-message {
                color: red;
                font-weight: bold;
            }
            .warning-message {
                color: orange;
                font-weight: bold;
            }
            .info-message {
                color: blue;
                font-weight: bold;
            }
            @media (max-width: 768px) {
                .container {
                    width: 100%;
                    padding: 0 20px;
                }
                .nav {
                    flex-direction: column;
                }
                .nav ul li {
                    display: block;
                    margin: 10px 0;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <nav class="nav">
                <div class="logo">
                    <h1>My App</h1>
                </div>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about">About</a>
                        <ul>
                            <li><a href="/about/team">Team</a>
                                <ul>
                                    <li><a href="/about/team/leadership">Leadership</a></li>
                                    <li><a href="/about/team/developers">Developers</a></li>
                                    <li><a href="/about/team/designers">Designers</a></li>
                                </ul>
                            </li>
                            <li><a href="/about/history">History</a></li>
                            <li><a href="/about/mission">Mission</a></li>
                        </ul>
                    </li>
                    <li><a href="/products">Products</a>
                        <ul>
                            <li><a href="/products/web">Web Apps</a></li>
                            <li><a href="/products/mobile">Mobile Apps</a></li>
                            <li><a href="/products/desktop">Desktop Apps</a></li>
                        </ul>
                    </li>
                    <li><a href="/contact">Contact</a></li>
                </ul>
            </nav>
            
            <main class="content">
                <h1>Welcome to Our Amazing Application</h1>
                <p>This is a very long paragraph that contains a lot of text and goes on for many lines without any breaks or proper formatting which makes it very difficult to read and understand the content that we are trying to convey to our users who are visiting this website for the first time and need to quickly understand what we offer.</p>
                
                <div class="image-container">
                    <img src="hero-image.jpg" alt="">
                </div>
                
                <h2>Get Started Today</h2>
                <p>Sign up for our service and start building amazing things right away with our comprehensive suite of tools and features designed specifically for modern developers and designers who want to create beautiful, functional applications quickly and efficiently.</p>
                
                <form>
                    <div class="form-group">
                        <input type="text" id="username" placeholder="Enter your username">
                    </div>
                    <div class="form-group">
                        <input type="email" id="email" placeholder="Enter your email">
                    </div>
                    <div class="form-group">
                        <input type="password" id="password" placeholder="Enter your password">
                    </div>
                    <button type="submit" class="cta-button">Sign Up Now</button>
                </form>
                
                <div class="messages">
                    <div class="success-message">Account created successfully!</div>
                    <div class="error-message">Please fix the following errors:</div>
                    <div class="warning-message">Your session will expire soon</div>
                    <div class="info-message">New features are available</div>
                </div>
            </main>
        </div>
    </body>
    </html>
    """
    
    # Write sample HTML to a temporary file
    sample_file = "sample_ui_test.html"
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(sample_html)
    
    try:
        # Analyze the sample file
        print("📄 Analyzing sample HTML file...")
        result = await agent.analyze_single_file(sample_file)
        
        # Display results
        print(f"\n🎯 Analysis Results:")
        print(f"Overall Score: {result.overall_score:.1f}/10")
        print(f"Accessibility Score: {result.accessibility_score:.1f}/10")
        print(f"Mobile Score: {result.mobile_score:.1f}/10")
        print(f"Performance Score: {result.performance_score:.1f}/10")
        print(f"Total Issues Found: {result.total_issues}")
        
        print(f"\n📊 Issues by Severity:")
        for severity, count in result.issues_by_severity.items():
            if count > 0:
                print(f"  {severity.title()}: {count}")
        
        print(f"\n📋 Issues by Category:")
        for category, count in result.issues_by_category.items():
            if count > 0:
                print(f"  {category.replace('_', ' ').title()}: {count}")
        
        print(f"\n🚨 Critical Issues:")
        critical_issues = [i for i in result.issues if i.severity == SeverityLevel.CRITICAL]
        for issue in critical_issues[:5]:  # Show first 5 critical issues
            print(f"  • {issue.title}")
            print(f"    {issue.description}")
            print(f"    💡 {issue.recommendation}")
            print()
        
        print(f"\n⚠️ High Priority Issues:")
        high_issues = [i for i in result.issues if i.severity == SeverityLevel.HIGH]
        for issue in high_issues[:5]:  # Show first 5 high priority issues
            print(f"  • {issue.title}")
            print(f"    {issue.description}")
            print(f"    💡 {issue.recommendation}")
            print()
        
        print(f"\n💡 Recommendations:")
        for i, recommendation in enumerate(result.recommendations, 1):
            print(f"  {i}. {recommendation}")
        
        print(f"\n📝 Summary:")
        print(result.summary)
        
        # Generate detailed report
        print(f"\n📊 Detailed Issue Report:")
        print("=" * 50)
        
        for i, issue in enumerate(result.issues, 1):
            print(f"\n{i}. {issue.title}")
            print(f"   Category: {issue.category.value}")
            print(f"   Severity: {issue.severity.value}")
            print(f"   Description: {issue.description}")
            print(f"   Recommendation: {issue.recommendation}")
            if issue.wcag_level:
                print(f"   WCAG Level: {issue.wcag_level}")
            print(f"   Impact: {issue.impact}")
            print(f"   Effort to Fix: {issue.effort_to_fix}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return None
    
    finally:
        # Clean up temporary file
        if os.path.exists(sample_file):
            os.remove(sample_file)


async def test_with_real_project():
    """Test with a real project from the software factory"""
    print("\n🏭 Testing with Software Factory Projects...")
    print("=" * 50)
    
    agent = UIAnalysisAgent()
    
    # Test with the C-Level Sales Guy project
    clevel_path = "../clevel-sales-guy"
    if os.path.exists(clevel_path):
        print(f"📁 Analyzing C-Level Sales Guy project...")
        try:
            result = await agent.analyze_project_ui(clevel_path)
            
            print(f"\n🎯 C-Level Sales Guy Analysis:")
            print(f"Overall Score: {result.overall_score:.1f}/10")
            print(f"Total Issues: {result.total_issues}")
            print(f"Critical Issues: {result.issues_by_severity.get('critical', 0)}")
            print(f"High Priority Issues: {result.issues_by_severity.get('high', 0)}")
            
            # Show top 3 recommendations
            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(result.recommendations[:3], 1):
                print(f"  {i}. {rec}")
            
        except Exception as e:
            print(f"❌ Error analyzing C-Level Sales Guy: {e}")
    else:
        print(f"⚠️ C-Level Sales Guy project not found at {clevel_path}")
    
    # Test with the Weight Tracker project
    weight_tracker_path = "../weight-tracker"
    if os.path.exists(weight_tracker_path):
        print(f"\n📁 Analyzing Weight Tracker project...")
        try:
            result = await agent.analyze_project_ui(weight_tracker_path)
            
            print(f"\n🎯 Weight Tracker Analysis:")
            print(f"Overall Score: {result.overall_score:.1f}/10")
            print(f"Total Issues: {result.total_issues}")
            print(f"Critical Issues: {result.issues_by_severity.get('critical', 0)}")
            print(f"High Priority Issues: {result.issues_by_severity.get('high', 0)}")
            
            # Show top 3 recommendations
            print(f"\n💡 Top Recommendations:")
            for i, rec in enumerate(result.recommendations[:3], 1):
                print(f"  {i}. {rec}")
            
        except Exception as e:
            print(f"❌ Error analyzing Weight Tracker: {e}")
    else:
        print(f"⚠️ Weight Tracker project not found at {weight_tracker_path}")


async def main():
    """Main test function"""
    print("🎨 UI Analysis Agent Test Suite")
    print("=" * 40)
    
    try:
        # Test with sample HTML
        await test_ui_analysis_agent()
        
        # Test with real projects
        await test_with_real_project()
        
        print("\n🎉 UI Analysis Agent testing completed!")
        print("\nNext steps:")
        print("1. Integrate the UI Analysis Agent into your software factory")
        print("2. Add UI analysis to your project templates")
        print("3. Set up automated UI testing in your CI/CD pipeline")
        print("4. Create UI improvement recommendations for your existing projects")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())

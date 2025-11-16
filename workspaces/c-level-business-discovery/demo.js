#!/usr/bin/env node

/**
 * C-Level Business Discovery Demo
 * Simple demonstration of Google AI Studio integration
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const API_KEY = 'AIzaSyCzvHSDaZJAkV-iXBm20rlCgncjJTFQwm8';
const MODEL = 'gemini-2.5-pro';
const BASE_URL = 'https://generativelanguage.googleapis.com/v1beta';

// AI Studio API client
async function callAIStudio(prompt, maxTokens = 2048) {
  const url = `${BASE_URL}/models/${MODEL}:generateContent?key=${API_KEY}`;
  
  const requestBody = {
    contents: [{
      parts: [{
        text: prompt
      }]
    }],
    generationConfig: {
      temperature: 0.7,
      maxOutputTokens: maxTokens,
      topP: 0.8,
      topK: 40
    }
  };

  return new Promise((resolve, reject) => {
    const req = https.request(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    }, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        try {
          const response = JSON.parse(data);
          if (response.candidates && response.candidates[0]) {
            resolve(response.candidates[0].content.parts[0].text);
          } else {
            reject(new Error('No content generated: ' + JSON.stringify(response)));
          }
        } catch (error) {
          reject(error);
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify(requestBody));
    req.end();
  });
}

// Demo functions
async function demoMarketAnalysis() {
  console.log('🔍 Market Analysis Demo');
  console.log('======================');
  
  const prompt = `Analyze the AI Sales Automation market for C-Level executives in the technology industry. 
  Focus on:
  1. Market size and growth potential
  2. Key trends and opportunities
  3. Competitive landscape
  4. Strategic recommendations for C-Level executives
  
  Keep the response concise but comprehensive.`;
  
  try {
    const analysis = await callAIStudio(prompt);
    console.log(analysis);
    
    // Save to file
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `market-analysis-${timestamp}.md`;
    fs.writeFileSync(filename, `# Market Analysis: AI Sales Automation\n\n${analysis}`);
    console.log(`\n📊 Analysis saved to: ${filename}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

async function demoOpportunityEvaluation() {
  console.log('\n💡 Opportunity Evaluation Demo');
  console.log('==============================');
  
  const prompt = `Evaluate this business opportunity: "AI-Powered CRM for C-Level Executives"
  
  Provide a structured analysis including:
  1. Market potential and size
  2. Competitive advantage
  3. Resource requirements
  4. Implementation risks
  5. Financial projections (3-year)
  6. Go/No-Go recommendation
  
  Keep response under 1000 words.`;
  
  try {
    const evaluation = await callAIStudio(prompt);
    console.log(evaluation);
    
    // Save to file
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `opportunity-evaluation-${timestamp}.md`;
    fs.writeFileSync(filename, `# Opportunity Evaluation: AI-Powered CRM\n\n${evaluation}`);
    console.log(`\n📊 Evaluation saved to: ${filename}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

async function demoStrategicPlanning() {
  console.log('\n📋 Strategic Planning Demo');
  console.log('==========================');
  
  const prompt = `Create a strategic plan for C-Level Sales Guy LLC, an AI-powered software development and sales consulting company in Dallas, TX.
  
  Include:
  1. Current market positioning
  2. Growth opportunities
  3. Competitive strategy
  4. Technology roadmap
  5. Financial projections
  6. Risk mitigation strategies
  
  Focus on practical, actionable recommendations.`;
  
  try {
    const plan = await callAIStudio(prompt);
    console.log(plan);
    
    // Save to file
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const filename = `strategic-plan-${timestamp}.md`;
    fs.writeFileSync(filename, `# Strategic Plan: C-Level Sales Guy LLC\n\n${plan}`);
    console.log(`\n📊 Strategic plan saved to: ${filename}`);
    
  } catch (error) {
    console.error('❌ Error:', error.message);
  }
}

// Main demo function
async function runDemo() {
  console.log('🚀 C-Level Business Discovery Demo');
  console.log('===================================');
  console.log('Using Google AI Studio with Gemini 2.5 Pro');
  console.log('Account: jckagnew@gmail.com');
  console.log('');
  
  try {
    await demoMarketAnalysis();
    await demoOpportunityEvaluation();
    await demoStrategicPlanning();
    
    console.log('\n✅ Demo completed successfully!');
    console.log('📁 Check the generated .md files for detailed analysis.');
    
  } catch (error) {
    console.error('❌ Demo failed:', error.message);
  }
}

// Run demo if called directly
if (require.main === module) {
  runDemo();
}

module.exports = { callAIStudio, demoMarketAnalysis, demoOpportunityEvaluation, demoStrategicPlanning };

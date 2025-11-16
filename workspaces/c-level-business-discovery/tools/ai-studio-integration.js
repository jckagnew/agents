#!/usr/bin/env node

/**
 * Google AI Studio Integration for C-Level Business Discovery
 * Provides AI-powered business analysis and strategic planning capabilities
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// Configuration
const CONFIG = {
  configFile: path.join(__dirname, '..', 'config', 'ai-studio-config.json'),
  sessionsDir: path.join(__dirname, '..', 'sessions'),
  reportsDir: path.join(__dirname, '..', 'reports')
};

// Load configuration
let config;
try {
  config = JSON.parse(fs.readFileSync(CONFIG.configFile, 'utf8'));
} catch (error) {
  console.error('❌ Error loading AI Studio configuration:', error.message);
  process.exit(1);
}

// AI Studio API client
class AIStudioClient {
  constructor(apiKey, baseUrl) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  async generateContent(model, prompt, options = {}) {
    const url = `${this.baseUrl}/models/${model}:generateContent?key=${this.apiKey}`;
    
    const requestBody = {
      contents: [{
        parts: [{
          text: prompt
        }]
      }],
      generationConfig: {
        temperature: options.temperature || config.settings.temperature,
        maxOutputTokens: options.maxOutputTokens || config.settings.maxOutputTokens,
        topP: options.topP || config.settings.topP,
        topK: options.topK || config.settings.topK
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
              reject(new Error('No content generated'));
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

  async analyzeMarket(market, industry, companyType) {
    const prompt = config.promptTemplates.marketAnalysis
      .replace('{market}', market)
      .replace('{industry}', industry)
      .replace('{companyType}', companyType);
    
    return await this.generateContent(config.models.primary, prompt);
  }

  async evaluateOpportunity(opportunity, timeframe = '12 months', market = 'current') {
    const prompt = config.promptTemplates.opportunityEvaluation
      .replace('{opportunity}', opportunity)
      .replace('{timeframe}', timeframe)
      .replace('{market}', market);
    
    return await this.generateContent(config.models.primary, prompt);
  }

  async createStrategicPlan(company, industry) {
    const prompt = config.promptTemplates.strategicPlanning
      .replace('{company}', company)
      .replace('{industry}', industry);
    
    return await this.generateContent(config.models.primary, prompt);
  }

  async buildFinancialModel(opportunity, timeframe = '24 months', market = 'current') {
    const prompt = config.promptTemplates.financialModeling
      .replace('{opportunity}', opportunity)
      .replace('{timeframe}', timeframe)
      .replace('{market}', market);
    
    return await this.generateContent(config.models.primary, prompt);
  }
}

// Business Discovery Tools
class BusinessDiscovery {
  constructor() {
    this.aiClient = new AIStudioClient(config.apiKey, config.endpoints.baseUrl);
    this.currentSession = null;
  }

  async startSession(sessionName) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    this.currentSession = path.join(CONFIG.sessionsDir, `${timestamp}-${sessionName.replace(/\s+/g, '-')}`);
    
    // Create session directory
    fs.mkdirSync(this.currentSession, { recursive: true });
    fs.mkdirSync(path.join(this.currentSession, 'analysis-reports'), { recursive: true });
    
    // Create session notes file
    const sessionNotes = `# Discovery Session: ${sessionName}
**Date**: ${new Date().toLocaleDateString()}
**Time**: ${new Date().toLocaleTimeString()}

## Session Overview
${sessionName}

## Key Insights
- 

## Opportunities Identified
- 

## Next Steps
- 

## Action Items
- [ ] 
- [ ] 
- [ ] 
`;

    fs.writeFileSync(path.join(this.currentSession, 'discovery-notes.md'), sessionNotes);
    
    console.log(`✅ Started discovery session: ${sessionName}`);
    console.log(`📁 Session directory: ${this.currentSession}`);
    
    return this.currentSession;
  }

  async analyzeMarket(market, industry, companyType) {
    console.log(`🔍 Analyzing ${market} market for ${industry}...`);
    
    try {
      const analysis = await this.aiClient.analyzeMarket(market, industry, companyType);
      
      if (this.currentSession) {
        const reportFile = path.join(this.currentSession, 'analysis-reports', `market-analysis-${Date.now()}.md`);
        fs.writeFileSync(reportFile, `# Market Analysis: ${market}\n\n${analysis}`);
        console.log(`📊 Analysis saved to: ${reportFile}`);
      }
      
      return analysis;
    } catch (error) {
      console.error('❌ Market analysis failed:', error.message);
      throw error;
    }
  }

  async evaluateOpportunity(opportunity, timeframe = '12 months') {
    console.log(`💡 Evaluating opportunity: ${opportunity}`);
    
    try {
      const evaluation = await this.aiClient.evaluateOpportunity(opportunity, timeframe);
      
      if (this.currentSession) {
        const reportFile = path.join(this.currentSession, 'analysis-reports', `opportunity-evaluation-${Date.now()}.md`);
        fs.writeFileSync(reportFile, `# Opportunity Evaluation: ${opportunity}\n\n${evaluation}`);
        console.log(`📊 Evaluation saved to: ${reportFile}`);
      }
      
      return evaluation;
    } catch (error) {
      console.error('❌ Opportunity evaluation failed:', error.message);
      throw error;
    }
  }

  async createStrategicPlan(company = config.businessContext.company, industry = config.businessContext.industry) {
    console.log(`📋 Creating strategic plan for ${company}...`);
    
    try {
      const plan = await this.aiClient.createStrategicPlan(company, industry);
      
      if (this.currentSession) {
        const reportFile = path.join(this.currentSession, 'analysis-reports', `strategic-plan-${Date.now()}.md`);
        fs.writeFileSync(reportFile, `# Strategic Plan: ${company}\n\n${plan}`);
        console.log(`📊 Strategic plan saved to: ${reportFile}`);
      }
      
      return plan;
    } catch (error) {
      console.error('❌ Strategic planning failed:', error.message);
      throw error;
    }
  }

  async buildFinancialModel(opportunity, timeframe = '24 months') {
    console.log(`💰 Building financial model for: ${opportunity}`);
    
    try {
      const model = await this.aiClient.buildFinancialModel(opportunity, timeframe);
      
      if (this.currentSession) {
        const reportFile = path.join(this.currentSession, 'analysis-reports', `financial-model-${Date.now()}.md`);
        fs.writeFileSync(reportFile, `# Financial Model: ${opportunity}\n\n${model}`);
        console.log(`📊 Financial model saved to: ${reportFile}`);
      }
      
      return model;
    } catch (error) {
      console.error('❌ Financial modeling failed:', error.message);
      throw error;
    }
  }

  async generateReport(type = 'monthly') {
    console.log(`📈 Generating ${type} report...`);
    
    const reportDir = path.join(CONFIG.reportsDir, `${type}-summary`);
    fs.mkdirSync(reportDir, { recursive: true });
    
    const timestamp = new Date().toISOString().split('T')[0];
    const reportFile = path.join(reportDir, `${type}-report-${timestamp}.md`);
    
    // Generate report content based on session data
    let reportContent = `# ${type.charAt(0).toUpperCase() + type.slice(1)} Business Intelligence Report\n`;
    reportContent += `**Date**: ${new Date().toLocaleDateString()}\n`;
    reportContent += `**Company**: ${config.businessContext.company}\n\n`;
    
    // Add session summaries
    if (fs.existsSync(CONFIG.sessionsDir)) {
      const sessions = fs.readdirSync(CONFIG.sessionsDir)
        .filter(dir => fs.statSync(path.join(CONFIG.sessionsDir, dir)).isDirectory())
        .sort()
        .slice(-5); // Last 5 sessions
      
      if (sessions.length > 0) {
        reportContent += `## Recent Discovery Sessions\n\n`;
        for (const session of sessions) {
          const sessionPath = path.join(CONFIG.sessionsDir, session);
          const notesFile = path.join(sessionPath, 'discovery-notes.md');
          if (fs.existsSync(notesFile)) {
            const notes = fs.readFileSync(notesFile, 'utf8');
            reportContent += `### ${session}\n${notes}\n\n`;
          }
        }
      }
    }
    
    fs.writeFileSync(reportFile, reportContent);
    console.log(`📊 Report saved to: ${reportFile}`);
    
    return reportFile;
  }
}

// Command line interface
async function main() {
  const args = process.argv.slice(2);
  const discovery = new BusinessDiscovery();
  
  if (args.length === 0) {
    console.log('🤖 C-Level Business Discovery - AI Studio Integration');
    console.log('====================================================');
    console.log('');
    console.log('Usage:');
    console.log('  node ai-studio-integration.js --session "Session Name"');
    console.log('  node ai-studio-integration.js --analyze-market "AI Sales Automation" "Technology" "C-Level"');
    console.log('  node ai-studio-integration.js --evaluate-opportunity "AI-Powered CRM"');
    console.log('  node ai-studio-integration.js --strategic-plan');
    console.log('  node ai-studio-integration.js --financial-model "AI Sales Platform"');
    console.log('  node ai-studio-integration.js --report monthly');
    console.log('');
    return;
  }
  
  try {
    if (args[0] === '--session' && args[1]) {
      await discovery.startSession(args[1]);
    } else if (args[0] === '--analyze-market' && args[1] && args[2] && args[3]) {
      await discovery.analyzeMarket(args[1], args[2], args[3]);
    } else if (args[0] === '--evaluate-opportunity' && args[1]) {
      await discovery.evaluateOpportunity(args[1]);
    } else if (args[0] === '--strategic-plan') {
      await discovery.createStrategicPlan();
    } else if (args[0] === '--financial-model' && args[1]) {
      await discovery.buildFinancialModel(args[1]);
    } else if (args[0] === '--report' && args[1]) {
      await discovery.generateReport(args[1]);
    } else {
      console.log('❌ Invalid arguments. Use --help for usage information.');
    }
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

module.exports = { AIStudioClient, BusinessDiscovery };

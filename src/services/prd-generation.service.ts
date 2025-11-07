/**
 * PRD Generation Service
 *
 * Converts free-form conversation into a structured Product Requirements Document (PRD)
 * This is the foundation for both Express and Concierge tiers
 *
 * Supports:
 * - Natural language conversation → structured requirements
 * - Existing website URL as baseline (for "Website Refresh" product)
 * - Brand guideline locking (1 URL marked as "Must Follow")
 * - Iterative refinement with user feedback
 */

import { ProjectIntake, InspirationWebsite } from '../types/project';

interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

interface PRD {
  project_name: string;
  executive_summary: string;
  problem_statement: string;
  target_audience: {
    primary: string;
    secondary?: string;
  };
  user_stories: {
    id: string;
    as_a: string;
    i_want: string;
    so_that: string;
    priority: 'must-have' | 'should-have' | 'nice-to-have';
    acceptance_criteria: string[];
  }[];
  features: {
    id: string;
    name: string;
    description: string;
    user_story_ids: string[];
    technical_requirements?: string[];
  }[];
  non_functional_requirements: {
    category: 'performance' | 'security' | 'accessibility' | 'scalability' | 'usability';
    requirement: string;
    rationale: string;
  }[];
  inspiration_sources: InspirationWebsite[];
  success_metrics: {
    metric: string;
    target: string;
    measurement_method: string;
  }[];
  out_of_scope: string[];
  assumptions: string[];
  constraints: string[];
  timeline_estimate?: string;
  budget_estimate?: string;
}

interface PRDGenerationResult {
  prd: PRD;
  confidence: number; // 0.0 to 1.0
  missing_information: string[];
  clarifying_questions: string[];
  conversation_history: ConversationMessage[];
}

/**
 * Website Refresh Modes
 */
export enum WebsiteRefreshMode {
  PRESERVE_BRAND = 'preserve_brand',     // Keep branding, modernize UX
  REFRESH_BRAND = 'refresh_brand',       // Keep screens/flow, new branding
  FULL_MODERNIZATION = 'full_modernization' // Modernize both UX and brand
}

/**
 * PRD Input Types
 */
export enum PRDInputType {
  GENERATE = 'generate',       // Generate PRD from conversation
  IMPORT = 'import',           // Import existing PRD document
  AUGMENT = 'augment'          // Start with partial PRD, fill gaps via conversation
}

interface PRDConfig {
  geminiApiKey: string;
  model?: string;
}

/**
 * PRD Generation Service using Gemini
 */
export class PRDGenerationService {
  private apiKey: string;
  private model: string;

  constructor(config: PRDConfig) {
    this.apiKey = config.geminiApiKey;
    this.model = config.model || 'gemini-1.5-pro';
  }

  /**
   * MAIN ENTRY POINT: Process PRD input (generate, import, or augment)
   */
  async processPRDInput(
    inputType: PRDInputType,
    input: {
      conversation?: ConversationMessage[];
      existingPRD?: PRD | Partial<PRD>;
      prdDocument?: string; // Markdown/text PRD document
      existingWebsiteUrl?: string;
      websiteRefreshMode?: WebsiteRefreshMode;
    }
  ): Promise<PRDGenerationResult> {
    switch (inputType) {
      case PRDInputType.GENERATE:
        return this.generatePRDFromConversation(
          input.conversation || [],
          input.existingWebsiteUrl,
          input.websiteRefreshMode
        );

      case PRDInputType.IMPORT:
        return this.importPRDDocument(
          input.prdDocument || input.existingPRD!
        );

      case PRDInputType.AUGMENT:
        return this.augmentPartialPRD(
          input.existingPRD!,
          input.conversation || []
        );

      default:
        throw new Error(`Unknown PRD input type: ${inputType}`);
    }
  }

  /**
   * Generate PRD from free-form conversation
   *
   * This is the entry point for both tiers - converts unstructured ideas
   * into a structured PRD that can be executed
   */
  async generatePRDFromConversation(
    conversationHistory: ConversationMessage[],
    existingWebsiteUrl?: string, // For "Website Refresh" product
    websiteRefreshMode: WebsiteRefreshMode = WebsiteRefreshMode.PRESERVE_BRAND
  ): Promise<PRDGenerationResult> {
    console.log('📝 Generating PRD from conversation...');
    console.log(`📊 Conversation length: ${conversationHistory.length} messages`);
    if (existingWebsiteUrl) {
      console.log(`🌐 Baseline website: ${existingWebsiteUrl}`);
      console.log(`🎨 Refresh mode: ${websiteRefreshMode}`);
    }

    // Build prompt for PRD generation
    const prompt = this.buildPRDGenerationPrompt(conversationHistory, existingWebsiteUrl);

    // Call Gemini
    const response = await this.callGemini(prompt);

    // Parse structured output
    const prd = this.parsePRDFromResponse(response);

    // Analyze completeness
    const analysis = this.analyzePRDCompleteness(prd);

    return {
      prd,
      confidence: analysis.confidence,
      missing_information: analysis.missing_information,
      clarifying_questions: analysis.clarifying_questions,
      conversation_history: conversationHistory,
    };
  }

  /**
   * Refine PRD based on user feedback
   * Iterative process to ensure PRD is complete and accurate
   */
  async refinePRD(
    currentPRD: PRD,
    userFeedback: string,
    conversationHistory: ConversationMessage[]
  ): Promise<PRDGenerationResult> {
    console.log('🔄 Refining PRD based on feedback...');

    const prompt = `You are refining a Product Requirements Document based on user feedback.

**Current PRD:**
${JSON.stringify(currentPRD, null, 2)}

**User Feedback:**
${userFeedback}

**Conversation History:**
${conversationHistory.map((m) => `${m.role}: ${m.content}`).join('\n')}

Generate an updated PRD that incorporates the feedback. Maintain all existing information unless explicitly contradicted by the feedback.

Return as JSON with the complete PRD structure.`;

    const response = await this.callGemini(prompt);
    const updatedPRD = this.parsePRDFromResponse(response);
    const analysis = this.analyzePRDCompleteness(updatedPRD);

    return {
      prd: updatedPRD,
      confidence: analysis.confidence,
      missing_information: analysis.missing_information,
      clarifying_questions: analysis.clarifying_questions,
      conversation_history: [
        ...conversationHistory,
        { role: 'user', content: userFeedback, timestamp: new Date().toISOString() },
      ],
    };
  }

  /**
   * Import existing PRD document
   * Accepts PRD as markdown/text or structured object
   */
  async importPRDDocument(
    prdInput: string | PRD | Partial<PRD>
  ): Promise<PRDGenerationResult> {
    console.log('📥 Importing existing PRD document...');

    let prd: PRD;

    if (typeof prdInput === 'string') {
      // Parse markdown/text PRD into structured format
      const prompt = `You are a product manager. Parse this PRD document into structured format.

**PRD Document:**
${prdInput}

Convert to structured JSON matching this schema:
{
  "project_name": string,
  "executive_summary": string,
  "problem_statement": string,
  "target_audience": { "primary": string, "secondary"?: string },
  "user_stories": [{ id, as_a, i_want, so_that, priority, acceptance_criteria[] }],
  "features": [{ id, name, description, user_story_ids[], technical_requirements[]? }],
  "non_functional_requirements": [{ category, requirement, rationale }],
  "inspiration_sources": [{ url, locked, notes }],
  "success_metrics": [{ metric, target, measurement_method }],
  "out_of_scope": string[],
  "assumptions": string[],
  "constraints": string[]
}

If information is missing, use empty arrays or reasonable defaults. Mark any URLs mentioned as inspiration sources.`;

      const response = await this.callGemini(prompt);
      prd = this.parsePRDFromResponse(response);
    } else if ('project_name' in prdInput && 'user_stories' in prdInput) {
      // Already structured PRD
      prd = prdInput as PRD;
    } else {
      // Partial PRD - fill in missing fields
      prd = this.fillMissingPRDFields(prdInput as Partial<PRD>);
    }

    const analysis = this.analyzePRDCompleteness(prd);

    console.log(`✅ PRD Imported`);
    console.log(`   Confidence: ${(analysis.confidence * 100).toFixed(0)}%`);
    if (analysis.missing_information.length > 0) {
      console.log(`   Missing: ${analysis.missing_information.join(', ')}`);
    }

    return {
      prd,
      confidence: analysis.confidence,
      missing_information: analysis.missing_information,
      clarifying_questions: analysis.clarifying_questions,
      conversation_history: [],
    };
  }

  /**
   * Augment partial PRD with conversation
   * Start with existing PRD elements, fill gaps via conversation
   */
  async augmentPartialPRD(
    partialPRD: Partial<PRD>,
    conversationHistory: ConversationMessage[]
  ): Promise<PRDGenerationResult> {
    console.log('🔧 Augmenting partial PRD with conversation...');

    const conversationText = conversationHistory
      .map((m) => `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`)
      .join('\n\n');

    const prompt = `You are a product manager. Complete this partial PRD using information from the conversation.

**Partial PRD:**
${JSON.stringify(partialPRD, null, 2)}

**Conversation:**
${conversationText}

Generate a complete PRD that:
1. Preserves ALL existing information from the partial PRD
2. Fills in missing fields using conversation context
3. Expands on incomplete sections
4. Maintains consistency with existing content

Return complete PRD as structured JSON.`;

    const response = await this.callGemini(prompt);
    const completedPRD = this.parsePRDFromResponse(response);

    const analysis = this.analyzePRDCompleteness(completedPRD);

    console.log(`✅ PRD Augmented`);
    console.log(`   Confidence: ${(analysis.confidence * 100).toFixed(0)}%`);

    return {
      prd: completedPRD,
      confidence: analysis.confidence,
      missing_information: analysis.missing_information,
      clarifying_questions: analysis.clarifying_questions,
      conversation_history: conversationHistory,
    };
  }

  /**
   * Convert PRD to ProjectIntake format
   * This bridges the PRD to the actual workflow execution
   */
  convertPRDToIntake(prd: PRD, serviceTier: 'express' | 'concierge'): ProjectIntake {
    return {
      appName: prd.project_name,
      appConcept: `${prd.executive_summary}\n\n${prd.problem_statement}`,
      serviceTier,
      inspirationWebsites: prd.inspiration_sources,
      targetAudience: prd.target_audience.primary,
      designPreferences: prd.non_functional_requirements
        .filter((r) => r.category === 'usability')
        .map((r) => r.requirement)
        .join('; '),
    };
  }

  /**
   * Analyze existing website for "Website Refresh" use case
   * Supports different refresh modes:
   * - PRESERVE_BRAND: Keep branding, modernize UX
   * - REFRESH_BRAND: Keep screens/flow, apply new branding
   * - FULL_MODERNIZATION: Modernize both
   */
  async analyzeExistingWebsite(
    websiteUrl: string,
    refreshMode: WebsiteRefreshMode = WebsiteRefreshMode.PRESERVE_BRAND
  ): Promise<{
    screenshot: string;
    refresh_mode: WebsiteRefreshMode;

    // Brand analysis (always extracted, but usage depends on mode)
    brand_analysis: {
      colors: string[];
      typography: { family: string; usage: string }[];
      logo_url?: string;
      brand_guidelines: string[]; // Used if PRESERVE_BRAND
      should_preserve: boolean; // True for PRESERVE_BRAND, false for REFRESH_BRAND
    };

    // Screens/flow analysis (used for REFRESH_BRAND)
    screens_analysis: {
      identified_screens: { name: string; purpose: string; key_elements: string[] }[];
      user_flows: { flow_name: string; steps: string[] }[];
      navigation_patterns: string[];
      information_architecture: string;
    };

    ux_analysis: {
      strengths: string[];
      weaknesses: string[];
      opportunities: string[];
    };

    technical_analysis: {
      framework?: string;
      responsive: boolean;
      accessibility_score?: number;
      performance_issues: string[];
    };

    recommended_improvements: {
      ux_improvements: string[]; // Always recommended
      brand_refresh_ideas?: string[]; // If REFRESH_BRAND
    };
  }> {
    console.log(`🔍 Analyzing existing website: ${websiteUrl}`);
    console.log(`🎨 Refresh mode: ${refreshMode}`);

    // Capture screenshot (this would use the screenshot service)
    const screenshot = 'base64-screenshot'; // TODO: Actual implementation

    // Analyze with vision
    const modeInstructions = {
      [WebsiteRefreshMode.PRESERVE_BRAND]: `
This is a PRESERVE BRAND refresh - we'll modernize the UX while keeping the brand identity intact.
Focus on extracting brand guidelines that MUST be preserved (colors, typography, logo usage).`,
      [WebsiteRefreshMode.REFRESH_BRAND]: `
This is a REFRESH BRAND project - we'll keep the screens and user flows but apply entirely new branding.
Focus on extracting the information architecture, user flows, and screen structure.
Brand analysis is for reference only - we'll replace it with new branding.`,
      [WebsiteRefreshMode.FULL_MODERNIZATION]: `
This is a FULL MODERNIZATION - we'll update both UX and branding.
Analyze both the current brand and UX, but we'll be replacing both.`,
    };

    const analysisPrompt = `Analyze this existing website screenshot from ${websiteUrl}.

**Refresh Mode: ${refreshMode}**
${modeInstructions[refreshMode]}

Provide comprehensive analysis:

1. **Brand Analysis**:
   - Extract color palette (hex codes)
   - Identify typography (font families and usage)
   - Locate logo
   - Extract brand guidelines
   - should_preserve: ${refreshMode === WebsiteRefreshMode.PRESERVE_BRAND}

2. **Screens/Flow Analysis** ${refreshMode === WebsiteRefreshMode.REFRESH_BRAND ? '(CRITICAL for this mode)' : ''}:
   - Identify all screens/pages visible or implied
   - Map out user flows (e.g., "Homepage → Product → Cart → Checkout")
   - Document navigation patterns
   - Describe information architecture

3. **UX Analysis**:
   - Strengths: What works well
   - Weaknesses: What needs improvement
   - Opportunities: Modern UX patterns that could enhance it

4. **Technical Analysis**:
   - Detect framework if possible
   - Assess responsiveness
   - Identify performance issues

5. **Recommended Improvements**:
   - ux_improvements: Always include
   - brand_refresh_ideas: ${refreshMode === WebsiteRefreshMode.REFRESH_BRAND ? 'Include fresh branding ideas' : 'Only if full modernization'}

Return as structured JSON matching this schema:
{
  "screenshot": "base64-placeholder",
  "refresh_mode": "${refreshMode}",
  "brand_analysis": {
    "colors": ["#hex1", "#hex2"],
    "typography": [{ "family": "Font Name", "usage": "headings/body" }],
    "logo_url": "url or null",
    "brand_guidelines": ["guideline1", "guideline2"],
    "should_preserve": ${refreshMode === WebsiteRefreshMode.PRESERVE_BRAND}
  },
  "screens_analysis": {
    "identified_screens": [{ "name": "Home", "purpose": "...", "key_elements": ["nav", "hero"] }],
    "user_flows": [{ "flow_name": "Purchase Flow", "steps": ["Browse", "Add to Cart", "Checkout"] }],
    "navigation_patterns": ["Top nav", "Footer links"],
    "information_architecture": "Description of how content is organized"
  },
  "ux_analysis": { "strengths": [], "weaknesses": [], "opportunities": [] },
  "technical_analysis": { "framework": "React", "responsive": true, "performance_issues": [] },
  "recommended_improvements": {
    "ux_improvements": [],
    "brand_refresh_ideas": []
  }
}`;

    // TODO: Actual Gemini call with vision
    const response = await this.callGemini(analysisPrompt);

    return this.parseWebsiteAnalysis(response);
  }

  /**
   * Build PRD generation prompt
   */
  private buildPRDGenerationPrompt(
    conversationHistory: ConversationMessage[],
    existingWebsiteUrl?: string
  ): string {
    const conversationText = conversationHistory
      .map((m) => `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`)
      .join('\n\n');

    return `You are a senior product manager. Generate a comprehensive Product Requirements Document (PRD) from this conversation.

${existingWebsiteUrl ? `**WEBSITE REFRESH PROJECT**\nThis is a website refresh project for: ${existingWebsiteUrl}\nThe PRD should focus on modernizing and improving the existing site while preserving its core brand identity.\n\n` : ''}**Conversation:**
${conversationText}

Generate a complete PRD with:

1. **Project Name**: Clear, concise name
2. **Executive Summary**: 2-3 sentence overview
3. **Problem Statement**: What problem does this solve?
4. **Target Audience**: Primary (and optional secondary) users
5. **User Stories**: 6-10 stories in "As a [role], I want [goal], so that [benefit]" format with acceptance criteria
6. **Features**: 5-8 features mapped to user stories
7. **Non-Functional Requirements**: Performance, security, accessibility, scalability, usability
8. **Inspiration Sources**: Extract any mentioned URLs or design references (up to 3, identify which should be "locked" as brand guideline)
9. **Success Metrics**: How will we measure success?
10. **Out of Scope**: What we're NOT building
11. **Assumptions**: What we're assuming to be true
12. **Constraints**: Technical, budget, or timeline constraints

**CRITICAL for Inspiration Sources**:
- Extract any URLs mentioned in the conversation
- If this is a website refresh, include ${existingWebsiteUrl} as the PRIMARY locked brand guideline
- Mark one source as "locked: true" if it represents mandatory brand guidelines
- Maximum 3 inspiration sources

Return as a structured JSON object with all fields. Use "unknown" or empty arrays if information is missing, but try to infer reasonable defaults from context.`;
  }

  /**
   * Call Gemini API
   */
  private async callGemini(prompt: string): Promise<string> {
    const { GoogleGenerativeAI } = await import('@google/generative-ai');
    const genAI = new GoogleGenerativeAI(this.apiKey);
    const model = genAI.getGenerativeModel({ model: this.model });

    const result = await model.generateContent(prompt);
    const response = await result.response;
    return response.text();
  }

  /**
   * Parse PRD from Gemini response
   */
  private parsePRDFromResponse(response: string): PRD {
    // Extract JSON from response
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Failed to parse PRD from response');
    }

    return JSON.parse(jsonMatch[0]);
  }

  /**
   * Analyze PRD completeness
   */
  private analyzePRDCompleteness(prd: PRD): {
    confidence: number;
    missing_information: string[];
    clarifying_questions: string[];
  } {
    const missing: string[] = [];
    const questions: string[] = [];

    // Check required fields
    if (!prd.project_name || prd.project_name === 'unknown') {
      missing.push('project_name');
      questions.push('What would you like to name this project?');
    }

    if (!prd.target_audience?.primary || prd.target_audience.primary === 'unknown') {
      missing.push('target_audience');
      questions.push('Who is the primary target audience for this application?');
    }

    if (!prd.user_stories || prd.user_stories.length === 0) {
      missing.push('user_stories');
      questions.push('Can you describe the main use cases or user journeys?');
    }

    if (!prd.inspiration_sources || prd.inspiration_sources.length === 0) {
      questions.push(
        'Do you have any websites or apps that inspire the design direction? (Optional: up to 3 URLs)'
      );
    }

    if (!prd.success_metrics || prd.success_metrics.length === 0) {
      questions.push('How will you measure the success of this project?');
    }

    // Calculate confidence
    const totalFields = 12; // Number of major PRD sections
    const missingFields = missing.length;
    const confidence = Math.max(0, (totalFields - missingFields) / totalFields);

    return {
      confidence,
      missing_information: missing,
      clarifying_questions: questions,
    };
  }

  /**
   * Parse website analysis
   */
  private parseWebsiteAnalysis(response: string): any {
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Failed to parse website analysis');
    }

    return JSON.parse(jsonMatch[0]);
  }

  /**
   * Fill in missing PRD fields with defaults
   */
  private fillMissingPRDFields(partialPRD: Partial<PRD>): PRD {
    return {
      project_name: partialPRD.project_name || 'Untitled Project',
      executive_summary: partialPRD.executive_summary || '',
      problem_statement: partialPRD.problem_statement || '',
      target_audience: partialPRD.target_audience || { primary: 'General users' },
      user_stories: partialPRD.user_stories || [],
      features: partialPRD.features || [],
      non_functional_requirements: partialPRD.non_functional_requirements || [],
      inspiration_sources: partialPRD.inspiration_sources || [],
      success_metrics: partialPRD.success_metrics || [],
      out_of_scope: partialPRD.out_of_scope || [],
      assumptions: partialPRD.assumptions || [],
      constraints: partialPRD.constraints || [],
      timeline_estimate: partialPRD.timeline_estimate,
      budget_estimate: partialPRD.budget_estimate,
    };
  }

  /**
   * Generate clarifying questions for interactive PRD refinement
   */
  async generateClarifyingQuestions(
    conversationHistory: ConversationMessage[],
    currentPRD?: Partial<PRD>
  ): Promise<string[]> {
    const prompt = `Based on this conversation, what clarifying questions should I ask to complete the PRD?

**Conversation:**
${conversationHistory.map((m) => `${m.role}: ${m.content}`).join('\n')}

${currentPRD ? `**Current PRD (Partial):**\n${JSON.stringify(currentPRD, null, 2)}` : ''}

Generate 3-5 specific, actionable questions that would help complete or refine the PRD. Focus on missing critical information.

Return as JSON array of strings.`;

    const response = await this.callGemini(prompt);
    const jsonMatch = response.match(/\[[\s\S]*\]/);

    if (!jsonMatch) {
      return [
        'Can you describe the main problem this application solves?',
        'Who is the primary target audience?',
        'What are the key features you envision?',
      ];
    }

    return JSON.parse(jsonMatch[0]);
  }
}

/**
 * Singleton instance
 */
let prdServiceInstance: PRDGenerationService | null = null;

export function getPRDService(apiKey?: string): PRDGenerationService {
  if (!prdServiceInstance && !apiKey) {
    throw new Error('Gemini API key required to initialize PRD service');
  }

  if (apiKey && !prdServiceInstance) {
    prdServiceInstance = new PRDGenerationService({ geminiApiKey: apiKey });
  }

  return prdServiceInstance!;
}

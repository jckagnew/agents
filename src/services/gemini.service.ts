/**
 * Gemini AI Service
 * Handles all Gemini-powered operations:
 * - Inspiration website analysis
 * - Problem deconstruction
 * - Screen mapping
 * - Stitch prompt generation
 */

import {
  ProjectIntake,
  InspirationWebsite,
  DesignAnalysis,
  ProblemDeconstruction,
  ScreenMapping,
  DesignSystem,
  UserStory,
  Feature,
  UXRequirement,
} from '../types/project';

// Note: This uses the Google AI SDK (formerly Generative AI)
// Install with: npm install @google/generative-ai

interface GeminiConfig {
  apiKey: string;
  model?: string;
}

/**
 * Gemini service for AI-powered design and planning operations
 */
export class GeminiService {
  private apiKey: string;
  private model: string;
  private genAI: any; // Will be GoogleGenerativeAI instance

  constructor(config: GeminiConfig) {
    this.apiKey = config.apiKey;
    this.model = config.model || 'gemini-1.5-pro';
  }

  /**
   * Initialize the Gemini SDK
   * Called lazily to avoid issues if API key not set
   */
  private async getGenerativeModel() {
    if (!this.genAI) {
      const { GoogleGenerativeAI } = await import('@google/generative-ai');
      this.genAI = new GoogleGenerativeAI(this.apiKey);
    }
    return this.genAI.getGenerativeModel({ model: this.model });
  }

  /**
   * STEP 1: Analyze inspiration website screenshots
   * Extracts design tokens, patterns, and brand guidelines
   */
  async analyzeInspirationWebsite(
    screenshot: string, // Base64 or URL
    websiteUrl: string,
    isLocked: boolean
  ): Promise<DesignAnalysis> {
    const model = await this.getGenerativeModel();

    const prompt = `Analyze this website design screenshot from ${websiteUrl}.
${isLocked ? '⚠️ THIS IS A LOCKED BRAND GUIDELINE - Extract exact brand rules that MUST be followed.' : ''}

Please analyze and extract:

1. **Color Palette**: List all primary colors used (hex codes if possible)
2. **Typography**:
   - Font families used for headings and body text
   - Font sizes for different heading levels and body text
3. **Layout Patterns**: Describe the layout structure, grid system, spacing patterns
4. **Spacing System**: Identify the base spacing unit and scale
5. **Component Styles**: Describe the visual style of:
   - Buttons (shape, size, hover states)
   - Cards (if present)
   - Input fields (if present)
6. **Overall Aesthetic**: Describe the overall design aesthetic (modern, minimalist, playful, etc.)
${isLocked ? `
7. **Brand Guidelines** (CRITICAL - this site is locked as brand guideline):
   - Logo usage rules
   - Color dos and don'ts
   - Typography rules
   - Any other strict brand requirements
` : ''}

Return your analysis as a structured JSON object with these exact keys:
{
  "color_palette": ["#hex1", "#hex2", ...],
  "typography": {
    "headings": ["Font Family 1", "Font Family 2"],
    "body": ["Font Family"],
    "sizes": {
      "h1": "48px",
      "h2": "36px",
      "h3": "24px",
      "body": "16px",
      "small": "14px"
    }
  },
  "layout_patterns": ["Pattern 1", "Pattern 2"],
  "spacing_system": {
    "base_unit": 8,
    "scale": [4, 8, 16, 24, 32, 48, 64]
  },
  "component_styles": {
    "buttons": ["Style description"],
    "cards": ["Style description"],
    "inputs": ["Style description"]
  },
  "overall_aesthetic": "Description",
  ${isLocked ? `"brand_guidelines": {
    "logo_usage": "Rules",
    "color_dos_donts": ["Do/Don't 1", "Do/Don't 2"],
    "typography_rules": ["Rule 1", "Rule 2"]
  }` : ''}
}`;

    const result = await model.generateContent([
      prompt,
      {
        inlineData: {
          mimeType: 'image/png',
          data: screenshot,
        },
      },
    ]);

    const response = await result.response;
    const text = response.text();

    // Parse JSON from response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Failed to parse design analysis from Gemini response');
    }

    return JSON.parse(jsonMatch[0]);
  }

  /**
   * STEP 2: Problem Deconstruction
   * Analyze app concept + inspiration websites → User stories, features, UX requirements
   */
  async generateProblemDeconstruction(
    intake: ProjectIntake,
    inspirationAnalyses: DesignAnalysis[]
  ): Promise<Omit<ProblemDeconstruction, 'id' | 'project_id' | 'created_at'>> {
    const model = await this.getGenerativeModel();

    const lockedGuideline = intake.inspirationWebsites.find((w) => w.locked);
    const lockedAnalysis = lockedGuideline
      ? inspirationAnalyses[intake.inspirationWebsites.indexOf(lockedGuideline)]
      : null;

    const prompt = `You are an expert product designer and UX researcher. Analyze this app concept and generate a comprehensive problem deconstruction.

**App Concept:**
${intake.appConcept}

**Target Audience:**
${intake.targetAudience || 'General users'}

**Design Preferences:**
${intake.designPreferences || 'No specific preferences'}

**Inspiration Websites:**
${intake.inspirationWebsites.map((w, i) => `
- ${w.url} ${w.locked ? '🔒 LOCKED BRAND GUIDELINE' : ''}
  ${w.notes}
  Design Analysis: ${JSON.stringify(inspirationAnalyses[i], null, 2)}
`).join('\n')}

${lockedGuideline && lockedAnalysis ? `
⚠️ **CRITICAL: Locked Brand Guideline**
The following design from ${lockedGuideline.url} is a LOCKED brand guideline and MUST be followed exactly:
${JSON.stringify(lockedAnalysis.brand_guidelines, null, 2)}
` : ''}

Generate a comprehensive problem deconstruction including:

1. **User Stories**: 8-12 user stories in the format "As a [role], I want [goal], so that [benefit]" with acceptance criteria
2. **Features**: Break down the app into 6-10 core features
3. **UX Requirements**: Define 10-15 UX requirements covering navigation, interaction, feedback, accessibility, and performance
4. **Design System**: Create a design system incorporating the inspiration website aesthetics${lockedGuideline ? ' (following the locked brand guideline exactly)' : ''}

Return your analysis as a structured JSON object with these exact keys:
{
  "user_stories": [
    {
      "id": "us-1",
      "role": "user role",
      "goal": "what they want to do",
      "benefit": "why they want it",
      "acceptance_criteria": ["criterion 1", "criterion 2"],
      "priority": "high" | "medium" | "low"
    }
  ],
  "features": [
    {
      "id": "feat-1",
      "name": "Feature name",
      "description": "Feature description",
      "user_stories": ["us-1", "us-2"],
      "complexity": "simple" | "moderate" | "complex",
      "required_for_mvp": true | false
    }
  ],
  "ux_requirements": [
    {
      "category": "navigation" | "interaction" | "feedback" | "accessibility" | "performance",
      "requirement": "The requirement",
      "rationale": "Why this matters"
    }
  ],
  "design_system": {
    "colors": {
      "primary": "#hex",
      "secondary": "#hex",
      "accent": "#hex",
      "background": "#hex",
      "surface": "#hex",
      "error": "#hex",
      "success": "#hex",
      "warning": "#hex",
      "text": {
        "primary": "#hex",
        "secondary": "#hex",
        "disabled": "#hex"
      }
    },
    "typography": {
      "fontFamily": {
        "heading": "Font name",
        "body": "Font name",
        "mono": "Font name"
      },
      "scale": {
        "h1": 32,
        "h2": 24,
        "h3": 20,
        "h4": 18,
        "body": 16,
        "small": 14
      },
      "weights": {
        "light": 300,
        "regular": 400,
        "medium": 500,
        "bold": 700
      }
    },
    "spacing": {
      "baseUnit": 8,
      "scale": [4, 8, 16, 24, 32, 48, 64]
    },
    "borderRadius": {
      "small": 4,
      "medium": 8,
      "large": 16,
      "full": 9999
    },
    "shadows": {
      "small": "shadow definition",
      "medium": "shadow definition",
      "large": "shadow definition"
    }
  }
}`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    // Parse JSON from response
    const jsonMatch = text.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Failed to parse problem deconstruction from Gemini response');
    }

    const parsed = JSON.parse(jsonMatch[0]);

    return {
      user_stories: parsed.user_stories,
      features: parsed.features,
      ux_requirements: parsed.ux_requirements,
      design_system: parsed.design_system,
      model_version: this.model,
      prompt_tokens: 0, // TODO: Extract from response metadata
      completion_tokens: 0, // TODO: Extract from response metadata
    };
  }

  /**
   * STEP 3: Screen Mapping
   * Map features to screens and generate Stitch prompts for each
   */
  async generateScreenMappings(
    problemDeconstruction: Pick<
      ProblemDeconstruction,
      'features' | 'user_stories' | 'design_system'
    >
  ): Promise<Omit<ScreenMapping, 'id' | 'project_id' | 'problem_deconstruction_id' | 'created_at'>[]> {
    const model = await this.getGenerativeModel();

    const prompt = `You are an expert mobile app designer. Based on these features and user stories, map them to screens and generate Stitch prompts.

**Features:**
${JSON.stringify(problemDeconstruction.features, null, 2)}

**User Stories:**
${JSON.stringify(problemDeconstruction.user_stories, null, 2)}

**Design System:**
${JSON.stringify(problemDeconstruction.design_system, null, 2)}

Generate a comprehensive screen mapping:

1. Identify 6-12 core screens needed for the app
2. Map features to screens
3. For each screen, generate a detailed Stitch prompt that:
   - Describes the screen layout and components
   - References the design system colors, typography, spacing
   - Specifies user interactions and states
   - Is detailed enough for Stitch to generate a high-quality design
4. Define navigation context (parent/child relationships, tab bar)
5. List state variations (empty, loading, error, success, etc.)

Return as JSON array:
[
  {
    "screen_name": "Login",
    "screen_type": "authentication" | "onboarding" | "main" | "detail" | "form" | "settings",
    "features": ["feat-1", "feat-2"],
    "stitch_prompt": "Design a mobile login screen with...[DETAILED PROMPT]",
    "navigation_context": {
      "parent_screen": null,
      "child_screens": ["ForgotPassword"],
      "tab_bar_item": false
    },
    "state_variations": ["default", "loading", "error"]
  }
]`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    const text = response.text();

    // Parse JSON from response
    const jsonMatch = text.match(/\[[\s\S]*\]/);
    if (!jsonMatch) {
      throw new Error('Failed to parse screen mappings from Gemini response');
    }

    return JSON.parse(jsonMatch[0]);
  }

  /**
   * STEP 4: Generate individual Stitch prompt for a specific screen and state
   * This creates a highly detailed, Stitch-optimized prompt
   */
  async generateStitchPrompt(
    screenMapping: ScreenMapping,
    designSystem: DesignSystem,
    stateVariation: string = 'default'
  ): Promise<string> {
    const model = await this.getGenerativeModel();

    const prompt = `Generate an extremely detailed Stitch prompt for the following screen.

**Screen Name:** ${screenMapping.screen_name}
**Screen Type:** ${screenMapping.screen_type}
**State Variation:** ${stateVariation}

**Base Stitch Prompt:**
${screenMapping.stitch_prompt}

**Design System to Apply:**
${JSON.stringify(designSystem, null, 2)}

Create a detailed, Stitch-optimized prompt that:
1. Describes exact layout with specific measurements
2. References exact colors from the design system (use hex codes)
3. Specifies typography with exact font sizes and weights
4. Details all interactive elements and their states
5. Describes the ${stateVariation} state clearly
6. Includes spacing using the design system's spacing scale
7. Is written in a clear, directive style that Stitch can interpret

The prompt should be 3-5 paragraphs, highly specific, and actionable for Stitch AI.

Return ONLY the prompt text, no JSON or extra formatting.`;

    const result = await model.generateContent(prompt);
    const response = await result.response;
    return response.text().trim();
  }

  /**
   * Estimate cost of an AI generation
   * Gemini 1.5 Pro pricing (as of 2024):
   * - Input: $3.50 per 1M tokens
   * - Output: $10.50 per 1M tokens
   */
  calculateCost(promptTokens: number, completionTokens: number): number {
    const inputCost = (promptTokens / 1_000_000) * 3.5;
    const outputCost = (completionTokens / 1_000_000) * 10.5;
    return inputCost + outputCost;
  }
}

/**
 * Singleton instance
 */
let geminiServiceInstance: GeminiService | null = null;

export function getGeminiService(apiKey?: string): GeminiService {
  if (!geminiServiceInstance && !apiKey) {
    throw new Error('Gemini API key required to initialize service');
  }

  if (apiKey && !geminiServiceInstance) {
    geminiServiceInstance = new GeminiService({ apiKey });
  }

  return geminiServiceInstance!;
}

/**
 * Codex Service - Agent-in-the-Loop Frontend Generation
 *
 * Uses OpenAI Codex's multimodal capabilities to:
 * 1. Generate frontend designs from requirements
 * 2. Visually compare against inspiration/benchmark screenshots
 * 3. Iterate automatically until design matches benchmarks
 * 4. Export production-ready code
 *
 * This enables fully automated Express tier workflow without human approval
 */

import { ProjectIntake, DesignSystem, ScreenMapping, InspirationWebsite } from '../types/project';

interface CodexConfig {
  apiKey: string;
  model?: string;
}

interface DesignIteration {
  iteration_number: number;
  generated_code: string;
  screenshot_url: string;
  comparison_score: number; // 0.0 to 1.0
  visual_diff_url?: string;
  feedback: string[];
  improvements_needed: string[];
}

interface DesignGenerationResult {
  screen_name: string;
  final_code: string;
  iterations: DesignIteration[];
  total_iterations: number;
  final_score: number;
  confidence: number;
}

/**
 * Codex service for automated frontend generation with visual validation
 */
export class CodexService {
  private apiKey: string;
  private model: string;
  private maxIterations: number;
  private targetScore: number;

  constructor(config: CodexConfig) {
    this.apiKey = config.apiKey;
    this.model = config.model || 'gpt-4o'; // GPT-4o has vision capabilities
    this.maxIterations = 5; // Max iterations before giving up
    this.targetScore = 0.85; // Target visual similarity score
  }

  /**
   * EXPRESS TIER: Fully automated design generation with agent-in-the-loop
   *
   * This replaces the human Stitch workflow with an automated agent that:
   * 1. Generates initial design from requirements
   * 2. Renders it and captures screenshot
   * 3. Compares against inspiration screenshots
   * 4. Iterates to improve until it matches benchmarks
   */
  async generateDesignWithIterativeValidation(
    screenMapping: ScreenMapping,
    designSystem: DesignSystem,
    inspirationScreenshots: { url: string; screenshot: string; locked: boolean }[],
    targetPlatform: 'react-native' | 'web' = 'react-native'
  ): Promise<DesignGenerationResult> {
    const iterations: DesignIteration[] = [];
    let currentCode = '';
    let currentScore = 0;
    let iterationCount = 0;

    // Get the locked inspiration as primary benchmark
    const primaryBenchmark = inspirationScreenshots.find((i) => i.locked) || inspirationScreenshots[0];

    console.log(`🤖 Starting agent-in-the-loop design generation for ${screenMapping.screen_name}`);
    console.log(`📊 Target score: ${this.targetScore}, Max iterations: ${this.maxIterations}`);

    while (iterationCount < this.maxIterations && currentScore < this.targetScore) {
      iterationCount++;
      console.log(`\n🔄 Iteration ${iterationCount}/${this.maxIterations}`);

      // STEP 1: Generate or refine the design
      if (iterationCount === 1) {
        // First iteration: Generate from scratch
        currentCode = await this.generateInitialDesign(
          screenMapping,
          designSystem,
          inspirationScreenshots,
          targetPlatform
        );
      } else {
        // Subsequent iterations: Refine based on comparison feedback
        const previousIteration = iterations[iterations.length - 1];
        currentCode = await this.refineDesign(
          screenMapping,
          designSystem,
          currentCode,
          previousIteration.feedback,
          primaryBenchmark.screenshot,
          targetPlatform
        );
      }

      // STEP 2: Render the design and capture screenshot
      const screenshot = await this.renderAndCaptureScreenshot(
        currentCode,
        screenMapping.screen_name,
        targetPlatform
      );

      // STEP 3: Compare against benchmark using vision
      const comparison = await this.compareDesignAgainstBenchmark(
        screenshot,
        primaryBenchmark.screenshot,
        designSystem,
        screenMapping
      );

      // STEP 4: Record iteration
      iterations.push({
        iteration_number: iterationCount,
        generated_code: currentCode,
        screenshot_url: screenshot,
        comparison_score: comparison.score,
        visual_diff_url: comparison.diff_url,
        feedback: comparison.feedback,
        improvements_needed: comparison.improvements_needed,
      });

      currentScore = comparison.score;

      console.log(`✅ Score: ${currentScore.toFixed(3)} (target: ${this.targetScore})`);
      console.log(`📝 Feedback: ${comparison.feedback.join(', ')}`);

      // Early exit if we hit target score
      if (currentScore >= this.targetScore) {
        console.log(`🎉 Target score reached! Final score: ${currentScore.toFixed(3)}`);
        break;
      }

      // Warn if not improving
      if (iterationCount > 1) {
        const previousScore = iterations[iterations.length - 2].comparison_score;
        if (currentScore <= previousScore) {
          console.warn(`⚠️ Score not improving (${previousScore.toFixed(3)} → ${currentScore.toFixed(3)})`);
        }
      }
    }

    return {
      screen_name: screenMapping.screen_name,
      final_code: currentCode,
      iterations,
      total_iterations: iterationCount,
      final_score: currentScore,
      confidence: this.calculateConfidence(currentScore, iterationCount),
    };
  }

  /**
   * Generate initial design from requirements and inspiration
   */
  private async generateInitialDesign(
    screenMapping: ScreenMapping,
    designSystem: DesignSystem,
    inspirationScreenshots: { url: string; screenshot: string; locked: boolean }[],
    targetPlatform: 'react-native' | 'web'
  ): Promise<string> {
    const messages: any[] = [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: `You are an expert ${targetPlatform === 'react-native' ? 'React Native' : 'React'} frontend developer. Generate a beautiful, pixel-perfect implementation of this screen.

**Screen Name:** ${screenMapping.screen_name}
**Screen Type:** ${screenMapping.screen_type}

**Requirements:**
${screenMapping.stitch_prompt}

**Design System:**
${JSON.stringify(designSystem, null, 2)}

**Inspiration Designs:**
Below are ${inspirationScreenshots.length} inspiration screenshots. Your goal is to match their visual aesthetic while implementing the requirements above.
${inspirationScreenshots.map((i, idx) => `
${idx + 1}. ${i.url} ${i.locked ? '🔒 PRIMARY BENCHMARK - Match this design closely' : '(Reference for inspiration)'}
`).join('\n')}

**Output Format:**
Generate complete, production-ready ${targetPlatform === 'react-native' ? 'React Native with TypeScript' : 'React with TypeScript'} code including:
1. Component with all UI elements
2. StyleSheet with exact design system values
3. Interactive elements with proper state management
4. Accessibility props

Return ONLY the code, no explanations or markdown.`,
          },
          // Add inspiration screenshots as images
          ...inspirationScreenshots.map((screenshot) => ({
            type: 'image_url',
            image_url: { url: `data:image/png;base64,${screenshot.screenshot}` },
          })),
        ],
      },
    ];

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: this.model,
        messages,
        max_tokens: 16000,
        temperature: 0.3,
      }),
    });

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status}`);
    }

    const result = await response.json();
    return this.extractCodeFromResponse(result.choices[0].message.content);
  }

  /**
   * Refine existing design based on comparison feedback
   */
  private async refineDesign(
    screenMapping: ScreenMapping,
    designSystem: DesignSystem,
    currentCode: string,
    feedback: string[],
    benchmarkScreenshot: string,
    targetPlatform: 'react-native' | 'web'
  ): Promise<string> {
    const messages: any[] = [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: `You are refining a ${targetPlatform === 'react-native' ? 'React Native' : 'React'} component to better match a benchmark design.

**Current Code:**
\`\`\`typescript
${currentCode}
\`\`\`

**Design System (must follow exactly):**
${JSON.stringify(designSystem, null, 2)}

**Comparison Feedback:**
The current implementation has these visual differences from the benchmark:
${feedback.map((f, i) => `${i + 1}. ${f}`).join('\n')}

**Benchmark Design:**
Below is the target design you should match. Make the necessary changes to address all feedback points.

**Output:**
Return the complete, improved component code. Preserve all functionality but adjust visual styling to match the benchmark.`,
          },
          {
            type: 'image_url',
            image_url: { url: `data:image/png;base64,${benchmarkScreenshot}` },
          },
        ],
      },
    ];

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: this.model,
        messages,
        max_tokens: 16000,
        temperature: 0.2, // Lower temperature for refinement
      }),
    });

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status}`);
    }

    const result = await response.json();
    return this.extractCodeFromResponse(result.choices[0].message.content);
  }

  /**
   * Render design and capture screenshot using Playwright
   * This is the key "check your own work" capability
   */
  private async renderAndCaptureScreenshot(
    code: string,
    screenName: string,
    targetPlatform: 'react-native' | 'web'
  ): Promise<string> {
    // For React Native, we need to render in Expo web
    // For web, we render directly

    // TODO: Implement with Playwright MCP or similar
    // For now, return a placeholder
    // In production, this would:
    // 1. Write code to temp file
    // 2. Start dev server
    // 3. Open browser with Playwright
    // 4. Navigate to component
    // 5. Capture screenshot
    // 6. Return base64 screenshot

    console.log(`📸 Capturing screenshot for ${screenName}...`);

    // Placeholder - in production, use Playwright
    return 'base64-screenshot-placeholder';
  }

  /**
   * Compare generated design against benchmark using vision model
   * This is where the "agent checks its own work" happens
   */
  private async compareDesignAgainstBenchmark(
    generatedScreenshot: string,
    benchmarkScreenshot: string,
    designSystem: DesignSystem,
    screenMapping: ScreenMapping
  ): Promise<{
    score: number;
    feedback: string[];
    improvements_needed: string[];
    diff_url?: string;
  }> {
    const messages: any[] = [
      {
        role: 'user',
        content: [
          {
            type: 'text',
            text: `You are a design quality assurance agent. Compare these two screenshots and evaluate how closely the generated design matches the benchmark.

**Evaluation Criteria:**
1. **Layout Match** (25%): Do elements have the same positioning and hierarchy?
2. **Color Accuracy** (25%): Do colors match the design system?
3. **Typography** (20%): Do fonts, sizes, and weights match?
4. **Spacing** (15%): Is spacing consistent with the design system?
5. **Component Styling** (15%): Do buttons, cards, inputs match the benchmark style?

**Design System Reference:**
${JSON.stringify(designSystem, null, 2)}

**Screen Requirements:**
${screenMapping.stitch_prompt}

**Screenshot 1: Benchmark (target)**
**Screenshot 2: Generated (current implementation)**

**Output Format (JSON):**
{
  "score": 0.0-1.0,
  "layout_match": 0.0-1.0,
  "color_accuracy": 0.0-1.0,
  "typography": 0.0-1.0,
  "spacing": 0.0-1.0,
  "component_styling": 0.0-1.0,
  "feedback": ["specific observation 1", "specific observation 2"],
  "improvements_needed": ["change 1", "change 2", "change 3"]
}

Be specific and actionable in your feedback. If the score is below 0.85, provide clear instructions for improvement.`,
          },
          {
            type: 'image_url',
            image_url: { url: `data:image/png;base64,${benchmarkScreenshot}` },
          },
          {
            type: 'image_url',
            image_url: { url: `data:image/png;base64,${generatedScreenshot}` },
          },
        ],
      },
    ];

    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${this.apiKey}`,
      },
      body: JSON.stringify({
        model: this.model,
        messages,
        max_tokens: 2000,
        temperature: 0.1, // Very low temperature for consistent evaluation
      }),
    });

    if (!response.ok) {
      throw new Error(`OpenAI API error: ${response.status}`);
    }

    const result = await response.json();
    const content = result.choices[0].message.content;

    // Parse JSON response
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Failed to parse comparison result');
    }

    const parsed = JSON.parse(jsonMatch[0]);

    return {
      score: parsed.score,
      feedback: parsed.feedback,
      improvements_needed: parsed.improvements_needed,
      diff_url: undefined, // Could generate visual diff overlay
    };
  }

  /**
   * Calculate confidence based on final score and iteration count
   */
  private calculateConfidence(finalScore: number, iterations: number): number {
    // Perfect score on first try = 1.0 confidence
    // Perfect score after max iterations = 0.85 confidence
    // Below target score = proportional to score
    const iterationPenalty = (iterations - 1) / (this.maxIterations * 10);
    const baseConfidence = Math.min(finalScore, 1.0);
    return Math.max(0, baseConfidence - iterationPenalty);
  }

  /**
   * Extract code from model response (removing markdown fences, etc.)
   */
  private extractCodeFromResponse(response: string): string {
    // Remove markdown code fences if present
    let code = response.trim();

    // Remove ```typescript or ```tsx or ```javascript fences
    code = code.replace(/^```(?:typescript|tsx|javascript|jsx)?\n/i, '');
    code = code.replace(/\n```$/i, '');

    return code.trim();
  }

  /**
   * Generate multiple screens in parallel with agent-in-the-loop
   */
  async generateAllScreensWithValidation(
    screenMappings: ScreenMapping[],
    designSystem: DesignSystem,
    inspirationScreenshots: { url: string; screenshot: string; locked: boolean }[],
    targetPlatform: 'react-native' | 'web' = 'react-native'
  ): Promise<DesignGenerationResult[]> {
    console.log(`\n🚀 Starting batch generation for ${screenMappings.length} screens`);
    console.log(`📋 Screens: ${screenMappings.map((s) => s.screen_name).join(', ')}`);

    // Generate screens sequentially to avoid rate limits
    // In production, could implement parallel with rate limiting
    const results: DesignGenerationResult[] = [];

    for (const mapping of screenMappings) {
      const result = await this.generateDesignWithIterativeValidation(
        mapping,
        designSystem,
        inspirationScreenshots,
        targetPlatform
      );
      results.push(result);

      console.log(`\n✅ Completed ${result.screen_name}:`);
      console.log(`   - Final score: ${result.final_score.toFixed(3)}`);
      console.log(`   - Iterations: ${result.total_iterations}`);
      console.log(`   - Confidence: ${result.confidence.toFixed(3)}`);
    }

    return results;
  }
}

/**
 * Singleton instance
 */
let codexServiceInstance: CodexService | null = null;

export function getCodexService(apiKey?: string): CodexService {
  if (!codexServiceInstance && !apiKey) {
    throw new Error('OpenAI API key required to initialize Codex service');
  }

  if (apiKey && !codexServiceInstance) {
    codexServiceInstance = new CodexService({ apiKey });
  }

  return codexServiceInstance!;
}

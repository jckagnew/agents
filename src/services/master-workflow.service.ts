/**
 * Master Workflow Service - Unified Design-First Software Factory
 *
 * This is THE workflow that combines the best of both approaches:
 * - Express tier: Automated design + agent validation
 * - Concierge tier: Human design approval + agent validation
 *
 * Key Innovation: Agent-in-the-loop validates that GENERATED CODE matches APPROVED DESIGN
 * regardless of whether that design came from Codex (Express) or Stitch (Concierge)
 *
 * ┌─────────────────────────────────────────────────────────┐
 * │ UNIFIED WORKFLOW (Both Tiers)                           │
 * │                                                          │
 * │ 1. Conversation → PRD (Both)                            │
 * │ 2. Requirements Analysis (Both)                         │
 * │ 3. Design Approval:                                     │
 * │    - Express: Codex auto-generates                      │
 * │    - Concierge: Human iterates in Stitch               │
 * │ 4. Code Generation (Both)                               │
 * │ 5. Agent Validates: Code matches approved design (Both) │
 * │ 6. Package & Handoff (Both)                            │
 * └─────────────────────────────────────────────────────────┘
 */

import {
  ProjectIntake,
  ProblemDeconstruction,
  ScreenMapping,
  StitchDesign,
  Project,
} from '../types/project';
import { getPRDService, PRD, ConversationMessage } from './prd-generation.service';
import { getGeminiService } from './gemini.service';
import { getCodexService } from './codex.service';
import { getPlaywrightService } from './playwright.service';
import { getSupabaseService } from './supabase.service';

interface MasterWorkflowConfig {
  geminiApiKey: string;
  codexApiKey: string;
  supabaseConfig: any;
}

interface WorkflowResult {
  project_id: string;
  status: 'completed' | 'failed' | 'awaiting_human_approval';
  service_tier: 'express' | 'concierge';

  // Timing
  total_time_ms: number;
  phase_timings: {
    prd_generation: number;
    requirements_analysis: number;
    design_approval: number;
    code_generation: number;
    code_validation: number;
    packaging: number;
  };

  // Quality metrics
  code_validation_score: number; // How well does code match approved design?
  code_validation_iterations: number;
  screens_generated: number;

  // Outputs
  prd?: PRD;
  approved_designs?: any[]; // Stitch HTML or Codex screenshots
  zip_url?: string;

  // Cost tracking
  cost_breakdown: {
    prd_generation: number;
    gemini_analysis: number;
    codex_design?: number; // Express only
    code_generation: number;
    code_validation: number;
    total: number;
  };

  error?: string;
}

/**
 * Master Workflow Orchestrator
 */
export class MasterWorkflowService {
  private geminiApiKey: string;
  private codexApiKey: string;
  private supabaseConfig: any;

  constructor(config: MasterWorkflowConfig) {
    this.geminiApiKey = config.geminiApiKey;
    this.codexApiKey = config.codexApiKey;
    this.supabaseConfig = config.supabaseConfig;
  }

  /**
   * MAIN ENTRY POINT: Execute complete workflow from conversation to code
   *
   * This handles both Express and Concierge tiers in a unified way
   */
  async executeWorkflow(
    conversationHistory: ConversationMessage[],
    serviceTier: 'express' | 'concierge',
    existingWebsiteUrl?: string // For "Website Refresh" product
  ): Promise<WorkflowResult> {
    const startTime = Date.now();
    const phaseTimings: any = {};
    let projectId: string | null = null;

    try {
      console.log('\n🚀 MASTER WORKFLOW STARTING');
      console.log(`📋 Service Tier: ${serviceTier.toUpperCase()}`);
      console.log(`💬 Conversation length: ${conversationHistory.length} messages`);
      if (existingWebsiteUrl) {
        console.log(`🔄 Website Refresh: ${existingWebsiteUrl}`);
      }

      // ======================================================================
      // PHASE 1: PRD GENERATION (Both Tiers)
      // ======================================================================
      console.log('\n📝 PHASE 1: PRD Generation from conversation...');
      const prdStart = Date.now();

      const prdService = getPRDService(this.geminiApiKey);
      const prdResult = await prdService.generatePRDFromConversation(
        conversationHistory,
        existingWebsiteUrl
      );

      phaseTimings.prd_generation = Date.now() - prdStart;

      console.log(`✅ PRD Generated (${(phaseTimings.prd_generation / 1000).toFixed(1)}s)`);
      console.log(`   Project: ${prdResult.prd.project_name}`);
      console.log(`   User Stories: ${prdResult.prd.user_stories.length}`);
      console.log(`   Features: ${prdResult.prd.features.length}`);
      console.log(`   Confidence: ${(prdResult.confidence * 100).toFixed(0)}%`);

      if (prdResult.missing_information.length > 0) {
        console.warn(`   ⚠️  Missing: ${prdResult.missing_information.join(', ')}`);
      }

      // Convert PRD to intake format
      const intake = prdService.convertPRDToIntake(prdResult.prd, serviceTier);

      // ======================================================================
      // PHASE 2: REQUIREMENTS ANALYSIS (Both Tiers)
      // ======================================================================
      console.log('\n🧠 PHASE 2: Requirements Analysis...');
      const requirementsStart = Date.now();

      const gemini = getGeminiService(this.geminiApiKey);
      const supabase = getSupabaseService(this.supabaseConfig);

      // Capture inspiration screenshots (including locked brand guideline)
      console.log('📸 Capturing inspiration screenshots...');
      const inspirationScreenshots = await Promise.all(
        intake.inspirationWebsites.map(async (site) => {
          console.log(`   ${site.locked ? '🔒' : '  '} ${site.url}`);
          const screenshot = await supabase['captureWebsiteScreenshot'](site.url);
          return {
            url: site.url,
            screenshot,
            locked: site.locked,
            notes: site.notes,
          };
        })
      );

      // Analyze inspiration websites
      console.log('🔍 Analyzing design patterns...');
      const inspirationAnalyses = await Promise.all(
        inspirationScreenshots.map(async (site) => {
          return await gemini.analyzeInspirationWebsite(
            site.screenshot,
            site.url,
            site.locked
          );
        })
      );

      // Generate problem deconstruction
      console.log('🎯 Generating problem deconstruction...');
      const problemDeconstruction = await gemini.generateProblemDeconstruction(
        intake,
        inspirationAnalyses
      );

      // Generate screen mappings
      console.log('🗺️  Generating screen mappings...');
      const screenMappings = await gemini.generateScreenMappings({
        features: problemDeconstruction.features,
        user_stories: problemDeconstruction.user_stories,
        design_system: problemDeconstruction.design_system,
      });

      phaseTimings.requirements_analysis = Date.now() - requirementsStart;

      console.log(
        `✅ Requirements Analysis Complete (${(phaseTimings.requirements_analysis / 1000).toFixed(1)}s)`
      );
      console.log(`   Screens: ${screenMappings.length}`);
      console.log(`   Design System: ✓`);

      // Create project in database
      const project = await supabase.createProject({
        name: intake.appName,
        app_concept: intake.appConcept,
        service_tier: serviceTier,
        status: serviceTier === 'express' ? 'design_generation' : 'stitch_iteration',
      });

      projectId = project.id;

      // ======================================================================
      // PHASE 3: DESIGN APPROVAL (Diverges by Tier)
      // ======================================================================
      console.log(
        `\n🎨 PHASE 3: Design Approval (${serviceTier.toUpperCase()} TIER)...`
      );
      const designStart = Date.now();

      let approvedDesigns: any[];
      let codexCost = 0;

      if (serviceTier === 'express') {
        // ===================================================================
        // EXPRESS TIER: Codex generates designs automatically
        // ===================================================================
        console.log('🤖 Codex generating designs automatically...');

        const codex = getCodexService(this.codexApiKey);

        // Find locked brand guideline (the benchmark)
        const lockedGuideline = inspirationScreenshots.find((s) => s.locked);

        if (!lockedGuideline) {
          console.warn(
            '⚠️  No locked brand guideline found, using first inspiration as benchmark'
          );
        }

        // Codex generates each screen and validates against locked guideline
        const designResults = await codex.generateAllScreensWithValidation(
          screenMappings as ScreenMapping[],
          problemDeconstruction.design_system,
          inspirationScreenshots,
          'react-native'
        );

        approvedDesigns = designResults.map((result) => ({
          screen_name: result.screen_name,
          type: 'codex_generated',
          screenshot: result.iterations[result.iterations.length - 1].screenshot_url,
          code: result.final_code,
          quality_score: result.final_score,
          confidence: result.confidence,
          iterations: result.total_iterations,
        }));

        codexCost = designResults.reduce((sum, r) => sum + r.total_iterations * 0.05, 0);

        console.log(`✅ Codex Design Complete`);
        console.log(`   Average quality: ${(designResults.reduce((sum, r) => sum + r.final_score, 0) / designResults.length).toFixed(3)}`);
        console.log(`   Total iterations: ${designResults.reduce((sum, r) => sum + r.total_iterations, 0)}`);
      } else {
        // ===================================================================
        // CONCIERGE TIER: Human iterates in Stitch
        // ===================================================================
        console.log('👤 Awaiting human design approval in Stitch...');
        console.log(`   → Present Stitch prompts to user`);
        console.log(`   → User iterates in stitch.withgoogle.com`);
        console.log(`   → User uploads approved HTML designs`);

        // Update project status
        await supabase.updateProject(projectId, {
          status: 'stitch_iteration',
        });

        // Return early - workflow will resume after human uploads designs
        return {
          project_id: projectId,
          status: 'awaiting_human_approval',
          service_tier: serviceTier,
          total_time_ms: Date.now() - startTime,
          phase_timings: {
            ...phaseTimings,
            design_approval: Date.now() - designStart,
            code_generation: 0,
            code_validation: 0,
            packaging: 0,
          },
          code_validation_score: 0,
          code_validation_iterations: 0,
          screens_generated: screenMappings.length,
          prd: prdResult.prd,
          cost_breakdown: {
            prd_generation: 0.05,
            gemini_analysis: 0.15,
            code_generation: 0,
            code_validation: 0,
            total: 0.2,
          },
        };
      }

      phaseTimings.design_approval = Date.now() - designStart;

      // ======================================================================
      // PHASE 4: CODE GENERATION (Both Tiers Converge)
      // ======================================================================
      console.log('\n💻 PHASE 4: Code Generation...');
      const codeGenStart = Date.now();

      // For Express: Codex already generated Expo code in Phase 3
      // For Concierge: Convert Stitch HTML to Expo
      // (This would be called after user uploads HTML in Concierge tier)

      if (serviceTier === 'express') {
        // Code already generated by Codex
        console.log('✅ Expo code already generated by Codex');
      } else {
        // This branch would be executed in a separate call after human approval
        console.log('📝 Converting Stitch HTML to Expo...');
        // TODO: Implement HTML → Expo conversion
      }

      phaseTimings.code_generation = Date.now() - codeGenStart;

      // ======================================================================
      // PHASE 5: AGENT VALIDATES CODE MATCHES DESIGN (Both Tiers)
      // ======================================================================
      console.log('\n🔍 PHASE 5: Agent-in-the-Loop Code Validation...');
      console.log('Agent ensures generated code matches approved design');
      const validationStart = Date.now();

      const codex = getCodexService(this.codexApiKey);
      const playwright = getPlaywrightService();

      let totalValidationIterations = 0;
      let totalValidationScore = 0;

      // For each approved design, validate that generated code matches
      for (const design of approvedDesigns) {
        console.log(`\n📱 Validating: ${design.screen_name}`);

        // Render the generated code
        const renderedScreenshot = await playwright.renderComponentAndCapture(
          design.code,
          design.screen_name,
          'react-native'
        );

        // Compare rendered code against approved design
        const comparison = await codex['compareDesignAgainstBenchmark'](
          renderedScreenshot.screenshot,
          design.screenshot, // The approved design is the benchmark
          problemDeconstruction.design_system,
          screenMappings.find((s: any) => s.screen_name === design.screen_name)!
        );

        console.log(`   Score: ${comparison.score.toFixed(3)}`);

        totalValidationScore += comparison.score;

        // If code doesn't match design well enough, iterate
        let iterations = 0;
        let currentCode = design.code;
        let currentScore = comparison.score;

        while (currentScore < 0.85 && iterations < 3) {
          iterations++;
          console.log(`   🔄 Iteration ${iterations}: Refining code...`);

          // Refine code to better match approved design
          currentCode = await codex['refineDesign'](
            screenMappings.find((s: any) => s.screen_name === design.screen_name)!,
            problemDeconstruction.design_system,
            currentCode,
            comparison.feedback,
            design.screenshot,
            'react-native'
          );

          // Re-render and compare
          const newScreenshot = await playwright.renderComponentAndCapture(
            currentCode,
            design.screen_name,
            'react-native'
          );

          const newComparison = await codex['compareDesignAgainstBenchmark'](
            newScreenshot.screenshot,
            design.screenshot,
            problemDeconstruction.design_system,
            screenMappings.find((s: any) => s.screen_name === design.screen_name)!
          );

          currentScore = newComparison.score;
          console.log(`   Score: ${currentScore.toFixed(3)}`);

          if (currentScore >= 0.85) {
            console.log(`   ✅ Code matches design!`);
            design.code = currentCode; // Update with refined code
            break;
          }
        }

        totalValidationIterations += iterations;
      }

      phaseTimings.code_validation = Date.now() - validationStart;

      const avgValidationScore = totalValidationScore / approvedDesigns.length;

      console.log(
        `✅ Code Validation Complete (${(phaseTimings.code_validation / 1000).toFixed(1)}s)`
      );
      console.log(`   Average match score: ${avgValidationScore.toFixed(3)}`);
      console.log(`   Total iterations: ${totalValidationIterations}`);

      // ======================================================================
      // PHASE 6: PROJECT PACKAGING (Both Tiers)
      // ======================================================================
      console.log('\n📦 PHASE 6: Project Packaging...');
      const packagingStart = Date.now();

      // Save all code artifacts
      for (const design of approvedDesigns) {
        await supabase.saveCodeArtifact({
          project_id: projectId,
          artifact_type: 'screen',
          file_path: `src/screens/${design.screen_name}Screen.tsx`,
          content: design.code,
          conversion_confidence: design.confidence || avgValidationScore,
        });
      }

      // Generate navigation
      const navigationCode = this.generateNavigationCode(approvedDesigns);
      await supabase.saveCodeArtifact({
        project_id: projectId,
        artifact_type: 'navigation',
        file_path: 'src/navigation/AppNavigator.tsx',
        content: navigationCode,
      });

      // Generate theme
      const themeCode = `export const theme = ${JSON.stringify(problemDeconstruction.design_system, null, 2)};`;
      await supabase.saveCodeArtifact({
        project_id: projectId,
        artifact_type: 'component',
        file_path: 'src/theme/index.ts',
        content: themeCode,
      });

      // Generate package.json
      const packageJson = this.generatePackageJson(intake.appName);
      await supabase.saveCodeArtifact({
        project_id: projectId,
        artifact_type: 'full_project',
        file_path: 'package.json',
        content: packageJson,
      });

      // Package as ZIP
      const zipUrl = await supabase.packageProjectAsZip(projectId);

      // Update project status
      await supabase.updateProject(projectId, {
        status: 'complete',
      });

      phaseTimings.packaging = Date.now() - packagingStart;

      // Cleanup
      await playwright.cleanup();

      // ======================================================================
      // COMPLETE
      // ======================================================================
      const totalTime = Date.now() - startTime;

      console.log('\n✅ MASTER WORKFLOW COMPLETE');
      console.log(`⏱️  Total time: ${(totalTime / 1000).toFixed(1)}s`);
      console.log(`📦 Download: ${zipUrl}`);

      const costBreakdown = {
        prd_generation: 0.05,
        gemini_analysis: 0.15,
        codex_design: codexCost,
        code_generation: serviceTier === 'express' ? 0 : 0.8,
        code_validation: totalValidationIterations * 0.05,
        total: 0.2 + codexCost + (serviceTier === 'express' ? 0 : 0.8) + totalValidationIterations * 0.05,
      };

      return {
        project_id: projectId,
        status: 'completed',
        service_tier: serviceTier,
        total_time_ms: totalTime,
        phase_timings: phaseTimings,
        code_validation_score: avgValidationScore,
        code_validation_iterations: totalValidationIterations,
        screens_generated: approvedDesigns.length,
        prd: prdResult.prd,
        approved_designs: approvedDesigns,
        zip_url: zipUrl,
        cost_breakdown: costBreakdown,
      };
    } catch (error) {
      console.error('\n❌ WORKFLOW FAILED:', error);

      if (projectId) {
        const supabase = getSupabaseService(this.supabaseConfig);
        await supabase.updateProject(projectId, {
          status: 'failed',
          metadata: { error: error.message },
        });
      }

      throw error;
    }
  }

  /**
   * Resume workflow after human approval (Concierge tier only)
   */
  async resumeAfterHumanApproval(
    projectId: string,
    approvedStitchDesigns: StitchDesign[]
  ): Promise<WorkflowResult> {
    console.log('\n🔄 RESUMING WORKFLOW after human approval...');

    // TODO: Implement continuation from Phase 4 (code generation)
    // This would:
    // 1. Convert Stitch HTML to Expo (universal React Native)
    // 2. Run agent-in-the-loop validation (code matches approved Stitch design)
    // 3. Package Expo project

    throw new Error('Not yet implemented - resumeAfterHumanApproval');
  }

  /**
   * Generate navigation code
   */
  private generateNavigationCode(designs: any[]): string {
    const screenImports = designs
      .map((d) => `import ${d.screen_name}Screen from '../screens/${d.screen_name}Screen';`)
      .join('\n');

    const screenConfigs = designs
      .map(
        (d) => `  {
    name: '${d.screen_name}',
    component: ${d.screen_name}Screen,
  }`
      )
      .join(',\n');

    return `import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

${screenImports}

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="${designs[0]?.screen_name || 'Home'}">
${screenConfigs}
      </Stack.Navigator>
    </NavigationContainer>
  );
}`;
  }

  /**
   * Generate package.json for Expo universal app (iOS, Android, Web)
   */
  private generatePackageJson(projectName: string): string {
    return JSON.stringify(
      {
        name: projectName.toLowerCase().replace(/\s+/g, '-'),
        version: '1.0.0',
        main: 'expo-router/entry',
        scripts: {
          start: 'expo start',
          android: 'expo start --android',
          ios: 'expo start --ios',
          web: 'expo start --web',
          test: 'jest',
          'test:e2e:ios': 'detox test --configuration ios.sim.debug',
          'test:e2e:android': 'detox test --configuration android.emu.debug',
          'test:e2e:web': 'playwright test',
          'build:ios': 'eas build --platform ios',
          'build:android': 'eas build --platform android',
          'build:web': 'expo export:web',
        },
        dependencies: {
          // Expo Framework - Universal (iOS, Android, Web)
          expo: '~50.0.0',
          'expo-router': '~3.4.0',
          'expo-status-bar': '~1.11.0',
          'expo-constants': '~15.4.0',

          // React
          react: '18.2.0',
          'react-native': '0.73.0',
          'react-dom': '18.2.0',
          'react-native-web': '~0.19.0',

          // Navigation
          '@react-navigation/native': '^6.1.0',
          '@react-navigation/native-stack': '^6.9.0',
          '@react-navigation/bottom-tabs': '^6.5.0',
          '@react-navigation/drawer': '^6.6.0',
          'react-native-screens': '~3.29.0',
          'react-native-safe-area-context': '4.8.2',

          // Platform-aware utilities
          '@expo/vector-icons': '^14.0.0',
        },
        devDependencies: {
          // TypeScript
          '@types/react': '~18.2.0',
          typescript: '^5.0.0',

          // Testing - Unit & Component
          jest: '^29.0.0',
          '@testing-library/react-native': '^12.0.0',
          '@testing-library/jest-native': '^5.4.0',

          // Testing - E2E
          detox: '^20.0.0',
          '@playwright/test': '^1.40.0',

          // Build
          '@babel/core': '^7.20.0',
        },
      },
      null,
      2
    );
  }
}

/**
 * Singleton instance
 */
let masterWorkflowInstance: MasterWorkflowService | null = null;

export function getMasterWorkflow(config?: MasterWorkflowConfig): MasterWorkflowService {
  if (!masterWorkflowInstance && !config) {
    throw new Error('Config required to initialize Master Workflow');
  }

  if (config && !masterWorkflowInstance) {
    masterWorkflowInstance = new MasterWorkflowService(config);
  }

  return masterWorkflowInstance!;
}

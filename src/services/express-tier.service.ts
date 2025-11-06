/**
 * Express Tier Service - Fully Automated Workflow
 *
 * Implements "agent in the loop" using Codex's multimodal capabilities
 * to replace human approval with automated visual validation.
 *
 * Workflow:
 * 1. User provides intake (app concept + inspiration websites)
 * 2. Gemini analyzes requirements and creates design system
 * 3. Codex generates designs with iterative visual validation
 * 4. Codex compares against benchmark screenshots
 * 5. Codex iterates until design quality is achieved
 * 6. Generate complete project (no human approval needed)
 *
 * This is the Express tier alternative to Concierge tier's Stitch workflow.
 */

import { ProjectIntake, ProblemDeconstruction, ScreenMapping } from '../types/project';
import { getGeminiService } from './gemini.service';
import { getCodexService } from './codex.service';
import { getPlaywrightService } from './playwright.service';
import { getSupabaseService } from './supabase.service';

interface ExpressTierResult {
  project_id: string;
  status: 'completed' | 'failed';
  screens_generated: number;
  total_iterations: number;
  average_quality_score: number;
  average_confidence: number;
  generation_time_ms: number;
  cost_breakdown: {
    gemini_cost: number;
    codex_cost: number;
    total_cost: number;
  };
  zip_url?: string;
  error?: string;
}

/**
 * Express Tier orchestrator - fully automated design-to-code
 */
export class ExpressTierService {
  private geminiApiKey: string;
  private codexApiKey: string;
  private supabaseConfig: any;

  constructor(config: {
    geminiApiKey: string;
    codexApiKey: string;
    supabaseConfig: any;
  }) {
    this.geminiApiKey = config.geminiApiKey;
    this.codexApiKey = config.codexApiKey;
    this.supabaseConfig = config.supabaseConfig;
  }

  /**
   * MAIN WORKFLOW: Fully automated Express tier
   * No human in the loop - agent validates everything
   */
  async executeExpressTierWorkflow(intake: ProjectIntake): Promise<ExpressTierResult> {
    const startTime = Date.now();
    let projectId: string | null = null;

    try {
      console.log('\n🚀 EXPRESS TIER: Starting fully automated workflow');
      console.log(`📱 App: ${intake.appName}`);
      console.log(`🎨 Inspiration sites: ${intake.inspirationWebsites.length}`);

      // Initialize services
      const gemini = getGeminiService(this.geminiApiKey);
      const codex = getCodexService(this.codexApiKey);
      const playwright = getPlaywrightService();
      const supabase = getSupabaseService(this.supabaseConfig);

      // ========================================================================
      // PHASE 1: Requirements Analysis (Gemini)
      // ========================================================================
      console.log('\n📊 PHASE 1: Analyzing requirements with Gemini...');

      // Capture inspiration screenshots
      const inspirationScreenshots = await Promise.all(
        intake.inspirationWebsites.map(async (site) => {
          console.log(`📸 Capturing screenshot: ${site.url}`);
          const screenshot = await supabase['captureWebsiteScreenshot'](site.url);
          return {
            url: site.url,
            screenshot,
            locked: site.locked,
          };
        })
      );

      // Analyze inspiration websites
      const inspirationAnalyses = await Promise.all(
        inspirationScreenshots.map(async (site) => {
          console.log(`🔍 Analyzing design: ${site.url}`);
          return await gemini.analyzeInspirationWebsite(
            site.screenshot,
            site.url,
            site.locked
          );
        })
      );

      // Generate problem deconstruction
      console.log('🧠 Generating problem deconstruction...');
      const problemDeconstruction = await gemini.generateProblemDeconstruction(
        intake,
        inspirationAnalyses
      );

      console.log(`✅ Generated:`);
      console.log(`   - ${problemDeconstruction.user_stories.length} user stories`);
      console.log(`   - ${problemDeconstruction.features.length} features`);
      console.log(`   - Complete design system`);

      // Generate screen mappings
      console.log('🗺️  Generating screen mappings...');
      const screenMappings = await gemini.generateScreenMappings({
        features: problemDeconstruction.features,
        user_stories: problemDeconstruction.user_stories,
        design_system: problemDeconstruction.design_system,
      });

      console.log(`✅ Mapped ${screenMappings.length} screens`);

      // Create project in database
      const project = await supabase.createProject({
        name: intake.appName,
        app_concept: intake.appConcept,
        service_tier: 'express',
        status: 'design_generation',
      });

      projectId = project.id;

      // ========================================================================
      // PHASE 2: Automated Design Generation (Codex + Agent-in-the-Loop)
      // ========================================================================
      console.log('\n🤖 PHASE 2: Automated design generation with Codex...');
      console.log('🔄 Agent will iterate until designs match benchmarks\n');

      // Generate all screens with iterative validation
      const designResults = await codex.generateAllScreensWithValidation(
        screenMappings as ScreenMapping[],
        problemDeconstruction.design_system,
        inspirationScreenshots,
        'react-native'
      );

      // Calculate statistics
      const totalIterations = designResults.reduce((sum, r) => sum + r.total_iterations, 0);
      const avgQualityScore =
        designResults.reduce((sum, r) => sum + r.final_score, 0) / designResults.length;
      const avgConfidence =
        designResults.reduce((sum, r) => sum + r.confidence, 0) / designResults.length;

      console.log('\n📊 GENERATION STATISTICS:');
      console.log(`   - Screens generated: ${designResults.length}`);
      console.log(`   - Total iterations: ${totalIterations}`);
      console.log(`   - Average quality score: ${avgQualityScore.toFixed(3)}`);
      console.log(`   - Average confidence: ${avgConfidence.toFixed(3)}`);

      // ========================================================================
      // PHASE 3: Quality Check & Warnings
      // ========================================================================
      console.log('\n🔍 PHASE 3: Quality check...');

      const lowQualityScreens = designResults.filter((r) => r.final_score < 0.75);
      if (lowQualityScreens.length > 0) {
        console.warn(
          `⚠️  Warning: ${lowQualityScreens.length} screens below quality threshold:`
        );
        lowQualityScreens.forEach((screen) => {
          console.warn(`   - ${screen.screen_name}: ${screen.final_score.toFixed(3)}`);
        });
      }

      const lowConfidenceScreens = designResults.filter((r) => r.confidence < 0.8);
      if (lowConfidenceScreens.length > 0) {
        console.warn(
          `⚠️  Warning: ${lowConfidenceScreens.length} screens with low confidence:`
        );
        lowConfidenceScreens.forEach((screen) => {
          console.warn(`   - ${screen.screen_name}: ${screen.confidence.toFixed(3)}`);
        });
      }

      // ========================================================================
      // PHASE 4: Code Artifact Generation
      // ========================================================================
      console.log('\n📦 PHASE 4: Generating code artifacts...');

      // Save all screen components
      for (const result of designResults) {
        await supabase.saveCodeArtifact({
          project_id: projectId,
          artifact_type: 'screen',
          file_path: `src/screens/${result.screen_name}Screen.tsx`,
          content: result.final_code,
          conversion_confidence: result.confidence,
          metadata: {
            iterations: result.total_iterations,
            quality_score: result.final_score,
          },
        });
      }

      // Generate navigation
      console.log('🧭 Generating navigation...');
      const navigationCode = this.generateNavigationCode(designResults);
      await supabase.saveCodeArtifact({
        project_id: projectId,
        artifact_type: 'navigation',
        file_path: 'src/navigation/AppNavigator.tsx',
        content: navigationCode,
      });

      // Generate theme file
      console.log('🎨 Generating theme...');
      const themeCode = JSON.stringify(problemDeconstruction.design_system, null, 2);
      await supabase.saveCodeArtifact({
        project_id: projectId,
        artifact_type: 'component',
        file_path: 'src/theme/index.ts',
        content: `export const theme = ${themeCode};`,
      });

      // Generate package.json
      console.log('📄 Generating package.json...');
      const packageJson = this.generatePackageJson(intake.appName);
      await supabase.saveCodeArtifact({
        project_id: projectId,
        artifact_type: 'full_project',
        file_path: 'package.json',
        content: packageJson,
      });

      // ========================================================================
      // PHASE 5: Project Packaging
      // ========================================================================
      console.log('\n📦 PHASE 5: Packaging project...');

      const zipUrl = await supabase.packageProjectAsZip(projectId);

      // Update project status
      await supabase.updateProject(projectId, {
        status: 'complete',
      });

      // ========================================================================
      // COMPLETE
      // ========================================================================
      const generationTime = Date.now() - startTime;

      console.log('\n✅ EXPRESS TIER WORKFLOW COMPLETE');
      console.log(`⏱️  Total time: ${(generationTime / 1000).toFixed(1)}s`);
      console.log(`📦 Download: ${zipUrl}`);

      // Cleanup
      await playwright.cleanup();

      return {
        project_id: projectId,
        status: 'completed',
        screens_generated: designResults.length,
        total_iterations: totalIterations,
        average_quality_score: avgQualityScore,
        average_confidence: avgConfidence,
        generation_time_ms: generationTime,
        cost_breakdown: {
          gemini_cost: 0.15, // TODO: Calculate from actual usage
          codex_cost: totalIterations * 0.05, // Estimate: $0.05 per iteration
          total_cost: 0.15 + totalIterations * 0.05,
        },
        zip_url: zipUrl,
      };
    } catch (error) {
      console.error('\n❌ EXPRESS TIER WORKFLOW FAILED:', error);

      if (projectId) {
        const supabase = getSupabaseService(this.supabaseConfig);
        await supabase.updateProject(projectId, {
          status: 'failed',
          metadata: { error: error.message },
        });
      }

      return {
        project_id: projectId || '',
        status: 'failed',
        screens_generated: 0,
        total_iterations: 0,
        average_quality_score: 0,
        average_confidence: 0,
        generation_time_ms: Date.now() - startTime,
        cost_breakdown: {
          gemini_cost: 0,
          codex_cost: 0,
          total_cost: 0,
        },
        error: error.message,
      };
    }
  }

  /**
   * Generate navigation code from design results
   */
  private generateNavigationCode(designResults: any[]): string {
    const screenImports = designResults
      .map(
        (r) => `import ${r.screen_name}Screen from '../screens/${r.screen_name}Screen';`
      )
      .join('\n');

    const screenConfigs = designResults
      .map(
        (r) => `  {
    name: '${r.screen_name}',
    component: ${r.screen_name}Screen,
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
      <Stack.Navigator
        initialRouteName="${designResults[0]?.screen_name || 'Home'}"
        screenOptions={{
          headerShown: true,
        }}
      >
${screenConfigs}
      </Stack.Navigator>
    </NavigationContainer>
  );
}`;
  }

  /**
   * Generate package.json
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
        },
        dependencies: {
          react: '^18.2.0',
          'react-native': '^0.73.0',
          expo: '^50.0.0',
          'expo-router': '^3.0.0',
          '@react-navigation/native': '^6.1.0',
          '@react-navigation/native-stack': '^6.9.0',
        },
        devDependencies: {
          '@types/react': '^18.2.0',
          '@types/react-native': '^0.72.0',
          typescript: '^5.0.0',
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
let expressTierServiceInstance: ExpressTierService | null = null;

export function getExpressTierService(config?: {
  geminiApiKey: string;
  codexApiKey: string;
  supabaseConfig: any;
}): ExpressTierService {
  if (!expressTierServiceInstance && !config) {
    throw new Error('Config required to initialize Express Tier service');
  }

  if (config && !expressTierServiceInstance) {
    expressTierServiceInstance = new ExpressTierService(config);
  }

  return expressTierServiceInstance!;
}

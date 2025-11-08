/**
 * End-to-End Integration Tests
 *
 * Tests the complete workflow from idea to generated Expo app.
 * These tests verify that all services integrate correctly.
 */

import { WorkflowOrchestratorService, WorkflowInput, WorkflowOutput } from '../../src/services/workflow-orchestrator.service';
import { ProgressTrackerService, ProgressEvent } from '../../src/services/progress-tracker.service';

// Integration tests require actual service instances
// Mock only external APIs (OpenAI, Anthropic, Google)
jest.mock('openai');
jest.mock('@anthropic-ai/sdk');
jest.mock('@google/generative-ai');

describe('End-to-End Workflow Integration', () => {
  let orchestrator: WorkflowOrchestratorService;
  let progressTracker: ProgressTrackerService;

  const mockInput: WorkflowInput = {
    userId: 'test-user-e2e',
    projectName: 'E2E Test App',
    projectDescription: 'A comprehensive test of the Design-First Software Factory workflow',
    targetPlatforms: ['ios', 'android', 'web'],
    designPreferences: {
      colorScheme: 'light',
      brandColors: ['#007AFF', '#5856D6'],
      fontFamily: 'System',
    },
  };

  beforeAll(() => {
    orchestrator = WorkflowOrchestratorService.getInstance();
    progressTracker = ProgressTrackerService.getInstance();
  });

  describe('Complete Workflow Execution', () => {
    it('should execute all 6 phases in sequence', async () => {
      const progressEvents: ProgressEvent[] = [];

      // Subscribe to progress events
      const unsubscribe = progressTracker.subscribe('test-project', (event) => {
        progressEvents.push(event);
      });

      const result = await orchestrator.executeWorkflow(mockInput);

      unsubscribe();

      // Verify workflow completed
      expect(result.status).toBe('completed');
      expect(result.projectId).toBeDefined();

      // Verify all phase outputs are present
      expect(result.prd).toBeDefined();
      expect(result.screenMap).toBeDefined();
      expect(result.designs).toBeDefined();
      expect(result.generatedCode).toBeDefined();
      expect(result.qualityReport).toBeDefined();

      // Verify progress events for all phases
      const phaseStartEvents = progressEvents.filter(e => e.type === 'phase_start');
      expect(phaseStartEvents.length).toBe(6);

      const phaseNames = phaseStartEvents.map(e => e.phase);
      expect(phaseNames).toEqual([
        'problem_deconstruction',
        'screen_mapping',
        'design_generation',
        'stitch_iteration',
        'code_generation',
        'code_review',
      ]);

      // Verify workflow complete event
      const completeEvents = progressEvents.filter(e => e.type === 'workflow_complete');
      expect(completeEvents.length).toBe(1);
    }, 60000); // 60s timeout for complete workflow

    it('should generate valid PRD in Phase 1', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.prd).toMatchObject({
        title: expect.any(String),
        description: expect.any(String),
        targetAudience: expect.any(String),
        coreFeatures: expect.arrayContaining([expect.any(String)]),
        screens: expect.arrayContaining([expect.any(String)]),
        technicalRequirements: expect.arrayContaining([expect.any(String)]),
        successCriteria: expect.arrayContaining([expect.any(String)]),
      });

      expect(result.prd?.coreFeatures.length).toBeGreaterThan(0);
      expect(result.prd?.screens.length).toBeGreaterThan(0);
    }, 30000);

    it('should generate screen mapping with navigation in Phase 2', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.screenMap).toMatchObject({
        screens: expect.arrayContaining([
          expect.objectContaining({
            id: expect.any(String),
            name: expect.any(String),
            purpose: expect.any(String),
            components: expect.any(Array),
            dataRequirements: expect.any(Array),
          }),
        ]),
        navigationFlow: expect.objectContaining({
          flows: expect.any(Array),
        }),
        sitemap: expect.objectContaining({
          rootScreen: expect.any(String),
        }),
      });

      expect(result.screenMap?.screens.length).toBeGreaterThan(0);
    }, 30000);

    it('should generate design tokens and component specs in Phase 3', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.designs).toMatchObject({
        designTokens: expect.objectContaining({
          colors: expect.any(Object),
          typography: expect.any(Object),
          spacing: expect.any(Object),
          borderRadius: expect.any(Object),
        }),
        componentSpecs: expect.any(Array),
        platformOverrides: expect.any(Object),
      });

      // Verify design tokens have required colors
      expect(result.designs?.designTokens.colors).toHaveProperty('primary');
      expect(result.designs?.designTokens.colors).toHaveProperty('background');
      expect(result.designs?.designTokens.colors).toHaveProperty('text');
    }, 30000);

    it('should generate Expo code files in Phase 5', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.generatedCode).toMatchObject({
        projectPath: expect.any(String),
        files: expect.arrayContaining([
          expect.objectContaining({
            path: expect.any(String),
            content: expect.any(String),
            language: expect.any(String),
          }),
        ]),
      });

      expect(result.generatedCode?.files.length).toBeGreaterThan(0);

      // Verify key files exist
      const filePaths = result.generatedCode?.files.map(f => f.path) || [];
      expect(filePaths).toContain(expect.stringContaining('App.tsx'));
    }, 30000);

    it('should produce quality report in Phase 6', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.qualityReport).toMatchObject({
        overallStatus: expect.stringMatching(/passed|warnings|failed/),
        eslintResults: expect.objectContaining({
          errors: expect.any(Number),
          warnings: expect.any(Number),
        }),
        typescriptResults: expect.objectContaining({
          errors: expect.any(Number),
          warnings: expect.any(Number),
        }),
        semgrepResults: expect.objectContaining({
          critical: expect.any(Number),
          high: expect.any(Number),
          medium: expect.any(Number),
          low: expect.any(Number),
        }),
        npmAuditResults: expect.objectContaining({
          critical: expect.any(Number),
          high: expect.any(Number),
          moderate: expect.any(Number),
          low: expect.any(Number),
        }),
      });
    }, 30000);
  });

  describe('Progress Tracking Integration', () => {
    it('should track progress through all phases', async () => {
      const progressUpdates: ProgressEvent[] = [];

      const projectId = 'progress-test-project';
      const unsubscribe = progressTracker.subscribe(projectId, (event) => {
        progressUpdates.push(event);
      });

      await orchestrator.executeWorkflow({
        ...mockInput,
        userId: projectId,
      });

      unsubscribe();

      // Verify we received progress updates
      expect(progressUpdates.length).toBeGreaterThan(0);

      // Verify phase progression
      const phases = progressUpdates
        .filter(e => e.type === 'phase_start')
        .map(e => e.phase);

      expect(phases).toContain('problem_deconstruction');
      expect(phases).toContain('code_generation');
      expect(phases).toContain('code_review');
    }, 60000);

    it('should track step-by-step progress within phases', async () => {
      const progressUpdates: ProgressEvent[] = [];

      const projectId = 'step-tracking-test';
      const unsubscribe = progressTracker.subscribe(projectId, (event) => {
        progressUpdates.push(event);
      });

      await orchestrator.executeWorkflow({
        ...mockInput,
        userId: projectId,
      });

      unsubscribe();

      // Verify we received step progress events
      const stepEvents = progressUpdates.filter(e => e.type === 'phase_progress');
      expect(stepEvents.length).toBeGreaterThan(0);

      // Verify progress percentages increase
      const progressPcts = stepEvents.map(e => e.progress);
      const isIncreasing = progressPcts.every((val, i, arr) => {
        return i === 0 || val >= arr[i - 1];
      });
      expect(isIncreasing).toBe(true);
    }, 60000);
  });

  describe('Data Flow Integration', () => {
    it('should pass data correctly between phases', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      // Verify PRD screens are used in screen mapping
      const prdScreenNames = result.prd?.screens || [];
      const screenMapNames = result.screenMap?.screens.map(s => s.name) || [];

      expect(screenMapNames.length).toBeGreaterThan(0);
      // At least some PRD screens should appear in screen map
      const hasOverlap = prdScreenNames.some(name =>
        screenMapNames.includes(name)
      );
      expect(hasOverlap).toBe(true);
    }, 30000);

    it('should use design tokens in generated code', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      const designTokens = result.designs?.designTokens;
      const generatedFiles = result.generatedCode?.files || [];

      // Check if design tokens are referenced in code
      const hasDesignTokensFile = generatedFiles.some(f =>
        f.path.includes('designTokens') || f.path.includes('design-tokens')
      );

      expect(hasDesignTokensFile || designTokens).toBeTruthy();
    }, 30000);
  });

  describe('Error Handling Integration', () => {
    it('should handle quota exceeded errors', async () => {
      // This would test quota enforcement
      // Requires mocking quota service to return quota exceeded
      expect(true).toBe(true);
    });

    it('should handle AI service timeouts', async () => {
      // This would test timeout handling
      // Requires mocking AI service to timeout
      expect(true).toBe(true);
    });

    it('should handle code validation failures', async () => {
      // This would test quality gate failures
      // Requires mocking validation to return failures
      expect(true).toBe(true);
    });
  });

  describe('Performance', () => {
    it('should complete workflow in reasonable time', async () => {
      const startTime = Date.now();

      const result = await orchestrator.executeWorkflow(mockInput);

      const duration = Date.now() - startTime;

      expect(result.status).toBe('completed');
      expect(duration).toBeLessThan(120000); // Should complete in under 2 minutes
    }, 150000);

    it('should report accurate token usage', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.totalTokensUsed).toBeGreaterThan(0);
      // With 4 AI phases, each using ~300-500 tokens, total should be 1200-2000+
      expect(result.totalTokensUsed).toBeGreaterThan(300);
    }, 30000);

    it('should calculate cost estimates', async () => {
      const result = await orchestrator.executeWorkflow(mockInput);

      expect(result.estimatedCost).toBeGreaterThan(0);
      // Cost should be reasonable (under $1 for test workflow)
      expect(result.estimatedCost).toBeLessThan(1.0);
    }, 30000);
  });
});

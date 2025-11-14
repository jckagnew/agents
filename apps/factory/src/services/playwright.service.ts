/**
 * Playwright Service - Automated Browser Testing & Screenshot Capture
 *
 * Provides the "eyes" for the agent-in-the-loop workflow.
 * Renders generated components and captures screenshots for comparison.
 *
 * This implements the key capability from the Codex video:
 * "The model can check its own work visually"
 */

import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

interface ScreenshotOptions {
  width?: number;
  height?: number;
  deviceScaleFactor?: number;
  fullPage?: boolean;
  darkMode?: boolean;
}

interface RenderResult {
  screenshot: string; // Base64
  url: string;
  renderTime: number;
  errors: string[];
}

/**
 * Playwright service for rendering and capturing screenshots
 * Works with both React Native (via Expo web) and regular React
 */
export class PlaywrightService {
  private tempDir: string;
  private devServerPort: number;

  constructor() {
    this.tempDir = join(tmpdir(), 'design-first-software-factory');
    this.devServerPort = 3000;

    // Ensure temp directory exists
    try {
      mkdirSync(this.tempDir, { recursive: true });
    } catch (error) {
      // Directory might already exist
    }
  }

  /**
   * Render component and capture screenshot
   * This is the core "check your own work" capability
   */
  async renderComponentAndCapture(
    componentCode: string,
    componentName: string,
    framework: 'react-native' | 'react' = 'react-native',
    options: ScreenshotOptions = {}
  ): Promise<RenderResult> {
    const startTime = Date.now();
    const errors: string[] = [];

    try {
      // STEP 1: Write component to temp file
      const projectDir = await this.createTempProject(componentCode, componentName, framework);

      // STEP 2: Start dev server
      const devServer = await this.startDevServer(projectDir, framework);

      // STEP 3: Wait for server to be ready
      await this.waitForServer(`http://localhost:${this.devServerPort}`, 30000);

      // STEP 4: Capture screenshot using Playwright
      const screenshot = await this.captureScreenshotWithPlaywright(
        `http://localhost:${this.devServerPort}`,
        options
      );

      // STEP 5: Stop dev server
      await this.stopDevServer(devServer);

      const renderTime = Date.now() - startTime;

      return {
        screenshot,
        url: `http://localhost:${this.devServerPort}`,
        renderTime,
        errors,
      };
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      errors.push(errorMessage);
      throw new Error(`Failed to render component: ${errorMessage}`);
    }
  }

  /**
   * Capture multiple screenshots at different sizes/modes
   * As mentioned in the video: "check light mode, dark mode, responsive, different sizes"
   */
  async captureMultipleVariations(
    componentCode: string,
    componentName: string,
    framework: 'react-native' | 'react' = 'react-native'
  ): Promise<{
    desktop: RenderResult;
    mobile: RenderResult;
    tablet: RenderResult;
    darkMode?: RenderResult;
  }> {
    // Desktop view
    const desktop = await this.renderComponentAndCapture(componentCode, componentName, framework, {
      width: 1920,
      height: 1080,
      deviceScaleFactor: 1,
    });

    // Mobile view
    const mobile = await this.renderComponentAndCapture(componentCode, componentName, framework, {
      width: 375,
      height: 812,
      deviceScaleFactor: 3, // iPhone X/11/12 scale
    });

    // Tablet view
    const tablet = await this.renderComponentAndCapture(componentCode, componentName, framework, {
      width: 768,
      height: 1024,
      deviceScaleFactor: 2, // iPad scale
    });

    // Dark mode (optional)
    const darkMode = await this.renderComponentAndCapture(componentCode, componentName, framework, {
      width: 1920,
      height: 1080,
      darkMode: true,
    });

    return { desktop, mobile, tablet, darkMode };
  }

  /**
   * Create temporary project with component
   */
  private async createTempProject(
    componentCode: string,
    componentName: string,
    framework: 'react-native' | 'react'
  ): Promise<string> {
    const projectName = `temp-${Date.now()}`;
    const projectDir = join(this.tempDir, projectName);

    mkdirSync(projectDir, { recursive: true });

    if (framework === 'react-native') {
      // Create minimal Expo project
      await this.createExpoProject(projectDir, componentCode, componentName);
    } else {
      // Create minimal Vite React project
      await this.createViteProject(projectDir, componentCode, componentName);
    }

    return projectDir;
  }

  /**
   * Create minimal Expo project for React Native component
   */
  private async createExpoProject(
    projectDir: string,
    componentCode: string,
    componentName: string
  ): Promise<void> {
    // package.json
    const packageJson = {
      name: 'temp-expo-project',
      version: '1.0.0',
      main: 'node_modules/expo/AppEntry.js',
      scripts: {
        start: 'expo start --web',
        web: 'expo start --web',
      },
      dependencies: {
        expo: '^50.0.0',
        react: '^18.2.0',
        'react-native': '^0.73.0',
        'react-native-web': '^0.19.0',
      },
    };

    writeFileSync(join(projectDir, 'package.json'), JSON.stringify(packageJson, null, 2));

    // App.tsx - renders the component
    const appCode = `import React from 'react';
import { View } from 'react-native';
import ${componentName} from './src/${componentName}';

export default function App() {
  return (
    <View style={{ flex: 1 }}>
      <${componentName} />
    </View>
  );
}`;

    writeFileSync(join(projectDir, 'App.tsx'), appCode);

    // Component file
    mkdirSync(join(projectDir, 'src'), { recursive: true });
    writeFileSync(join(projectDir, `src/${componentName}.tsx`), componentCode);

    // app.json
    const appJson = {
      expo: {
        name: 'temp-expo-project',
        slug: 'temp-expo-project',
        version: '1.0.0',
        platforms: ['web'],
        web: {
          bundler: 'metro',
        },
      },
    };

    writeFileSync(join(projectDir, 'app.json'), JSON.stringify(appJson, null, 2));
  }

  /**
   * Create minimal Vite project for React component
   */
  private async createViteProject(
    projectDir: string,
    componentCode: string,
    componentName: string
  ): Promise<void> {
    // package.json
    const packageJson = {
      name: 'temp-vite-project',
      version: '1.0.0',
      type: 'module',
      scripts: {
        dev: 'vite --port 3000',
        build: 'vite build',
      },
      dependencies: {
        react: '^18.2.0',
        'react-dom': '^18.2.0',
      },
      devDependencies: {
        '@vitejs/plugin-react': '^4.2.0',
        vite: '^5.0.0',
        typescript: '^5.0.0',
      },
    };

    writeFileSync(join(projectDir, 'package.json'), JSON.stringify(packageJson, null, 2));

    // index.html
    const indexHtml = `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Component Preview</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>`;

    writeFileSync(join(projectDir, 'index.html'), indexHtml);

    // vite.config.ts
    const viteConfig = `import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
  },
});`;

    writeFileSync(join(projectDir, 'vite.config.ts'), viteConfig);

    // src/main.tsx
    mkdirSync(join(projectDir, 'src'), { recursive: true });
    const mainCode = `import React from 'react';
import ReactDOM from 'react-dom/client';
import ${componentName} from './${componentName}';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <${componentName} />
  </React.StrictMode>
);`;

    writeFileSync(join(projectDir, 'src/main.tsx'), mainCode);

    // Component file
    writeFileSync(join(projectDir, `src/${componentName}.tsx`), componentCode);
  }

  /**
   * Start dev server (Expo or Vite)
   */
  private async startDevServer(
    projectDir: string,
    framework: 'react-native' | 'react'
  ): Promise<any> {
    // Import dynamically to avoid bundling issues
    const { spawn } = await import('child_process');

    // Install dependencies first
    console.log('📦 Installing dependencies...');
    await this.runCommand(projectDir, 'npm', ['install']);

    // Start dev server
    console.log('🚀 Starting dev server...');
    const command = framework === 'react-native' ? 'npm' : 'npm';
    const args = framework === 'react-native' ? ['run', 'web'] : ['run', 'dev'];

    const devServer = spawn(command, args, {
      cwd: projectDir,
      stdio: 'pipe',
    });

    // Capture errors
    devServer.stderr?.on('data', (data) => {
      console.error(`Dev server error: ${data}`);
    });

    return devServer;
  }

  /**
   * Stop dev server
   */
  private async stopDevServer(devServer: any): Promise<void> {
    devServer.kill();
  }

  /**
   * Wait for server to be ready
   */
  private async waitForServer(url: string, timeout: number): Promise<void> {
    const startTime = Date.now();

    while (Date.now() - startTime < timeout) {
      try {
        const response = await fetch(url);
        if (response.ok) {
          console.log('✅ Server ready');
          return;
        }
      } catch (error) {
        // Server not ready yet
      }

      await new Promise((resolve) => setTimeout(resolve, 500));
    }

    throw new Error('Server failed to start within timeout');
  }

  /**
   * Capture screenshot using Playwright
   * This is where the magic happens - the agent "sees" its own work
   */
  private async captureScreenshotWithPlaywright(
    url: string,
    options: ScreenshotOptions
  ): Promise<string> {
    // Import Playwright dynamically
    // @ts-expect-error - playwright is a runtime dependency that may not be available at compile time
    const playwright = await import('playwright');

    const browser = await playwright.chromium.launch({
      headless: true,
    });

    const context = await browser.newContext({
      viewport: {
        width: options.width || 1280,
        height: options.height || 720,
      },
      deviceScaleFactor: options.deviceScaleFactor || 1,
      colorScheme: options.darkMode ? 'dark' : 'light',
    });

    const page = await context.newPage();

    try {
      // Navigate to component
      await page.goto(url, {
        waitUntil: 'networkidle',
        timeout: 30000,
      });

      // Wait for React to render
      await page.waitForTimeout(1000);

      // Capture screenshot
      const screenshot = await page.screenshot({
        fullPage: options.fullPage || false,
        type: 'png',
      });

      await browser.close();

      // Convert to base64
      return screenshot.toString('base64');
    } catch (error) {
      await browser.close();
      throw error;
    }
  }

  /**
   * Run command and wait for completion
   */
  private async runCommand(
    cwd: string,
    command: string,
    args: string[]
  ): Promise<{ stdout: string; stderr: string }> {
    const { spawn } = await import('child_process');

    return new Promise((resolve, reject) => {
      const proc = spawn(command, args, { cwd });
      let stdout = '';
      let stderr = '';

      proc.stdout?.on('data', (data) => {
        stdout += data.toString();
      });

      proc.stderr?.on('data', (data) => {
        stderr += data.toString();
      });

      proc.on('close', (code) => {
        if (code === 0) {
          resolve({ stdout, stderr });
        } else {
          reject(new Error(`Command failed with code ${code}: ${stderr}`));
        }
      });
    });
  }

  /**
   * Cleanup temporary projects
   */
  async cleanup(): Promise<void> {
    const { rm } = await import('fs/promises');
    try {
      await rm(this.tempDir, { recursive: true, force: true });
    } catch (error) {
      console.error('Failed to cleanup temp directory:', error);
    }
  }
}

/**
 * Singleton instance
 */
let playwrightServiceInstance: PlaywrightService | null = null;

export function getPlaywrightService(): PlaywrightService {
  if (!playwrightServiceInstance) {
    playwrightServiceInstance = new PlaywrightService();
  }

  return playwrightServiceInstance;
}

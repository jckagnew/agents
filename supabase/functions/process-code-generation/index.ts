/**
 * Supabase Edge Function: Process Code Generation
 *
 * Background worker for generating full Expo projects from approved Stitch designs
 * Converts all approved HTML designs to React Native and packages them into a complete project
 *
 * Deploy with: supabase functions deploy process-code-generation
 */

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

interface CodeGenerationRequest {
  job_id: string;
}

/**
 * Main handler
 */
serve(async (req) => {
  try {
    // CORS headers
    if (req.method === 'OPTIONS') {
      return new Response('ok', {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
        },
      });
    }

    const { job_id }: CodeGenerationRequest = await req.json();

    if (!job_id) {
      return new Response(
        JSON.stringify({ error: 'job_id is required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Initialize Supabase client (service role for background jobs)
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    // Get the job
    const { data: job, error: jobError } = await supabaseClient
      .from('code_generation_jobs')
      .select('*')
      .eq('id', job_id)
      .single();

    if (jobError) {
      throw new Error(`Failed to fetch job: ${jobError.message}`);
    }

    // Update job status to processing
    await supabaseClient
      .from('code_generation_jobs')
      .update({ status: 'processing', started_at: new Date().toISOString() })
      .eq('id', job_id);

    try {
      // Get all approved Stitch designs for this project
      const { data: designs, error: designsError } = await supabaseClient
        .from('stitch_designs')
        .select('*, screen_mappings(*)')
        .eq('project_id', job.project_id)
        .eq('approved', true);

      if (designsError) {
        throw new Error(`Failed to fetch designs: ${designsError.message}`);
      }

      if (!designs || designs.length === 0) {
        throw new Error('No approved designs found');
      }

      // Get project details
      const { data: project } = await supabaseClient
        .from('projects')
        .select('*')
        .eq('id', job.project_id)
        .single();

      // Get problem deconstruction for design system
      const { data: deconstruction } = await supabaseClient
        .from('problem_deconstructions')
        .select('*')
        .eq('project_id', job.project_id)
        .single();

      // Convert each design to React Native
      const convertedScreens = [];
      for (const design of designs) {
        const conversionResult = await convertDesignToReactNative(
          design,
          deconstruction.design_system
        );

        // Save artifact
        await supabaseClient.from('code_artifacts').insert({
          project_id: job.project_id,
          code_generation_job_id: job_id,
          artifact_type: 'screen',
          file_path: `src/screens/${design.screen_name}Screen.tsx`,
          content: conversionResult.component_code,
          conversion_confidence: conversionResult.confidence,
          warnings: conversionResult.warnings,
        });

        convertedScreens.push(conversionResult);
      }

      // Generate navigation structure
      const navigationCode = await generateNavigation(
        designs,
        deconstruction.design_system
      );

      await supabaseClient.from('code_artifacts').insert({
        project_id: job.project_id,
        code_generation_job_id: job_id,
        artifact_type: 'navigation',
        file_path: 'src/navigation/AppNavigator.tsx',
        content: navigationCode,
      });

      // Generate theme file
      const themeCode = generateThemeFile(deconstruction.design_system);

      await supabaseClient.from('code_artifacts').insert({
        project_id: job.project_id,
        code_generation_job_id: job_id,
        artifact_type: 'component',
        file_path: 'src/theme/index.ts',
        content: themeCode,
      });

      // Generate package.json
      const packageJson = generatePackageJson(project.name, convertedScreens);

      await supabaseClient.from('code_artifacts').insert({
        project_id: job.project_id,
        code_generation_job_id: job_id,
        artifact_type: 'full_project',
        file_path: 'package.json',
        content: packageJson,
      });

      // Package all artifacts into a ZIP file
      const zipUrl = await packageProjectAsZip(job.project_id, job_id, supabaseClient);

      // Update job status to completed
      await supabaseClient
        .from('code_generation_jobs')
        .update({
          status: 'completed',
          completed_at: new Date().toISOString(),
          output_data: {
            screen_count: designs.length,
            zip_url: zipUrl,
            warnings: convertedScreens.flatMap((s) => s.warnings),
          },
        })
        .eq('id', job_id);

      // Update project status
      await supabaseClient
        .from('projects')
        .update({ status: 'complete' })
        .eq('id', job.project_id);

      // TODO: Send notification to user
      // await notifyUser(project.user_id, 'project_complete', { project_id: job.project_id });

      return new Response(
        JSON.stringify({
          success: true,
          job_id,
          screen_count: designs.length,
          zip_url: zipUrl,
        }),
        {
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
          },
        }
      );
    } catch (error) {
      console.error('Code generation error:', error);

      // Update job status to failed
      await supabaseClient
        .from('code_generation_jobs')
        .update({
          status: 'failed',
          error_message: error.message,
          completed_at: new Date().toISOString(),
        })
        .eq('id', job_id);

      // Update project status
      await supabaseClient
        .from('projects')
        .update({ status: 'failed' })
        .eq('id', job.project_id);

      throw error;
    }
  } catch (error) {
    console.error('Process error:', error);
    return new Response(
      JSON.stringify({
        error: error.message || 'Internal server error',
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  }
});

/**
 * Convert a single design to React Native
 */
async function convertDesignToReactNative(design: any, designSystem: any): Promise<any> {
  const anthropicApiKey = Deno.env.get('ANTHROPIC_API_KEY');

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': anthropicApiKey!,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 16000,
      messages: [
        {
          role: 'user',
          content: `Convert this Stitch HTML to React Native TypeScript component.

Screen: ${design.screen_name}
Design System: ${JSON.stringify(designSystem, null, 2)}

HTML:
${design.html_content}

Return JSON: {"component_code": "...", "dependencies": [], "warnings": [], "confidence": 0.9}`,
        },
      ],
    }),
  });

  const result = await response.json();
  const content = result.content[0].text;
  const jsonMatch = content.match(/\{[\s\S]*\}/);

  return JSON.parse(jsonMatch![0]);
}

/**
 * Generate navigation structure
 */
async function generateNavigation(designs: any[], designSystem: any): Promise<string> {
  // Simple navigation generation
  // In production, use Claude to generate sophisticated navigation

  const screenImports = designs
    .map(
      (d) =>
        `import ${d.screen_name}Screen from '../screens/${d.screen_name}Screen';`
    )
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
      <Stack.Navigator>
${screenConfigs}
      </Stack.Navigator>
    </NavigationContainer>
  );
}`;
}

/**
 * Generate theme file from design system
 */
function generateThemeFile(designSystem: any): string {
  return `export const theme = ${JSON.stringify(designSystem, null, 2)};`;
}

/**
 * Generate package.json
 */
function generatePackageJson(projectName: string, screens: any[]): string {
  const dependencies = new Set([
    'react',
    'react-native',
    'expo',
    'expo-router',
    '@react-navigation/native',
    '@react-navigation/native-stack',
  ]);

  screens.forEach((screen) => {
    screen.dependencies?.forEach((dep: string) => dependencies.add(dep));
  });

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
      dependencies: Object.fromEntries(
        Array.from(dependencies).map((dep) => [dep, 'latest'])
      ),
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

/**
 * Package all artifacts as a ZIP file
 */
async function packageProjectAsZip(
  projectId: string,
  jobId: string,
  supabase: any
): Promise<string> {
  // Get all artifacts
  const { data: artifacts } = await supabase
    .from('code_artifacts')
    .select('*')
    .eq('code_generation_job_id', jobId);

  // In production, use a ZIP library like JSZip
  // For now, return a placeholder URL
  const zipFileName = `${projectId}/generated-project.zip`;

  // TODO: Create actual ZIP file and upload to storage
  // const zip = new JSZip();
  // artifacts.forEach(artifact => {
  //   zip.file(artifact.file_path, artifact.content);
  // });
  // const zipBlob = await zip.generateAsync({ type: 'blob' });
  // await supabase.storage.from('projects').upload(zipFileName, zipBlob);

  const { data } = supabase.storage.from('projects').getPublicUrl(zipFileName);

  return data.publicUrl;
}

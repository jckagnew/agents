/**
 * Supabase Edge Function: Convert HTML to React Native
 *
 * This function converts Stitch HTML exports to React Native code
 * Uses Claude or GPT-4 for intelligent conversion
 *
 * Deploy with: supabase functions deploy convert-html-to-react-native
 */

import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

interface ConversionRequest {
  design_id: string;
  target_framework?: 'react-native' | 'expo';
}

interface ConversionResponse {
  component_code: string;
  style_code: string;
  dependencies: string[];
  warnings: string[];
  confidence: number;
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

    // Parse request
    const { design_id, target_framework = 'expo' }: ConversionRequest = await req.json();

    if (!design_id) {
      return new Response(
        JSON.stringify({ error: 'design_id is required' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Initialize Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: { Authorization: req.headers.get('Authorization')! },
        },
      }
    );

    // Get the Stitch design from database
    const { data: design, error: designError } = await supabaseClient
      .from('stitch_designs')
      .select('*')
      .eq('id', design_id)
      .single();

    if (designError) {
      throw new Error(`Failed to fetch design: ${designError.message}`);
    }

    // Get the design system from problem deconstruction
    const { data: screenMapping } = await supabaseClient
      .from('screen_mappings')
      .select('problem_deconstruction_id')
      .eq('id', design.screen_mapping_id)
      .single();

    const { data: deconstruction } = await supabaseClient
      .from('problem_deconstructions')
      .select('design_system')
      .eq('id', screenMapping?.problem_deconstruction_id)
      .single();

    // Convert HTML to React Native using AI
    const conversionResult = await convertHtmlToReactNative(
      design.html_content,
      design.screen_name,
      deconstruction?.design_system,
      target_framework
    );

    // Save the generated code
    const { data: artifact, error: artifactError } = await supabaseClient
      .from('code_artifacts')
      .insert({
        project_id: design.project_id,
        artifact_type: 'component',
        file_path: `src/screens/${design.screen_name}Screen.tsx`,
        content: conversionResult.component_code,
        conversion_confidence: conversionResult.confidence,
        warnings: conversionResult.warnings,
      })
      .select()
      .single();

    if (artifactError) {
      console.error('Failed to save artifact:', artifactError);
    }

    return new Response(
      JSON.stringify({
        success: true,
        artifact_id: artifact?.id,
        ...conversionResult,
      }),
      {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      }
    );
  } catch (error) {
    console.error('Conversion error:', error);
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
 * Convert HTML to React Native using Claude
 */
async function convertHtmlToReactNative(
  html: string,
  screenName: string,
  designSystem: any,
  targetFramework: string
): Promise<ConversionResponse> {
  const anthropicApiKey = Deno.env.get('ANTHROPIC_API_KEY');

  if (!anthropicApiKey) {
    throw new Error('ANTHROPIC_API_KEY not configured');
  }

  const prompt = `You are an expert React Native developer. Convert the following Stitch HTML export to a high-quality ${targetFramework} component.

**Screen Name:** ${screenName}

**Design System:**
${JSON.stringify(designSystem, null, 2)}

**Stitch HTML:**
\`\`\`html
${html}
\`\`\`

**Requirements:**
1. Create a TypeScript React Native component using functional components and hooks
2. Use StyleSheet.create() for all styles
3. Follow the design system colors, typography, and spacing exactly
4. Preserve the visual hierarchy and layout from the HTML
5. Use appropriate React Native components (View, Text, ScrollView, TouchableOpacity, etc.)
6. Make the component responsive and platform-aware
7. Add TypeScript types for all props
8. Include accessibility props (accessibilityLabel, accessibilityRole, etc.)
9. Handle interactive elements (buttons, inputs) with proper state management
10. List any warnings or limitations in the conversion

**Output Format:**
Return a JSON object with:
{
  "component_code": "// Full TypeScript component code",
  "style_code": "// StyleSheet styles (if separate file preferred)",
  "dependencies": ["dependency1", "dependency2"],
  "warnings": ["warning1", "warning2"],
  "confidence": 0.95 // 0.0 to 1.0
}

IMPORTANT: Return ONLY the JSON object, no other text.`;

  const response = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': anthropicApiKey,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 16000,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Claude API error: ${response.status} ${errorText}`);
  }

  const result = await response.json();
  const content = result.content[0].text;

  // Parse JSON from response
  const jsonMatch = content.match(/\{[\s\S]*\}/);
  if (!jsonMatch) {
    throw new Error('Failed to parse conversion result from Claude');
  }

  return JSON.parse(jsonMatch[0]);
}

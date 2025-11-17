import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseServiceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    
    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    const { report, marketConfig, marketInsights } = await req.json();

    if (!report || !marketConfig) {
      return new Response(
        JSON.stringify({ error: 'Missing required fields: report, marketConfig' }),
        {
          status: 400,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    // Extract executive summary from report (first paragraph or section)
    const executiveSummary = report.split('\n\n')[0] || report.substring(0, 500);

    // Insert main report
    const { data: reportData, error: reportError } = await supabase
      .from('market_research_reports')
      .insert({
        report_date: new Date().toISOString().split('T')[0],
        executive_summary: executiveSummary,
        full_report: report,
        market_count: marketConfig.markets?.length || 0,
        market_config: marketConfig,
      })
      .select()
      .single();

    if (reportError) {
      // If duplicate date, update instead
      if (reportError.code === '23505') {
        const { data: updatedData, error: updateError } = await supabase
          .from('market_research_reports')
          .update({
            executive_summary: executiveSummary,
            full_report: report,
            market_count: marketConfig.markets?.length || 0,
            market_config: marketConfig,
            updated_at: new Date().toISOString(),
          })
          .eq('report_date', new Date().toISOString().split('T')[0])
          .select()
          .single();

        if (updateError) {
          throw updateError;
        }

        // Delete old insights and insert new ones
        if (marketInsights && marketInsights.length > 0) {
          await supabase
            .from('market_insights')
            .delete()
            .eq('report_id', updatedData.id);

          const insightsToInsert = marketInsights.map((insight: any) => ({
            report_id: updatedData.id,
            market_id: insight.market_id,
            market_name: insight.market_name,
            sentiment_analysis: insight.sentiment_analysis,
            key_trends: insight.key_trends || [],
            opportunities: insight.opportunities || [],
            threats: insight.threats || [],
            competitor_activity: insight.competitor_activity,
            search_keywords: insight.search_keywords || [],
            competitors_tracked: insight.competitors_tracked || [],
          }));

          await supabase.from('market_insights').insert(insightsToInsert);
        }

        return new Response(
          JSON.stringify({ 
            success: true, 
            report_id: updatedData.id,
            message: 'Report updated successfully' 
          }),
          {
            status: 200,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          }
        );
      }
      throw reportError;
    }

    // Insert market insights if provided
    if (marketInsights && marketInsights.length > 0 && reportData) {
      const insightsToInsert = marketInsights.map((insight: any) => ({
        report_id: reportData.id,
        market_id: insight.market_id,
        market_name: insight.market_name,
        sentiment_analysis: insight.sentiment_analysis,
        key_trends: insight.key_trends || [],
        opportunities: insight.opportunities || [],
        threats: insight.threats || [],
        competitor_activity: insight.competitor_activity,
        search_keywords: insight.search_keywords || [],
        competitors_tracked: insight.competitors_tracked || [],
      }));

      const { error: insightsError } = await supabase
        .from('market_insights')
        .insert(insightsToInsert);

      if (insightsError) {
        console.error('Error inserting insights:', insightsError);
        // Don't fail the whole request if insights fail
      }
    }

    return new Response(
      JSON.stringify({ 
        success: true, 
        report_id: reportData.id,
        message: 'Report saved successfully' 
      }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    console.error('Error saving market research report:', error);
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});


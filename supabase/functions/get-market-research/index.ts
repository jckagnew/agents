import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { getCorsHeaders, handleCors } from '../_shared/cors.ts';
import { verifyAdmin } from '../_shared/auth.ts';

serve(async (req) => {
  // Handle CORS
  const corsResponse = handleCors(req);
  if (corsResponse) return corsResponse;

  const corsHeaders = getCorsHeaders(req);

  try {
    // Verify admin authentication
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return new Response(
        JSON.stringify({ error: 'Missing authorization header' }),
        {
          status: 401,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        }
      );
    }

    const { user, supabase } = await verifyAdmin(authHeader);

    // Parse query parameters
    const url = new URL(req.url);
    const reportId = url.searchParams.get('id');
    const startDate = url.searchParams.get('start_date');
    const endDate = url.searchParams.get('end_date');
    const limit = parseInt(url.searchParams.get('limit') || '30');

    let reports;

    if (reportId) {
      // Get specific report
      const { data, error } = await supabase
        .from('market_research_reports')
        .select(`
          *,
          market_insights (*)
        `)
        .eq('id', reportId)
        .single();

      if (error) throw error;
      reports = data;
    } else {
      // Get reports by date range
      const start = startDate || null;
      const end = endDate || null;

      const { data, error } = await supabase
        .from('market_research_reports')
        .select('*')
        .order('report_date', { ascending: false })
        .limit(limit);

      if (start) {
        data?.filter(r => r.report_date >= start);
      }
      if (end) {
        data?.filter(r => r.report_date <= end);
      }

      if (error) throw error;
      reports = data;
    }

    return new Response(
      JSON.stringify({ reports }),
      {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  } catch (error) {
    console.error('Error fetching market research reports:', error);
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      }
    );
  }
});


import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { corsHeaders, handleCors } from '../_shared/cors.ts';
import { verifyAdmin } from '../_shared/auth.ts';

serve(async (req) => {
  // Handle CORS
  const corsResponse = handleCors(req);
  if (corsResponse) return corsResponse;

  try {
    // Verify admin authentication
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return new Response(JSON.stringify({ error: 'Missing authorization header' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const { supabase } = await verifyAdmin(authHeader);

    const url = new URL(req.url);
    const projectId = url.searchParams.get('id');

    switch (req.method) {
      case 'GET': {
        if (projectId) {
          // Get single project with full details
          const { data: project, error } = await supabase
            .from('projects')
            .select(`
              *,
              customer:customers(*),
              notes:project_notes(
                *,
                author:admin_users(full_name, email)
              ),
              invoices:invoices(*)
            `)
            .eq('id', projectId)
            .single();

          if (error) {
            return new Response(JSON.stringify({ error: error.message }), {
              status: 400,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            });
          }

          return new Response(JSON.stringify(project), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        } else {
          // Get all projects with filters
          const page = parseInt(url.searchParams.get('page') || '1');
          const limit = parseInt(url.searchParams.get('limit') || '20');
          const status = url.searchParams.get('status');
          const productType = url.searchParams.get('product_type');
          const customerId = url.searchParams.get('customer_id');

          let query = supabase
            .from('projects')
            .select(`
              *,
              customer:customers(id, full_name, email, company_name)
            `, { count: 'exact' })
            .order('created_at', { ascending: false })
            .range((page - 1) * limit, page * limit - 1);

          if (status) {
            query = query.eq('status', status);
          }

          if (productType) {
            query = query.eq('product_type', productType);
          }

          if (customerId) {
            query = query.eq('customer_id', customerId);
          }

          const { data: projects, error, count } = await query;

          if (error) {
            return new Response(JSON.stringify({ error: error.message }), {
              status: 400,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            });
          }

          return new Response(
            JSON.stringify({
              projects,
              pagination: {
                page,
                limit,
                total: count,
                totalPages: Math.ceil((count || 0) / limit),
              },
            }),
            {
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            }
          );
        }
      }

      case 'POST': {
        const body = await req.json();

        // Validate required fields
        if (!body.name || !body.customer_id) {
          return new Response(
            JSON.stringify({ error: 'Missing required fields: name, customer_id' }),
            {
              status: 400,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            }
          );
        }

        const { data: project, error } = await supabase
          .from('projects')
          .insert({
            name: body.name,
            description: body.description,
            customer_id: body.customer_id,
            product_type: body.product_type || 'express',
            pricing_tier: body.pricing_tier,
            status: body.status || 'INTAKE',
            estimated_delivery_date: body.estimated_delivery_date,
            design_upload_url: body.design_upload_url,
          })
          .select(`
            *,
            customer:customers(*)
          `)
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(project), {
          status: 201,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      case 'PATCH': {
        if (!projectId) {
          return new Response(JSON.stringify({ error: 'Project ID required' }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        const body = await req.json();

        const { data: project, error } = await supabase
          .from('projects')
          .update({
            name: body.name,
            description: body.description,
            status: body.status,
            product_type: body.product_type,
            pricing_tier: body.pricing_tier,
            estimated_delivery_date: body.estimated_delivery_date,
            actual_delivery_date: body.actual_delivery_date,
            design_upload_url: body.design_upload_url,
            final_code_url: body.final_code_url,
            visual_qa_score: body.visual_qa_score,
          })
          .eq('id', projectId)
          .select(`
            *,
            customer:customers(*)
          `)
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(project), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      case 'DELETE': {
        if (!projectId) {
          return new Response(JSON.stringify({ error: 'Project ID required' }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        const { error } = await supabase.from('projects').delete().eq('id', projectId);

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify({ success: true }), {
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      default:
        return new Response(JSON.stringify({ error: 'Method not allowed' }), {
          status: 405,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
    }
  } catch (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: error.message.includes('Unauthorized') || error.message.includes('admin') ? 403 : 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
});

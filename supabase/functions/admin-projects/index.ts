import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { getCorsHeaders, handleCors } from '../_shared/cors.ts';
import { verifyAdmin } from '../_shared/auth.ts';
import {
  createProjectSchema,
  updateProjectSchema,
  validateInput,
} from '../_shared/validation.ts';
import {
  checkRateLimit,
  rateLimitExceededResponse,
  getRateLimitHeaders,
  RATE_LIMITS,
} from '../_shared/rate-limit.ts';

serve(async (req) => {
  // Handle CORS
  const corsResponse = handleCors(req);
  if (corsResponse) return corsResponse;

  // Get CORS headers for this request
  const corsHeaders = getCorsHeaders(req);

  try {
    // Verify admin authentication
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return new Response(JSON.stringify({ error: 'Missing authorization header' }), {
        status: 401,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const { user, supabase } = await verifyAdmin(authHeader);

    // Rate limiting - use user ID as identifier
    const rateLimitInfo = checkRateLimit(user.id, RATE_LIMITS.moderate);
    if (!rateLimitInfo.allowed) {
      return rateLimitExceededResponse(rateLimitInfo, RATE_LIMITS.moderate, corsHeaders);
    }

    const url = new URL(req.url);
    const projectId = url.searchParams.get('id');

    switch (req.method) {
      case 'GET': {
        if (projectId) {
          // Get single project with full details (exclude soft-deleted)
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
            .is('deleted_at', null)
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
            .is('deleted_at', null) // Exclude soft-deleted
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

        // Validate input
        const validation = validateInput(createProjectSchema, body);
        if (!validation.success) {
          return new Response(
            JSON.stringify({
              error: 'Validation failed',
              details: validation.errors,
            }),
            {
              status: 400,
              headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
            }
          );
        }

        const { data: project, error } = await supabase
          .from('projects')
          .insert(validation.data)
          .select(`
            *,
            customer:customers(*)
          `)
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(project), {
          status: 201,
          headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
        });
      }

      case 'PATCH': {
        if (!projectId) {
          return new Response(JSON.stringify({ error: 'Project ID required' }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        const body = await req.json();

        // Validate input
        const validation = validateInput(updateProjectSchema, body);
        if (!validation.success) {
          return new Response(
            JSON.stringify({
              error: 'Validation failed',
              details: validation.errors,
            }),
            {
              status: 400,
              headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
            }
          );
        }

        const { data: project, error } = await supabase
          .from('projects')
          .update(validation.data)
          .eq('id', projectId)
          .select(`
            *,
            customer:customers(*)
          `)
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(project), {
          headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
        });
      }

      case 'DELETE': {
        if (!projectId) {
          return new Response(JSON.stringify({ error: 'Project ID required' }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        // Soft delete instead of hard delete
        const { error } = await supabase
          .from('projects')
          .update({
            deleted_at: new Date().toISOString(),
            deleted_by: user.id,
          })
          .eq('id', projectId);

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify({ success: true, message: 'Project archived successfully' }), {
          headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
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

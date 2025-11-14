import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { getCorsHeaders, handleCors } from '../_shared/cors.ts';
import { verifyAdmin } from '../_shared/auth.ts';
import {
  createCustomerSchema,
  updateCustomerSchema,
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
    const customerId = url.searchParams.get('id');

    switch (req.method) {
      case 'GET': {
        if (customerId) {
          // Get single customer with stats (exclude soft-deleted)
          const { data: customer, error } = await supabase
            .from('customers')
            .select(`
              *,
              projects:projects(count),
              invoices:invoices(
                id,
                amount,
                status,
                created_at
              )
            `)
            .eq('id', customerId)
            .is('deleted_at', null)
            .single();

          if (error) {
            return new Response(JSON.stringify({ error: error.message }), {
              status: 400,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            });
          }

          return new Response(JSON.stringify(customer), {
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        } else {
          // Get all customers with pagination
          const page = parseInt(url.searchParams.get('page') || '1');
          const limit = parseInt(url.searchParams.get('limit') || '20');
          const status = url.searchParams.get('status');
          const search = url.searchParams.get('search');

          let query = supabase
            .from('customers')
            .select(`
              *,
              projects:projects(count)
            `, { count: 'exact' })
            .is('deleted_at', null) // Exclude soft-deleted
            .order('created_at', { ascending: false })
            .range((page - 1) * limit, page * limit - 1);

          if (status) {
            query = query.eq('status', status);
          }

          if (search) {
            // Sanitize search input to prevent SQL injection
            // Escape special LIKE characters: % and _
            const sanitizedSearch = search.replace(/[%_]/g, '\\$&');
            query = query.or(`full_name.ilike.%${sanitizedSearch}%,email.ilike.%${sanitizedSearch}%,company_name.ilike.%${sanitizedSearch}%`);
          }

          const { data: customers, error, count } = await query;

          if (error) {
            return new Response(JSON.stringify({ error: error.message }), {
              status: 400,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            });
          }

          return new Response(
            JSON.stringify({
              customers,
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
        const validation = validateInput(createCustomerSchema, body);
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

        const { data: customer, error } = await supabase
          .from('customers')
          .insert(validation.data)
          .select()
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(customer), {
          status: 201,
          headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
        });
      }

      case 'PATCH': {
        if (!customerId) {
          return new Response(JSON.stringify({ error: 'Customer ID required' }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        const body = await req.json();

        // Validate input
        const validation = validateInput(updateCustomerSchema, body);
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

        const { data: customer, error } = await supabase
          .from('customers')
          .update(validation.data)
          .eq('id', customerId)
          .select()
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(customer), {
          headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
        });
      }

      case 'DELETE': {
        if (!customerId) {
          return new Response(JSON.stringify({ error: 'Customer ID required' }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        // Soft delete instead of hard delete
        const { error } = await supabase
          .from('customers')
          .update({
            deleted_at: new Date().toISOString(),
            deleted_by: user.id,
          })
          .eq('id', customerId);

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, ...getRateLimitHeaders(rateLimitInfo, RATE_LIMITS.moderate), 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify({ success: true, message: 'Customer archived successfully' }), {
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

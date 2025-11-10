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
    const customerId = url.searchParams.get('id');

    switch (req.method) {
      case 'GET': {
        if (customerId) {
          // Get single customer with stats
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
            .order('created_at', { ascending: false })
            .range((page - 1) * limit, page * limit - 1);

          if (status) {
            query = query.eq('status', status);
          }

          if (search) {
            query = query.or(`full_name.ilike.%${search}%,email.ilike.%${search}%,company_name.ilike.%${search}%`);
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

        // Validate required fields
        if (!body.full_name || !body.email) {
          return new Response(
            JSON.stringify({ error: 'Missing required fields: full_name, email' }),
            {
              status: 400,
              headers: { ...corsHeaders, 'Content-Type': 'application/json' },
            }
          );
        }

        const { data: customer, error } = await supabase
          .from('customers')
          .insert({
            full_name: body.full_name,
            email: body.email,
            phone: body.phone,
            company_name: body.company_name,
            subscription_status: body.subscription_status || 'none',
            subscription_tier: body.subscription_tier,
            source: body.source,
            tags: body.tags || [],
          })
          .select()
          .single();

        if (error) {
          return new Response(JSON.stringify({ error: error.message }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        return new Response(JSON.stringify(customer), {
          status: 201,
          headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        });
      }

      case 'PATCH': {
        if (!customerId) {
          return new Response(JSON.stringify({ error: 'Customer ID required' }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        const body = await req.json();

        const { data: customer, error } = await supabase
          .from('customers')
          .update({
            full_name: body.full_name,
            email: body.email,
            phone: body.phone,
            company_name: body.company_name,
            subscription_status: body.subscription_status,
            subscription_tier: body.subscription_tier,
            status: body.status,
            tags: body.tags,
            notes: body.notes,
          })
          .eq('id', customerId)
          .select()
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
      }

      case 'DELETE': {
        if (!customerId) {
          return new Response(JSON.stringify({ error: 'Customer ID required' }), {
            status: 400,
            headers: { ...corsHeaders, 'Content-Type': 'application/json' },
          });
        }

        const { error } = await supabase.from('customers').delete().eq('id', customerId);

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

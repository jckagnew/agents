import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

/**
 * Check if the authenticated user is an admin
 */
export async function verifyAdmin(authHeader: string) {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    {
      global: {
        headers: { Authorization: authHeader },
      },
    }
  );

  // Get the authenticated user
  const {
    data: { user },
    error: userError,
  } = await supabase.auth.getUser();

  if (userError || !user) {
    throw new Error('Unauthorized');
  }

  // Check if user is admin
  const { data: adminUser, error: adminError } = await supabase
    .from('admin_users')
    .select('role, is_active')
    .eq('user_id', user.id)
    .single();

  if (adminError || !adminUser) {
    throw new Error('Not an admin user');
  }

  if (!adminUser.is_active) {
    throw new Error('Admin account is inactive');
  }

  if (!['super_admin', 'admin'].includes(adminUser.role)) {
    throw new Error('Insufficient permissions');
  }

  return { user, adminUser, supabase };
}

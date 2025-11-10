import React, { createContext, useContext, useEffect, useState } from 'react';
import { Session, User } from '@supabase/supabase-js';
import { supabase } from '@/lib/supabase';

interface AdminUser {
  role: 'super_admin' | 'admin' | 'viewer';
  is_active: boolean;
  full_name: string;
  email: string;
}

interface AuthContextType {
  session: Session | null;
  user: User | null;
  adminUser: AdminUser | null;
  isAdmin: boolean;
  loading: boolean;
  signOut: () => Promise<void>;
  refreshAdminStatus: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const [adminUser, setAdminUser] = useState<AdminUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      if (session?.user) {
        checkAdminStatus(session.user.id);
      } else {
        setLoading(false);
      }
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        if (session?.user) {
          checkAdminStatus(session.user.id);
        } else {
          setAdminUser(null);
          setLoading(false);
        }
      }
    );

    return () => subscription.unsubscribe();
  }, []);

  const checkAdminStatus = async (userId: string) => {
    try {
      const { data, error } = await supabase
        .from('admin_users')
        .select('role, is_active, full_name, email')
        .eq('user_id', userId)
        .single();

      if (error) {
        console.error('Error fetching admin status:', error);
        setAdminUser(null);
      } else {
        setAdminUser(data);
      }
    } catch (error) {
      console.error('Error checking admin status:', error);
      setAdminUser(null);
    } finally {
      setLoading(false);
    }
  };

  const refreshAdminStatus = async () => {
    if (user) {
      await checkAdminStatus(user.id);
    }
  };

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  const isAdmin =
    adminUser !== null &&
    adminUser.is_active &&
    ['super_admin', 'admin'].includes(adminUser.role);

  return (
    <AuthContext.Provider
      value={{
        session,
        user,
        adminUser,
        isAdmin,
        loading,
        signOut,
        refreshAdminStatus,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

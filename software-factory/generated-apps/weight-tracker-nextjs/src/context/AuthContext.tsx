'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

// Types
interface User {
  id: string;
  username: string;
  emoji: string;
  loginTime: number;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  isLoading: boolean;
}

// Context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider Component
interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isClient, setIsClient] = useState(false);

  // Set client flag on mount
  useEffect(() => {
    setIsClient(true);
  }, []);

  // Check for existing session on mount
  useEffect(() => {
    if (!isClient) return;

    const checkSession = () => {
      try {
        console.log('AuthContext: Client side, checking session');
        const storedUser = localStorage.getItem('weight-tracker-user');
        if (storedUser) {
          const userData = JSON.parse(storedUser);
          const now = Date.now();
          const sessionDuration = 24 * 60 * 60 * 1000; // 24 hours
          
          if (now - userData.loginTime < sessionDuration) {
            console.log('AuthContext: Valid session found, setting user');
            setUser(userData);
          } else {
            console.log('AuthContext: Session expired, clearing');
            // Session expired
            localStorage.removeItem('weight-tracker-user');
          }
        } else {
          console.log('AuthContext: No stored user found');
        }
      } catch (error) {
        console.error('Error checking session:', error);
        localStorage.removeItem('weight-tracker-user');
      }
    };

    checkSession();
  }, [isClient]);

  const login = async (username: string, password: string): Promise<boolean> => {
    setIsLoading(true);
    
    try {
      // Demo credentials for now
      const validCredentials = [
        { username: 'demo', password: 'demo123' },
        { username: 'admin', password: 'admin123' },
        { username: 'user', password: 'password' }
      ];

      const isValid = validCredentials.some(
        cred => cred.username === username && cred.password === password
      );

      if (isValid) {
        const userData: User = {
          id: `user_${Date.now()}`,
          username,
          emoji: '👤', // Default emoji, can be customized later
          loginTime: Date.now()
        };

        setUser(userData);
        if (typeof window !== 'undefined') {
          localStorage.setItem('weight-tracker-user', JSON.stringify(userData));
        }
        return true;
      } else {
        return false;
      }
    } catch (error) {
      console.error('Login error:', error);
      return false;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setUser(null);
    if (typeof window !== 'undefined') {
      localStorage.removeItem('weight-tracker-user');
      // Clear all weight data for privacy
      localStorage.removeItem('weight-tracker-data');
    }
  };

  const value: AuthContextType = {
    user,
    isAuthenticated: !!user,
    login,
    logout,
    isLoading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook
export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

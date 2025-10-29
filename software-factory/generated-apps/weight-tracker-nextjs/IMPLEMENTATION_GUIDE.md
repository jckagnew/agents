# Weight Tracker Enhancement Implementation Guide

## Quick Start Implementation

### Step 1: Create Authentication Context
```typescript
// src/context/AuthContext.tsx
'use client';
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface User {
  id: string;
  username: string;
  emoji: string;
  loginTime: Date;
}

interface AuthContextType {
  isAuthenticated: boolean;
  user: User | null;
  login: (username: string, password: string) => Promise<boolean>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Demo credentials
const DEMO_CREDENTIALS = {
  username: 'demo',
  password: 'weighttracker2025',
  emoji: '🏃‍♂️'
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing session
    const savedUser = localStorage.getItem('weightTrackerUser');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      setIsAuthenticated(true);
    }
    setLoading(false);
  }, []);

  const login = async (username: string, password: string): Promise<boolean> => {
    setLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (username === DEMO_CREDENTIALS.username && password === DEMO_CREDENTIALS.password) {
      const newUser: User = {
        id: '1',
        username,
        emoji: DEMO_CREDENTIALS.emoji,
        loginTime: new Date()
      };
      
      setUser(newUser);
      setIsAuthenticated(true);
      localStorage.setItem('weightTrackerUser', JSON.stringify(newUser));
      setLoading(false);
      return true;
    }
    
    setLoading(false);
    return false;
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem('weightTrackerUser');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
```

### Step 2: Create Splash Screen
```typescript
// src/components/SplashScreen.tsx
'use client';
import React, { useState, useEffect } from 'react';
import { PillButton } from './design-system';

interface SplashScreenProps {
  onGetStarted: () => void;
}

export const SplashScreen: React.FC<SplashScreenProps> = ({ onGetStarted }) => {
  const [animationPhase, setAnimationPhase] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimationPhase(prev => (prev + 1) % 4);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const getCharacter = () => {
    switch (animationPhase) {
      case 0: return '🧑‍💼'; // Before
      case 1: return '🧑‍💼'; // Transition
      case 2: return '🏃‍♂️'; // After
      case 3: return '🏃‍♂️'; // Celebration
      default: return '🧑‍💼';
    }
  };

  const getMessage = () => {
    switch (animationPhase) {
      case 0: return 'Start your journey...';
      case 1: return 'Transform your body...';
      case 2: return 'Achieve your goals...';
      case 3: return 'You can do it!';
      default: return 'Start your journey...';
    }
  };

  return (
    <div className="splash-container">
      <div className="splash-content">
        <div className="character-animation">
          <div className="character">
            {getCharacter()}
          </div>
        </div>
        
        <h1 className="splash-title">
          Transform Your Life
        </h1>
        
        <p className="splash-subtitle">
          {getMessage()}
        </p>
        
        <p className="splash-description">
          Track. Transform. Triumph.<br />
          Your journey starts here.
        </p>
        
        <PillButton
          variant="primary"
          onClick={onGetStarted}
          className="splash-cta"
        >
          Start Your Journey
        </PillButton>
      </div>
      
      <style jsx>{`
        .splash-container {
          min-height: 100vh;
          background: linear-gradient(135deg, #dc2626 0%, #ef4444 25%, #f59e0b 50%, #84cc16 75%, #22c55e 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
        }
        
        .splash-content {
          text-align: center;
          color: white;
          max-width: 500px;
        }
        
        .character-animation {
          margin-bottom: 2rem;
        }
        
        .character {
          font-size: 8rem;
          animation: bounce 2s ease-in-out infinite;
          display: inline-block;
        }
        
        .splash-title {
          font-size: 3rem;
          font-weight: bold;
          margin-bottom: 1rem;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .splash-subtitle {
          font-size: 1.5rem;
          margin-bottom: 1rem;
          opacity: 0.9;
        }
        
        .splash-description {
          font-size: 1.2rem;
          margin-bottom: 2rem;
          opacity: 0.8;
          line-height: 1.6;
        }
        
        .splash-cta {
          font-size: 1.2rem;
          padding: 1rem 2rem;
          box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-20px);
          }
          60% {
            transform: translateY(-10px);
          }
        }
        
        @media (max-width: 768px) {
          .character {
            font-size: 6rem;
          }
          
          .splash-title {
            font-size: 2.5rem;
          }
          
          .splash-subtitle {
            font-size: 1.2rem;
          }
          
          .splash-description {
            font-size: 1rem;
          }
        }
      `}</style>
    </div>
  );
};
```

### Step 3: Create Login Screen
```typescript
// src/components/LoginScreen.tsx
'use client';
import React, { useState } from 'react';
import { PillButton } from './design-system';
import { useAuth } from '../context/AuthContext';

interface LoginScreenProps {
  onBack: () => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onBack }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    const success = await login(username, password);
    if (!success) {
      setError('Invalid username or password');
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>Welcome Back</h1>
          <p>Sign in to continue your journey</p>
        </div>
        
        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>
          
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}
          
          <div className="form-actions">
            <PillButton
              type="button"
              variant="tertiary"
              onClick={onBack}
            >
              Back
            </PillButton>
            
            <PillButton
              type="submit"
              variant="primary"
              disabled={loading}
            >
              {loading ? 'Signing In...' : 'Sign In'}
            </PillButton>
          </div>
        </form>
        
        <div className="demo-credentials">
          <p><strong>Demo Credentials:</strong></p>
          <p>Username: <code>demo</code></p>
          <p>Password: <code>weighttracker2025</code></p>
        </div>
      </div>
      
      <style jsx>{`
        .login-container {
          min-height: 100vh;
          background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
        }
        
        .login-card {
          background: white;
          border-radius: 1rem;
          padding: 2rem;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
          width: 100%;
          max-width: 400px;
        }
        
        .login-header {
          text-align: center;
          margin-bottom: 2rem;
        }
        
        .login-header h1 {
          font-size: 2rem;
          font-weight: bold;
          color: #1f2937;
          margin-bottom: 0.5rem;
        }
        
        .login-header p {
          color: #6b7280;
        }
        
        .form-group {
          margin-bottom: 1.5rem;
        }
        
        .form-group label {
          display: block;
          margin-bottom: 0.5rem;
          font-weight: 500;
          color: #374151;
        }
        
        .form-group input {
          width: 100%;
          padding: 0.75rem;
          border: 2px solid #e5e7eb;
          border-radius: 0.5rem;
          font-size: 1rem;
          transition: border-color 0.2s;
        }
        
        .form-group input:focus {
          outline: none;
          border-color: #3b82f6;
        }
        
        .error-message {
          background: #fef2f2;
          color: #dc2626;
          padding: 0.75rem;
          border-radius: 0.5rem;
          margin-bottom: 1rem;
          text-align: center;
        }
        
        .form-actions {
          display: flex;
          gap: 1rem;
          margin-bottom: 1.5rem;
        }
        
        .form-actions button {
          flex: 1;
        }
        
        .demo-credentials {
          background: #f3f4f6;
          padding: 1rem;
          border-radius: 0.5rem;
          text-align: center;
          font-size: 0.875rem;
          color: #6b7280;
        }
        
        .demo-credentials code {
          background: #e5e7eb;
          padding: 0.25rem 0.5rem;
          border-radius: 0.25rem;
          font-family: monospace;
        }
      `}</style>
    </div>
  );
};
```

### Step 4: Create User Indicator
```typescript
// src/components/UserIndicator.tsx
'use client';
import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export const UserIndicator: React.FC = () => {
  const [showMenu, setShowMenu] = useState(false);
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <div className="user-indicator">
      <button
        className="user-avatar"
        onClick={() => setShowMenu(!showMenu)}
        aria-label="User menu"
      >
        <span className="user-emoji">{user.emoji}</span>
      </button>
      
      {showMenu && (
        <div className="user-menu">
          <div className="user-info">
            <span className="user-emoji">{user.emoji}</span>
            <span className="user-name">{user.username}</span>
          </div>
          
          <div className="menu-divider"></div>
          
          <button className="menu-item" onClick={() => setShowMenu(false)}>
            View Profile
          </button>
          
          <button className="menu-item" onClick={() => setShowMenu(false)}>
            Settings
          </button>
          
          <div className="menu-divider"></div>
          
          <button className="menu-item logout" onClick={logout}>
            Logout
          </button>
        </div>
      )}
      
      <style jsx>{`
        .user-indicator {
          position: fixed;
          top: 1rem;
          right: 1rem;
          z-index: 1000;
        }
        
        .user-avatar {
          width: 3rem;
          height: 3rem;
          border-radius: 50%;
          background: white;
          border: 2px solid #e5e7eb;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: all 0.2s;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .user-avatar:hover {
          border-color: #3b82f6;
          transform: scale(1.05);
        }
        
        .user-emoji {
          font-size: 1.5rem;
        }
        
        .user-menu {
          position: absolute;
          top: 100%;
          right: 0;
          background: white;
          border-radius: 0.5rem;
          box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
          min-width: 200px;
          margin-top: 0.5rem;
          overflow: hidden;
        }
        
        .user-info {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 1rem;
          background: #f9fafb;
        }
        
        .user-name {
          font-weight: 500;
          color: #374151;
        }
        
        .menu-divider {
          height: 1px;
          background: #e5e7eb;
        }
        
        .menu-item {
          width: 100%;
          padding: 0.75rem 1rem;
          text-align: left;
          background: none;
          border: none;
          cursor: pointer;
          transition: background-color 0.2s;
          color: #374151;
        }
        
        .menu-item:hover {
          background: #f3f4f6;
        }
        
        .menu-item.logout {
          color: #dc2626;
        }
        
        .menu-item.logout:hover {
          background: #fef2f2;
        }
      `}</style>
    </div>
  );
};
```

### Step 5: Update Main App Router
```typescript
// src/app/page.tsx
'use client';
import React, { useState } from 'react';
import { WeightProvider } from '../context/WeightContext';
import { AuthProvider, useAuth } from '../context/AuthContext';
import { SplashScreen } from '../components/SplashScreen';
import { LoginScreen } from '../components/LoginScreen';
import { UserIndicator } from '../components/UserIndicator';
import { DashboardScreen } from '../components/DashboardScreen';
import { HistoryScreen } from '../components/HistoryScreen';
import { LogEntryScreen } from '../components/LogEntryScreen';
import { AnalyticsScreen } from '../components/AnalyticsScreen';
import { SettingsScreen } from '../components/SettingsScreen';

function AppContent() {
  const { isAuthenticated, loading } = useAuth();
  const [appState, setAppState] = useState<'splash' | 'login' | 'app'>('splash');
  const [currentScreen, setCurrentScreen] = useState('dashboard');

  const handleNavigate = (screen: string) => {
    setCurrentScreen(screen);
  };

  const handleGetStarted = () => {
    setAppState('login');
  };

  const handleBackToSplash = () => {
    setAppState('splash');
  };

  const renderScreen = () => {
    switch (currentScreen) {
      case 'dashboard':
        return <DashboardScreen onNavigate={handleNavigate} />;
      case 'history':
        return <HistoryScreen onNavigate={handleNavigate} />;
      case 'log-entry':
        return <LogEntryScreen onNavigate={handleNavigate} />;
      case 'analytics':
        return <AnalyticsScreen onNavigate={handleNavigate} />;
      case 'settings':
        return <SettingsScreen onNavigate={handleNavigate} />;
      default:
        return <DashboardScreen onNavigate={handleNavigate} />;
    }
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner">🏃‍♂️</div>
        <p>Loading...</p>
      </div>
    );
  }

  if (!isAuthenticated) {
    if (appState === 'splash') {
      return <SplashScreen onGetStarted={handleGetStarted} />;
    }
    return <LoginScreen onBack={handleBackToSplash} />;
  }

  return (
    <div className="app-container">
      <UserIndicator />
      {renderScreen()}
    </div>
  );
}

export default function WeightTrackerPro() {
  return (
    <AuthProvider>
      <WeightProvider>
        <AppContent />
      </WeightProvider>
    </AuthProvider>
  );
}
```

## Implementation Checklist

### Phase 1: Core Components
- [ ] Create `AuthContext.tsx`
- [ ] Create `SplashScreen.tsx`
- [ ] Create `LoginScreen.tsx`
- [ ] Create `UserIndicator.tsx`

### Phase 2: Integration
- [ ] Update `page.tsx` with new routing
- [ ] Add `UserIndicator` to all screens
- [ ] Test authentication flow
- [ ] Test logout functionality

### Phase 3: Polish
- [ ] Add loading states
- [ ] Improve error handling
- [ ] Test mobile responsiveness
- [ ] Add accessibility features

## Testing the Implementation

1. **Start the app** - Should show splash screen
2. **Click "Start Your Journey"** - Should show login screen
3. **Enter demo credentials** - Should show dashboard with user indicator
4. **Click user indicator** - Should show user menu
5. **Click logout** - Should return to splash screen

## Demo Credentials
- **Username**: `demo`
- **Password**: `weighttracker2025`
- **User Emoji**: `🏃‍♂️`

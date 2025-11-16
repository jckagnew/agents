'use client';

import React from 'react';
import {
  HomeIcon,
  ClockIcon,
  PlusCircleIcon,
  ChartBarIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

export type NavTab = 'dashboard' | 'history' | 'logEntry' | 'analytics' | 'settings';

interface NavigationBarProps {
  activeTab: NavTab;
  onNavigate: (tab: NavTab) => void;
}

export function NavigationBar({ activeTab, onNavigate }: NavigationBarProps) {
  const tabs: Array<{ id: NavTab; label: string; icon: React.ReactNode; route: string }> = [
    { id: 'dashboard', label: 'Dashboard', icon: <HomeIcon className="h-6 w-6" />, route: 'dashboard' },
    { id: 'history', label: 'History', icon: <ClockIcon className="h-6 w-6" />, route: 'history' },
    { id: 'logEntry', label: 'Log', icon: <PlusCircleIcon className="h-6 w-6" />, route: 'logEntry' },
    { id: 'analytics', label: 'Analytics', icon: <ChartBarIcon className="h-6 w-6" />, route: 'analytics' },
    { id: 'settings', label: 'Settings', icon: <Cog6ToothIcon className="h-6 w-6" />, route: 'settings' },
  ];

  return (
    <>
      {/* Mobile bottom navigation (< 768px) */}
      <nav
        className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-40"
        role="navigation"
        aria-label="Main navigation"
      >
        <ul className="flex justify-around items-center h-16 px-2">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <li key={tab.id} className="flex-1">
                <button
                  type="button"
                  onClick={() => onNavigate(tab.id)}
                  aria-current={isActive ? 'page' : undefined}
                  className={`
                    w-full h-full flex flex-col items-center justify-center space-y-1
                    transition-colors duration-200
                    ${isActive ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'}
                  `}
                  aria-label={tab.label}
                >
                  {tab.icon}
                  <span className="text-xs font-medium">{tab.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* Desktop sidebar navigation (>= 768px) */}
      <nav
        className="hidden md:flex fixed left-0 top-0 bottom-0 w-64 bg-white border-r border-gray-200 z-30"
        role="navigation"
        aria-label="Main navigation"
      >
        <ul className="w-full flex flex-col space-y-2 p-4">
          {tabs.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <li key={tab.id}>
                <button
                  type="button"
                  onClick={() => onNavigate(tab.id)}
                  aria-current={isActive ? 'page' : undefined}
                  className={`
                    w-full flex items-center space-x-3 px-4 py-3 rounded-lg
                    transition-colors duration-200
                    ${isActive 
                      ? 'bg-blue-50 text-blue-600 font-semibold' 
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                    }
                  `}
                >
                  {tab.icon}
                  <span>{tab.label}</span>
                </button>
              </li>
            );
          })}
        </ul>
      </nav>
    </>
  );
}

'use client';

import React, { useState } from 'react';
import { WeightProvider } from '../context/WeightContext';
import { DashboardScreen } from '../components/DashboardScreen';
import { HistoryScreen } from '../components/HistoryScreen';
import { LogEntryScreen } from '../components/LogEntryScreen';
import { AnalyticsScreen } from '../components/AnalyticsScreen';
import { SettingsScreen } from '../components/SettingsScreen';

export default function WeightTrackerPro() {
  const [currentScreen, setCurrentScreen] = useState('dashboard');

  const handleNavigate = (screen: string) => {
    setCurrentScreen(screen);
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

  return (
    <WeightProvider>
      {renderScreen()}
    </WeightProvider>
  );
}
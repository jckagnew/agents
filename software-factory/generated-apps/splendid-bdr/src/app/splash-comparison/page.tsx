'use client';
import React, { useState } from 'react';
import SplashScreen1 from '../../components/splash-prototypes/SplashScreen1';
import SplashScreen2 from '../../components/splash-prototypes/SplashScreen2';
import SplashScreen3 from '../../components/splash-prototypes/SplashScreen3';

export default function SplashComparison() {
  const [currentVersion, setCurrentVersion] = useState(1);
  const versions = [
    { id: 1, name: 'Version 1', component: SplashScreen1, score: 0.87 },
    { id: 2, name: 'Version 2', component: SplashScreen2, score: 0.87 },
    { id: 3, name: 'Version 3', component: SplashScreen3, score: 0.87 }
  ];

  const CurrentComponent = versions.find((version) => version.id === currentVersion)?.component;

  const handleCreateProfile = () => {
    console.log('Create Profile clicked');
  };

  const handleLogin = () => {
    console.log('Login clicked');
  };

  return (
    <div className="comparison-container">
      <div className="version-selector">
        {versions.map((version) => (
          <button
            key={version.id}
            className={`version-button ${currentVersion === version.id ? 'active' : ''}`}
            onClick={() => setCurrentVersion(version.id)}
          >
            <span className="version-name">{version.name}</span>
            <span className="score">Score: {version.score.toFixed(2)}</span>
          </button>
        ))}
      </div>

      <div className="prototype-container">
        {CurrentComponent ? (
          <CurrentComponent onGetStarted={handleCreateProfile} onLogin={handleLogin} />
        ) : (
          <div className="empty-state">
            <p>No prototypes generated yet.</p>
          </div>
        )}
      </div>

      <style jsx>{`
        .comparison-container {
          min-height: 100vh;
          background: #f5f7fa;
        }

        .version-selector {
          position: sticky;
          top: 0;
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          justify-content: center;
          background: rgba(255, 255, 255, 0.92);
          padding: 1rem;
          box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);
          backdrop-filter: blur(10px);
          z-index: 10;
        }

        .version-button {
          min-width: 180px;
          border-radius: 999px;
          padding: 0.75rem 1.25rem;
          border: 2px solid #e2e8f0;
          background: white;
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          align-items: center;
          transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .version-button:hover {
          transform: translateY(-2px);
          border-color: #38bdf8;
          box-shadow: 0 16px 32px rgba(56, 189, 248, 0.18);
        }

        .version-button.active {
          border-color: #22c55e;
          background: linear-gradient(135deg, #ecfeff 0%, #dcfce7 100%);
        }

        .version-name {
          font-weight: 600;
          color: #0f172a;
        }

        .score {
          font-size: 0.85rem;
          color: #475569;
        }

        .prototype-container {
          padding: 2rem 0 4rem;
        }

        .empty-state {
          padding: 6rem 2rem;
          text-align: center;
          color: #64748b;
        }
      `}</style>
    </div>
  );
}
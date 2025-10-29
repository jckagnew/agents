'use client';
import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { PillButton } from '../design-system';

interface SplashScreenV3Props {
  onCreateProfile: () => void;
  onLogin: () => void;
}

export const SplashScreenV3: React.FC<SplashScreenV3Props> = ({
  onCreateProfile,
  onLogin,
}) => {
  const [currentFrame, setCurrentFrame] = useState(0);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const frames = [
  {
    "src": "data:image/svg+xml;base64,CjxzdmcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB3aWR0aD0nNjAwJyBoZWlnaHQ9JzgwMCc+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9J2dyYWQnIHgxPScwJScgeTE9JzAlJyB4Mj0nMCUnIHkyPScxMDAlJz4KICAgICAgPHN0b3Agb2Zmc2V0PScwJScgc3RvcC1jb2xvcj0nIzExMTgyNycvPgogICAgICA8c3RvcCBvZmZzZXQ9JzEwMCUnIHN0b3AtY29sb3I9JyMxRjI5MzcnLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSc2MDAnIGhlaWdodD0nODAwJyByeD0nNDgnIGZpbGw9J3VybCgjZ3JhZCknLz4KICA8dGV4dCB4PSc1MCUnIHk9JzQ1JScgZG9taW5hbnQtYmFzZWxpbmU9J21pZGRsZScgdGV4dC1hbmNob3I9J21pZGRsZScKICAgICAgICBmb250LWZhbWlseT0nUG9wcGlucywgSGVsdmV0aWNhLCBBcmlhbCcgZm9udC1zaXplPSc0OCcgZmlsbD0nd2hpdGUnIGZvbnQtd2VpZ2h0PSc3MDAnPgogICAgQ29uZmlkZW5jZQogIDwvdGV4dD4KICA8dGV4dCB4PSc1MCUnIHk9JzU4JScgZG9taW5hbnQtYmFzZWxpbmU9J21pZGRsZScgdGV4dC1hbmNob3I9J21pZGRsZScKICAgICAgICBmb250LWZhbWlseT0nTnVuaXRvLCBIZWx2ZXRpY2EsIEFyaWFsJyBmb250LXNpemU9JzI4JyBmaWxsPSdyZ2JhKDI1NSwyNTUsMjU1LDAuOTIpJz4KICAgIEZlZWwgdGhlIGNoYW5nZQogIDwvdGV4dD4KPC9zdmc+",
    "alt": "Confidence \u2013 Feel the change",
    "headline": "Start Strong",
    "message": "Document day-one stats and set a confident baseline."
  },
  {
    "src": "data:image/svg+xml;base64,CjxzdmcgeG1sbnM9J2h0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnJyB3aWR0aD0nNjAwJyBoZWlnaHQ9JzgwMCc+CiAgPGRlZnM+CiAgICA8bGluZWFyR3JhZGllbnQgaWQ9J2dyYWQnIHgxPScwJScgeTE9JzAlJyB4Mj0nMCUnIHkyPScxMDAlJz4KICAgICAgPHN0b3Agb2Zmc2V0PScwJScgc3RvcC1jb2xvcj0nIzIyQzU1RScvPgogICAgICA8c3RvcCBvZmZzZXQ9JzEwMCUnIHN0b3AtY29sb3I9JyMxNkEzNEEnLz4KICAgIDwvbGluZWFyR3JhZGllbnQ+CiAgPC9kZWZzPgogIDxyZWN0IHdpZHRoPSc2MDAnIGhlaWdodD0nODAwJyByeD0nNDgnIGZpbGw9J3VybCgjZ3JhZCknLz4KICA8dGV4dCB4PSc1MCUnIHk9JzQ1JScgZG9taW5hbnQtYmFzZWxpbmU9J21pZGRsZScgdGV4dC1hbmNob3I9J21pZGRsZScKICAgICAgICBmb250LWZhbWlseT0nUG9wcGlucywgSGVsdmV0aWNhLCBBcmlhbCcgZm9udC1zaXplPSc0OCcgZmlsbD0nd2hpdGUnIGZvbnQtd2VpZ2h0PSc3MDAnPgogICAgTmV4dCBNaWxlc3RvbmUKICA8L3RleHQ+CiAgPHRleHQgeD0nNTAlJyB5PSc1OCUnIGRvbWluYW50LWJhc2VsaW5lPSdtaWRkbGUnIHRleHQtYW5jaG9yPSdtaWRkbGUnCiAgICAgICAgZm9udC1mYW1pbHk9J051bml0bywgSGVsdmV0aWNhLCBBcmlhbCcgZm9udC1zaXplPScyOCcgZmlsbD0ncmdiYSgyNTUsMjU1LDI1NSwwLjkyKSc+CiAgICBZb3UgZWFybmVkIGl0CiAgPC90ZXh0Pgo8L3N2Zz4=",
    "alt": "Next Milestone \u2013 You earned it",
    "headline": "Stay Consistent",
    "message": "Celebrate habit streaks and incremental wins."
  }
];

  useEffect(() => {
    const interval = setInterval(() => {
      setIsTransitioning(true);
      setTimeout(() => {
        setCurrentFrame((prev) => (prev + 1) % frames.length);
        setIsTransitioning(false);
      }, 400);
    }, 3600);

    return () => clearInterval(interval);
  }, [frames.length]);

  const gradient = `linear-gradient(135deg,
    rgba(220,38,38,0.85) 0%,
    rgba(59,130,246,0.85) 45%,
    rgba(34,197,94,0.9) 100%
  )`;

  return (
    <div className="splash-container" style={{ background: gradient }}>
      <div className="splash-content">
        <div className="hero-visual">
          <div className={`image-frame ${isTransitioning ? 'fade-out' : 'fade-in'}`}>
            <Image
              src={frames[currentFrame].src}
              alt={frames[currentFrame].alt}
              fill
              priority
              sizes="(max-width: 768px) 90vw, 480px"
            />
          </div>
        </div>

        <div className="copy-stack">
          <h1 className="splash-title">{frames[currentFrame].headline}</h1>
          <p className="splash-subtitle">{frames[currentFrame].message}</p>


          <div className="splash-actions">
            <PillButton variant="primary" onClick={onCreateProfile}>
              Create Profile
            </PillButton>
            <PillButton variant="secondary" onClick={onLogin}>
              Log In
            </PillButton>
          </div>
        </div>
      </div>

      <style jsx>{`
        .splash-container {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          position: relative;
          overflow: hidden;
          color: #f8fafc;
        }

        .splash-content {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 3rem;
          align-items: center;
          width: min(1080px, 100%);
        }

        .hero-visual {
          position: relative;
          width: 100%;
          aspect-ratio: 3 / 4;
          border-radius: 32px;
          overflow: hidden;
          box-shadow: 0 45px 70px rgba(15, 23, 42, 0.28);
          isolation: isolate;
        }

        .image-frame {
          position: absolute;
          inset: 0;
          transition: opacity 0.4s ease;
        }

        .image-frame :global(img) {
          object-fit: cover;
        }

        .fade-in {
          opacity: 1;
        }

        .fade-out {
          opacity: 0;
        }

        .copy-stack {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .splash-title {
          font-size: clamp(2.5rem, 4vw, 3.5rem);
          font-weight: 700;
          letter-spacing: -0.03em;
          margin: 0;
        }

        .splash-subtitle {
          font-size: clamp(1.1rem, 2.2vw, 1.4rem);
          line-height: 1.6;
          opacity: 0.92;
          margin: 0;
        }


        .splash-actions {
          display: flex;
          gap: 1rem;
          flex-wrap: wrap;
        }

        :global(.pill-button) {
          min-width: 160px;
          justify-content: center;
        }

        @media (max-width: 900px) {
          .splash-content {
            grid-template-columns: 1fr;
            text-align: center;
          }

          .copy-stack {
            align-items: center;
          }

          .splash-actions {
            justify-content: center;
          }
        }
      `}</style>
    </div>
  );
};
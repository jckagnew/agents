import React, { useState, useEffect } from 'react';
import Image from 'next/image';

interface SplashScreen3Props {
  onGetStarted: () => void;
  onLogin: () => void;
}

const SplashScreen3: React.FC<SplashScreen3Props> = ({ onGetStarted, onLogin }) => {
  const [currentImage, setCurrentImage] = useState(0);
  const [isAnimating, setIsAnimating] = useState(false);

  const images = [
    {
      src: "https://images.pexels.com/photos/6670943/pexels-photo-6670943.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
      alt: "Before transformation",
      description: "Photo by Moe Magners - Person holding 'weight loss' sign for fitness motivation and health goals...."
    },
    {
      src: "https://images.pexels.com/photos/5622199/pexels-photo-5622199.jpeg?auto=compress&cs=tinysrgb&h=650&w=940",
      alt: "After transformation",
      description: "Photo by Gustavo Fring - Close-up image of a woman measuring her waist with a tape measure, promotin..."
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setIsAnimating(true);
      setTimeout(() => {
        setCurrentImage((prev) => (prev + 1) % images.length);
        setIsAnimating(false);
      }, 300);
    }, 3000);

    return () => clearInterval(interval);
  }, [images.length]);

  return (
    <div className="splash-screen">
      <div className="splash-background">
        <div className="image-container">
          <Image
            src={images[currentImage].src}
            alt={images[currentImage].alt}
            fill
            className={`splash-image ${isAnimating ? 'fade-out' : 'fade-in'}`}
            priority
          />
          <div className="image-overlay" />
        </div>
      </div>

      <div className="splash-content">
        <div className="splash-header">
          <h1 className="splash-title">Transform Your Life</h1>
          <h2 className="splash-subtitle">Track. Transform. Triumph.</h2>
          <p className="splash-description">Your journey starts here.</p>
        </div>

        <div className="splash-stats">
        <div className="stat-item">
          <div className="stat-value">67%</div>
          <div className="stat-label">Complete</div>
        </div>
        <div className="stat-item">
          <div className="stat-value">3</div>
          <div className="stat-label">Days to Goal</div>
        </div>
        </div>

        <div className="splash-actions">
          <button
            className="btn-primary"
            onClick={onGetStarted}
          >
            Create Profile
          </button>
          <button
            className="btn-secondary"
            onClick={onLogin}
          >
            Log In
          </button>
        </div>

        <div className="splash-footer">
          <p className="transformation-text">
            Watch your transformation unfold
          </p>
        </div>
      </div>

      <style jsx>{`{
        .splash-screen {
          position: relative;
          width: 100vw;
          height: 100vh;
          overflow: hidden;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .splash-background {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          z-index: 1;
        }

        .image-container {
          position: relative;
          width: 100%;
          height: 100%;
        }

        .splash-image {
          object-fit: cover;
          transition: opacity 0.3s ease-in-out;
        }

        .fade-in {
          opacity: 1;
        }

        .fade-out {
          opacity: 0;
        }

        .image-overlay {
          position: absolute;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background: linear-gradient(
            135deg,
            rgba(0, 0, 0, 0.7) 0%,
            rgba(0, 0, 0, 0.3) 50%,
            rgba(0, 0, 0, 0.7) 100%
          );
          z-index: 2;
        }

        .splash-content {
          position: relative;
          z-index: 3;
          text-align: center;
          color: white;
          max-width: 600px;
          padding: 2rem;
        }

        .splash-title {
          font-size: 3.5rem;
          font-weight: 800;
          margin-bottom: 1rem;
          background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .splash-subtitle {
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 1rem;
          color: #e2e8f0;
        }

        .splash-description {
          font-size: 1.1rem;
          margin-bottom: 2rem;
          color: #cbd5e0;
          line-height: 1.6;
        }

        .splash-stats {
          display: flex;
          justify-content: center;
          gap: 2rem;
          margin-bottom: 2rem;
        }

        .stat-item {
          text-align: center;
        }

        .stat-value {
          font-size: 2rem;
          font-weight: 700;
          color: #4ecdc4;
          margin-bottom: 0.5rem;
        }

        .stat-label {
          font-size: 0.9rem;
          color: #a0aec0;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .splash-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
          margin-bottom: 2rem;
        }

        .btn-primary {
          background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
          color: white;
          border: none;
          padding: 1rem 2rem;
          border-radius: 50px;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: transform 0.2s ease;
        }

        .btn-primary:hover {
          transform: translateY(-2px);
        }

        .btn-secondary {
          background: transparent;
          color: white;
          border: 2px solid white;
          padding: 1rem 2rem;
          border-radius: 50px;
          font-size: 1.1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .btn-secondary:hover {
          background: white;
          color: #1a202c;
        }

        .splash-footer {
          margin-top: 2rem;
        }

        .transformation-text {
          font-size: 0.9rem;
          color: #a0aec0;
          font-style: italic;
        }

        @media (max-width: 768px) {
          .splash-title {
            font-size: 2.5rem;
          }

          .splash-subtitle {
            font-size: 1.2rem;
          }

          .splash-stats {
            flex-direction: column;
            gap: 1rem;
          }

          .splash-actions {
            flex-direction: column;
            align-items: center;
          }
        }
      `}</style>
    </div>
  );
};

export default SplashScreen3;
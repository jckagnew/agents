'use client';

import React from 'react';
import { PillButton, LayoutContainer } from './design-system';

interface SplashScreenProps {
  onContinue?: () => void;
}

export function SplashScreen({ onContinue }: SplashScreenProps) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-blue-700 to-indigo-800">
      {/* Hero Section */}
      <section className="py-16 md:py-24 text-white">
        <LayoutContainer>
          <div className="text-center max-w-4xl mx-auto">
            {/* Hero Emoji */}
            <div className="mb-8">
              <div className="text-8xl md:text-9xl mb-6 animate-bounce inline-block">
                ⚖️
              </div>
              <p className="text-sm md:text-base text-blue-200">Transforming...</p>
            </div>

            {/* Headline */}
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6 leading-tight">
              Transform Your Life,<br />
              <span className="text-yellow-300">One Weigh-In at a Time</span>
            </h1>

            {/* Subheadline */}
            <p className="text-xl md:text-2xl mb-10 text-blue-100 leading-relaxed max-w-2xl mx-auto">
              Track. Transform. Triumph.
            </p>

            {/* CTA Button */}
            <div className="mb-16">
              <PillButton
                onClick={onContinue}
                variant="primary"
                className="bg-white text-blue-600 hover:bg-gray-100 text-lg font-semibold px-10 py-4 shadow-2xl"
              >
                Start Your Journey
              </PillButton>
            </div>

            {/* Feature Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-3xl mx-auto">
              {[
                { icon: '📊', title: 'Track Progress', desc: 'Monitor your journey' },
                { icon: '🎯', title: 'Set Goals', desc: 'Define your targets' },
                { icon: '🏆', title: 'Achieve Success', desc: 'Reach your peak' },
              ].map((feature, idx) => (
                <div
                  key={idx}
                  className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:bg-white/20 transition-colors"
                >
                  <div className="text-4xl mb-3">{feature.icon}</div>
                  <h3 className="font-bold text-lg mb-2">{feature.title}</h3>
                  <p className="text-sm text-blue-200">{feature.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </LayoutContainer>
      </section>

      {/* Testimonials Section */}
      <section className="py-12 bg-white/5 backdrop-blur-sm">
        <LayoutContainer>
          <div className="max-w-3xl mx-auto">
            <h2 className="text-2xl font-bold text-center text-white mb-8">What Users Say</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {[
                { quote: 'This app changed my life!', author: 'Sarah M.' },
                { quote: 'Simple, effective, powerful.', author: 'John D.' },
              ].map((testimonial, idx) => (
                <div
                  key={idx}
                  className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20"
                >
                  <p className="text-white/90 mb-3">&ldquo;{testimonial.quote}&rdquo;</p>
                  <p className="text-sm text-blue-200">— {testimonial.author}</p>
                </div>
              ))}
            </div>
          </div>
        </LayoutContainer>
      </section>

      {/* Footer */}
      <footer className="py-8 bg-black/20 text-center text-sm text-blue-200">
        <LayoutContainer>
          <p>&copy; 2025 Weight Tracker. Your journey starts here.</p>
        </LayoutContainer>
      </footer>
    </div>
  );
}

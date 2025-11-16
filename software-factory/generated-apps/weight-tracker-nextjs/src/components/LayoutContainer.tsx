'use client';

import React, { ReactNode } from 'react';

interface LayoutContainerProps {
  children: ReactNode;
  fullWidth?: boolean;
  className?: string;
}

/**
 * LayoutContainer - Provides consistent layout constraints across all screens
 * - Max-width: 1200px for optimal readability
 * - Uniform padding: 24-32px
 * - Proper vertical spacing
 * - Centered content
 */
export function LayoutContainer({ 
  children, 
  fullWidth = false, 
  className = '' 
}: LayoutContainerProps) {
  return (
    <div 
      className={`w-full ${
        fullWidth ? '' : 'max-w-screen-xl'
      } mx-auto px-6 sm:px-8 lg:px-12 ${className}`}
    >
      {children}
    </div>
  );
}

/**
 * Section - Provides consistent vertical spacing between content sections
 */
export function Section({ 
  children, 
  className = '' 
}: { 
  children: ReactNode; 
  className?: string;
}) {
  return (
    <section className={`mb-8 sm:mb-12 lg:mb-16 ${className}`}>
      {children}
    </section>
  );
}

/**
 * ContentGrid - Responsive grid layout for dashboard content
 */
export function ContentGrid({ 
  children,
  className = ''
}: { 
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 ${className}`}>
      {children}
    </div>
  );
}

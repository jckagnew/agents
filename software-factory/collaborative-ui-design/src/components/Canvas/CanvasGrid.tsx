import React from 'react';

interface CanvasGridProps {
  enabled: boolean;
  size: number;
}

export const CanvasGrid: React.FC<CanvasGridProps> = ({ enabled, size }) => {
  if (!enabled) return null;

  return (
    <div
      className="canvas-grid"
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        pointerEvents: 'none',
        backgroundImage: `
          linear-gradient(to right, #e5e7eb 1px, transparent 1px),
          linear-gradient(to bottom, #e5e7eb 1px, transparent 1px)
        `,
        backgroundSize: `${size}px ${size}px`,
        zIndex: 1,
      }}
    />
  );
};

export default CanvasGrid;

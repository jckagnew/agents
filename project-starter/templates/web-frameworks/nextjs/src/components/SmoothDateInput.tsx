/**
 * Smooth Date Input Component - Web Version (Next.js)
 * Non-jumpy date input with US format validation
 * 
 * Usage:
 * import SmoothDateInput from '@/components/SmoothDateInput';
 * 
 * <SmoothDateInput
 *   value={date}
 *   onChangeText={setDate}
 *   placeholder="MM/DD/YYYY"
 *   error={errors.date}
 * />
 */

'use client';

import React, { useState, useRef, useEffect } from 'react';

interface SmoothDateInputProps {
  value: string;
  onChangeText: (value: string) => void;
  placeholder?: string;
  error?: string;
  onFocus?: () => void;
  onBlur?: () => void;
  className?: string;
}

export default function SmoothDateInput({
  value,
  onChangeText,
  placeholder = 'MM/DD/YYYY',
  error,
  onFocus,
  onBlur,
  className = '',
}: SmoothDateInputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [displayValue, setDisplayValue] = useState(value);

  useEffect(() => {
    setDisplayValue(value);
  }, [value]);

  const handleFocus = () => {
    setIsFocused(true);
    onFocus?.();
  };

  const handleBlur = () => {
    setIsFocused(false);
    onBlur?.();
  };

  const handleTextChange = (text: string) => {
    // Auto-format as user types
    let formatted = text.replace(/\D/g, ''); // Remove non-digits
    
    if (formatted.length >= 2) {
      formatted = formatted.substring(0, 2) + '/' + formatted.substring(2);
    }
    if (formatted.length >= 5) {
      formatted = formatted.substring(0, 5) + '/' + formatted.substring(5, 9);
    }
    
    setDisplayValue(formatted);
    onChangeText(formatted);
  };

  const baseClasses = `
    w-full px-4 py-3 text-center text-gray-800 bg-white border-2 rounded-xl
    transition-all duration-200 ease-in-out
    focus:outline-none focus:ring-0
    ${error 
      ? 'border-red-500 focus:border-red-500' 
      : isFocused 
        ? 'border-blue-500 shadow-lg shadow-blue-500/20' 
        : 'border-gray-200 hover:border-gray-300'
    }
  `;

  return (
    <div className={className}>
      <input
        type="text"
        value={displayValue}
        onChange={(e) => handleTextChange(e.target.value)}
        placeholder={placeholder}
        maxLength={10}
        onFocus={handleFocus}
        onBlur={handleBlur}
        className={baseClasses}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}

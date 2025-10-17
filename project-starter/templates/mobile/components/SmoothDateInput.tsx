/**
 * Smooth Date Input Component - Project Starter Template
 * Non-jumpy date input with US format validation
 * 
 * Usage:
 * import SmoothDateInput from './components/SmoothDateInput';
 * 
 * <SmoothDateInput
 *   value={date}
 *   onChangeText={setDate}
 *   placeholder="MM/DD/YYYY"
 *   error={errors.date}
 * />
 */

import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  Animated,
} from 'react-native';

interface SmoothDateInputProps {
  value: string;
  onChangeText: (value: string) => void;
  placeholder?: string;
  error?: string;
  onFocus?: () => void;
  onBlur?: () => void;
  style?: any;
}

export default function SmoothDateInput({
  value,
  onChangeText,
  placeholder = 'MM/DD/YYYY',
  error,
  onFocus,
  onBlur,
  style,
}: SmoothDateInputProps) {
  const [isFocused, setIsFocused] = useState(false);
  const [displayValue, setDisplayValue] = useState(value);
  const animatedValue = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    setDisplayValue(value);
  }, [value]);

  useEffect(() => {
    Animated.timing(animatedValue, {
      toValue: isFocused ? 1 : 0,
      duration: 200,
      useNativeDriver: false,
    }).start();
  }, [isFocused]);

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

  const borderColor = animatedValue.interpolate({
    inputRange: [0, 1],
    outputRange: [error ? '#dc3545' : '#e2e8f0', error ? '#dc3545' : '#667eea'],
  });

  const shadowOpacity = animatedValue.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 0.2],
  });

  return (
    <View style={style}>
      <Animated.View
        style={[
          styles.inputContainer,
          {
            borderColor,
            shadowOpacity,
          },
        ]}
      >
        <TextInput
          style={styles.input}
          value={displayValue}
          onChangeText={handleTextChange}
          placeholder={placeholder}
          keyboardType="numeric"
          maxLength={10}
          returnKeyType="next"
          blurOnSubmit={false}
          selectTextOnFocus={true}
          clearButtonMode="while-editing"
          onFocus={handleFocus}
          onBlur={handleBlur}
        />
      </Animated.View>
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
}

const styles = StyleSheet.create({
  inputContainer: {
    backgroundColor: '#fff',
    borderWidth: 2,
    borderRadius: 12,
    padding: 16,
    minHeight: 50,
    shadowColor: '#667eea',
    shadowOffset: { width: 0, height: 0 },
    shadowRadius: 4,
    elevation: 2,
  },
  input: {
    fontSize: 16,
    color: '#2d3748',
    textAlign: 'center',
    padding: 0,
  },
  errorText: {
    color: '#dc3545',
    fontSize: 14,
    marginTop: 4,
  },
});

import { useState, useEffect } from 'react';
import { Alert } from 'react-native';

interface ErrorHandlerOptions {
  showAlert?: boolean;
  logToConsole?: boolean;
  customMessage?: string;
}

export function useErrorHandler() {
  const [error, setError] = useState<Error | null>(null);

  const handleError = (
    error: any,
    options: ErrorHandlerOptions = {}
  ) => {
    const {
      showAlert = true,
      logToConsole = true,
      customMessage,
    } = options;

    const errorMessage = customMessage || error?.message || 'An unexpected error occurred';

    if (logToConsole) {
      console.error('Error:', error);
    }

    setError(error);

    if (showAlert) {
      Alert.alert('Error', errorMessage, [
        { text: 'OK', onPress: () => setError(null) },
      ]);
    }

    // TODO: Log to error tracking service
    // logErrorToService(error, errorMessage);
  };

  const clearError = () => setError(null);

  return { error, handleError, clearError };
}

export function getErrorMessage(error: any): string {
  // Supabase errors
  if (error?.message) {
    // Common Supabase error patterns
    if (error.message.includes('duplicate key')) {
      return 'This record already exists';
    }
    if (error.message.includes('foreign key')) {
      return 'Cannot delete - this record is being used';
    }
    if (error.message.includes('not found')) {
      return 'Record not found';
    }
    if (error.message.includes('permission denied')) {
      return 'You do not have permission to perform this action';
    }
    if (error.message.includes('JWT')) {
      return 'Session expired. Please sign in again';
    }
    return error.message;
  }

  // Network errors
  if (error?.code === 'NETWORK_ERROR') {
    return 'Network error. Please check your internet connection';
  }

  // Validation errors
  if (error?.code === 'VALIDATION_ERROR') {
    return 'Please check your input and try again';
  }

  return 'An unexpected error occurred. Please try again';
}

export function isNetworkError(error: any): boolean {
  return (
    error?.code === 'NETWORK_ERROR' ||
    error?.message?.includes('network') ||
    error?.message?.includes('fetch')
  );
}

export function isAuthError(error: any): boolean {
  return (
    error?.message?.includes('JWT') ||
    error?.message?.includes('auth') ||
    error?.message?.includes('permission')
  );
}

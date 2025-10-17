import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Animated,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { Audio } from 'expo-av';
import * as Speech from 'expo-speech';
import { Ionicons } from '@expo/vector-icons';

interface WorkoutData {
  exercise: string;
  sets: number;
  reps: number;
  weight?: number;
  unit: string;
  duration?: number;
  distance?: number;
  rest_time?: number;
  notes?: string;
  timestamp: Date;
  confidence: number;
}

interface VoiceWorkoutLoggerProps {
  onWorkoutLogged: (workout: WorkoutData) => void;
  onError: (error: string) => void;
}

const VoiceWorkoutLogger: React.FC<VoiceWorkoutLoggerProps> = ({
  onWorkoutLogged,
  onError,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recording, setRecording] = useState<Audio.Recording | null>(null);
  const [permissionResponse, requestPermission] = Audio.usePermissions();
  const [transcription, setTranscription] = useState<string>('');
  const [workoutData, setWorkoutData] = useState<WorkoutData | null>(null);
  
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const waveAnim = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    // Request microphone permission on mount
    if (!permissionResponse?.granted) {
      requestPermission();
    }
  }, []);

  useEffect(() => {
    // Start pulse animation when recording
    if (isRecording) {
      startPulseAnimation();
      startWaveAnimation();
    } else {
      stopAnimations();
    }
  }, [isRecording]);

  const startPulseAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.2,
          duration: 800,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 800,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const startWaveAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(waveAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(waveAnim, {
          toValue: 0,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  const stopAnimations = () => {
    pulseAnim.stopAnimation();
    waveAnim.stopAnimation();
    pulseAnim.setValue(1);
    waveAnim.setValue(0);
  };

  const startRecording = async () => {
    try {
      if (permissionResponse?.status !== 'granted') {
        Alert.alert('Permission Required', 'Microphone permission is required to record workouts.');
        return;
      }

      // Configure audio recording
      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
        shouldDuckAndroid: true,
        playThroughEarpieceAndroid: false,
      });

      // Start recording
      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      
      setRecording(recording);
      setIsRecording(true);
      setTranscription('');
      setWorkoutData(null);

    } catch (error) {
      console.error('Failed to start recording:', error);
      onError('Failed to start recording. Please try again.');
    }
  };

  const stopRecording = async () => {
    try {
      if (!recording) return;

      setIsRecording(false);
      await recording.stopAndUnloadAsync();
      
      // Get the URI of the recorded audio
      const uri = recording.getURI();
      if (uri) {
        await processAudio(uri);
      }
      
      setRecording(null);
    } catch (error) {
      console.error('Failed to stop recording:', error);
      onError('Failed to stop recording. Please try again.');
    }
  };

  const processAudio = async (audioUri: string) => {
    setIsProcessing(true);
    
    try {
      // Send audio to backend for processing
      const formData = new FormData();
      formData.append('audio', {
        uri: audioUri,
        type: 'audio/m4a',
        name: 'workout_audio.m4a',
      } as any);

      const response = await fetch('/api/process-workout-audio', {
        method: 'POST',
        body: formData,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to process audio');
      }

      const result = await response.json();
      
      setTranscription(result.transcription);
      setWorkoutData(result.workoutData);
      
      // Speak the transcription back to user
      if (result.transcription) {
        Speech.speak(`I heard: ${result.transcription}`, {
          language: 'en-US',
          pitch: 1.0,
          rate: 0.8,
        });
      }

    } catch (error) {
      console.error('Failed to process audio:', error);
      onError('Failed to process your workout. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const confirmWorkout = () => {
    if (workoutData) {
      onWorkoutLogged(workoutData);
      setWorkoutData(null);
      setTranscription('');
    }
  };

  const retryRecording = () => {
    setTranscription('');
    setWorkoutData(null);
  };

  const getRecordingButtonStyle = () => {
    if (isRecording) {
      return [styles.recordButton, styles.recordingButton];
    }
    return styles.recordButton;
  };

  const getRecordingButtonText = () => {
    if (isProcessing) return 'Processing...';
    if (isRecording) return 'Stop Recording';
    return 'Start Recording';
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Voice Workout Logger</Text>
      <Text style={styles.subtitle}>
        Tap and hold to record your workout, then release when done.
      </Text>

      {/* Recording Button */}
      <View style={styles.recordingContainer}>
        <Animated.View
          style={[
            styles.recordingButtonContainer,
            {
              transform: [{ scale: pulseAnim }],
            },
          ]}
        >
          <TouchableOpacity
            style={getRecordingButtonStyle()}
            onPressIn={startRecording}
            onPressOut={stopRecording}
            disabled={isProcessing}
          >
            <Ionicons
              name={isRecording ? 'stop' : 'mic'}
              size={40}
              color="white"
            />
          </TouchableOpacity>
        </Animated.View>

        {/* Wave Animation */}
        {isRecording && (
          <View style={styles.waveContainer}>
            {[...Array(5)].map((_, index) => (
              <Animated.View
                key={index}
                style={[
                  styles.waveBar,
                  {
                    transform: [
                      {
                        scaleY: waveAnim.interpolate({
                          inputRange: [0, 1],
                          outputRange: [0.3, 1.0],
                        }),
                      },
                    ],
                    opacity: waveAnim.interpolate({
                      inputRange: [0, 1],
                      outputRange: [0.3, 1.0],
                    }),
                  },
                ]}
              />
            ))}
          </View>
        )}
      </View>

      {/* Processing Indicator */}
      {isProcessing && (
        <View style={styles.processingContainer}>
          <ActivityIndicator size="large" color="#007AFF" />
          <Text style={styles.processingText}>
            Processing your workout...
          </Text>
        </View>
      )}

      {/* Transcription Display */}
      {transcription && (
        <View style={styles.transcriptionContainer}>
          <Text style={styles.transcriptionLabel}>What I heard:</Text>
          <Text style={styles.transcriptionText}>{transcription}</Text>
        </View>
      )}

      {/* Workout Data Display */}
      {workoutData && (
        <View style={styles.workoutDataContainer}>
          <Text style={styles.workoutDataLabel}>Extracted Workout:</Text>
          <View style={styles.workoutDataItem}>
            <Text style={styles.workoutDataKey}>Exercise:</Text>
            <Text style={styles.workoutDataValue}>{workoutData.exercise}</Text>
          </View>
          <View style={styles.workoutDataItem}>
            <Text style={styles.workoutDataKey}>Sets:</Text>
            <Text style={styles.workoutDataValue}>{workoutData.sets}</Text>
          </View>
          <View style={styles.workoutDataItem}>
            <Text style={styles.workoutDataKey}>Reps:</Text>
            <Text style={styles.workoutDataValue}>{workoutData.reps}</Text>
          </View>
          {workoutData.weight && (
            <View style={styles.workoutDataItem}>
              <Text style={styles.workoutDataKey}>Weight:</Text>
              <Text style={styles.workoutDataValue}>
                {workoutData.weight} {workoutData.unit}
              </Text>
            </View>
          )}
          <View style={styles.workoutDataItem}>
            <Text style={styles.workoutDataKey}>Confidence:</Text>
            <Text style={styles.workoutDataValue}>
              {Math.round(workoutData.confidence * 100)}%
            </Text>
          </View>

          {/* Action Buttons */}
          <View style={styles.actionButtons}>
            <TouchableOpacity
              style={[styles.actionButton, styles.retryButton]}
              onPress={retryRecording}
            >
              <Text style={styles.retryButtonText}>Retry</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={[styles.actionButton, styles.confirmButton]}
              onPress={confirmWorkout}
            >
              <Text style={styles.confirmButtonText}>Confirm</Text>
            </TouchableOpacity>
          </View>
        </View>
      )}

      {/* Instructions */}
      <View style={styles.instructionsContainer}>
        <Text style={styles.instructionsTitle}>How to use:</Text>
        <Text style={styles.instructionText}>
          • Say your workout in natural language
        </Text>
        <Text style={styles.instructionText}>
          • Example: "I did 3 sets of 10 reps of bench press at 135 pounds"
        </Text>
        <Text style={styles.instructionText}>
          • The AI will extract and structure your data
        </Text>
        <Text style={styles.instructionText}>
          • Review and confirm before saving
        </Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f8f9fa',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: 8,
    color: '#1a1a1a',
  },
  subtitle: {
    fontSize: 16,
    textAlign: 'center',
    marginBottom: 40,
    color: '#666',
    lineHeight: 22,
  },
  recordingContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  recordingButtonContainer: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  recordButton: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#007AFF',
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 4,
  },
  recordingButton: {
    backgroundColor: '#FF3B30',
  },
  waveContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 20,
    height: 40,
  },
  waveBar: {
    width: 4,
    height: 20,
    backgroundColor: '#007AFF',
    marginHorizontal: 2,
    borderRadius: 2,
  },
  processingContainer: {
    alignItems: 'center',
    marginBottom: 20,
  },
  processingText: {
    marginTop: 10,
    fontSize: 16,
    color: '#666',
  },
  transcriptionContainer: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  transcriptionLabel: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#1a1a1a',
  },
  transcriptionText: {
    fontSize: 16,
    color: '#333',
    lineHeight: 22,
  },
  workoutDataContainer: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    marginBottom: 20,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  workoutDataLabel: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 12,
    color: '#1a1a1a',
  },
  workoutDataItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  workoutDataKey: {
    fontSize: 16,
    color: '#666',
    fontWeight: '500',
  },
  workoutDataValue: {
    fontSize: 16,
    color: '#1a1a1a',
    fontWeight: '600',
  },
  actionButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 16,
  },
  actionButton: {
    flex: 1,
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    marginHorizontal: 8,
  },
  retryButton: {
    backgroundColor: '#f0f0f0',
    borderWidth: 1,
    borderColor: '#ddd',
  },
  retryButtonText: {
    textAlign: 'center',
    fontSize: 16,
    fontWeight: '600',
    color: '#666',
  },
  confirmButton: {
    backgroundColor: '#34C759',
  },
  confirmButtonText: {
    textAlign: 'center',
    fontSize: 16,
    fontWeight: '600',
    color: 'white',
  },
  instructionsContainer: {
    backgroundColor: 'white',
    padding: 16,
    borderRadius: 12,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  instructionsTitle: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 8,
    color: '#1a1a1a',
  },
  instructionText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 4,
    lineHeight: 20,
  },
});

export default VoiceWorkoutLogger;


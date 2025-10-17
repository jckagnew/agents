import { Platform } from 'react-native';
import Voice, { SpeechResultsEvent, SpeechErrorEvent } from '@react-native-voice/voice';
import { Audio } from 'expo-av';

export interface WorkoutData {
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

export interface VoiceProcessingResult {
  transcription: string;
  workoutData: WorkoutData | null;
  confidence: number;
  error?: string;
}

class VoiceProcessingService {
  private isInitialized = false;
  private isRecording = false;
  private onResultsCallback?: (result: VoiceProcessingResult) => void;
  private onErrorCallback?: (error: string) => void;

  async initialize(): Promise<boolean> {
    try {
      if (Platform.OS === 'ios') {
        // Request microphone permission for iOS
        const { status } = await Audio.requestPermissionsAsync();
        if (status !== 'granted') {
          throw new Error('Microphone permission not granted');
        }
      }

      // Initialize Voice recognition
      Voice.onSpeechStart = this.onSpeechStart;
      Voice.onSpeechEnd = this.onSpeechEnd;
      Voice.onSpeechResults = this.onSpeechResults;
      Voice.onSpeechError = this.onSpeechError;

      this.isInitialized = true;
      return true;
    } catch (error) {
      console.error('Failed to initialize voice processing service:', error);
      return false;
    }
  }

  private onSpeechStart = () => {
    console.log('Speech recognition started');
  };

  private onSpeechEnd = () => {
    console.log('Speech recognition ended');
    this.isRecording = false;
  };

  private onSpeechResults = (e: SpeechResultsEvent) => {
    if (e.value && e.value.length > 0) {
      const transcription = e.value[0];
      console.log('Speech results:', transcription);
      
      // Process the transcription
      this.processTranscription(transcription);
    }
  };

  private onSpeechError = (e: SpeechErrorEvent) => {
    console.error('Speech recognition error:', e.error);
    this.isRecording = false;
    
    if (this.onErrorCallback) {
      this.onErrorCallback(e.error?.message || 'Speech recognition failed');
    }
  };

  async startListening(): Promise<boolean> {
    if (!this.isInitialized) {
      throw new Error('Voice processing service not initialized');
    }

    if (this.isRecording) {
      return false;
    }

    try {
      await Voice.start('en-US');
      this.isRecording = true;
      return true;
    } catch (error) {
      console.error('Failed to start listening:', error);
      if (this.onErrorCallback) {
        this.onErrorCallback('Failed to start voice recognition');
      }
      return false;
    }
  }

  async stopListening(): Promise<void> {
    if (!this.isRecording) {
      return;
    }

    try {
      await Voice.stop();
      this.isRecording = false;
    } catch (error) {
      console.error('Failed to stop listening:', error);
    }
  }

  async cancelListening(): Promise<void> {
    try {
      await Voice.cancel();
      this.isRecording = false;
    } catch (error) {
      console.error('Failed to cancel listening:', error);
    }
  }

  setOnResults(callback: (result: VoiceProcessingResult) => void): void {
    this.onResultsCallback = callback;
  }

  setOnError(callback: (error: string) => void): void {
    this.onErrorCallback = callback;
  }

  private async processTranscription(transcription: string): Promise<void> {
    try {
      // Send transcription to backend for AI processing
      const response = await fetch('/api/process-workout-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: transcription,
          user_id: 'current_user', // This would come from auth context
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to process transcription');
      }

      const result = await response.json();
      
      const voiceResult: VoiceProcessingResult = {
        transcription: transcription,
        workoutData: result.workout_data ? this.convertToWorkoutData(result.workout_data) : null,
        confidence: result.confidence || 0,
        error: result.error,
      };

      if (this.onResultsCallback) {
        this.onResultsCallback(voiceResult);
      }
    } catch (error) {
      console.error('Failed to process transcription:', error);
      
      const voiceResult: VoiceProcessingResult = {
        transcription: transcription,
        workoutData: null,
        confidence: 0,
        error: 'Failed to process workout data',
      };

      if (this.onResultsCallback) {
        this.onResultsCallback(voiceResult);
      }
    }
  }

  private convertToWorkoutData(data: any): WorkoutData {
    return {
      exercise: data.exercise || 'unknown',
      sets: data.sets || 0,
      reps: data.reps || 0,
      weight: data.weight,
      unit: data.unit || 'pounds',
      duration: data.duration,
      distance: data.distance,
      rest_time: data.rest_time,
      notes: data.notes,
      timestamp: new Date(data.timestamp || Date.now()),
      confidence: data.confidence || 0,
    };
  }

  // Local processing fallback (simplified)
  async processTextLocally(text: string): Promise<WorkoutData | null> {
    try {
      // Simple regex-based parsing as fallback
      const workoutData = this.parseWorkoutText(text);
      return workoutData;
    } catch (error) {
      console.error('Local text processing failed:', error);
      return null;
    }
  }

  private parseWorkoutText(text: string): WorkoutData | null {
    const lowerText = text.toLowerCase();
    
    // Extract sets
    const setsMatch = lowerText.match(/(\d+)\s*sets?/);
    const sets = setsMatch ? parseInt(setsMatch[1]) : 1;
    
    // Extract reps
    const repsMatch = lowerText.match(/(\d+)\s*reps?/);
    const reps = repsMatch ? parseInt(repsMatch[1]) : 0;
    
    // Extract weight
    const weightMatch = lowerText.match(/(\d+(?:\.\d+)?)\s*(pounds?|lbs?|kg|kilos?)/);
    const weight = weightMatch ? parseFloat(weightMatch[1]) : undefined;
    const unit = weightMatch ? (weightMatch[2].includes('kg') ? 'kg' : 'pounds') : 'pounds';
    
    // Extract exercise name
    let exercise = 'unknown';
    const exercisePatterns = [
      { pattern: /bench\s*press/i, name: 'bench_press' },
      { pattern: /squat/i, name: 'squat' },
      { pattern: /deadlift/i, name: 'deadlift' },
      { pattern: /pull\s*up/i, name: 'pull_up' },
      { pattern: /push\s*up/i, name: 'push_up' },
      { pattern: /running|run/i, name: 'running' },
      { pattern: /cycling|bike/i, name: 'cycling' },
    ];
    
    for (const { pattern, name } of exercisePatterns) {
      if (pattern.test(text)) {
        exercise = name;
        break;
      }
    }
    
    // Calculate confidence based on how much data we extracted
    let confidence = 0;
    if (sets > 0) confidence += 0.3;
    if (reps > 0) confidence += 0.3;
    if (weight !== undefined) confidence += 0.2;
    if (exercise !== 'unknown') confidence += 0.2;
    
    return {
      exercise,
      sets,
      reps,
      weight,
      unit,
      timestamp: new Date(),
      confidence,
    };
  }

  isRecording(): boolean {
    return this.isRecording;
  }

  isReady(): boolean {
    return this.isInitialized;
  }

  async destroy(): Promise<void> {
    try {
      await Voice.destroy();
      this.isInitialized = false;
      this.isRecording = false;
    } catch (error) {
      console.error('Failed to destroy voice service:', error);
    }
  }
}

export default new VoiceProcessingService();


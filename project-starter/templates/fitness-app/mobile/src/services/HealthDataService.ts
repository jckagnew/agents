import { Platform } from 'react-native';
import { GoogleFit } from 'react-native-google-fit';
import { HealthConnect } from 'react-native-health-connect';

export interface HealthData {
  steps: number;
  calories: number;
  distance: number;
  heartRate: number;
  sleepHours: number;
  weight: number;
  height: number;
  bmi: number;
  activeMinutes: number;
  timestamp: Date;
}

export interface WorkoutData {
  id: string;
  type: string;
  startTime: Date;
  endTime: Date;
  calories: number;
  distance?: number;
  heartRate?: number;
  steps?: number;
}

class HealthDataService {
  private isInitialized = false;
  private isGoogleFitConnected = false;
  private isHealthConnectConnected = false;

  async initialize(): Promise<boolean> {
    try {
      if (Platform.OS === 'android') {
        // Initialize Google Fit
        await this.initializeGoogleFit();
        
        // Initialize Health Connect
        await this.initializeHealthConnect();
      } else if (Platform.OS === 'ios') {
        // Initialize HealthKit
        await this.initializeHealthKit();
      }
      
      this.isInitialized = true;
      return true;
    } catch (error) {
      console.error('Failed to initialize health data service:', error);
      return false;
    }
  }

  private async initializeGoogleFit(): Promise<void> {
    try {
      const options = {
        scopes: [
          'https://www.googleapis.com/auth/fitness.activity.read',
          'https://www.googleapis.com/auth/fitness.body.read',
          'https://www.googleapis.com/auth/fitness.location.read',
        ],
      };
      
      const authResult = await GoogleFit.authorize(options);
      this.isGoogleFitConnected = authResult.success;
      
      if (!this.isGoogleFitConnected) {
        throw new Error('Google Fit authorization failed');
      }
    } catch (error) {
      console.error('Google Fit initialization failed:', error);
      throw error;
    }
  }

  private async initializeHealthConnect(): Promise<void> {
    try {
      const isAvailable = await HealthConnect.isHealthConnectAvailable();
      if (!isAvailable) {
        throw new Error('Health Connect not available');
      }

      const permissions = [
        'steps',
        'active_calories_burned',
        'distance',
        'heart_rate',
        'sleep_session',
        'weight',
        'height',
      ];

      const granted = await HealthConnect.requestPermissions(permissions);
      this.isHealthConnectConnected = granted;
      
      if (!this.isHealthConnectConnected) {
        throw new Error('Health Connect permissions not granted');
      }
    } catch (error) {
      console.error('Health Connect initialization failed:', error);
      throw error;
    }
  }

  private async initializeHealthKit(): Promise<void> {
    try {
      // HealthKit initialization would go here
      // This would use react-native-health or similar library
      console.log('HealthKit initialization (iOS)');
    } catch (error) {
      console.error('HealthKit initialization failed:', error);
      throw error;
    }
  }

  async getTodayHealthData(): Promise<HealthData | null> {
    if (!this.isInitialized) {
      throw new Error('Health data service not initialized');
    }

    try {
      if (Platform.OS === 'android') {
        return await this.getAndroidHealthData();
      } else if (Platform.OS === 'ios') {
        return await this.getIOSHealthData();
      }
      
      return null;
    } catch (error) {
      console.error('Failed to get health data:', error);
      return null;
    }
  }

  private async getAndroidHealthData(): Promise<HealthData> {
    const today = new Date();
    const startOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate());
    const endOfDay = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 1);

    // Get data from Google Fit
    const stepsData = await GoogleFit.getDailySteps({
      startDate: startOfDay.toISOString(),
      endDate: endOfDay.toISOString(),
    });

    const caloriesData = await GoogleFit.getDailyCalories({
      startDate: startOfDay.toISOString(),
      endDate: endOfDay.toISOString(),
    });

    const distanceData = await GoogleFit.getDailyDistance({
      startDate: startOfDay.toISOString(),
      endDate: endOfDay.toISOString(),
    });

    // Get data from Health Connect
    const heartRateData = await HealthConnect.getHeartRate(startOfDay, endOfDay);
    const sleepData = await HealthConnect.getSleepSessions(startOfDay, endOfDay);
    const weightData = await HealthConnect.getWeight(startOfDay, endOfDay);
    const heightData = await HealthConnect.getHeight(startOfDay, endOfDay);

    const steps = stepsData.steps?.[0]?.value || 0;
    const calories = caloriesData.calories?.[0]?.value || 0;
    const distance = distanceData.distance?.[0]?.value || 0;
    const heartRate = heartRateData.length > 0 ? heartRateData[0].beatsPerMinute : 0;
    const sleepHours = sleepData.length > 0 ? sleepData[0].duration / (1000 * 60 * 60) : 0;
    const weight = weightData.length > 0 ? weightData[0].weight : 0;
    const height = heightData.length > 0 ? heightData[0].height : 0;
    const bmi = weight > 0 && height > 0 ? weight / (height * height) : 0;

    return {
      steps,
      calories,
      distance,
      heartRate,
      sleepHours,
      weight,
      height,
      bmi,
      activeMinutes: 0, // Calculate from activity data
      timestamp: today,
    };
  }

  private async getIOSHealthData(): Promise<HealthData> {
    // HealthKit data retrieval would go here
    // This is a mock implementation
    return {
      steps: 0,
      calories: 0,
      distance: 0,
      heartRate: 0,
      sleepHours: 0,
      weight: 0,
      height: 0,
      bmi: 0,
      activeMinutes: 0,
      timestamp: new Date(),
    };
  }

  async getWorkoutHistory(days: number = 30): Promise<WorkoutData[]> {
    if (!this.isInitialized) {
      throw new Error('Health data service not initialized');
    }

    try {
      if (Platform.OS === 'android') {
        return await this.getAndroidWorkoutHistory(days);
      } else if (Platform.OS === 'ios') {
        return await this.getIOSWorkoutHistory(days);
      }
      
      return [];
    } catch (error) {
      console.error('Failed to get workout history:', error);
      return [];
    }
  }

  private async getAndroidWorkoutHistory(days: number): Promise<WorkoutData[]> {
    const endDate = new Date();
    const startDate = new Date(endDate.getTime() - days * 24 * 60 * 60 * 1000);

    try {
      const workoutData = await GoogleFit.getSamples({
        startDate: startDate.toISOString(),
        endDate: endDate.toISOString(),
        bucketUnit: 'DAY',
        bucketInterval: 1,
      });

      return workoutData.map((workout: any) => ({
        id: workout.id || Math.random().toString(),
        type: workout.activityType || 'unknown',
        startTime: new Date(workout.startTime),
        endTime: new Date(workout.endTime),
        calories: workout.calories || 0,
        distance: workout.distance || 0,
        heartRate: workout.heartRate || 0,
        steps: workout.steps || 0,
      }));
    } catch (error) {
      console.error('Failed to get Android workout history:', error);
      return [];
    }
  }

  private async getIOSWorkoutHistory(days: number): Promise<WorkoutData[]> {
    // HealthKit workout history retrieval would go here
    // This is a mock implementation
    return [];
  }

  async syncWorkoutData(workoutData: WorkoutData): Promise<boolean> {
    if (!this.isInitialized) {
      throw new Error('Health data service not initialized');
    }

    try {
      if (Platform.OS === 'android') {
        return await this.syncToAndroid(workoutData);
      } else if (Platform.OS === 'ios') {
        return await this.syncToIOS(workoutData);
      }
      
      return false;
    } catch (error) {
      console.error('Failed to sync workout data:', error);
      return false;
    }
  }

  private async syncToAndroid(workoutData: WorkoutData): Promise<boolean> {
    try {
      // Sync to Google Fit
      if (this.isGoogleFitConnected) {
        await GoogleFit.saveWorkout({
          activityType: workoutData.type,
          startTime: workoutData.startTime.toISOString(),
          endTime: workoutData.endTime.toISOString(),
          calories: workoutData.calories,
          distance: workoutData.distance,
        });
      }

      // Sync to Health Connect
      if (this.isHealthConnectConnected) {
        await HealthConnect.insertWorkout({
          startTime: workoutData.startTime,
          endTime: workoutData.endTime,
          activityType: workoutData.type,
          calories: workoutData.calories,
          distance: workoutData.distance,
        });
      }

      return true;
    } catch (error) {
      console.error('Failed to sync to Android:', error);
      return false;
    }
  }

  private async syncToIOS(workoutData: WorkoutData): Promise<boolean> {
    try {
      // HealthKit sync would go here
      console.log('Syncing to HealthKit:', workoutData);
      return true;
    } catch (error) {
      console.error('Failed to sync to iOS:', error);
      return false;
    }
  }

  isConnected(): boolean {
    return this.isInitialized && (this.isGoogleFitConnected || this.isHealthConnectConnected);
  }

  getConnectionStatus(): {
    initialized: boolean;
    googleFit: boolean;
    healthConnect: boolean;
    platform: string;
  } {
    return {
      initialized: this.isInitialized,
      googleFit: this.isGoogleFitConnected,
      healthConnect: this.isHealthConnectConnected,
      platform: Platform.OS,
    };
  }
}

export default new HealthDataService();


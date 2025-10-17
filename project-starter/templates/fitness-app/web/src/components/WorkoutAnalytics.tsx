import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, TrendingDown, Activity, Target, Calendar } from 'lucide-react';

interface WorkoutData {
  id: string;
  exercise: string;
  sets: number;
  reps: number;
  weight?: number;
  unit: string;
  duration?: number;
  distance?: number;
  timestamp: string;
  confidence: number;
}

interface AnalyticsData {
  consistency: {
    score: number;
    workout_days: number;
    total_days: number;
    streak: number;
    average_workouts_per_week: number;
    insights: Array<{
      type: string;
      message: string;
      confidence: number;
      actionable: boolean;
      priority: string;
    }>;
  };
  strength_progression: {
    exercise: string;
    progression_rate: number;
    total_workouts: number;
    max_weight: number;
    trend: string;
    recommendations: Array<{
      type: string;
      title: string;
      description: string;
      reasoning: string;
      priority: string;
      estimated_impact: string;
    }>;
  };
  volume_analysis: {
    total_volume: number;
    average_volume_per_workout: number;
    volume_trend: string;
    insights: Array<{
      type: string;
      message: string;
      confidence: number;
      actionable: boolean;
      priority: string;
    }>;
  };
  patterns: {
    total_workouts: number;
    favorite_exercises: Array<[string, number]>;
    workout_frequency: string;
    strength_focus: number;
    cardio_focus: number;
    patterns: string[];
  };
}

const WorkoutAnalytics: React.FC = () => {
  const [analyticsData, setAnalyticsData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [selectedPeriod, setSelectedPeriod] = useState('30d');
  const [selectedExercise, setSelectedExercise] = useState('all');

  useEffect(() => {
    fetchAnalyticsData();
  }, [selectedPeriod, selectedExercise]);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/analytics?period=${selectedPeriod}&exercise=${selectedExercise}`);
      const data = await response.json();
      setAnalyticsData(data);
    } catch (error) {
      console.error('Failed to fetch analytics data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getConsistencyColor = (score: number) => {
    if (score >= 0.8) return 'text-green-600';
    if (score >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving':
        return <TrendingUp className="h-4 w-4 text-green-600" />;
      case 'declining':
        return <TrendingDown className="h-4 w-4 text-red-600" />;
      default:
        return <Activity className="h-4 w-4 text-gray-600" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800';
      case 'low':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!analyticsData) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500">No analytics data available</p>
      </div>
    );
  }

  const { consistency, strength_progression, volume_analysis, patterns } = analyticsData;

  // Mock data for charts (in real app, this would come from the API)
  const workoutHistoryData = [
    { date: '2024-01-01', workouts: 1, volume: 1200 },
    { date: '2024-01-02', workouts: 0, volume: 0 },
    { date: '2024-01-03', workouts: 1, volume: 1500 },
    { date: '2024-01-04', workouts: 1, volume: 1800 },
    { date: '2024-01-05', workouts: 0, volume: 0 },
    { date: '2024-01-06', workouts: 1, volume: 2000 },
    { date: '2024-01-07', workouts: 1, volume: 1600 },
  ];

  const exerciseFrequencyData = patterns.favorite_exercises.map(([exercise, count]) => ({
    name: exercise.replace('_', ' ').toUpperCase(),
    value: count,
  }));

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Workout Analytics</h1>
        <div className="flex space-x-2">
          <select
            value={selectedPeriod}
            onChange={(e) => setSelectedPeriod(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
          </select>
          <select
            value={selectedExercise}
            onChange={(e) => setSelectedExercise(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md"
          >
            <option value="all">All Exercises</option>
            <option value="bench_press">Bench Press</option>
            <option value="squat">Squat</option>
            <option value="deadlift">Deadlift</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Consistency Score</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              <span className={getConsistencyColor(consistency.score)}>
                {Math.round(consistency.score * 100)}%
              </span>
            </div>
            <p className="text-xs text-muted-foreground">
              {consistency.workout_days} of {consistency.total_days} days
            </p>
            <Progress value={consistency.score * 100} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{consistency.streak} days</div>
            <p className="text-xs text-muted-foreground">
              {consistency.average_workouts_per_week.toFixed(1)} workouts/week
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Strength Progression</CardTitle>
            {getTrendIcon(strength_progression.trend)}
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {strength_progression.progression_rate > 0 ? '+' : ''}
              {strength_progression.progression_rate.toFixed(1)}%
            </div>
            <p className="text-xs text-muted-foreground">
              {strength_progression.exercise.replace('_', ' ')}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Volume</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {volume_analysis.total_volume.toLocaleString()}
            </div>
            <p className="text-xs text-muted-foreground">
              {volume_analysis.average_volume_per_workout.toFixed(0)} avg per workout
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Workout History Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Workout History</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={workoutHistoryData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="workouts"
                  stroke="#8884d8"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Exercise Frequency Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Exercise Frequency</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={exerciseFrequencyData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {exerciseFrequencyData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Insights and Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Consistency Insights */}
        <Card>
          <CardHeader>
            <CardTitle>Consistency Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {consistency.insights.map((insight, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <Badge className={getPriorityColor(insight.priority)}>
                    {insight.priority}
                  </Badge>
                  <div className="flex-1">
                    <p className="text-sm font-medium">{insight.message}</p>
                    <p className="text-xs text-muted-foreground">
                      Confidence: {Math.round(insight.confidence * 100)}%
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Strength Recommendations */}
        <Card>
          <CardHeader>
            <CardTitle>Strength Recommendations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {strength_progression.recommendations.map((rec, index) => (
                <div key={index} className="border-l-4 border-blue-500 pl-4">
                  <h4 className="font-medium text-sm">{rec.title}</h4>
                  <p className="text-sm text-muted-foreground mt-1">
                    {rec.description}
                  </p>
                  <div className="flex items-center space-x-2 mt-2">
                    <Badge className={getPriorityColor(rec.priority)}>
                      {rec.priority}
                    </Badge>
                    <span className="text-xs text-muted-foreground">
                      {rec.estimated_impact} impact
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Workout Patterns */}
      <Card>
        <CardHeader>
          <CardTitle>Workout Patterns</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium text-sm mb-2">Focus Areas</h4>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm">Strength</span>
                  <span className="text-sm font-medium">
                    {Math.round(patterns.strength_focus * 100)}%
                  </span>
                </div>
                <Progress value={patterns.strength_focus * 100} className="h-2" />
                <div className="flex justify-between">
                  <span className="text-sm">Cardio</span>
                  <span className="text-sm font-medium">
                    {Math.round(patterns.cardio_focus * 100)}%
                  </span>
                </div>
                <Progress value={patterns.cardio_focus * 100} className="h-2" />
              </div>
            </div>

            <div>
              <h4 className="font-medium text-sm mb-2">Frequency</h4>
              <Badge className="text-sm">
                {patterns.workout_frequency.replace('_', ' ').toUpperCase()}
              </Badge>
              <p className="text-sm text-muted-foreground mt-2">
                {patterns.total_workouts} total workouts
              </p>
            </div>

            <div>
              <h4 className="font-medium text-sm mb-2">Patterns</h4>
              <div className="space-y-1">
                {patterns.patterns.map((pattern, index) => (
                  <p key={index} className="text-sm text-muted-foreground">
                    • {pattern}
                  </p>
                ))}
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default WorkoutAnalytics;


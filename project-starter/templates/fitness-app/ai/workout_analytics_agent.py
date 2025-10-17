#!/usr/bin/env python3
"""
Workout Analytics Agent for Fitness App
Provides AI-driven insights and analytics for workout data
Inspired by Terry Lin's Cooper's Corner approach
"""

import os
import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutInsight(BaseModel):
    """Individual workout insight"""
    type: str = Field(description="Type of insight")
    message: str = Field(description="Insight message")
    confidence: float = Field(description="Confidence score")
    actionable: bool = Field(description="Whether the insight is actionable")
    priority: str = Field(description="Priority level: low, medium, high")

class WorkoutTrend(BaseModel):
    """Workout trend analysis"""
    metric: str = Field(description="Metric being tracked")
    trend: str = Field(description="Trend direction: up, down, stable")
    change_percent: float = Field(description="Percentage change")
    period: str = Field(description="Time period analyzed")
    significance: str = Field(description="Statistical significance")

class WorkoutRecommendation(BaseModel):
    """AI-generated workout recommendation"""
    type: str = Field(description="Type of recommendation")
    title: str = Field(description="Recommendation title")
    description: str = Field(description="Detailed description")
    reasoning: str = Field(description="Why this recommendation")
    priority: str = Field(description="Priority level")
    estimated_impact: str = Field(description="Expected impact")

class WorkoutAnalyticsAgent:
    """AI-powered analytics agent for workout data"""
    
    def __init__(self, 
                 supabase_url: str = None,
                 supabase_key: str = None,
                 openai_api_key: str = None):
        """
        Initialize the workout analytics agent
        
        Args:
            supabase_url: Supabase project URL
            supabase_key: Supabase API key
            openai_api_key: OpenAI API key for AI insights
        """
        self.supabase_url = supabase_url or os.getenv("SUPABASE_URL")
        self.supabase_key = supabase_key or os.getenv("SUPABASE_ANON_KEY")
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        
        if not all([self.supabase_url, self.supabase_key]):
            raise ValueError("Supabase credentials are required")
        
        # Initialize database client (simplified for example)
        self.db_client = None  # Would initialize Supabase client here
        
        # Analytics configuration
        self.analytics_config = {
            "consistency_threshold": 0.7,  # 70% consistency threshold
            "progress_window_days": 30,    # 30-day progress window
            "strength_progression_threshold": 0.05,  # 5% strength increase
            "volume_progression_threshold": 0.1,     # 10% volume increase
        }
    
    async def analyze_workout_consistency(self, user_id: str, days: int = 30) -> Dict:
        """
        Analyze workout consistency for a user
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Consistency analysis results
        """
        try:
            logger.info(f"Analyzing workout consistency for user {user_id}")
            
            # Get workout data (simplified - would query database)
            workouts = await self._get_user_workouts(user_id, days)
            
            if not workouts:
                return {
                    "consistency_score": 0.0,
                    "workout_days": 0,
                    "total_days": days,
                    "streak": 0,
                    "average_workouts_per_week": 0.0,
                    "insights": []
                }
            
            # Calculate consistency metrics
            workout_dates = [w["timestamp"].date() for w in workouts]
            unique_workout_days = len(set(workout_dates))
            consistency_score = unique_workout_days / days
            
            # Calculate current streak
            current_streak = self._calculate_current_streak(workout_dates)
            
            # Calculate average workouts per week
            weeks = days / 7
            avg_workouts_per_week = unique_workout_days / weeks if weeks > 0 else 0
            
            # Generate insights
            insights = await self._generate_consistency_insights(
                consistency_score, current_streak, avg_workouts_per_week
            )
            
            result = {
                "consistency_score": consistency_score,
                "workout_days": unique_workout_days,
                "total_days": days,
                "streak": current_streak,
                "average_workouts_per_week": avg_workouts_per_week,
                "insights": insights
            }
            
            logger.info(f"Consistency analysis complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Consistency analysis failed: {e}")
            raise
    
    async def analyze_strength_progression(self, user_id: str, exercise: str, days: int = 30) -> Dict:
        """
        Analyze strength progression for a specific exercise
        
        Args:
            user_id: User identifier
            exercise: Exercise name
            days: Number of days to analyze
            
        Returns:
            Strength progression analysis
        """
        try:
            logger.info(f"Analyzing strength progression for {exercise}")
            
            # Get exercise-specific workouts
            workouts = await self._get_exercise_workouts(user_id, exercise, days)
            
            if len(workouts) < 2:
                return {
                    "exercise": exercise,
                    "progression_rate": 0.0,
                    "total_workouts": len(workouts),
                    "max_weight": 0.0,
                    "trend": "insufficient_data",
                    "recommendations": []
                }
            
            # Calculate progression metrics
            weights = [w["weight"] for w in workouts if w["weight"]]
            dates = [w["timestamp"] for w in workouts if w["weight"]]
            
            if not weights:
                return {
                    "exercise": exercise,
                    "progression_rate": 0.0,
                    "total_workouts": len(workouts),
                    "max_weight": 0.0,
                    "trend": "no_weight_data",
                    "recommendations": []
                }
            
            # Calculate progression rate
            progression_rate = self._calculate_progression_rate(weights, dates)
            
            # Determine trend
            trend = self._determine_trend(progression_rate)
            
            # Generate recommendations
            recommendations = await self._generate_strength_recommendations(
                exercise, progression_rate, trend, len(workouts)
            )
            
            result = {
                "exercise": exercise,
                "progression_rate": progression_rate,
                "total_workouts": len(workouts),
                "max_weight": max(weights),
                "trend": trend,
                "recommendations": recommendations
            }
            
            logger.info(f"Strength progression analysis complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Strength progression analysis failed: {e}")
            raise
    
    async def analyze_workout_volume(self, user_id: str, days: int = 30) -> Dict:
        """
        Analyze workout volume trends
        
        Args:
            user_id: User identifier
            days: Number of days to analyze
            
        Returns:
            Volume analysis results
        """
        try:
            logger.info(f"Analyzing workout volume for user {user_id}")
            
            # Get workout data
            workouts = await self._get_user_workouts(user_id, days)
            
            if not workouts:
                return {
                    "total_volume": 0.0,
                    "average_volume_per_workout": 0.0,
                    "volume_trend": "no_data",
                    "insights": []
                }
            
            # Calculate volume metrics
            daily_volumes = self._calculate_daily_volumes(workouts)
            total_volume = sum(daily_volumes.values())
            avg_volume_per_workout = total_volume / len(workouts) if workouts else 0
            
            # Calculate volume trend
            volume_trend = self._calculate_volume_trend(daily_volumes)
            
            # Generate insights
            insights = await self._generate_volume_insights(
                total_volume, avg_volume_per_workout, volume_trend
            )
            
            result = {
                "total_volume": total_volume,
                "average_volume_per_workout": avg_volume_per_workout,
                "volume_trend": volume_trend,
                "insights": insights
            }
            
            logger.info(f"Volume analysis complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Volume analysis failed: {e}")
            raise
    
    async def generate_workout_recommendations(self, user_id: str) -> List[WorkoutRecommendation]:
        """
        Generate AI-powered workout recommendations
        
        Args:
            user_id: User identifier
            
        Returns:
            List of workout recommendations
        """
        try:
            logger.info(f"Generating workout recommendations for user {user_id}")
            
            # Get user's recent workout data
            recent_workouts = await self._get_user_workouts(user_id, 14)  # Last 2 weeks
            
            # Analyze workout patterns
            workout_analysis = await self._analyze_workout_patterns(recent_workouts)
            
            # Generate recommendations based on patterns
            recommendations = await self._generate_pattern_based_recommendations(
                workout_analysis, user_id
            )
            
            logger.info(f"Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            logger.error(f"Recommendation generation failed: {e}")
            raise
    
    async def analyze_workout_patterns(self, user_id: str) -> Dict:
        """
        Analyze overall workout patterns and habits
        
        Args:
            user_id: User identifier
            
        Returns:
            Comprehensive workout pattern analysis
        """
        try:
            logger.info(f"Analyzing workout patterns for user {user_id}")
            
            # Get comprehensive workout data
            workouts = await self._get_user_workouts(user_id, 90)  # Last 3 months
            
            if not workouts:
                return {
                    "total_workouts": 0,
                    "favorite_exercises": [],
                    "workout_frequency": "no_data",
                    "strength_focus": 0.0,
                    "cardio_focus": 0.0,
                    "patterns": []
                }
            
            # Analyze exercise preferences
            exercise_counts = self._count_exercises(workouts)
            favorite_exercises = sorted(exercise_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            
            # Analyze workout frequency
            workout_frequency = self._analyze_frequency_patterns(workouts)
            
            # Analyze strength vs cardio focus
            strength_focus, cardio_focus = self._analyze_focus_areas(workouts)
            
            # Identify patterns
            patterns = await self._identify_workout_patterns(workouts)
            
            result = {
                "total_workouts": len(workouts),
                "favorite_exercises": favorite_exercises,
                "workout_frequency": workout_frequency,
                "strength_focus": strength_focus,
                "cardio_focus": cardio_focus,
                "patterns": patterns
            }
            
            logger.info(f"Pattern analysis complete: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Pattern analysis failed: {e}")
            raise
    
    def _calculate_current_streak(self, workout_dates: List[datetime.date]) -> int:
        """Calculate current workout streak"""
        if not workout_dates:
            return 0
        
        # Sort dates in descending order
        sorted_dates = sorted(set(workout_dates), reverse=True)
        
        streak = 0
        current_date = datetime.now().date()
        
        for i, workout_date in enumerate(sorted_dates):
            if i == 0:
                # Check if most recent workout was today or yesterday
                if workout_date == current_date or workout_date == current_date - timedelta(days=1):
                    streak = 1
                    current_date = workout_date
                else:
                    break
            else:
                # Check if workout was on consecutive day
                if workout_date == current_date - timedelta(days=1):
                    streak += 1
                    current_date = workout_date
                else:
                    break
        
        return streak
    
    def _calculate_progression_rate(self, weights: List[float], dates: List[datetime]) -> float:
        """Calculate strength progression rate"""
        if len(weights) < 2:
            return 0.0
        
        # Create DataFrame for analysis
        df = pd.DataFrame({
            'weight': weights,
            'date': dates
        })
        df = df.sort_values('date')
        
        # Calculate progression rate using linear regression
        x = np.arange(len(df))
        y = df['weight'].values
        
        # Simple linear regression
        slope, _ = np.polyfit(x, y, 1)
        
        # Convert to percentage per week
        progression_rate = slope * 7  # Assuming daily workouts
        
        return progression_rate
    
    def _determine_trend(self, progression_rate: float) -> str:
        """Determine trend direction based on progression rate"""
        threshold = self.analytics_config["strength_progression_threshold"]
        
        if progression_rate > threshold:
            return "improving"
        elif progression_rate < -threshold:
            return "declining"
        else:
            return "stable"
    
    def _calculate_daily_volumes(self, workouts: List[Dict]) -> Dict[datetime.date, float]:
        """Calculate daily workout volumes"""
        daily_volumes = {}
        
        for workout in workouts:
            date = workout["timestamp"].date()
            volume = workout["sets"] * workout["reps"] * (workout["weight"] or 0)
            
            if date in daily_volumes:
                daily_volumes[date] += volume
            else:
                daily_volumes[date] = volume
        
        return daily_volumes
    
    def _calculate_volume_trend(self, daily_volumes: Dict[datetime.date, float]) -> str:
        """Calculate volume trend over time"""
        if len(daily_volumes) < 2:
            return "insufficient_data"
        
        # Sort by date
        sorted_volumes = sorted(daily_volumes.items())
        volumes = [v for _, v in sorted_volumes]
        
        # Calculate trend using linear regression
        x = np.arange(len(volumes))
        slope, _ = np.polyfit(x, volumes, 1)
        
        threshold = self.analytics_config["volume_progression_threshold"]
        
        if slope > threshold:
            return "increasing"
        elif slope < -threshold:
            return "decreasing"
        else:
            return "stable"
    
    def _count_exercises(self, workouts: List[Dict]) -> Dict[str, int]:
        """Count exercise frequency"""
        exercise_counts = {}
        
        for workout in workouts:
            exercise = workout["exercise"]
            exercise_counts[exercise] = exercise_counts.get(exercise, 0) + 1
        
        return exercise_counts
    
    def _analyze_frequency_patterns(self, workouts: List[Dict]) -> str:
        """Analyze workout frequency patterns"""
        if not workouts:
            return "no_data"
        
        # Group by week
        weekly_counts = {}
        for workout in workouts:
            week = workout["timestamp"].isocalendar()[1]  # Week number
            weekly_counts[week] = weekly_counts.get(week, 0) + 1
        
        avg_workouts_per_week = sum(weekly_counts.values()) / len(weekly_counts)
        
        if avg_workouts_per_week >= 5:
            return "very_high"
        elif avg_workouts_per_week >= 3:
            return "high"
        elif avg_workouts_per_week >= 2:
            return "moderate"
        elif avg_workouts_per_week >= 1:
            return "low"
        else:
            return "very_low"
    
    def _analyze_focus_areas(self, workouts: List[Dict]) -> Tuple[float, float]:
        """Analyze strength vs cardio focus"""
        strength_exercises = ["bench_press", "squat", "deadlift", "pull_up", "push_up"]
        cardio_exercises = ["running", "cycling", "swimming", "rowing"]
        
        strength_count = sum(1 for w in workouts if w["exercise"] in strength_exercises)
        cardio_count = sum(1 for w in workouts if w["exercise"] in cardio_exercises)
        total_count = len(workouts)
        
        if total_count == 0:
            return 0.0, 0.0
        
        strength_focus = strength_count / total_count
        cardio_focus = cardio_count / total_count
        
        return strength_focus, cardio_focus
    
    async def _get_user_workouts(self, user_id: str, days: int) -> List[Dict]:
        """Get user workouts from database (simplified)"""
        # This would query the actual database
        # For now, return mock data
        return []
    
    async def _get_exercise_workouts(self, user_id: str, exercise: str, days: int) -> List[Dict]:
        """Get exercise-specific workouts from database (simplified)"""
        # This would query the actual database
        # For now, return mock data
        return []
    
    async def _generate_consistency_insights(self, consistency_score: float, streak: int, avg_workouts: float) -> List[WorkoutInsight]:
        """Generate consistency insights"""
        insights = []
        
        if consistency_score < 0.3:
            insights.append(WorkoutInsight(
                type="consistency",
                message="Your workout consistency is low. Try to establish a regular routine.",
                confidence=0.9,
                actionable=True,
                priority="high"
            ))
        elif consistency_score > 0.8:
            insights.append(WorkoutInsight(
                type="consistency",
                message="Excellent workout consistency! Keep up the great work.",
                confidence=0.9,
                actionable=False,
                priority="low"
            ))
        
        if streak > 7:
            insights.append(WorkoutInsight(
                type="streak",
                message=f"Amazing {streak}-day streak! You're building great habits.",
                confidence=0.8,
                actionable=False,
                priority="medium"
            ))
        
        return insights
    
    async def _generate_strength_recommendations(self, exercise: str, progression_rate: float, trend: str, workout_count: int) -> List[WorkoutRecommendation]:
        """Generate strength-based recommendations"""
        recommendations = []
        
        if trend == "declining":
            recommendations.append(WorkoutRecommendation(
                type="strength",
                title="Focus on Form",
                description="Your strength progression has declined. Focus on proper form and technique.",
                reasoning="Declining strength often indicates form issues or overtraining.",
                priority="high",
                estimated_impact="medium"
            ))
        elif trend == "improving":
            recommendations.append(WorkoutRecommendation(
                type="strength",
                title="Progressive Overload",
                description="Great strength gains! Consider increasing weight or reps gradually.",
                reasoning="Your strength is improving, so you can safely increase intensity.",
                priority="medium",
                estimated_impact="high"
            ))
        
        if workout_count < 5:
            recommendations.append(WorkoutRecommendation(
                type="frequency",
                title="Increase Frequency",
                description=f"Try to do {exercise} more often to see better results.",
                reasoning="More frequent practice leads to better strength gains.",
                priority="medium",
                estimated_impact="high"
            ))
        
        return recommendations
    
    async def _generate_volume_insights(self, total_volume: float, avg_volume: float, trend: str) -> List[WorkoutInsight]:
        """Generate volume-based insights"""
        insights = []
        
        if trend == "increasing":
            insights.append(WorkoutInsight(
                type="volume",
                message="Your workout volume is increasing. Make sure to balance intensity with recovery.",
                confidence=0.8,
                actionable=True,
                priority="medium"
            ))
        elif trend == "decreasing":
            insights.append(WorkoutInsight(
                type="volume",
                message="Your workout volume has decreased. Consider adding more exercises or sets.",
                confidence=0.8,
                actionable=True,
                priority="high"
            ))
        
        return insights
    
    async def _analyze_workout_patterns(self, workouts: List[Dict]) -> Dict:
        """Analyze workout patterns (simplified)"""
        return {
            "total_workouts": len(workouts),
            "average_sets": sum(w["sets"] for w in workouts) / len(workouts) if workouts else 0,
            "average_reps": sum(w["reps"] for w in workouts) / len(workouts) if workouts else 0
        }
    
    async def _generate_pattern_based_recommendations(self, analysis: Dict, user_id: str) -> List[WorkoutRecommendation]:
        """Generate recommendations based on workout patterns"""
        recommendations = []
        
        if analysis["total_workouts"] < 10:
            recommendations.append(WorkoutRecommendation(
                type="frequency",
                title="Build Consistency",
                description="Try to work out more regularly to build a strong foundation.",
                reasoning="Consistent practice is key to seeing results.",
                priority="high",
                estimated_impact="high"
            ))
        
        return recommendations
    
    async def _identify_workout_patterns(self, workouts: List[Dict]) -> List[str]:
        """Identify specific workout patterns"""
        patterns = []
        
        # Analyze workout timing
        workout_hours = [w["timestamp"].hour for w in workouts]
        if workout_hours:
            most_common_hour = max(set(workout_hours), key=workout_hours.count)
            patterns.append(f"Most workouts at {most_common_hour}:00")
        
        # Analyze exercise variety
        unique_exercises = len(set(w["exercise"] for w in workouts))
        if unique_exercises < 5:
            patterns.append("Limited exercise variety")
        elif unique_exercises > 15:
            patterns.append("High exercise variety")
        
        return patterns

# Example usage
async def main():
    """Example usage of Workout Analytics Agent"""
    
    # Initialize agent
    agent = WorkoutAnalyticsAgent(
        supabase_url=os.getenv("SUPABASE_URL"),
        supabase_key=os.getenv("SUPABASE_ANON_KEY"),
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Analyze consistency
    consistency = await agent.analyze_workout_consistency("user123", 30)
    print(f"Consistency analysis: {consistency}")
    
    # Analyze strength progression
    strength = await agent.analyze_strength_progression("user123", "bench_press", 30)
    print(f"Strength progression: {strength}")
    
    # Generate recommendations
    recommendations = await agent.generate_workout_recommendations("user123")
    print(f"Recommendations: {recommendations}")

if __name__ == "__main__":
    asyncio.run(main())


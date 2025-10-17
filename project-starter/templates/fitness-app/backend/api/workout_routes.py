#!/usr/bin/env python3
"""
Workout API Routes for Fitness App
Handles workout data processing, storage, and retrieval
"""

import os
import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import json

# Import AI agents
from ai.voice_processing_agent import VoiceProcessingAgent, WorkoutData
from ai.workout_analytics_agent import WorkoutAnalyticsAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(prefix="/api/workouts", tags=["workouts"])

# Initialize AI agents
voice_agent = VoiceProcessingAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    whisper_model="base",
    language="en"
)

analytics_agent = WorkoutAnalyticsAgent(
    supabase_url=os.getenv("SUPABASE_URL"),
    supabase_key=os.getenv("SUPABASE_ANON_KEY"),
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# Pydantic models for API
class WorkoutCreate(BaseModel):
    exercise: str
    sets: int
    reps: int
    weight: Optional[float] = None
    unit: str = "pounds"
    duration: Optional[int] = None
    distance: Optional[float] = None
    rest_time: Optional[int] = None
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

class WorkoutResponse(BaseModel):
    id: str
    user_id: str
    exercise: str
    sets: int
    reps: int
    weight: Optional[float] = None
    unit: str
    duration: Optional[int] = None
    distance: Optional[float] = None
    rest_time: Optional[int] = None
    notes: Optional[str] = None
    timestamp: datetime
    confidence: float
    created_at: datetime
    updated_at: datetime

class WorkoutListResponse(BaseModel):
    workouts: List[WorkoutResponse]
    total: int
    page: int
    per_page: int
    has_next: bool
    has_prev: bool

class VoiceProcessingResponse(BaseModel):
    transcription: str
    workout_data: WorkoutData
    confidence: float
    processing_time: float

@router.post("/process-audio", response_model=VoiceProcessingResponse)
async def process_workout_audio(
    audio_file: UploadFile = File(...),
    user_id: str = Query(..., description="User ID")
):
    """
    Process audio file and extract workout data using AI
    """
    try:
        logger.info(f"Processing audio file for user {user_id}")
        
        # Save uploaded file temporarily
        temp_file_path = f"/tmp/{audio_file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await audio_file.read()
            buffer.write(content)
        
        # Process audio with AI agent
        start_time = datetime.now()
        workout_data = await voice_agent.process_workout_audio(temp_file_path)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Clean up temp file
        os.remove(temp_file_path)
        
        # Return response
        response = VoiceProcessingResponse(
            transcription=workout_data.notes or "Audio processed",
            workout_data=workout_data,
            confidence=workout_data.confidence,
            processing_time=processing_time
        )
        
        logger.info(f"Audio processing completed in {processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Audio processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

@router.post("/process-text", response_model=VoiceProcessingResponse)
async def process_workout_text(
    text: str = Query(..., description="Workout description text"),
    user_id: str = Query(..., description="User ID")
):
    """
    Process text input and extract workout data using AI
    """
    try:
        logger.info(f"Processing text input for user {user_id}: {text}")
        
        # Process text with AI agent
        start_time = datetime.now()
        workout_data = await voice_agent.process_text_input(text)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # Return response
        response = VoiceProcessingResponse(
            transcription=text,
            workout_data=workout_data,
            confidence=workout_data.confidence,
            processing_time=processing_time
        )
        
        logger.info(f"Text processing completed in {processing_time:.2f}s")
        return response
        
    except Exception as e:
        logger.error(f"Text processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Text processing failed: {str(e)}")

@router.post("/", response_model=WorkoutResponse)
async def create_workout(
    workout: WorkoutCreate,
    user_id: str = Query(..., description="User ID")
):
    """
    Create a new workout record
    """
    try:
        logger.info(f"Creating workout for user {user_id}")
        
        # Convert to WorkoutData for validation
        workout_data = WorkoutData(
            exercise=workout.exercise,
            sets=workout.sets,
            reps=workout.reps,
            weight=workout.weight,
            unit=workout.unit,
            duration=workout.duration,
            distance=workout.distance,
            rest_time=workout.rest_time,
            notes=workout.notes,
            timestamp=workout.timestamp or datetime.now(),
            confidence=1.0  # Manual entry has full confidence
        )
        
        # Save to database (simplified - would use actual database)
        workout_id = f"workout_{datetime.now().timestamp()}"
        
        # Create response
        response = WorkoutResponse(
            id=workout_id,
            user_id=user_id,
            exercise=workout_data.exercise,
            sets=workout_data.sets,
            reps=workout_data.reps,
            weight=workout_data.weight,
            unit=workout_data.unit,
            duration=workout_data.duration,
            distance=workout_data.distance,
            rest_time=workout_data.rest_time,
            notes=workout_data.notes,
            timestamp=workout_data.timestamp,
            confidence=workout_data.confidence,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        logger.info(f"Workout created with ID: {workout_id}")
        return response
        
    except Exception as e:
        logger.error(f"Workout creation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Workout creation failed: {str(e)}")

@router.get("/", response_model=WorkoutListResponse)
async def get_workouts(
    user_id: str = Query(..., description="User ID"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Items per page"),
    exercise: Optional[str] = Query(None, description="Filter by exercise"),
    start_date: Optional[datetime] = Query(None, description="Start date filter"),
    end_date: Optional[datetime] = Query(None, description="End date filter")
):
    """
    Get workouts for a user with pagination and filtering
    """
    try:
        logger.info(f"Getting workouts for user {user_id}")
        
        # Mock data - in real app, would query database
        mock_workouts = [
            WorkoutResponse(
                id=f"workout_{i}",
                user_id=user_id,
                exercise="bench_press",
                sets=3,
                reps=10,
                weight=135.0,
                unit="pounds",
                timestamp=datetime.now() - timedelta(days=i),
                confidence=0.95,
                created_at=datetime.now() - timedelta(days=i),
                updated_at=datetime.now() - timedelta(days=i)
            )
            for i in range(50)  # Mock 50 workouts
        ]
        
        # Apply filters
        filtered_workouts = mock_workouts
        
        if exercise:
            filtered_workouts = [w for w in filtered_workouts if w.exercise == exercise]
        
        if start_date:
            filtered_workouts = [w for w in filtered_workouts if w.timestamp >= start_date]
        
        if end_date:
            filtered_workouts = [w for w in filtered_workouts if w.timestamp <= end_date]
        
        # Apply pagination
        total = len(filtered_workouts)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_workouts = filtered_workouts[start_idx:end_idx]
        
        # Create response
        response = WorkoutListResponse(
            workouts=paginated_workouts,
            total=total,
            page=page,
            per_page=per_page,
            has_next=end_idx < total,
            has_prev=page > 1
        )
        
        logger.info(f"Retrieved {len(paginated_workouts)} workouts for user {user_id}")
        return response
        
    except Exception as e:
        logger.error(f"Failed to get workouts: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workouts: {str(e)}")

@router.get("/{workout_id}", response_model=WorkoutResponse)
async def get_workout(
    workout_id: str,
    user_id: str = Query(..., description="User ID")
):
    """
    Get a specific workout by ID
    """
    try:
        logger.info(f"Getting workout {workout_id} for user {user_id}")
        
        # Mock data - in real app, would query database
        mock_workout = WorkoutResponse(
            id=workout_id,
            user_id=user_id,
            exercise="bench_press",
            sets=3,
            reps=10,
            weight=135.0,
            unit="pounds",
            timestamp=datetime.now(),
            confidence=0.95,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        return mock_workout
        
    except Exception as e:
        logger.error(f"Failed to get workout {workout_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workout: {str(e)}")

@router.put("/{workout_id}", response_model=WorkoutResponse)
async def update_workout(
    workout_id: str,
    workout: WorkoutCreate,
    user_id: str = Query(..., description="User ID")
):
    """
    Update an existing workout
    """
    try:
        logger.info(f"Updating workout {workout_id} for user {user_id}")
        
        # Mock update - in real app, would update database
        updated_workout = WorkoutResponse(
            id=workout_id,
            user_id=user_id,
            exercise=workout.exercise,
            sets=workout.sets,
            reps=workout.reps,
            weight=workout.weight,
            unit=workout.unit,
            duration=workout.duration,
            distance=workout.distance,
            rest_time=workout.rest_time,
            notes=workout.notes,
            timestamp=workout.timestamp or datetime.now(),
            confidence=1.0,
            created_at=datetime.now() - timedelta(days=1),  # Mock created date
            updated_at=datetime.now()
        )
        
        logger.info(f"Workout {workout_id} updated successfully")
        return updated_workout
        
    except Exception as e:
        logger.error(f"Failed to update workout {workout_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to update workout: {str(e)}")

@router.delete("/{workout_id}")
async def delete_workout(
    workout_id: str,
    user_id: str = Query(..., description="User ID")
):
    """
    Delete a workout
    """
    try:
        logger.info(f"Deleting workout {workout_id} for user {user_id}")
        
        # Mock deletion - in real app, would delete from database
        logger.info(f"Workout {workout_id} deleted successfully")
        return {"message": "Workout deleted successfully"}
        
    except Exception as e:
        logger.error(f"Failed to delete workout {workout_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete workout: {str(e)}")

@router.get("/analytics/consistency")
async def get_consistency_analytics(
    user_id: str = Query(..., description="User ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get workout consistency analytics
    """
    try:
        logger.info(f"Getting consistency analytics for user {user_id}")
        
        # Get analytics from AI agent
        analytics = await analytics_agent.analyze_workout_consistency(user_id, days)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Failed to get consistency analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get consistency analytics: {str(e)}")

@router.get("/analytics/strength-progression")
async def get_strength_progression_analytics(
    user_id: str = Query(..., description="User ID"),
    exercise: str = Query(..., description="Exercise name"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get strength progression analytics for a specific exercise
    """
    try:
        logger.info(f"Getting strength progression analytics for {exercise}")
        
        # Get analytics from AI agent
        analytics = await analytics_agent.analyze_strength_progression(user_id, exercise, days)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Failed to get strength progression analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get strength progression analytics: {str(e)}")

@router.get("/analytics/volume")
async def get_volume_analytics(
    user_id: str = Query(..., description="User ID"),
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze")
):
    """
    Get workout volume analytics
    """
    try:
        logger.info(f"Getting volume analytics for user {user_id}")
        
        # Get analytics from AI agent
        analytics = await analytics_agent.analyze_workout_volume(user_id, days)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Failed to get volume analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get volume analytics: {str(e)}")

@router.get("/analytics/patterns")
async def get_workout_patterns(
    user_id: str = Query(..., description="User ID")
):
    """
    Get workout patterns and habits analysis
    """
    try:
        logger.info(f"Getting workout patterns for user {user_id}")
        
        # Get analytics from AI agent
        patterns = await analytics_agent.analyze_workout_patterns(user_id)
        
        return patterns
        
    except Exception as e:
        logger.error(f"Failed to get workout patterns: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workout patterns: {str(e)}")

@router.get("/analytics/recommendations")
async def get_workout_recommendations(
    user_id: str = Query(..., description="User ID")
):
    """
    Get AI-generated workout recommendations
    """
    try:
        logger.info(f"Getting workout recommendations for user {user_id}")
        
        # Get recommendations from AI agent
        recommendations = await analytics_agent.generate_workout_recommendations(user_id)
        
        return {"recommendations": recommendations}
        
    except Exception as e:
        logger.error(f"Failed to get workout recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get workout recommendations: {str(e)}")

@router.get("/exercises/supported")
async def get_supported_exercises():
    """
    Get list of supported exercises
    """
    try:
        logger.info("Getting supported exercises")
        
        # Get from voice processing agent
        exercises = voice_agent.get_supported_exercises()
        
        return {"exercises": exercises}
        
    except Exception as e:
        logger.error(f"Failed to get supported exercises: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get supported exercises: {str(e)}")

@router.get("/exercises/{exercise_name}")
async def get_exercise_info(exercise_name: str):
    """
    Get information about a specific exercise
    """
    try:
        logger.info(f"Getting exercise info for {exercise_name}")
        
        # Get from voice processing agent
        exercise_info = voice_agent.get_exercise_info(exercise_name)
        
        if not exercise_info:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        return exercise_info
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get exercise info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get exercise info: {str(e)}")

# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


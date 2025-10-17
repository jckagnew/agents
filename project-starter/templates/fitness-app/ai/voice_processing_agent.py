#!/usr/bin/env python3
"""
Voice Processing Agent for Fitness App
Handles voice-to-text conversion and workout data extraction
Inspired by Terry Lin's Cooper's Corner approach
"""

import os
import asyncio
import json
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import openai
import whisper
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkoutData(BaseModel):
    """Structured workout data extracted from voice input"""
    exercise: str = Field(description="Name of the exercise")
    sets: int = Field(description="Number of sets")
    reps: int = Field(description="Number of repetitions per set")
    weight: Optional[float] = Field(description="Weight used (if applicable)")
    unit: str = Field(default="pounds", description="Unit of weight")
    duration: Optional[int] = Field(description="Duration in seconds (for cardio)")
    distance: Optional[float] = Field(description="Distance covered (for cardio)")
    rest_time: Optional[int] = Field(description="Rest time between sets in seconds")
    notes: Optional[str] = Field(description="Additional notes")
    timestamp: datetime = Field(default_factory=datetime.now)
    confidence: float = Field(description="Confidence score for the extraction")

class VoiceProcessingAgent:
    """AI-powered voice processing agent for fitness tracking"""
    
    def __init__(self, 
                 openai_api_key: str = None,
                 whisper_model: str = "base",
                 language: str = "en"):
        """
        Initialize the voice processing agent
        
        Args:
            openai_api_key: OpenAI API key for GPT-4 processing
            whisper_model: Whisper model size (tiny, base, small, medium, large)
            language: Language code for speech recognition
        """
        self.openai_api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        self.whisper_model_name = whisper_model
        self.language = language
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize OpenAI client
        openai.api_key = self.openai_api_key
        
        # Load Whisper model
        self.whisper_model = None
        self._load_whisper_model()
        
        # Exercise database for validation
        self.exercise_database = self._load_exercise_database()
        
    def _load_whisper_model(self):
        """Load Whisper model for speech recognition"""
        try:
            logger.info(f"Loading Whisper model: {self.whisper_model_name}")
            self.whisper_model = whisper.load_model(self.whisper_model_name)
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def _load_exercise_database(self) -> Dict[str, Dict]:
        """Load exercise database for validation and mapping"""
        return {
            "bench_press": {
                "name": "Bench Press",
                "category": "chest",
                "equipment": "barbell",
                "muscles": ["chest", "shoulders", "triceps"],
                "aliases": ["bench", "chest press", "barbell bench press"]
            },
            "squat": {
                "name": "Squat",
                "category": "legs",
                "equipment": "barbell",
                "muscles": ["quadriceps", "glutes", "hamstrings"],
                "aliases": ["squats", "barbell squat", "back squat"]
            },
            "deadlift": {
                "name": "Deadlift",
                "category": "back",
                "equipment": "barbell",
                "muscles": ["back", "glutes", "hamstrings"],
                "aliases": ["deadlifts", "barbell deadlift"]
            },
            "pull_up": {
                "name": "Pull Up",
                "category": "back",
                "equipment": "bodyweight",
                "muscles": ["lats", "biceps", "rhomboids"],
                "aliases": ["pullups", "pull-ups", "chin ups"]
            },
            "push_up": {
                "name": "Push Up",
                "category": "chest",
                "equipment": "bodyweight",
                "muscles": ["chest", "shoulders", "triceps"],
                "aliases": ["pushups", "push-ups"]
            },
            "running": {
                "name": "Running",
                "category": "cardio",
                "equipment": "none",
                "muscles": ["legs", "core"],
                "aliases": ["run", "jog", "sprint"]
            },
            "cycling": {
                "name": "Cycling",
                "category": "cardio",
                "equipment": "bike",
                "muscles": ["legs", "core"],
                "aliases": ["bike", "bicycle", "spin"]
            }
        }
    
    async def process_workout_audio(self, audio_file_path: str) -> WorkoutData:
        """
        Process audio file and extract structured workout data
        
        Args:
            audio_file_path: Path to the audio file
            
        Returns:
            WorkoutData object with extracted information
        """
        try:
            logger.info(f"Processing audio file: {audio_file_path}")
            
            # Step 1: Convert speech to text using Whisper
            transcription = await self._transcribe_audio(audio_file_path)
            logger.info(f"Transcription: {transcription}")
            
            # Step 2: Extract structured data using GPT-4
            workout_data = await self._extract_workout_data(transcription)
            
            # Step 3: Validate and enhance data
            validated_data = await self._validate_workout_data(workout_data)
            
            logger.info(f"Extracted workout data: {validated_data}")
            return validated_data
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            raise
    
    async def process_text_input(self, text_input: str) -> WorkoutData:
        """
        Process text input and extract structured workout data
        
        Args:
            text_input: Text description of the workout
            
        Returns:
            WorkoutData object with extracted information
        """
        try:
            logger.info(f"Processing text input: {text_input}")
            
            # Extract structured data using GPT-4
            workout_data = await self._extract_workout_data(text_input)
            
            # Validate and enhance data
            validated_data = await self._validate_workout_data(workout_data)
            
            logger.info(f"Extracted workout data: {validated_data}")
            return validated_data
            
        except Exception as e:
            logger.error(f"Error processing text: {e}")
            raise
    
    async def _transcribe_audio(self, audio_file_path: str) -> str:
        """Transcribe audio file to text using Whisper"""
        try:
            # Use Whisper to transcribe audio
            result = self.whisper_model.transcribe(
                audio_file_path,
                language=self.language,
                fp16=False  # Use fp32 for better compatibility
            )
            
            transcription = result["text"].strip()
            logger.info(f"Transcription completed: {transcription}")
            return transcription
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    async def _extract_workout_data(self, text: str) -> WorkoutData:
        """Extract structured workout data from text using GPT-4"""
        try:
            # Create prompt for GPT-4
            prompt = self._create_extraction_prompt(text)
            
            # Call GPT-4 API
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=500
            )
            
            # Parse response
            extracted_text = response.choices[0].message.content.strip()
            logger.info(f"GPT-4 extraction: {extracted_text}")
            
            # Convert to WorkoutData object
            workout_data = self._parse_gpt_response(extracted_text)
            
            return workout_data
            
        except Exception as e:
            logger.error(f"GPT-4 extraction failed: {e}")
            raise
    
    def _create_extraction_prompt(self, text: str) -> str:
        """Create prompt for GPT-4 workout data extraction"""
        return f"""
        Extract workout information from the following text and return it in JSON format:
        
        Text: "{text}"
        
        Please extract:
        - exercise: The name of the exercise (standardized)
        - sets: Number of sets
        - reps: Number of repetitions per set
        - weight: Weight used (if applicable)
        - unit: Unit of weight (pounds, kg, etc.)
        - duration: Duration in seconds (for cardio)
        - distance: Distance covered (for cardio)
        - rest_time: Rest time between sets in seconds
        - notes: Any additional notes
        - confidence: Your confidence in the extraction (0.0-1.0)
        
        Return only valid JSON, no additional text.
        """
    
    def _get_system_prompt(self) -> str:
        """Get system prompt for GPT-4"""
        return """
        You are an expert fitness data extraction AI. Your job is to extract structured workout information from natural language text.
        
        Rules:
        1. Always return valid JSON
        2. Standardize exercise names (e.g., "bench press" not "bench pressing")
        3. Extract numbers accurately
        4. If information is missing, use null
        5. Be conservative with confidence scores
        6. Handle both strength and cardio exercises
        7. Recognize common exercise aliases
        
        Exercise categories:
        - Strength: bench press, squat, deadlift, pull up, push up, etc.
        - Cardio: running, cycling, swimming, rowing, etc.
        - Bodyweight: push up, pull up, sit up, etc.
        """
    
    def _parse_gpt_response(self, response_text: str) -> WorkoutData:
        """Parse GPT-4 response and create WorkoutData object"""
        try:
            # Clean response text
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            # Parse JSON
            data = json.loads(response_text)
            
            # Create WorkoutData object
            workout_data = WorkoutData(
                exercise=data.get("exercise", ""),
                sets=data.get("sets", 0),
                reps=data.get("reps", 0),
                weight=data.get("weight"),
                unit=data.get("unit", "pounds"),
                duration=data.get("duration"),
                distance=data.get("distance"),
                rest_time=data.get("rest_time"),
                notes=data.get("notes"),
                confidence=data.get("confidence", 0.5)
            )
            
            return workout_data
            
        except Exception as e:
            logger.error(f"Failed to parse GPT response: {e}")
            # Return default workout data
            return WorkoutData(
                exercise="unknown",
                sets=0,
                reps=0,
                confidence=0.0
            )
    
    async def _validate_workout_data(self, workout_data: WorkoutData) -> WorkoutData:
        """Validate and enhance workout data"""
        try:
            # Validate exercise name
            validated_exercise = self._validate_exercise_name(workout_data.exercise)
            workout_data.exercise = validated_exercise
            
            # Validate numbers
            if workout_data.sets < 0:
                workout_data.sets = 0
            if workout_data.reps < 0:
                workout_data.reps = 0
            if workout_data.weight and workout_data.weight < 0:
                workout_data.weight = None
            
            # Enhance with exercise database info
            if validated_exercise in self.exercise_database:
                exercise_info = self.exercise_database[validated_exercise]
                if not workout_data.notes:
                    workout_data.notes = f"Category: {exercise_info['category']}"
            
            # Adjust confidence based on validation
            if validated_exercise == "unknown":
                workout_data.confidence *= 0.5
            
            logger.info(f"Validated workout data: {workout_data}")
            return workout_data
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return workout_data
    
    def _validate_exercise_name(self, exercise: str) -> str:
        """Validate and standardize exercise name"""
        if not exercise:
            return "unknown"
        
        exercise_lower = exercise.lower().strip()
        
        # Check against exercise database
        for exercise_key, exercise_info in self.exercise_database.items():
            if (exercise_lower == exercise_key or 
                exercise_lower in exercise_info["aliases"]):
                return exercise_key
        
        # Try fuzzy matching for common variations
        if "bench" in exercise_lower and "press" in exercise_lower:
            return "bench_press"
        elif "squat" in exercise_lower:
            return "squat"
        elif "deadlift" in exercise_lower:
            return "deadlift"
        elif "pull" in exercise_lower and "up" in exercise_lower:
            return "pull_up"
        elif "push" in exercise_lower and "up" in exercise_lower:
            return "push_up"
        elif "run" in exercise_lower:
            return "running"
        elif "bike" in exercise_lower or "cycle" in exercise_lower:
            return "cycling"
        
        return "unknown"
    
    async def batch_process_workouts(self, audio_files: List[str]) -> List[WorkoutData]:
        """Process multiple audio files in batch"""
        try:
            logger.info(f"Processing {len(audio_files)} audio files")
            
            # Process files concurrently
            tasks = [self.process_workout_audio(file_path) for file_path in audio_files]
            workout_data_list = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Filter out exceptions
            valid_workouts = []
            for workout_data in workout_data_list:
                if isinstance(workout_data, WorkoutData):
                    valid_workouts.append(workout_data)
                else:
                    logger.error(f"Failed to process workout: {workout_data}")
            
            logger.info(f"Successfully processed {len(valid_workouts)} workouts")
            return valid_workouts
            
        except Exception as e:
            logger.error(f"Batch processing failed: {e}")
            raise
    
    def get_supported_exercises(self) -> List[str]:
        """Get list of supported exercises"""
        return list(self.exercise_database.keys())
    
    def get_exercise_info(self, exercise: str) -> Optional[Dict]:
        """Get information about a specific exercise"""
        return self.exercise_database.get(exercise)

# Example usage
async def main():
    """Example usage of Voice Processing Agent"""
    
    # Initialize agent
    agent = VoiceProcessingAgent(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        whisper_model="base",
        language="en"
    )
    
    # Process text input
    text_input = "I did 3 sets of 10 reps of bench press at 135 pounds"
    workout_data = await agent.process_text_input(text_input)
    
    print(f"Extracted workout data:")
    print(f"  Exercise: {workout_data.exercise}")
    print(f"  Sets: {workout_data.sets}")
    print(f"  Reps: {workout_data.reps}")
    print(f"  Weight: {workout_data.weight} {workout_data.unit}")
    print(f"  Confidence: {workout_data.confidence}")
    
    # Process audio file (if available)
    # audio_file = "workout_audio.wav"
    # if os.path.exists(audio_file):
    #     workout_data = await agent.process_workout_audio(audio_file)
    #     print(f"Audio workout data: {workout_data}")

if __name__ == "__main__":
    asyncio.run(main())


"""
FastAPI Application Template
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title=os.getenv("PROJECT_NAME", "API"),
    description="A FastAPI application created from project-starter template",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class HealthResponse(BaseModel):
    status: str
    message: str
    project: str

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

# Routes
@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint"""
    return HealthResponse(
        status="healthy",
        message="API is running",
        project=os.getenv("PROJECT_NAME", "Unknown")
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="Service is operational",
        project=os.getenv("PROJECT_NAME", "Unknown")
    )

@app.post("/items/")
async def create_item(item: Item):
    """Create a new item"""
    return {"message": f"Item {item.name} created successfully", "item": item}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    """Read an item by ID"""
    if item_id < 1:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    return {"item_id": item_id, "message": "Item retrieved successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

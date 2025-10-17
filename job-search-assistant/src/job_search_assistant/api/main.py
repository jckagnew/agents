"""FastAPI main application for the Job Search Assistant."""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import logging
import os
from contextlib import asynccontextmanager

from job_search_assistant.services.database import get_db, create_tables
from .routes import job_search, job_opportunities, applications, documents, email_interactions, analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    
    This function handles startup and shutdown events for the FastAPI application.
    It creates database tables on startup and performs cleanup on shutdown.
    """
    # Startup
    logger.info("🚀 Starting Job Search Assistant API...")
    create_tables()
    logger.info("✅ Database tables created")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Job Search Assistant API...")

# Create FastAPI application
app = FastAPI(
    title="Job Search Assistant API",
    description="AI-powered job search platform for enterprise sales positions",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
)

# Include API routes
app.include_router(
    job_search.router,
    prefix="/api/job-search",
    tags=["Job Search"]
)

app.include_router(
    job_opportunities.router,
    prefix="/api/job-opportunities",
    tags=["Job Opportunities"]
)

app.include_router(
    applications.router,
    prefix="/api/applications",
    tags=["Applications"]
)

app.include_router(
    documents.router,
    prefix="/api/documents",
    tags=["Documents"]
)

app.include_router(
    email_interactions.router,
    prefix="/api/email-interactions",
    tags=["Email Interactions"]
)

app.include_router(
    analytics.router,
    prefix="/api/analytics",
    tags=["Analytics"]
)

@app.get("/")
async def root():
    """
    Root endpoint.
    
    Returns:
        Welcome message and API information
    """
    return {
        "message": "🎯 Job Search Assistant API",
        "version": "1.0.0",
        "description": "AI-powered job search platform for enterprise sales positions",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        API health status
    """
    return {
        "status": "healthy",
        "message": "Job Search Assistant API is running",
        "version": "1.0.0"
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Custom HTTP exception handler.
    
    Args:
        request: FastAPI request object
        exc: HTTP exception
        
    Returns:
        JSON response with error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    General exception handler.
    
    Args:
        request: FastAPI request object
        exc: Exception
        
    Returns:
        JSON response with error details
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": str(request.url)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

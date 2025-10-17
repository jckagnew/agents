"""
{{PROJECT_NAME}} FastAPI Application
{{PROJECT_DESCRIPTION}}
"""

import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from dotenv import load_dotenv
import logging

from .config import settings
from .database import init_db
from .routers import api, auth, admin
from .middleware import LoggingMiddleware, RateLimitMiddleware

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting {{PROJECT_NAME}} application...")
    await init_db()
    logger.info("Database initialized")
    yield
    # Shutdown
    logger.info("Shutting down {{PROJECT_NAME}} application...")

# Create FastAPI application
app = FastAPI(
    title="{{PROJECT_NAME}}",
    description="{{PROJECT_DESCRIPTION}}",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(api.router, prefix="/api/v1", tags=["api"])
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint with HTML response"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "{{PROJECT_NAME}}",
            "description": "{{PROJECT_DESCRIPTION}}",
            "version": "1.0.0"
        }
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "{{PROJECT_NAME}}",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }

@app.get("/info")
async def app_info():
    """Application information"""
    return {
        "name": "{{PROJECT_NAME}}",
        "description": "{{PROJECT_DESCRIPTION}}",
        "version": "1.0.0",
        "author": "{{AUTHOR_NAME}}",
        "email": "{{AUTHOR_EMAIL}}",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "features": [
            "FastAPI",
            "Pydantic",
            "SQLAlchemy",
            "Alembic",
            "Redis",
            "Celery",
            "OpenAI",
            "Anthropic",
            "Google AI"
        ]
    }

def main():
    """Main entry point"""
    uvicorn.run(
        "{{PROJECT_SLUG}}.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )

def dev():
    """Development entry point"""
    uvicorn.run(
        "{{PROJECT_SLUG}}.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug"
    )

def test():
    """Test entry point"""
    import subprocess
    subprocess.run(["pytest", "tests/", "-v", "--cov={{PROJECT_SLUG}}"])

if __name__ == "__main__":
    main()

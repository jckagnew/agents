"""Job Search Assistant - AI-powered job search platform."""

__version__ = "1.0.0"
__author__ = "Jack Agnew"
__email__ = "jack@clevelsalesguy.com"
__description__ = "AI-powered job search assistant for enterprise sales positions"

from .models import (
    JobOpportunity, JobStatus,
    JobSearch, SearchStatus,
    Application, ApplicationStatus,
    Document, DocumentType, DocumentFormat,
    EmailInteraction, EmailType
)
from .services.database import DatabaseManager, get_db
from .api.main import app

__all__ = [
    # Package metadata
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    # Models
    "JobOpportunity",
    "JobStatus",
    "JobSearch",
    "SearchStatus", 
    "Application",
    "ApplicationStatus",
    "Document",
    "DocumentType",
    "DocumentFormat",
    "EmailInteraction",
    "EmailType",
    # Services
    "DatabaseManager",
    "get_db",
    # API
    "app"
]
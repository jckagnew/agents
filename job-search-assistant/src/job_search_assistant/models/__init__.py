"""Database models for the Job Search Assistant."""

from .job_opportunity import JobOpportunity, JobStatus
from .job_search import JobSearch, SearchStatus
from .application import Application, ApplicationStatus
from .document import Document, DocumentType, DocumentFormat
from .email_interaction import EmailInteraction, EmailType

__all__ = [
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
]

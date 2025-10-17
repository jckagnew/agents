"""Database models for the Job Search Assistant."""

from .job_opportunity import JobOpportunity
from .job_search import JobSearch
from .application import Application
from .document import Document
from .email_interaction import EmailInteraction

__all__ = [
    "JobOpportunity",
    "JobSearch", 
    "Application",
    "Document",
    "EmailInteraction",
]

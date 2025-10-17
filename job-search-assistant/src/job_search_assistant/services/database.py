"""Database service for the Job Search Assistant."""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from typing import Generator

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./job_search.db")

# Create engine with appropriate configuration
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
    )
else:
    engine = create_engine(
        DATABASE_URL,
        echo=os.getenv("DATABASE_ECHO", "false").lower() == "true"
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session.
    
    This function provides a database session that is automatically
    closed after use. It's designed to be used as a FastAPI dependency.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """
    Create all database tables.
    
    This function creates all tables defined in the models.
    It should be called during application startup.
    """
    # Import all models to ensure they're registered
    from job_search_assistant.models.job_opportunity import JobOpportunity
    from job_search_assistant.models.job_search import JobSearch
    from job_search_assistant.models.application import Application
    from job_search_assistant.models.document import Document
    from job_search_assistant.models.email_interaction import EmailInteraction
    
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """
    Drop all database tables.
    
    WARNING: This will delete all data!
    Only use this for testing or development.
    """
    Base.metadata.drop_all(bind=engine)

def reset_database():
    """
    Reset the database by dropping and recreating all tables.
    
    WARNING: This will delete all data!
    Only use this for testing or development.
    """
    drop_tables()
    create_tables()

class DatabaseManager:
    """
    Database manager for advanced operations.
    
    This class provides methods for complex database operations
    that require multiple queries or transactions.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_job_opportunities_by_status(self, status: str) -> list:
        """
        Get job opportunities by status.
        
        Args:
            status: Job status to filter by
            
        Returns:
            List of job opportunities with the specified status
        """
        from job_search_assistant.models.job_opportunity import JobOpportunity
        return self.db.query(JobOpportunity).filter(JobOpportunity.status == status).all()
    
    def get_approved_opportunities(self) -> list:
        """
        Get all approved job opportunities.
        
        Returns:
            List of approved job opportunities
        """
        return self.get_job_opportunities_by_status("approved")
    
    def get_applications_by_status(self, status: str) -> list:
        """
        Get applications by status.
        
        Args:
            status: Application status to filter by
            
        Returns:
            List of applications with the specified status
        """
        from job_search_assistant.models.application import Application
        return self.db.query(Application).filter(Application.status == status).all()
    
    def get_pending_follow_ups(self) -> list:
        """
        Get all pending follow-ups.
        
        Returns:
            List of applications that need follow-up
        """
        from job_search_assistant.models.application import Application
        from datetime import datetime
        return self.db.query(Application).filter(
            Application.follow_up_date <= datetime.utcnow(),
            Application.status.in_(["submitted", "under_review"])
        ).all()
    
    def get_email_interactions_by_type(self, email_type: str) -> list:
        """
        Get email interactions by type.
        
        Args:
            email_type: Email type to filter by
            
        Returns:
            List of email interactions with the specified type
        """
        from job_search_assistant.models.email_interaction import EmailInteraction
        return self.db.query(EmailInteraction).filter(
            EmailInteraction.email_type == email_type
        ).all()
    
    def get_unprocessed_emails(self) -> list:
        """
        Get all unprocessed emails.
        
        Returns:
            List of unprocessed email interactions
        """
        from job_search_assistant.models.email_interaction import EmailInteraction
        return self.db.query(EmailInteraction).filter(
            EmailInteraction.status == "unread"
        ).all()
    
    def get_search_statistics(self, search_id: int) -> dict:
        """
        Get statistics for a specific search session.
        
        Args:
            search_id: ID of the search session
            
        Returns:
            Dictionary containing search statistics
        """
        from job_search_assistant.models.job_search import JobSearch
        from job_search_assistant.models.job_opportunity import JobOpportunity
        from job_search_assistant.models.application import Application
        
        search = self.db.query(JobSearch).filter(JobSearch.id == search_id).first()
        if not search:
            return {}
        
        opportunities = self.db.query(JobOpportunity).filter(
            JobOpportunity.search_session_id == search_id
        ).all()
        
        applications = self.db.query(Application).filter(
            Application.search_session_id == search_id
        ).all()
        
        return {
            "search_id": search_id,
            "total_searches": search.total_searches,
            "completed_searches": search.completed_searches,
            "opportunities_found": len(opportunities),
            "approved_opportunities": len([o for o in opportunities if o.status == "approved"]),
            "applications_submitted": len(applications),
            "interviews_scheduled": len([a for a in applications if a.status == "interview_scheduled"]),
            "offers_received": len([a for a in applications if a.status == "offered"]),
            "created_at": search.created_at,
            "completed_at": search.completed_at
        }
    
    def get_overall_statistics(self) -> dict:
        """
        Get overall statistics for all searches.
        
        Returns:
            Dictionary containing overall statistics
        """
        from job_search_assistant.models.job_search import JobSearch
        from job_search_assistant.models.job_opportunity import JobOpportunity
        from job_search_assistant.models.application import Application
        from job_search_assistant.models.email_interaction import EmailInteraction
        
        total_searches = self.db.query(JobSearch).count()
        total_opportunities = self.db.query(JobOpportunity).count()
        total_applications = self.db.query(Application).count()
        total_emails = self.db.query(EmailInteraction).count()
        
        approved_opportunities = self.db.query(JobOpportunity).filter(
            JobOpportunity.status == "approved"
        ).count()
        
        successful_applications = self.db.query(Application).filter(
            Application.status.in_(["interviewed", "offered", "accepted"])
        ).count()
        
        return {
            "total_searches": total_searches,
            "total_opportunities": total_opportunities,
            "approved_opportunities": approved_opportunities,
            "approval_rate": (approved_opportunities / total_opportunities * 100) if total_opportunities > 0 else 0,
            "total_applications": total_applications,
            "successful_applications": successful_applications,
            "success_rate": (successful_applications / total_applications * 100) if total_applications > 0 else 0,
            "total_emails_processed": total_emails
        }

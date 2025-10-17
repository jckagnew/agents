"""Email interaction database model for tracking incoming emails."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

Base = declarative_base()

class EmailType(str, Enum):
    """Email type."""
    JOB_RESPONSE = "job_response"
    INTERVIEW_INVITATION = "interview_invitation"
    REJECTION = "rejection"
    OFFER = "offer"
    FOLLOW_UP = "follow_up"
    GENERAL_INQUIRY = "general_inquiry"
    SPAM = "spam"
    OTHER = "other"

class EmailStatus(str, Enum):
    """Email processing status."""
    UNREAD = "unread"
    READ = "read"
    PROCESSED = "processed"
    ARCHIVED = "archived"
    DELETED = "deleted"

class EmailInteraction(Base):
    """Email interaction database model."""
    __tablename__ = "email_interactions"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), nullable=False, unique=True, index=True)
    from_email = Column(String(255), nullable=False, index=True)
    to_email = Column(String(255), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    email_type = Column(String(50), nullable=True)
    status = Column(String(50), default=EmailStatus.UNREAD)
    job_opportunity_id = Column(Integer, ForeignKey("job_opportunities.id"), nullable=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    confidence_score = Column(Integer, nullable=True)  # AI confidence in classification
    extracted_data = Column(JSON, nullable=True)  # Structured data extracted from email
    action_taken = Column(String(255), nullable=True)  # What action was taken
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    received_at = Column(DateTime, nullable=True)
    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_opportunity = relationship("JobOpportunity", back_populates="email_interactions")
    application = relationship("Application")

class EmailInteractionCreate(BaseModel):
    """Pydantic model for creating email interactions."""
    message_id: str = Field(..., min_length=1, max_length=255)
    from_email: str = Field(..., min_length=1, max_length=255)
    to_email: str = Field(..., min_length=1, max_length=255)
    subject: str = Field(..., min_length=1, max_length=500)
    body_text: Optional[str] = None
    body_html: Optional[str] = None
    email_type: Optional[EmailType] = None
    job_opportunity_id: Optional[int] = Field(None, gt=0)
    application_id: Optional[int] = Field(None, gt=0)
    confidence_score: Optional[int] = Field(None, ge=0, le=100)
    extracted_data: Optional[dict] = None
    received_at: Optional[datetime] = None

class EmailInteractionUpdate(BaseModel):
    """Pydantic model for updating email interactions."""
    email_type: Optional[EmailType] = None
    status: Optional[EmailStatus] = None
    job_opportunity_id: Optional[int] = Field(None, gt=0)
    application_id: Optional[int] = Field(None, gt=0)
    confidence_score: Optional[int] = Field(None, ge=0, le=100)
    extracted_data: Optional[dict] = None
    action_taken: Optional[str] = Field(None, max_length=255)
    follow_up_required: Optional[bool] = None
    follow_up_date: Optional[datetime] = None
    notes: Optional[str] = None
    processed_at: Optional[datetime] = None

class EmailInteractionResponse(BaseModel):
    """Pydantic model for email interaction responses."""
    id: int
    message_id: str
    from_email: str
    to_email: str
    subject: str
    body_text: Optional[str]
    body_html: Optional[str]
    email_type: Optional[EmailType]
    status: EmailStatus
    job_opportunity_id: Optional[int]
    application_id: Optional[int]
    confidence_score: Optional[int]
    extracted_data: Optional[dict]
    action_taken: Optional[str]
    follow_up_required: bool
    follow_up_date: Optional[datetime]
    notes: Optional[str]
    received_at: Optional[datetime]
    processed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

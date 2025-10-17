"""Job application database model."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

Base = declarative_base()

class ApplicationStatus(str, Enum):
    """Application status."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    INTERVIEW_SCHEDULED = "interview_scheduled"
    INTERVIEWED = "interviewed"
    REJECTED = "rejected"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"

class Application(Base):
    """Job application database model."""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_opportunity_id = Column(Integer, ForeignKey("job_opportunities.id"), nullable=False)
    search_session_id = Column(Integer, ForeignKey("job_searches.id"), nullable=True)
    status = Column(String(50), default=ApplicationStatus.DRAFT)
    cover_letter_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    resume_id = Column(Integer, ForeignKey("documents.id"), nullable=True)
    application_date = Column(DateTime, nullable=True)
    application_method = Column(String(100), nullable=True)  # email, website, linkedin, etc.
    application_reference = Column(String(255), nullable=True)  # job posting reference
    notes = Column(Text, nullable=True)
    follow_up_date = Column(DateTime, nullable=True)
    interview_date = Column(DateTime, nullable=True)
    rejection_reason = Column(Text, nullable=True)
    offer_details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_opportunity = relationship("JobOpportunity", back_populates="applications")
    search_session = relationship("JobSearch", back_populates="applications")
    cover_letter = relationship("Document", foreign_keys=[cover_letter_id])
    resume = relationship("Document", foreign_keys=[resume_id])

class ApplicationCreate(BaseModel):
    """Pydantic model for creating applications."""
    job_opportunity_id: int = Field(..., gt=0)
    search_session_id: Optional[int] = Field(None, gt=0)
    application_method: Optional[str] = Field(None, max_length=100)
    application_reference: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None

class ApplicationUpdate(BaseModel):
    """Pydantic model for updating applications."""
    status: Optional[ApplicationStatus] = None
    cover_letter_id: Optional[int] = Field(None, gt=0)
    resume_id: Optional[int] = Field(None, gt=0)
    application_date: Optional[datetime] = None
    application_method: Optional[str] = Field(None, max_length=100)
    application_reference: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    interview_date: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    offer_details: Optional[str] = None

class ApplicationResponse(BaseModel):
    """Pydantic model for application responses."""
    id: int
    job_opportunity_id: int
    search_session_id: Optional[int]
    status: ApplicationStatus
    cover_letter_id: Optional[int]
    resume_id: Optional[int]
    application_date: Optional[datetime]
    application_method: Optional[str]
    application_reference: Optional[str]
    notes: Optional[str]
    follow_up_date: Optional[datetime]
    interview_date: Optional[datetime]
    rejection_reason: Optional[str]
    offer_details: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

"""Job opportunity database model."""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

Base = declarative_base()

class JobStatus(str, Enum):
    """Job opportunity status."""
    DISCOVERED = "discovered"
    APPROVED = "approved"
    APPLIED = "applied"
    INTERVIEWED = "interviewed"
    REJECTED = "rejected"
    OFFERED = "offered"
    ACCEPTED = "accepted"
    WITHDRAWN = "withdrawn"

class JobOpportunity(Base):
    """Job opportunity database model."""
    __tablename__ = "job_opportunities"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True)
    remote_ok = Column(Boolean, default=False)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(3), default="USD")
    description = Column(Text, nullable=True)
    requirements = Column(JSON, nullable=True)
    benefits = Column(JSON, nullable=True)
    application_url = Column(String(500), nullable=True)
    contact_email = Column(String(255), nullable=True)
    contact_name = Column(String(255), nullable=True)
    source = Column(String(100), nullable=True)  # job board, company website, etc.
    source_url = Column(String(500), nullable=True)
    status = Column(String(50), default=JobStatus.DISCOVERED)
    fit_score = Column(Float, nullable=True)  # 1-10 scale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    applied_at = Column(DateTime, nullable=True)
    search_session_id = Column(Integer, ForeignKey("job_searches.id"), nullable=True)
    
    # Relationships
    search_session = relationship("JobSearch", back_populates="opportunities")
    applications = relationship("Application", back_populates="job_opportunity")
    documents = relationship("Document", back_populates="job_opportunity")
    email_interactions = relationship("EmailInteraction", back_populates="job_opportunity")

class JobOpportunityCreate(BaseModel):
    """Pydantic model for creating job opportunities."""
    title: str = Field(..., min_length=1, max_length=255)
    company: str = Field(..., min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    remote_ok: bool = False
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    salary_currency: str = Field("USD", max_length=3)
    description: Optional[str] = None
    requirements: Optional[list[str]] = None
    benefits: Optional[list[str]] = None
    application_url: Optional[str] = Field(None, max_length=500)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    source: Optional[str] = Field(None, max_length=100)
    source_url: Optional[str] = Field(None, max_length=500)
    fit_score: Optional[float] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class JobOpportunityUpdate(BaseModel):
    """Pydantic model for updating job opportunities."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    remote_ok: Optional[bool] = None
    salary_min: Optional[float] = Field(None, ge=0)
    salary_max: Optional[float] = Field(None, ge=0)
    salary_currency: Optional[str] = Field(None, max_length=3)
    description: Optional[str] = None
    requirements: Optional[list[str]] = None
    benefits: Optional[list[str]] = None
    application_url: Optional[str] = Field(None, max_length=500)
    contact_email: Optional[str] = Field(None, max_length=255)
    contact_name: Optional[str] = Field(None, max_length=255)
    source: Optional[str] = Field(None, max_length=100)
    source_url: Optional[str] = Field(None, max_length=500)
    status: Optional[JobStatus] = None
    fit_score: Optional[float] = Field(None, ge=1, le=10)
    notes: Optional[str] = None

class JobOpportunityResponse(BaseModel):
    """Pydantic model for job opportunity responses."""
    id: int
    title: str
    company: str
    location: Optional[str]
    remote_ok: bool
    salary_min: Optional[float]
    salary_max: Optional[float]
    salary_currency: str
    description: Optional[str]
    requirements: Optional[list[str]]
    benefits: Optional[list[str]]
    application_url: Optional[str]
    contact_email: Optional[str]
    contact_name: Optional[str]
    source: Optional[str]
    source_url: Optional[str]
    status: JobStatus
    fit_score: Optional[float]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    approved_at: Optional[datetime]
    applied_at: Optional[datetime]
    
    class Config:
        from_attributes = True

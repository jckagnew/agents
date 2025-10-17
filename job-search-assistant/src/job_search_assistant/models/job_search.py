"""Job search session database model."""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

Base = declarative_base()

class SearchStatus(str, Enum):
    """Job search status."""
    PLANNING = "planning"
    SEARCHING = "searching"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobSearch(Base):
    """Job search session database model."""
    __tablename__ = "job_searches"
    
    id = Column(Integer, primary_key=True, index=True)
    search_query = Column(Text, nullable=False)
    candidate_profile = Column(Text, nullable=True)
    status = Column(String(50), default=SearchStatus.PLANNING)
    total_searches = Column(Integer, default=0)
    completed_searches = Column(Integer, default=0)
    opportunities_found = Column(Integer, default=0)
    search_config = Column(JSON, nullable=True)  # Store search parameters
    results_summary = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    opportunities = relationship("JobOpportunity", back_populates="search_session")
    applications = relationship("Application", back_populates="search_session")

class JobSearchCreate(BaseModel):
    """Pydantic model for creating job searches."""
    search_query: str = Field(..., min_length=1)
    candidate_profile: Optional[str] = None
    search_config: Optional[dict] = None

class JobSearchUpdate(BaseModel):
    """Pydantic model for updating job searches."""
    status: Optional[SearchStatus] = None
    total_searches: Optional[int] = Field(None, ge=0)
    completed_searches: Optional[int] = Field(None, ge=0)
    opportunities_found: Optional[int] = Field(None, ge=0)
    results_summary: Optional[str] = None
    error_message: Optional[str] = None

class JobSearchResponse(BaseModel):
    """Pydantic model for job search responses."""
    id: int
    search_query: str
    candidate_profile: Optional[str]
    status: SearchStatus
    total_searches: int
    completed_searches: int
    opportunities_found: int
    search_config: Optional[dict]
    results_summary: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

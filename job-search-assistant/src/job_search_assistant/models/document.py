"""Document database model for resumes, cover letters, and other files."""

from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field

Base = declarative_base()

class DocumentType(str, Enum):
    """Document type."""
    RESUME = "resume"
    COVER_LETTER = "cover_letter"
    PORTFOLIO = "portfolio"
    REFERENCE_LETTER = "reference_letter"
    CERTIFICATE = "certificate"
    OTHER = "other"

class DocumentFormat(str, Enum):
    """Document format."""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    HTML = "html"
    MARKDOWN = "markdown"

class Document(Base):
    """Document database model."""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    document_type = Column(String(50), nullable=False)
    format = Column(String(20), nullable=False)
    content = Column(LargeBinary, nullable=True)  # Store binary content
    file_path = Column(String(500), nullable=True)  # Store file system path
    file_size = Column(Integer, nullable=True)  # Size in bytes
    mime_type = Column(String(100), nullable=True)
    version = Column(Integer, default=1)
    is_template = Column(Boolean, default=False)
    template_name = Column(String(255), nullable=True)
    job_opportunity_id = Column(Integer, ForeignKey("job_opportunities.id"), nullable=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True)
    meta_data = Column(Text, nullable=True)  # JSON metadata as text
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job_opportunity = relationship("JobOpportunity", back_populates="documents")
    application = relationship("Application", foreign_keys=[application_id])

class DocumentCreate(BaseModel):
    """Pydantic model for creating documents."""
    name: str = Field(..., min_length=1, max_length=255)
    document_type: DocumentType
    format: DocumentFormat
    content: Optional[bytes] = None
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    mime_type: Optional[str] = Field(None, max_length=100)
    is_template: bool = False
    template_name: Optional[str] = Field(None, max_length=255)
    job_opportunity_id: Optional[int] = Field(None, gt=0)
    application_id: Optional[int] = Field(None, gt=0)
    meta_data: Optional[str] = None

class DocumentUpdate(BaseModel):
    """Pydantic model for updating documents."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    document_type: Optional[DocumentType] = None
    format: Optional[DocumentFormat] = None
    content: Optional[bytes] = None
    file_path: Optional[str] = Field(None, max_length=500)
    file_size: Optional[int] = Field(None, ge=0)
    mime_type: Optional[str] = Field(None, max_length=100)
    version: Optional[int] = Field(None, ge=1)
    is_template: Optional[bool] = None
    template_name: Optional[str] = Field(None, max_length=255)
    meta_data: Optional[str] = None

class DocumentResponse(BaseModel):
    """Pydantic model for document responses."""
    id: int
    name: str
    document_type: DocumentType
    format: DocumentFormat
    file_size: Optional[int]
    mime_type: Optional[str]
    version: int
    is_template: bool
    template_name: Optional[str]
    job_opportunity_id: Optional[int]
    application_id: Optional[int]
    metadata: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentDownloadResponse(BaseModel):
    """Pydantic model for document download responses."""
    id: int
    name: str
    content: bytes
    mime_type: str
    file_size: int

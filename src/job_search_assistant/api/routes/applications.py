"""Job applications API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from job_search_assistant.services.database import get_db
from job_search_assistant.models.application import Application, ApplicationCreate, ApplicationUpdate, ApplicationResponse, ApplicationStatus

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[ApplicationResponse])
async def get_applications(
    skip: int = 0,
    limit: int = 100,
    status: Optional[ApplicationStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all job applications with optional filtering."""
    try:
        query = db.query(Application)
        
        if status:
            query = query.filter(Application.status == status)
        
        applications = query.offset(skip).limit(limit).all()
        return applications
    except Exception as e:
        logger.error(f"Error fetching applications: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch applications")

@router.get("/{application_id}", response_model=ApplicationResponse)
async def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application by ID."""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.post("/", response_model=ApplicationResponse)
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application."""
    try:
        db_application = Application(**application.dict())
        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application
    except Exception as e:
        logger.error(f"Error creating application: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create application")

@router.put("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: int,
    application: ApplicationUpdate,
    db: Session = Depends(get_db)
):
    """Update a job application."""
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    try:
        update_data = application.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_application, field, value)
        
        db.commit()
        db.refresh(db_application)
        return db_application
    except Exception as e:
        logger.error(f"Error updating application: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update application")

@router.delete("/{application_id}")
async def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete a job application."""
    db_application = db.query(Application).filter(Application.id == application_id).first()
    if not db_application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    try:
        db.delete(db_application)
        db.commit()
        return {"message": "Application deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting application: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete application")
"""Job opportunities API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from job_search_assistant.services.database import get_db
from job_search_assistant.models.job_opportunity import JobOpportunity, JobOpportunityCreate, JobOpportunityUpdate, JobOpportunityResponse, JobStatus

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[JobOpportunityResponse])
async def get_job_opportunities(
    skip: int = 0,
    limit: int = 100,
    status: Optional[JobStatus] = None,
    db: Session = Depends(get_db)
):
    """Get all job opportunities with optional filtering."""
    try:
        query = db.query(JobOpportunity)
        
        if status:
            query = query.filter(JobOpportunity.status == status)
        
        opportunities = query.offset(skip).limit(limit).all()
        return opportunities
    except Exception as e:
        logger.error(f"Error fetching job opportunities: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch job opportunities")

@router.get("/{opportunity_id}", response_model=JobOpportunityResponse)
async def get_job_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Get a specific job opportunity by ID."""
    opportunity = db.query(JobOpportunity).filter(JobOpportunity.id == opportunity_id).first()
    if not opportunity:
        raise HTTPException(status_code=404, detail="Job opportunity not found")
    return opportunity

@router.post("/", response_model=JobOpportunityResponse)
async def create_job_opportunity(
    opportunity: JobOpportunityCreate,
    db: Session = Depends(get_db)
):
    """Create a new job opportunity."""
    try:
        db_opportunity = JobOpportunity(**opportunity.dict())
        db.add(db_opportunity)
        db.commit()
        db.refresh(db_opportunity)
        return db_opportunity
    except Exception as e:
        logger.error(f"Error creating job opportunity: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create job opportunity")

@router.put("/{opportunity_id}", response_model=JobOpportunityResponse)
async def update_job_opportunity(
    opportunity_id: int,
    opportunity: JobOpportunityUpdate,
    db: Session = Depends(get_db)
):
    """Update a job opportunity."""
    db_opportunity = db.query(JobOpportunity).filter(JobOpportunity.id == opportunity_id).first()
    if not db_opportunity:
        raise HTTPException(status_code=404, detail="Job opportunity not found")
    
    try:
        update_data = opportunity.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_opportunity, field, value)
        
        db.commit()
        db.refresh(db_opportunity)
        return db_opportunity
    except Exception as e:
        logger.error(f"Error updating job opportunity: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update job opportunity")

@router.delete("/{opportunity_id}")
async def delete_job_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Delete a job opportunity."""
    db_opportunity = db.query(JobOpportunity).filter(JobOpportunity.id == opportunity_id).first()
    if not db_opportunity:
        raise HTTPException(status_code=404, detail="Job opportunity not found")
    
    try:
        db.delete(db_opportunity)
        db.commit()
        return {"message": "Job opportunity deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting job opportunity: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete job opportunity")
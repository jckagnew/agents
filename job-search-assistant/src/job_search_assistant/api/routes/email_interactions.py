"""Email interactions API routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from job_search_assistant.services.database import get_db
from job_search_assistant.models.email_interaction import EmailInteraction, EmailInteractionCreate, EmailInteractionUpdate, EmailInteractionResponse, EmailType

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/", response_model=List[EmailInteractionResponse])
async def get_email_interactions(
    skip: int = 0,
    limit: int = 100,
    email_type: Optional[EmailType] = None,
    db: Session = Depends(get_db)
):
    """Get all email interactions with optional filtering."""
    try:
        query = db.query(EmailInteraction)
        
        if email_type:
            query = query.filter(EmailInteraction.email_type == email_type)
        
        interactions = query.offset(skip).limit(limit).all()
        return interactions
    except Exception as e:
        logger.error(f"Error fetching email interactions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch email interactions")

@router.get("/{interaction_id}", response_model=EmailInteractionResponse)
async def get_email_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific email interaction by ID."""
    interaction = db.query(EmailInteraction).filter(EmailInteraction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Email interaction not found")
    return interaction

@router.post("/", response_model=EmailInteractionResponse)
async def create_email_interaction(
    interaction: EmailInteractionCreate,
    db: Session = Depends(get_db)
):
    """Create a new email interaction."""
    try:
        db_interaction = EmailInteraction(**interaction.dict())
        db.add(db_interaction)
        db.commit()
        db.refresh(db_interaction)
        return db_interaction
    except Exception as e:
        logger.error(f"Error creating email interaction: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create email interaction")

@router.put("/{interaction_id}", response_model=EmailInteractionResponse)
async def update_email_interaction(
    interaction_id: int,
    interaction: EmailInteractionUpdate,
    db: Session = Depends(get_db)
):
    """Update an email interaction."""
    db_interaction = db.query(EmailInteraction).filter(EmailInteraction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Email interaction not found")
    
    try:
        update_data = interaction.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_interaction, field, value)
        
        db.commit()
        db.refresh(db_interaction)
        return db_interaction
    except Exception as e:
        logger.error(f"Error updating email interaction: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update email interaction")

@router.delete("/{interaction_id}")
async def delete_email_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an email interaction."""
    db_interaction = db.query(EmailInteraction).filter(EmailInteraction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Email interaction not found")
    
    try:
        db.delete(db_interaction)
        db.commit()
        return {"message": "Email interaction deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting email interaction: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete email interaction")

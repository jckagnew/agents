"""Job search API routes."""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import asyncio
import logging

from job_search_assistant.services.database import get_db, DatabaseManager
from job_search_assistant.models.job_search import JobSearch, JobSearchCreate, JobSearchUpdate, JobSearchResponse, SearchStatus
from job_search_assistant.services.job_search_service import JobSearchService

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/start", response_model=JobSearchResponse)
async def start_job_search(
    search_data: JobSearchCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start a new job search session.
    
    This endpoint creates a new job search session and starts the search process
    in the background. The search will run asynchronously and update the database
    as it progresses.
    
    Args:
        search_data: Job search configuration
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        JobSearchResponse: Created job search session
        
    Raises:
        HTTPException: If search creation fails
    """
    try:
        # Create job search service
        job_search_service = JobSearchService(db)
        
        # Create new search session
        search_session = job_search_service.create_search_session(search_data)
        
        # Start background search process
        background_tasks.add_task(
            job_search_service.run_search_async,
            search_session.id
        )
        
        logger.info(f"Started job search session {search_session.id}")
        
        return JobSearchResponse.from_orm(search_session)
        
    except Exception as e:
        logger.error(f"Failed to start job search: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start job search: {str(e)}"
        )

@router.get("/{search_id}", response_model=JobSearchResponse)
async def get_job_search(
    search_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific job search session.
    
    Args:
        search_id: ID of the search session
        db: Database session
        
    Returns:
        JobSearchResponse: Job search session details
        
    Raises:
        HTTPException: If search not found
    """
    job_search_service = JobSearchService(db)
    search_session = job_search_service.get_search_session(search_id)
    
    if not search_session:
        raise HTTPException(
            status_code=404,
            detail=f"Job search {search_id} not found"
        )
    
    return JobSearchResponse.from_orm(search_session)

@router.get("/{search_id}/status")
async def get_search_status(
    search_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the current status of a job search session.
    
    Args:
        search_id: ID of the search session
        db: Database session
        
    Returns:
        dict: Search status and progress information
        
    Raises:
        HTTPException: If search not found
    """
    job_search_service = JobSearchService(db)
    search_session = job_search_service.get_search_session(search_id)
    
    if not search_session:
        raise HTTPException(
            status_code=404,
            detail=f"Job search {search_id} not found"
        )
    
    return {
        "search_id": search_id,
        "status": search_session.status,
        "progress": {
            "total_searches": search_session.total_searches,
            "completed_searches": search_session.completed_searches,
            "opportunities_found": search_session.opportunities_found
        },
        "created_at": search_session.created_at,
        "updated_at": search_session.updated_at,
        "completed_at": search_session.completed_at
    }

@router.get("/{search_id}/results")
async def get_search_results(
    search_id: int,
    db: Session = Depends(get_db)
):
    """
    Get the results of a completed job search session.
    
    Args:
        search_id: ID of the search session
        db: Database session
        
    Returns:
        dict: Search results and opportunities found
        
    Raises:
        HTTPException: If search not found or not completed
    """
    job_search_service = JobSearchService(db)
    search_session = job_search_service.get_search_session(search_id)
    
    if not search_session:
        raise HTTPException(
            status_code=404,
            detail=f"Job search {search_id} not found"
        )
    
    if search_session.status != SearchStatus.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Search {search_id} is not completed yet. Status: {search_session.status}"
        )
    
    # Get opportunities found in this search
    opportunities = job_search_service.get_search_opportunities(search_id)
    
    return {
        "search_id": search_id,
        "status": search_session.status,
        "summary": search_session.results_summary,
        "opportunities": [
            {
                "id": opp.id,
                "title": opp.title,
                "company": opp.company,
                "location": opp.location,
                "remote_ok": opp.remote_ok,
                "fit_score": opp.fit_score,
                "status": opp.status,
                "created_at": opp.created_at
            }
            for opp in opportunities
        ],
        "statistics": {
            "total_opportunities": len(opportunities),
            "approved_opportunities": len([o for o in opportunities if o.status == "approved"]),
            "average_fit_score": sum(o.fit_score for o in opportunities if o.fit_score) / len([o for o in opportunities if o.fit_score]) if opportunities else 0
        }
    }

@router.get("/", response_model=List[JobSearchResponse])
async def list_job_searches(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all job search sessions.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List[JobSearchResponse]: List of job search sessions
    """
    job_search_service = JobSearchService(db)
    searches = job_search_service.list_search_sessions(skip=skip, limit=limit)
    
    return [JobSearchResponse.from_orm(search) for search in searches]

@router.put("/{search_id}", response_model=JobSearchResponse)
async def update_job_search(
    search_id: int,
    search_update: JobSearchUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a job search session.
    
    Args:
        search_id: ID of the search session
        search_update: Updated search data
        db: Database session
        
    Returns:
        JobSearchResponse: Updated job search session
        
    Raises:
        HTTPException: If search not found or update fails
    """
    job_search_service = JobSearchService(db)
    search_session = job_search_service.update_search_session(search_id, search_update)
    
    if not search_session:
        raise HTTPException(
            status_code=404,
            detail=f"Job search {search_id} not found"
        )
    
    return JobSearchResponse.from_orm(search_session)

@router.delete("/{search_id}")
async def delete_job_search(
    search_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a job search session.
    
    Args:
        search_id: ID of the search session
        db: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If search not found or deletion fails
    """
    job_search_service = JobSearchService(db)
    success = job_search_service.delete_search_session(search_id)
    
    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"Job search {search_id} not found"
        )
    
    return {"message": f"Job search {search_id} deleted successfully"}

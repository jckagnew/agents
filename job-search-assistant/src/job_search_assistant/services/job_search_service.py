"""Job search service for managing search sessions and operations."""

import asyncio
import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from job_search_assistant.models.job_search import JobSearch, JobSearchCreate, JobSearchUpdate, SearchStatus
from job_search_assistant.models.job_opportunity import JobOpportunity
from job_search_assistant.agents.job_planner_agent import job_planner_agent
from job_search_assistant.agents.job_search_agent import job_search_agent
from job_search_assistant.agents.job_analyzer_agent import job_analyzer_agent
from agents import Runner

logger = logging.getLogger(__name__)

class JobSearchService:
    """Service for managing job search operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_search_session(self, search_data: JobSearchCreate) -> JobSearch:
        """Create a new job search session."""
        search_session = JobSearch(
            search_query=search_data.search_query,
            candidate_profile=search_data.candidate_profile,
            search_config=search_data.search_config or {},
            status=SearchStatus.PLANNING
        )
        
        self.db.add(search_session)
        self.db.commit()
        self.db.refresh(search_session)
        
        logger.info(f"Created search session {search_session.id}")
        return search_session
    
    def get_search_session(self, search_id: int) -> Optional[JobSearch]:
        """Get a search session by ID."""
        return self.db.query(JobSearch).filter(JobSearch.id == search_id).first()
    
    def list_search_sessions(self, skip: int = 0, limit: int = 100) -> List[JobSearch]:
        """List search sessions with pagination."""
        return self.db.query(JobSearch).offset(skip).limit(limit).all()
    
    def update_search_session(self, search_id: int, update_data: JobSearchUpdate) -> Optional[JobSearch]:
        """Update a search session."""
        search_session = self.get_search_session(search_id)
        if not search_session:
            return None
        
        for field, value in update_data.dict(exclude_unset=True).items():
            setattr(search_session, field, value)
        
        search_session.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(search_session)
        
        return search_session
    
    def delete_search_session(self, search_id: int) -> bool:
        """Delete a search session."""
        search_session = self.get_search_session(search_id)
        if not search_session:
            return False
        
        self.db.delete(search_session)
        self.db.commit()
        return True
    
    def get_search_opportunities(self, search_id: int) -> List[JobOpportunity]:
        """Get opportunities found in a search session."""
        return self.db.query(JobOpportunity).filter(
            JobOpportunity.search_session_id == search_id
        ).all()
    
    async def run_search_async(self, search_id: int):
        """Run a job search asynchronously."""
        try:
            search_session = self.get_search_session(search_id)
            if not search_session:
                logger.error(f"Search session {search_id} not found")
                return
            
            # Update status to searching
            self.update_search_session(search_id, JobSearchUpdate(status=SearchStatus.SEARCHING))
            
            # Run the actual search process
            await self._execute_search_process(search_session)
            
            # Update status to completed
            self.update_search_session(search_id, JobSearchUpdate(
                status=SearchStatus.COMPLETED,
                completed_at=datetime.utcnow()
            ))
            
            logger.info(f"Search session {search_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Search session {search_id} failed: {e}")
            self.update_search_session(search_id, JobSearchUpdate(
                status=SearchStatus.FAILED,
                error_message=str(e)
            ))
    
    async def _execute_search_process(self, search_session: JobSearch):
        """Execute the actual search process."""
        # This is a simplified version - in reality, you'd run the full agent workflow
        logger.info(f"Executing search process for session {search_session.id}")
        
        # Simulate search process
        await asyncio.sleep(1)
        
        # Update search statistics
        self.update_search_session(search_session.id, JobSearchUpdate(
            total_searches=20,
            completed_searches=20,
            opportunities_found=5,
            results_summary="Found 5 relevant opportunities"
        ))

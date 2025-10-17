"""Analytics API routes for the Job Search Assistant."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import logging

from job_search_assistant.services.database import get_db, DatabaseManager
from job_search_assistant.models.job_search import JobSearch
from job_search_assistant.models.job_opportunity import JobOpportunity
from job_search_assistant.models.application import Application
from job_search_assistant.models.email_interaction import EmailInteraction

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/overview")
async def get_overview_analytics(
    db: Session = Depends(get_db)
):
    """
    Get overview analytics for the job search platform.
    
    This endpoint provides high-level statistics about job searches,
    opportunities, applications, and success rates.
    
    Args:
        db: Database session
        
    Returns:
        dict: Overview analytics data
    """
    try:
        db_manager = DatabaseManager(db)
        stats = db_manager.get_overall_statistics()
        
        # Calculate additional metrics
        total_searches = stats.get("total_searches", 0)
        total_opportunities = stats.get("total_opportunities", 0)
        approved_opportunities = stats.get("approved_opportunities", 0)
        total_applications = stats.get("total_applications", 0)
        successful_applications = stats.get("successful_applications", 0)
        
        return {
            "overview": {
                "total_searches": total_searches,
                "total_opportunities": total_opportunities,
                "approved_opportunities": approved_opportunities,
                "total_applications": total_applications,
                "successful_applications": successful_applications
            },
            "metrics": {
                "approval_rate": stats.get("approval_rate", 0),
                "success_rate": stats.get("success_rate", 0),
                "opportunities_per_search": total_opportunities / total_searches if total_searches > 0 else 0,
                "applications_per_opportunity": total_applications / approved_opportunities if approved_opportunities > 0 else 0
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get overview analytics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get overview analytics: {str(e)}"
        )

@router.get("/search/{search_id}")
async def get_search_analytics(
    search_id: int,
    db: Session = Depends(get_db)
):
    """
    Get analytics for a specific search session.
    
    Args:
        search_id: ID of the search session
        db: Database session
        
    Returns:
        dict: Search-specific analytics data
        
    Raises:
        HTTPException: If search not found
    """
    try:
        db_manager = DatabaseManager(db)
        stats = db_manager.get_search_statistics(search_id)
        
        if not stats:
            raise HTTPException(
                status_code=404,
                detail=f"Search {search_id} not found"
            )
        
        return {
            "search_id": search_id,
            "statistics": stats,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get search analytics for {search_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get search analytics: {str(e)}"
        )

@router.get("/opportunities/status")
async def get_opportunity_status_analytics(
    db: Session = Depends(get_db)
):
    """
    Get analytics for job opportunity statuses.
    
    Args:
        db: Database session
        
    Returns:
        dict: Opportunity status analytics
    """
    try:
        # Get opportunities by status
        discovered = db.query(JobOpportunity).filter(JobOpportunity.status == "discovered").count()
        approved = db.query(JobOpportunity).filter(JobOpportunity.status == "approved").count()
        applied = db.query(JobOpportunity).filter(JobOpportunity.status == "applied").count()
        interviewed = db.query(JobOpportunity).filter(JobOpportunity.status == "interviewed").count()
        rejected = db.query(JobOpportunity).filter(JobOpportunity.status == "rejected").count()
        offered = db.query(JobOpportunity).filter(JobOpportunity.status == "offered").count()
        accepted = db.query(JobOpportunity).filter(JobOpportunity.status == "accepted").count()
        
        total = discovered + approved + applied + interviewed + rejected + offered + accepted
        
        return {
            "status_breakdown": {
                "discovered": discovered,
                "approved": approved,
                "applied": applied,
                "interviewed": interviewed,
                "rejected": rejected,
                "offered": offered,
                "accepted": accepted,
                "total": total
            },
            "percentages": {
                "discovered": (discovered / total * 100) if total > 0 else 0,
                "approved": (approved / total * 100) if total > 0 else 0,
                "applied": (applied / total * 100) if total > 0 else 0,
                "interviewed": (interviewed / total * 100) if total > 0 else 0,
                "rejected": (rejected / total * 100) if total > 0 else 0,
                "offered": (offered / total * 100) if total > 0 else 0,
                "accepted": (accepted / total * 100) if total > 0 else 0
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get opportunity status analytics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get opportunity status analytics: {str(e)}"
        )

@router.get("/applications/status")
async def get_application_status_analytics(
    db: Session = Depends(get_db)
):
    """
    Get analytics for application statuses.
    
    Args:
        db: Database session
        
    Returns:
        dict: Application status analytics
    """
    try:
        # Get applications by status
        draft = db.query(Application).filter(Application.status == "draft").count()
        submitted = db.query(Application).filter(Application.status == "submitted").count()
        under_review = db.query(Application).filter(Application.status == "under_review").count()
        interview_scheduled = db.query(Application).filter(Application.status == "interview_scheduled").count()
        interviewed = db.query(Application).filter(Application.status == "interviewed").count()
        rejected = db.query(Application).filter(Application.status == "rejected").count()
        offered = db.query(Application).filter(Application.status == "offered").count()
        accepted = db.query(Application).filter(Application.status == "accepted").count()
        withdrawn = db.query(Application).filter(Application.status == "withdrawn").count()
        
        total = draft + submitted + under_review + interview_scheduled + interviewed + rejected + offered + accepted + withdrawn
        
        return {
            "status_breakdown": {
                "draft": draft,
                "submitted": submitted,
                "under_review": under_review,
                "interview_scheduled": interview_scheduled,
                "interviewed": interviewed,
                "rejected": rejected,
                "offered": offered,
                "accepted": accepted,
                "withdrawn": withdrawn,
                "total": total
            },
            "percentages": {
                "draft": (draft / total * 100) if total > 0 else 0,
                "submitted": (submitted / total * 100) if total > 0 else 0,
                "under_review": (under_review / total * 100) if total > 0 else 0,
                "interview_scheduled": (interview_scheduled / total * 100) if total > 0 else 0,
                "interviewed": (interviewed / total * 100) if total > 0 else 0,
                "rejected": (rejected / total * 100) if total > 0 else 0,
                "offered": (offered / total * 100) if total > 0 else 0,
                "accepted": (accepted / total * 100) if total > 0 else 0,
                "withdrawn": (withdrawn / total * 100) if total > 0 else 0
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get application status analytics: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get application status analytics: {str(e)}"
        )

@router.get("/trends/daily")
async def get_daily_trends(
    days: int = 30,
    db: Session = Depends(get_db)
):
    """
    Get daily trends for the last N days.
    
    Args:
        days: Number of days to look back
        db: Database session
        
    Returns:
        dict: Daily trends data
    """
    try:
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Get daily counts
        daily_data = []
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            next_date = current_date + timedelta(days=1)
            
            searches = db.query(JobSearch).filter(
                JobSearch.created_at >= current_date,
                JobSearch.created_at < next_date
            ).count()
            
            opportunities = db.query(JobOpportunity).filter(
                JobOpportunity.created_at >= current_date,
                JobOpportunity.created_at < next_date
            ).count()
            
            applications = db.query(Application).filter(
                Application.created_at >= current_date,
                Application.created_at < next_date
            ).count()
            
            daily_data.append({
                "date": current_date.date().isoformat(),
                "searches": searches,
                "opportunities": opportunities,
                "applications": applications
            })
        
        return {
            "period": f"Last {days} days",
            "daily_data": daily_data,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get daily trends: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get daily trends: {str(e)}"
        )

@router.get("/email-interactions/summary")
async def get_email_interactions_summary(
    db: Session = Depends(get_db)
):
    """
    Get summary of email interactions.
    
    Args:
        db: Database session
        
    Returns:
        dict: Email interactions summary
    """
    try:
        # Get email interactions by type
        job_responses = db.query(EmailInteraction).filter(
            EmailInteraction.email_type == "job_response"
        ).count()
        
        interview_invitations = db.query(EmailInteraction).filter(
            EmailInteraction.email_type == "interview_invitation"
        ).count()
        
        rejections = db.query(EmailInteraction).filter(
            EmailInteraction.email_type == "rejection"
        ).count()
        
        offers = db.query(EmailInteraction).filter(
            EmailInteraction.email_type == "offer"
        ).count()
        
        follow_ups = db.query(EmailInteraction).filter(
            EmailInteraction.email_type == "follow_up"
        ).count()
        
        unprocessed = db.query(EmailInteraction).filter(
            EmailInteraction.status == "unread"
        ).count()
        
        total = job_responses + interview_invitations + rejections + offers + follow_ups
        
        return {
            "email_types": {
                "job_responses": job_responses,
                "interview_invitations": interview_invitations,
                "rejections": rejections,
                "offers": offers,
                "follow_ups": follow_ups,
                "total": total
            },
            "processing_status": {
                "unprocessed": unprocessed,
                "processed": total - unprocessed,
                "processing_rate": ((total - unprocessed) / total * 100) if total > 0 else 0
            },
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Failed to get email interactions summary: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get email interactions summary: {str(e)}"
        )

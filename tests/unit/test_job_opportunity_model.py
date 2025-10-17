"""Unit tests for job opportunity model."""

import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from job_search_assistant.models.job_opportunity import JobOpportunity, JobStatus, JobOpportunityCreate, JobOpportunityUpdate


class TestJobOpportunityModel:
    """Test cases for JobOpportunity model."""
    
    def test_job_opportunity_creation(self, db_session):
        """Test creating a job opportunity."""
        job = JobOpportunity(
            title="AI Sales Engineer",
            company="TechCorp",
            location="Remote",
            remote_ok=True,
            salary_min=100000.0,
            salary_max=150000.0,
            fit_score=8.5
        )
        
        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)
        
        assert job.id is not None
        assert job.title == "AI Sales Engineer"
        assert job.company == "TechCorp"
        assert job.remote_ok is True
        assert job.fit_score == 8.5
        assert job.status == JobStatus.DISCOVERED
        assert job.created_at is not None
        assert job.updated_at is not None
    
    def test_job_opportunity_required_fields(self, db_session):
        """Test that required fields are enforced."""
        job = JobOpportunity()
        
        db_session.add(job)
        
        with pytest.raises(IntegrityError):
            db_session.commit()
    
    def test_job_opportunity_status_enum(self, db_session):
        """Test job status enum values."""
        job = JobOpportunity(
            title="Test Job",
            company="Test Company",
            status=JobStatus.APPROVED
        )
        
        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)
        
        assert job.status == JobStatus.APPROVED
    
    def test_job_opportunity_timestamps(self, db_session):
        """Test that timestamps are automatically set."""
        job = JobOpportunity(
            title="Test Job",
            company="Test Company"
        )
        
        db_session.add(job)
        db_session.commit()
        db_session.refresh(job)
        
        assert job.created_at is not None
        assert job.updated_at is not None
        assert isinstance(job.created_at, datetime)
        assert isinstance(job.updated_at, datetime)


class TestJobOpportunityPydanticModels:
    """Test cases for Pydantic models."""
    
    def test_job_opportunity_create_valid(self):
        """Test creating a valid JobOpportunityCreate."""
        data = {
            "title": "AI Sales Engineer",
            "company": "TechCorp",
            "location": "Remote",
            "remote_ok": True,
            "salary_min": 100000.0,
            "salary_max": 150000.0,
            "fit_score": 8.5
        }
        
        job_create = JobOpportunityCreate(**data)
        
        assert job_create.title == "AI Sales Engineer"
        assert job_create.company == "TechCorp"
        assert job_create.remote_ok is True
        assert job_create.fit_score == 8.5
    
    def test_job_opportunity_create_validation(self):
        """Test JobOpportunityCreate validation."""
        # Test required fields
        with pytest.raises(ValueError):
            JobOpportunityCreate()
        
        # Test invalid fit_score
        with pytest.raises(ValueError):
            JobOpportunityCreate(
                title="Test",
                company="Test",
                fit_score=15.0  # Invalid: > 10
            )
        
        # Test negative salary
        with pytest.raises(ValueError):
            JobOpportunityCreate(
                title="Test",
                company="Test",
                salary_min=-1000.0  # Invalid: negative
            )
    
    def test_job_opportunity_update_partial(self):
        """Test partial updates with JobOpportunityUpdate."""
        data = {
            "title": "Updated Title",
            "fit_score": 9.0
        }
        
        job_update = JobOpportunityUpdate(**data)
        
        assert job_update.title == "Updated Title"
        assert job_update.fit_score == 9.0
        assert job_update.company is None  # Not provided
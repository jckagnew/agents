"""Pytest configuration and fixtures for the Job Search Assistant."""

import asyncio
import pytest
from typing import AsyncGenerator, Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from httpx import AsyncClient

from job_search_assistant.models.job_opportunity import Base, JobOpportunity
from job_search_assistant.api.main import app
from job_search_assistant.services.database import get_db

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def db_session() -> Generator:
    """Create a fresh database session for each test."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Drop tables
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session) -> Generator:
    """Create a test client with database dependency override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def async_client(db_session) -> AsyncGenerator:
    """Create an async test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_job_opportunity_data():
    """Sample job opportunity data for testing."""
    return {
        "title": "Senior AI Sales Engineer",
        "company": "TechCorp Inc",
        "location": "Remote",
        "remote_ok": True,
        "salary_min": 120000.0,
        "salary_max": 180000.0,
        "salary_currency": "USD",
        "description": "Lead AI sales initiatives for enterprise clients",
        "requirements": ["5+ years sales experience", "AI/ML knowledge"],
        "benefits": ["Health insurance", "401k", "Stock options"],
        "application_url": "https://techcorp.com/careers/ai-sales-engineer",
        "contact_email": "hr@techcorp.com",
        "source": "company_website",
        "fit_score": 8.5,
        "notes": "Great fit for Jack's background"
    }

@pytest.fixture
def sample_job_opportunity(db_session, sample_job_opportunity_data):
    """Create a sample job opportunity in the database."""
    job = JobOpportunity(**sample_job_opportunity_data)
    db_session.add(job)
    db_session.commit()
    db_session.refresh(job)
    return job
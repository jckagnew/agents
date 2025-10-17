"""End-to-end tests for job search workflow."""

import pytest
from playwright.async_api import async_playwright, Page, Browser
from httpx import AsyncClient

from job_search_assistant.api.main import app


class TestJobSearchWorkflow:
    """E2E tests for the complete job search workflow."""
    
    @pytest.fixture
    async def browser(self) -> Browser:
        """Create a browser instance for testing."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            yield browser
            await browser.close()
    
    @pytest.fixture
    async def page(self, browser: Browser) -> Page:
        """Create a page instance for testing."""
        page = await browser.new_page()
        yield page
        await page.close()
    
    @pytest.fixture
    async def client(self) -> AsyncClient:
        """Create an async HTTP client for testing."""
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
    
    async def test_job_search_complete_workflow(self, client: AsyncClient, page: Page):
        """Test the complete job search workflow from start to finish."""
        # Step 1: Start job search
        response = await client.post("/api/job-search/start")
        assert response.status_code == 200
        
        search_data = response.json()
        search_id = search_data["search_id"]
        assert search_id is not None
        
        # Step 2: Check search status
        response = await client.get(f"/api/job-search/{search_id}/status")
        assert response.status_code == 200
        
        status_data = response.json()
        assert status_data["status"] in ["planning", "searching", "analyzing", "completed"]
        
        # Step 3: Wait for search completion (in real test, you'd poll)
        # For now, we'll simulate completion
        
        # Step 4: Get search results
        response = await client.get(f"/api/job-search/{search_id}/results")
        assert response.status_code == 200
        
        results_data = response.json()
        assert "opportunities" in results_data
        assert isinstance(results_data["opportunities"], list)
        
        # Step 5: Approve an opportunity
        if results_data["opportunities"]:
            opportunity_id = results_data["opportunities"][0]["id"]
            
            response = await client.post(
                f"/api/job-opportunities/{opportunity_id}/approve"
            )
            assert response.status_code == 200
            
            # Step 6: Check approved opportunities
            response = await client.get("/api/job-opportunities/approved")
            assert response.status_code == 200
            
            approved_data = response.json()
            assert len(approved_data) >= 1
            
            # Step 7: Generate custom resume
            response = await client.post(
                f"/api/job-opportunities/{opportunity_id}/generate-resume"
            )
            assert response.status_code == 200
            
            resume_data = response.json()
            assert "document_id" in resume_data
            assert "download_url" in resume_data
            
            # Step 8: Generate custom cover letter
            response = await client.post(
                f"/api/job-opportunities/{opportunity_id}/generate-cover-letter"
            )
            assert response.status_code == 200
            
            cover_letter_data = response.json()
            assert "document_id" in cover_letter_data
            assert "download_url" in cover_letter_data
    
    async def test_job_search_ui_workflow(self, page: Page):
        """Test the job search workflow through the UI."""
        # Navigate to the job search page
        await page.goto("http://localhost:3000/job-search")
        
        # Wait for page to load
        await page.wait_for_selector("[data-testid='job-search-form']")
        
        # Start a new job search
        await page.click("[data-testid='start-search-button']")
        
        # Wait for search to start
        await page.wait_for_selector("[data-testid='search-progress']")
        
        # Wait for search to complete (in real test, you'd wait for completion)
        await page.wait_for_selector("[data-testid='search-results']", timeout=30000)
        
        # Check that results are displayed
        results = await page.query_selector_all("[data-testid='job-opportunity']")
        assert len(results) > 0
        
        # Approve the first opportunity
        await page.click("[data-testid='approve-button']:first-child")
        
        # Check that opportunity is marked as approved
        approved_indicator = await page.query_selector("[data-testid='approved-indicator']")
        assert approved_indicator is not None
        
        # Generate custom resume
        await page.click("[data-testid='generate-resume-button']")
        
        # Wait for resume generation
        await page.wait_for_selector("[data-testid='resume-generated']")
        
        # Check that download link is available
        download_link = await page.query_selector("[data-testid='resume-download-link']")
        assert download_link is not None
        
        # Generate custom cover letter
        await page.click("[data-testid='generate-cover-letter-button']")
        
        # Wait for cover letter generation
        await page.wait_for_selector("[data-testid='cover-letter-generated']")
        
        # Check that download link is available
        cover_letter_link = await page.query_selector("[data-testid='cover-letter-download-link']")
        assert cover_letter_link is not None
    
    async def test_email_monitoring_workflow(self, client: AsyncClient):
        """Test email monitoring and response tracking."""
        # Simulate receiving an email response
        email_data = {
            "from": "hr@techcorp.com",
            "subject": "Re: Application for AI Sales Engineer Position",
            "body": "Thank you for your application. We'd like to schedule an interview.",
            "job_opportunity_id": 1
        }
        
        response = await client.post("/api/email-interactions/", json=email_data)
        assert response.status_code == 200
        
        # Check that email interaction is recorded
        response = await client.get("/api/email-interactions/")
        assert response.status_code == 200
        
        interactions = response.json()
        assert len(interactions) >= 1
        
        # Check that job opportunity status is updated
        response = await client.get("/api/job-opportunities/1")
        assert response.status_code == 200
        
        opportunity = response.json()
        assert opportunity["status"] == "interviewed"
    
    async def test_analytics_dashboard(self, page: Page):
        """Test the analytics dashboard."""
        # Navigate to analytics dashboard
        await page.goto("http://localhost:3000/analytics")
        
        # Wait for dashboard to load
        await page.wait_for_selector("[data-testid='analytics-dashboard']")
        
        # Check that key metrics are displayed
        metrics = [
            "[data-testid='total-searches']",
            "[data-testid='opportunities-found']",
            "[data-testid='approval-rate']",
            "[data-testid='application-rate']",
            "[data-testid='interview-rate']"
        ]
        
        for metric in metrics:
            element = await page.query_selector(metric)
            assert element is not None
            assert await element.text_content() != ""
        
        # Check that charts are rendered
        charts = await page.query_selector_all("[data-testid='chart']")
        assert len(charts) > 0

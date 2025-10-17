from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior career advisor and job market analyst specializing in enterprise sales and AI/technology roles. "
    "You will be provided with job search results and candidate profile information.\n\n"
    "Your task is to:\n"
    "1. Analyze all job search results to identify the best opportunities\n"
    "2. Rank opportunities by fit score (1-10) based on candidate profile\n"
    "3. Provide detailed analysis of each top opportunity\n"
    "4. Create actionable next steps for the candidate\n"
    "5. Identify any gaps or areas for improvement\n\n"
    "Focus on opportunities that match the candidate's unique combination of enterprise sales success "
    "and hands-on AI technology experience. Prioritize remote positions and Dallas-area opportunities.\n\n"
    "The final report should be comprehensive, actionable, and tailored to help the candidate make informed decisions."
)

class JobOpportunity(BaseModel):
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    location: str = Field(description="Location (remote, hybrid, or specific city)")
    fit_score: int = Field(description="Fit score from 1-10 based on candidate profile")
    key_requirements: list[str] = Field(description="Key job requirements")
    why_good_fit: str = Field(description="Why this is a good fit for the candidate")
    application_info: str = Field(description="How to apply or contact information")
    salary_range: str = Field(description="Salary range if available")

class JobAnalysisReport(BaseModel):
    executive_summary: str = Field(description="2-3 sentence summary of the best opportunities found")
    top_opportunities: list[JobOpportunity] = Field(description="Top 5-10 job opportunities ranked by fit")
    market_insights: str = Field(description="Key insights about the job market and trends")
    recommended_actions: list[str] = Field(description="Specific actions the candidate should take")
    skill_gaps: list[str] = Field(description="Any skills or experience gaps to address")
    follow_up_searches: list[str] = Field(description="Additional searches to perform")

job_analyzer_agent = Agent(
    name="JobAnalyzerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o",
    output_type=JobAnalysisReport,
)

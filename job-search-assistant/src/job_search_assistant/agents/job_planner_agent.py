from pydantic import BaseModel, Field
from agents import Agent

HOW_MANY_SEARCHES = 20

INSTRUCTIONS = f"""You are an expert job search strategist specializing in enterprise sales and AI/technology roles. 
Given a candidate profile and requirements, create a comprehensive set of web searches to find the best job opportunities.

Focus on:
- Remote enterprise sales positions in AI/technology companies
- Dallas/Fort Worth area technology companies
- Companies that value both sales excellence and technical credibility
- Enterprise software, SaaS, AI/ML, and data analytics companies
- Strategic account executive, enterprise sales, and sales director roles

Output {HOW_MANY_SEARCHES} targeted search terms that will uncover the best opportunities."""

class JobSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to find relevant job opportunities.")
    query: str = Field(description="The search term to use for the web search.")

class JobSearchPlan(BaseModel):
    searches: list[JobSearchItem] = Field(description="A list of web searches to perform to find the best job opportunities.")
    
job_planner_agent = Agent(
    name="JobSearchPlannerAgent",
    instructions=INSTRUCTIONS,
    model="gpt-4o",
    output_type=JobSearchPlan,
)

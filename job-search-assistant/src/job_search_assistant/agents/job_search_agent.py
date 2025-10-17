from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add utilities directory to path for date_manager import
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent
utilities_dir = project_root / "utilities"
sys.path.append(str(utilities_dir))

from date_manager import get_formatted_date

# Get current date for search context
CURRENT_DATE = get_formatted_date('standard')
CURRENT_YEAR = get_formatted_date('iso')[:4]

INSTRUCTIONS = (
    "You are a specialized job search research assistant. Given a search term, you search the web for job opportunities "
    "and produce a detailed summary of the results. Focus on finding specific job postings, company information, "
    "and relevant details that would help a candidate evaluate opportunities.\n\n"
    "Your summary should include:\n"
    "- Specific job titles and companies found\n"
    "- Key requirements and qualifications\n"
    "- Location and remote work options\n"
    "- Company size and stage\n"
    "- Salary ranges if available\n"
    "- Application links or contact information\n\n"
    "Write 3-4 paragraphs, up to 400 words. Be specific and actionable. Capture the most relevant opportunities "
    "and provide enough detail for the candidate to evaluate each opportunity.\n\n"
    f"IMPORTANT DATE CONTEXT:\n"
    f"- Current Date: {CURRENT_DATE}\n"
    f"- Current Year: {CURRENT_YEAR}\n"
    f"- Search for the most recent job postings available\n"
    f"- Prioritize job listings from {CURRENT_YEAR} and recent months\n"
    f"- Include terms like 'latest', 'recent', 'current', '{CURRENT_YEAR}' in searches\n"
    f"- Focus on active job postings, not expired ones\n"
    f"- Look for recent company hiring announcements and job fairs"
)

job_search_agent = Agent(
    name="JobSearchAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o",
    model_settings=ModelSettings(tool_choice="required"),
)

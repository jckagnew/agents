#!/usr/bin/env python3
"""
Date-Aware Search Agent Template
Template for creating search agents with current date context
"""

from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for date_manager import
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from date_manager import get_formatted_date

# Get current date for search context
CURRENT_DATE = get_formatted_date('standard')
CURRENT_YEAR = get_formatted_date('iso')[:4]

INSTRUCTIONS = (
    "You are a research assistant. Given a search term, you search the web for that term and "
    "produce a concise summary of the results. The summary must 2-3 paragraphs and less than 300 "
    "words. Capture the main points. Write succinctly, no need to have complete sentences or good "
    "grammar. This will be consumed by someone synthesizing a report, so it's vital you capture the "
    "essence and ignore any fluff. Do not include any additional commentary other than the summary itself.\n\n"
    f"IMPORTANT DATE CONTEXT:\n"
    f"- Current Date: {CURRENT_DATE}\n"
    f"- Current Year: {CURRENT_YEAR}\n"
    f"- Search for the most recent information available\n"
    f"- Prioritize data from {CURRENT_YEAR} and recent months\n"
    f"- Include terms like 'latest', 'recent', 'current', '{CURRENT_YEAR}' in searches\n"
    f"- Avoid outdated information from previous years unless specifically requested"
)

search_agent = Agent(
    name="Date-Aware Search Agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)

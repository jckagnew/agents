#!/usr/bin/env python3
"""
Smart Writing Agent Template
Template for creating writing agents with intelligent date handling
"""

from agents import Agent, WebSearchTool, ModelSettings
import sys
from pathlib import Path

# Add parent directory to path for smart_date_manager import
current_dir = Path(__file__).parent
parent_dir = current_dir.parent.parent
sys.path.append(str(parent_dir))

from smart_date_manager import SmartDateManager, create_smart_writing_agent_instructions

# Initialize smart date manager
smart_date_manager = SmartDateManager()

# Base instructions for a writing agent
BASE_INSTRUCTIONS = (
    "You are a professional writer. Create high-quality, well-structured content "
    "based on the provided requirements and context."
)

# Create smart instructions with date awareness
INSTRUCTIONS = create_smart_writing_agent_instructions(BASE_INSTRUCTIONS, "general")

# Create the agent
writing_agent = Agent(
    name="Smart Writing Agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="medium")],
    model="gpt-4o",
    model_settings=ModelSettings(tool_choice="optional"),
)

# Example usage
if __name__ == "__main__":
    print("📝 Smart Writing Agent Template")
    print("=" * 50)
    print(f"Current Date: {smart_date_manager.current_date}")
    print(f"Current Year: {smart_date_manager.current_year}")
    print("\nAgent Instructions:")
    print(INSTRUCTIONS[:200] + "...")

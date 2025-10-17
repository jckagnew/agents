# 🎯 Job Search Assistant

AI-powered job search assistant designed specifically for finding remote enterprise sales positions in AI/technology companies.

## 🎯 Purpose

This tool helps Jack Agnew find the best enterprise sales opportunities that match his unique profile:
- 20 years of enterprise sales experience
- Hands-on AI technology development skills
- Preference for remote work or Dallas/Fort Worth area
- Focus on AI/technology companies

## 🚀 Features

- **Intelligent Search Planning**: Uses GPT-4o to plan 20 targeted job searches
- **Comprehensive Research**: Searches multiple job boards and company websites
- **Smart Analysis**: Ranks opportunities by fit score and provides detailed insights
- **Email Reports**: Automatically sends findings via email
- **Remote Focus**: Prioritizes remote and Dallas-area opportunities

## 🛠️ Technology Stack

- **AI Framework**: OpenAI Agents SDK with GPT-4o
- **Search Engine**: WebSearchTool for comprehensive job research
- **Email**: SendGrid for automated report delivery
- **Data Storage**: Pydantic models for structured data
- **Async Processing**: Asyncio for efficient parallel searches

## 📁 Project Structure

```
job-search-assistant/
├── src/
│   ├── agents/           # AI agents for job search
│   ├── data/            # Job requirements and profiles
│   ├── templates/       # Email and report templates
│   └── utils/           # Utility functions
├── main.py              # Main application
├── pyproject.toml       # Project configuration
└── README.md           # This file
```

## 🚀 Quick Start

1. **Install dependencies**:
   ```bash
   uv add agents openai pydantic python-dotenv sendgrid
   ```

2. **Set up environment variables**:
   ```bash
   cp ../.env .env
   ```

3. **Run the job search**:
   ```bash
   uv run python main.py
   ```

## 📊 What It Does

1. **Plans 20 targeted searches** based on your profile
2. **Searches job boards** for relevant positions
3. **Analyzes opportunities** and ranks by fit score
4. **Generates comprehensive report** with top opportunities
5. **Sends email report** to jack@clevelsalesguy.com

## 🎯 Target Companies

- AI/ML platforms and solutions
- Enterprise SaaS companies
- Data analytics and business intelligence
- Customer experience management
- Sales technology and automation

## 📧 Output

The tool generates a detailed report including:
- Top 5-10 job opportunities ranked by fit
- Company information and requirements
- Application instructions
- Market insights and trends
- Recommended next steps

## 🔧 Customization

Edit `src/data/job_requirements.md` to modify:
- Target job titles
- Geographic preferences
- Company criteria
- Skill requirements

## 📞 Support

For questions or issues, contact Jack Agnew at jack@clevelsalesguy.com

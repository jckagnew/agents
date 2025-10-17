from agents import Runner, trace, gen_trace_id
from .agents.job_planner_agent import job_planner_agent, JobSearchPlan
from .agents.job_search_agent import job_search_agent
from .agents.job_analyzer_agent import job_analyzer_agent, JobAnalysisReport
from .agents.job_email_agent import job_email_agent
import asyncio

class JobSearchManager:
    """Manages the complete job search process using AI agents"""

    async def run_job_search(self, candidate_profile: str = None):
        """Run the complete job search process"""
        trace_id = gen_trace_id()
        with trace("Job Search Trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            
            print("🎯 Starting comprehensive job search...")
            yield "🎯 Starting comprehensive job search..."
            
            # Load candidate profile if not provided
            if not candidate_profile:
                with open('src/data/job_requirements.md', 'r') as f:
                    candidate_profile = f.read()
            
            # Step 1: Plan searches
            print("📋 Planning targeted job searches...")
            yield "📋 Planning targeted job searches..."
            search_plan = await self.plan_searches(candidate_profile)
            yield f"✅ Planned {len(search_plan.searches)} targeted searches"
            
            # Step 2: Execute searches
            print("🔍 Executing job searches...")
            yield "🔍 Executing job searches..."
            search_results = await self.perform_searches(search_plan)
            yield f"✅ Completed {len(search_results)} searches"
            
            # Step 3: Analyze results
            print("📊 Analyzing job opportunities...")
            yield "📊 Analyzing job opportunities..."
            analysis = await self.analyze_opportunities(candidate_profile, search_results)
            yield "✅ Analysis complete"
            
            # Step 4: Send email report
            print("📧 Sending email report...")
            yield "📧 Sending email report..."
            await self.send_report(analysis)
            yield "✅ Email sent"
            
            # Return final report
            yield "🎉 Job search complete! Here's your comprehensive report:"
            yield analysis.markdown_report

    async def plan_searches(self, candidate_profile: str) -> JobSearchPlan:
        """Plan targeted job searches based on candidate profile"""
        result = await Runner.run(
            job_planner_agent,
            f"Candidate Profile: {candidate_profile}",
        )
        return result.final_output_as(JobSearchPlan)

    async def perform_searches(self, search_plan: JobSearchPlan) -> list[str]:
        """Execute all planned searches"""
        tasks = [asyncio.create_task(self.search_job(item)) for item in search_plan.searches]
        results = []
        
        for i, task in enumerate(asyncio.as_completed(tasks), 1):
            result = await task
            if result:
                results.append(result)
            print(f"Search progress: {i}/{len(tasks)} completed")
        
        return results

    async def search_job(self, search_item) -> str | None:
        """Execute a single job search"""
        input_text = f"Search term: {search_item.query}\nReason: {search_item.reason}"
        try:
            result = await Runner.run(job_search_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            print(f"Search failed for '{search_item.query}': {e}")
            return None

    async def analyze_opportunities(self, candidate_profile: str, search_results: list[str]) -> JobAnalysisReport:
        """Analyze job search results and create comprehensive report"""
        input_text = f"Candidate Profile: {candidate_profile}\n\nSearch Results: {search_results}"
        result = await Runner.run(job_analyzer_agent, input_text)
        return result.final_output_as(JobAnalysisReport)

    async def send_report(self, analysis: JobAnalysisReport) -> None:
        """Send the job search report via email"""
        await Runner.run(job_email_agent, analysis.markdown_report)

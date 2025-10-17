"""
Analyst Agent - Database and Data Analysis Specialist for Advanced Agentic RAG Pipeline

This agent specializes in structured data analysis, SQL querying, and statistical analysis.
Based on the advanced agentic RAG pipeline principles from Fareed Khan's research.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import logging
import pandas as pd
import numpy as np

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent
sys.path.append(str(project_root))

from date_manager import get_formatted_date
from agents import Agent, WebSearchTool, ModelSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalystAgent:
    """
    Specialist agent for structured data analysis and database operations.
    
    Capabilities:
    - SQL query generation and execution
    - Statistical analysis and trend identification
    - Data validation and cleaning
    - Financial analysis and reporting
    - Predictive modeling and forecasting
    """
    
    def __init__(self, database_connection=None, data_sources=None):
        self.database_connection = database_connection
        self.data_sources = data_sources or {}
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        self.current_quarter = self._get_current_quarter()
        
        # Initialize tools
        self.tools = [
            WebSearchTool(search_context_size="medium"),
            # Add more specialized tools as needed
        ]
        
        # Initialize the CrewAI agent
        self.agent = Agent(
            name="Analyst",
            role="Data Analysis Specialist",
            goal="Analyze structured data, generate insights, and provide statistical analysis with high accuracy",
            backstory="""You are an expert data analyst and database specialist with deep expertise in:
            - SQL query generation and optimization
            - Statistical analysis and trend identification
            - Financial analysis and reporting
            - Data validation and quality assurance
            - Predictive modeling and forecasting
            
            You excel at extracting insights from complex datasets,
            identifying patterns and trends, and providing actionable
            recommendations based on data analysis.""",
            tools=self.tools,
            model="gpt-4o",
            model_settings=ModelSettings(tool_choice="required"),
            verbose=True
        )
    
    def analyze_data(self, query: str, data_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Comprehensive data analysis process.
        
        Args:
            query: Analysis query or request
            data_context: Context about the data to analyze
            
        Returns:
            Dictionary containing analysis results and insights
        """
        logger.info(f"Analyst: Starting data analysis for query: {query}")
        
        # Step 1: Generate SQL queries
        sql_queries = self._generate_sql_queries(query, data_context)
        
        # Step 2: Execute queries and retrieve data
        data_results = self._execute_queries(sql_queries)
        
        # Step 3: Perform statistical analysis
        statistical_analysis = self._perform_statistical_analysis(data_results, query)
        
        # Step 4: Identify trends and patterns
        trend_analysis = self._identify_trends(data_results, query)
        
        # Step 5: Generate insights and recommendations
        insights = self._generate_insights(statistical_analysis, trend_analysis, query)
        
        return {
            "query": query,
            "sql_queries": sql_queries,
            "data_results": data_results,
            "statistical_analysis": statistical_analysis,
            "trend_analysis": trend_analysis,
            "insights": insights,
            "metadata": {
                "analysis_timestamp": datetime.now().isoformat(),
                "current_date": self.current_date,
                "current_quarter": self.current_quarter,
                "analysis_method": "comprehensive_data_analysis"
            }
        }
    
    def _generate_sql_queries(self, query: str, data_context: Dict[str, Any] = None) -> List[str]:
        """Generate SQL queries based on the analysis request."""
        logger.info("Analyst: Generating SQL queries")
        
        # Enhanced query with date context
        enhanced_query = f"{query} {self.current_year} {self.current_quarter} recent current"
        
        # Create SQL generation prompt
        sql_prompt = f"""
        Based on the following analysis request: "{enhanced_query}"
        
        Generate appropriate SQL queries for data analysis. Consider:
        1. Current date context: {self.current_date}
        2. Current quarter: {self.current_quarter}
        3. Recent trends and patterns
        4. Statistical analysis requirements
        
        Provide 2-3 SQL queries that would help answer this analysis request.
        Focus on:
        - Time-based filtering (recent data)
        - Aggregation and grouping
        - Statistical calculations
        - Trend analysis
        
        SQL Queries:
        """
        
        # Use the agent to generate SQL queries
        sql_response = self.agent.execute_task(sql_prompt)
        
        # Parse SQL queries from response (simplified parsing)
        sql_queries = self._parse_sql_queries(sql_response)
        
        return sql_queries
    
    def _execute_queries(self, sql_queries: List[str]) -> List[Dict[str, Any]]:
        """Execute SQL queries and retrieve data."""
        logger.info("Analyst: Executing SQL queries")
        
        results = []
        for i, query in enumerate(sql_queries):
            try:
                # In a real implementation, this would execute against a database
                # For now, we'll simulate the results
                result = {
                    "query_id": i + 1,
                    "query": query,
                    "status": "success",
                    "data": self._simulate_query_result(query),
                    "execution_time": 0.1,  # Simulated
                    "row_count": 10  # Simulated
                }
                results.append(result)
            except Exception as e:
                logger.error(f"Error executing query {i + 1}: {e}")
                results.append({
                    "query_id": i + 1,
                    "query": query,
                    "status": "error",
                    "error": str(e),
                    "data": None
                })
        
        return results
    
    def _perform_statistical_analysis(self, data_results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """Perform statistical analysis on the retrieved data."""
        logger.info("Analyst: Performing statistical analysis")
        
        # Combine all data for analysis
        all_data = []
        for result in data_results:
            if result["status"] == "success" and result["data"]:
                all_data.extend(result["data"])
        
        if not all_data:
            return {"error": "No data available for statistical analysis"}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(all_data)
        
        # Perform basic statistical analysis
        statistical_summary = {
            "descriptive_stats": df.describe().to_dict() if not df.empty else {},
            "correlation_matrix": df.corr().to_dict() if len(df.columns) > 1 else {},
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.to_dict(),
            "shape": df.shape
        }
        
        # Calculate additional metrics
        if "value" in df.columns:
            statistical_summary["value_analysis"] = {
                "mean": df["value"].mean(),
                "median": df["value"].median(),
                "std": df["value"].std(),
                "min": df["value"].min(),
                "max": df["value"].max(),
                "quartiles": df["value"].quantile([0.25, 0.5, 0.75]).to_dict()
            }
        
        return statistical_summary
    
    def _identify_trends(self, data_results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """Identify trends and patterns in the data."""
        logger.info("Analyst: Identifying trends and patterns")
        
        # Combine all data for trend analysis
        all_data = []
        for result in data_results:
            if result["status"] == "success" and result["data"]:
                all_data.extend(result["data"])
        
        if not all_data:
            return {"error": "No data available for trend analysis"}
        
        df = pd.DataFrame(all_data)
        
        trend_analysis = {
            "time_series_trends": {},
            "seasonal_patterns": {},
            "growth_rates": {},
            "anomalies": []
        }
        
        # Analyze time series trends if date column exists
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values("date")
            
            # Calculate growth rates
            if "value" in df.columns:
                df["growth_rate"] = df["value"].pct_change()
                trend_analysis["growth_rates"] = {
                    "average_growth": df["growth_rate"].mean(),
                    "recent_growth": df["growth_rate"].tail(3).mean(),
                    "volatility": df["growth_rate"].std()
                }
        
        # Identify anomalies (simplified)
        if "value" in df.columns:
            mean_val = df["value"].mean()
            std_val = df["value"].std()
            threshold = 2 * std_val
            anomalies = df[abs(df["value"] - mean_val) > threshold]
            trend_analysis["anomalies"] = anomalies.to_dict("records")
        
        return trend_analysis
    
    def _generate_insights(self, statistical_analysis: Dict[str, Any], trend_analysis: Dict[str, Any], query: str) -> str:
        """Generate insights and recommendations based on the analysis."""
        logger.info("Analyst: Generating insights and recommendations")
        
        # Create insights generation prompt
        insights_prompt = f"""
        Based on the following data analysis for the query "{query}":
        
        Statistical Analysis:
        {json.dumps(statistical_analysis, indent=2)}
        
        Trend Analysis:
        {json.dumps(trend_analysis, indent=2)}
        
        Current Context:
        - Current Date: {self.current_date}
        - Current Quarter: {self.current_quarter}
        
        Provide comprehensive insights and recommendations that:
        1. Summarize key findings from the statistical analysis
        2. Highlight important trends and patterns
        3. Identify anomalies or unusual data points
        4. Provide actionable recommendations
        5. Suggest areas for further investigation
        
        Focus on business value and practical applications.
        """
        
        # Use the agent to generate insights
        insights_response = self.agent.execute_task(insights_prompt)
        
        return insights_response
    
    def _parse_sql_queries(self, sql_response: str) -> List[str]:
        """Parse SQL queries from the agent response."""
        # Simple parsing - in practice, this would be more sophisticated
        lines = sql_response.split('\n')
        queries = []
        current_query = []
        
        for line in lines:
            line = line.strip()
            if line.upper().startswith('SELECT') or line.upper().startswith('WITH'):
                if current_query:
                    queries.append('\n'.join(current_query))
                current_query = [line]
            elif current_query and line:
                current_query.append(line)
            elif current_query and not line:
                queries.append('\n'.join(current_query))
                current_query = []
        
        if current_query:
            queries.append('\n'.join(current_query))
        
        return queries
    
    def _simulate_query_result(self, query: str) -> List[Dict[str, Any]]:
        """Simulate query results for testing purposes."""
        # This would be replaced with actual database execution
        return [
            {"date": "2025-01-01", "value": 100, "category": "A"},
            {"date": "2025-01-02", "value": 105, "category": "A"},
            {"date": "2025-01-03", "value": 98, "category": "B"},
            {"date": "2025-01-04", "value": 110, "category": "A"},
            {"date": "2025-01-05", "value": 95, "category": "B"},
        ]
    
    def _get_current_quarter(self) -> str:
        """Get current quarter string."""
        month = datetime.now().month
        quarter = (month - 1) // 3 + 1
        return f"Q{quarter}"
    
    def get_agent_instructions(self) -> str:
        """Get detailed instructions for the Analyst agent."""
        return f"""
        ANALYST AGENT INSTRUCTIONS:
        
        You are a specialized data analysis expert with expertise in:
        - SQL query generation and optimization
        - Statistical analysis and trend identification
        - Financial analysis and reporting
        - Data validation and quality assurance
        - Predictive modeling and forecasting
        
        CURRENT CONTEXT:
        - Current Date: {self.current_date}
        - Current Year: {self.current_year}
        - Current Quarter: {self.current_quarter}
        
        ANALYSIS METHODOLOGY:
        1. Generate appropriate SQL queries for data retrieval
        2. Execute queries and validate data quality
        3. Perform comprehensive statistical analysis
        4. Identify trends, patterns, and anomalies
        5. Generate actionable insights and recommendations
        
        QUALITY STANDARDS:
        - Prioritize recent and current data
        - Validate data quality and completeness
        - Use appropriate statistical methods
        - Identify meaningful patterns and trends
        - Provide actionable business insights
        - Highlight anomalies and potential issues
        
        When analyzing data:
        - Always consider current date and quarter context
        - Focus on recent trends and patterns
        - Validate data quality and completeness
        - Use appropriate statistical methods
        - Provide clear, actionable insights
        - Highlight important findings and recommendations
        """

# Example usage and testing
if __name__ == "__main__":
    print("📊 Analyst Agent Test")
    print("====================")
    
    # Initialize the analyst agent
    analyst = AnalystAgent()
    
    # Test analysis functionality
    test_query = "analyze sales performance trends for Q1 2025"
    results = analyst.analyze_data(test_query)
    
    print(f"Query: {test_query}")
    print(f"SQL Queries Generated: {len(results['sql_queries'])}")
    print(f"Data Results: {len(results['data_results'])}")
    print(f"Statistical Analysis: {bool(results['statistical_analysis'])}")
    print(f"Trend Analysis: {bool(results['trend_analysis'])}")
    print(f"Insights: {results['insights'][:200]}...")
    
    print("\nAgent Instructions:")
    print(analyst.get_agent_instructions())

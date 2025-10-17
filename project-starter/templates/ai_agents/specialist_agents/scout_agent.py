"""
Scout Agent - Live Data and Real-time Information Specialist for Advanced Agentic RAG Pipeline

This agent specializes in real-time web data collection, news monitoring, and live information gathering.
Based on the advanced agentic RAG pipeline principles from Fareed Khan's research.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json
import logging
import requests
from bs4 import BeautifulSoup

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent
sys.path.append(str(project_root))

from date_manager import get_formatted_date
from agents import Agent, WebSearchTool, ModelSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScoutAgent:
    """
    Specialist agent for real-time data collection and live information gathering.
    
    Capabilities:
    - Real-time web search and data collection
    - News monitoring and analysis
    - Social media trend tracking
    - API integration and data fetching
    - Live data validation and freshness checking
    """
    
    def __init__(self, api_keys: Dict[str, str] = None):
        self.api_keys = api_keys or {}
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        self.current_datetime = datetime.now()
        
        # Initialize tools
        self.tools = [
            WebSearchTool(search_context_size="high"),
            # Add more specialized tools as needed
        ]
        
        # Initialize the CrewAI agent
        self.agent = Agent(
            name="Scout",
            role="Live Data Collection Specialist",
            goal="Gather real-time information, monitor trends, and provide up-to-date insights from live sources",
            backstory="""You are an expert scout and real-time data specialist with deep expertise in:
            - Live web data collection and monitoring
            - News and social media trend analysis
            - API integration and real-time data fetching
            - Data freshness validation and quality assurance
            - Market intelligence and competitive monitoring
            
            You excel at finding the most current information,
            monitoring live trends, and providing real-time insights
            that are accurate and up-to-date.""",
            tools=self.tools,
            model="gpt-4o",
            model_settings=ModelSettings(tool_choice="required"),
            verbose=True
        )
    
    def gather_live_data(self, query: str, sources: List[str] = None, time_window: str = "24h") -> Dict[str, Any]:
        """
        Comprehensive live data gathering process.
        
        Args:
            query: Information query or topic to monitor
            sources: Specific sources to monitor (optional)
            time_window: Time window for data collection (e.g., "24h", "7d", "30d")
            
        Returns:
            Dictionary containing live data and insights
        """
        logger.info(f"Scout: Starting live data gathering for query: {query}")
        
        # Step 1: Real-time web search
        web_results = self._perform_live_search(query, time_window)
        
        # Step 2: News monitoring
        news_results = self._monitor_news(query, time_window)
        
        # Step 3: Social media monitoring
        social_results = self._monitor_social_media(query, time_window)
        
        # Step 4: API data collection
        api_results = self._collect_api_data(query, sources)
        
        # Step 5: Data freshness validation
        validated_results = self._validate_data_freshness(web_results, news_results, social_results, api_results)
        
        # Step 6: Trend analysis
        trend_analysis = self._analyze_trends(validated_results, query)
        
        # Step 7: Generate live insights
        live_insights = self._generate_live_insights(validated_results, trend_analysis, query)
        
        return {
            "query": query,
            "time_window": time_window,
            "web_results": web_results,
            "news_results": news_results,
            "social_results": social_results,
            "api_results": api_results,
            "validated_results": validated_results,
            "trend_analysis": trend_analysis,
            "live_insights": live_insights,
            "metadata": {
                "collection_timestamp": datetime.now().isoformat(),
                "current_date": self.current_date,
                "data_freshness": self._calculate_data_freshness(validated_results),
                "collection_method": "comprehensive_live_monitoring"
            }
        }
    
    def _perform_live_search(self, query: str, time_window: str) -> List[Dict[str, Any]]:
        """Perform real-time web search with time filtering."""
        logger.info("Scout: Performing live web search")
        
        # Enhanced query with time context
        time_context = self._get_time_context(time_window)
        enhanced_query = f"{query} {time_context} {self.current_year} latest recent current"
        
        # Use WebSearchTool for live search
        search_results = self.agent.tools[0].search(enhanced_query)
        
        # Process and structure results
        structured_results = []
        for result in search_results:
            structured_results.append({
                "content": result.get("content", ""),
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "relevance_score": result.get("relevance_score", 0.0),
                "source_type": "web_search",
                "timestamp": datetime.now().isoformat(),
                "freshness_score": self._calculate_freshness_score(result)
            })
        
        return structured_results
    
    def _monitor_news(self, query: str, time_window: str) -> List[Dict[str, Any]]:
        """Monitor news sources for relevant information."""
        logger.info("Scout: Monitoring news sources")
        
        # Enhanced query for news monitoring
        news_query = f"{query} news {self.current_year} latest breaking"
        
        # Use WebSearchTool for news search
        news_results = self.agent.tools[0].search(news_query)
        
        # Process news results
        structured_news = []
        for result in news_results:
            structured_news.append({
                "content": result.get("content", ""),
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "source_type": "news",
                "timestamp": datetime.now().isoformat(),
                "freshness_score": self._calculate_freshness_score(result),
                "news_category": self._categorize_news(result)
            })
        
        return structured_news
    
    def _monitor_social_media(self, query: str, time_window: str) -> List[Dict[str, Any]]:
        """Monitor social media for trends and discussions."""
        logger.info("Scout: Monitoring social media")
        
        # Enhanced query for social media monitoring
        social_query = f"{query} social media trends {self.current_year} latest"
        
        # Use WebSearchTool for social media search
        social_results = self.agent.tools[0].search(social_query)
        
        # Process social media results
        structured_social = []
        for result in social_results:
            structured_social.append({
                "content": result.get("content", ""),
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "source_type": "social_media",
                "timestamp": datetime.now().isoformat(),
                "freshness_score": self._calculate_freshness_score(result),
                "engagement_indicators": self._extract_engagement_indicators(result)
            })
        
        return structured_social
    
    def _collect_api_data(self, query: str, sources: List[str] = None) -> List[Dict[str, Any]]:
        """Collect data from various APIs."""
        logger.info("Scout: Collecting API data")
        
        api_results = []
        
        # Example API integrations (would be expanded based on available APIs)
        if "financial" in query.lower() and "ALPHA_VANTAGE_API_KEY" in self.api_keys:
            api_results.extend(self._fetch_financial_data(query))
        
        if "news" in query.lower() and "NEWS_API_KEY" in self.api_keys:
            api_results.extend(self._fetch_news_api_data(query))
        
        if "social" in query.lower() and "TWITTER_API_KEY" in self.api_keys:
            api_results.extend(self._fetch_social_media_data(query))
        
        return api_results
    
    def _validate_data_freshness(self, *result_sets) -> List[Dict[str, Any]]:
        """Validate and filter results based on data freshness."""
        logger.info("Scout: Validating data freshness")
        
        all_results = []
        for result_set in result_sets:
            all_results.extend(result_set)
        
        # Filter results based on freshness
        fresh_results = []
        for result in all_results:
            freshness_score = result.get("freshness_score", 0)
            if freshness_score > 0.5:  # Threshold for freshness
                fresh_results.append(result)
        
        # Sort by freshness score
        fresh_results.sort(key=lambda x: x.get("freshness_score", 0), reverse=True)
        
        return fresh_results
    
    def _analyze_trends(self, results: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
        """Analyze trends from the collected data."""
        logger.info("Scout: Analyzing trends")
        
        # Group results by source type
        source_groups = {}
        for result in results:
            source_type = result.get("source_type", "unknown")
            if source_type not in source_groups:
                source_groups[source_type] = []
            source_groups[source_type].append(result)
        
        # Analyze trends for each source type
        trend_analysis = {
            "source_breakdown": {source: len(results) for source, results in source_groups.items()},
            "trending_topics": self._extract_trending_topics(results),
            "sentiment_analysis": self._analyze_sentiment(results),
            "volume_trends": self._analyze_volume_trends(results),
            "key_insights": []
        }
        
        return trend_analysis
    
    def _generate_live_insights(self, results: List[Dict[str, Any]], trend_analysis: Dict[str, Any], query: str) -> str:
        """Generate live insights from the collected data."""
        logger.info("Scout: Generating live insights")
        
        # Create insights generation prompt
        insights_prompt = f"""
        Based on the following live data collection for the query "{query}":
        
        Collected Results: {len(results)} items
        Trend Analysis: {json.dumps(trend_analysis, indent=2)}
        
        Current Context:
        - Current Date: {self.current_date}
        - Collection Time: {datetime.now().isoformat()}
        
        Provide comprehensive live insights that:
        1. Summarize the most current and relevant information
        2. Highlight emerging trends and patterns
        3. Identify breaking news or significant developments
        4. Assess data quality and reliability
        5. Provide actionable recommendations based on live data
        
        Focus on real-time value and current relevance.
        """
        
        # Use the agent to generate insights
        insights_response = self.agent.execute_task(insights_prompt)
        
        return insights_response
    
    def _get_time_context(self, time_window: str) -> str:
        """Get time context string for search queries."""
        if time_window == "24h":
            return "last 24 hours today"
        elif time_window == "7d":
            return "last week past 7 days"
        elif time_window == "30d":
            return "last month past 30 days"
        else:
            return "recent latest"
    
    def _calculate_freshness_score(self, result: Dict[str, Any]) -> float:
        """Calculate freshness score for a result."""
        # This would be implemented based on actual timestamp extraction
        # For now, return a simulated score
        return 0.8  # Simulated freshness score
    
    def _categorize_news(self, result: Dict[str, Any]) -> str:
        """Categorize news content."""
        # Simple categorization based on content keywords
        content = result.get("content", "").lower()
        if any(word in content for word in ["breaking", "urgent", "alert"]):
            return "breaking"
        elif any(word in content for word in ["analysis", "opinion", "commentary"]):
            return "analysis"
        else:
            return "general"
    
    def _extract_engagement_indicators(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract engagement indicators from social media content."""
        # This would be implemented based on actual social media API data
        return {
            "likes": 0,
            "shares": 0,
            "comments": 0,
            "engagement_rate": 0.0
        }
    
    def _extract_trending_topics(self, results: List[Dict[str, Any]]) -> List[str]:
        """Extract trending topics from the results."""
        # Simple keyword extraction for trending topics
        all_content = " ".join([result.get("content", "") for result in results])
        # This would be implemented with more sophisticated NLP
        return ["trending_topic_1", "trending_topic_2"]
    
    def _analyze_sentiment(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Analyze sentiment of the collected data."""
        # This would be implemented with actual sentiment analysis
        return {
            "positive": 0.6,
            "negative": 0.2,
            "neutral": 0.2
        }
    
    def _analyze_volume_trends(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze volume trends in the data."""
        # This would be implemented with actual volume analysis
        return {
            "peak_hours": ["09:00", "14:00", "20:00"],
            "volume_trend": "increasing",
            "peak_sources": ["web_search", "news"]
        }
    
    def _calculate_data_freshness(self, results: List[Dict[str, Any]]) -> float:
        """Calculate overall data freshness score."""
        if not results:
            return 0.0
        
        freshness_scores = [result.get("freshness_score", 0) for result in results]
        return sum(freshness_scores) / len(freshness_scores)
    
    def _fetch_financial_data(self, query: str) -> List[Dict[str, Any]]:
        """Fetch financial data from APIs."""
        # This would be implemented with actual financial API calls
        return []
    
    def _fetch_news_api_data(self, query: str) -> List[Dict[str, Any]]:
        """Fetch news data from APIs."""
        # This would be implemented with actual news API calls
        return []
    
    def _fetch_social_media_data(self, query: str) -> List[Dict[str, Any]]:
        """Fetch social media data from APIs."""
        # This would be implemented with actual social media API calls
        return []
    
    def get_agent_instructions(self) -> str:
        """Get detailed instructions for the Scout agent."""
        return f"""
        SCOUT AGENT INSTRUCTIONS:
        
        You are a specialized live data collection expert with expertise in:
        - Real-time web data collection and monitoring
        - News and social media trend analysis
        - API integration and real-time data fetching
        - Data freshness validation and quality assurance
        - Market intelligence and competitive monitoring
        
        CURRENT CONTEXT:
        - Current Date: {self.current_date}
        - Current Year: {self.current_year}
        - Collection Time: {self.current_datetime.isoformat()}
        
        COLLECTION METHODOLOGY:
        1. Perform real-time web search with time filtering
        2. Monitor news sources for breaking developments
        3. Track social media trends and discussions
        4. Collect data from relevant APIs
        5. Validate data freshness and quality
        6. Analyze trends and patterns
        7. Generate live insights and recommendations
        
        QUALITY STANDARDS:
        - Prioritize the most current and recent information
        - Validate data freshness and reliability
        - Monitor multiple sources for comprehensive coverage
        - Identify emerging trends and breaking developments
        - Provide real-time insights and actionable intelligence
        
        When collecting live data:
        - Always focus on current and recent information
        - Use time-based filtering to ensure freshness
        - Monitor multiple sources for comprehensive coverage
        - Validate data quality and reliability
        - Identify trends and patterns in real-time
        - Provide actionable insights based on live data
        """

# Example usage and testing
if __name__ == "__main__":
    print("🔍 Scout Agent Test")
    print("==================")
    
    # Initialize the scout agent
    scout = ScoutAgent()
    
    # Test live data gathering
    test_query = "artificial intelligence developments"
    results = scout.gather_live_data(test_query, time_window="24h")
    
    print(f"Query: {test_query}")
    print(f"Web Results: {len(results['web_results'])}")
    print(f"News Results: {len(results['news_results'])}")
    print(f"Social Results: {len(results['social_results'])}")
    print(f"API Results: {len(results['api_results'])}")
    print(f"Validated Results: {len(results['validated_results'])}")
    print(f"Data Freshness: {results['metadata']['data_freshness']:.2f}")
    print(f"Live Insights: {results['live_insights'][:200]}...")
    
    print("\nAgent Instructions:")
    print(scout.get_agent_instructions())

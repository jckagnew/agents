"""
Librarian Agent - Document Specialist for Advanced Agentic RAG Pipeline

This agent specializes in document retrieval, analysis, and knowledge extraction.
Based on the advanced agentic RAG pipeline principles from Fareed Khan's research.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import logging

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent
sys.path.append(str(project_root))

from date_manager import get_formatted_date
from agents import Agent, WebSearchTool, ModelSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LibrarianAgent:
    """
    Specialist agent for document retrieval and analysis.
    
    Capabilities:
    - Multi-step document search
    - Structure-aware document processing
    - Metadata extraction and enhancement
    - Cross-reference validation
    - Document summarization
    """
    
    def __init__(self, vector_store=None, document_store=None):
        self.vector_store = vector_store
        self.document_store = document_store
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        
        # Initialize tools
        self.tools = [
            WebSearchTool(search_context_size="medium"),
            # Add more specialized tools as needed
        ]
        
        # Initialize the CrewAI agent
        self.agent = Agent(
            name="Librarian",
            role="Document Research Specialist",
            goal="Retrieve, analyze, and synthesize information from documents with high accuracy and context awareness",
            backstory="""You are an expert librarian and research specialist with deep expertise in:
            - Document retrieval and analysis
            - Information synthesis and summarization
            - Cross-reference validation
            - Metadata extraction and enhancement
            - Structure-aware document processing
            
            You excel at finding the most relevant information from complex documents,
            validating sources, and providing comprehensive yet concise summaries.""",
            tools=self.tools,
            model="gpt-4o",
            model_settings=ModelSettings(tool_choice="required"),
            verbose=True
        )
    
    def search_documents(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Multi-step document search process.
        
        Args:
            query: Search query
            context: Additional context for the search
            
        Returns:
            Dictionary containing search results and metadata
        """
        logger.info(f"Librarian: Starting document search for query: {query}")
        
        # Step 1: Semantic search
        semantic_results = self._semantic_search(query, context)
        
        # Step 2: Exact match verification
        exact_matches = self._exact_match_search(query, semantic_results)
        
        # Step 3: Metadata filtering
        filtered_results = self._metadata_filtering(exact_matches, context)
        
        # Step 4: Cross-reference validation
        validated_results = self._cross_reference_validation(filtered_results)
        
        # Step 5: Generate summary
        summary = self._generate_summary(validated_results, query)
        
        return {
            "query": query,
            "results": validated_results,
            "summary": summary,
            "metadata": {
                "search_timestamp": datetime.now().isoformat(),
                "total_results": len(validated_results),
                "search_method": "multi_step_librarian",
                "current_date": self.current_date
            }
        }
    
    def _semantic_search(self, query: str, context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Perform semantic search using vector similarity."""
        logger.info("Librarian: Performing semantic search")
        
        # Enhanced query with date context
        enhanced_query = f"{query} {self.current_year} recent current latest"
        
        # Use WebSearchTool for semantic search
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
                "timestamp": datetime.now().isoformat()
            })
        
        return structured_results
    
    def _exact_match_search(self, query: str, semantic_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Verify semantic results with exact match search."""
        logger.info("Librarian: Performing exact match verification")
        
        # Extract key terms for exact matching
        key_terms = self._extract_key_terms(query)
        
        verified_results = []
        for result in semantic_results:
            # Check for exact matches of key terms
            exact_matches = sum(1 for term in key_terms if term.lower() in result["content"].lower())
            result["exact_match_score"] = exact_matches / len(key_terms) if key_terms else 0
            
            # Only include results with some exact matches
            if result["exact_match_score"] > 0:
                verified_results.append(result)
        
        return verified_results
    
    def _metadata_filtering(self, results: List[Dict[str, Any]], context: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Filter results based on metadata criteria."""
        logger.info("Librarian: Applying metadata filtering")
        
        if not context:
            return results
        
        filtered_results = []
        for result in results:
            # Apply date filtering if specified
            if "date_range" in context:
                if self._is_within_date_range(result, context["date_range"]):
                    filtered_results.append(result)
            else:
                # Default: prioritize recent content
                if self._is_recent_content(result):
                    filtered_results.append(result)
        
        return filtered_results
    
    def _cross_reference_validation(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate results through cross-referencing."""
        logger.info("Librarian: Performing cross-reference validation")
        
        validated_results = []
        for result in results:
            # Check for consistency with other results
            consistency_score = self._calculate_consistency_score(result, results)
            result["consistency_score"] = consistency_score
            
            # Only include results with reasonable consistency
            if consistency_score > 0.3:  # Threshold for consistency
                validated_results.append(result)
        
        return validated_results
    
    def _generate_summary(self, results: List[Dict[str, Any]], query: str) -> str:
        """Generate a comprehensive summary of the search results."""
        logger.info("Librarian: Generating summary")
        
        if not results:
            return f"No relevant documents found for query: {query}"
        
        # Combine all content for summarization
        combined_content = "\n\n".join([result["content"] for result in results])
        
        # Create summary prompt
        summary_prompt = f"""
        Based on the following search results for the query "{query}", 
        provide a comprehensive summary that:
        
        1. Captures the main points and key information
        2. Identifies any patterns or trends
        3. Highlights important details and specifics
        4. Notes any contradictions or inconsistencies
        5. Provides context and relevance to the query
        
        Current Date: {self.current_date}
        Search Results:
        {combined_content}
        
        Summary:
        """
        
        # Use the agent to generate summary
        summary_response = self.agent.execute_task(summary_prompt)
        
        return summary_response
    
    def _extract_key_terms(self, query: str) -> List[str]:
        """Extract key terms from the query for exact matching."""
        # Simple key term extraction - could be enhanced with NLP
        words = query.lower().split()
        # Filter out common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        key_terms = [word for word in words if word not in stop_words and len(word) > 2]
        return key_terms
    
    def _is_within_date_range(self, result: Dict[str, Any], date_range: Dict[str, str]) -> bool:
        """Check if result is within specified date range."""
        # This would need to be implemented based on your date extraction logic
        # For now, return True as a placeholder
        return True
    
    def _is_recent_content(self, result: Dict[str, Any]) -> bool:
        """Check if content is recent (within last year)."""
        # This would need to be implemented based on your date extraction logic
        # For now, return True as a placeholder
        return True
    
    def _calculate_consistency_score(self, result: Dict[str, Any], all_results: List[Dict[str, Any]]) -> float:
        """Calculate consistency score for a result against all other results."""
        # Simple consistency check - could be enhanced with more sophisticated logic
        if len(all_results) <= 1:
            return 1.0
        
        # Check for common terms with other results
        result_terms = set(result["content"].lower().split())
        consistency_scores = []
        
        for other_result in all_results:
            if other_result != result:
                other_terms = set(other_result["content"].lower().split())
                common_terms = result_terms.intersection(other_terms)
                if len(result_terms) > 0:
                    consistency_scores.append(len(common_terms) / len(result_terms))
        
        return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0.0
    
    def get_agent_instructions(self) -> str:
        """Get detailed instructions for the Librarian agent."""
        return f"""
        LIBRARIAN AGENT INSTRUCTIONS:
        
        You are a specialized document research librarian with expertise in:
        - Multi-step document retrieval and analysis
        - Information synthesis and summarization
        - Cross-reference validation and verification
        - Metadata extraction and enhancement
        - Structure-aware document processing
        
        CURRENT CONTEXT:
        - Current Date: {self.current_date}
        - Current Year: {self.current_year}
        
        SEARCH METHODOLOGY:
        1. Perform semantic search using enhanced queries with date context
        2. Verify results with exact match search for key terms
        3. Apply metadata filtering based on relevance and recency
        4. Cross-reference results for consistency and accuracy
        5. Generate comprehensive summaries with key insights
        
        QUALITY STANDARDS:
        - Prioritize recent and current information
        - Validate information through multiple sources
        - Identify patterns, trends, and contradictions
        - Provide context and relevance to the query
        - Maintain high accuracy and reliability
        
        When searching for information:
        - Always include current year and date context in searches
        - Use terms like "latest", "recent", "current" to find up-to-date information
        - Cross-reference findings with multiple sources
        - Highlight any inconsistencies or contradictions
        - Provide comprehensive yet concise summaries
        """

# Example usage and testing
if __name__ == "__main__":
    print("📚 Librarian Agent Test")
    print("========================")
    
    # Initialize the librarian agent
    librarian = LibrarianAgent()
    
    # Test search functionality
    test_query = "artificial intelligence trends in healthcare"
    results = librarian.search_documents(test_query)
    
    print(f"Query: {test_query}")
    print(f"Results found: {len(results['results'])}")
    print(f"Summary: {results['summary'][:200]}...")
    
    print("\nAgent Instructions:")
    print(librarian.get_agent_instructions())

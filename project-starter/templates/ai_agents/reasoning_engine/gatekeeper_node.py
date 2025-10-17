"""
Gatekeeper Node - Ambiguity Detection and Query Validation for Advanced Agentic RAG Pipeline

This component validates queries before processing and detects ambiguity to ensure high-quality responses.
Based on the advanced agentic RAG pipeline principles from Fareed Khan's research.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import logging
import re

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent.parent
sys.path.append(str(project_root))

from date_manager import get_formatted_date
from agents import Agent, ModelSettings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GatekeeperNode:
    """
    Gatekeeper node for query validation and ambiguity detection.
    
    Capabilities:
    - Query clarity assessment
    - Ambiguity detection and resolution
    - Intent classification
    - Resource requirement estimation
    - Query routing to appropriate specialists
    """
    
    def __init__(self):
        self.current_date = get_formatted_date('standard')
        self.current_year = get_formatted_date('iso')[:4]
        
        # Initialize the CrewAI agent
        self.agent = Agent(
            name="Gatekeeper",
            role="Query Validation Specialist",
            goal="Validate queries, detect ambiguity, and route requests to appropriate specialists",
            backstory="""You are an expert query validation specialist with deep expertise in:
            - Query clarity assessment and ambiguity detection
            - Intent classification and understanding
            - Resource requirement estimation
            - Query routing and delegation
            - Quality assurance and validation
            
            You excel at understanding user intent,
            identifying unclear or ambiguous requests,
            and ensuring queries are properly routed
            to the most appropriate specialist agents.""",
            model="gpt-4o",
            model_settings=ModelSettings(tool_choice="auto"),
            verbose=True
        )
        
        # Ambiguity patterns to detect
        self.ambiguity_patterns = [
            r"\b(what|which|how|when|where|why)\b.*\b(about|regarding|concerning)\b",
            r"\b(can you|could you|would you)\b.*\b(help|assist|support)\b",
            r"\b(tell me|show me|give me)\b.*\b(something|anything|everything)\b",
            r"\b(analyze|research|investigate)\b.*\b(this|that|it)\b",
            r"\b(compare|contrast)\b.*\b(and|with)\b.*\b(and|with)\b"
        ]
        
        # Intent classification patterns
        self.intent_patterns = {
            "document_search": [
                r"\b(find|search|look for|retrieve)\b.*\b(document|file|paper|report)\b",
                r"\b(what does|what is|explain)\b.*\b(say|state|mention)\b"
            ],
            "data_analysis": [
                r"\b(analyze|analyze|examine)\b.*\b(data|numbers|statistics|trends)\b",
                r"\b(calculate|compute|determine)\b.*\b(percentage|rate|ratio|average)\b"
            ],
            "live_monitoring": [
                r"\b(current|latest|recent|now|today)\b.*\b(news|updates|developments)\b",
                r"\b(monitor|track|watch)\b.*\b(trends|changes|updates)\b"
            ],
            "comparison": [
                r"\b(compare|contrast|versus|vs)\b",
                r"\b(difference|similarity|relationship)\b.*\b(between|among)\b"
            ],
            "prediction": [
                r"\b(predict|forecast|project|estimate)\b",
                r"\b(what will|what might|what could)\b.*\b(happen|occur|be)\b"
            ]
        }
    
    def process_query(self, query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process and validate a query through the gatekeeper.
        
        Args:
            query: The user query to validate
            context: Additional context for validation
            
        Returns:
            Dictionary containing validation results and routing information
        """
        logger.info(f"Gatekeeper: Processing query: {query}")
        
        # Step 1: Assess query clarity
        clarity_assessment = self._assess_query_clarity(query)
        
        # Step 2: Detect ambiguity
        ambiguity_detection = self._detect_ambiguity(query)
        
        # Step 3: Classify intent
        intent_classification = self._classify_intent(query)
        
        # Step 4: Estimate resource requirements
        resource_estimation = self._estimate_resource_requirements(query, intent_classification)
        
        # Step 5: Determine routing
        routing_decision = self._determine_routing(query, intent_classification, resource_estimation)
        
        # Step 6: Generate validation response
        validation_response = self._generate_validation_response(
            query, clarity_assessment, ambiguity_detection, 
            intent_classification, routing_decision
        )
        
        return {
            "query": query,
            "clarity_assessment": clarity_assessment,
            "ambiguity_detection": ambiguity_detection,
            "intent_classification": intent_classification,
            "resource_estimation": resource_estimation,
            "routing_decision": routing_decision,
            "validation_response": validation_response,
            "metadata": {
                "validation_timestamp": datetime.now().isoformat(),
                "current_date": self.current_date,
                "gatekeeper_version": "1.0"
            }
        }
    
    def _assess_query_clarity(self, query: str) -> Dict[str, Any]:
        """Assess the clarity of the query."""
        logger.info("Gatekeeper: Assessing query clarity")
        
        # Check for basic clarity indicators
        clarity_indicators = {
            "has_specific_subject": bool(re.search(r"\b(specific|particular|exact)\b", query.lower())),
            "has_clear_action": bool(re.search(r"\b(find|analyze|compare|explain|calculate)\b", query.lower())),
            "has_context": bool(re.search(r"\b(in|for|about|regarding|concerning)\b", query.lower())),
            "has_timeframe": bool(re.search(r"\b(recent|current|latest|past|future)\b", query.lower())),
            "has_scope": bool(re.search(r"\b(all|some|specific|particular)\b", query.lower()))
        }
        
        # Calculate clarity score
        clarity_score = sum(clarity_indicators.values()) / len(clarity_indicators)
        
        # Determine clarity level
        if clarity_score >= 0.8:
            clarity_level = "high"
        elif clarity_score >= 0.6:
            clarity_level = "medium"
        else:
            clarity_level = "low"
        
        return {
            "clarity_score": clarity_score,
            "clarity_level": clarity_level,
            "indicators": clarity_indicators,
            "needs_clarification": clarity_score < 0.6
        }
    
    def _detect_ambiguity(self, query: str) -> Dict[str, Any]:
        """Detect ambiguity in the query."""
        logger.info("Gatekeeper: Detecting ambiguity")
        
        # Check for ambiguity patterns
        ambiguity_matches = []
        for pattern in self.ambiguity_patterns:
            matches = re.findall(pattern, query.lower())
            if matches:
                ambiguity_matches.append({
                    "pattern": pattern,
                    "matches": matches,
                    "type": "ambiguous_phrase"
                })
        
        # Check for vague pronouns
        vague_pronouns = re.findall(r"\b(this|that|it|they|them|those)\b", query.lower())
        
        # Check for unclear references
        unclear_references = re.findall(r"\b(above|below|mentioned|aforementioned)\b", query.lower())
        
        # Calculate ambiguity score
        ambiguity_score = len(ambiguity_matches) + len(vague_pronouns) + len(unclear_references)
        
        # Determine ambiguity level
        if ambiguity_score == 0:
            ambiguity_level = "none"
        elif ambiguity_score <= 2:
            ambiguity_level = "low"
        elif ambiguity_score <= 4:
            ambiguity_level = "medium"
        else:
            ambiguity_level = "high"
        
        return {
            "ambiguity_score": ambiguity_score,
            "ambiguity_level": ambiguity_level,
            "pattern_matches": ambiguity_matches,
            "vague_pronouns": vague_pronouns,
            "unclear_references": unclear_references,
            "needs_clarification": ambiguity_level in ["medium", "high"]
        }
    
    def _classify_intent(self, query: str) -> Dict[str, Any]:
        """Classify the intent of the query."""
        logger.info("Gatekeeper: Classifying intent")
        
        # Check for intent patterns
        intent_scores = {}
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, query.lower())
                score += len(matches)
            intent_scores[intent] = score
        
        # Determine primary intent
        primary_intent = max(intent_scores, key=intent_scores.get) if intent_scores else "general"
        
        # Check for secondary intents
        secondary_intents = [intent for intent, score in intent_scores.items() 
                           if score > 0 and intent != primary_intent]
        
        # Determine complexity
        complexity_indicators = [
            "compare" in query.lower(),
            "analyze" in query.lower(),
            "predict" in query.lower(),
            "multiple" in query.lower(),
            "several" in query.lower()
        ]
        complexity = "high" if sum(complexity_indicators) >= 2 else "medium" if sum(complexity_indicators) == 1 else "low"
        
        return {
            "primary_intent": primary_intent,
            "secondary_intents": secondary_intents,
            "intent_scores": intent_scores,
            "complexity": complexity,
            "requires_specialist": primary_intent != "general"
        }
    
    def _estimate_resource_requirements(self, query: str, intent_classification: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate resource requirements for processing the query."""
        logger.info("Gatekeeper: Estimating resource requirements")
        
        # Estimate based on intent and complexity
        primary_intent = intent_classification["primary_intent"]
        complexity = intent_classification["complexity"]
        
        # Base resource requirements
        base_requirements = {
            "document_search": {"time_estimate": "2-5 minutes", "complexity": "medium"},
            "data_analysis": {"time_estimate": "5-15 minutes", "complexity": "high"},
            "live_monitoring": {"time_estimate": "3-8 minutes", "complexity": "medium"},
            "comparison": {"time_estimate": "5-20 minutes", "complexity": "high"},
            "prediction": {"time_estimate": "10-30 minutes", "complexity": "very_high"},
            "general": {"time_estimate": "1-3 minutes", "complexity": "low"}
        }
        
        # Adjust based on complexity
        complexity_multipliers = {
            "low": 1.0,
            "medium": 1.5,
            "high": 2.0,
            "very_high": 3.0
        }
        
        base_req = base_requirements.get(primary_intent, base_requirements["general"])
        complexity_mult = complexity_multipliers.get(complexity, 1.0)
        
        # Estimate required specialists
        required_specialists = []
        if primary_intent in ["document_search"]:
            required_specialists.append("librarian")
        if primary_intent in ["data_analysis", "comparison", "prediction"]:
            required_specialists.append("analyst")
        if primary_intent in ["live_monitoring"]:
            required_specialists.append("scout")
        if complexity == "high" or len(intent_classification["secondary_intents"]) > 0:
            required_specialists.append("strategist")
        
        return {
            "primary_intent": primary_intent,
            "complexity": complexity,
            "time_estimate": base_req["time_estimate"],
            "complexity_multiplier": complexity_mult,
            "required_specialists": required_specialists,
            "estimated_tokens": int(1000 * complexity_mult),
            "estimated_cost": f"${0.01 * complexity_mult:.2f}"
        }
    
    def _determine_routing(self, query: str, intent_classification: Dict[str, Any], resource_estimation: Dict[str, Any]) -> Dict[str, Any]:
        """Determine how to route the query to appropriate specialists."""
        logger.info("Gatekeeper: Determining routing")
        
        # Get required specialists
        required_specialists = resource_estimation["required_specialists"]
        
        # Determine routing strategy
        if len(required_specialists) == 1:
            routing_strategy = "direct"
            primary_specialist = required_specialists[0]
            secondary_specialists = []
        elif len(required_specialists) == 2:
            routing_strategy = "sequential"
            primary_specialist = required_specialists[0]
            secondary_specialists = required_specialists[1:]
        else:
            routing_strategy = "parallel"
            primary_specialist = required_specialists[0]
            secondary_specialists = required_specialists[1:]
        
        # Determine if clarification is needed
        needs_clarification = (
            intent_classification["primary_intent"] == "general" or
            resource_estimation["complexity"] == "very_high" or
            len(required_specialists) > 3
        )
        
        return {
            "routing_strategy": routing_strategy,
            "primary_specialist": primary_specialist,
            "secondary_specialists": secondary_specialists,
            "needs_clarification": needs_clarification,
            "estimated_processing_time": resource_estimation["time_estimate"],
            "priority": "high" if needs_clarification else "normal"
        }
    
    def _generate_validation_response(self, query: str, clarity_assessment: Dict[str, Any], 
                                    ambiguity_detection: Dict[str, Any], intent_classification: Dict[str, Any], 
                                    routing_decision: Dict[str, Any]) -> str:
        """Generate a validation response for the user."""
        logger.info("Gatekeeper: Generating validation response")
        
        # Create validation prompt
        validation_prompt = f"""
        Based on the following query validation analysis:
        
        Query: "{query}"
        Clarity Level: {clarity_assessment['clarity_level']}
        Ambiguity Level: {ambiguity_detection['ambiguity_level']}
        Primary Intent: {intent_classification['primary_intent']}
        Complexity: {intent_classification['complexity']}
        Routing Strategy: {routing_decision['routing_strategy']}
        Needs Clarification: {routing_decision['needs_clarification']}
        
        Generate a validation response that:
        1. Acknowledges the query
        2. Confirms understanding or requests clarification
        3. Explains the planned approach
        4. Sets expectations for response time and quality
        
        Current Date: {self.current_date}
        """
        
        # Use the agent to generate validation response
        validation_response = self.agent.execute_task(validation_prompt)
        
        return validation_response
    
    def get_agent_instructions(self) -> str:
        """Get detailed instructions for the Gatekeeper agent."""
        return f"""
        GATEKEEPER AGENT INSTRUCTIONS:
        
        You are a specialized query validation expert with expertise in:
        - Query clarity assessment and ambiguity detection
        - Intent classification and understanding
        - Resource requirement estimation
        - Query routing and delegation
        - Quality assurance and validation
        
        CURRENT CONTEXT:
        - Current Date: {self.current_date}
        - Current Year: {self.current_year}
        
        VALIDATION METHODOLOGY:
        1. Assess query clarity and specificity
        2. Detect ambiguity and unclear references
        3. Classify intent and determine complexity
        4. Estimate resource requirements
        5. Determine optimal routing strategy
        6. Generate validation response
        
        QUALITY STANDARDS:
        - Ensure queries are clear and actionable
        - Identify and resolve ambiguity
        - Route queries to appropriate specialists
        - Set realistic expectations
        - Provide clear feedback to users
        
        When validating queries:
        - Always assess clarity and specificity
        - Detect and flag ambiguity
        - Classify intent accurately
        - Estimate resources appropriately
        - Route queries effectively
        - Provide clear validation feedback
        """

# Example usage and testing
if __name__ == "__main__":
    print("🚪 Gatekeeper Node Test")
    print("=======================")
    
    # Initialize the gatekeeper node
    gatekeeper = GatekeeperNode()
    
    # Test query validation
    test_queries = [
        "What is the current status of artificial intelligence in healthcare?",
        "Analyze the data and tell me something interesting",
        "Compare the performance of Apple and Microsoft stocks this year",
        "Find documents about machine learning",
        "What will happen next?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = gatekeeper.process_query(query)
        
        print(f"Clarity Level: {result['clarity_assessment']['clarity_level']}")
        print(f"Ambiguity Level: {result['ambiguity_detection']['ambiguity_level']}")
        print(f"Primary Intent: {result['intent_classification']['primary_intent']}")
        print(f"Complexity: {result['intent_classification']['complexity']}")
        print(f"Routing Strategy: {result['routing_decision']['routing_strategy']}")
        print(f"Needs Clarification: {result['routing_decision']['needs_clarification']}")
        print(f"Required Specialists: {result['routing_decision']['primary_specialist']}")
    
    print("\nAgent Instructions:")
    print(gatekeeper.get_agent_instructions())

"""
Prompt Engineering Toolkit
Based on Stanford research and best practices for AI collaboration
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class PromptTechnique(Enum):
    """Available prompt engineering techniques"""
    CHAIN_OF_THOUGHT = "chain_of_thought"
    FEW_SHOT = "few_shot"
    REVERSE_PROMPTING = "reverse_prompting"
    ROLE_ASSIGNMENT = "role_assignment"
    CONTEXT_ENGINEERING = "context_engineering"
    CRITICAL_FEEDBACK = "critical_feedback"

@dataclass
class PromptTemplate:
    """Template for different prompt techniques"""
    technique: PromptTechnique
    template: str
    description: str
    example: str

class PromptEngineeringToolkit:
    """
    Comprehensive toolkit for prompt engineering based on Stanford research
    """
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.context_manager = ContextManager()
    
    def _initialize_templates(self) -> Dict[PromptTechnique, PromptTemplate]:
        """Initialize prompt templates"""
        return {
            PromptTechnique.CHAIN_OF_THOUGHT: PromptTemplate(
                technique=PromptTechnique.CHAIN_OF_THOUGHT,
                template="Before you respond to my query, please walk me through your thought process step by step.",
                description="Gets AI to think out loud before responding",
                example="Write me a sales email. Before you respond, please walk me through your thought process step by step."
            ),
            
            PromptTechnique.FEW_SHOT: PromptTemplate(
                technique=PromptTechnique.FEW_SHOT,
                template="Here are examples of good output:\n{good_examples}\n\nHere are examples to avoid:\n{bad_examples}\n\nNow create similar content:",
                description="Provides examples of good and bad outputs",
                example="Here are my best sales emails: [examples]. Avoid this style: [bad example]. Write me a new sales email."
            ),
            
            PromptTechnique.REVERSE_PROMPTING: PromptTemplate(
                technique=PromptTechnique.REVERSE_PROMPTING,
                template="Before you get started, ask me for any information you need to do a good job.",
                description="Lets AI ask questions before proceeding",
                example="Help me write a sales email. Before you get started, ask me for any information you need to do a good job."
            ),
            
            PromptTechnique.ROLE_ASSIGNMENT: PromptTemplate(
                technique=PromptTechnique.ROLE_ASSIGNMENT,
                template="You are a {role}. How would {famous_person} approach this problem?",
                description="Assigns specific roles or personas to AI",
                example="You are a professional communications expert. How would Dale Carnegie approach this sales email?"
            ),
            
            PromptTechnique.CRITICAL_FEEDBACK: PromptTemplate(
                technique=PromptTechnique.CRITICAL_FEEDBACK,
                template="I want you to be a cold war era Russian Olympic judge. Be brutal. Be exacting. Deduct points for every minor flaw.",
                description="Enables critical feedback mode",
                example="Review this code. I want you to be a cold war era Russian Olympic judge. Be brutal. Be exacting. Deduct points for every minor flaw."
            ),
            
            PromptTechnique.CONTEXT_ENGINEERING: PromptTemplate(
                technique=PromptTechnique.CONTEXT_ENGINEERING,
                template="Context: {context}\n\nBrand Guidelines: {brand_guidelines}\n\nPrevious Examples: {examples}\n\nTask: {task}",
                description="Provides comprehensive context for better outputs",
                example="Context: Customer call transcript. Brand Guidelines: Professional tone. Examples: Previous successful emails. Task: Write follow-up email."
            )
        }
    
    def build_enhanced_prompt(self, base_prompt: str, techniques: List[PromptTechnique], 
                            context: Optional[Dict[str, Any]] = None) -> str:
        """
        Build an enhanced prompt using multiple techniques
        
        Args:
            base_prompt: The original prompt
            techniques: List of techniques to apply
            context: Additional context for context engineering
        """
        prompt_parts = [base_prompt]
        
        for technique in techniques:
            template = self.templates[technique]
            
            if technique == PromptTechnique.CHAIN_OF_THOUGHT:
                prompt_parts.append(f"\n{template.template}")
            
            elif technique == PromptTechnique.REVERSE_PROMPTING:
                prompt_parts.append(f"\n{template.template}")
            
            elif technique == PromptTechnique.CRITICAL_FEEDBACK:
                prompt_parts.append(f"\n{template.template}")
            
            elif technique == PromptTechnique.ROLE_ASSIGNMENT:
                role = context.get('role', 'helpful assistant') if context else 'helpful assistant'
                famous_person = context.get('famous_person', 'a professional') if context else 'a professional'
                prompt_parts.append(f"\n{template.template.format(role=role, famous_person=famous_person)}")
            
            elif technique == PromptTechnique.FEW_SHOT:
                good_examples = context.get('good_examples', 'No examples provided') if context else 'No examples provided'
                bad_examples = context.get('bad_examples', 'No bad examples provided') if context else 'No bad examples provided'
                prompt_parts.append(f"\n{template.template.format(good_examples=good_examples, bad_examples=bad_examples)}")
            
            elif technique == PromptTechnique.CONTEXT_ENGINEERING:
                if context:
                    context_str = context.get('context', 'No additional context')
                    brand_guidelines = context.get('brand_guidelines', 'No brand guidelines')
                    examples = context.get('examples', 'No examples')
                    prompt_parts.append(f"\n{template.template.format(context=context_str, brand_guidelines=brand_guidelines, examples=examples, task=base_prompt)}")
        
        return "\n".join(prompt_parts)
    
    def create_conversation_simulator(self, scenario: str, character_profile: Dict[str, Any]) -> str:
        """
        Create a conversation simulator for difficult conversations
        
        Args:
            scenario: Description of the conversation scenario
            character_profile: Profile of the person you're talking to
        """
        simulator_prompt = f"""
        I need help preparing for a difficult conversation.
        
        Scenario: {scenario}
        Character Profile: {json.dumps(character_profile, indent=2)}
        
        Please:
        1. Analyze the character's communication style and motivations
        2. Suggest conversation strategies and talking points
        3. Identify potential challenges and how to handle them
        4. Provide a step-by-step conversation guide
        5. Roleplay as the character so I can practice
        """
        
        return self.build_enhanced_prompt(
            simulator_prompt,
            [PromptTechnique.CHAIN_OF_THOUGHT, PromptTechnique.CRITICAL_FEEDBACK]
        )
    
    def create_feedback_analyzer(self, content: str, content_type: str = "general") -> str:
        """
        Create a feedback analyzer for content review
        
        Args:
            content: The content to analyze
            content_type: Type of content (email, code, analysis, etc.)
        """
        feedback_prompt = f"""
        Please analyze this {content_type} and provide objective feedback:
        
        {content}
        
        Rate the content on:
        1. Clarity and effectiveness (1-10)
        2. Professionalism and tone (1-10)
        3. Completeness and accuracy (1-10)
        4. Areas for improvement
        5. What was done well
        6. Specific suggestions for enhancement
        
        Be specific and actionable in your feedback.
        """
        
        return self.build_enhanced_prompt(
            feedback_prompt,
            [PromptTechnique.CHAIN_OF_THOUGHT, PromptTechnique.CRITICAL_FEEDBACK]
        )
    
    def create_creative_brainstormer(self, topic: str, constraints: List[str] = None) -> str:
        """
        Create a creative brainstorming prompt
        
        Args:
            topic: The topic to brainstorm about
            constraints: List of constraints to consider
        """
        constraints_str = "\n".join([f"- {constraint}" for constraint in (constraints or [])])
        
        brainstorm_prompt = f"""
        Let's brainstorm creative solutions for: {topic}
        
        Constraints to consider:
        {constraints_str if constraints else "No specific constraints"}
        
        Please:
        1. Generate 10+ creative ideas
        2. Consider multiple perspectives and approaches
        3. Think outside the box
        4. Consider implementation challenges
        5. Suggest ways to test and validate ideas
        """
        
        return self.build_enhanced_prompt(
            brainstorm_prompt,
            [PromptTechnique.CHAIN_OF_THOUGHT, PromptTechnique.ROLE_ASSIGNMENT],
            context={'role': 'creative strategist', 'famous_person': 'Steve Jobs'}
        )
    
    def create_problem_solver(self, problem: str, context: Dict[str, Any] = None) -> str:
        """
        Create a problem-solving prompt
        
        Args:
            problem: The problem to solve
            context: Additional context about the problem
        """
        context_str = json.dumps(context, indent=2) if context else "No additional context"
        
        problem_prompt = f"""
        I need help solving this problem: {problem}
        
        Context: {context_str}
        
        Please:
        1. Break down the problem into components
        2. Identify root causes and contributing factors
        3. Generate multiple solution approaches
        4. Evaluate pros and cons of each approach
        5. Recommend the best solution with implementation steps
        6. Identify potential risks and mitigation strategies
        """
        
        return self.build_enhanced_prompt(
            problem_prompt,
            [PromptTechnique.CHAIN_OF_THOUGHT, PromptTechnique.REVERSE_PROMPTING, PromptTechnique.CRITICAL_FEEDBACK]
        )
    
    def get_technique_info(self, technique: PromptTechnique) -> PromptTemplate:
        """Get information about a specific technique"""
        return self.templates[technique]
    
    def list_available_techniques(self) -> List[PromptTemplate]:
        """List all available prompt techniques"""
        return list(self.templates.values())

class ContextManager:
    """Manages context and examples for better AI collaboration"""
    
    def __init__(self):
        self.brand_guidelines = self._load_brand_guidelines()
        self.example_outputs = self._load_examples()
        self.bad_examples = self._load_bad_examples()
    
    def _load_brand_guidelines(self) -> str:
        """Load brand guidelines"""
        return """
        Brand Voice: Professional, helpful, but direct
        Tone: Confident but not arrogant
        Style: Clear and concise
        Values: Quality, integrity, innovation
        Communication Style: Data-driven, evidence-based
        """
    
    def _load_examples(self) -> Dict[str, str]:
        """Load good examples for different task types"""
        return {
            "email": """
            Subject: Clear and compelling
            Body: Professional, concise, with clear call to action
            Tone: Confident but not pushy
            Structure: Problem, solution, next steps
            """,
            "code": """
            Well-documented with clear comments
            Follows best practices and conventions
            Includes error handling and validation
            Modular and reusable design
            """,
            "analysis": """
            Data-driven with clear methodology
            Considers multiple perspectives
            Provides actionable insights
            Acknowledges limitations
            """
        }
    
    def _load_bad_examples(self) -> Dict[str, str]:
        """Load bad examples to avoid"""
        return {
            "email": """
            Subject: Generic or unclear
            Body: Vague, no clear purpose, too long
            Tone: Unprofessional or too casual
            Structure: No clear flow or call to action
            """,
            "code": """
            Poorly documented with no comments
            No error handling or validation
            Hard to read and maintain
            Monolithic design
            """,
            "analysis": """
            Opinion-based without data
            No clear methodology
            No actionable insights
            Ignores limitations
            """
        }

# Example usage
if __name__ == "__main__":
    toolkit = PromptEngineeringToolkit()
    
    print("=== Prompt Engineering Toolkit Demo ===\n")
    
    # Example 1: Enhanced prompt for sales email
    print("1. Enhanced Sales Email Prompt:")
    sales_prompt = toolkit.build_enhanced_prompt(
        "Write me a sales email for our new AI product",
        [PromptTechnique.CHAIN_OF_THOUGHT, PromptTechnique.REVERSE_PROMPTING, PromptTechnique.FEW_SHOT],
        context={
            'good_examples': 'Professional tone, clear value proposition, specific call to action',
            'bad_examples': 'Generic, too long, no clear purpose'
        }
    )
    print(sales_prompt)
    print("\n" + "="*50 + "\n")
    
    # Example 2: Conversation simulator
    print("2. Conversation Simulator:")
    character_profile = {
        "name": "Jim",
        "communication_style": "Direct and confrontational",
        "background": "Sales leader, East Coast, sarcastic",
        "motivation": "Wants commission on deals"
    }
    
    simulator_prompt = toolkit.create_conversation_simulator(
        "I need to discuss commission attribution with Jim about a deal that came through our social team",
        character_profile
    )
    print(simulator_prompt)
    print("\n" + "="*50 + "\n")
    
    # Example 3: Creative brainstorming
    print("3. Creative Brainstorming:")
    brainstorm_prompt = toolkit.create_creative_brainstormer(
        "How to increase user engagement in our mobile app",
        constraints=["Limited budget", "Small team", "3-month timeline"]
    )
    print(brainstorm_prompt)
    print("\n" + "="*50 + "\n")
    
    # Example 4: List available techniques
    print("4. Available Techniques:")
    for technique in toolkit.list_available_techniques():
        print(f"- {technique.technique.value}: {technique.description}")
    
    print("\n✅ Prompt Engineering Toolkit ready for use!")

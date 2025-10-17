"""
Rapid Prototyping Agent

This agent handles rapid prototyping by selecting appropriate templates,
generating code, and creating functional prototypes quickly.
"""

import asyncio
import os
import shutil
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Template configurations
TEMPLATE_CONFIGS = {
    "web_app": {
        "name": "Next.js Web Application",
        "path": "templates/web-frameworks/nextjs",
        "description": "Full-stack React application with TypeScript",
        "suitable_for": ["web apps", "dashboards", "saas platforms"],
        "tech_stack": ["Next.js", "TypeScript", "Tailwind CSS", "Supabase"]
    },
    "mobile_app": {
        "name": "React Native Mobile App",
        "path": "templates/mobile/react-native",
        "description": "Cross-platform mobile application",
        "suitable_for": ["mobile apps", "consumer apps", "fitness apps"],
        "tech_stack": ["React Native", "Expo", "TypeScript", "Supabase"]
    },
    "api_backend": {
        "name": "FastAPI Backend",
        "path": "templates/web-frameworks/fastapi",
        "description": "High-performance Python API",
        "suitable_for": ["apis", "microservices", "data processing"],
        "tech_stack": ["FastAPI", "Python", "PostgreSQL", "Redis"]
    },
    "ai_agent": {
        "name": "AI Agent System",
        "path": "templates/ai-agents/crewai",
        "description": "Multi-agent AI system",
        "suitable_for": ["ai assistants", "automation", "intelligent systems"],
        "tech_stack": ["CrewAI", "OpenAI", "LangChain", "Python"]
    },
    "fitness_app": {
        "name": "AI-Powered Fitness App",
        "path": "templates/fitness-app",
        "description": "Voice-powered fitness tracking with AI analytics",
        "suitable_for": ["fitness apps", "health apps", "voice interfaces"],
        "tech_stack": ["React Native", "Next.js", "FastAPI", "OpenAI Whisper"]
    }
}


class TemplateSelectorAgent:
    """Selects the most appropriate template based on project requirements"""
    
    async def select_template(self, idea_description: str, validation_result: Dict) -> str:
        """Select the best template for the project"""
        await asyncio.sleep(0.5)  # Simulate analysis
        
        # Analyze idea description for keywords
        idea_lower = idea_description.lower()
        
        # Mobile app indicators
        if any(keyword in idea_lower for keyword in ["mobile", "app", "phone", "ios", "android"]):
            if "fitness" in idea_lower or "health" in idea_lower:
                return "fitness_app"
            return "mobile_app"
        
        # AI agent indicators
        if any(keyword in idea_lower for keyword in ["ai", "agent", "assistant", "automation", "intelligent"]):
            return "ai_agent"
        
        # Web app indicators
        if any(keyword in idea_lower for keyword in ["web", "dashboard", "saas", "platform", "website"]):
            return "web_app"
        
        # API indicators
        if any(keyword in idea_lower for keyword in ["api", "backend", "service", "microservice"]):
            return "api_backend"
        
        # Default to web app for most projects
        return "web_app"


class CodeGeneratorAgent:
    """Generates code based on project requirements and selected template"""
    
    async def generate_project_structure(self, template_config: Dict, project_name: str) -> Dict[str, Any]:
        """Generate the basic project structure"""
        await asyncio.sleep(1)  # Simulate code generation
        
        return {
            "project_name": project_name,
            "template_used": template_config["name"],
            "tech_stack": template_config["tech_stack"],
            "generated_files": [
                "package.json",
                "README.md",
                "src/main.py" if "fastapi" in template_config["tech_stack"] else "src/app.tsx",
                "src/components/",
                "src/services/",
                "src/types/",
                "tests/",
                "docs/"
            ],
            "dependencies": self._generate_dependencies(template_config),
            "configuration_files": [
                ".env.example",
                "docker-compose.yml",
                "Dockerfile",
                ".gitignore",
                "tsconfig.json" if "typescript" in template_config["tech_stack"] else "pyproject.toml"
            ]
        }
    
    def _generate_dependencies(self, template_config: Dict) -> Dict[str, List[str]]:
        """Generate dependency lists based on tech stack"""
        deps = {
            "production": [],
            "development": [],
            "ai_services": []
        }
        
        tech_stack = template_config["tech_stack"]
        
        if "Next.js" in tech_stack:
            deps["production"].extend([
                "next@latest",
                "react@latest",
                "react-dom@latest",
                "@types/react",
                "@types/react-dom"
            ])
            deps["development"].extend([
                "typescript",
                "tailwindcss",
                "eslint",
                "prettier"
            ])
        
        if "FastAPI" in tech_stack:
            deps["production"].extend([
                "fastapi",
                "uvicorn",
                "sqlalchemy",
                "pydantic"
            ])
            deps["development"].extend([
                "pytest",
                "black",
                "isort",
                "mypy"
            ])
        
        if "React Native" in tech_stack:
            deps["production"].extend([
                "react-native",
                "expo",
                "@react-navigation/native"
            ])
        
        if "OpenAI" in tech_stack:
            deps["ai_services"].extend([
                "openai",
                "langchain",
                "crewai"
            ])
        
        return deps


class DatabaseDesignAgent:
    """Designs database schema based on project requirements"""
    
    async def design_schema(self, idea_description: str, project_type: str) -> Dict[str, Any]:
        """Design database schema for the project"""
        await asyncio.sleep(0.5)  # Simulate schema design
        
        # Common tables for most applications
        base_tables = {
            "users": {
                "id": "UUID PRIMARY KEY",
                "email": "VARCHAR(255) UNIQUE NOT NULL",
                "name": "VARCHAR(255)",
                "created_at": "TIMESTAMP DEFAULT NOW()",
                "updated_at": "TIMESTAMP DEFAULT NOW()"
            },
            "sessions": {
                "id": "UUID PRIMARY KEY",
                "user_id": "UUID REFERENCES users(id)",
                "token": "VARCHAR(255) UNIQUE NOT NULL",
                "expires_at": "TIMESTAMP NOT NULL",
                "created_at": "TIMESTAMP DEFAULT NOW()"
            }
        }
        
        # Project-specific tables
        project_tables = {}
        
        if "finance" in idea_description.lower():
            project_tables.update({
                "accounts": {
                    "id": "UUID PRIMARY KEY",
                    "user_id": "UUID REFERENCES users(id)",
                    "account_name": "VARCHAR(255) NOT NULL",
                    "account_type": "VARCHAR(50) NOT NULL",
                    "balance": "DECIMAL(15,2) DEFAULT 0",
                    "created_at": "TIMESTAMP DEFAULT NOW()"
                },
                "transactions": {
                    "id": "UUID PRIMARY KEY",
                    "account_id": "UUID REFERENCES accounts(id)",
                    "amount": "DECIMAL(15,2) NOT NULL",
                    "description": "TEXT",
                    "category": "VARCHAR(100)",
                    "transaction_date": "DATE NOT NULL",
                    "created_at": "TIMESTAMP DEFAULT NOW()"
                },
                "budgets": {
                    "id": "UUID PRIMARY KEY",
                    "user_id": "UUID REFERENCES users(id)",
                    "category": "VARCHAR(100) NOT NULL",
                    "amount": "DECIMAL(15,2) NOT NULL",
                    "period": "VARCHAR(20) NOT NULL",
                    "created_at": "TIMESTAMP DEFAULT NOW()"
                }
            })
        
        elif "fitness" in idea_description.lower():
            project_tables.update({
                "workouts": {
                    "id": "UUID PRIMARY KEY",
                    "user_id": "UUID REFERENCES users(id)",
                    "workout_name": "VARCHAR(255) NOT NULL",
                    "workout_date": "DATE NOT NULL",
                    "duration_minutes": "INTEGER",
                    "created_at": "TIMESTAMP DEFAULT NOW()"
                },
                "exercises": {
                    "id": "UUID PRIMARY KEY",
                    "workout_id": "UUID REFERENCES workouts(id)",
                    "exercise_name": "VARCHAR(255) NOT NULL",
                    "sets": "INTEGER",
                    "reps": "INTEGER",
                    "weight": "DECIMAL(8,2)",
                    "created_at": "TIMESTAMP DEFAULT NOW()"
                }
            })
        
        return {
            "database_type": "PostgreSQL",
            "tables": {**base_tables, **project_tables},
            "indexes": self._generate_indexes(project_tables),
            "relationships": self._generate_relationships(project_tables)
        }
    
    def _generate_indexes(self, tables: Dict) -> List[str]:
        """Generate database indexes for performance"""
        indexes = []
        for table_name, columns in tables.items():
            if "user_id" in columns:
                indexes.append(f"CREATE INDEX idx_{table_name}_user_id ON {table_name}(user_id);")
            if "created_at" in columns:
                indexes.append(f"CREATE INDEX idx_{table_name}_created_at ON {table_name}(created_at);")
        return indexes
    
    def _generate_relationships(self, tables: Dict) -> List[str]:
        """Generate foreign key relationships"""
        relationships = []
        for table_name, columns in tables.items():
            for column_name, column_def in columns.items():
                if "REFERENCES" in column_def:
                    relationships.append(f"{table_name}.{column_name} -> {column_def.split('REFERENCES ')[1].split('(')[0]}")
        return relationships


class APIDesignAgent:
    """Designs API endpoints based on project requirements"""
    
    async def design_api(self, idea_description: str, database_schema: Dict) -> Dict[str, Any]:
        """Design REST API endpoints"""
        await asyncio.sleep(0.5)  # Simulate API design
        
        base_endpoints = {
            "auth": {
                "POST /auth/register": "User registration",
                "POST /auth/login": "User login",
                "POST /auth/logout": "User logout",
                "GET /auth/me": "Get current user"
            },
            "users": {
                "GET /users": "List users (admin only)",
                "GET /users/{id}": "Get user by ID",
                "PUT /users/{id}": "Update user",
                "DELETE /users/{id}": "Delete user"
            }
        }
        
        # Project-specific endpoints
        project_endpoints = {}
        
        if "finance" in idea_description.lower():
            project_endpoints.update({
                "accounts": {
                    "GET /accounts": "List user accounts",
                    "POST /accounts": "Create new account",
                    "GET /accounts/{id}": "Get account details",
                    "PUT /accounts/{id}": "Update account",
                    "DELETE /accounts/{id}": "Delete account"
                },
                "transactions": {
                    "GET /transactions": "List transactions",
                    "POST /transactions": "Create transaction",
                    "GET /transactions/{id}": "Get transaction",
                    "PUT /transactions/{id}": "Update transaction",
                    "DELETE /transactions/{id}": "Delete transaction"
                },
                "analytics": {
                    "GET /analytics/spending": "Get spending analytics",
                    "GET /analytics/budgets": "Get budget analytics",
                    "GET /analytics/trends": "Get spending trends"
                }
            })
        
        return {
            "base_url": "https://api.yourproject.com/v1",
            "authentication": "JWT Bearer tokens",
            "endpoints": {**base_endpoints, **project_endpoints},
            "response_format": "JSON",
            "error_handling": "Standard HTTP status codes",
            "rate_limiting": "1000 requests per hour per user"
        }


class RapidPrototypingAgent:
    """
    Master agent for rapid prototyping.
    
    This agent coordinates template selection, code generation, database design,
    and API design to create functional prototypes quickly.
    """
    
    def __init__(self):
        """Initialize with specialized sub-agents"""
        self.template_selector = TemplateSelectorAgent()
        self.code_generator = CodeGeneratorAgent()
        self.database_designer = DatabaseDesignAgent()
        self.api_designer = APIDesignAgent()
    
    async def create_prototype(
        self, 
        idea_description: str, 
        validation_result: Dict
    ) -> Dict[str, Any]:
        """
        Create a complete prototype based on idea and validation results.
        
        Args:
            idea_description: Detailed description of the software idea
            validation_result: Results from idea validation
            
        Returns:
            Complete prototype specification and generated code
        """
        print(f"Starting rapid prototyping for: {idea_description[:100]}...")
        
        # Step 1: Select appropriate template
        template_name = await self.template_selector.select_template(
            idea_description, validation_result
        )
        template_config = TEMPLATE_CONFIGS[template_name]
        
        # Step 2: Generate project structure
        project_name = self._extract_project_name(idea_description)
        project_structure = await self.code_generator.generate_project_structure(
            template_config, project_name
        )
        
        # Step 3: Design database schema
        database_schema = await self.database_designer.design_schema(
            idea_description, template_name
        )
        
        # Step 4: Design API endpoints
        api_design = await self.api_designer.design_api(
            idea_description, database_schema
        )
        
        # Step 5: Generate deployment configuration
        deployment_config = await self._generate_deployment_config(template_config)
        
        # Step 6: Create development plan
        development_plan = await self._create_development_plan(
            idea_description, template_config, validation_result
        )
        
        prototype = {
            "project_name": project_name,
            "template_used": template_name,
            "template_config": template_config,
            "project_structure": project_structure,
            "database_schema": database_schema,
            "api_design": api_design,
            "deployment_config": deployment_config,
            "development_plan": development_plan,
            "estimated_development_time": self._estimate_development_time(template_config),
            "estimated_cost": self._estimate_development_cost(template_config),
            "created_at": datetime.now().isoformat(),
            "status": "ready_for_development"
        }
        
        print(f"Prototype created successfully: {project_name}")
        return prototype
    
    async def create_deployment_plan(self, project: Any) -> Dict[str, Any]:
        """Create deployment plan for the project"""
        await asyncio.sleep(0.5)  # Simulate deployment planning
        
        return {
            "staging_environment": {
                "url": f"https://staging-{project.id}.yourdomain.com",
                "database": "PostgreSQL (Supabase)",
                "hosting": "Vercel (frontend) + Railway (backend)",
                "monitoring": "Basic logging and error tracking"
            },
            "production_environment": {
                "url": f"https://{project.id}.yourdomain.com",
                "database": "PostgreSQL with read replicas",
                "hosting": "AWS/GCP with auto-scaling",
                "monitoring": "DataDog/New Relic with alerts",
                "cdn": "CloudFlare for global distribution"
            },
            "deployment_steps": [
                "Set up infrastructure",
                "Deploy database and run migrations",
                "Deploy backend API",
                "Deploy frontend application",
                "Configure domain and SSL",
                "Set up monitoring and alerts",
                "Run smoke tests",
                "Go live with gradual rollout"
            ],
            "rollback_plan": "Automated rollback to previous version if health checks fail"
        }
    
    def _extract_project_name(self, idea_description: str) -> str:
        """Extract a project name from the idea description"""
        # Simple extraction - in production, use AI for better naming
        words = idea_description.split()[:3]
        return "_".join(words).lower().replace(" ", "_").replace(",", "")
    
    async def _generate_deployment_config(self, template_config: Dict) -> Dict[str, Any]:
        """Generate deployment configuration"""
        await asyncio.sleep(0.3)  # Simulate config generation
        
        return {
            "docker": {
                "enabled": True,
                "multi_stage": True,
                "optimization": "Production-optimized images"
            },
            "ci_cd": {
                "provider": "GitHub Actions",
                "stages": ["test", "build", "deploy"],
                "automated_testing": True,
                "security_scanning": True
            },
            "monitoring": {
                "application": "DataDog/New Relic",
                "infrastructure": "AWS CloudWatch",
                "logs": "Centralized logging with ELK stack",
                "alerts": "Slack/Email notifications"
            },
            "scaling": {
                "auto_scaling": True,
                "load_balancer": "AWS ALB/CloudFlare",
                "database": "Read replicas for read-heavy workloads",
                "caching": "Redis for session and data caching"
            }
        }
    
    async def _create_development_plan(
        self, 
        idea_description: str, 
        template_config: Dict, 
        validation_result: Dict
    ) -> Dict[str, Any]:
        """Create a detailed development plan"""
        await asyncio.sleep(0.5)  # Simulate planning
        
        return {
            "phases": [
                {
                    "name": "Setup & Foundation",
                    "duration": "1-2 days",
                    "tasks": [
                        "Initialize project structure",
                        "Set up development environment",
                        "Configure database",
                        "Set up basic authentication"
                    ]
                },
                {
                    "name": "Core Features",
                    "duration": "1-2 weeks",
                    "tasks": [
                        "Implement main business logic",
                        "Create API endpoints",
                        "Build user interface",
                        "Add data validation"
                    ]
                },
                {
                    "name": "Integration & Testing",
                    "duration": "3-5 days",
                    "tasks": [
                        "Integrate third-party services",
                        "Write comprehensive tests",
                        "Set up CI/CD pipeline",
                        "Performance optimization"
                    ]
                },
                {
                    "name": "Deployment & Launch",
                    "duration": "2-3 days",
                    "tasks": [
                        "Deploy to staging",
                        "User acceptance testing",
                        "Deploy to production",
                        "Monitor and iterate"
                    ]
                }
            ],
            "milestones": [
                "MVP ready for testing",
                "Beta version with core features",
                "Production-ready release",
                "First paying customers"
            ],
            "success_criteria": [
                "All tests passing",
                "Performance benchmarks met",
                "Security audit passed",
                "User feedback incorporated"
            ]
        }
    
    def _estimate_development_time(self, template_config: Dict) -> str:
        """Estimate development time based on template complexity"""
        base_time = 2  # weeks
        
        tech_stack = template_config["tech_stack"]
        
        if "React Native" in tech_stack:
            base_time += 1  # Mobile development adds complexity
        
        if "OpenAI" in tech_stack:
            base_time += 1  # AI integration adds complexity
        
        if "PostgreSQL" in tech_stack:
            base_time += 0.5  # Database setup
        
        return f"{base_time}-{base_time + 2} weeks"
    
    def _estimate_development_cost(self, template_config: Dict) -> Dict[str, Any]:
        """Estimate development costs"""
        base_cost = 50000  # Base cost in USD
        
        tech_stack = template_config["tech_stack"]
        
        if "React Native" in tech_stack:
            base_cost += 15000  # Mobile development
        
        if "OpenAI" in tech_stack:
            base_cost += 10000  # AI integration
        
        return {
            "development": f"${base_cost:,}",
            "infrastructure": "$500-2000/month",
            "third_party_services": "$200-1000/month",
            "total_first_year": f"${base_cost + 12000:,}"
        }


# Example usage and testing
async def main():
    """Example usage of the Rapid Prototyping Agent"""
    agent = RapidPrototypingAgent()
    
    # Example idea
    idea = """
    I want to create an AI-powered personal finance assistant that helps users 
    track expenses, create budgets, and get personalized financial advice. 
    The app should integrate with bank accounts, provide real-time spending 
    insights, and offer investment recommendations based on user goals.
    """
    
    # Mock validation result
    validation_result = {
        "is_viable": True,
        "market_analysis": {"market_size": "Large"},
        "technical_analysis": {"feasibility_score": 8.5}
    }
    
    # Create prototype
    prototype = await agent.create_prototype(idea, validation_result)
    
    print(f"Project Name: {prototype['project_name']}")
    print(f"Template Used: {prototype['template_used']}")
    print(f"Tech Stack: {prototype['template_config']['tech_stack']}")
    print(f"Development Time: {prototype['estimated_development_time']}")
    print(f"Development Cost: {prototype['estimated_cost']['development']}")


if __name__ == "__main__":
    asyncio.run(main())


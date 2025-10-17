"""
Project Marketplace for AI Agent Project Generation

This module provides a marketplace of community-contributed project templates,
presets, and configurations that users can browse, rate, and use.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import uuid

# Add parent directories to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

# Add the ai_agents directory to path
ai_agents_dir = current_dir.parent
sys.path.append(str(ai_agents_dir))

from schemas.agent_schemas import AgentSchemaGenerator
from mcp.mcp_framework import MCPFramework
from prompting.structured_prompts import PromptFramework, PromptType
from test_data.data_generator import TestDataGenerator, DataContext
from configuration.subject_setting_style import SubjectSettingStyleFramework, SubjectType, SettingType, StyleType


class ProjectMarketplace:
    """Marketplace for community project templates and configurations"""
    
    def __init__(self):
        """Initialize the project marketplace"""
        self.schema_generator = AgentSchemaGenerator()
        self.mcp_framework = MCPFramework()
        self.prompt_framework = PromptFramework()
        self.data_generator = TestDataGenerator()
        self.config_framework = SubjectSettingStyleFramework()
        
        self.marketplace_data = self._load_marketplace_data()
        self.user_ratings = self._load_user_ratings()
        self.user_favorites = self._load_user_favorites()
        
    def _load_marketplace_data(self):
        """Load marketplace data with community templates"""
        return {
            "templates": {
                "customer_service_champion": {
                    "id": "customer_service_champion",
                    "name": "Customer Service Champion",
                    "description": "Advanced customer service agent with empathy, problem-solving, and escalation handling",
                    "author": "AI Agent Community",
                    "version": "1.2.0",
                    "rating": 4.8,
                    "downloads": 1250,
                    "tags": ["customer-service", "empathy", "escalation", "problem-solving"],
                    "domain": "customer_service",
                    "difficulty": "intermediate",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-20T14:45:00Z",
                    "configuration": {
                        "patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_16", "pattern_17"],
                        "capabilities": [
                            "customer support", "problem solving", "empathy", "ticket management",
                            "escalation handling", "sentiment analysis", "knowledge base search"
                        ],
                        "communication_style": "empathetic and supportive",
                        "integrations": ["database", "api", "file_processing"],
                        "test_requirements": {
                            "data_types": ["user_profiles", "conversations", "tasks"],
                            "volume": 1000,
                            "context": "customer_service"
                        }
                    },
                    "features": [
                        "Real-time sentiment analysis",
                        "Intelligent escalation routing",
                        "Knowledge base integration",
                        "Multi-language support",
                        "Performance analytics"
                    ],
                    "use_cases": [
                        "Customer support automation",
                        "Ticket management",
                        "Customer satisfaction improvement",
                        "Support team assistance"
                    ]
                },
                "data_science_assistant": {
                    "id": "data_science_assistant",
                    "name": "Data Science Assistant",
                    "description": "Intelligent data analysis agent with learning capabilities and optimization",
                    "author": "Data Science Pro",
                    "version": "2.0.1",
                    "rating": 4.9,
                    "downloads": 890,
                    "tags": ["data-science", "analytics", "machine-learning", "optimization"],
                    "domain": "technology",
                    "difficulty": "advanced",
                    "created_at": "2024-01-10T09:15:00Z",
                    "updated_at": "2024-01-25T16:20:00Z",
                    "configuration": {
                        "patterns": ["pattern_4", "pattern_8", "pattern_10", "pattern_15", "pattern_17"],
                        "capabilities": [
                            "data analysis", "pattern recognition", "statistical modeling",
                            "machine learning", "data visualization", "report generation"
                        ],
                        "communication_style": "technical and precise",
                        "integrations": ["database", "api", "file_processing"],
                        "test_requirements": {
                            "data_types": ["metrics", "documents", "events"],
                            "volume": 2000,
                            "context": "technology"
                        }
                    },
                    "features": [
                        "Automated data analysis",
                        "Machine learning model training",
                        "Statistical report generation",
                        "Data visualization",
                        "Performance optimization"
                    ],
                    "use_cases": [
                        "Data analysis automation",
                        "ML model development",
                        "Business intelligence",
                        "Research assistance"
                    ]
                },
                "healthcare_companion": {
                    "id": "healthcare_companion",
                    "name": "Healthcare Companion",
                    "description": "Medical AI assistant with empathy, ethics, and safety guardrails",
                    "author": "Healthcare AI Team",
                    "version": "1.5.0",
                    "rating": 4.7,
                    "downloads": 650,
                    "tags": ["healthcare", "medical", "empathy", "safety", "ethics"],
                    "domain": "healthcare",
                    "difficulty": "advanced",
                    "created_at": "2024-01-05T11:00:00Z",
                    "updated_at": "2024-01-22T13:30:00Z",
                    "configuration": {
                        "patterns": ["pattern_14", "pattern_16", "pattern_17", "pattern_18"],
                        "capabilities": [
                            "medical information", "patient support", "safety monitoring",
                            "compliance", "privacy protection", "symptom analysis"
                        ],
                        "communication_style": "empathetic and precise",
                        "integrations": ["database", "api"],
                        "test_requirements": {
                            "data_types": ["user_profiles", "conversations", "documents"],
                            "volume": 1000,
                            "context": "healthcare"
                        }
                    },
                    "features": [
                        "Medical knowledge base",
                        "Safety monitoring",
                        "Privacy protection",
                        "Compliance checking",
                        "Patient support"
                    ],
                    "use_cases": [
                        "Patient support",
                        "Medical information",
                        "Health monitoring",
                        "Clinical assistance"
                    ]
                },
                "creative_writing_buddy": {
                    "id": "creative_writing_buddy",
                    "name": "Creative Writing Buddy",
                    "description": "AI assistant for creative content generation with empathy and creativity",
                    "author": "Creative Writers Guild",
                    "version": "1.3.0",
                    "rating": 4.6,
                    "downloads": 750,
                    "tags": ["creative-writing", "content-generation", "creativity", "empathy"],
                    "domain": "education",
                    "difficulty": "beginner",
                    "created_at": "2024-01-12T14:20:00Z",
                    "updated_at": "2024-01-18T10:15:00Z",
                    "configuration": {
                        "patterns": ["pattern_13", "pattern_14", "pattern_16", "pattern_19"],
                        "capabilities": [
                            "creative writing", "content generation", "style adaptation",
                            "feedback", "inspiration", "editing"
                        ],
                        "communication_style": "creative and engaging",
                        "integrations": ["file_processing", "image_processing"],
                        "test_requirements": {
                            "data_types": ["documents", "conversations", "sessions"],
                            "volume": 500,
                            "context": "education"
                        }
                    },
                    "features": [
                        "Creative content generation",
                        "Style adaptation",
                        "Writing feedback",
                        "Inspiration prompts",
                        "Collaborative editing"
                    ],
                    "use_cases": [
                        "Creative writing assistance",
                        "Content generation",
                        "Writing education",
                        "Creative collaboration"
                    ]
                },
                "e_commerce_optimizer": {
                    "id": "e_commerce_optimizer",
                    "name": "E-commerce Optimizer",
                    "description": "AI agent for e-commerce optimization with personalization and analytics",
                    "author": "E-commerce Solutions",
                    "version": "1.8.0",
                    "rating": 4.5,
                    "downloads": 1100,
                    "tags": ["e-commerce", "personalization", "analytics", "optimization"],
                    "domain": "e_commerce",
                    "difficulty": "intermediate",
                    "created_at": "2024-01-08T16:45:00Z",
                    "updated_at": "2024-01-23T12:00:00Z",
                    "configuration": {
                        "patterns": ["pattern_2", "pattern_3", "pattern_14", "pattern_15", "pattern_17"],
                        "capabilities": [
                            "product recommendations", "customer analysis", "sales optimization",
                            "inventory management", "customer service", "analytics"
                        ],
                        "communication_style": "friendly and helpful",
                        "integrations": ["database", "api", "file_processing", "image_processing"],
                        "test_requirements": {
                            "data_types": ["user_profiles", "conversations", "tasks", "events"],
                            "volume": 1500,
                            "context": "e_commerce"
                        }
                    },
                    "features": [
                        "Product recommendation engine",
                        "Customer behavior analysis",
                        "Sales optimization",
                        "Inventory management",
                        "Customer service automation"
                    ],
                    "use_cases": [
                        "E-commerce personalization",
                        "Sales optimization",
                        "Customer service",
                        "Inventory management"
                    ]
                },
                "financial_advisor": {
                    "id": "financial_advisor",
                    "name": "Financial Advisor",
                    "description": "AI financial advisor with ethics, compliance, and risk management",
                    "author": "FinTech Solutions",
                    "version": "2.1.0",
                    "rating": 4.8,
                    "downloads": 420,
                    "tags": ["finance", "advisory", "ethics", "compliance", "risk-management"],
                    "domain": "finance",
                    "difficulty": "advanced",
                    "created_at": "2024-01-03T08:30:00Z",
                    "updated_at": "2024-01-24T15:45:00Z",
                    "configuration": {
                        "patterns": ["pattern_16", "pattern_17", "pattern_18", "pattern_15"],
                        "capabilities": [
                            "financial analysis", "risk assessment", "compliance",
                            "investment advice", "portfolio management", "security"
                        ],
                        "communication_style": "professional and precise",
                        "integrations": ["database", "api"],
                        "test_requirements": {
                            "data_types": ["user_profiles", "documents", "events"],
                            "volume": 1000,
                            "context": "finance"
                        }
                    },
                    "features": [
                        "Financial analysis",
                        "Risk assessment",
                        "Compliance monitoring",
                        "Investment advice",
                        "Portfolio management"
                    ],
                    "use_cases": [
                        "Financial advisory",
                        "Risk management",
                        "Investment analysis",
                        "Compliance monitoring"
                    ]
                }
            },
            "categories": {
                "customer_service": {
                    "name": "Customer Service",
                    "description": "Templates for customer support and service automation",
                    "templates": ["customer_service_champion"]
                },
                "data_science": {
                    "name": "Data Science",
                    "description": "Templates for data analysis and machine learning",
                    "templates": ["data_science_assistant"]
                },
                "healthcare": {
                    "name": "Healthcare",
                    "description": "Templates for medical and health-related applications",
                    "templates": ["healthcare_companion"]
                },
                "creative": {
                    "name": "Creative",
                    "description": "Templates for creative writing and content generation",
                    "templates": ["creative_writing_buddy"]
                },
                "e_commerce": {
                    "name": "E-commerce",
                    "description": "Templates for online retail and shopping",
                    "templates": ["e_commerce_optimizer"]
                },
                "finance": {
                    "name": "Finance",
                    "description": "Templates for financial services and banking",
                    "templates": ["financial_advisor"]
                }
            },
            "difficulty_levels": {
                "beginner": {
                    "name": "Beginner",
                    "description": "Easy to use, minimal configuration required",
                    "templates": ["creative_writing_buddy"]
                },
                "intermediate": {
                    "name": "Intermediate",
                    "description": "Moderate complexity, some configuration required",
                    "templates": ["customer_service_champion", "e_commerce_optimizer"]
                },
                "advanced": {
                    "name": "Advanced",
                    "description": "Complex setup, requires technical knowledge",
                    "templates": ["data_science_assistant", "healthcare_companion", "financial_advisor"]
                }
            }
        }
    
    def _load_user_ratings(self):
        """Load user ratings data"""
        return {
            "customer_service_champion": [
                {"user": "user123", "rating": 5, "comment": "Excellent for customer support!"},
                {"user": "user456", "rating": 4, "comment": "Great template, easy to customize"},
                {"user": "user789", "rating": 5, "comment": "Saved us hours of development time"}
            ],
            "data_science_assistant": [
                {"user": "data_pro", "rating": 5, "comment": "Perfect for ML projects"},
                {"user": "analyst_ai", "rating": 4, "comment": "Very comprehensive, love the features"}
            ]
        }
    
    def _load_user_favorites(self):
        """Load user favorites data"""
        return {
            "user123": ["customer_service_champion", "e_commerce_optimizer"],
            "user456": ["creative_writing_buddy", "healthcare_companion"],
            "data_pro": ["data_science_assistant", "financial_advisor"]
        }
    
    def browse_templates(self, category=None, difficulty=None, search_term=None):
        """Browse available templates with filtering"""
        templates = self.marketplace_data["templates"]
        
        # Apply filters
        filtered_templates = []
        for template_id, template in templates.items():
            # Category filter
            if category and template["domain"] != category:
                continue
            
            # Difficulty filter
            if difficulty and template["difficulty"] != difficulty:
                continue
            
            # Search term filter
            if search_term:
                search_lower = search_term.lower()
                if not (search_lower in template["name"].lower() or 
                       search_lower in template["description"].lower() or
                       any(search_lower in tag.lower() for tag in template["tags"])):
                    continue
            
            filtered_templates.append(template)
        
        # Sort by rating and downloads
        filtered_templates.sort(key=lambda x: (x["rating"], x["downloads"]), reverse=True)
        
        return filtered_templates
    
    def get_template_details(self, template_id):
        """Get detailed information about a specific template"""
        if template_id not in self.marketplace_data["templates"]:
            return None
        
        template = self.marketplace_data["templates"][template_id]
        
        # Add user ratings
        if template_id in self.user_ratings:
            template["user_reviews"] = self.user_ratings[template_id]
        else:
            template["user_reviews"] = []
        
        return template
    
    def rate_template(self, template_id, user_id, rating, comment=None):
        """Rate a template"""
        if template_id not in self.marketplace_data["templates"]:
            return False
        
        if template_id not in self.user_ratings:
            self.user_ratings[template_id] = []
        
        # Add or update user rating
        user_rating = {"user": user_id, "rating": rating, "comment": comment}
        
        # Remove existing rating from user
        self.user_ratings[template_id] = [
            r for r in self.user_ratings[template_id] if r["user"] != user_id
        ]
        
        # Add new rating
        self.user_ratings[template_id].append(user_rating)
        
        # Update template rating
        ratings = [r["rating"] for r in self.user_ratings[template_id]]
        self.marketplace_data["templates"][template_id]["rating"] = sum(ratings) / len(ratings)
        
        return True
    
    def add_to_favorites(self, user_id, template_id):
        """Add template to user favorites"""
        if template_id not in self.marketplace_data["templates"]:
            return False
        
        if user_id not in self.user_favorites:
            self.user_favorites[user_id] = []
        
        if template_id not in self.user_favorites[user_id]:
            self.user_favorites[user_id].append(template_id)
        
        return True
    
    def remove_from_favorites(self, user_id, template_id):
        """Remove template from user favorites"""
        if user_id in self.user_favorites and template_id in self.user_favorites[user_id]:
            self.user_favorites[user_id].remove(template_id)
            return True
        return False
    
    def get_user_favorites(self, user_id):
        """Get user's favorite templates"""
        if user_id not in self.user_favorites:
            return []
        
        favorites = []
        for template_id in self.user_favorites[user_id]:
            if template_id in self.marketplace_data["templates"]:
                favorites.append(self.marketplace_data["templates"][template_id])
        
        return favorites
    
    def create_project_from_template(self, template_id, customizations=None):
        """Create a project from a marketplace template"""
        if template_id not in self.marketplace_data["templates"]:
            return None
        
        template = self.marketplace_data["templates"][template_id]
        configuration = template["configuration"].copy()
        
        # Apply customizations
        if customizations:
            for key, value in customizations.items():
                if key in configuration:
                    configuration[key] = value
        
        # Create project configuration
        project = {
            "name": template["name"],
            "description": template["description"],
            "domain": template["domain"],
            "template_id": template_id,
            "template_version": template["version"],
            "created_at": datetime.now().isoformat(),
            **configuration
        }
        
        # Increment download count
        self.marketplace_data["templates"][template_id]["downloads"] += 1
        
        return project
    
    def submit_template(self, template_data, author):
        """Submit a new template to the marketplace"""
        template_id = template_data.get("id") or f"template_{uuid.uuid4().hex[:8]}"
        
        # Validate template data
        required_fields = ["name", "description", "domain", "configuration"]
        for field in required_fields:
            if field not in template_data:
                return False, f"Missing required field: {field}"
        
        # Create template entry
        template = {
            "id": template_id,
            "name": template_data["name"],
            "description": template_data["description"],
            "author": author,
            "version": "1.0.0",
            "rating": 0.0,
            "downloads": 0,
            "tags": template_data.get("tags", []),
            "domain": template_data["domain"],
            "difficulty": template_data.get("difficulty", "intermediate"),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "configuration": template_data["configuration"],
            "features": template_data.get("features", []),
            "use_cases": template_data.get("use_cases", [])
        }
        
        # Add to marketplace
        self.marketplace_data["templates"][template_id] = template
        
        # Add to category
        domain = template_data["domain"]
        if domain in self.marketplace_data["categories"]:
            if template_id not in self.marketplace_data["categories"][domain]["templates"]:
                self.marketplace_data["categories"][domain]["templates"].append(template_id)
        
        # Add to difficulty level
        difficulty = template_data.get("difficulty", "intermediate")
        if difficulty in self.marketplace_data["difficulty_levels"]:
            if template_id not in self.marketplace_data["difficulty_levels"][difficulty]["templates"]:
                self.marketplace_data["difficulty_levels"][difficulty]["templates"].append(template_id)
        
        return True, template_id
    
    def get_categories(self):
        """Get all available categories"""
        return self.marketplace_data["categories"]
    
    def get_difficulty_levels(self):
        """Get all available difficulty levels"""
        return self.marketplace_data["difficulty_levels"]
    
    def get_popular_templates(self, limit=10):
        """Get most popular templates"""
        templates = list(self.marketplace_data["templates"].values())
        templates.sort(key=lambda x: x["downloads"], reverse=True)
        return templates[:limit]
    
    def get_recent_templates(self, limit=10):
        """Get most recently added templates"""
        templates = list(self.marketplace_data["templates"].values())
        templates.sort(key=lambda x: x["created_at"], reverse=True)
        return templates[:limit]
    
    def get_highly_rated_templates(self, limit=10):
        """Get highest rated templates"""
        templates = list(self.marketplace_data["templates"].values())
        templates.sort(key=lambda x: x["rating"], reverse=True)
        return templates[:limit]
    
    def search_templates(self, query):
        """Search templates by query"""
        query_lower = query.lower()
        results = []
        
        for template in self.marketplace_data["templates"].values():
            if (query_lower in template["name"].lower() or
                query_lower in template["description"].lower() or
                any(query_lower in tag.lower() for tag in template["tags"]) or
                query_lower in template["domain"].lower()):
                results.append(template)
        
        # Sort by relevance (rating and downloads)
        results.sort(key=lambda x: (x["rating"], x["downloads"]), reverse=True)
        
        return results


class MarketplaceUI:
    """User interface for the project marketplace"""
    
    def __init__(self):
        """Initialize the marketplace UI"""
        self.marketplace = ProjectMarketplace()
        self.current_user = None
    
    def login(self, user_id):
        """Login user"""
        self.current_user = user_id
        print(f"✅ Logged in as {user_id}")
    
    def browse_marketplace(self):
        """Browse the marketplace"""
        print("\n🛒 AI Agent Project Marketplace")
        print("=" * 40)
        print()
        
        while True:
            print("What would you like to do?")
            print("1. Browse all templates")
            print("2. Browse by category")
            print("3. Browse by difficulty")
            print("4. Search templates")
            print("5. View popular templates")
            print("6. View recent templates")
            print("7. View highly rated templates")
            print("8. View my favorites")
            print("9. Submit a template")
            print("0. Back to main menu")
            
            choice = input("\nChoose an option (0-9): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self._browse_all_templates()
            elif choice == "2":
                self._browse_by_category()
            elif choice == "3":
                self._browse_by_difficulty()
            elif choice == "4":
                self._search_templates()
            elif choice == "5":
                self._view_popular_templates()
            elif choice == "6":
                self._view_recent_templates()
            elif choice == "7":
                self._view_highly_rated_templates()
            elif choice == "8":
                self._view_favorites()
            elif choice == "9":
                self._submit_template()
            else:
                print("❌ Invalid choice")
    
    def _browse_all_templates(self):
        """Browse all templates"""
        templates = self.marketplace.browse_templates()
        self._display_templates(templates)
    
    def _browse_by_category(self):
        """Browse templates by category"""
        categories = self.marketplace.get_categories()
        
        print("\nAvailable categories:")
        for i, (cat_id, cat_info) in enumerate(categories.items(), 1):
            print(f"{i}. {cat_info['name']} - {cat_info['description']}")
        
        try:
            choice = int(input("\nChoose a category: ")) - 1
            cat_ids = list(categories.keys())
            if 0 <= choice < len(cat_ids):
                category = cat_ids[choice]
                templates = self.marketplace.browse_templates(category=category)
                self._display_templates(templates)
            else:
                print("❌ Invalid category choice")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _browse_by_difficulty(self):
        """Browse templates by difficulty"""
        difficulties = self.marketplace.get_difficulty_levels()
        
        print("\nAvailable difficulty levels:")
        for i, (diff_id, diff_info) in enumerate(difficulties.items(), 1):
            print(f"{i}. {diff_info['name']} - {diff_info['description']}")
        
        try:
            choice = int(input("\nChoose a difficulty: ")) - 1
            diff_ids = list(difficulties.keys())
            if 0 <= choice < len(diff_ids):
                difficulty = diff_ids[choice]
                templates = self.marketplace.browse_templates(difficulty=difficulty)
                self._display_templates(templates)
            else:
                print("❌ Invalid difficulty choice")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _search_templates(self):
        """Search templates"""
        query = input("\nEnter search query: ").strip()
        if query:
            templates = self.marketplace.search_templates(query)
            self._display_templates(templates)
        else:
            print("❌ Please enter a search query")
    
    def _view_popular_templates(self):
        """View popular templates"""
        templates = self.marketplace.get_popular_templates()
        print("\n🔥 Popular Templates:")
        self._display_templates(templates)
    
    def _view_recent_templates(self):
        """View recent templates"""
        templates = self.marketplace.get_recent_templates()
        print("\n🆕 Recent Templates:")
        self._display_templates(templates)
    
    def _view_highly_rated_templates(self):
        """View highly rated templates"""
        templates = self.marketplace.get_highly_rated_templates()
        print("\n⭐ Highly Rated Templates:")
        self._display_templates(templates)
    
    def _view_favorites(self):
        """View user favorites"""
        if not self.current_user:
            print("❌ Please login first")
            return
        
        favorites = self.marketplace.get_user_favorites(self.current_user)
        if favorites:
            print(f"\n❤️  Your Favorites:")
            self._display_templates(favorites)
        else:
            print("\n❤️  You don't have any favorites yet")
    
    def _display_templates(self, templates):
        """Display templates in a formatted way"""
        if not templates:
            print("\n❌ No templates found")
            return
        
        print(f"\nFound {len(templates)} templates:")
        print("-" * 50)
        
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template['name']}")
            print(f"   {template['description']}")
            print(f"   Author: {template['author']} | Rating: {template['rating']:.1f} ⭐ | Downloads: {template['downloads']}")
            print(f"   Domain: {template['domain']} | Difficulty: {template['difficulty']}")
            print(f"   Tags: {', '.join(template['tags'])}")
            print()
        
        # Template actions
        if templates:
            self._template_actions(templates)
    
    def _template_actions(self, templates):
        """Handle template actions"""
        while True:
            print("What would you like to do?")
            print("1. View template details")
            print("2. Create project from template")
            print("3. Rate template")
            print("4. Add to favorites")
            print("5. Remove from favorites")
            print("0. Back")
            
            choice = input("\nChoose an option (0-5): ").strip()
            
            if choice == "0":
                break
            elif choice == "1":
                self._view_template_details(templates)
            elif choice == "2":
                self._create_project_from_template(templates)
            elif choice == "3":
                self._rate_template(templates)
            elif choice == "4":
                self._add_to_favorites(templates)
            elif choice == "5":
                self._remove_from_favorites(templates)
            else:
                print("❌ Invalid choice")
    
    def _view_template_details(self, templates):
        """View detailed template information"""
        try:
            choice = int(input("\nEnter template number: ")) - 1
            if 0 <= choice < len(templates):
                template = templates[choice]
                details = self.marketplace.get_template_details(template["id"])
                
                if details:
                    print(f"\n📋 {details['name']} - Details")
                    print("=" * 50)
                    print(f"Description: {details['description']}")
                    print(f"Author: {details['author']}")
                    print(f"Version: {details['version']}")
                    print(f"Rating: {details['rating']:.1f} ⭐ ({len(details['user_reviews'])} reviews)")
                    print(f"Downloads: {details['downloads']}")
                    print(f"Domain: {details['domain']}")
                    print(f"Difficulty: {details['difficulty']}")
                    print(f"Tags: {', '.join(details['tags'])}")
                    print(f"Created: {details['created_at']}")
                    print(f"Updated: {details['updated_at']}")
                    
                    print(f"\nFeatures:")
                    for feature in details['features']:
                        print(f"  • {feature}")
                    
                    print(f"\nUse Cases:")
                    for use_case in details['use_cases']:
                        print(f"  • {use_case}")
                    
                    print(f"\nConfiguration:")
                    config = details['configuration']
                    print(f"  Patterns: {', '.join(config['patterns'])}")
                    print(f"  Capabilities: {', '.join(config['capabilities'])}")
                    print(f"  Communication Style: {config['communication_style']}")
                    print(f"  Integrations: {', '.join(config['integrations'])}")
                    
                    if details['user_reviews']:
                        print(f"\nUser Reviews:")
                        for review in details['user_reviews']:
                            print(f"  {review['user']}: {review['rating']} ⭐ - {review['comment']}")
                else:
                    print("❌ Template not found")
            else:
                print("❌ Invalid template number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _create_project_from_template(self, templates):
        """Create project from template"""
        try:
            choice = int(input("\nEnter template number: ")) - 1
            if 0 <= choice < len(templates):
                template = templates[choice]
                
                print(f"\nCreating project from '{template['name']}'...")
                
                # Get customizations
                customizations = {}
                print("\nWould you like to customize the template? (y/n)")
                if input("> ").strip().lower() == 'y':
                    print("\nEnter customizations (press Enter to skip):")
                    
                    # Project name
                    custom_name = input("Project name: ").strip()
                    if custom_name:
                        customizations["name"] = custom_name
                    
                    # Project description
                    custom_desc = input("Project description: ").strip()
                    if custom_desc:
                        customizations["description"] = custom_desc
                
                # Create project
                project = self.marketplace.create_project_from_template(template["id"], customizations)
                
                if project:
                    print("✅ Project created successfully!")
                    print(f"Project: {project['name']}")
                    print(f"Domain: {project['domain']}")
                    print(f"Patterns: {', '.join(project['patterns'])}")
                    print(f"Capabilities: {', '.join(project['capabilities'])}")
                    
                    # Save project configuration
                    project_file = f"generated_projects/{project['name'].replace(' ', '_').lower()}_config.json"
                    with open(project_file, 'w') as f:
                        json.dump(project, f, indent=2, default=str)
                    print(f"Configuration saved to: {project_file}")
                else:
                    print("❌ Failed to create project")
            else:
                print("❌ Invalid template number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _rate_template(self, templates):
        """Rate a template"""
        if not self.current_user:
            print("❌ Please login first")
            return
        
        try:
            choice = int(input("\nEnter template number: ")) - 1
            if 0 <= choice < len(templates):
                template = templates[choice]
                
                print(f"\nRating '{template['name']}'")
                print("Rate from 1 to 5 stars:")
                
                while True:
                    try:
                        rating = int(input("Rating (1-5): "))
                        if 1 <= rating <= 5:
                            break
                        print("❌ Please enter a rating between 1 and 5")
                    except ValueError:
                        print("❌ Please enter a valid number")
                
                comment = input("Comment (optional): ").strip()
                
                success = self.marketplace.rate_template(template["id"], self.current_user, rating, comment)
                
                if success:
                    print("✅ Rating submitted successfully!")
                else:
                    print("❌ Failed to submit rating")
            else:
                print("❌ Invalid template number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _add_to_favorites(self, templates):
        """Add template to favorites"""
        if not self.current_user:
            print("❌ Please login first")
            return
        
        try:
            choice = int(input("\nEnter template number: ")) - 1
            if 0 <= choice < len(templates):
                template = templates[choice]
                
                success = self.marketplace.add_to_favorites(self.current_user, template["id"])
                
                if success:
                    print("✅ Added to favorites!")
                else:
                    print("❌ Failed to add to favorites")
            else:
                print("❌ Invalid template number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _remove_from_favorites(self, templates):
        """Remove template from favorites"""
        if not self.current_user:
            print("❌ Please login first")
            return
        
        try:
            choice = int(input("\nEnter template number: ")) - 1
            if 0 <= choice < len(templates):
                template = templates[choice]
                
                success = self.marketplace.remove_from_favorites(self.current_user, template["id"])
                
                if success:
                    print("✅ Removed from favorites!")
                else:
                    print("❌ Template not in favorites")
            else:
                print("❌ Invalid template number")
        except ValueError:
            print("❌ Please enter a valid number")
    
    def _submit_template(self):
        """Submit a new template"""
        if not self.current_user:
            print("❌ Please login first")
            return
        
        print("\n📝 Submit New Template")
        print("=" * 30)
        
        # Get template information
        name = input("Template name: ").strip()
        if not name:
            print("❌ Template name is required")
            return
        
        description = input("Description: ").strip()
        if not description:
            print("❌ Description is required")
            return
        
        print("\nAvailable domains:")
        domains = ["customer_service", "healthcare", "technology", "e_commerce", "education", "finance"]
        for i, domain in enumerate(domains, 1):
            print(f"{i}. {domain}")
        
        try:
            domain_choice = int(input("Choose domain: ")) - 1
            if 0 <= domain_choice < len(domains):
                domain = domains[domain_choice]
            else:
                print("❌ Invalid domain choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        print("\nDifficulty levels:")
        difficulties = ["beginner", "intermediate", "advanced"]
        for i, diff in enumerate(difficulties, 1):
            print(f"{i}. {diff}")
        
        try:
            diff_choice = int(input("Choose difficulty: ")) - 1
            if 0 <= diff_choice < len(difficulties):
                difficulty = difficulties[diff_choice]
            else:
                print("❌ Invalid difficulty choice")
                return
        except ValueError:
            print("❌ Please enter a valid number")
            return
        
        tags = input("Tags (comma-separated): ").strip()
        tags_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
        
        # Get configuration
        print("\nConfiguration:")
        patterns = input("Patterns (comma-separated): ").strip()
        patterns_list = [p.strip() for p in patterns.split(",") if p.strip()]
        
        capabilities = input("Capabilities (comma-separated): ").strip()
        capabilities_list = [c.strip() for c in capabilities.split(",") if c.strip()]
        
        communication_style = input("Communication style: ").strip()
        if not communication_style:
            communication_style = "professional and formal"
        
        integrations = input("Integrations (comma-separated): ").strip()
        integrations_list = [i.strip() for i in integrations.split(",") if i.strip()]
        
        # Create template data
        template_data = {
            "name": name,
            "description": description,
            "domain": domain,
            "difficulty": difficulty,
            "tags": tags_list,
            "configuration": {
                "patterns": patterns_list,
                "capabilities": capabilities_list,
                "communication_style": communication_style,
                "integrations": integrations_list,
                "test_requirements": {
                    "data_types": ["user_profiles", "conversations"],
                    "volume": 1000,
                    "context": domain
                }
            }
        }
        
        # Submit template
        success, template_id = self.marketplace.submit_template(template_data, self.current_user)
        
        if success:
            print(f"✅ Template submitted successfully! ID: {template_id}")
        else:
            print(f"❌ Failed to submit template: {template_id}")


def main():
    """Main entry point for the marketplace"""
    marketplace_ui = MarketplaceUI()
    
    # Login user
    user_id = input("Enter your user ID: ").strip()
    if user_id:
        marketplace_ui.login(user_id)
    
    # Browse marketplace
    marketplace_ui.browse_marketplace()


if __name__ == "__main__":
    main()

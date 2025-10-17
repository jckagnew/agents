"""
Realistic Test Data Generator for AI Agents

This module generates realistic test data using Ravi Mehta's data-driven approach,
creating structured, contextual data for testing agent patterns and behaviors.
"""

import json
import random
import uuid
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field

# Try to import faker, fallback to mock if not available
try:
    import faker
    fake = faker.Faker()
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False
    # Mock faker for when it's not available
    class MockFaker:
        def __init__(self):
            self.seed_value = 42
        
        def name(self):
            return f"User {random.randint(1, 1000)}"
        
        def email(self):
            return f"user{random.randint(1, 1000)}@example.com"
        
        def city(self):
            return f"City {random.randint(1, 100)}"
        
        def country(self):
            return f"Country {random.randint(1, 50)}"
        
        def timezone(self):
            return f"UTC{random.randint(-12, 12):+d}"
        
        def date_time_between(self, start_date, end_date):
            start = datetime.now() - timedelta(days=365)
            end = datetime.now()
            return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))
        
        def word(self):
            words = ["example", "test", "sample", "demo", "mock", "fake", "dummy", "placeholder"]
            return random.choice(words)
        
        def sentence(self):
            return f"This is a {self.word()} sentence for testing purposes."
        
        def paragraph(self):
            return f"This is a {self.word()} paragraph with {self.word()} content for testing."
        
        def paragraphs(self, nb=3, ext_word_list=None):
            return [self.paragraph() for _ in range(nb)]
        
        def url(self):
            return f"https://example.com/{self.word()}"
        
        def user_agent(self):
            agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"]
            return random.choice(agents)
        
        def ipv4(self):
            return f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        def text(self):
            return f"This is {self.word()} text content for testing purposes."
        
        def seed(self, seed):
            self.seed_value = seed
            random.seed(seed)
    
    fake = MockFaker()


class DataType(str, Enum):
    """Types of test data"""
    USER_PROFILES = "user_profiles"
    CONVERSATIONS = "conversations"
    TASKS = "tasks"
    EVENTS = "events"
    METRICS = "metrics"
    DOCUMENTS = "documents"
    INTERACTIONS = "interactions"
    SESSIONS = "sessions"
    FEEDBACK = "feedback"
    PERFORMANCE = "performance"


class DataContext(str, Enum):
    """Contexts for generated data"""
    E_COMMERCE = "e_commerce"
    HEALTHCARE = "healthcare"
    EDUCATION = "education"
    FINANCE = "finance"
    TECHNOLOGY = "technology"
    CUSTOMER_SERVICE = "customer_service"
    SOCIAL_MEDIA = "social_media"
    GAMING = "gaming"
    TRAVEL = "travel"
    REAL_ESTATE = "real_estate"


class TestDataGenerator:
    """Main test data generator"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize test data generator"""
        self.config = config or {}
        self.generated_data: Dict[str, List[Dict[str, Any]]] = {}
        self.data_schemas: Dict[str, Dict[str, Any]] = {}
        
        # Initialize data schemas
        self._initialize_data_schemas()
        
        # Set random seed for reproducibility
        random.seed(self.config.get("seed", 42))
        fake.seed(self.config.get("seed", 42))
    
    def _initialize_data_schemas(self):
        """Initialize data schemas for different data types"""
        self.data_schemas = {
            DataType.USER_PROFILES: {
                "required_fields": ["user_id", "name", "email", "created_at"],
                "optional_fields": ["age", "location", "preferences", "subscription_tier", "last_active"],
                "constraints": {
                    "age": {"min": 18, "max": 80},
                    "email": "valid_email",
                    "name": "non_empty"
                }
            },
            DataType.CONVERSATIONS: {
                "required_fields": ["conversation_id", "user_id", "messages", "started_at"],
                "optional_fields": ["ended_at", "context", "sentiment", "language", "channel"],
                "constraints": {
                    "messages": "non_empty_list",
                    "started_at": "valid_datetime"
                }
            },
            DataType.TASKS: {
                "required_fields": ["task_id", "title", "description", "priority", "status", "created_at"],
                "optional_fields": ["assigned_to", "due_date", "tags", "progress", "dependencies"],
                "constraints": {
                    "priority": {"min": 1, "max": 5},
                    "status": ["pending", "in_progress", "completed", "cancelled"]
                }
            },
            DataType.EVENTS: {
                "required_fields": ["event_id", "event_type", "timestamp", "user_id"],
                "optional_fields": ["properties", "session_id", "context", "value"],
                "constraints": {
                    "event_type": "non_empty",
                    "timestamp": "valid_datetime"
                }
            },
            DataType.METRICS: {
                "required_fields": ["metric_id", "metric_name", "value", "timestamp", "context"],
                "optional_fields": ["unit", "tags", "threshold", "trend"],
                "constraints": {
                    "value": "numeric",
                    "metric_name": "non_empty"
                }
            }
        }
    
    def generate_user_profiles(self, count: int, context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic user profiles"""
        profiles = []
        
        for _ in range(count):
            profile = {
                "user_id": str(uuid.uuid4()),
                "name": fake.name(),
                "email": fake.email(),
                "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
                "age": random.randint(18, 80),
                "location": {
                    "city": fake.city(),
                    "country": fake.country(),
                    "timezone": fake.timezone()
                },
                "preferences": self._generate_user_preferences(context),
                "subscription_tier": random.choice(["free", "basic", "premium", "enterprise"]),
                "last_active": fake.date_time_between(start_date="-30d", end_date="now").isoformat()
            }
            profiles.append(profile)
        
        self.generated_data[DataType.USER_PROFILES] = profiles
        return profiles
    
    def generate_conversations(self, count: int, user_profiles: Optional[List[Dict[str, Any]]] = None,
                             context: DataContext = DataContext.CUSTOMER_SERVICE) -> List[Dict[str, Any]]:
        """Generate realistic conversations"""
        conversations = []
        
        if not user_profiles:
            user_profiles = self.generate_user_profiles(count)
        
        for _ in range(count):
            user = random.choice(user_profiles)
            conversation = {
                "conversation_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "started_at": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
                "ended_at": fake.date_time_between(start_date="-29d", end_date="now").isoformat(),
                "context": self._generate_conversation_context(context),
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "language": random.choice(["en", "es", "fr", "de", "it"]),
                "channel": random.choice(["web", "mobile", "api", "email", "chat"]),
                "messages": self._generate_messages(context, random.randint(2, 20))
            }
            conversations.append(conversation)
        
        self.generated_data[DataType.CONVERSATIONS] = conversations
        return conversations
    
    def generate_tasks(self, count: int, context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic tasks"""
        tasks = []
        
        task_templates = self._get_task_templates(context)
        
        for _ in range(count):
            template = random.choice(task_templates)
            task = {
                "task_id": str(uuid.uuid4()),
                "title": template["title"],
                "description": template["description"],
                "priority": random.randint(1, 5),
                "status": random.choice(["pending", "in_progress", "completed", "cancelled"]),
                "created_at": fake.date_time_between(start_date="-90d", end_date="now").isoformat(),
                "assigned_to": str(uuid.uuid4()) if random.random() > 0.3 else None,
                "due_date": fake.date_time_between(start_date="now", end_date="+30d").isoformat() if random.random() > 0.5 else None,
                "tags": random.sample(template["tags"], min(random.randint(1, 3), len(template["tags"]))),
                "progress": random.randint(0, 100),
                "dependencies": [str(uuid.uuid4()) for _ in range(random.randint(0, 3))] if random.random() > 0.7 else []
            }
            tasks.append(task)
        
        self.generated_data[DataType.TASKS] = tasks
        return tasks
    
    def generate_events(self, count: int, user_profiles: Optional[List[Dict[str, Any]]] = None,
                       context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic events"""
        events = []
        
        if not user_profiles:
            user_profiles = self.generate_user_profiles(count // 10)  # 10 events per user on average
        
        event_types = self._get_event_types(context)
        
        for _ in range(count):
            user = random.choice(user_profiles)
            event_type = random.choice(event_types)
            event = {
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
                "user_id": user["user_id"],
                "session_id": str(uuid.uuid4()),
                "properties": self._generate_event_properties(event_type, context),
                "context": {
                    "page": fake.url(),
                    "referrer": fake.url() if random.random() > 0.5 else None,
                    "user_agent": fake.user_agent(),
                    "ip_address": fake.ipv4()
                },
                "value": random.uniform(0, 1000) if random.random() > 0.7 else None
            }
            events.append(event)
        
        self.generated_data[DataType.EVENTS] = events
        return events
    
    def generate_metrics(self, count: int, context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic metrics"""
        metrics = []
        
        metric_types = self._get_metric_types(context)
        
        for _ in range(count):
            metric_type = random.choice(metric_types)
            metric = {
                "metric_id": str(uuid.uuid4()),
                "metric_name": metric_type["name"],
                "value": self._generate_metric_value(metric_type),
                "timestamp": fake.date_time_between(start_date="-7d", end_date="now").isoformat(),
                "context": {
                    "environment": random.choice(["production", "staging", "development"]),
                    "service": metric_type["service"],
                    "region": random.choice(["us-east", "us-west", "eu-west", "ap-south"])
                },
                "unit": metric_type["unit"],
                "tags": random.sample(metric_type["tags"], min(random.randint(1, 3), len(metric_type["tags"]))),
                "threshold": metric_type.get("threshold"),
                "trend": random.choice(["increasing", "decreasing", "stable", "volatile"])
            }
            metrics.append(metric)
        
        self.generated_data[DataType.METRICS] = metrics
        return metrics
    
    def generate_documents(self, count: int, context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic documents"""
        documents = []
        
        doc_types = self._get_document_types(context)
        
        for _ in range(count):
            doc_type = random.choice(doc_types)
            document = {
                "document_id": str(uuid.uuid4()),
                "title": doc_type["title_template"].format(
                    topic=fake.word().title(),
                    number=random.randint(1, 100)
                ),
                "content": self._generate_document_content(doc_type, context),
                "document_type": doc_type["type"],
                "created_at": fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
                "author": fake.name(),
                "tags": random.sample(doc_type["tags"], min(random.randint(1, 4), len(doc_type["tags"]))),
                "status": random.choice(["draft", "review", "published", "archived"]),
                "word_count": random.randint(100, 5000),
                "language": random.choice(["en", "es", "fr", "de"]),
                "metadata": {
                    "version": f"1.{random.randint(0, 9)}",
                    "category": doc_type["category"],
                    "difficulty": random.choice(["beginner", "intermediate", "advanced"]),
                    "read_time": random.randint(2, 30)
                }
            }
            documents.append(document)
        
        self.generated_data[DataType.DOCUMENTS] = documents
        return documents
    
    def generate_interactions(self, count: int, user_profiles: Optional[List[Dict[str, Any]]] = None,
                            context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic interactions"""
        interactions = []
        
        if not user_profiles:
            user_profiles = self.generate_user_profiles(count // 5)  # 5 interactions per user on average
        
        interaction_types = self._get_interaction_types(context)
        
        for _ in range(count):
            user = random.choice(user_profiles)
            interaction_type = random.choice(interaction_types)
            interaction = {
                "interaction_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "interaction_type": interaction_type["type"],
                "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
                "duration": random.randint(1, 3600),  # seconds
                "context": {
                    "page": fake.url(),
                    "feature": interaction_type["feature"],
                    "device": random.choice(["desktop", "mobile", "tablet"]),
                    "browser": random.choice(["chrome", "firefox", "safari", "edge"])
                },
                "outcome": random.choice(["success", "failure", "partial", "timeout"]),
                "data": self._generate_interaction_data(interaction_type, context),
                "feedback": {
                    "rating": random.randint(1, 5) if random.random() > 0.3 else None,
                    "comment": fake.sentence() if random.random() > 0.7 else None
                }
            }
            interactions.append(interaction)
        
        self.generated_data[DataType.INTERACTIONS] = interactions
        return interactions
    
    def generate_sessions(self, count: int, user_profiles: Optional[List[Dict[str, Any]]] = None,
                         context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic user sessions"""
        sessions = []
        
        if not user_profiles:
            user_profiles = self.generate_user_profiles(count // 3)  # 3 sessions per user on average
        
        for _ in range(count):
            user = random.choice(user_profiles)
            session = {
                "session_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "started_at": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
                "ended_at": fake.date_time_between(start_date="-29d", end_date="now").isoformat(),
                "duration": random.randint(60, 7200),  # 1 minute to 2 hours
                "context": {
                    "platform": random.choice(["web", "mobile", "api"]),
                    "device": random.choice(["desktop", "mobile", "tablet"]),
                    "browser": random.choice(["chrome", "firefox", "safari", "edge"]),
                    "os": random.choice(["windows", "macos", "linux", "ios", "android"]),
                    "ip_address": fake.ipv4(),
                    "location": {
                        "city": fake.city(),
                        "country": fake.country(),
                        "timezone": fake.timezone()
                    }
                },
                "activities": random.randint(1, 50),
                "pages_visited": random.randint(1, 20),
                "features_used": random.sample(self._get_features(context), min(random.randint(1, 5), len(self._get_features(context)))),
                "conversion": random.random() > 0.8,  # 20% conversion rate
                "revenue": random.uniform(0, 500) if random.random() > 0.7 else 0
            }
            sessions.append(session)
        
        self.generated_data[DataType.SESSIONS] = sessions
        return sessions
    
    def generate_feedback(self, count: int, user_profiles: Optional[List[Dict[str, Any]]] = None,
                         context: DataContext = DataContext.CUSTOMER_SERVICE) -> List[Dict[str, Any]]:
        """Generate realistic feedback"""
        feedback_list = []
        
        if not user_profiles:
            user_profiles = self.generate_user_profiles(count // 2)  # 2 feedback per user on average
        
        feedback_types = self._get_feedback_types(context)
        
        for _ in range(count):
            user = random.choice(user_profiles)
            feedback_type = random.choice(feedback_types)
            feedback = {
                "feedback_id": str(uuid.uuid4()),
                "user_id": user["user_id"],
                "feedback_type": feedback_type["type"],
                "rating": random.randint(1, 5),
                "comment": fake.paragraph() if random.random() > 0.3 else None,
                "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
                "context": {
                    "feature": feedback_type["feature"],
                    "version": f"1.{random.randint(0, 9)}",
                    "platform": random.choice(["web", "mobile", "api"])
                },
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "category": feedback_type["category"],
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["new", "in_review", "resolved", "closed"]),
                "tags": random.sample(feedback_type["tags"], min(random.randint(1, 3), len(feedback_type["tags"])))
            }
            feedback_list.append(feedback)
        
        self.generated_data[DataType.FEEDBACK] = feedback_list
        return feedback_list
    
    def generate_performance_data(self, count: int, context: DataContext = DataContext.TECHNOLOGY) -> List[Dict[str, Any]]:
        """Generate realistic performance data"""
        performance_data = []
        
        performance_metrics = self._get_performance_metrics(context)
        
        for _ in range(count):
            metric = random.choice(performance_metrics)
            data_point = {
                "performance_id": str(uuid.uuid4()),
                "metric_name": metric["name"],
                "value": self._generate_performance_value(metric),
                "timestamp": fake.date_time_between(start_date="-7d", end_date="now").isoformat(),
                "context": {
                    "service": metric["service"],
                    "endpoint": metric.get("endpoint", "/api/v1/health"),
                    "method": random.choice(["GET", "POST", "PUT", "DELETE"]),
                    "status_code": random.choice([200, 201, 400, 401, 404, 500]),
                    "environment": random.choice(["production", "staging", "development"])
                },
                "dimensions": {
                    "region": random.choice(["us-east", "us-west", "eu-west", "ap-south"]),
                    "datacenter": random.choice(["dc1", "dc2", "dc3"]),
                    "instance_type": random.choice(["small", "medium", "large", "xlarge"])
                },
                "tags": random.sample(metric["tags"], min(random.randint(1, 3), len(metric["tags"]))),
                "threshold": metric.get("threshold"),
                "alert_level": random.choice(["normal", "warning", "critical"])
            }
            performance_data.append(data_point)
        
        self.generated_data[DataType.PERFORMANCE] = performance_data
        return performance_data
    
    def _generate_user_preferences(self, context: DataContext) -> Dict[str, Any]:
        """Generate user preferences based on context"""
        preferences = {
            "notifications": {
                "email": random.choice([True, False]),
                "push": random.choice([True, False]),
                "sms": random.choice([True, False])
            },
            "privacy": {
                "data_sharing": random.choice([True, False]),
                "analytics": random.choice([True, False])
            }
        }
        
        if context == DataContext.E_COMMERCE:
            preferences.update({
                "shopping": {
                    "categories": random.sample(["electronics", "clothing", "books", "home"], min(random.randint(1, 3), 4)),
                    "price_range": random.choice(["budget", "mid-range", "premium"]),
                    "shipping": random.choice(["standard", "express", "overnight"])
                }
            })
        elif context == DataContext.HEALTHCARE:
            preferences.update({
                "health": {
                    "conditions": random.sample(["diabetes", "hypertension", "asthma"], min(random.randint(0, 2), 3)),
                    "medications": random.randint(0, 5),
                    "appointments": random.choice(["weekly", "monthly", "as_needed"])
                }
            })
        
        return preferences
    
    def _generate_conversation_context(self, context: DataContext) -> Dict[str, Any]:
        """Generate conversation context based on domain"""
        contexts = {
            DataContext.CUSTOMER_SERVICE: {
                "issue_type": random.choice(["billing", "technical", "account", "product"]),
                "urgency": random.choice(["low", "medium", "high"]),
                "channel": random.choice(["chat", "email", "phone"])
            },
            DataContext.E_COMMERCE: {
                "product_category": random.choice(["electronics", "clothing", "books"]),
                "purchase_intent": random.choice(["browsing", "comparing", "ready_to_buy"]),
                "cart_value": random.uniform(0, 1000)
            },
            DataContext.HEALTHCARE: {
                "appointment_type": random.choice(["consultation", "follow_up", "emergency"]),
                "specialty": random.choice(["cardiology", "dermatology", "pediatrics"]),
                "insurance": random.choice([True, False])
            }
        }
        
        return contexts.get(context, {"general": "conversation"})
    
    def _generate_messages(self, context: DataContext, count: int) -> List[Dict[str, Any]]:
        """Generate realistic messages for conversations"""
        messages = []
        
        for i in range(count):
            is_user = i % 2 == 0
            message = {
                "message_id": str(uuid.uuid4()),
                "sender": "user" if is_user else "assistant",
                "content": self._generate_message_content(is_user, context),
                "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat(),
                "message_type": random.choice(["text", "image", "file", "link"]),
                "sentiment": random.choice(["positive", "neutral", "negative"]),
                "metadata": {
                    "word_count": random.randint(1, 50),
                    "language": random.choice(["en", "es", "fr", "de"])
                }
            }
            messages.append(message)
        
        return messages
    
    def _generate_message_content(self, is_user: bool, context: DataContext) -> str:
        """Generate message content based on context and sender"""
        if is_user:
            user_messages = {
                DataContext.CUSTOMER_SERVICE: [
                    "I'm having trouble with my account",
                    "Can you help me with billing?",
                    "I need to update my information",
                    "There's an issue with my order"
                ],
                DataContext.E_COMMERCE: [
                    "What's the return policy?",
                    "Do you have this in a different size?",
                    "When will this be back in stock?",
                    "Can you recommend similar products?"
                ],
                DataContext.HEALTHCARE: [
                    "I need to schedule an appointment",
                    "Can I get my test results?",
                    "I have a question about my medication",
                    "Is the doctor available today?"
                ]
            }
            return random.choice(user_messages.get(context, ["Hello", "I need help", "Can you assist me?"]))
        else:
            assistant_messages = [
                "I'd be happy to help you with that",
                "Let me look into that for you",
                "I understand your concern",
                "Here's what I can do for you"
            ]
            return random.choice(assistant_messages)
    
    def _get_task_templates(self, context: DataContext) -> List[Dict[str, Any]]:
        """Get task templates based on context"""
        templates = {
            DataContext.TECHNOLOGY: [
                {
                    "title": "Implement {feature}",
                    "description": "Develop and test the {feature} functionality",
                    "tags": ["development", "testing", "feature"]
                },
                {
                    "title": "Fix {bug_type} bug",
                    "description": "Investigate and resolve the {bug_type} issue",
                    "tags": ["bugfix", "debugging", "maintenance"]
                },
                {
                    "title": "Optimize {component}",
                    "description": "Improve performance of the {component} system",
                    "tags": ["optimization", "performance", "refactoring"]
                }
            ],
            DataContext.E_COMMERCE: [
                {
                    "title": "Update product catalog",
                    "description": "Add new products and update existing ones",
                    "tags": ["catalog", "products", "inventory"]
                },
                {
                    "title": "Process {order_count} orders",
                    "description": "Handle order fulfillment and shipping",
                    "tags": ["orders", "fulfillment", "shipping"]
                }
            ]
        }
        
        return templates.get(context, [
            {
                "title": "Complete {task_name}",
                "description": "Work on the {task_name} assignment",
                "tags": ["general", "task"]
            }
        ])
    
    def _get_event_types(self, context: DataContext) -> List[str]:
        """Get event types based on context"""
        event_types = {
            DataContext.TECHNOLOGY: [
                "user_login", "user_logout", "feature_used", "error_occurred",
                "api_call", "page_view", "button_click", "search_performed"
            ],
            DataContext.E_COMMERCE: [
                "product_viewed", "cart_added", "checkout_started", "purchase_completed",
                "product_searched", "wishlist_added", "review_submitted"
            ],
            DataContext.HEALTHCARE: [
                "appointment_scheduled", "test_result_viewed", "medication_reminder",
                "symptom_logged", "prescription_renewed"
            ]
        }
        
        return event_types.get(context, ["event_occurred", "action_taken", "state_changed"])
    
    def _generate_event_properties(self, event_type: str, context: DataContext) -> Dict[str, Any]:
        """Generate event properties based on event type"""
        properties = {
            "event_type": event_type,
            "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat()
        }
        
        if "login" in event_type:
            properties.update({
                "method": random.choice(["email", "social", "sso"]),
                "success": random.choice([True, False])
            })
        elif "purchase" in event_type:
            properties.update({
                "amount": random.uniform(10, 1000),
                "currency": "USD",
                "payment_method": random.choice(["credit_card", "paypal", "apple_pay"])
            })
        elif "error" in event_type:
            properties.update({
                "error_code": random.randint(100, 599),
                "error_message": fake.sentence(),
                "stack_trace": fake.text()[:200]
            })
        
        return properties
    
    def _get_metric_types(self, context: DataContext) -> List[Dict[str, Any]]:
        """Get metric types based on context"""
        metric_types = {
            DataContext.TECHNOLOGY: [
                {"name": "response_time", "service": "api", "unit": "ms", "tags": ["performance", "api"]},
                {"name": "error_rate", "service": "api", "unit": "%", "tags": ["reliability", "errors"]},
                {"name": "throughput", "service": "api", "unit": "requests/sec", "tags": ["performance", "load"]},
                {"name": "cpu_usage", "service": "infrastructure", "unit": "%", "tags": ["system", "resources"]},
                {"name": "memory_usage", "service": "infrastructure", "unit": "MB", "tags": ["system", "resources"]}
            ],
            DataContext.E_COMMERCE: [
                {"name": "conversion_rate", "service": "analytics", "unit": "%", "tags": ["business", "conversion"]},
                {"name": "cart_abandonment", "service": "analytics", "unit": "%", "tags": ["business", "conversion"]},
                {"name": "average_order_value", "service": "analytics", "unit": "USD", "tags": ["business", "revenue"]},
                {"name": "customer_satisfaction", "service": "feedback", "unit": "rating", "tags": ["quality", "satisfaction"]}
            ]
        }
        
        return metric_types.get(context, [
            {"name": "custom_metric", "service": "general", "unit": "count", "tags": ["general"]}
        ])
    
    def _generate_metric_value(self, metric_type: Dict[str, Any]) -> float:
        """Generate realistic metric values"""
        if metric_type["name"] == "response_time":
            return random.uniform(50, 2000)  # 50ms to 2s
        elif metric_type["name"] == "error_rate":
            return random.uniform(0, 5)  # 0-5%
        elif metric_type["name"] == "throughput":
            return random.uniform(100, 10000)  # 100-10k requests/sec
        elif metric_type["name"] in ["cpu_usage", "memory_usage"]:
            return random.uniform(10, 90)  # 10-90%
        else:
            return random.uniform(0, 100)
    
    def _get_document_types(self, context: DataContext) -> List[Dict[str, Any]]:
        """Get document types based on context"""
        doc_types = {
            DataContext.TECHNOLOGY: [
                {
                    "type": "technical_spec",
                    "title_template": "{topic} Technical Specification v{number}",
                    "category": "technical",
                    "tags": ["specification", "technical", "architecture"]
                },
                {
                    "type": "api_documentation",
                    "title_template": "{topic} API Documentation",
                    "category": "documentation",
                    "tags": ["api", "documentation", "reference"]
                },
                {
                    "type": "bug_report",
                    "title_template": "Bug Report: {topic} #{number}",
                    "category": "issue",
                    "tags": ["bug", "issue", "report"]
                }
            ],
            DataContext.E_COMMERCE: [
                {
                    "type": "product_description",
                    "title_template": "{topic} Product Description",
                    "category": "marketing",
                    "tags": ["product", "marketing", "description"]
                },
                {
                    "type": "policy_document",
                    "title_template": "{topic} Policy Document",
                    "category": "legal",
                    "tags": ["policy", "legal", "terms"]
                }
            ]
        }
        
        return doc_types.get(context, [
            {
                "type": "general_document",
                "title_template": "{topic} Document {number}",
                "category": "general",
                "tags": ["document", "general"]
            }
        ])
    
    def _generate_document_content(self, doc_type: Dict[str, Any], context: DataContext) -> str:
        """Generate document content based on type"""
        if doc_type["type"] == "technical_spec":
            return f"""
# {doc_type['title_template']}

## Overview
This document describes the technical specification for {fake.word().title()}.

## Requirements
- {fake.sentence()}
- {fake.sentence()}
- {fake.sentence()}

## Implementation
The implementation should follow these guidelines:
1. {fake.sentence()}
2. {fake.sentence()}
3. {fake.sentence()}

## Testing
Test cases should cover:
- {fake.sentence()}
- {fake.sentence()}
"""
        elif doc_type["type"] == "api_documentation":
            return f"""
# {doc_type['title_template']}

## Endpoints

### GET /api/v1/{fake.word()}
Description: {fake.sentence()}

Parameters:
- {fake.word()}: {fake.sentence()}
- {fake.word()}: {fake.sentence()}

Response:
```json
{{
  "status": "success",
  "data": {{
    "id": "string",
    "name": "string"
  }}
}}
```
"""
        else:
            return fake.paragraphs(nb=3, ext_word_list=None)
    
    def _get_interaction_types(self, context: DataContext) -> List[Dict[str, Any]]:
        """Get interaction types based on context"""
        interaction_types = {
            DataContext.TECHNOLOGY: [
                {"type": "feature_usage", "feature": "dashboard", "tags": ["feature", "usage"]},
                {"type": "api_call", "feature": "api", "tags": ["api", "integration"]},
                {"type": "search", "feature": "search", "tags": ["search", "discovery"]},
                {"type": "navigation", "feature": "ui", "tags": ["navigation", "ui"]}
            ],
            DataContext.E_COMMERCE: [
                {"type": "product_view", "feature": "catalog", "tags": ["product", "viewing"]},
                {"type": "add_to_cart", "feature": "shopping", "tags": ["cart", "purchase"]},
                {"type": "checkout", "feature": "checkout", "tags": ["checkout", "purchase"]},
                {"type": "search", "feature": "search", "tags": ["search", "discovery"]}
            ]
        }
        
        return interaction_types.get(context, [
            {"type": "general_interaction", "feature": "general", "tags": ["interaction"]}
        ])
    
    def _generate_interaction_data(self, interaction_type: Dict[str, Any], context: DataContext) -> Dict[str, Any]:
        """Generate interaction data based on type"""
        data = {
            "interaction_type": interaction_type["type"],
            "feature": interaction_type["feature"],
            "timestamp": fake.date_time_between(start_date="-30d", end_date="now").isoformat()
        }
        
        if interaction_type["type"] == "feature_usage":
            data.update({
                "feature_name": interaction_type["feature"],
                "duration": random.randint(1, 300),
                "success": random.choice([True, False])
            })
        elif interaction_type["type"] == "api_call":
            data.update({
                "endpoint": f"/api/v1/{fake.word()}",
                "method": random.choice(["GET", "POST", "PUT", "DELETE"]),
                "status_code": random.choice([200, 201, 400, 401, 404, 500]),
                "response_time": random.uniform(10, 1000)
            })
        elif interaction_type["type"] == "search":
            data.update({
                "query": fake.word(),
                "results_count": random.randint(0, 100),
                "filters_applied": random.randint(0, 5)
            })
        
        return data
    
    def _get_features(self, context: DataContext) -> List[str]:
        """Get features based on context"""
        features = {
            DataContext.TECHNOLOGY: ["dashboard", "api", "search", "analytics", "settings"],
            DataContext.E_COMMERCE: ["catalog", "cart", "checkout", "search", "reviews"],
            DataContext.HEALTHCARE: ["appointments", "records", "prescriptions", "billing", "messaging"]
        }
        
        return features.get(context, ["feature1", "feature2", "feature3"])
    
    def _get_feedback_types(self, context: DataContext) -> List[Dict[str, Any]]:
        """Get feedback types based on context"""
        feedback_types = {
            DataContext.CUSTOMER_SERVICE: [
                {"type": "service_quality", "feature": "support", "category": "service", "tags": ["quality", "support"]},
                {"type": "response_time", "feature": "support", "category": "performance", "tags": ["speed", "response"]},
                {"type": "resolution", "feature": "support", "category": "outcome", "tags": ["resolution", "satisfaction"]}
            ],
            DataContext.E_COMMERCE: [
                {"type": "product_quality", "feature": "catalog", "category": "product", "tags": ["quality", "product"]},
                {"type": "shipping", "feature": "checkout", "category": "delivery", "tags": ["shipping", "delivery"]},
                {"type": "website_usability", "feature": "ui", "category": "usability", "tags": ["usability", "ui"]}
            ]
        }
        
        return feedback_types.get(context, [
            {"type": "general_feedback", "feature": "general", "category": "general", "tags": ["feedback"]}
        ])
    
    def _get_performance_metrics(self, context: DataContext) -> List[Dict[str, Any]]:
        """Get performance metrics based on context"""
        performance_metrics = {
            DataContext.TECHNOLOGY: [
                {"name": "response_time", "service": "api", "unit": "ms", "threshold": 500, "tags": ["performance"]},
                {"name": "error_rate", "service": "api", "unit": "%", "threshold": 1, "tags": ["reliability"]},
                {"name": "throughput", "service": "api", "unit": "rps", "threshold": 1000, "tags": ["performance"]},
                {"name": "cpu_usage", "service": "infrastructure", "unit": "%", "threshold": 80, "tags": ["system"]},
                {"name": "memory_usage", "service": "infrastructure", "unit": "%", "threshold": 85, "tags": ["system"]}
            ]
        }
        
        return performance_metrics.get(context, [
            {"name": "custom_metric", "service": "general", "unit": "count", "threshold": 100, "tags": ["general"]}
        ])
    
    def _generate_performance_value(self, metric: Dict[str, Any]) -> float:
        """Generate performance values based on metric type"""
        if metric["name"] == "response_time":
            return random.uniform(50, 2000)
        elif metric["name"] == "error_rate":
            return random.uniform(0, 5)
        elif metric["name"] == "throughput":
            return random.uniform(100, 10000)
        elif metric["name"] in ["cpu_usage", "memory_usage"]:
            return random.uniform(10, 95)
        else:
            return random.uniform(0, 1000)
    
    def export_data(self, data_type: DataType, format: str = "json") -> Union[str, Dict[str, Any]]:
        """Export generated data in specified format"""
        if data_type not in self.generated_data:
            raise ValueError(f"No data generated for type: {data_type}")
        
        data = self.generated_data[data_type]
        
        if format == "json":
            return {
                "data_type": data_type.value,
                "count": len(data),
                "generated_at": datetime.now().isoformat(),
                "data": data
            }
        elif format == "csv":
            # Simple CSV export (would need proper CSV library for complex data)
            if not data:
                return ""
            
            headers = list(data[0].keys())
            rows = [headers]
            for item in data:
                row = []
                for header in headers:
                    value = item.get(header, "")
                    if isinstance(value, (dict, list)):
                        value = json.dumps(value)
                    row.append(str(value))
                rows.append(row)
            
            return "\n".join([",".join(row) for row in rows])
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of all generated data"""
        summary = {
            "total_data_types": len(self.generated_data),
            "data_types": {},
            "total_records": 0
        }
        
        for data_type, data in self.generated_data.items():
            summary["data_types"][data_type.value] = {
                "count": len(data),
                "sample_fields": list(data[0].keys()) if data else []
            }
            summary["total_records"] += len(data)
        
        return summary


# Example usage and testing
if __name__ == "__main__":
    print("🧪 Testing Test Data Generator")
    print("=" * 35)
    
    # Create generator
    generator = TestDataGenerator({"seed": 42})
    
    # Test user profiles
    users = generator.generate_user_profiles(5, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(users)} user profiles")
    
    # Test conversations
    conversations = generator.generate_conversations(3, users, DataContext.CUSTOMER_SERVICE)
    print(f"✅ Generated {len(conversations)} conversations")
    
    # Test tasks
    tasks = generator.generate_tasks(5, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(tasks)} tasks")
    
    # Test events
    events = generator.generate_events(10, users, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(events)} events")
    
    # Test metrics
    metrics = generator.generate_metrics(8, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(metrics)} metrics")
    
    # Test documents
    documents = generator.generate_documents(3, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(documents)} documents")
    
    # Test interactions
    interactions = generator.generate_interactions(5, users, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(interactions)} interactions")
    
    # Test sessions
    sessions = generator.generate_sessions(4, users, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(sessions)} sessions")
    
    # Test feedback
    feedback = generator.generate_feedback(6, users, DataContext.CUSTOMER_SERVICE)
    print(f"✅ Generated {len(feedback)} feedback")
    
    # Test performance data
    performance = generator.generate_performance_data(7, DataContext.TECHNOLOGY)
    print(f"✅ Generated {len(performance)} performance data points")
    
    # Test data summary
    summary = generator.get_data_summary()
    print(f"✅ Data summary: {summary['total_records']} total records across {summary['total_data_types']} types")
    
    # Test export
    json_export = generator.export_data(DataType.USER_PROFILES, "json")
    print(f"✅ JSON export: {json_export['count']} records")
    
    print("🎯 Test Data Generator test completed!")

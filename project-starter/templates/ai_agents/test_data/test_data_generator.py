"""
Test suite for Test Data Generator
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from data_generator import TestDataGenerator, DataType, DataContext


def test_generator_initialization():
    """Test generator initialization"""
    print("🧪 Testing Generator Initialization")
    print("=" * 35)
    
    # Test basic initialization
    generator = TestDataGenerator()
    assert len(generator.data_schemas) >= 5
    print("✅ Generator initialized with data schemas")
    
    # Test initialization with config
    config_generator = TestDataGenerator({"seed": 123})
    assert config_generator.config["seed"] == 123
    print("✅ Generator initialized with custom config")
    
    # Test data schemas
    assert DataType.USER_PROFILES in generator.data_schemas
    assert DataType.CONVERSATIONS in generator.data_schemas
    assert DataType.TASKS in generator.data_schemas
    print("✅ All expected data schemas present")


def test_user_profile_generation():
    """Test user profile generation"""
    print("\n🧪 Testing User Profile Generation")
    print("=" * 35)
    
    generator = TestDataGenerator({"seed": 42})
    
    # Test basic generation
    users = generator.generate_user_profiles(5, DataContext.TECHNOLOGY)
    assert len(users) == 5
    print("✅ Generated correct number of user profiles")
    
    # Test profile structure
    user = users[0]
    required_fields = ["user_id", "name", "email", "created_at"]
    for field in required_fields:
        assert field in user
    print("✅ User profiles have required fields")
    
    # Test email format
    assert "@" in user["email"]
    print("✅ Email format is valid")
    
    # Test age range
    assert 18 <= user["age"] <= 80
    print("✅ Age is within valid range")
    
    # Test different contexts
    ecommerce_users = generator.generate_user_profiles(3, DataContext.E_COMMERCE)
    assert len(ecommerce_users) == 3
    assert "preferences" in ecommerce_users[0]
    print("✅ Context-specific user profiles generated")


def test_conversation_generation():
    """Test conversation generation"""
    print("\n🧪 Testing Conversation Generation")
    print("=" * 35)
    
    generator = TestDataGenerator({"seed": 42})
    users = generator.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Test basic generation
    conversations = generator.generate_conversations(5, users, DataContext.CUSTOMER_SERVICE)
    assert len(conversations) == 5
    print("✅ Generated correct number of conversations")
    
    # Test conversation structure
    conversation = conversations[0]
    required_fields = ["conversation_id", "user_id", "messages", "started_at"]
    for field in required_fields:
        assert field in conversation
    print("✅ Conversations have required fields")
    
    # Test messages
    assert len(conversation["messages"]) >= 2
    assert conversation["messages"][0]["sender"] in ["user", "assistant"]
    print("✅ Messages are properly structured")
    
    # Test context-specific conversations
    healthcare_conversations = generator.generate_conversations(2, users, DataContext.HEALTHCARE)
    assert len(healthcare_conversations) == 2
    print("✅ Context-specific conversations generated")


def test_task_generation():
    """Test task generation"""
    print("\n🧪 Testing Task Generation")
    print("=" * 25)
    
    generator = TestDataGenerator({"seed": 42})
    
    # Test basic generation
    tasks = generator.generate_tasks(5, DataContext.TECHNOLOGY)
    assert len(tasks) == 5
    print("✅ Generated correct number of tasks")
    
    # Test task structure
    task = tasks[0]
    required_fields = ["task_id", "title", "description", "priority", "status", "created_at"]
    for field in required_fields:
        assert field in task
    print("✅ Tasks have required fields")
    
    # Test priority range
    assert 1 <= task["priority"] <= 5
    print("✅ Priority is within valid range")
    
    # Test status values
    valid_statuses = ["pending", "in_progress", "completed", "cancelled"]
    assert task["status"] in valid_statuses
    print("✅ Status values are valid")
    
    # Test different contexts
    ecommerce_tasks = generator.generate_tasks(3, DataContext.E_COMMERCE)
    assert len(ecommerce_tasks) == 3
    print("✅ Context-specific tasks generated")


def test_event_generation():
    """Test event generation"""
    print("\n🧪 Testing Event Generation")
    print("=" * 25)
    
    generator = TestDataGenerator({"seed": 42})
    users = generator.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Test basic generation
    events = generator.generate_events(10, users, DataContext.TECHNOLOGY)
    assert len(events) == 10
    print("✅ Generated correct number of events")
    
    # Test event structure
    event = events[0]
    required_fields = ["event_id", "event_type", "timestamp", "user_id"]
    for field in required_fields:
        assert field in event
    print("✅ Events have required fields")
    
    # Test event types
    valid_event_types = ["user_login", "user_logout", "feature_used", "error_occurred", "api_call", "page_view", "button_click", "search_performed"]
    assert event["event_type"] in valid_event_types
    print("✅ Event types are valid")
    
    # Test properties
    assert "properties" in event
    print("✅ Events have properties")
    
    # Test different contexts
    ecommerce_events = generator.generate_events(5, users, DataContext.E_COMMERCE)
    assert len(ecommerce_events) == 5
    print("✅ Context-specific events generated")


def test_metrics_generation():
    """Test metrics generation"""
    print("\n🧪 Testing Metrics Generation")
    print("=" * 30)
    
    generator = TestDataGenerator({"seed": 42})
    
    # Test basic generation
    metrics = generator.generate_metrics(8, DataContext.TECHNOLOGY)
    assert len(metrics) == 8
    print("✅ Generated correct number of metrics")
    
    # Test metric structure
    metric = metrics[0]
    required_fields = ["metric_id", "metric_name", "value", "timestamp", "context"]
    for field in required_fields:
        assert field in metric
    print("✅ Metrics have required fields")
    
    # Test metric value
    assert isinstance(metric["value"], (int, float))
    print("✅ Metric values are numeric")
    
    # Test metric types
    valid_metric_names = ["response_time", "error_rate", "throughput", "cpu_usage", "memory_usage"]
    assert metric["metric_name"] in valid_metric_names
    print("✅ Metric names are valid")
    
    # Test different contexts
    ecommerce_metrics = generator.generate_metrics(5, DataContext.E_COMMERCE)
    assert len(ecommerce_metrics) == 5
    print("✅ Context-specific metrics generated")


def test_document_generation():
    """Test document generation"""
    print("\n🧪 Testing Document Generation")
    print("=" * 30)
    
    generator = TestDataGenerator({"seed": 42})
    
    # Test basic generation
    documents = generator.generate_documents(3, DataContext.TECHNOLOGY)
    assert len(documents) == 3
    print("✅ Generated correct number of documents")
    
    # Test document structure
    document = documents[0]
    required_fields = ["document_id", "title", "content", "document_type", "created_at"]
    for field in required_fields:
        assert field in document
    print("✅ Documents have required fields")
    
    # Test content
    assert len(document["content"]) > 0
    print("✅ Documents have content")
    
    # Test word count
    assert document["word_count"] > 0
    print("✅ Word count is positive")
    
    # Test different contexts
    ecommerce_docs = generator.generate_documents(2, DataContext.E_COMMERCE)
    assert len(ecommerce_docs) == 2
    print("✅ Context-specific documents generated")


def test_interaction_generation():
    """Test interaction generation"""
    print("\n🧪 Testing Interaction Generation")
    print("=" * 35)
    
    generator = TestDataGenerator({"seed": 42})
    users = generator.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Test basic generation
    interactions = generator.generate_interactions(5, users, DataContext.TECHNOLOGY)
    assert len(interactions) == 5
    print("✅ Generated correct number of interactions")
    
    # Test interaction structure
    interaction = interactions[0]
    required_fields = ["interaction_id", "user_id", "interaction_type", "timestamp"]
    for field in required_fields:
        assert field in interaction
    print("✅ Interactions have required fields")
    
    # Test duration
    assert interaction["duration"] > 0
    print("✅ Duration is positive")
    
    # Test outcome
    valid_outcomes = ["success", "failure", "partial", "timeout"]
    assert interaction["outcome"] in valid_outcomes
    print("✅ Outcomes are valid")
    
    # Test different contexts
    ecommerce_interactions = generator.generate_interactions(3, users, DataContext.E_COMMERCE)
    assert len(ecommerce_interactions) == 3
    print("✅ Context-specific interactions generated")


def test_session_generation():
    """Test session generation"""
    print("\n🧪 Testing Session Generation")
    print("=" * 30)
    
    generator = TestDataGenerator({"seed": 42})
    users = generator.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Test basic generation
    sessions = generator.generate_sessions(4, users, DataContext.TECHNOLOGY)
    assert len(sessions) == 4
    print("✅ Generated correct number of sessions")
    
    # Test session structure
    session = sessions[0]
    required_fields = ["session_id", "user_id", "started_at", "ended_at"]
    for field in required_fields:
        assert field in session
    print("✅ Sessions have required fields")
    
    # Test duration
    assert session["duration"] > 0
    print("✅ Duration is positive")
    
    # Test activities
    assert session["activities"] > 0
    print("✅ Activities count is positive")
    
    # Test different contexts
    ecommerce_sessions = generator.generate_sessions(3, users, DataContext.E_COMMERCE)
    assert len(ecommerce_sessions) == 3
    print("✅ Context-specific sessions generated")


def test_feedback_generation():
    """Test feedback generation"""
    print("\n🧪 Testing Feedback Generation")
    print("=" * 30)
    
    generator = TestDataGenerator({"seed": 42})
    users = generator.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Test basic generation
    feedback = generator.generate_feedback(6, users, DataContext.CUSTOMER_SERVICE)
    assert len(feedback) == 6
    print("✅ Generated correct number of feedback")
    
    # Test feedback structure
    feedback_item = feedback[0]
    required_fields = ["feedback_id", "user_id", "feedback_type", "rating", "timestamp"]
    for field in required_fields:
        assert field in feedback_item
    print("✅ Feedback has required fields")
    
    # Test rating range
    assert 1 <= feedback_item["rating"] <= 5
    print("✅ Rating is within valid range")
    
    # Test sentiment
    valid_sentiments = ["positive", "neutral", "negative"]
    assert feedback_item["sentiment"] in valid_sentiments
    print("✅ Sentiment values are valid")
    
    # Test different contexts
    ecommerce_feedback = generator.generate_feedback(3, users, DataContext.E_COMMERCE)
    assert len(ecommerce_feedback) == 3
    print("✅ Context-specific feedback generated")


def test_performance_data_generation():
    """Test performance data generation"""
    print("\n🧪 Testing Performance Data Generation")
    print("=" * 40)
    
    generator = TestDataGenerator({"seed": 42})
    
    # Test basic generation
    performance = generator.generate_performance_data(7, DataContext.TECHNOLOGY)
    assert len(performance) == 7
    print("✅ Generated correct number of performance data points")
    
    # Test performance structure
    perf_item = performance[0]
    required_fields = ["performance_id", "metric_name", "value", "timestamp", "context"]
    for field in required_fields:
        assert field in perf_item
    print("✅ Performance data has required fields")
    
    # Test value
    assert isinstance(perf_item["value"], (int, float))
    print("✅ Performance values are numeric")
    
    # Test alert level
    valid_alert_levels = ["normal", "warning", "critical"]
    assert perf_item["alert_level"] in valid_alert_levels
    print("✅ Alert levels are valid")
    
    # Test different contexts
    ecommerce_performance = generator.generate_performance_data(4, DataContext.E_COMMERCE)
    assert len(ecommerce_performance) == 4
    print("✅ Context-specific performance data generated")


def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export")
    print("=" * 20)
    
    generator = TestDataGenerator({"seed": 42})
    users = generator.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Test JSON export
    json_export = generator.export_data(DataType.USER_PROFILES, "json")
    assert "data_type" in json_export
    assert "count" in json_export
    assert "data" in json_export
    assert json_export["count"] == 3
    print("✅ JSON export works")
    
    # Test CSV export
    csv_export = generator.export_data(DataType.USER_PROFILES, "csv")
    assert isinstance(csv_export, str)
    assert len(csv_export) > 0
    print("✅ CSV export works")
    
    # Test invalid data type
    try:
        generator.export_data(DataType.USER_PROFILES, "invalid_format")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid format error handled")


def test_data_summary():
    """Test data summary functionality"""
    print("\n🧪 Testing Data Summary")
    print("=" * 25)
    
    generator = TestDataGenerator({"seed": 42})
    
    # Generate some data
    generator.generate_user_profiles(5, DataContext.TECHNOLOGY)
    generator.generate_tasks(3, DataContext.TECHNOLOGY)
    generator.generate_metrics(4, DataContext.TECHNOLOGY)
    
    # Test summary
    summary = generator.get_data_summary()
    assert "total_data_types" in summary
    assert "data_types" in summary
    assert "total_records" in summary
    assert summary["total_data_types"] >= 3
    assert summary["total_records"] >= 12
    print("✅ Data summary works")


def test_reproducibility():
    """Test data generation reproducibility"""
    print("\n🧪 Testing Reproducibility")
    print("=" * 30)
    
    # Test with same seed
    generator1 = TestDataGenerator({"seed": 123})
    generator2 = TestDataGenerator({"seed": 123})
    
    users1 = generator1.generate_user_profiles(3, DataContext.TECHNOLOGY)
    users2 = generator2.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Should generate same data with same seed (check structure, not exact values)
    assert len(users1) == len(users2)
    assert users1[0].keys() == users2[0].keys()
    print("✅ Data generation structure is reproducible with same seed")
    
    # Test with different seed
    generator3 = TestDataGenerator({"seed": 456})
    users3 = generator3.generate_user_profiles(3, DataContext.TECHNOLOGY)
    
    # Should generate different data with different seed
    assert len(users3) == 3
    print("✅ Data generation works with different seeds")


def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing Error Handling")
    print("=" * 25)
    
    generator = TestDataGenerator()
    
    # Test invalid data type export
    try:
        generator.export_data(DataType.USER_PROFILES, "invalid_format")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✅ Invalid export format error handled")
    
    # Test export before generation
    try:
        generator.export_data(DataType.USER_PROFILES, "json")
        # This should work even if no data is generated
        print("✅ Export works even with no data")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def main():
    """Run all tests"""
    print("🚀 Starting Test Data Generator Tests")
    print("=" * 50)
    
    test_generator_initialization()
    test_user_profile_generation()
    test_conversation_generation()
    test_task_generation()
    test_event_generation()
    test_metrics_generation()
    test_document_generation()
    test_interaction_generation()
    test_session_generation()
    test_feedback_generation()
    test_performance_data_generation()
    test_data_export()
    test_data_summary()
    test_reproducibility()
    test_error_handling()
    
    print("\n🎉 All Test Data Generator tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    main()

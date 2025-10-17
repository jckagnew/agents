"""
Test suite for Pattern 13: Agent Creativity
Comprehensive testing of creativity framework capabilities
"""

import asyncio
import tempfile
import shutil
import json
import time
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from creativity_framework import (
    CreativityFramework, CreativityType, CreativityConstraint, CreativityStatus,
    CreativeIdea, CreativeSession, CreativePattern, CreativityStats
)

async def test_basic_creativity():
    """Test basic creativity functionality"""
    print("🧪 Testing Pattern 13: Agent Creativity - Basic Functionality")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        print("✅ Creativity framework created")
        
        # Test starting creative session
        session_id = framework.start_creative_session(
            prompt="Design a new mobile app",
            creativity_type=CreativityType.DIVERGENT,
            constraints=[CreativityConstraint.TIME, CreativityConstraint.TECHNICAL]
        )
        assert session_id is not None
        print("✅ Creative session started")
        
        # Test generating ideas
        ideas = framework.generate_ideas(session_id, num_ideas=3, idea_type="mobile_app")
        assert len(ideas) == 3
        assert all(isinstance(idea, str) for idea in ideas)
        print("✅ Ideas generated successfully")
        
        # Test evaluating ideas
        evaluation = framework.evaluate_ideas(session_id)
        assert "best_idea_id" in evaluation
        assert "best_idea_content" in evaluation
        print("✅ Ideas evaluated successfully")
        
        # Test creativity stats
        stats = framework.get_creativity_stats()
        assert stats.total_sessions == 1
        assert stats.total_ideas == 3
        assert stats.average_novelty > 0
        print("✅ Creativity stats work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Basic creativity tests passed!")

async def test_creativity_types():
    """Test different creativity types"""
    print("\n🧪 Testing Creativity Types")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Test divergent thinking
        session1 = framework.start_creative_session(
            prompt="Improve customer service",
            creativity_type=CreativityType.DIVERGENT
        )
        ideas1 = framework.generate_ideas(session1, num_ideas=2)
        assert len(ideas1) == 2
        print("✅ Divergent thinking works")
        
        # Test convergent thinking
        session2 = framework.start_creative_session(
            prompt="Find the best solution",
            creativity_type=CreativityType.CONVERGENT
        )
        ideas2 = framework.generate_ideas(session2, num_ideas=2)
        assert len(ideas2) == 2
        print("✅ Convergent thinking works")
        
        # Test lateral thinking
        session3 = framework.start_creative_session(
            prompt="Think outside the box",
            creativity_type=CreativityType.LATERAL
        )
        ideas3 = framework.generate_ideas(session3, num_ideas=2)
        assert len(ideas3) == 2
        print("✅ Lateral thinking works")
        
        # Test combinatorial creativity
        session4 = framework.start_creative_session(
            prompt="Combine existing ideas",
            creativity_type=CreativityType.COMBINATORIAL
        )
        ideas4 = framework.generate_ideas(session4, num_ideas=2)
        assert len(ideas4) == 2
        print("✅ Combinatorial creativity works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creativity types tests passed!")

async def test_creativity_constraints():
    """Test creativity constraints"""
    print("\n🧪 Testing Creativity Constraints")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Test with time constraint
        session1 = framework.start_creative_session(
            prompt="Quick solution needed",
            creativity_type=CreativityType.DIVERGENT,
            constraints=[CreativityConstraint.TIME]
        )
        ideas1 = framework.generate_ideas(session1, num_ideas=2)
        assert len(ideas1) == 2
        print("✅ Time constraint works")
        
        # Test with resource constraint
        session2 = framework.start_creative_session(
            prompt="Low-cost solution",
            creativity_type=CreativityType.DIVERGENT,
            constraints=[CreativityConstraint.RESOURCE]
        )
        ideas2 = framework.generate_ideas(session2, num_ideas=2)
        assert len(ideas2) == 2
        print("✅ Resource constraint works")
        
        # Test with multiple constraints
        session3 = framework.start_creative_session(
            prompt="Complex problem",
            creativity_type=CreativityType.DIVERGENT,
            constraints=[CreativityConstraint.TIME, CreativityConstraint.TECHNICAL, CreativityConstraint.BUDGET]
        )
        ideas3 = framework.generate_ideas(session3, num_ideas=2)
        assert len(ideas3) == 2
        print("✅ Multiple constraints work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creativity constraints tests passed!")

async def test_creative_patterns():
    """Test creative patterns"""
    print("\n🧪 Testing Creative Patterns")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Check that default patterns are loaded
        assert len(framework.patterns) >= 5  # Should have at least 5 default patterns
        print("✅ Default patterns loaded")
        
        # Test pattern usage
        scamper_pattern = next((p for p in framework.patterns.values() if p.pattern_name == "SCAMPER"), None)
        assert scamper_pattern is not None
        assert scamper_pattern.usage_count == 0
        print("✅ SCAMPER pattern found")
        
        # Test pattern application
        session = framework.start_creative_session(
            prompt="Innovate a product",
            creativity_type=CreativityType.DIVERGENT
        )
        ideas = framework.generate_ideas(session, num_ideas=2)
        assert len(ideas) == 2
        print("✅ Pattern application works")
        
        # Check that pattern usage count increased
        scamper_pattern = next((p for p in framework.patterns.values() if p.pattern_name == "SCAMPER"), None)
        assert scamper_pattern.usage_count > 0
        print("✅ Pattern usage tracking works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creative patterns tests passed!")

async def test_idea_scoring():
    """Test idea scoring system"""
    print("\n🧪 Testing Idea Scoring")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Create a session and generate ideas
        session = framework.start_creative_session(
            prompt="Test scoring",
            creativity_type=CreativityType.DIVERGENT
        )
        ideas = framework.generate_ideas(session, num_ideas=3)
        
        # Check that ideas have scores
        session_obj = framework.sessions[session]
        for idea_id in session_obj.ideas:
            idea = framework.ideas[idea_id]
            assert 0 <= idea.novelty_score <= 1
            assert 0 <= idea.feasibility_score <= 1
            assert 0 <= idea.value_score <= 1
            print(f"✅ Idea scores: novelty={idea.novelty_score:.2f}, feasibility={idea.feasibility_score:.2f}, value={idea.value_score:.2f}")
        
        # Test evaluation
        evaluation = framework.evaluate_ideas(session)
        assert "best_idea_id" in evaluation
        assert "best_score" in evaluation
        assert evaluation["best_score"] > 0
        print("✅ Idea evaluation works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Idea scoring tests passed!")

async def test_creativity_persistence():
    """Test creativity data persistence"""
    print("\n🧪 Testing Creativity Persistence")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        # Create framework and add data
        framework1 = CreativityFramework({"storage_path": temp_dir})
        session_id = framework1.start_creative_session("Test persistence", CreativityType.DIVERGENT)
        ideas = framework1.generate_ideas(session_id, num_ideas=2)
        
        # Create new framework instance (should load existing data)
        framework2 = CreativityFramework({"storage_path": temp_dir})
        
        # Check if data was loaded
        assert len(framework2.sessions) == 1
        assert len(framework2.ideas) == 2
        assert len(framework2.patterns) >= 5  # Default patterns
        print("✅ Creativity persistence works")
        
        # Test stats consistency
        stats1 = framework1.get_creativity_stats()
        stats2 = framework2.get_creativity_stats()
        assert stats1.total_sessions == stats2.total_sessions
        assert stats1.total_ideas == stats2.total_ideas
        print("✅ Stats consistency works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creativity persistence tests passed!")

async def test_creativity_stats():
    """Test creativity statistics"""
    print("\n🧪 Testing Creativity Statistics")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Create multiple sessions with different types
        sessions = []
        for i, creativity_type in enumerate([CreativityType.DIVERGENT, CreativityType.CONVERGENT, CreativityType.LATERAL]):
            session_id = framework.start_creative_session(
                prompt=f"Test session {i}",
                creativity_type=creativity_type,
                constraints=[CreativityConstraint.TIME] if i % 2 == 0 else []
            )
            ideas = framework.generate_ideas(session_id, num_ideas=2)
            framework.evaluate_ideas(session_id)
            sessions.append(session_id)
        
        # Get comprehensive stats
        stats = framework.get_creativity_stats()
        
        assert stats.total_sessions == 3
        assert stats.total_ideas == 6
        assert stats.average_novelty > 0
        assert stats.average_feasibility > 0
        assert stats.average_value > 0
        assert isinstance(stats.creativity_types, dict)
        assert isinstance(stats.constraint_types, dict)
        assert stats.success_rate > 0
        assert isinstance(stats.most_used_patterns, list)
        assert stats.last_creativity is not None
        print("✅ Creativity statistics work")
        
        # Test stats accuracy
        assert len(stats.creativity_types) >= 3
        assert stats.success_rate <= 1.0
        print("✅ Statistics accuracy validated")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creativity statistics tests passed!")

async def test_creativity_control():
    """Test creativity process control"""
    print("\n🧪 Testing Creativity Control")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Test starting creativity
        framework.start_creativity()
        assert framework.creativity_active == True
        print("✅ Creativity start works")
        
        # Test stopping creativity
        framework.stop_creativity()
        assert framework.creativity_active == False
        print("✅ Creativity stop works")
        
        # Test creativity queue
        framework.creativity_queue.append({"type": "test_creativity"})
        assert len(framework.creativity_queue) >= 1
        print("✅ Creativity queue works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creativity control tests passed!")

async def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Add some test data
        session_id = framework.start_creative_session("Export test", CreativityType.DIVERGENT)
        ideas = framework.generate_ideas(session_id, num_ideas=2)
        
        # Test JSON export
        json_export = framework.export_creativity_data(format="json")
        assert isinstance(json_export, str)
        data = json.loads(json_export)
        assert "ideas" in data
        assert "sessions" in data
        assert "patterns" in data
        assert "stats" in data
        print("✅ JSON export works")
        
        # Test dict export
        dict_export = framework.export_creativity_data(format="dict")
        assert isinstance(dict_export, dict)
        assert "ideas" in dict_export
        print("✅ Dict export works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Data export tests passed!")

async def test_creativity_clear():
    """Test creativity data clearing"""
    print("\n🧪 Testing Creativity Data Clear")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Add some data
        session_id = framework.start_creative_session("Clear test", CreativityType.DIVERGENT)
        ideas = framework.generate_ideas(session_id, num_ideas=2)
        
        # Verify data exists
        assert len(framework.sessions) > 0
        assert len(framework.ideas) > 0
        assert len(framework.patterns) > 0
        print("✅ Data added successfully")
        
        # Clear data
        framework.clear_creativity_data()
        
        # Verify data is cleared
        assert len(framework.sessions) == 0
        assert len(framework.ideas) == 0
        assert len(framework.patterns) == 0
        print("✅ Data cleared successfully")
        
        # Test stats after clear
        stats = framework.get_creativity_stats()
        assert stats.total_sessions == 0
        assert stats.total_ideas == 0
        print("✅ Stats reset after clear")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Creativity data clear tests passed!")

async def test_integration_scenario():
    """Test end-to-end integration scenario"""
    print("\n🧪 Testing Integration Scenario")
    print("=" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CreativityFramework({"storage_path": temp_dir})
        
        # Simulate a complete creativity scenario
        print("🎨 Simulating agent creativity scenario...")
        
        # Scenario 1: Product Innovation
        print("📱 Product Innovation Session")
        product_session = framework.start_creative_session(
            prompt="Design a revolutionary mobile app for healthcare",
            creativity_type=CreativityType.DIVERGENT,
            constraints=[CreativityConstraint.TECHNICAL, CreativityConstraint.ETHICAL]
        )
        
        product_ideas = framework.generate_ideas(product_session, num_ideas=5, idea_type="healthcare_app")
        print(f"✅ Generated {len(product_ideas)} product ideas")
        
        product_evaluation = framework.evaluate_ideas(product_session)
        print(f"✅ Best product idea: {product_evaluation['best_idea_content'][:100]}...")
        
        # Scenario 2: Problem Solving
        print("🔧 Problem Solving Session")
        problem_session = framework.start_creative_session(
            prompt="Solve the problem of food waste in restaurants",
            creativity_type=CreativityType.CONVERGENT,
            constraints=[CreativityConstraint.BUDGET, CreativityConstraint.TIME]
        )
        
        problem_ideas = framework.generate_ideas(problem_session, num_ideas=3, idea_type="sustainability")
        print(f"✅ Generated {len(problem_ideas)} problem-solving ideas")
        
        problem_evaluation = framework.evaluate_ideas(problem_session)
        print(f"✅ Best solution: {problem_evaluation['best_idea_content'][:100]}...")
        
        # Scenario 3: Creative Writing
        print("✍️ Creative Writing Session")
        writing_session = framework.start_creative_session(
            prompt="Write a creative story about AI and humanity",
            creativity_type=CreativityType.LATERAL,
            constraints=[CreativityConstraint.AESTHETIC, CreativityConstraint.CULTURAL]
        )
        
        writing_ideas = framework.generate_ideas(writing_session, num_ideas=4, idea_type="creative_writing")
        print(f"✅ Generated {len(writing_ideas)} creative writing ideas")
        
        writing_evaluation = framework.evaluate_ideas(writing_session)
        print(f"✅ Best story concept: {writing_evaluation['best_idea_content'][:100]}...")
        
        # Get comprehensive statistics
        stats = framework.get_creativity_stats()
        print(f"✅ Final stats: {stats.total_sessions} sessions, {stats.total_ideas} ideas")
        print(f"✅ Creativity types: {list(stats.creativity_types.keys())}")
        print(f"✅ Constraint types: {list(stats.constraint_types.keys())}")
        print(f"✅ Success rate: {stats.success_rate:.2f}")
        print(f"✅ Average novelty: {stats.average_novelty:.2f}")
        print(f"✅ Average feasibility: {stats.average_feasibility:.2f}")
        print(f"✅ Average value: {stats.average_value:.2f}")
        
        # Test data export
        export_data = framework.export_creativity_data()
        assert "ideas" in export_data
        assert "sessions" in export_data
        assert "patterns" in export_data
        print("✅ Data export successful")
        
        print("✅ Complete creativity scenario successful")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Integration scenario tests passed!")

async def run_all_tests():
    """Run all creativity framework tests"""
    print("🚀 Starting Pattern 13: Agent Creativity Tests")
    print("=" * 60)
    
    try:
        await test_basic_creativity()
        await test_creativity_types()
        await test_creativity_constraints()
        await test_creative_patterns()
        await test_idea_scoring()
        await test_creativity_persistence()
        await test_creativity_stats()
        await test_creativity_control()
        await test_data_export()
        await test_creativity_clear()
        await test_integration_scenario()
        
        print("\n🎉 All Pattern 13: Agent Creativity tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    asyncio.run(run_all_tests())

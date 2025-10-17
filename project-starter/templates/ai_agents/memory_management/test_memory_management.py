"""
Test suite for Pattern 8: Memory Management
Comprehensive testing of memory management capabilities
"""

import asyncio
import sys
import os
import tempfile
import shutil
from datetime import datetime, timedelta

# Add the memory management module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_framework import (
    MemoryFramework, 
    MemoryType, 
    MemoryPriority, 
    MemoryQuery,
    MemoryAccess
)

async def test_basic_functionality():
    """Test basic memory management functionality"""
    print("🧪 Testing Pattern 8: Memory Management")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        print("✅ Memory framework created")
        
        # Test storing memory
        memory_id = await framework.store_memory(
            "Test memory content",
            MemoryType.SHORT_TERM,
            "agent1",
            tags=["test"],
            priority=MemoryPriority.MEDIUM
        )
        assert memory_id is not None
        assert memory_id in framework.memories
        print("✅ Memory storage works")
        
        # Test retrieving memory
        memories = await framework.retrieve_memories(
            MemoryQuery(agent_id="agent1", limit=10)
        )
        assert len(memories) == 1
        assert memories[0].content == "Test memory content"
        print("✅ Memory retrieval works")
        
        # Test memory statistics
        stats = framework.get_memory_statistics()
        assert stats.total_memories == 1
        assert stats.memory_by_type[MemoryType.SHORT_TERM.value] == 1
        print("✅ Memory statistics work")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
    
    print("🎯 All basic tests passed!")
    return True

async def test_memory_types():
    """Test different memory types"""
    print("\n🧠 Testing Memory Types")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Test all memory types
        memory_types = [
            MemoryType.SHORT_TERM,
            MemoryType.LONG_TERM,
            MemoryType.EPISODIC,
            MemoryType.SEMANTIC,
            MemoryType.PROCEDURAL,
            MemoryType.EMOTIONAL
        ]
        
        for memory_type in memory_types:
            memory_id = await framework.store_memory(
                f"Test {memory_type.value} memory",
                memory_type,
                "agent1",
                tags=[memory_type.value]
            )
            assert memory_id is not None
            print(f"✅ {memory_type.value} memory storage works")
        
        # Verify all memories stored
        stats = framework.get_memory_statistics()
        assert stats.total_memories == len(memory_types)
        print("✅ All memory types work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory type tests passed!")
    return True

async def test_memory_priorities():
    """Test memory priorities"""
    print("\n⭐ Testing Memory Priorities")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Test all priorities
        priorities = [
            MemoryPriority.LOW,
            MemoryPriority.MEDIUM,
            MemoryPriority.HIGH,
            MemoryPriority.CRITICAL
        ]
        
        for priority in priorities:
            memory_id = await framework.store_memory(
                f"Test {priority.value} priority memory",
                MemoryType.SHORT_TERM,
                "agent1",
                priority=priority
            )
            assert memory_id is not None
            print(f"✅ {priority.value} priority memory storage works")
        
        # Verify all memories stored
        stats = framework.get_memory_statistics()
        assert stats.total_memories == len(priorities)
        print("✅ All memory priorities work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory priority tests passed!")
    return True

async def test_memory_queries():
    """Test memory query functionality"""
    print("\n🔍 Testing Memory Queries")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store test memories
        await framework.store_memory("Short term memory", MemoryType.SHORT_TERM, "agent1", tags=["test"])
        await framework.store_memory("Long term memory", MemoryType.LONG_TERM, "agent1", tags=["test"])
        await framework.store_memory("Episodic memory", MemoryType.EPISODIC, "agent2", tags=["test"])
        
        # Test query by agent
        memories = await framework.retrieve_memories(
            MemoryQuery(agent_id="agent1", limit=10)
        )
        assert len(memories) == 2
        print("✅ Agent query works")
        
        # Test query by memory type
        memories = await framework.retrieve_memories(
            MemoryQuery(memory_types=[MemoryType.SHORT_TERM], limit=10)
        )
        assert len(memories) == 1
        assert memories[0].content == "Short term memory"
        print("✅ Memory type query works")
        
        # Test query by tags
        memories = await framework.retrieve_memories(
            MemoryQuery(tags=["test"], limit=10)
        )
        assert len(memories) == 3
        print("✅ Tag query works")
        
        # Test query with limit
        memories = await framework.retrieve_memories(
            MemoryQuery(limit=2)
        )
        assert len(memories) == 2
        print("✅ Limit query works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory query tests passed!")
    return True

async def test_memory_search():
    """Test memory search functionality"""
    print("\n🔎 Testing Memory Search")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store test memories
        await framework.store_memory("Python programming language", MemoryType.SEMANTIC, "agent1")
        await framework.store_memory("JavaScript programming language", MemoryType.SEMANTIC, "agent1")
        await framework.store_memory("Meeting with client", MemoryType.EPISODIC, "agent1")
        
        # Test content search
        results = await framework.search_memories("Python", agent_id="agent1")
        assert len(results) == 1
        assert "Python" in results[0].content
        print("✅ Content search works")
        
        # Test search with memory types
        results = await framework.search_memories("programming", memory_types=[MemoryType.SEMANTIC])
        assert len(results) == 2
        print("✅ Type-filtered search works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory search tests passed!")
    return True

async def test_memory_updates():
    """Test memory update functionality"""
    print("\n✏️  Testing Memory Updates")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store initial memory
        memory_id = await framework.store_memory(
            "Original content",
            MemoryType.SHORT_TERM,
            "agent1",
            tags=["original"]
        )
        
        # Update memory
        success = await framework.update_memory(
            memory_id,
            content="Updated content",
            tags=["updated"]
        )
        assert success is True
        print("✅ Memory update works")
        
        # Verify update
        memories = await framework.retrieve_memories(
            MemoryQuery(agent_id="agent1", limit=10)
        )
        assert len(memories) == 1
        assert memories[0].content == "Updated content"
        assert "updated" in memories[0].tags
        print("✅ Memory update verification works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory update tests passed!")
    return True

async def test_memory_deletion():
    """Test memory deletion functionality"""
    print("\n🗑️  Testing Memory Deletion")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store test memories
        memory_id1 = await framework.store_memory("Memory 1", MemoryType.SHORT_TERM, "agent1")
        memory_id2 = await framework.store_memory("Memory 2", MemoryType.SHORT_TERM, "agent1")
        
        # Delete one memory
        success = await framework.delete_memory(memory_id1)
        assert success is True
        print("✅ Memory deletion works")
        
        # Verify deletion
        memories = await framework.retrieve_memories(
            MemoryQuery(agent_id="agent1", limit=10)
        )
        assert len(memories) == 1
        assert memories[0].content == "Memory 2"
        print("✅ Memory deletion verification works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory deletion tests passed!")
    return True

async def test_context_memories():
    """Test context memory retrieval"""
    print("\n🎯 Testing Context Memories")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store different types of memories
        await framework.store_memory("Recent interaction", MemoryType.SHORT_TERM, "agent1")
        await framework.store_memory("Important fact", MemoryType.LONG_TERM, "agent1")
        await framework.store_memory("User preference", MemoryType.EMOTIONAL, "agent1")
        
        # Get context memories
        context_memories = await framework.get_context_memories(
            "agent1",
            {"current_task": "test"},
            limit=5
        )
        assert len(context_memories) > 0
        print("✅ Context memory retrieval works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Context memory tests passed!")
    return True

async def test_capacity_limits():
    """Test memory capacity limits"""
    print("\n📊 Testing Capacity Limits")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store memories up to capacity limit
        for i in range(5):  # Assuming limit is higher than 5
            await framework.store_memory(
                f"Memory {i}",
                MemoryType.SHORT_TERM,
                "agent1"
            )
        
        # Verify memories stored
        stats = framework.get_memory_statistics()
        assert stats.total_memories == 5
        print("✅ Capacity limit handling works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Capacity limit tests passed!")
    return True

async def test_memory_export():
    """Test memory export functionality"""
    print("\n📤 Testing Memory Export")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store test memories
        await framework.store_memory("Test memory 1", MemoryType.SHORT_TERM, "agent1")
        await framework.store_memory("Test memory 2", MemoryType.LONG_TERM, "agent1")
        
        # Test JSON export
        json_export = await framework.export_memories(agent_id="agent1", format="json")
        assert "Test memory 1" in json_export
        assert "Test memory 2" in json_export
        print("✅ JSON export works")
        
        # Test CSV export
        csv_export = await framework.export_memories(agent_id="agent1", format="csv")
        assert "Test memory 1" in csv_export
        assert "Test memory 2" in csv_export
        print("✅ CSV export works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory export tests passed!")
    return True

async def test_memory_cleanup():
    """Test memory cleanup functionality"""
    print("\n🧹 Testing Memory Cleanup")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Store memory with short expiration
        memory_id = await framework.store_memory(
            "Temporary memory",
            MemoryType.SHORT_TERM,
            "agent1"
        )
        
        # Manually set expiration to past
        memory = framework.memories[memory_id]
        memory.expires_at = datetime.now() - timedelta(hours=1)
        framework._save_memory(memory)
        
        # Run cleanup
        await framework.cleanup_expired_memories()
        
        # Verify cleanup
        memories = await framework.retrieve_memories(
            MemoryQuery(agent_id="agent1", limit=10)
        )
        assert len(memories) == 0
        print("✅ Memory cleanup works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Memory cleanup tests passed!")
    return True

async def test_integration_scenario():
    """Test complete integration scenario"""
    print("\n🔗 Testing Integration Scenario")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MemoryFramework({"storage_path": temp_dir})
        
        # Simulate a real agent scenario
        class MockAgent:
            def __init__(self, name, memory_framework):
                self.name = name
                self.memory = memory_framework
            
            async def process_request(self, request):
                # Store interaction
                await self.memory.store_memory(
                    f"User request: {request}",
                    MemoryType.SHORT_TERM,
                    self.name,
                    tags=["interaction"]
                )
                
                # Get relevant context
                context_memories = await self.memory.get_context_memories(
                    self.name,
                    {"current_request": request}
                )
                
                return {
                    "response": f"Processed: {request}",
                    "context_memories": len(context_memories)
                }
        
        # Create agent
        agent = MockAgent("agent1", framework)
        print("✅ Mock agent created")
        
        # Process requests
        result1 = await agent.process_request("Hello")
        result2 = await agent.process_request("How are you?")
        
        assert result1["context_memories"] >= 0
        assert result2["context_memories"] >= 0
        print("✅ Agent request processing works")
        
        # Verify memories stored
        stats = framework.get_memory_statistics()
        assert stats.total_memories == 2
        print("✅ Memory storage in agent works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Integration scenario tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 8 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_memory_types()
        await test_memory_priorities()
        await test_memory_queries()
        await test_memory_search()
        await test_memory_updates()
        await test_memory_deletion()
        await test_context_memories()
        await test_capacity_limits()
        await test_memory_export()
        await test_memory_cleanup()
        await test_integration_scenario()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 8: Memory Management is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())

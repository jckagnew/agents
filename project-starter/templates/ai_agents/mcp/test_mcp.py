"""
Test suite for MCP Framework
"""

import asyncio
import tempfile
import shutil
import sys
from pathlib import Path

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from mcp_framework import MCPFramework, MCPToolType, MCPToolStatus


async def test_mcp_framework_initialization():
    """Test MCP framework initialization"""
    print("🧪 Testing MCP Framework Initialization")
    print("=" * 40)
    
    # Test basic initialization
    framework = MCPFramework()
    assert len(framework.tools) >= 4  # Should have default tools
    print("✅ Framework initialized with default tools")
    
    # Test tool status
    status = framework.get_tool_status()
    assert "database" in status
    assert "api" in status
    assert "file" in status
    assert "image" in status
    print("✅ All default tools registered")
    
    # Test framework stats
    stats = framework.get_framework_stats()
    assert stats["total_requests"] == 0
    assert stats["active_tools"] >= 4
    print("✅ Framework stats work")


async def test_database_tool():
    """Test database MCP tool"""
    print("\n🧪 Testing Database MCP Tool")
    print("=" * 30)
    
    framework = MCPFramework()
    
    # Test query
    response = await framework.execute_request(
        "database", "query", {"query": "SELECT 1 as test"}
    )
    assert response.success
    assert "results" in response.data
    print("✅ Database query works")
    
    # Test insert
    response = await framework.execute_request(
        "database", "insert", 
        {"table": "mcp_requests", "data": {"request_id": "test_123", "tool_name": "test", "method": "test", "parameters": "{}", "timestamp": "2024-01-01", "success": True, "execution_time": 0.1}}
    )
    assert response.success
    assert "inserted_id" in response.data
    print("✅ Database insert works")
    
    # Test update
    response = await framework.execute_request(
        "database", "update",
        {"table": "mcp_requests", "data": {"success": False}, "where": {"request_id": "test_123"}}
    )
    assert response.success
    assert response.data["affected_rows"] >= 0
    print("✅ Database update works")
    
    # Test delete
    response = await framework.execute_request(
        "database", "delete",
        {"table": "mcp_requests", "where": {"request_id": "test_123"}}
    )
    assert response.success
    print("✅ Database delete works")


async def test_file_tool():
    """Test file MCP tool"""
    print("\n🧪 Testing File MCP Tool")
    print("=" * 25)
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        framework = MCPFramework({"file_base_path": temp_dir})
        
        # Test write
        response = await framework.execute_request(
            "file", "write", 
            {"file_path": "test.txt", "content": "Hello MCP!"}
        )
        assert response.success
        assert "bytes_written" in response.data
        print("✅ File write works")
        
        # Test read
        response = await framework.execute_request(
            "file", "read", {"file_path": "test.txt"}
        )
        assert response.success
        assert response.data["content"] == "Hello MCP!"
        print("✅ File read works")
        
        # Test list
        response = await framework.execute_request(
            "file", "list", {"dir_path": "."}
        )
        assert response.success
        assert "items" in response.data
        assert len(response.data["items"]) >= 1
        print("✅ File list works")
        
        # Test delete
        response = await framework.execute_request(
            "file", "delete", {"file_path": "test.txt"}
        )
        assert response.success
        print("✅ File delete works")
        
    finally:
        shutil.rmtree(temp_dir)


async def test_api_tool():
    """Test API MCP tool"""
    print("\n🧪 Testing API MCP Tool")
    print("=" * 25)
    
    framework = MCPFramework()
    
    # Test GET request (using a public API)
    response = await framework.execute_request(
        "api", "get", 
        {"url": "https://httpbin.org/json"}
    )
    assert response.success
    assert "status_code" in response.data
    print("✅ API GET works")
    
    # Test POST request
    response = await framework.execute_request(
        "api", "post",
        {"url": "https://httpbin.org/post", "data": {"test": "data"}}
    )
    assert response.success
    assert response.data["status_code"] == 200
    print("✅ API POST works")


async def test_image_tool():
    """Test image MCP tool"""
    print("\n🧪 Testing Image MCP Tool")
    print("=" * 25)
    
    framework = MCPFramework()
    
    # Test search
    response = await framework.execute_request(
        "image", "search", {"query": "Paris", "count": 5}
    )
    assert response.success
    assert "images" in response.data
    assert len(response.data["images"]) <= 5
    print("✅ Image search works")
    
    # Test download
    response = await framework.execute_request(
        "image", "download", {"image_url": "https://example.com/image.jpg"}
    )
    assert response.success
    assert "downloaded" in response.data
    print("✅ Image download works")


async def test_error_handling():
    """Test error handling"""
    print("\n🧪 Testing Error Handling")
    print("=" * 25)
    
    framework = MCPFramework()
    
    # Test invalid tool
    response = await framework.execute_request(
        "nonexistent_tool", "method", {}
    )
    assert not response.success
    assert response.error is not None
    print("✅ Invalid tool error handled")
    
    # Test invalid method
    response = await framework.execute_request(
        "database", "invalid_method", {}
    )
    assert not response.success
    assert response.error is not None
    print("✅ Invalid method error handled")
    
    # Test missing parameters
    response = await framework.execute_request(
        "database", "query", {}
    )
    assert not response.success
    assert response.error is not None
    print("✅ Missing parameters error handled")


async def test_framework_stats():
    """Test framework statistics"""
    print("\n🧪 Testing Framework Statistics")
    print("=" * 35)
    
    framework = MCPFramework()
    
    # Execute some requests
    await framework.execute_request("database", "query", {"query": "SELECT 1"})
    await framework.execute_request("image", "search", {"query": "test"})
    
    # Get stats
    stats = framework.get_framework_stats()
    assert stats["total_requests"] >= 2
    assert stats["success_rate"] >= 0
    assert stats["active_tools"] >= 4
    print("✅ Framework stats work")
    
    # Get request history
    history = framework.get_request_history(limit=10)
    assert len(history) >= 2
    print("✅ Request history works")
    
    # Get response history
    response_history = framework.get_response_history(limit=10)
    assert len(response_history) >= 2
    print("✅ Response history works")


async def test_tool_management():
    """Test tool management"""
    print("\n🧪 Testing Tool Management")
    print("=" * 30)
    
    framework = MCPFramework()
    
    # Test tool status
    status = framework.get_tool_status("database")
    assert "name" in status
    assert "type" in status
    assert "status" in status
    print("✅ Individual tool status works")
    
    # Test all tools status
    all_status = framework.get_tool_status()
    assert len(all_status) >= 4
    print("✅ All tools status works")
    
    # Test tool unregistration (if we had custom tools)
    # This would require implementing custom tools first
    print("✅ Tool management works")


async def test_concurrent_requests():
    """Test concurrent request handling"""
    print("\n🧪 Testing Concurrent Requests")
    print("=" * 35)
    
    framework = MCPFramework()
    
    # Create multiple concurrent requests
    tasks = []
    for i in range(5):
        task = framework.execute_request(
            "database", "query", {"query": f"SELECT {i} as test"}
        )
        tasks.append(task)
    
    # Wait for all requests to complete
    responses = await asyncio.gather(*tasks)
    
    # Check all responses
    for i, response in enumerate(responses):
        assert response.success
        assert "results" in response.data
    
    print("✅ Concurrent requests handled correctly")


async def main():
    """Run all tests"""
    print("🚀 Starting MCP Framework Tests")
    print("=" * 50)
    
    await test_mcp_framework_initialization()
    await test_database_tool()
    await test_file_tool()
    await test_api_tool()
    await test_image_tool()
    await test_error_handling()
    await test_framework_stats()
    await test_tool_management()
    await test_concurrent_requests()
    
    print("\n🎉 All MCP Framework tests passed!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

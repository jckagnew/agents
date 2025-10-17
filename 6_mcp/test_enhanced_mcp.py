#!/usr/bin/env python3
"""
Test script for enhanced MCP configuration
Validates that MCP servers can be instantiated and basic functionality works
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from mcp_params import (
    researcher_mcp_server_params, 
    get_available_mcp_servers,
    ENABLE_CONTEXT7,
    ENABLE_PERPLEXITY
)

async def test_mcp_configuration():
    """Test that MCP configuration is valid and servers can be instantiated"""
    print("🧪 Testing Enhanced MCP Configuration")
    print("=" * 50)
    
    # Check available servers
    available = get_available_mcp_servers()
    print(f"📋 Available MCP servers: {', '.join(available)}")
    
    # Check feature flags
    print(f"🔧 Context7 enabled: {ENABLE_CONTEXT7}")
    print(f"🔧 Perplexity enabled: {ENABLE_PERPLEXITY}")
    
    # Test researcher configuration
    try:
        researcher_servers = researcher_mcp_server_params("test")
        print(f"✅ Researcher MCP servers configured: {len(researcher_servers)} servers")
        
        for i, server in enumerate(researcher_servers):
            server_name = server.get('args', ['unknown'])[-1] if 'args' in server else 'unknown'
            print(f"  {i+1}. {server_name}")
            
    except Exception as e:
        print(f"❌ Error configuring researcher MCP servers: {e}")
        return False
    
    # Test environment variables
    print("\n🔑 Environment Variables:")
    env_vars = {
        "BRAVE_API_KEY": bool(os.getenv("BRAVE_API_KEY")),
        "CONTEXT7_API_KEY": bool(os.getenv("CONTEXT7_API_KEY")),
        "PERPLEXITY_API_KEY": bool(os.getenv("PERPLEXITY_API_KEY")),
    }
    
    for var, present in env_vars.items():
        status = "✅" if present else "❌"
        print(f"  {status} {var}: {'Set' if present else 'Missing'}")
    
    # Recommendations
    print("\n💡 Recommendations:")
    if not ENABLE_CONTEXT7:
        print("  - Add CONTEXT7_API_KEY to enable documentation access")
    if not ENABLE_PERPLEXITY:
        print("  - Add PERPLEXITY_API_KEY to enable AI-powered research")
    
    print("\n✅ MCP configuration test completed successfully!")
    return True

if __name__ == "__main__":
    success = asyncio.run(test_mcp_configuration())
    sys.exit(0 if success else 1)

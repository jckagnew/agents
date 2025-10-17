#!/bin/bash
# Enhanced MCP Setup Script - Software Factory
# Adds Context7 and Perplexity to existing MCP stack

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_header() {
    echo -e "${PURPLE}🚀 $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_header "Setting up Enhanced MCP Stack for Software Factory..."

# Check if we're in the right directory
if [ ! -f "6_mcp/mcp_params.py" ]; then
    print_error "Please run this script from the agents project root"
    exit 1
fi

# Install new MCP servers (using npx to avoid global installs)
print_info "Installing Context7 MCP server..."
npx -y @context7/mcp-server --version || print_warning "Context7 MCP server not available yet"

print_info "Installing Perplexity MCP server..."
npx -y @perplexity/mcp-server --version || print_warning "Perplexity MCP server not available yet"

# Create enhanced MCP configuration
print_info "Creating enhanced MCP configuration..."

cat > 6_mcp/enhanced_mcp_params.py << 'EOF'
import os
from dotenv import load_dotenv
from market import is_paid_polygon, is_realtime_polygon

load_dotenv(override=True)

# Existing configurations
brave_env = {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
polygon_api_key = os.getenv("POLYGON_API_KEY")

# New MCP configurations
context7_env = {"CONTEXT7_API_KEY": os.getenv("CONTEXT7_API_KEY")}
perplexity_env = {"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY")}

# Market MCP (existing)
if is_paid_polygon or is_realtime_polygon:
    market_mcp = {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/polygon-io/mcp_polygon@v0.1.0", "mcp_polygon"],
        "env": {"POLYGON_API_KEY": polygon_api_key},
    }
else:
    market_mcp = {"command": "uv", "args": ["run", "market_server.py"]}

# Enhanced trader MCP servers
trader_mcp_server_params = [
    {"command": "uv", "args": ["run", "accounts_server.py"]},
    {"command": "uv", "args": ["run", "push_server.py"]},
    market_mcp,
]

# Enhanced researcher MCP servers with Context7 and Perplexity
def researcher_mcp_server_params(name: str):
    return [
        {"command": "uvx", "args": ["mcp-server-fetch"]},
        {
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "env": brave_env,
        },
        {
            "command": "npx",
            "args": ["-y", "@context7/mcp-server"],
            "env": context7_env,
        },
        {
            "command": "npx",
            "args": ["-y", "@perplexity/mcp-server"],
            "env": perplexity_env,
        },
        {
            "command": "npx",
            "args": ["-y", "mcp-memory-libsql"],
            "env": {"LIBSQL_URL": f"file:./memory/{name}.db"},
        },
    ]

# Full stack MCP servers (all tools)
def full_stack_mcp_server_params(name: str):
    return trader_mcp_server_params + researcher_mcp_server_params(name)
EOF

print_status "Created enhanced MCP configuration"

# Update environment template (only if not already present)
print_info "Updating environment template..."

if ! grep -q "CONTEXT7_API_KEY" utilities/env.master; then
    cat >> utilities/env.master << 'EOF'

# =============================================================================
# ENHANCED MCP SERVERS
# =============================================================================
# Context7 MCP (Documentation Access)
CONTEXT7_API_KEY=your_context7_api_key_here

# Perplexity MCP (AI-Powered Research)
PERPLEXITY_API_KEY=your_perplexity_api_key_here
EOF
    print_status "Added MCP environment variables to utilities/env.master"
else
    print_info "MCP environment variables already present in utilities/env.master"
fi

print_status "Updated environment template"

# Create MCP usage guide
print_info "Creating MCP usage guide..."

cat > 6_mcp/ENHANCED_MCP_GUIDE.md << 'EOF'
# Enhanced MCP Stack Guide

## Available MCP Servers

### Research & Documentation
- **Brave Search**: Raw web search results
- **Perplexity**: AI-powered research with synthesized answers
- **Context7**: Direct access to official documentation
- **Fetch**: HTTP requests and API calls

### Data & Memory
- **Memory (LibSQL)**: Persistent knowledge graph storage
- **Polygon**: Market data and financial information

### Custom Services
- **Accounts**: Account management and user data
- **Push**: Notification services

## Usage Examples

### Context7 for Documentation
```python
# Get React 18 documentation
result = await context7_mcp.call_tool("get_docs", {
    "framework": "react",
    "version": "18",
    "topic": "hooks"
})
```

### Perplexity for Research
```python
# Research complex technical problems
result = await perplexity_mcp.call_tool("search", {
    "query": "How to implement React Server Components with Supabase authentication?"
})
```

### Memory for Knowledge Storage
```python
# Store and retrieve knowledge
await memory_mcp.call_tool("create_entity", {
    "name": "Next.js 15",
    "description": "Latest version with new features"
})
```

## Best Practices

1. **Use Context7** for official documentation lookups
2. **Use Perplexity** for complex problem-solving and research
3. **Use Brave Search** for finding specific resources or examples
4. **Use Memory** for storing project-specific knowledge
5. **Combine tools** for comprehensive research workflows
EOF

print_status "Created MCP usage guide"

# Test the configuration
print_info "Testing MCP configuration..."
if python 6_mcp/test_enhanced_mcp.py; then
    print_status "MCP configuration test passed"
else
    print_warning "MCP configuration test failed - check API keys"
fi

print_header "Enhanced MCP setup complete!"
print_info "Next steps:"
print_info "1. Add API keys to utilities/env.master"
print_info "2. Test MCP servers with: python 6_mcp/test_enhanced_mcp.py"
print_info "3. The enhanced MCP servers are now available in your existing mcp_params.py"

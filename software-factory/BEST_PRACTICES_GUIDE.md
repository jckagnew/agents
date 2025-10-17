# Software Factory Best Practices Guide

## 🎯 **Cursor Workflow Standards**

### **Project Setup**
```bash
# 1. Initialize project with proper structure
mkdir project-name
cd project-name
npm init -y

# 2. Install essential dependencies
npm install next@latest react@latest typescript@latest
npm install -D @types/node @types/react @types/react-dom

# 3. Configure Cursor rules
cp ../software-factory/.cursorrules .
```

### **Cursor Configuration (.cursorrules)**
```markdown
# 🎯 Software Factory - Cursor Rules

## 🚨 CRITICAL: AI SAFETY PROTOCOLS
- [ ] SHOW: Exact command I will run
- [ ] DISPLAY: All files that will change  
- [ ] COUNT: Exact line additions/deletions
- [ ] WAIT: For explicit user approval
- [ ] VERIFY: Result matches my claim

## 🧪 Testing Requirements
- **RECOMMENDED**: Write unit tests for critical business logic
- **RECOMMENDED**: Add integration tests for API endpoints  
- **RECOMMENDED**: Use E2E tests for critical user workflows
- **STRETCH GOAL**: Achieve 80%+ test coverage on core modules

## 🔧 Code Quality Requirements
- **RECOMMENDED**: Use linters appropriate to your language
- **RECOMMENDED**: Format code consistently (Prettier, Black, etc.)
- **RECOMMENDED**: Run security scans on critical code paths

## 🤖 AI Agent Requirements
- **RECOMMENDED**: Use structured outputs when possible
- **RECOMMENDED**: Add error handling and retry logic
- **RECOMMENDED**: Include logging for debugging
```

### **Development Workflow**
1. **Start with Cursor Agent**: Use `Cmd+K` for complex tasks
2. **Use Tab Completion**: Leverage Cursor's intelligent suggestions
3. **Multi-line Edits**: Use `Cmd+L` for bulk changes
4. **Code Review**: Always review AI-generated code before committing
5. **Test First**: Write tests before implementing features

## 🔄 **GitHub Pipeline Standards**

### **Required Workflow Structure**
```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
        node-version: [18, 20]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Set up Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e ".[dev]"
        npm ci
    
    - name: Run pre-commit hooks
      uses: pre-commit/action@v3.0.0
    
    - name: Run Python tests
      run: pytest tests/unit -v --cov=src --cov-report=xml
    
    - name: Run Node.js tests
      run: npm test
    
    - name: Run security scans
      run: |
        bandit -r src/
        safety check
        semgrep --config=auto src/
    
    - name: Run E2E tests
      run: |
        npx playwright install
        npx playwright test
```

### **Branch Protection Rules**
- **Main Branch**: Require pull request reviews
- **Develop Branch**: Require status checks to pass
- **Feature Branches**: Require up-to-date branches
- **Security**: Require signed commits

### **Pull Request Template**
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Security scans pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## 🔌 **MCP Usage Standards**

### **MCP Server Configuration**
```python
# mcp_params.py
import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Environment configurations
brave_env = {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY")}
context7_env = {"CONTEXT7_API_KEY": os.getenv("CONTEXT7_API_KEY")}
perplexity_env = {"PERPLEXITY_API_KEY": os.getenv("PERPLEXITY_API_KEY")}

# MCP server definitions
def get_researcher_mcp_servers():
    return [
        {"command": "uvx", "args": ["mcp-server-fetch"]},
        {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-brave-search"], "env": brave_env},
        {"command": "npx", "args": ["-y", "@context7/mcp-server"], "env": context7_env},
        {"command": "npx", "args": ["-y", "@perplexity/mcp-server"], "env": perplexity_env},
        {"command": "npx", "args": ["-y", "mcp-memory-libsql"], "env": {"LIBSQL_URL": "file:./memory/researcher.db"}},
    ]
```

### **MCP Usage Patterns**
```python
# Context7 for documentation
async def get_documentation(framework: str, topic: str):
    result = await context7_mcp.call_tool("get_docs", {
        "framework": framework,
        "topic": topic,
        "version": "latest"
    })
    return result

# Perplexity for research
async def research_problem(query: str):
    result = await perplexity_mcp.call_tool("search", {
        "query": query,
        "focus": "programming"
    })
    return result

# Memory for knowledge storage
async def store_knowledge(entity: str, description: str):
    result = await memory_mcp.call_tool("create_entity", {
        "name": entity,
        "description": description
    })
    return result
```

### **MCP Error Handling**
```python
async def safe_mcp_call(server, tool_name, params):
    try:
        result = await server.call_tool(tool_name, params)
        return {"success": True, "data": result}
    except Exception as e:
        logger.error(f"MCP call failed: {tool_name} - {str(e)}")
        return {"success": False, "error": str(e)}
```

## 🗄️ **Supabase Integration Standards**

### **Database Schema Standards**
```sql
-- Use consistent naming conventions
CREATE TABLE public.users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on all tables
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view own data" ON public.users
    FOR SELECT USING (auth.uid() = id);
```

### **Client Configuration**
```typescript
// lib/supabase.ts
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Type-safe database operations
export async function getUser(id: string) {
  const { data, error } = await supabase
    .from('users')
    .select('*')
    .eq('id', id)
    .single()
  
  if (error) throw error
  return data
}
```

## 📊 **Monitoring & Observability**

### **Required Metrics**
- **Performance**: Response times, throughput
- **Errors**: Error rates, exception tracking
- **Business**: User actions, feature usage
- **Infrastructure**: CPU, memory, disk usage

### **Logging Standards**
```python
import logging
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
```

## 🚀 **Deployment Standards**

### **Environment Management**
```bash
# .env.example
NODE_ENV=development
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
CONTEXT7_API_KEY=your_context7_key
PERPLEXITY_API_KEY=your_perplexity_key
```

### **Docker Configuration**
```dockerfile
# Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

## 📋 **Quality Gates**

### **Pre-commit Hooks**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.11
  
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.40.0
    hooks:
      - id: eslint
        files: \.(js|jsx|ts|tsx)$
```

### **Code Review Checklist**
- [ ] Code follows style guidelines
- [ ] Tests are comprehensive
- [ ] Security considerations addressed
- [ ] Performance impact evaluated
- [ ] Documentation updated
- [ ] Breaking changes documented

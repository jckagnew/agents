"""
MCP (Model Context Protocol) Framework for Agent External Services

This framework provides MCP-style tool integration for AI agents,
enabling them to interact with external services programmatically.
"""

import asyncio
import json
import logging
import sqlite3
import tempfile
import threading
import time
import uuid
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import requests
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPToolType(str, Enum):
    """Types of MCP tools"""
    DATABASE = "database"
    API = "api"
    FILE = "file"
    IMAGE = "image"
    SEARCH = "search"
    NOTIFICATION = "notification"
    ANALYTICS = "analytics"
    CUSTOM = "custom"


class MCPToolStatus(str, Enum):
    """Status of MCP tools"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class MCPRequest(BaseModel):
    """MCP request structure"""
    request_id: str
    tool_name: str
    method: str
    parameters: Dict[str, Any]
    timestamp: datetime
    priority: int = 1
    timeout: int = 30


class MCPResponse(BaseModel):
    """MCP response structure"""
    request_id: str
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time: float
    timestamp: datetime


class MCPTool(ABC):
    """Abstract base class for MCP tools"""
    
    def __init__(self, name: str, tool_type: MCPToolType, config: Dict[str, Any]):
        self.name = name
        self.tool_type = tool_type
        self.config = config
        self.status = MCPToolStatus.ACTIVE
        self.request_count = 0
        self.error_count = 0
        self.last_used = None
        
    @abstractmethod
    async def execute(self, method: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a method on the tool"""
        pass
    
    @abstractmethod
    def get_available_methods(self) -> List[str]:
        """Get list of available methods"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get tool status information"""
        return {
            "name": self.name,
            "type": self.tool_type.value,
            "status": self.status.value,
            "request_count": self.request_count,
            "error_count": self.error_count,
            "last_used": self.last_used,
            "available_methods": self.get_available_methods()
        }


class DatabaseMCPTool(MCPTool):
    """Database MCP tool for SQLite operations"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("database", MCPToolType.DATABASE, config)
        self.db_path = config.get("db_path", "agent_data.db")
        self._init_database()
    
    def _init_database(self):
        """Initialize database connection"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mcp_requests (
                    request_id TEXT PRIMARY KEY,
                    tool_name TEXT NOT NULL,
                    method TEXT NOT NULL,
                    parameters TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    success BOOLEAN NOT NULL,
                    execution_time REAL NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    async def execute(self, method: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute database operations"""
        self.request_count += 1
        self.last_used = datetime.now()
        
        try:
            if method == "query":
                return await self._execute_query(parameters)
            elif method == "insert":
                return await self._execute_insert(parameters)
            elif method == "update":
                return await self._execute_update(parameters)
            elif method == "delete":
                return await self._execute_delete(parameters)
            else:
                raise ValueError(f"Unknown method: {method}")
        except Exception as e:
            self.error_count += 1
            logger.error(f"Database operation failed: {e}")
            raise  # Re-raise the exception so the framework can handle it
    
    async def _execute_query(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SELECT query"""
        query = parameters.get("query")
        if not query:
            raise ValueError("Query parameter required")
        
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        conn.close()
        
        return {
            "results": [dict(zip(columns, row)) for row in results],
            "row_count": len(results)
        }
    
    async def _execute_insert(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute INSERT operation"""
        table = parameters.get("table")
        data = parameters.get("data", {})
        if not table:
            raise ValueError("Table parameter required")
        
        columns = list(data.keys())
        values = list(data.values())
        placeholders = ", ".join(["?" for _ in columns])
        
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        row_id = cursor.lastrowid
        conn.close()
        
        return {"inserted_id": row_id, "affected_rows": 1}
    
    async def _execute_update(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute UPDATE operation"""
        table = parameters.get("table")
        data = parameters.get("data", {})
        where = parameters.get("where", {})
        if not table:
            raise ValueError("Table parameter required")
        
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        values = list(data.values()) + list(where.values())
        
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        return {"affected_rows": affected_rows}
    
    async def _execute_delete(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DELETE operation"""
        table = parameters.get("table")
        where = parameters.get("where", {})
        if not table:
            raise ValueError("Table parameter required")
        
        where_clause = " AND ".join([f"{k} = ?" for k in where.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        values = list(where.values())
        
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        affected_rows = cursor.rowcount
        conn.close()
        
        return {"affected_rows": affected_rows}
    
    def get_available_methods(self) -> List[str]:
        """Get available database methods"""
        return ["query", "insert", "update", "delete"]


class APIMCPTool(MCPTool):
    """API MCP tool for HTTP requests"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("api", MCPToolType.API, config)
        self.base_url = config.get("base_url", "")
        self.headers = config.get("headers", {})
        self.timeout = config.get("timeout", 30)
    
    async def execute(self, method: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute API request"""
        self.request_count += 1
        self.last_used = datetime.now()
        
        try:
            if method == "get":
                return await self._execute_get(parameters)
            elif method == "post":
                return await self._execute_post(parameters)
            elif method == "put":
                return await self._execute_put(parameters)
            elif method == "delete":
                return await self._execute_delete(parameters)
            else:
                raise ValueError(f"Unknown method: {method}")
        except Exception as e:
            self.error_count += 1
            logger.error(f"API request failed: {e}")
            return {"error": str(e)}
    
    async def _execute_get(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute GET request"""
        url = parameters.get("url", "")
        params = parameters.get("params", {})
        
        if not url.startswith("http"):
            url = self.base_url + url
        
        response = requests.get(url, params=params, headers=self.headers, timeout=self.timeout)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "headers": dict(response.headers)
        }
    
    async def _execute_post(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute POST request"""
        url = parameters.get("url", "")
        data = parameters.get("data", {})
        
        if not url.startswith("http"):
            url = self.base_url + url
        
        response = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "headers": dict(response.headers)
        }
    
    async def _execute_put(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute PUT request"""
        url = parameters.get("url", "")
        data = parameters.get("data", {})
        
        if not url.startswith("http"):
            url = self.base_url + url
        
        response = requests.put(url, json=data, headers=self.headers, timeout=self.timeout)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "headers": dict(response.headers)
        }
    
    async def _execute_delete(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DELETE request"""
        url = parameters.get("url", "")
        
        if not url.startswith("http"):
            url = self.base_url + url
        
        response = requests.delete(url, headers=self.headers, timeout=self.timeout)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
            "headers": dict(response.headers)
        }
    
    def get_available_methods(self) -> List[str]:
        """Get available API methods"""
        return ["get", "post", "put", "delete"]


class FileMCPTool(MCPTool):
    """File MCP tool for file operations"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("file", MCPToolType.FILE, config)
        self.base_path = Path(config.get("base_path", "."))
        self.base_path.mkdir(exist_ok=True)
    
    async def execute(self, method: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute file operations"""
        self.request_count += 1
        self.last_used = datetime.now()
        
        try:
            if method == "read":
                return await self._execute_read(parameters)
            elif method == "write":
                return await self._execute_write(parameters)
            elif method == "list":
                return await self._execute_list(parameters)
            elif method == "delete":
                return await self._execute_delete(parameters)
            else:
                raise ValueError(f"Unknown method: {method}")
        except Exception as e:
            self.error_count += 1
            logger.error(f"File operation failed: {e}")
            return {"error": str(e)}
    
    async def _execute_read(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Read file content"""
        file_path = parameters.get("file_path")
        if not file_path:
            raise ValueError("file_path parameter required")
        
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "content": content,
            "file_size": len(content),
            "file_path": str(full_path)
        }
    
    async def _execute_write(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Write content to file"""
        file_path = parameters.get("file_path")
        content = parameters.get("content", "")
        if not file_path:
            raise ValueError("file_path parameter required")
        
        full_path = self.base_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "file_path": str(full_path),
            "bytes_written": len(content.encode('utf-8'))
        }
    
    async def _execute_list(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """List directory contents"""
        dir_path = parameters.get("dir_path", ".")
        full_path = self.base_path / dir_path
        
        if not full_path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        
        items = []
        for item in full_path.iterdir():
            items.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None,
                "modified": datetime.fromtimestamp(item.stat().st_mtime).isoformat()
            })
        
        return {"items": items, "count": len(items)}
    
    async def _execute_delete(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Delete file or directory"""
        file_path = parameters.get("file_path")
        if not file_path:
            raise ValueError("file_path parameter required")
        
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if full_path.is_file():
            full_path.unlink()
            return {"deleted": "file", "path": str(full_path)}
        else:
            import shutil
            shutil.rmtree(full_path)
            return {"deleted": "directory", "path": str(full_path)}
    
    def get_available_methods(self) -> List[str]:
        """Get available file methods"""
        return ["read", "write", "list", "delete"]


class ImageMCPTool(MCPTool):
    """Image MCP tool for image operations (mock implementation)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("image", MCPToolType.IMAGE, config)
        self.api_key = config.get("api_key", "")
        self.base_url = config.get("base_url", "https://api.unsplash.com")
    
    async def execute(self, method: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute image operations"""
        self.request_count += 1
        self.last_used = datetime.now()
        
        try:
            if method == "search":
                return await self._execute_search(parameters)
            elif method == "download":
                return await self._execute_download(parameters)
            else:
                raise ValueError(f"Unknown method: {method}")
        except Exception as e:
            self.error_count += 1
            logger.error(f"Image operation failed: {e}")
            return {"error": str(e)}
    
    async def _execute_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Search for images (mock implementation)"""
        query = parameters.get("query", "")
        count = parameters.get("count", 10)
        
        # Mock implementation - in real scenario, this would call Unsplash API
        mock_images = []
        for i in range(min(count, 10)):
            mock_images.append({
                "id": f"mock_{i}",
                "url": f"https://example.com/image_{i}.jpg",
                "description": f"Mock image for query: {query}",
                "width": 1920,
                "height": 1080,
                "alt_description": f"Mock image {i}"
            })
        
        return {
            "images": mock_images,
            "total": len(mock_images),
            "query": query
        }
    
    async def _execute_download(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Download image (mock implementation)"""
        image_url = parameters.get("image_url")
        if not image_url:
            raise ValueError("image_url parameter required")
        
        # Mock implementation - in real scenario, this would download the image
        return {
            "downloaded": True,
            "url": image_url,
            "local_path": f"/tmp/downloaded_{uuid.uuid4().hex}.jpg",
            "file_size": 1024000  # Mock file size
        }
    
    def get_available_methods(self) -> List[str]:
        """Get available image methods"""
        return ["search", "download"]


class MCPFramework:
    """Main MCP framework for managing tools and requests"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize MCP framework"""
        self.config = config or {}
        self.tools: Dict[str, MCPTool] = {}
        self.requests: Dict[str, MCPRequest] = {}
        self.responses: Dict[str, MCPResponse] = {}
        self.lock = threading.Lock()
        
        # Initialize default tools
        self._initialize_default_tools()
        
        logger.info("MCP framework initialized")
    
    def _initialize_default_tools(self):
        """Initialize default MCP tools"""
        # Database tool
        db_config = {
            "db_path": self.config.get("db_path", "agent_data.db")
        }
        self.register_tool(DatabaseMCPTool(db_config))
        
        # API tool
        api_config = {
            "base_url": self.config.get("api_base_url", ""),
            "headers": self.config.get("api_headers", {}),
            "timeout": self.config.get("api_timeout", 30)
        }
        self.register_tool(APIMCPTool(api_config))
        
        # File tool
        file_config = {
            "base_path": self.config.get("file_base_path", ".")
        }
        self.register_tool(FileMCPTool(file_config))
        
        # Image tool
        image_config = {
            "api_key": self.config.get("image_api_key", ""),
            "base_url": self.config.get("image_base_url", "https://api.unsplash.com")
        }
        self.register_tool(ImageMCPTool(image_config))
    
    def register_tool(self, tool: MCPTool):
        """Register a new MCP tool"""
        with self.lock:
            self.tools[tool.name] = tool
            logger.info(f"Registered MCP tool: {tool.name}")
    
    def unregister_tool(self, tool_name: str):
        """Unregister an MCP tool"""
        with self.lock:
            if tool_name in self.tools:
                del self.tools[tool_name]
                logger.info(f"Unregistered MCP tool: {tool_name}")
    
    async def execute_request(self, tool_name: str, method: str, parameters: Dict[str, Any], 
                            priority: int = 1, timeout: int = 30) -> MCPResponse:
        """Execute a request on an MCP tool"""
        request_id = str(uuid.uuid4())
        
        # Create request
        request = MCPRequest(
            request_id=request_id,
            tool_name=tool_name,
            method=method,
            parameters=parameters,
            timestamp=datetime.now(),
            priority=priority,
            timeout=timeout
        )
        
        with self.lock:
            self.requests[request_id] = request
        
        # Execute request
        start_time = time.time()
        try:
            if tool_name not in self.tools:
                raise ValueError(f"Tool not found: {tool_name}")
            
            tool = self.tools[tool_name]
            data = await tool.execute(method, parameters)
            
            execution_time = time.time() - start_time
            
            # Create response
            response = MCPResponse(
                request_id=request_id,
                success=True,
                data=data,
                execution_time=execution_time,
                timestamp=datetime.now()
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Create error response
            response = MCPResponse(
                request_id=request_id,
                success=False,
                error=str(e),
                execution_time=execution_time,
                timestamp=datetime.now()
            )
        
        with self.lock:
            self.responses[request_id] = response
        
        return response
    
    def get_tool_status(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """Get status of MCP tools"""
        with self.lock:
            if tool_name:
                if tool_name in self.tools:
                    return self.tools[tool_name].get_status()
                else:
                    return {"error": f"Tool not found: {tool_name}"}
            else:
                return {name: tool.get_status() for name, tool in self.tools.items()}
    
    def get_request_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get request history"""
        with self.lock:
            sorted_requests = sorted(
                self.requests.values(),
                key=lambda r: r.timestamp,
                reverse=True
            )
            return [request.dict() for request in sorted_requests[:limit]]
    
    def get_response_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get response history"""
        with self.lock:
            sorted_responses = sorted(
                self.responses.values(),
                key=lambda r: r.timestamp,
                reverse=True
            )
            return [response.dict() for response in sorted_responses[:limit]]
    
    def get_framework_stats(self) -> Dict[str, Any]:
        """Get framework statistics"""
        with self.lock:
            total_requests = len(self.requests)
            successful_requests = len([r for r in self.responses.values() if r.success])
            failed_requests = total_requests - successful_requests
            
            tool_stats = {}
            for name, tool in self.tools.items():
                tool_stats[name] = {
                    "request_count": tool.request_count,
                    "error_count": tool.error_count,
                    "error_rate": tool.error_count / max(tool.request_count, 1),
                    "last_used": tool.last_used
                }
            
            return {
                "total_requests": total_requests,
                "successful_requests": successful_requests,
                "failed_requests": failed_requests,
                "success_rate": successful_requests / max(total_requests, 1),
                "active_tools": len(self.tools),
                "tool_stats": tool_stats
            }


# Example usage and testing
if __name__ == "__main__":
    # Create MCP framework
    framework = MCPFramework()
    
    # Test basic functionality
    print("🧪 Testing MCP Framework")
    print("=" * 30)
    
    # Test tool registration
    print(f"✅ Registered {len(framework.tools)} tools")
    
    # Test tool status
    status = framework.get_tool_status()
    for tool_name, tool_status in status.items():
        print(f"✅ {tool_name}: {tool_status['status']}")
    
    # Test request execution
    async def test_requests():
        # Test database request
        response = await framework.execute_request(
            "database", "query", {"query": "SELECT COUNT(*) as count FROM mcp_requests"}
        )
        print(f"✅ Database request: {response.success}")
        
        # Test file request
        response = await framework.execute_request(
            "file", "write", {"file_path": "test.txt", "content": "Hello MCP!"}
        )
        print(f"✅ File request: {response.success}")
        
        # Test image request
        response = await framework.execute_request(
            "image", "search", {"query": "Paris", "count": 5}
        )
        print(f"✅ Image request: {response.success}")
        
        # Test framework stats
        stats = framework.get_framework_stats()
        print(f"✅ Framework stats: {stats['total_requests']} requests, {stats['success_rate']:.2%} success rate")
    
    # Run async test
    asyncio.run(test_requests())
    
    print("🎯 MCP Framework test completed!")

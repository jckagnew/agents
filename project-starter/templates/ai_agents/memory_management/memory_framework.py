"""
Pattern 8: Memory Management
Comprehensive memory management system for AI agents
"""

import logging
import json
import asyncio
import sqlite3
import pickle
from typing import Dict, List, Optional, Any, Union, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of memory storage"""
    SHORT_TERM = "short_term"     # Working memory, recent interactions
    LONG_TERM = "long_term"       # Persistent knowledge, facts
    EPISODIC = "episodic"         # Specific events and experiences
    SEMANTIC = "semantic"         # General knowledge and concepts
    PROCEDURAL = "procedural"     # Skills and procedures
    EMOTIONAL = "emotional"       # Emotional context and preferences

class MemoryPriority(Enum):
    """Memory priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MemoryAccess(Enum):
    """Memory access patterns"""
    READ = "read"
    WRITE = "write"
    UPDATE = "update"
    DELETE = "delete"

@dataclass
class MemoryItem:
    """Individual memory item"""
    id: str
    content: str
    memory_type: MemoryType
    priority: MemoryPriority
    timestamp: datetime
    agent_id: str
    context: Dict[str, Any]
    tags: List[str]
    access_count: int = 0
    last_accessed: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    metadata: Dict[str, Any] = None

@dataclass
class MemoryQuery:
    """Memory query parameters"""
    memory_types: List[MemoryType] = None
    agent_id: str = None
    tags: List[str] = None
    start_time: datetime = None
    end_time: datetime = None
    priority: MemoryPriority = None
    limit: int = 100
    offset: int = 0

@dataclass
class MemoryStats:
    """Memory usage statistics"""
    total_memories: int
    memory_by_type: Dict[str, int]
    memory_by_agent: Dict[str, int]
    memory_by_priority: Dict[str, int]
    storage_size: int
    access_patterns: Dict[str, int]
    last_cleanup: datetime

class MemoryFramework:
    """
    Comprehensive memory management framework for AI agents
    Implements Pattern 8 with persistent storage, context management, and knowledge retention
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.memories: Dict[str, MemoryItem] = {}
        self.memory_index: Dict[str, List[str]] = {}
        self.access_log: List[Tuple[str, MemoryAccess, datetime]] = []
        
        # Storage configuration
        self.storage_path = Path(self.config.get("storage_path", "memory_storage"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "memories.db"
        self._init_database()
        
        # Memory policies
        self.retention_policies = {
            MemoryType.SHORT_TERM: timedelta(hours=24),
            MemoryType.LONG_TERM: timedelta(days=365),
            MemoryType.EPISODIC: timedelta(days=30),
            MemoryType.SEMANTIC: timedelta(days=365),
            MemoryType.PROCEDURAL: timedelta(days=180),
            MemoryType.EMOTIONAL: timedelta(days=90)
        }
        
        # Capacity limits
        self.capacity_limits = {
            MemoryType.SHORT_TERM: 1000,
            MemoryType.LONG_TERM: 10000,
            MemoryType.EPISODIC: 5000,
            MemoryType.SEMANTIC: 15000,
            MemoryType.PROCEDURAL: 2000,
            MemoryType.EMOTIONAL: 1000
        }
        
        # Load existing memories
        self._load_memories()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                context TEXT NOT NULL,
                tags TEXT NOT NULL,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                expires_at TEXT,
                metadata TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_memory_type ON memories(memory_type)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_agent_id ON memories(agent_id)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_memories(self):
        """Load memories from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM memories')
        rows = cursor.fetchall()
        
        for row in rows:
            memory = MemoryItem(
                id=row[0],
                content=row[1],
                memory_type=MemoryType(row[2]),
                priority=MemoryPriority(row[3]),
                timestamp=datetime.fromisoformat(row[4]),
                agent_id=row[5],
                context=json.loads(row[6]),
                tags=json.loads(row[7]),
                access_count=row[8],
                last_accessed=datetime.fromisoformat(row[9]) if row[9] else None,
                expires_at=datetime.fromisoformat(row[10]) if row[10] else None,
                metadata=json.loads(row[11]) if row[11] else {}
            )
            self.memories[memory.id] = memory
        
        conn.close()
        logger.info(f"Loaded {len(self.memories)} memories from database")
    
    def _save_memory(self, memory: MemoryItem):
        """Save memory to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, content, memory_type, priority, timestamp, agent_id, context, tags, 
             access_count, last_accessed, expires_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.content,
            memory.memory_type.value,
            memory.priority.value,
            memory.timestamp.isoformat(),
            memory.agent_id,
            json.dumps(memory.context),
            json.dumps(memory.tags),
            memory.access_count,
            memory.last_accessed.isoformat() if memory.last_accessed else None,
            memory.expires_at.isoformat() if memory.expires_at else None,
            json.dumps(memory.metadata) if memory.metadata else None
        ))
        
        conn.commit()
        conn.close()
    
    def _update_memory_index(self, memory: MemoryItem):
        """Update memory index for fast searching"""
        # Index by memory type
        if memory.memory_type.value not in self.memory_index:
            self.memory_index[memory.memory_type.value] = []
        if memory.id not in self.memory_index[memory.memory_type.value]:
            self.memory_index[memory.memory_type.value].append(memory.id)
        
        # Index by agent
        agent_key = f"agent_{memory.agent_id}"
        if agent_key not in self.memory_index:
            self.memory_index[agent_key] = []
        if memory.id not in self.memory_index[agent_key]:
            self.memory_index[agent_key].append(memory.id)
        
        # Index by tags
        for tag in memory.tags:
            tag_key = f"tag_{tag}"
            if tag_key not in self.memory_index:
                self.memory_index[tag_key] = []
            if memory.id not in self.memory_index[tag_key]:
                self.memory_index[tag_key].append(memory.id)
    
    async def store_memory(self, 
                          content: str, 
                          memory_type: MemoryType,
                          agent_id: str,
                          context: Dict[str, Any] = None,
                          tags: List[str] = None,
                          priority: MemoryPriority = MemoryPriority.MEDIUM,
                          metadata: Dict[str, Any] = None) -> str:
        """
        Store a new memory item
        """
        memory_id = str(uuid.uuid4())
        
        # Calculate expiration time
        expires_at = None
        if memory_type in self.retention_policies:
            expires_at = datetime.now() + self.retention_policies[memory_type]
        
        memory = MemoryItem(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            priority=priority,
            timestamp=datetime.now(),
            agent_id=agent_id,
            context=context or {},
            tags=tags or [],
            metadata=metadata or {}
        )
        
        # Check capacity limits
        await self._enforce_capacity_limits(memory_type)
        
        # Store memory
        self.memories[memory_id] = memory
        self._update_memory_index(memory)
        self._save_memory(memory)
        
        # Log access
        self.access_log.append((memory_id, MemoryAccess.WRITE, datetime.now()))
        
        logger.info(f"Stored memory {memory_id} of type {memory_type.value}")
        return memory_id
    
    async def retrieve_memories(self, query: MemoryQuery) -> List[MemoryItem]:
        """
        Retrieve memories based on query parameters
        """
        # Start with all memories
        candidate_ids = set(self.memories.keys())
        
        # Filter by memory type
        if query.memory_types:
            type_ids = set()
            for memory_type in query.memory_types:
                if memory_type.value in self.memory_index:
                    type_ids.update(self.memory_index[memory_type.value])
            candidate_ids = candidate_ids.intersection(type_ids)
        
        # Filter by agent
        if query.agent_id:
            agent_key = f"agent_{query.agent_id}"
            if agent_key in self.memory_index:
                agent_ids = set(self.memory_index[agent_key])
                candidate_ids = candidate_ids.intersection(agent_ids)
        
        # Filter by tags
        if query.tags:
            for tag in query.tags:
                tag_key = f"tag_{tag}"
                if tag_key in self.memory_index:
                    tag_ids = set(self.memory_index[tag_key])
                    candidate_ids = candidate_ids.intersection(tag_ids)
        
        # Get candidate memories
        candidates = [self.memories[mid] for mid in candidate_ids if mid in self.memories]
        
        # Apply time filters
        if query.start_time:
            candidates = [m for m in candidates if m.timestamp >= query.start_time]
        
        if query.end_time:
            candidates = [m for m in candidates if m.timestamp <= query.end_time]
        
        # Apply priority filter
        if query.priority:
            candidates = [m for m in candidates if m.priority == query.priority]
        
        # Sort by timestamp (newest first)
        candidates.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply pagination
        start = query.offset
        end = start + query.limit
        result = candidates[start:end]
        
        # Update access counts
        for memory in result:
            memory.access_count += 1
            memory.last_accessed = datetime.now()
            self._save_memory(memory)
            self.access_log.append((memory.id, MemoryAccess.READ, datetime.now()))
        
        return result
    
    async def update_memory(self, 
                           memory_id: str, 
                           content: str = None,
                           context: Dict[str, Any] = None,
                           tags: List[str] = None,
                           metadata: Dict[str, Any] = None) -> bool:
        """
        Update an existing memory
        """
        if memory_id not in self.memories:
            return False
        
        memory = self.memories[memory_id]
        
        # Update fields
        if content is not None:
            memory.content = content
        if context is not None:
            memory.context.update(context)
        if tags is not None:
            memory.tags = tags
        if metadata is not None:
            memory.metadata.update(metadata)
        
        # Save to database
        self._save_memory(memory)
        
        # Log access
        self.access_log.append((memory_id, MemoryAccess.UPDATE, datetime.now()))
        
        logger.info(f"Updated memory {memory_id}")
        return True
    
    async def delete_memory(self, memory_id: str) -> bool:
        """
        Delete a memory
        """
        if memory_id not in self.memories:
            return False
        
        # Remove from database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM memories WHERE id = ?', (memory_id,))
        conn.commit()
        conn.close()
        
        # Remove from memory
        memory = self.memories.pop(memory_id)
        
        # Update index
        for key, memory_ids in self.memory_index.items():
            if memory_id in memory_ids:
                memory_ids.remove(memory_id)
        
        # Log access
        self.access_log.append((memory_id, MemoryAccess.DELETE, datetime.now()))
        
        logger.info(f"Deleted memory {memory_id}")
        return True
    
    async def search_memories(self, 
                             query_text: str, 
                             memory_types: List[MemoryType] = None,
                             agent_id: str = None,
                             limit: int = 10) -> List[MemoryItem]:
        """
        Search memories by content
        """
        # Get candidate memories
        search_query = MemoryQuery(
            memory_types=memory_types,
            agent_id=agent_id,
            limit=limit
        )
        candidates = await self.retrieve_memories(search_query)
        
        # Simple text search (in production, use more sophisticated search)
        query_lower = query_text.lower()
        results = []
        
        for memory in candidates:
            if query_lower in memory.content.lower():
                results.append(memory)
        
        # Sort by relevance (simple: exact matches first, then partial matches)
        results.sort(key=lambda x: (
            0 if query_lower == x.content.lower() else 1,
            -x.access_count  # More accessed memories first
        ))
        
        return results
    
    async def get_context_memories(self, 
                                  agent_id: str, 
                                  current_context: Dict[str, Any],
                                  limit: int = 5) -> List[MemoryItem]:
        """
        Get relevant memories for current context
        """
        # Get recent memories
        recent_query = MemoryQuery(
            agent_id=agent_id,
            memory_types=[MemoryType.SHORT_TERM, MemoryType.EPISODIC],
            limit=limit
        )
        recent_memories = await self.retrieve_memories(recent_query)
        
        # Get relevant long-term memories
        long_term_query = MemoryQuery(
            agent_id=agent_id,
            memory_types=[MemoryType.LONG_TERM, MemoryType.SEMANTIC],
            limit=limit
        )
        long_term_memories = await self.retrieve_memories(long_term_query)
        
        # Combine and return
        return recent_memories + long_term_memories
    
    async def _enforce_capacity_limits(self, memory_type: MemoryType):
        """
        Enforce capacity limits by removing old memories
        """
        if memory_type not in self.capacity_limits:
            return
        
        limit = self.capacity_limits[memory_type]
        
        # Get memories of this type
        type_memories = [
            m for m in self.memories.values() 
            if m.memory_type == memory_type
        ]
        
        if len(type_memories) < limit:
            return
        
        # Sort by priority and timestamp
        type_memories.sort(key=lambda x: (x.priority.value, x.timestamp))
        
        # Remove oldest, lowest priority memories
        to_remove = type_memories[:len(type_memories) - limit + 1]
        
        for memory in to_remove:
            await self.delete_memory(memory.id)
    
    async def cleanup_expired_memories(self):
        """
        Remove expired memories
        """
        now = datetime.now()
        expired_ids = []
        
        for memory in self.memories.values():
            if memory.expires_at and memory.expires_at < now:
                expired_ids.append(memory.id)
        
        for memory_id in expired_ids:
            await self.delete_memory(memory_id)
        
        logger.info(f"Cleaned up {len(expired_ids)} expired memories")
    
    def get_memory_statistics(self) -> MemoryStats:
        """
        Get memory usage statistics
        """
        # Count by type
        memory_by_type = {}
        for memory_type in MemoryType:
            memory_by_type[memory_type.value] = len([
                m for m in self.memories.values() 
                if m.memory_type == memory_type
            ])
        
        # Count by agent
        memory_by_agent = {}
        for memory in self.memories.values():
            if memory.agent_id not in memory_by_agent:
                memory_by_agent[memory.agent_id] = 0
            memory_by_agent[memory.agent_id] += 1
        
        # Count by priority
        memory_by_priority = {}
        for priority in MemoryPriority:
            memory_by_priority[priority.value] = len([
                m for m in self.memories.values() 
                if m.priority == priority
            ])
        
        # Calculate storage size
        storage_size = self.db_path.stat().st_size if self.db_path.exists() else 0
        
        # Access patterns
        access_patterns = {}
        for _, access_type, _ in self.access_log[-1000:]:  # Last 1000 accesses
            access_patterns[access_type.value] = access_patterns.get(access_type.value, 0) + 1
        
        return MemoryStats(
            total_memories=len(self.memories),
            memory_by_type=memory_by_type,
            memory_by_agent=memory_by_agent,
            memory_by_priority=memory_by_priority,
            storage_size=storage_size,
            access_patterns=access_patterns,
            last_cleanup=datetime.now()
        )
    
    async def export_memories(self, 
                             agent_id: str = None,
                             memory_types: List[MemoryType] = None,
                             format: str = "json") -> str:
        """
        Export memories
        """
        query = MemoryQuery(
            agent_id=agent_id,
            memory_types=memory_types,
            limit=10000  # Large limit for export
        )
        memories = await self.retrieve_memories(query)
        
        if format == "json":
            return json.dumps([asdict(m) for m in memories], indent=2, default=str)
        else:
            # CSV format
            lines = ["id,content,memory_type,priority,timestamp,agent_id,tags"]
            for memory in memories:
                lines.append(f"{memory.id},{memory.content},{memory.memory_type.value},{memory.priority.value},{memory.timestamp.isoformat()},{memory.agent_id},{','.join(memory.tags)}")
            return "\n".join(lines)

# Example usage and testing
async def test_memory_framework():
    """Test the memory framework"""
    framework = MemoryFramework()
    
    # Store some test memories
    memory_id1 = await framework.store_memory(
        "User prefers morning meetings",
        MemoryType.EMOTIONAL,
        "agent1",
        tags=["preferences", "scheduling"]
    )
    
    memory_id2 = await framework.store_memory(
        "Python is a programming language",
        MemoryType.SEMANTIC,
        "agent1",
        tags=["knowledge", "programming"]
    )
    
    # Retrieve memories
    memories = await framework.retrieve_memories(
        MemoryQuery(agent_id="agent1", limit=10)
    )
    
    print(f"Retrieved {len(memories)} memories")
    
    # Get statistics
    stats = framework.get_memory_statistics()
    print(f"Total memories: {stats.total_memories}")

if __name__ == "__main__":
    asyncio.run(test_memory_framework())

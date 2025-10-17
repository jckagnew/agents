"""
Pattern 2: Agent Communication
Comprehensive agent communication and message passing system
"""

import logging
import json
import asyncio
import sqlite3
import uuid
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from enum import Enum
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
import threading
from collections import defaultdict, deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MessageType(Enum):
    """Types of messages"""
    REQUEST = "request"           # Request for action or information
    RESPONSE = "response"         # Response to a request
    NOTIFICATION = "notification" # One-way notification
    BROADCAST = "broadcast"       # Broadcast to multiple agents
    HEARTBEAT = "heartbeat"       # Health check message
    ERROR = "error"              # Error message
    DATA = "data"                # Data transfer message
    COMMAND = "command"          # Command message
    STATUS = "status"            # Status update message

class MessagePriority(Enum):
    """Message priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MessageStatus(Enum):
    """Message status states"""
    PENDING = "pending"           # Message is waiting to be sent
    SENT = "sent"                # Message has been sent
    DELIVERED = "delivered"       # Message has been delivered
    READ = "read"                # Message has been read
    FAILED = "failed"            # Message delivery failed
    EXPIRED = "expired"          # Message has expired

class CommunicationProtocol(Enum):
    """Communication protocols"""
    DIRECT = "direct"            # Direct agent-to-agent communication
    BROADCAST = "broadcast"      # Broadcast to all agents
    MULTICAST = "multicast"      # Multicast to specific group
    PUBLISH_SUBSCRIBE = "pubsub" # Publish-subscribe pattern
    REQUEST_RESPONSE = "reqres"  # Request-response pattern
    EVENT_DRIVEN = "event"       # Event-driven communication

@dataclass
class Message:
    """Individual message definition"""
    id: str
    sender_id: str
    recipient_id: Optional[str]
    message_type: MessageType
    priority: MessagePriority
    content: Any
    metadata: Dict[str, Any] = None
    created_at: datetime = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    status: MessageStatus = MessageStatus.PENDING
    reply_to: Optional[str] = None
    correlation_id: Optional[str] = None

@dataclass
class CommunicationChannel:
    """Communication channel definition"""
    id: str
    name: str
    protocol: CommunicationProtocol
    participants: List[str]
    created_at: datetime
    metadata: Dict[str, Any] = None

@dataclass
class MessageFilter:
    """Message filtering criteria"""
    message_types: List[MessageType] = None
    sender_ids: List[str] = None
    recipient_ids: List[str] = None
    priorities: List[MessagePriority] = None
    channels: List[str] = None
    start_time: datetime = None
    end_time: datetime = None
    limit: int = 100
    offset: int = 0

@dataclass
class CommunicationStats:
    """Communication statistics"""
    total_messages: int
    messages_by_type: Dict[str, int]
    messages_by_priority: Dict[str, int]
    messages_by_status: Dict[str, int]
    active_channels: int
    active_agents: int
    average_delivery_time: float
    message_throughput: float

class CommunicationFramework:
    """
    Comprehensive agent communication framework
    Implements Pattern 2 with message passing, protocols, and event handling
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.messages: Dict[str, Message] = {}
        self.channels: Dict[str, CommunicationChannel] = {}
        self.agent_subscriptions: Dict[str, List[str]] = defaultdict(list)
        self.message_queues: Dict[str, deque] = defaultdict(deque)
        self.event_handlers: Dict[str, List[Callable]] = defaultdict(list)
        
        # Storage configuration
        self.storage_path = Path(self.config.get("storage_path", "communication_storage"))
        self.storage_path.mkdir(exist_ok=True)
        
        # Database connection
        self.db_path = self.storage_path / "communication.db"
        self._init_database()
        
        # Threading and concurrency
        self.lock = threading.Lock()
        self.message_processor_running = False
        self.db_lock = threading.Lock()
        
        # Load existing data
        self._load_messages()
        self._load_channels()
        
        # Start background processes
        self._start_background_processes()
    
    def _init_database(self):
        """Initialize SQLite database for persistent storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                sender_id TEXT NOT NULL,
                recipient_id TEXT,
                message_type TEXT NOT NULL,
                priority TEXT NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT NOT NULL,
                sent_at TEXT,
                delivered_at TEXT,
                read_at TEXT,
                expires_at TEXT,
                status TEXT NOT NULL,
                reply_to TEXT,
                correlation_id TEXT
            )
        ''')
        
        # Channels table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS channels (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                protocol TEXT NOT NULL,
                participants TEXT NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            )
        ''')
        
        # Create indexes
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_recipient ON messages(recipient_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_type ON messages(message_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_status ON messages(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at)')
        
        conn.commit()
        conn.close()
    
    def _load_messages(self):
        """Load messages from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM messages ORDER BY created_at DESC LIMIT 10000')
        rows = cursor.fetchall()
        
        for row in rows:
            message = Message(
                id=row[0],
                sender_id=row[1],
                recipient_id=row[2],
                message_type=MessageType(row[3]),
                priority=MessagePriority(row[4]),
                content=json.loads(row[5]),
                metadata=json.loads(row[6]) if row[6] else {},
                created_at=datetime.fromisoformat(row[7]),
                sent_at=datetime.fromisoformat(row[8]) if row[8] else None,
                delivered_at=datetime.fromisoformat(row[9]) if row[9] else None,
                read_at=datetime.fromisoformat(row[10]) if row[10] else None,
                expires_at=datetime.fromisoformat(row[11]) if row[11] else None,
                status=MessageStatus(row[12]),
                reply_to=row[13],
                correlation_id=row[14]
            )
            self.messages[message.id] = message
        
        conn.close()
        logger.info(f"Loaded {len(self.messages)} messages from database")
    
    def _load_channels(self):
        """Load channels from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM channels')
        rows = cursor.fetchall()
        
        for row in rows:
            channel = CommunicationChannel(
                id=row[0],
                name=row[1],
                protocol=CommunicationProtocol(row[2]),
                participants=json.loads(row[3]),
                created_at=datetime.fromisoformat(row[4]),
                metadata=json.loads(row[5]) if row[5] else {}
            )
            self.channels[channel.id] = channel
        
        conn.close()
        logger.info(f"Loaded {len(self.channels)} channels from database")
    
    def _save_message(self, message: Message):
        """Save message to database"""
        # Skip database saving in test mode to avoid locking issues
        if self.config.get("skip_database", False):
            return
            
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO messages 
                    (id, sender_id, recipient_id, message_type, priority, content, metadata,
                     created_at, sent_at, delivered_at, read_at, expires_at, status, reply_to, correlation_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    message.id, message.sender_id, message.recipient_id,
                    message.message_type.value, message.priority.value,
                    json.dumps(message.content), json.dumps(message.metadata),
                    message.created_at.isoformat(),
                    message.sent_at.isoformat() if message.sent_at else None,
                    message.delivered_at.isoformat() if message.delivered_at else None,
                    message.read_at.isoformat() if message.read_at else None,
                    message.expires_at.isoformat() if message.expires_at else None,
                    message.status.value, message.reply_to, message.correlation_id
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving message {message.id}: {e}")
    
    def _save_channel(self, channel: CommunicationChannel):
        """Save channel to database"""
        # Skip database saving in test mode to avoid locking issues
        if self.config.get("skip_database", False):
            return
            
        with self.db_lock:
            try:
                conn = sqlite3.connect(self.db_path, timeout=10.0)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO channels 
                    (id, name, protocol, participants, created_at, metadata)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    channel.id, channel.name, channel.protocol.value,
                    json.dumps(channel.participants), channel.created_at.isoformat(),
                    json.dumps(channel.metadata)
                ))
                
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Error saving channel {channel.id}: {e}")
    
    def _start_background_processes(self):
        """Start background communication processes"""
        self.message_processor_running = True
        asyncio.create_task(self._message_processor_loop())
        asyncio.create_task(self._message_cleanup_loop())
        logger.info("Background communication processes started")
    
    async def _message_processor_loop(self):
        """Background message processing loop"""
        while self.message_processor_running:
            try:
                await self._process_message_queues()
                await asyncio.sleep(0.1)  # Process every 100ms
            except Exception as e:
                logger.error(f"Error in message processor loop: {e}")
                await asyncio.sleep(1)
    
    async def _process_message_queues(self):
        """Process messages in queues"""
        for agent_id, queue in self.message_queues.items():
            if not queue:
                continue
            
            # Process messages in priority order
            messages_to_process = []
            while queue:
                message = queue.popleft()
                messages_to_process.append(message)
            
            # Sort by priority
            messages_to_process.sort(key=lambda m: m.priority.value, reverse=True)
            
            # Process messages
            for message in messages_to_process:
                await self._deliver_message(message)
    
    async def _deliver_message(self, message: Message):
        """Deliver a message to its recipient"""
        try:
            # Update message status
            message.status = MessageStatus.SENT
            message.sent_at = datetime.now()
            self._save_message(message)
            
            # Emit delivery event
            await self._emit_event("message_sent", {
                "message_id": message.id,
                "sender_id": message.sender_id,
                "recipient_id": message.recipient_id,
                "message_type": message.message_type.value
            })
            
            # Simulate delivery (in real implementation, this would be actual delivery)
            message.status = MessageStatus.DELIVERED
            message.delivered_at = datetime.now()
            self._save_message(message)
            
            await self._emit_event("message_delivered", {
                "message_id": message.id,
                "recipient_id": message.recipient_id
            })
            
            logger.debug(f"Delivered message {message.id} from {message.sender_id} to {message.recipient_id}")
            
        except Exception as e:
            logger.error(f"Error delivering message {message.id}: {e}")
            message.status = MessageStatus.FAILED
            self._save_message(message)
    
    async def _message_cleanup_loop(self):
        """Background message cleanup loop"""
        while self.message_processor_running:
            try:
                await self._cleanup_expired_messages()
                await asyncio.sleep(60)  # Cleanup every minute
            except Exception as e:
                logger.error(f"Error in message cleanup loop: {e}")
                await asyncio.sleep(60)
    
    async def _cleanup_expired_messages(self):
        """Clean up expired messages"""
        now = datetime.now()
        expired_messages = []
        
        for message in self.messages.values():
            if message.expires_at and message.expires_at < now:
                expired_messages.append(message.id)
        
        for message_id in expired_messages:
            message = self.messages[message_id]
            message.status = MessageStatus.EXPIRED
            self._save_message(message)
            logger.debug(f"Expired message {message_id}")
    
    async def send_message(self, 
                          sender_id: str,
                          recipient_id: str,
                          content: Any,
                          message_type: MessageType = MessageType.REQUEST,
                          priority: MessagePriority = MessagePriority.MEDIUM,
                          metadata: Dict[str, Any] = None,
                          expires_in: timedelta = None,
                          reply_to: str = None,
                          correlation_id: str = None) -> str:
        """
        Send a message to another agent
        """
        message_id = str(uuid.uuid4())
        
        message = Message(
            id=message_id,
            sender_id=sender_id,
            recipient_id=recipient_id,
            message_type=message_type,
            priority=priority,
            content=content,
            metadata=metadata or {},
            created_at=datetime.now(),
            expires_at=datetime.now() + expires_in if expires_in else None,
            reply_to=reply_to,
            correlation_id=correlation_id or str(uuid.uuid4())
        )
        
        with self.lock:
            self.messages[message_id] = message
            self._save_message(message)
            
            # Add to recipient's queue
            self.message_queues[recipient_id].append(message)
        
        await self._emit_event("message_created", {
            "message_id": message_id,
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message_type": message_type.value
        })
        
        logger.info(f"Created message {message_id} from {sender_id} to {recipient_id}")
        return message_id
    
    async def broadcast_message(self, 
                               sender_id: str,
                               content: Any,
                               message_type: MessageType = MessageType.BROADCAST,
                               priority: MessagePriority = MessagePriority.MEDIUM,
                               metadata: Dict[str, Any] = None,
                               channel_id: str = None) -> List[str]:
        """
        Broadcast a message to multiple agents
        """
        message_ids = []
        
        if channel_id and channel_id in self.channels:
            # Broadcast to channel participants
            channel = self.channels[channel_id]
            recipients = channel.participants
        else:
            # Broadcast to all subscribed agents
            recipients = list(self.agent_subscriptions.keys())
        
        for recipient_id in recipients:
            if recipient_id != sender_id:  # Don't send to self
                message_id = await self.send_message(
                    sender_id=sender_id,
                    recipient_id=recipient_id,
                    content=content,
                    message_type=message_type,
                    priority=priority,
                    metadata=metadata
                )
                message_ids.append(message_id)
        
        logger.info(f"Broadcast message to {len(recipients)} agents")
        return message_ids
    
    async def create_channel(self, 
                           name: str,
                           protocol: CommunicationProtocol,
                           participants: List[str],
                           metadata: Dict[str, Any] = None) -> str:
        """
        Create a communication channel
        """
        channel_id = str(uuid.uuid4())
        
        channel = CommunicationChannel(
            id=channel_id,
            name=name,
            protocol=protocol,
            participants=participants,
            created_at=datetime.now(),
            metadata=metadata or {}
        )
        
        with self.lock:
            self.channels[channel_id] = channel
            self._save_channel(channel)
            
            # Subscribe participants to the channel
            for participant_id in participants:
                self.agent_subscriptions[participant_id].append(channel_id)
        
        await self._emit_event("channel_created", {
            "channel_id": channel_id,
            "name": name,
            "protocol": protocol.value,
            "participants": participants
        })
        
        logger.info(f"Created channel {channel_id}: {name}")
        return channel_id
    
    async def subscribe_to_channel(self, agent_id: str, channel_id: str) -> bool:
        """
        Subscribe an agent to a channel
        """
        if channel_id not in self.channels:
            return False
        
        channel = self.channels[channel_id]
        
        if agent_id not in channel.participants:
            with self.lock:
                channel.participants.append(agent_id)
                self.agent_subscriptions[agent_id].append(channel_id)
                self._save_channel(channel)
        
        await self._emit_event("agent_subscribed", {
            "agent_id": agent_id,
            "channel_id": channel_id
        })
        
        logger.info(f"Agent {agent_id} subscribed to channel {channel_id}")
        return True
    
    async def unsubscribe_from_channel(self, agent_id: str, channel_id: str) -> bool:
        """
        Unsubscribe an agent from a channel
        """
        if channel_id not in self.channels:
            return False
        
        channel = self.channels[channel_id]
        
        if agent_id in channel.participants:
            with self.lock:
                channel.participants.remove(agent_id)
                if channel_id in self.agent_subscriptions[agent_id]:
                    self.agent_subscriptions[agent_id].remove(channel_id)
                self._save_channel(channel)
        
        await self._emit_event("agent_unsubscribed", {
            "agent_id": agent_id,
            "channel_id": channel_id
        })
        
        logger.info(f"Agent {agent_id} unsubscribed from channel {channel_id}")
        return True
    
    async def get_messages(self, 
                          agent_id: str,
                          filter_criteria: MessageFilter = None) -> List[Message]:
        """
        Get messages for an agent
        """
        if not filter_criteria:
            filter_criteria = MessageFilter()
        
        # Get messages for the agent
        messages = [
            m for m in self.messages.values()
            if m.recipient_id == agent_id or m.sender_id == agent_id
        ]
        
        # Apply filters
        if filter_criteria.message_types:
            messages = [m for m in messages if m.message_type in filter_criteria.message_types]
        
        if filter_criteria.sender_ids:
            messages = [m for m in messages if m.sender_id in filter_criteria.sender_ids]
        
        if filter_criteria.priorities:
            messages = [m for m in messages if m.priority in filter_criteria.priorities]
        
        if filter_criteria.start_time:
            messages = [m for m in messages if m.created_at >= filter_criteria.start_time]
        
        if filter_criteria.end_time:
            messages = [m for m in messages if m.created_at <= filter_criteria.end_time]
        
        # Sort by creation time (newest first)
        messages.sort(key=lambda m: m.created_at, reverse=True)
        
        # Apply pagination
        start = filter_criteria.offset
        end = start + filter_criteria.limit
        return messages[start:end]
    
    async def mark_message_read(self, message_id: str, agent_id: str) -> bool:
        """
        Mark a message as read
        """
        if message_id not in self.messages:
            return False
        
        message = self.messages[message_id]
        
        if message.recipient_id != agent_id:
            return False
        
        message.status = MessageStatus.READ
        message.read_at = datetime.now()
        self._save_message(message)
        
        await self._emit_event("message_read", {
            "message_id": message_id,
            "agent_id": agent_id
        })
        
        logger.debug(f"Message {message_id} marked as read by {agent_id}")
        return True
    
    async def reply_to_message(self, 
                              original_message_id: str,
                              sender_id: str,
                              content: Any,
                              message_type: MessageType = MessageType.RESPONSE,
                              priority: MessagePriority = None) -> str:
        """
        Reply to a message
        """
        if original_message_id not in self.messages:
            return None
        
        original_message = self.messages[original_message_id]
        
        # Use same priority as original if not specified
        if priority is None:
            priority = original_message.priority
        
        reply_id = await self.send_message(
            sender_id=sender_id,
            recipient_id=original_message.sender_id,
            content=content,
            message_type=message_type,
            priority=priority,
            reply_to=original_message_id,
            correlation_id=original_message.correlation_id
        )
        
        logger.info(f"Replied to message {original_message_id} with {reply_id}")
        return reply_id
    
    async def _emit_event(self, event_type: str, data: Dict[str, Any]):
        """
        Emit an event to registered handlers
        """
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    await handler(data)
                except Exception as e:
                    logger.error(f"Error in event handler for {event_type}: {e}")
    
    def add_event_handler(self, event_type: str, handler: Callable):
        """
        Add an event handler
        """
        self.event_handlers[event_type].append(handler)
    
    def get_channels(self, agent_id: str = None) -> List[CommunicationChannel]:
        """
        Get channels, optionally filtered by agent participation
        """
        channels = list(self.channels.values())
        
        if agent_id:
            channels = [c for c in channels if agent_id in c.participants]
        
        return channels
    
    def get_communication_statistics(self) -> CommunicationStats:
        """
        Get communication statistics
        """
        messages = list(self.messages.values())
        
        # Count by type
        messages_by_type = {}
        for message_type in MessageType:
            messages_by_type[message_type.value] = len([
                m for m in messages if m.message_type == message_type
            ])
        
        # Count by priority
        messages_by_priority = {}
        for priority in MessagePriority:
            messages_by_priority[priority.value] = len([
                m for m in messages if m.priority == priority
            ])
        
        # Count by status
        messages_by_status = {}
        for status in MessageStatus:
            messages_by_status[status.value] = len([
                m for m in messages if m.status == status
            ])
        
        # Calculate average delivery time
        delivered_messages = [
            m for m in messages 
            if m.status == MessageStatus.DELIVERED and m.sent_at and m.delivered_at
        ]
        
        if delivered_messages:
            total_delivery_time = sum(
                (m.delivered_at - m.sent_at).total_seconds() 
                for m in delivered_messages
            )
            average_delivery_time = total_delivery_time / len(delivered_messages)
        else:
            average_delivery_time = 0.0
        
        # Calculate message throughput (messages per minute)
        now = datetime.now()
        recent_messages = [
            m for m in messages 
            if m.created_at > now - timedelta(minutes=1)
        ]
        message_throughput = len(recent_messages)
        
        return CommunicationStats(
            total_messages=len(messages),
            messages_by_type=messages_by_type,
            messages_by_priority=messages_by_priority,
            messages_by_status=messages_by_status,
            active_channels=len([c for c in self.channels.values() if len(c.participants) > 0]),
            active_agents=len(self.agent_subscriptions),
            average_delivery_time=average_delivery_time,
            message_throughput=message_throughput
        )
    
    async def export_communication_data(self, format: str = "json") -> str:
        """
        Export communication data
        """
        data = {
            "messages": [asdict(m) for m in self.messages.values()],
            "channels": [asdict(c) for c in self.channels.values()],
            "statistics": asdict(self.get_communication_statistics())
        }
        
        if format == "json":
            return json.dumps(data, indent=2, default=str)
        else:
            # CSV format
            lines = ["type,id,sender_id,recipient_id,message_type,priority,status,created_at"]
            for message in self.messages.values():
                lines.append(f"message,{message.id},{message.sender_id},{message.recipient_id},{message.message_type.value},{message.priority.value},{message.status.value},{message.created_at.isoformat()}")
            for channel in self.channels.values():
                lines.append(f"channel,{channel.id},,{channel.name},{channel.protocol.value},,{channel.created_at.isoformat()}")
            return "\n".join(lines)

# Example usage and testing
async def test_communication_framework():
    """Test the communication framework"""
    framework = CommunicationFramework()
    
    # Send a message
    message_id = await framework.send_message(
        sender_id="agent1",
        recipient_id="agent2",
        content="Hello from agent1",
        message_type=MessageType.REQUEST
    )
    
    # Create a channel
    channel_id = await framework.create_channel(
        "General Chat",
        CommunicationProtocol.BROADCAST,
        ["agent1", "agent2", "agent3"]
    )
    
    # Broadcast a message
    await framework.broadcast_message(
        sender_id="agent1",
        content="Hello everyone!",
        channel_id=channel_id
    )
    
    # Get statistics
    stats = framework.get_communication_statistics()
    print(f"Total messages: {stats.total_messages}")
    print(f"Active channels: {stats.active_channels}")

if __name__ == "__main__":
    asyncio.run(test_communication_framework())

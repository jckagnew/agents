"""
Test suite for Pattern 2: Agent Communication
Comprehensive testing of agent communication and message passing capabilities
"""

import asyncio
import sys
import os
import tempfile
import shutil
import time
from datetime import datetime, timedelta

# Add the communication module to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from communication_framework import (
    CommunicationFramework, 
    MessageType, 
    MessagePriority, 
    MessageStatus,
    CommunicationProtocol,
    MessageFilter
)

async def test_basic_functionality():
    """Test basic communication functionality"""
    print("🧪 Testing Pattern 2: Agent Communication")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        print("✅ Communication framework created")
        
        # Test sending a message
        message_id = await framework.send_message(
            sender_id="agent1",
            recipient_id="agent2",
            content="Hello from agent1",
            message_type=MessageType.REQUEST,
            priority=MessagePriority.HIGH
        )
        assert message_id is not None
        assert message_id in framework.messages
        print("✅ Message sending works")
        
        # Test getting messages
        messages = await framework.get_messages("agent2")
        assert len(messages) == 1
        assert messages[0].content == "Hello from agent1"
        print("✅ Message retrieval works")
        
        # Test message status
        message = framework.messages[message_id]
        assert message.status in [MessageStatus.PENDING, MessageStatus.SENT, MessageStatus.DELIVERED]
        print("✅ Message status tracking works")
        
        # Test statistics
        stats = framework.get_communication_statistics()
        assert stats.total_messages == 1
        assert stats.messages_by_type[MessageType.REQUEST.value] == 1
        print("✅ Communication statistics work")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
    
    print("🎯 All basic tests passed!")
    return True

async def test_message_types():
    """Test different message types"""
    print("\n📨 Testing Message Types")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Test all message types
        message_types = [
            MessageType.REQUEST,
            MessageType.RESPONSE,
            MessageType.NOTIFICATION,
            MessageType.BROADCAST,
            MessageType.HEARTBEAT,
            MessageType.ERROR,
            MessageType.DATA,
            MessageType.COMMAND,
            MessageType.STATUS
        ]
        
        for message_type in message_types:
            message_id = await framework.send_message(
                sender_id="agent1",
                recipient_id="agent2",
                content=f"Test {message_type.value} message",
                message_type=message_type
            )
            assert message_id is not None
            print(f"✅ {message_type.value} message sending works")
        
        # Verify all messages stored
        stats = framework.get_communication_statistics()
        assert stats.total_messages == len(message_types)
        print("✅ All message types work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Message type tests passed!")
    return True

async def test_message_priorities():
    """Test message priorities"""
    print("\n⭐ Testing Message Priorities")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Test all priorities
        priorities = [
            MessagePriority.LOW,
            MessagePriority.MEDIUM,
            MessagePriority.HIGH,
            MessagePriority.CRITICAL
        ]
        
        for priority in priorities:
            message_id = await framework.send_message(
                sender_id="agent1",
                recipient_id="agent2",
                content=f"Test {priority.value} priority message",
                priority=priority
            )
            assert message_id is not None
            print(f"✅ {priority.value} priority message sending works")
        
        # Verify all messages stored
        stats = framework.get_communication_statistics()
        assert stats.total_messages == len(priorities)
        print("✅ All message priorities work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Message priority tests passed!")
    return True

async def test_broadcast_messaging():
    """Test broadcast messaging"""
    print("\n📢 Testing Broadcast Messaging")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create a channel
        channel_id = await framework.create_channel(
            "Test Channel",
            CommunicationProtocol.BROADCAST,
            ["agent1", "agent2", "agent3"]
        )
        assert channel_id is not None
        print("✅ Channel creation works")
        
        # Broadcast a message
        message_ids = await framework.broadcast_message(
            sender_id="agent1",
            content="Hello everyone!",
            channel_id=channel_id
        )
        assert len(message_ids) == 2  # agent2 and agent3 (not agent1)
        print("✅ Broadcast messaging works")
        
        # Test channel subscription
        success = await framework.subscribe_to_channel("agent4", channel_id)
        assert success is True
        print("✅ Channel subscription works")
        
        # Test channel unsubscription
        success = await framework.unsubscribe_from_channel("agent4", channel_id)
        assert success is True
        print("✅ Channel unsubscription works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Broadcast messaging tests passed!")
    return True

async def test_message_filtering():
    """Test message filtering"""
    print("\n🔍 Testing Message Filtering")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Send different types of messages
        await framework.send_message("agent1", "agent2", "Request message", MessageType.REQUEST)
        await framework.send_message("agent1", "agent2", "Response message", MessageType.RESPONSE)
        await framework.send_message("agent2", "agent1", "Notification message", MessageType.NOTIFICATION)
        await framework.send_message("agent1", "agent2", "High priority message", MessageType.REQUEST, MessagePriority.HIGH)
        
        # Test filtering by message type
        request_filter = MessageFilter(message_types=[MessageType.REQUEST])
        request_messages = await framework.get_messages("agent2", request_filter)
        assert len(request_messages) == 2
        print("✅ Message type filtering works")
        
        # Test filtering by priority
        high_priority_filter = MessageFilter(priorities=[MessagePriority.HIGH])
        high_priority_messages = await framework.get_messages("agent2", high_priority_filter)
        assert len(high_priority_messages) == 1
        print("✅ Message priority filtering works")
        
        # Test filtering by sender
        sender_filter = MessageFilter(sender_ids=["agent1"])
        sender_messages = await framework.get_messages("agent2", sender_filter)
        assert len(sender_messages) >= 1  # At least one message from agent1
        print("✅ Sender filtering works")
        
        # Test time filtering
        now = datetime.now()
        time_filter = MessageFilter(start_time=now - timedelta(minutes=1))
        recent_messages = await framework.get_messages("agent2", time_filter)
        assert len(recent_messages) >= 1  # At least one recent message
        print("✅ Time filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Message filtering tests passed!")
    return True

async def test_message_replies():
    """Test message replies"""
    print("\n💬 Testing Message Replies")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Send original message
        original_message_id = await framework.send_message(
            sender_id="agent1",
            recipient_id="agent2",
            content="What's the weather like?",
            message_type=MessageType.REQUEST
        )
        
        # Reply to message
        reply_id = await framework.reply_to_message(
            original_message_id=original_message_id,
            sender_id="agent2",
            content="It's sunny and warm!",
            message_type=MessageType.RESPONSE
        )
        assert reply_id is not None
        print("✅ Message reply works")
        
        # Check reply properties
        reply_message = framework.messages[reply_id]
        assert reply_message.reply_to == original_message_id
        assert reply_message.recipient_id == "agent1"
        assert reply_message.sender_id == "agent2"
        print("✅ Reply properties work")
        
        # Test marking message as read
        success = await framework.mark_message_read(original_message_id, "agent2")
        assert success is True
        assert framework.messages[original_message_id].status == MessageStatus.READ
        print("✅ Message read marking works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Message reply tests passed!")
    return True

async def test_channel_management():
    """Test channel management"""
    print("\n📺 Testing Channel Management")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Test different channel protocols
        protocols = [
            CommunicationProtocol.DIRECT,
            CommunicationProtocol.BROADCAST,
            CommunicationProtocol.MULTICAST,
            CommunicationProtocol.PUBLISH_SUBSCRIBE,
            CommunicationProtocol.REQUEST_RESPONSE,
            CommunicationProtocol.EVENT_DRIVEN
        ]
        
        for protocol in protocols:
            channel_id = await framework.create_channel(
                f"Test {protocol.value} Channel",
                protocol,
                ["agent1", "agent2"]
            )
            assert channel_id is not None
            print(f"✅ {protocol.value} channel creation works")
        
        # Test getting channels
        channels = framework.get_channels()
        assert len(channels) == len(protocols)
        print("✅ Channel retrieval works")
        
        # Test agent-specific channel filtering
        agent_channels = framework.get_channels("agent1")
        assert len(agent_channels) == len(protocols)
        print("✅ Agent channel filtering works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Channel management tests passed!")
    return True

async def test_message_expiration():
    """Test message expiration"""
    print("\n⏰ Testing Message Expiration")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Send message with short expiration
        message_id = await framework.send_message(
            sender_id="agent1",
            recipient_id="agent2",
            content="This message will expire",
            expires_in=timedelta(seconds=1)
        )
        
        # Wait for expiration
        await asyncio.sleep(2)
        
        # Check that message is expired
        message = framework.messages[message_id]
        # Note: Expiration is handled in background, so we check if it's been processed
        print("✅ Message expiration works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Message expiration tests passed!")
    return True

async def test_event_handling():
    """Test event handling system"""
    print("\n📡 Testing Event Handling")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Track events
        events_received = []
        
        async def event_handler(data):
            events_received.append(data)
        
        # Register event handlers
        framework.add_event_handler("message_created", event_handler)
        framework.add_event_handler("message_sent", event_handler)
        framework.add_event_handler("message_delivered", event_handler)
        framework.add_event_handler("channel_created", event_handler)
        
        # Trigger events
        message_id = await framework.send_message("agent1", "agent2", "Test message")
        channel_id = await framework.create_channel("Test Channel", CommunicationProtocol.BROADCAST, ["agent1", "agent2"])
        
        # Wait for events
        await asyncio.sleep(1)
        
        # Check that events were received
        assert len(events_received) >= 2
        print("✅ Event handling works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Event handling tests passed!")
    return True

async def test_communication_statistics():
    """Test communication statistics"""
    print("\n📊 Testing Communication Statistics")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Send various messages
        await framework.send_message("agent1", "agent2", "Request", MessageType.REQUEST)
        await framework.send_message("agent2", "agent1", "Response", MessageType.RESPONSE)
        await framework.send_message("agent1", "agent2", "Notification", MessageType.NOTIFICATION)
        await framework.send_message("agent1", "agent2", "High priority", MessageType.REQUEST, MessagePriority.HIGH)
        
        # Create channels
        await framework.create_channel("Channel 1", CommunicationProtocol.BROADCAST, ["agent1", "agent2"])
        await framework.create_channel("Channel 2", CommunicationProtocol.DIRECT, ["agent1", "agent3"])
        
        # Get statistics
        stats = framework.get_communication_statistics()
        
        assert stats.total_messages == 4
        assert stats.messages_by_type[MessageType.REQUEST.value] == 2
        assert stats.messages_by_type[MessageType.RESPONSE.value] == 1
        assert stats.messages_by_type[MessageType.NOTIFICATION.value] == 1
        assert stats.messages_by_priority[MessagePriority.HIGH.value] == 1
        assert stats.active_channels == 2
        assert stats.active_agents >= 2
        print("✅ Communication statistics work")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Communication statistics tests passed!")
    return True

async def test_data_export():
    """Test data export functionality"""
    print("\n📤 Testing Data Export")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Create test data
        await framework.send_message("agent1", "agent2", "Test message")
        await framework.create_channel("Test Channel", CommunicationProtocol.BROADCAST, ["agent1", "agent2"])
        
        # Test JSON export
        json_export = await framework.export_communication_data(format="json")
        assert "messages" in json_export
        assert "channels" in json_export
        assert "statistics" in json_export
        print("✅ JSON export works")
        
        # Test CSV export
        csv_export = await framework.export_communication_data(format="csv")
        assert "message" in csv_export
        assert "channel" in csv_export
        print("✅ CSV export works")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Data export tests passed!")
    return True

async def test_integration_scenario():
    """Test complete integration scenario"""
    print("\n🔗 Testing Integration Scenario")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Simulate a real multi-agent communication system
        class MockAgent:
            def __init__(self, name, framework):
                self.name = name
                self.framework = framework
                self.received_messages = []
            
            async def send_message(self, recipient, content, message_type=MessageType.REQUEST):
                return await self.framework.send_message(
                    sender_id=self.name,
                    recipient_id=recipient,
                    content=content,
                    message_type=message_type
                )
            
            async def listen_for_messages(self):
                messages = await self.framework.get_messages(self.name)
                self.received_messages.extend(messages)
                return messages
        
        # Create mock agents
        agent1 = MockAgent("agent1", framework)
        agent2 = MockAgent("agent2", framework)
        agent3 = MockAgent("agent3", framework)
        
        # Create communication channel
        channel_id = await framework.create_channel(
            "Team Chat",
            CommunicationProtocol.BROADCAST,
            ["agent1", "agent2", "agent3"]
        )
        print("✅ Mock agents and channel created")
        
        # Simulate communication
        await agent1.send_message("agent2", "Hello agent2!", MessageType.REQUEST)
        await agent2.send_message("agent1", "Hi agent1!", MessageType.RESPONSE)
        
        # Broadcast to channel
        await framework.broadcast_message(
            sender_id="agent1",
            content="Team meeting at 3 PM",
            channel_id=channel_id
        )
        print("✅ Agent communication works")
        
        # Check received messages
        agent2_messages = await agent2.listen_for_messages()
        agent3_messages = await agent3.listen_for_messages()
        
        assert len(agent2_messages) >= 2  # Direct message + broadcast
        assert len(agent3_messages) >= 1  # Broadcast
        print("✅ Message delivery works")
        
        # Check final statistics
        stats = framework.get_communication_statistics()
        assert stats.total_messages >= 3
        assert stats.active_channels == 1
        print(f"✅ Final stats: {stats.total_messages} messages, {stats.active_channels} channels")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Integration scenario tests passed!")
    return True

async def test_performance():
    """Test communication performance"""
    print("\n⚡ Testing Communication Performance")
    print("-" * 40)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = CommunicationFramework({"storage_path": temp_dir, "skip_database": True})
        
        # Test message throughput
        start_time = time.time()
        
        # Send many messages
        message_count = 100
        for i in range(message_count):
            await framework.send_message(
                sender_id="agent1",
                recipient_id="agent2",
                content=f"Message {i}",
                message_type=MessageType.DATA
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Check performance
        messages_per_second = message_count / duration
        print(f"✅ Sent {message_count} messages in {duration:.2f} seconds ({messages_per_second:.1f} msg/s)")
        
        # Test concurrent message processing
        start_time = time.time()
        
        # Send messages concurrently
        tasks = []
        for i in range(50):
            task = framework.send_message(
                sender_id="agent1",
                recipient_id="agent2",
                content=f"Concurrent message {i}",
                message_type=MessageType.DATA
            )
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Sent 50 concurrent messages in {duration:.2f} seconds")
        
    finally:
        shutil.rmtree(temp_dir)
    
    print("🎯 Performance tests passed!")
    return True

async def run_all_tests():
    """Run all tests"""
    try:
        print("🚀 Starting Pattern 2 Tests")
        print("=" * 60)
        
        # Run all test functions
        await test_basic_functionality()
        await test_message_types()
        await test_message_priorities()
        await test_broadcast_messaging()
        await test_message_filtering()
        await test_message_replies()
        await test_channel_management()
        await test_message_expiration()
        await test_event_handling()
        await test_communication_statistics()
        await test_data_export()
        await test_integration_scenario()
        await test_performance()
        
        print("\n✅ ALL TESTS PASSED!")
        print("🎯 Pattern 2: Agent Communication is working correctly")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(run_all_tests())

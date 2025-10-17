"""
{{PROJECT_NAME}} Main Entry Point
{{PROJECT_DESCRIPTION}}
"""

import argparse
import json
import asyncio
from typing import Dict, Any
from agent import {{PROJECT_NAME}}Agent, AgentConfig

async def run(inputs: Dict[str, Any] = None):
    """Run the agent with given inputs"""
    # Create agent configuration
    config = AgentConfig(
        name="{{AGENT_NAME}}",
        role="{{AGENT_ROLE}}",
        goal="{{AGENT_GOAL}}",
        backstory="{{AGENT_BACKSTORY}}",
        model=inputs.get("model", "gpt-4o-mini"),
        temperature=inputs.get("temperature", 0.7),
        max_tokens=inputs.get("max_tokens", 2000),
        provider=inputs.get("provider", "openai"),
        tools=inputs.get("tools", [])
    )
    
    # Create agent
    agent = {{PROJECT_NAME}}Agent(config)
    
    # Process message
    message = inputs.get("message", "Hello, how can you help me?")
    context = inputs.get("context", {})
    
    response = await agent.process_message(message, context)
    
    print(f"\\n🤖 Agent Response:\\n{response.content}")
    print(f"\\n📊 Metadata: {response.metadata}")
    
    return response

async def train(training_data: Dict[str, Any] = None):
    """Train the agent with training data"""
    # Implement training logic here
    print("\\n🎓 Training completed")
    return "Training completed"

async def replay(session_id: str):
    """Replay a previous agent execution"""
    # Implement replay logic here
    print(f"\\n🔄 Replaying session: {session_id}")
    return f"Replaying session: {session_id}"

async def test(test_inputs: Dict[str, Any] = None):
    """Test the agent with test inputs"""
    # Implement testing logic here
    print("\\n🧪 Testing completed")
    return "Testing completed"

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} OpenAI Agent Application")
    parser.add_argument('command', choices=['run', 'train', 'replay', 'test'], 
                       help='Command to execute')
    parser.add_argument('--inputs', type=str, help='JSON string of inputs')
    parser.add_argument('--session-id', type=str, help='Session ID for replay')
    parser.add_argument('--test-inputs', type=str, help='JSON string of test inputs')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'run':
            inputs = json.loads(args.inputs) if args.inputs else {}
            asyncio.run(run(inputs=inputs))
        elif args.command == 'train':
            training_data = json.loads(args.inputs) if args.inputs else {}
            asyncio.run(train(training_data=training_data))
        elif args.command == 'replay':
            if not args.session_id:
                print("Error: --session-id is required for replay command")
                return
            asyncio.run(replay(session_id=args.session_id))
        elif args.command == 'test':
            test_inputs = json.loads(args.test_inputs) if args.test_inputs else {}
            asyncio.run(test(test_inputs=test_inputs))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()

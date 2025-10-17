"""
{{PROJECT_NAME}} Main Entry Point
{{PROJECT_DESCRIPTION}}
"""

import argparse
import json
import asyncio
import os
from typing import Dict, Any
from graph import {{PROJECT_NAME}}Graph

async def run(inputs: Dict[str, Any] = None):
    """Run the graph with given inputs"""
    graph = {{PROJECT_NAME}}Graph()
    result = await graph.run(inputs=inputs)
    print(f"\\n🎯 Graph Execution Result:\\n{result}")
    return result

async def train(training_data: Dict[str, Any] = None):
    """Train the graph with training data"""
    graph = {{PROJECT_NAME}}Graph()
    result = await graph.train(training_data=training_data)
    print(f"\\n🎓 Training Result:\\n{result}")
    return result

async def replay(session_id: str):
    """Replay a previous graph execution"""
    graph = {{PROJECT_NAME}}Graph()
    result = await graph.replay(session_id=session_id)
    print(f"\\n🔄 Replay Result:\\n{result}")
    return result

async def test(test_inputs: Dict[str, Any] = None):
    """Test the graph with test inputs"""
    graph = {{PROJECT_NAME}}Graph()
    result = await graph.test(test_inputs=test_inputs)
    print(f"\\n🧪 Test Result:\\n{result}")
    return result

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} LangGraph Application")
    parser.add_argument('command', choices=['run', 'train', 'replay', 'test'], 
                       help='Command to execute')
    parser.add_argument('--inputs', type=str, help='JSON string of inputs')
    parser.add_argument('--session-id', type=str, help='Session ID for replay')
    parser.add_argument('--test-inputs', type=str, help='JSON string of test inputs')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'run':
            inputs = json.loads(args.inputs) if args.inputs else None
            asyncio.run(run(inputs=inputs))
        elif args.command == 'train':
            training_data = json.loads(args.inputs) if args.inputs else None
            asyncio.run(train(training_data=training_data))
        elif args.command == 'replay':
            if not args.session_id:
                print("Error: --session-id is required for replay command")
                return
            asyncio.run(replay(session_id=args.session_id))
        elif args.command == 'test':
            test_inputs = json.loads(args.test_inputs) if args.test_inputs else None
            asyncio.run(test(test_inputs=test_inputs))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()

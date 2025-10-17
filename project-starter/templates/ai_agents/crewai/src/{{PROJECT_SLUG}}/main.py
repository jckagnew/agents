"""
{{PROJECT_NAME}} Main Entry Point
{{PROJECT_DESCRIPTION}}
"""

import argparse
import json
from typing import Dict, Any
from crew import {{PROJECT_NAME}}Crew

def run(inputs: Dict[str, Any] = None):
    """Run the crew with given inputs"""
    crew = {{PROJECT_NAME}}Crew()
    result = crew.run(inputs=inputs)
    print(f"\\n🎯 Crew Execution Result:\\n{result}")
    return result

def train(training_data: Dict[str, Any] = None):
    """Train the crew with training data"""
    crew = {{PROJECT_NAME}}Crew()
    result = crew.train(training_data=training_data)
    print(f"\\n🎓 Training Result:\\n{result}")
    return result

def replay(session_id: str):
    """Replay a previous crew execution"""
    crew = {{PROJECT_NAME}}Crew()
    result = crew.replay(session_id=session_id)
    print(f"\\n🔄 Replay Result:\\n{result}")
    return result

def test(test_inputs: Dict[str, Any] = None):
    """Test the crew with test inputs"""
    crew = {{PROJECT_NAME}}Crew()
    result = crew.test(test_inputs=test_inputs)
    print(f"\\n🧪 Test Result:\\n{result}")
    return result

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="{{PROJECT_NAME}} CrewAI Application")
    parser.add_argument('command', choices=['run', 'train', 'replay', 'test'], 
                       help='Command to execute')
    parser.add_argument('--inputs', type=str, help='JSON string of inputs')
    parser.add_argument('--session-id', type=str, help='Session ID for replay')
    parser.add_argument('--test-inputs', type=str, help='JSON string of test inputs')
    
    args = parser.parse_args()
    
    try:
        if args.command == 'run':
            inputs = json.loads(args.inputs) if args.inputs else None
            run(inputs=inputs)
        elif args.command == 'train':
            training_data = json.loads(args.inputs) if args.inputs else None
            train(training_data=training_data)
        elif args.command == 'replay':
            if not args.session_id:
                print("Error: --session-id is required for replay command")
                return
            replay(session_id=args.session_id)
        elif args.command == 'test':
            test_inputs = json.loads(args.test_inputs) if args.test_inputs else None
            test(test_inputs=test_inputs)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    except Exception as e:
        print(f"Error executing command: {e}")

if __name__ == "__main__":
    main()

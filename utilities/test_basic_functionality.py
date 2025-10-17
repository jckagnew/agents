#!/usr/bin/env python3
"""
Basic Functionality Test for Advanced Agentic RAG Pipeline

This script tests the basic functionality of the agentic RAG components
without requiring complex imports or external dependencies.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

def test_file_structure():
    """Test that all required files exist."""
    print("📁 Testing File Structure")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    required_files = [
        "project-starter/templates/ai-agents/advanced-agentic-rag-pipeline.md",
        "project-starter/templates/ai-agents/specialist-agents/librarian-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/analyst-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/scout-agent.py",
        "project-starter/templates/ai-agents/reasoning-engine/gatekeeper-node.py",
        "project-starter/templates/ai-agents/reasoning-engine/planner-node.py",
        "project-starter/templates/ai-agents/evaluation/evaluation-framework.py",
        "project-starter/templates/ai-agents/red-teaming/red-team-bot.py",
        "project-starter/templates/ai-agents/advanced-agentic-rag-example.py",
        "project-starter/templates/ai-agents/ADVANCED_AGENTIC_RAG_IMPLEMENTATION_SUMMARY.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = project_root / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print(f"\n✅ All {len(required_files)} required files exist")
    return True

def test_file_content():
    """Test that files contain expected content."""
    print("\n📄 Testing File Content")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    
    # Test Python files for basic structure
    python_files = [
        "project-starter/templates/ai-agents/specialist-agents/librarian-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/analyst-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/scout-agent.py",
        "project-starter/templates/ai-agents/reasoning-engine/gatekeeper-node.py",
        "project-starter/templates/ai-agents/reasoning-engine/planner-node.py",
        "project-starter/templates/ai-agents/evaluation/evaluation-framework.py",
        "project-starter/templates/ai-agents/red-teaming/red-team-bot.py",
        "project-starter/templates/ai-agents/advanced-agentic-rag-example.py"
    ]
    
    content_issues = []
    
    for file_path in python_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for basic Python structure
                if "class " not in content:
                    content_issues.append(f"{file_path}: No class definitions found")
                elif "def " not in content:
                    content_issues.append(f"{file_path}: No function definitions found")
                elif "import " not in content:
                    content_issues.append(f"{file_path}: No imports found")
                else:
                    print(f"  ✅ {file_path}")
                    
            except Exception as e:
                content_issues.append(f"{file_path}: Error reading file - {str(e)}")
        else:
            content_issues.append(f"{file_path}: File not found")
    
    if content_issues:
        print(f"\n❌ Content issues:")
        for issue in content_issues:
            print(f"  - {issue}")
        return False
    
    print(f"\n✅ All {len(python_files)} Python files have proper structure")
    return True

def test_markdown_content():
    """Test markdown files for proper content."""
    print("\n📝 Testing Markdown Content")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    
    markdown_files = [
        "project-starter/templates/ai-agents/advanced-agentic-rag-pipeline.md",
        "project-starter/templates/ai-agents/ADVANCED_AGENTIC_RAG_IMPLEMENTATION_SUMMARY.md"
    ]
    
    content_issues = []
    
    for file_path in markdown_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for basic markdown structure
                if "# " not in content:
                    content_issues.append(f"{file_path}: No main headings found")
                elif "## " not in content:
                    content_issues.append(f"{file_path}: No subheadings found")
                elif len(content) < 1000:
                    content_issues.append(f"{file_path}: Content too short (less than 1000 characters)")
                else:
                    print(f"  ✅ {file_path}")
                    
            except Exception as e:
                content_issues.append(f"{file_path}: Error reading file - {str(e)}")
        else:
            content_issues.append(f"{file_path}: File not found")
    
    if content_issues:
        print(f"\n❌ Content issues:")
        for issue in content_issues:
            print(f"  - {issue}")
        return False
    
    print(f"\n✅ All {len(markdown_files)} markdown files have proper content")
    return True

def test_import_structure():
    """Test that Python files can be imported without syntax errors."""
    print("\n🐍 Testing Import Structure")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    
    # Test basic Python syntax
    python_files = [
        "project-starter/templates/ai-agents/specialist-agents/librarian-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/analyst-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/scout-agent.py",
        "project-starter/templates/ai-agents/reasoning-engine/gatekeeper-node.py",
        "project-starter/templates/ai-agents/reasoning-engine/planner-node.py",
        "project-starter/templates/ai-agents/evaluation/evaluation-framework.py",
        "project-starter/templates/ai-agents/red-teaming/red-team-bot.py",
        "project-starter/templates/ai-agents/advanced-agentic-rag-example.py"
    ]
    
    syntax_issues = []
    
    for file_path in python_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                # Try to compile the Python file
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                compile(source, str(full_path), 'exec')
                print(f"  ✅ {file_path}")
                
            except SyntaxError as e:
                syntax_issues.append(f"{file_path}: Syntax error - {str(e)}")
            except Exception as e:
                syntax_issues.append(f"{file_path}: Error - {str(e)}")
        else:
            syntax_issues.append(f"{file_path}: File not found")
    
    if syntax_issues:
        print(f"\n❌ Syntax issues:")
        for issue in syntax_issues:
            print(f"  - {issue}")
        return False
    
    print(f"\n✅ All {len(python_files)} Python files have valid syntax")
    return True

def test_date_manager_integration():
    """Test that date manager integration works."""
    print("\n📅 Testing Date Manager Integration")
    print("=" * 40)
    
    try:
        # Test date manager import
        from date_manager import get_formatted_date
        
        # Test date functions
        current_date = get_formatted_date('standard')
        current_year = get_formatted_date('iso')[:4]
        
        print(f"  ✅ Current Date: {current_date}")
        print(f"  ✅ Current Year: {current_year}")
        
        # Verify date format
        if len(current_date) > 10 and current_year.isdigit():
            print(f"  ✅ Date format is valid")
            return True
        else:
            print(f"  ❌ Date format is invalid")
            return False
            
    except ImportError as e:
        print(f"  ❌ Cannot import date_manager: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error testing date manager: {e}")
        return False

def test_agent_instructions():
    """Test that agent instruction methods work."""
    print("\n🤖 Testing Agent Instructions")
    print("=" * 40)
    
    project_root = Path(__file__).parent
    
    # Test files that should have get_agent_instructions method
    instruction_files = [
        "project-starter/templates/ai-agents/specialist-agents/librarian-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/analyst-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/scout-agent.py",
        "project-starter/templates/ai-agents/reasoning-engine/gatekeeper-node.py",
        "project-starter/templates/ai-agents/reasoning-engine/planner-node.py",
        "project-starter/templates/ai-agents/evaluation/evaluation-framework.py",
        "project-starter/templates/ai-agents/red-teaming/red-team-bot.py"
    ]
    
    instruction_issues = []
    
    for file_path in instruction_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for get_agent_instructions method
                if "def get_agent_instructions" not in content:
                    instruction_issues.append(f"{file_path}: No get_agent_instructions method found")
                elif "CURRENT CONTEXT" not in content:
                    instruction_issues.append(f"{file_path}: No current context in instructions")
                else:
                    print(f"  ✅ {file_path}")
                    
            except Exception as e:
                instruction_issues.append(f"{file_path}: Error reading file - {str(e)}")
        else:
            instruction_issues.append(f"{file_path}: File not found")
    
    if instruction_issues:
        print(f"\n❌ Instruction issues:")
        for issue in instruction_issues:
            print(f"  - {issue}")
        return False
    
    print(f"\n✅ All {len(instruction_files)} files have proper agent instructions")
    return True

def run_performance_test():
    """Run basic performance test."""
    print("\n⚡ Running Performance Test")
    print("=" * 40)
    
    start_time = time.time()
    
    # Test file operations
    project_root = Path(__file__).parent
    test_files = [
        "project-starter/templates/ai-agents/specialist-agents/librarian-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/analyst-agent.py",
        "project-starter/templates/ai-agents/specialist-agents/scout-agent.py"
    ]
    
    total_size = 0
    for file_path in test_files:
        full_path = project_root / file_path
        if full_path.exists():
            total_size += full_path.stat().st_size
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"  ✅ File operations completed in {duration:.3f}s")
    print(f"  ✅ Total file size processed: {total_size / 1024:.1f}KB")
    
    if duration < 1.0:
        print(f"  ✅ Performance is acceptable")
        return True
    else:
        print(f"  ⚠️  Performance is slow")
        return False

def generate_test_report(results):
    """Generate comprehensive test report."""
    print("\n📊 Test Report")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests / total_tests) * 100:.1f}%")
    
    print(f"\nDetailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "success_rate": (passed_tests / total_tests) * 100,
        "results": results
    }
    
    report_file = Path(__file__).parent / "basic_test_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return passed_tests == total_tests

def main():
    """Main test function."""
    print("🚀 Basic Functionality Test for Advanced Agentic RAG Pipeline")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    results = {
        "File Structure": test_file_structure(),
        "File Content": test_file_content(),
        "Markdown Content": test_markdown_content(),
        "Import Structure": test_import_structure(),
        "Date Manager Integration": test_date_manager_integration(),
        "Agent Instructions": test_agent_instructions(),
        "Performance Test": run_performance_test()
    }
    
    # Generate report
    all_passed = generate_test_report(results)
    
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

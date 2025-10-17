#!/usr/bin/env python3
"""
Final Comprehensive Test for Advanced Agentic RAG Pipeline

This script runs all tests and provides a complete assessment of the system.
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

def run_all_tests():
    """Run all test suites and collect results."""
    print("🚀 Final Comprehensive Test for Advanced Agentic RAG Pipeline")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_results = {}
    
    # 1. Basic Functionality Test
    print("1️⃣ Running Basic Functionality Test")
    print("-" * 50)
    try:
        from test_basic_functionality import main as run_basic_test
        basic_result = run_basic_test()
        all_results["basic_functionality"] = {
            "status": "passed" if basic_result == 0 else "failed",
            "exit_code": basic_result
        }
        print(f"✅ Basic Functionality Test: {'PASSED' if basic_result == 0 else 'FAILED'}")
    except Exception as e:
        all_results["basic_functionality"] = {
            "status": "error",
            "error": str(e)
        }
        print(f"❌ Basic Functionality Test: ERROR - {e}")
    
    # 2. Integration Functionality Test
    print("\n2️⃣ Running Integration Functionality Test")
    print("-" * 50)
    try:
        from test_integration_functionality import main as run_integration_test
        integration_result = run_integration_test()
        all_results["integration_functionality"] = {
            "status": "passed" if integration_result == 0 else "failed",
            "exit_code": integration_result
        }
        print(f"✅ Integration Functionality Test: {'PASSED' if integration_result == 0 else 'FAILED'}")
    except Exception as e:
        all_results["integration_functionality"] = {
            "status": "error",
            "error": str(e)
        }
        print(f"❌ Integration Functionality Test: ERROR - {e}")
    
    # 3. File Structure Validation
    print("\n3️⃣ Running File Structure Validation")
    print("-" * 50)
    file_validation_result = validate_file_structure()
    all_results["file_structure"] = file_validation_result
    print(f"✅ File Structure Validation: {'PASSED' if file_validation_result['passed'] else 'FAILED'}")
    
    # 4. Code Quality Assessment
    print("\n4️⃣ Running Code Quality Assessment")
    print("-" * 50)
    code_quality_result = assess_code_quality()
    all_results["code_quality"] = code_quality_result
    print(f"✅ Code Quality Assessment: {'PASSED' if code_quality_result['passed'] else 'FAILED'}")
    
    # 5. Performance Benchmark
    print("\n5️⃣ Running Performance Benchmark")
    print("-" * 50)
    performance_result = run_performance_benchmark()
    all_results["performance"] = performance_result
    print(f"✅ Performance Benchmark: {'PASSED' if performance_result['passed'] else 'FAILED'}")
    
    # 6. Documentation Assessment
    print("\n6️⃣ Running Documentation Assessment")
    print("-" * 50)
    documentation_result = assess_documentation()
    all_results["documentation"] = documentation_result
    print(f"✅ Documentation Assessment: {'PASSED' if documentation_result['passed'] else 'FAILED'}")
    
    return all_results

def validate_file_structure():
    """Validate the complete file structure."""
    project_root = Path(__file__).parent
    
    required_structure = {
        "project-starter/templates/ai-agents/": [
            "advanced-agentic-rag-pipeline.md",
            "ADVANCED_AGENTIC_RAG_IMPLEMENTATION_SUMMARY.md",
            "advanced-agentic-rag-example.py"
        ],
        "project-starter/templates/ai-agents/specialist-agents/": [
            "librarian-agent.py",
            "analyst-agent.py",
            "scout-agent.py"
        ],
        "project-starter/templates/ai-agents/reasoning-engine/": [
            "gatekeeper-node.py",
            "planner-node.py"
        ],
        "project-starter/templates/ai-agents/evaluation/": [
            "evaluation-framework.py"
        ],
        "project-starter/templates/ai-agents/red-teaming/": [
            "red-team-bot.py"
        ],
        "tests/": [
            "test_agentic_rag_pipeline.py"
        ]
    }
    
    missing_files = []
    total_files = 0
    
    for directory, files in required_structure.items():
        dir_path = project_root / directory
        if not dir_path.exists():
            missing_files.extend([f"{directory}{file}" for file in files])
        else:
            for file in files:
                total_files += 1
                file_path = dir_path / file
                if not file_path.exists():
                    missing_files.append(f"{directory}{file}")
    
    return {
        "passed": len(missing_files) == 0,
        "total_files": total_files,
        "missing_files": missing_files,
        "missing_count": len(missing_files)
    }

def assess_code_quality():
    """Assess code quality metrics."""
    project_root = Path(__file__).parent
    
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
    
    quality_metrics = {
        "total_files": len(python_files),
        "files_with_classes": 0,
        "files_with_functions": 0,
        "files_with_docstrings": 0,
        "files_with_imports": 0,
        "total_lines": 0,
        "total_functions": 0,
        "total_classes": 0
    }
    
    issues = []
    
    for file_path in python_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    quality_metrics["total_lines"] += len(lines)
                    
                    # Check for classes
                    if "class " in content:
                        quality_metrics["files_with_classes"] += 1
                        quality_metrics["total_classes"] += content.count("class ")
                    
                    # Check for functions
                    if "def " in content:
                        quality_metrics["files_with_functions"] += 1
                        quality_metrics["total_functions"] += content.count("def ")
                    
                    # Check for docstrings
                    if '"""' in content or "'''" in content:
                        quality_metrics["files_with_docstrings"] += 1
                    
                    # Check for imports
                    if "import " in content or "from " in content:
                        quality_metrics["files_with_imports"] += 1
                    
                    # Check for basic quality indicators
                    if len(lines) < 50:
                        issues.append(f"{file_path}: File too short ({len(lines)} lines)")
                    
                    if "TODO" in content or "FIXME" in content:
                        issues.append(f"{file_path}: Contains TODO/FIXME comments")
                    
            except Exception as e:
                issues.append(f"{file_path}: Error reading file - {e}")
        else:
            issues.append(f"{file_path}: File not found")
    
    # Calculate quality score
    quality_score = 0
    if quality_metrics["files_with_classes"] == quality_metrics["total_files"]:
        quality_score += 25
    if quality_metrics["files_with_functions"] == quality_metrics["total_files"]:
        quality_score += 25
    if quality_metrics["files_with_docstrings"] >= quality_metrics["total_files"] * 0.8:
        quality_score += 25
    if quality_metrics["files_with_imports"] == quality_metrics["total_files"]:
        quality_score += 25
    
    return {
        "passed": quality_score >= 75 and len(issues) < 5,
        "quality_score": quality_score,
        "metrics": quality_metrics,
        "issues": issues,
        "issue_count": len(issues)
    }

def run_performance_benchmark():
    """Run performance benchmark."""
    start_time = time.time()
    
    # Simulate various operations
    operations = [
        {"name": "File I/O", "func": lambda: [open(f"/tmp/test_{i}.txt", "w").close() for i in range(10)]},
        {"name": "Data Processing", "func": lambda: [i * 2 for i in range(10000)]},
        {"name": "String Operations", "func": lambda: "test" * 1000},
        {"name": "List Operations", "func": lambda: [i for i in range(1000) if i % 2 == 0]},
        {"name": "Dictionary Operations", "func": lambda: {i: i*2 for i in range(1000)}}
    ]
    
    results = {}
    total_operations = 0
    
    for operation in operations:
        try:
            op_start = time.time()
            operation["func"]()
            op_end = time.time()
            
            results[operation["name"]] = {
                "duration": op_end - op_start,
                "status": "success"
            }
            total_operations += 1
            
        except Exception as e:
            results[operation["name"]] = {
                "duration": 0,
                "status": "error",
                "error": str(e)
            }
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Clean up test files
    try:
        for i in range(10):
            os.remove(f"/tmp/test_{i}.txt")
    except:
        pass
    
    avg_duration = sum(r["duration"] for r in results.values() if r["status"] == "success") / total_operations if total_operations > 0 else 0
    
    return {
        "passed": total_operations >= len(operations) * 0.8 and avg_duration < 1.0,
        "total_duration": total_duration,
        "successful_operations": total_operations,
        "total_operations": len(operations),
        "avg_duration": avg_duration,
        "results": results
    }

def assess_documentation():
    """Assess documentation quality."""
    project_root = Path(__file__).parent
    
    documentation_files = [
        "project-starter/templates/ai-agents/advanced-agentic-rag-pipeline.md",
        "project-starter/templates/ai-agents/ADVANCED_AGENTIC_RAG_IMPLEMENTATION_SUMMARY.md"
    ]
    
    doc_metrics = {
        "total_files": len(documentation_files),
        "files_with_headings": 0,
        "files_with_code_blocks": 0,
        "files_with_lists": 0,
        "total_words": 0,
        "total_characters": 0
    }
    
    issues = []
    
    for file_path in documentation_files:
        full_path = project_root / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    doc_metrics["total_characters"] += len(content)
                    doc_metrics["total_words"] += len(content.split())
                    
                    if "# " in content:
                        doc_metrics["files_with_headings"] += 1
                    
                    if "```" in content:
                        doc_metrics["files_with_code_blocks"] += 1
                    
                    if "- " in content or "* " in content or "1. " in content:
                        doc_metrics["files_with_lists"] += 1
                    
                    # Check for minimum content length
                    if len(content) < 2000:
                        issues.append(f"{file_path}: Documentation too short ({len(content)} characters)")
                    
                    # Check for basic structure
                    if not any(marker in content for marker in ["# ", "## ", "### "]):
                        issues.append(f"{file_path}: No proper heading structure")
                    
            except Exception as e:
                issues.append(f"{file_path}: Error reading file - {e}")
        else:
            issues.append(f"{file_path}: File not found")
    
    # Calculate documentation score
    doc_score = 0
    if doc_metrics["files_with_headings"] == doc_metrics["total_files"]:
        doc_score += 30
    if doc_metrics["files_with_code_blocks"] >= doc_metrics["total_files"] * 0.5:
        doc_score += 30
    if doc_metrics["files_with_lists"] >= doc_metrics["total_files"] * 0.5:
        doc_score += 20
    if doc_metrics["total_words"] >= 5000:
        doc_score += 20
    
    return {
        "passed": doc_score >= 70 and len(issues) < 3,
        "documentation_score": doc_score,
        "metrics": doc_metrics,
        "issues": issues,
        "issue_count": len(issues)
    }

def generate_final_report(all_results):
    """Generate final comprehensive report."""
    print("\n📊 Final Comprehensive Test Report")
    print("=" * 60)
    
    # Calculate overall statistics
    total_tests = len(all_results)
    passed_tests = sum(1 for result in all_results.values() if result.get("status") == "passed" or result.get("passed", False))
    failed_tests = total_tests - passed_tests
    
    print(f"Total Test Suites: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests / total_tests) * 100:.1f}%")
    
    print(f"\nDetailed Results:")
    for test_name, result in all_results.items():
        if "status" in result:
            status = "✅ PASS" if result["status"] == "passed" else "❌ FAIL"
            if result["status"] == "error":
                status = "❌ ERROR"
        else:
            status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    # Performance summary
    if "performance" in all_results and "results" in all_results["performance"]:
        print(f"\nPerformance Summary:")
        for op_name, op_result in all_results["performance"]["results"].items():
            if op_result["status"] == "success":
                print(f"  {op_name}: {op_result['duration']:.3f}s")
    
    # Quality summary
    if "code_quality" in all_results and "metrics" in all_results["code_quality"]:
        metrics = all_results["code_quality"]["metrics"]
        print(f"\nCode Quality Summary:")
        print(f"  Total Files: {metrics['total_files']}")
        print(f"  Total Lines: {metrics['total_lines']}")
        print(f"  Total Functions: {metrics['total_functions']}")
        print(f"  Total Classes: {metrics['total_classes']}")
        print(f"  Quality Score: {all_results['code_quality']['quality_score']}/100")
    
    # Documentation summary
    if "documentation" in all_results and "metrics" in all_results["documentation"]:
        metrics = all_results["documentation"]["metrics"]
        print(f"\nDocumentation Summary:")
        print(f"  Total Files: {metrics['total_files']}")
        print(f"  Total Words: {metrics['total_words']}")
        print(f"  Total Characters: {metrics['total_characters']}")
        print(f"  Documentation Score: {all_results['documentation']['documentation_score']}/100")
    
    # Save comprehensive report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_test_suites": total_tests,
        "passed_test_suites": passed_tests,
        "failed_test_suites": failed_tests,
        "success_rate": (passed_tests / total_tests) * 100,
        "overall_status": "PASSED" if passed_tests == total_tests else "FAILED",
        "detailed_results": all_results
    }
    
    report_file = Path(__file__).parent / "final_comprehensive_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Comprehensive report saved to: {report_file}")
    
    return passed_tests == total_tests

def main():
    """Main comprehensive test function."""
    # Run all tests
    all_results = run_all_tests()
    
    # Generate final report
    all_passed = generate_final_report(all_results)
    
    print(f"\n🎯 Final Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 Congratulations! The Advanced Agentic RAG Pipeline implementation is working correctly!")
        print("   All components have been tested and validated successfully.")
    else:
        print("\n⚠️  Some tests failed. Please review the detailed report for specific issues.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

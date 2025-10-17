#!/usr/bin/env python3
"""
Test Runner for Advanced Agentic RAG Pipeline

This script runs comprehensive tests including unit tests, integration tests,
and performance benchmarks for the advanced agentic RAG pipeline.
"""

import os
import sys
import unittest
import time
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def run_unit_tests():
    """Run unit tests for all components."""
    print("🧪 Running Unit Tests")
    print("=" * 50)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = project_root / 'tests'
    suite = loader.discover(start_dir, pattern='test_agentic_rag_pipeline.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful(), result.testsRun, len(result.failures), len(result.errors)

def run_integration_tests():
    """Run integration tests for the complete pipeline."""
    print("\n🔗 Running Integration Tests")
    print("=" * 50)
    
    try:
        # Import the pipeline - using direct path
        sys.path.append(str(project_root / "project-starter" / "templates" / "ai-agents"))
        from advanced_agentic_rag_example import AdvancedAgenticRAGPipeline
        
        # Initialize pipeline
        pipeline = AdvancedAgenticRAGPipeline()
        
        # Test queries
        test_queries = [
            "What are the latest developments in artificial intelligence?",
            "Analyze the performance of Apple stock this year",
            "What are the current trends in renewable energy?",
            "Compare the security features of different cloud platforms"
        ]
        
        results = []
        
        for i, query in enumerate(test_queries, 1):
            print(f"Test Query {i}: {query}")
            
            try:
                start_time = time.time()
                result = pipeline.process_query(query)
                end_time = time.time()
                
                response_time = end_time - start_time
                overall_score = result['evaluation']['overall_score']['overall_score']
                
                print(f"  ✅ Response Time: {response_time:.2f}s")
                print(f"  ✅ Overall Score: {overall_score:.2f}/10")
                print(f"  ✅ Grade: {result['evaluation']['overall_score']['grade']}")
                
                results.append({
                    "query": query,
                    "response_time": response_time,
                    "overall_score": overall_score,
                    "grade": result['evaluation']['overall_score']['grade'],
                    "status": "success"
                })
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
                results.append({
                    "query": query,
                    "error": str(e),
                    "status": "error"
                })
        
        # Calculate statistics
        successful_tests = [r for r in results if r["status"] == "success"]
        avg_response_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests) if successful_tests else 0
        avg_score = sum(r["overall_score"] for r in successful_tests) / len(successful_tests) if successful_tests else 0
        
        print(f"\nIntegration Test Summary:")
        print(f"  Total Tests: {len(test_queries)}")
        print(f"  Successful: {len(successful_tests)}")
        print(f"  Failed: {len(results) - len(successful_tests)}")
        print(f"  Average Response Time: {avg_response_time:.2f}s")
        print(f"  Average Score: {avg_score:.2f}/10")
        
        return len(successful_tests) == len(test_queries), results
        
    except Exception as e:
        print(f"❌ Integration test setup failed: {str(e)}")
        return False, []

def run_performance_benchmarks():
    """Run performance benchmarks."""
    print("\n⚡ Running Performance Benchmarks")
    print("=" * 50)
    
    try:
        sys.path.append(str(project_root / "project-starter" / "templates" / "ai-agents"))
        from advanced_agentic_rag_example import AdvancedAgenticRAGPipeline
        
        pipeline = AdvancedAgenticRAGPipeline()
        
        # Benchmark queries
        benchmark_queries = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "What are the benefits of cloud computing?",
            "Explain quantum computing",
            "What is blockchain technology?"
        ]
        
        # Run benchmarks
        response_times = []
        memory_usage = []
        
        for i, query in enumerate(benchmark_queries, 1):
            print(f"Benchmark {i}: {query}")
            
            start_time = time.time()
            start_memory = get_memory_usage()
            
            try:
                result = pipeline.process_query(query)
                
                end_time = time.time()
                end_memory = get_memory_usage()
                
                response_time = end_time - start_time
                memory_delta = end_memory - start_memory
                
                response_times.append(response_time)
                memory_usage.append(memory_delta)
                
                print(f"  ⏱️  Response Time: {response_time:.2f}s")
                print(f"  💾 Memory Delta: {memory_delta:.2f}MB")
                
            except Exception as e:
                print(f"  ❌ Error: {str(e)}")
        
        # Calculate statistics
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            print(f"\nPerformance Summary:")
            print(f"  Average Response Time: {avg_response_time:.2f}s")
            print(f"  Min Response Time: {min_response_time:.2f}s")
            print(f"  Max Response Time: {max_response_time:.2f}s")
            
            if memory_usage:
                avg_memory = sum(memory_usage) / len(memory_usage)
                print(f"  Average Memory Usage: {avg_memory:.2f}MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Performance benchmark failed: {str(e)}")
        return False

def run_red_team_testing():
    """Run red team testing."""
    print("\n🔴 Running Red Team Testing")
    print("=" * 50)
    
    try:
        sys.path.append(str(project_root / "project-starter" / "templates" / "ai-agents"))
        from advanced_agentic_rag_example import AdvancedAgenticRAGPipeline
        
        pipeline = AdvancedAgenticRAGPipeline()
        
        # Run red team testing
        red_team_report = pipeline.run_red_team_testing(domain="technology", num_attacks=3)
        
        print(f"Red Team Test Results:")
        print(f"  Total Attacks: {red_team_report['summary']['total_attacks']}")
        print(f"  Vulnerable Attacks: {red_team_report['summary']['vulnerable_attacks']}")
        print(f"  Success Rate: {red_team_report['summary']['success_rate']}")
        print(f"  Average Response Quality: {red_team_report['summary']['avg_response_quality']}")
        print(f"  Average Safety Score: {red_team_report['summary']['avg_safety_score']}")
        
        print(f"\nRecommendations:")
        for i, rec in enumerate(red_team_report['recommendations'], 1):
            print(f"  {i}. {rec}")
        
        return True
        
    except Exception as e:
        print(f"❌ Red team testing failed: {str(e)}")
        return False

def get_memory_usage():
    """Get current memory usage in MB."""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        return 0

def run_stress_test():
    """Run stress test with multiple concurrent queries."""
    print("\n💪 Running Stress Test")
    print("=" * 50)
    
    try:
        sys.path.append(str(project_root / "project-starter" / "templates" / "ai-agents"))
        from advanced_agentic_rag_example import AdvancedAgenticRAGPipeline
        import threading
        import queue
        
        pipeline = AdvancedAgenticRAGPipeline()
        
        # Stress test queries
        stress_queries = [
            "What is artificial intelligence?",
            "How does machine learning work?",
            "What are the benefits of cloud computing?",
            "Explain quantum computing",
            "What is blockchain technology?",
            "What is the Internet of Things?",
            "How does cybersecurity work?",
            "What is data science?",
            "Explain software engineering",
            "What is DevOps?"
        ] * 2  # 20 queries total
        
        results = queue.Queue()
        
        def process_query_worker(query):
            try:
                start_time = time.time()
                result = pipeline.process_query(query)
                end_time = time.time()
                
                results.put({
                    "query": query,
                    "response_time": end_time - start_time,
                    "status": "success",
                    "score": result['evaluation']['overall_score']['overall_score']
                })
            except Exception as e:
                results.put({
                    "query": query,
                    "error": str(e),
                    "status": "error"
                })
        
        # Start threads
        threads = []
        start_time = time.time()
        
        for query in stress_queries:
            thread = threading.Thread(target=process_query_worker, args=(query,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Collect results
        test_results = []
        while not results.empty():
            test_results.append(results.get())
        
        # Calculate statistics
        successful_tests = [r for r in test_results if r["status"] == "success"]
        failed_tests = [r for r in test_results if r["status"] == "error"]
        
        if successful_tests:
            avg_response_time = sum(r["response_time"] for r in successful_tests) / len(successful_tests)
            avg_score = sum(r["score"] for r in successful_tests) / len(successful_tests)
            
            print(f"Stress Test Results:")
            print(f"  Total Queries: {len(stress_queries)}")
            print(f"  Successful: {len(successful_tests)}")
            print(f"  Failed: {len(failed_tests)}")
            print(f"  Total Time: {total_time:.2f}s")
            print(f"  Average Response Time: {avg_response_time:.2f}s")
            print(f"  Average Score: {avg_score:.2f}/10")
            print(f"  Queries per Second: {len(stress_queries) / total_time:.2f}")
        
        return len(successful_tests) > len(failed_tests)
        
    except Exception as e:
        print(f"❌ Stress test failed: {str(e)}")
        return False

def generate_test_report(unit_success, unit_tests, unit_failures, unit_errors,
                        integration_success, integration_results,
                        performance_success, red_team_success, stress_success):
    """Generate comprehensive test report."""
    print("\n📊 Test Report")
    print("=" * 50)
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "unit_tests": {
            "success": unit_success,
            "total_tests": unit_tests,
            "failures": unit_failures,
            "errors": unit_errors
        },
        "integration_tests": {
            "success": integration_success,
            "results": integration_results
        },
        "performance_benchmarks": {
            "success": performance_success
        },
        "red_team_testing": {
            "success": red_team_success
        },
        "stress_testing": {
            "success": stress_success
        },
        "overall_success": all([
            unit_success, integration_success, performance_success, 
            red_team_success, stress_success
        ])
    }
    
    # Print summary
    print(f"Unit Tests: {'✅ PASS' if unit_success else '❌ FAIL'} ({unit_tests} tests, {unit_failures} failures, {unit_errors} errors)")
    print(f"Integration Tests: {'✅ PASS' if integration_success else '❌ FAIL'}")
    print(f"Performance Benchmarks: {'✅ PASS' if performance_success else '❌ FAIL'}")
    print(f"Red Team Testing: {'✅ PASS' if red_team_success else '❌ FAIL'}")
    print(f"Stress Testing: {'✅ PASS' if stress_success else '❌ FAIL'}")
    print(f"\nOverall Result: {'✅ ALL TESTS PASSED' if report['overall_success'] else '❌ SOME TESTS FAILED'}")
    
    # Save report
    report_file = project_root / "test_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return report

def main():
    """Main test runner function."""
    print("🚀 Advanced Agentic RAG Pipeline Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all test suites
    unit_success, unit_tests, unit_failures, unit_errors = run_unit_tests()
    integration_success, integration_results = run_integration_tests()
    performance_success = run_performance_benchmarks()
    red_team_success = run_red_team_testing()
    stress_success = run_stress_test()
    
    # Generate report
    report = generate_test_report(
        unit_success, unit_tests, unit_failures, unit_errors,
        integration_success, integration_results,
        performance_success, red_team_success, stress_success
    )
    
    # Exit with appropriate code
    sys.exit(0 if report['overall_success'] else 1)

if __name__ == "__main__":
    main()

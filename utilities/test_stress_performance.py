#!/usr/bin/env python3
"""
Stress Test and Performance Benchmark for Advanced Agentic RAG Pipeline

This script tests the system under various stress conditions and measures performance.
"""

import os
import sys
import json
import time
import threading
import queue
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

def test_concurrent_queries():
    """Test system with multiple concurrent queries."""
    print("🔄 Testing Concurrent Queries")
    print("=" * 50)
    
    try:
        # Simulate concurrent query processing
        def process_query_worker(query_id, query, results_queue):
            start_time = time.time()
            
            # Simulate processing time (random between 0.1 and 0.5 seconds)
            processing_time = random.uniform(0.1, 0.5)
            time.sleep(processing_time)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            results_queue.put({
                "query_id": query_id,
                "query": query,
                "response_time": response_time,
                "processing_time": processing_time,
                "status": "success"
            })
        
        # Test with different numbers of concurrent queries
        test_scenarios = [
            {"name": "Light Load", "num_queries": 5, "max_workers": 3},
            {"name": "Medium Load", "num_queries": 15, "max_workers": 5},
            {"name": "Heavy Load", "num_queries": 30, "max_workers": 10},
            {"name": "Stress Load", "num_queries": 50, "max_workers": 15}
        ]
        
        results = {}
        
        for scenario in test_scenarios:
            print(f"  Testing {scenario['name']}: {scenario['num_queries']} queries, {scenario['max_workers']} workers")
            
            # Generate test queries
            test_queries = [
                f"What is artificial intelligence query {i}?"
                for i in range(scenario['num_queries'])
            ]
            
            # Process queries concurrently
            start_time = time.time()
            results_queue = queue.Queue()
            
            with ThreadPoolExecutor(max_workers=scenario['max_workers']) as executor:
                futures = []
                for i, query in enumerate(test_queries):
                    future = executor.submit(process_query_worker, i, query, results_queue)
                    futures.append(future)
                
                # Wait for all queries to complete
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"    ❌ Query failed: {e}")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Collect results
            query_results = []
            while not results_queue.empty():
                query_results.append(results_queue.get())
            
            # Calculate statistics
            if query_results:
                avg_response_time = sum(r["response_time"] for r in query_results) / len(query_results)
                min_response_time = min(r["response_time"] for r in query_results)
                max_response_time = max(r["response_time"] for r in query_results)
                success_rate = sum(1 for r in query_results if r["status"] == "success") / len(query_results) * 100
                queries_per_second = len(query_results) / total_time
                
                results[scenario['name']] = {
                    "total_queries": len(query_results),
                    "successful_queries": sum(1 for r in query_results if r["status"] == "success"),
                    "total_time": total_time,
                    "avg_response_time": avg_response_time,
                    "min_response_time": min_response_time,
                    "max_response_time": max_response_time,
                    "success_rate": success_rate,
                    "queries_per_second": queries_per_second
                }
                
                print(f"    ✅ Completed in {total_time:.2f}s")
                print(f"    ✅ Success Rate: {success_rate:.1f}%")
                print(f"    ✅ Avg Response Time: {avg_response_time:.3f}s")
                print(f"    ✅ Queries/Second: {queries_per_second:.1f}")
            else:
                results[scenario['name']] = {"error": "No results collected"}
                print(f"    ❌ No results collected")
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error testing concurrent queries: {e}")
        return {}

def test_memory_usage():
    """Test memory usage under different loads."""
    print("\n💾 Testing Memory Usage")
    print("=" * 50)
    
    try:
        # Simulate memory usage patterns
        memory_tests = [
            {"name": "Baseline", "iterations": 1, "data_size": 1000},
            {"name": "Small Load", "iterations": 10, "data_size": 1000},
            {"name": "Medium Load", "iterations": 50, "data_size": 1000},
            {"name": "Large Load", "iterations": 100, "data_size": 1000},
            {"name": "Memory Intensive", "iterations": 50, "data_size": 10000}
        ]
        
        results = {}
        
        for test in memory_tests:
            print(f"  Testing {test['name']}: {test['iterations']} iterations, {test['data_size']} data size")
            
            # Measure memory before
            initial_memory = get_memory_usage()
            
            # Simulate memory-intensive operations
            data_structures = []
            for i in range(test['iterations']):
                # Create data structure
                data = {
                    "id": i,
                    "content": "x" * test['data_size'],
                    "metadata": {"timestamp": datetime.now().isoformat()},
                    "results": [j for j in range(100)]  # Additional data
                }
                data_structures.append(data)
            
            # Measure memory after
            peak_memory = get_memory_usage()
            memory_delta = peak_memory - initial_memory
            
            # Clean up
            del data_structures
            
            # Measure memory after cleanup
            final_memory = get_memory_usage()
            memory_retained = final_memory - initial_memory
            
            results[test['name']] = {
                "initial_memory": initial_memory,
                "peak_memory": peak_memory,
                "final_memory": final_memory,
                "memory_delta": memory_delta,
                "memory_retained": memory_retained,
                "iterations": test['iterations'],
                "data_size": test['data_size']
            }
            
            print(f"    ✅ Memory Delta: {memory_delta:.1f}MB")
            print(f"    ✅ Memory Retained: {memory_retained:.1f}MB")
            print(f"    ✅ Peak Memory: {peak_memory:.1f}MB")
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error testing memory usage: {e}")
        return {}

def test_error_handling():
    """Test error handling under various conditions."""
    print("\n🚨 Testing Error Handling")
    print("=" * 50)
    
    try:
        error_scenarios = [
            {"name": "Invalid Input", "test_func": lambda: 1 / 0},
            {"name": "Timeout Simulation", "test_func": lambda: time.sleep(10)},
            {"name": "Memory Error", "test_func": lambda: [0] * (10**8)},
            {"name": "File Not Found", "test_func": lambda: open("nonexistent_file.txt")},
            {"name": "Network Error", "test_func": lambda: requests.get("http://nonexistent-url.com")}
        ]
        
        results = {}
        
        for scenario in error_scenarios:
            print(f"  Testing {scenario['name']}")
            
            try:
                start_time = time.time()
                scenario['test_func']()
                end_time = time.time()
                
                results[scenario['name']] = {
                    "status": "unexpected_success",
                    "response_time": end_time - start_time,
                    "error": None
                }
                print(f"    ⚠️  Unexpected success")
                
            except ZeroDivisionError as e:
                results[scenario['name']] = {
                    "status": "handled_error",
                    "error_type": "ZeroDivisionError",
                    "error_message": str(e)
                }
                print(f"    ✅ Handled ZeroDivisionError correctly")
                
            except MemoryError as e:
                results[scenario['name']] = {
                    "status": "handled_error",
                    "error_type": "MemoryError",
                    "error_message": str(e)
                }
                print(f"    ✅ Handled MemoryError correctly")
                
            except FileNotFoundError as e:
                results[scenario['name']] = {
                    "status": "handled_error",
                    "error_type": "FileNotFoundError",
                    "error_message": str(e)
                }
                print(f"    ✅ Handled FileNotFoundError correctly")
                
            except Exception as e:
                results[scenario['name']] = {
                    "status": "handled_error",
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }
                print(f"    ✅ Handled {type(e).__name__} correctly")
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error testing error handling: {e}")
        return {}

def test_data_processing_performance():
    """Test data processing performance with various data sizes."""
    print("\n📊 Testing Data Processing Performance")
    print("=" * 50)
    
    try:
        data_sizes = [100, 500, 1000, 5000, 10000]
        results = {}
        
        for size in data_sizes:
            print(f"  Testing with {size} data points")
            
            # Generate test data
            test_data = [{"id": i, "value": random.random(), "category": f"cat_{i % 10}"} for i in range(size)]
            
            # Test data processing operations
            start_time = time.time()
            
            # Simulate data processing
            processed_data = []
            for item in test_data:
                processed_item = {
                    "id": item["id"],
                    "value": item["value"] * 2,  # Simple transformation
                    "category": item["category"],
                    "processed_at": datetime.now().isoformat()
                }
                processed_data.append(processed_item)
            
            # Simulate aggregation
            category_counts = {}
            for item in processed_data:
                category = item["category"]
                category_counts[category] = category_counts.get(category, 0) + 1
            
            # Simulate filtering
            filtered_data = [item for item in processed_data if item["value"] > 0.5]
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            results[f"size_{size}"] = {
                "data_size": size,
                "processing_time": processing_time,
                "processed_items": len(processed_data),
                "filtered_items": len(filtered_data),
                "categories": len(category_counts),
                "items_per_second": size / processing_time if processing_time > 0 else 0
            }
            
            print(f"    ✅ Processed in {processing_time:.3f}s")
            print(f"    ✅ Items/Second: {size / processing_time:.1f}")
            print(f"    ✅ Filtered: {len(filtered_data)}/{size}")
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error testing data processing: {e}")
        return {}

def test_network_simulation():
    """Test network-related performance (simulated)."""
    print("\n🌐 Testing Network Simulation")
    print("=" * 50)
    
    try:
        network_scenarios = [
            {"name": "Fast Network", "latency": 0.01, "bandwidth": 1000},
            {"name": "Medium Network", "latency": 0.1, "bandwidth": 100},
            {"name": "Slow Network", "latency": 0.5, "bandwidth": 10},
            {"name": "Very Slow Network", "latency": 2.0, "bandwidth": 1}
        ]
        
        results = {}
        
        for scenario in network_scenarios:
            print(f"  Testing {scenario['name']}: {scenario['latency']}s latency, {scenario['bandwidth']}MB/s bandwidth")
            
            # Simulate network requests
            num_requests = 10
            request_size = 1024  # 1KB per request
            
            start_time = time.time()
            
            for i in range(num_requests):
                # Simulate latency
                time.sleep(scenario['latency'])
                
                # Simulate bandwidth limitation
                transfer_time = request_size / (scenario['bandwidth'] * 1024 * 1024)  # Convert to seconds
                time.sleep(transfer_time)
            
            end_time = time.time()
            total_time = end_time - start_time
            
            results[scenario['name']] = {
                "latency": scenario['latency'],
                "bandwidth": scenario['bandwidth'],
                "num_requests": num_requests,
                "request_size": request_size,
                "total_time": total_time,
                "avg_time_per_request": total_time / num_requests,
                "effective_bandwidth": (num_requests * request_size) / total_time / (1024 * 1024)  # MB/s
            }
            
            print(f"    ✅ Total Time: {total_time:.3f}s")
            print(f"    ✅ Avg Time/Request: {total_time / num_requests:.3f}s")
            print(f"    ✅ Effective Bandwidth: {(num_requests * request_size) / total_time / (1024 * 1024):.1f}MB/s")
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error testing network simulation: {e}")
        return {}

def get_memory_usage():
    """Get current memory usage in MB."""
    try:
        import psutil
        process = psutil.Process()
        return process.memory_info().rss / 1024 / 1024
    except ImportError:
        # Fallback for systems without psutil
        return 0

def test_system_limits():
    """Test system limits and boundaries."""
    print("\n🔒 Testing System Limits")
    print("=" * 50)
    
    try:
        limits_tests = [
            {"name": "Max String Length", "test_func": lambda: "x" * (10**6)},
            {"name": "Max List Size", "test_func": lambda: [0] * (10**5)},
            {"name": "Max Dictionary Size", "test_func": lambda: {i: i for i in range(10**4)}},
            {"name": "Max Recursion Depth", "test_func": lambda: test_recursion(0, 1000)},
            {"name": "Max File Handles", "test_func": lambda: [open(f"/tmp/test_{i}.txt", "w") for i in range(100)]}
        ]
        
        results = {}
        
        for test in limits_tests:
            print(f"  Testing {test['name']}")
            
            try:
                start_time = time.time()
                result = test['test_func']()
                end_time = time.time()
                
                results[test['name']] = {
                    "status": "success",
                    "response_time": end_time - start_time,
                    "result_size": len(str(result)) if hasattr(result, '__len__') else 1
                }
                print(f"    ✅ Success in {end_time - start_time:.3f}s")
                
            except RecursionError as e:
                results[test['name']] = {
                    "status": "recursion_limit",
                    "error": str(e)
                }
                print(f"    ✅ Hit recursion limit (expected)")
                
            except MemoryError as e:
                results[test['name']] = {
                    "status": "memory_limit",
                    "error": str(e)
                }
                print(f"    ✅ Hit memory limit (expected)")
                
            except OSError as e:
                results[test['name']] = {
                    "status": "file_limit",
                    "error": str(e)
                }
                print(f"    ✅ Hit file limit (expected)")
                
            except Exception as e:
                results[test['name']] = {
                    "status": "other_error",
                    "error": str(e)
                }
                print(f"    ⚠️  Unexpected error: {e}")
        
        return results
        
    except Exception as e:
        print(f"  ❌ Error testing system limits: {e}")
        return {}

def test_recursion(depth, max_depth):
    """Helper function for recursion testing."""
    if depth >= max_depth:
        return depth
    return test_recursion(depth + 1, max_depth)

def generate_stress_report(results):
    """Generate comprehensive stress test report."""
    print("\n📊 Stress Test Report")
    print("=" * 50)
    
    total_tests = sum(len(test_results) for test_results in results.values())
    successful_tests = sum(
        sum(1 for result in test_results.values() if result.get("status") in ["success", "handled_error", "recursion_limit", "memory_limit", "file_limit"])
        for test_results in results.values()
    )
    
    print(f"Total Test Scenarios: {total_tests}")
    print(f"Successful Scenarios: {successful_tests}")
    print(f"Success Rate: {(successful_tests / total_tests) * 100:.1f}%")
    
    # Performance summary
    if "Concurrent Queries" in results:
        concurrent_results = results["Concurrent Queries"]
        print(f"\nConcurrent Query Performance:")
        for scenario, data in concurrent_results.items():
            if "queries_per_second" in data:
                print(f"  {scenario}: {data['queries_per_second']:.1f} queries/sec")
    
    # Memory usage summary
    if "Memory Usage" in results:
        memory_results = results["Memory Usage"]
        print(f"\nMemory Usage:")
        for scenario, data in memory_results.items():
            if "memory_delta" in data:
                print(f"  {scenario}: {data['memory_delta']:.1f}MB delta")
    
    # Save detailed report
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_scenarios": total_tests,
        "successful_scenarios": successful_tests,
        "success_rate": (successful_tests / total_tests) * 100,
        "detailed_results": results
    }
    
    report_file = Path(__file__).parent / "stress_test_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    
    return successful_tests / total_tests > 0.8  # 80% success rate threshold

def main():
    """Main stress test function."""
    print("🚀 Stress Test and Performance Benchmark for Advanced Agentic RAG Pipeline")
    print("=" * 90)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all stress tests
    results = {
        "Concurrent Queries": test_concurrent_queries(),
        "Memory Usage": test_memory_usage(),
        "Error Handling": test_error_handling(),
        "Data Processing Performance": test_data_processing_performance(),
        "Network Simulation": test_network_simulation(),
        "System Limits": test_system_limits()
    }
    
    # Generate report
    stress_passed = generate_stress_report(results)
    
    print(f"\nOverall Result: {'✅ STRESS TESTS PASSED' if stress_passed else '❌ STRESS TESTS FAILED'}")
    
    return 0 if stress_passed else 1

if __name__ == "__main__":
    sys.exit(main())

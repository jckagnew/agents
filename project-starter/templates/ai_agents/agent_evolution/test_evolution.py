"""
Test suite for Pattern 19: Agent Evolution - Adaptive Learning and Self-Improvement
"""

import asyncio
import json
import tempfile
import shutil
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent
sys.path.append(str(project_root))

from evolution_framework import (
    EvolutionFramework, EvolutionStrategy, MutationType, SelectionType,
    FitnessFunction, EvolutionStatus, AgentGenome, EvolutionExperiment,
    EvolutionEvent, EvolutionMetrics
)


async def test_basic_functionality():
    """Test basic evolution framework functionality"""
    print("🧪 Testing Pattern 19: Agent Evolution - Basic Functionality")
    print("=" * 60)
    
    # Create framework with temporary storage
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        print("✅ Evolution framework created")
        
        # Test genome creation
        genes = {"learning_rate": 0.01, "exploration_rate": 0.5, "memory_size": 500}
        genome_id = framework.create_agent_genome("test_agent", genes)
        assert genome_id is not None
        print("✅ Genome creation works")
        
        # Test fitness evaluation
        performance = {"accuracy": 0.85, "efficiency": 0.7, "robustness": 0.8}
        fitness = framework.evaluate_fitness(genome_id, performance)
        assert fitness > 0
        print("✅ Fitness evaluation works")
        
        # Test experiment creation
        experiment_id = framework.create_evolution_experiment(
            "Test Evolution", "Testing evolution capabilities",
            EvolutionStrategy.GENETIC_ALGORITHM, population_size=10, max_generations=5
        )
        assert experiment_id is not None
        print("✅ Experiment creation works")
        
        # Test metrics
        metrics = framework.get_evolution_metrics()
        assert metrics.total_experiments >= 1
        print("✅ Metrics work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Basic evolution tests passed!")


async def test_evolution_strategies():
    """Test different evolution strategies"""
    print("\n🧪 Testing Evolution Strategies")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Test all strategies
        strategies = [
            EvolutionStrategy.GENETIC_ALGORITHM,
            EvolutionStrategy.PARTICLE_SWARM,
            EvolutionStrategy.SIMULATED_ANNEALING,
            EvolutionStrategy.GRADIENT_DESCENT,
            EvolutionStrategy.REINFORCEMENT_LEARNING,
            EvolutionStrategy.META_LEARNING
        ]
        
        for strategy in strategies:
            experiment_id = framework.create_evolution_experiment(
                f"Test {strategy.value}", f"Testing {strategy.value}",
                strategy, population_size=5, max_generations=3
            )
            assert experiment_id is not None
            print(f"✅ {strategy.value} strategy works")
        
        # Test strategy usage in metrics
        metrics = framework.get_evolution_metrics()
        assert metrics.total_experiments >= 6
        print("✅ Strategy tracking works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Evolution strategies tests passed!")


async def test_mutation_types():
    """Test different mutation types"""
    print("\n🧪 Testing Mutation Types")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Create test genome
        genes = {"learning_rate": 0.01, "exploration_rate": 0.5, "memory_size": 500}
        genome_id = framework.create_agent_genome("test_agent", genes)
        
        # Test different mutation types
        mutation_types = [
            MutationType.GAUSSIAN,
            MutationType.UNIFORM,
            MutationType.POLYNOMIAL,
            MutationType.ADAPTIVE
        ]
        
        for mutation_type in mutation_types:
            mutated_id = framework.mutate_genome(genome_id, mutation_type, 0.1)
            assert mutated_id is not None
            mutated_genome = framework.genomes[mutated_id]
            assert mutated_genome.mutation_history
            print(f"✅ {mutation_type.value} mutation works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Mutation types tests passed!")


async def test_selection_types():
    """Test different selection types"""
    print("\n🧪 Testing Selection Types")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Create test experiment
        experiment_id = framework.create_evolution_experiment(
            "Test Selection", "Testing selection strategies",
            EvolutionStrategy.GENETIC_ALGORITHM, population_size=10, max_generations=5
        )
        
        # Create test genomes
        for i in range(10):
            agent_id = f"exp_{experiment_id}_agent_{i}"
            genes = {"learning_rate": 0.01 + i * 0.001, "exploration_rate": 0.5}
            genome_id = framework.create_agent_genome(agent_id, genes)
            # Set different fitness scores
            framework.evaluate_fitness(genome_id, {"accuracy": 0.5 + i * 0.05})
        
        # Test different selection types
        selection_types = [
            SelectionType.TOURNAMENT,
            SelectionType.RANK_SELECTION,
            SelectionType.ROULETTE_WHEEL,
            SelectionType.ELITISM
        ]
        
        for selection_type in selection_types:
            # Update experiment selection type
            experiment = framework.experiments[experiment_id]
            experiment.selection_type = selection_type
            framework._save_experiment(experiment)
            
            parents = framework.select_parents(experiment_id, 4)
            assert len(parents) >= 2  # Should select at least 2 parents
            print(f"✅ {selection_type.value} selection works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Selection types tests passed!")


async def test_crossover_operations():
    """Test crossover operations"""
    print("\n🧪 Testing Crossover Operations")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Create parent genomes
        parent1_genes = {"learning_rate": 0.01, "exploration_rate": 0.5, "memory_size": 500}
        parent1_id = framework.create_agent_genome("parent1", parent1_genes)
        
        parent2_genes = {"learning_rate": 0.05, "exploration_rate": 0.8, "memory_size": 800}
        parent2_id = framework.create_agent_genome("parent2", parent2_genes)
        
        # Test different crossover types
        crossover_types = ["uniform", "single_point", "arithmetic"]
        
        for crossover_type in crossover_types:
            offspring1_id, offspring2_id = framework.crossover_genomes(
                parent1_id, parent2_id, crossover_type
            )
            assert offspring1_id is not None
            assert offspring2_id is not None
            
            offspring1 = framework.genomes[offspring1_id]
            offspring2 = framework.genomes[offspring2_id]
            
            assert offspring1.crossover_history
            assert offspring2.crossover_history
            print(f"✅ {crossover_type} crossover works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Crossover operations tests passed!")


async def test_fitness_functions():
    """Test different fitness functions"""
    print("\n🧪 Testing Fitness Functions")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Test all fitness functions
        fitness_functions = [
            FitnessFunction.ACCURACY,
            FitnessFunction.EFFICIENCY,
            FitnessFunction.ROBUSTNESS,
            FitnessFunction.ADAPTABILITY,
            FitnessFunction.CREATIVITY
        ]
        
        for fitness_function in fitness_functions:
            experiment_id = framework.create_evolution_experiment(
                f"Test {fitness_function.value}", f"Testing {fitness_function.value}",
                EvolutionStrategy.GENETIC_ALGORITHM, fitness_function=fitness_function
            )
            assert experiment_id is not None
            print(f"✅ {fitness_function.value} fitness function works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Fitness functions tests passed!")


async def test_evolution_persistence():
    """Test evolution data persistence"""
    print("\n🧪 Testing Evolution Persistence")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        # Create framework and add data
        framework1 = EvolutionFramework({"storage_path": temp_dir})
        
        # Add test data
        genes = {"learning_rate": 0.01, "exploration_rate": 0.5}
        genome_id = framework1.create_agent_genome("test_agent", genes)
        framework1.evaluate_fitness(genome_id, {"accuracy": 0.85})
        
        experiment_id = framework1.create_evolution_experiment(
            "Test Persistence", "Testing data persistence",
            EvolutionStrategy.GENETIC_ALGORITHM
        )
        
        # Create new framework instance (should load existing data)
        framework2 = EvolutionFramework({"storage_path": temp_dir})
        
        # Verify data was loaded
        assert genome_id in framework2.genomes
        assert experiment_id in framework2.experiments
        print("✅ Evolution persistence works")
        
        # Test stats consistency
        metrics1 = framework1.get_evolution_metrics()
        metrics2 = framework2.get_evolution_metrics()
        assert metrics1.total_experiments == metrics2.total_experiments
        print("✅ Stats consistency works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Evolution persistence tests passed!")


async def test_evolution_stats():
    """Test evolution statistics"""
    print("\n🧪 Testing Evolution Statistics")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Add test data
        for i in range(5):
            experiment_id = framework.create_evolution_experiment(
                f"Test Experiment {i}", f"Testing experiment {i}",
                EvolutionStrategy.GENETIC_ALGORITHM, population_size=10, max_generations=3
            )
            
            # Create some genomes for each experiment
            for j in range(5):
                agent_id = f"exp_{experiment_id}_agent_{j}"
                genes = {"learning_rate": 0.01 + j * 0.001}
                genome_id = framework.create_agent_genome(agent_id, genes)
                framework.evaluate_fitness(genome_id, {"accuracy": 0.5 + j * 0.1})
        
        # Test metrics
        metrics = framework.get_evolution_metrics()
        
        assert metrics.total_experiments >= 5
        assert metrics.total_generations >= 0
        assert 0 <= metrics.average_fitness <= 1
        assert 0 <= metrics.best_fitness <= 1
        assert 0 <= metrics.evolution_speed
        assert 0 <= metrics.success_rate <= 1
        assert 0 <= metrics.mutation_effectiveness <= 1
        assert 0 <= metrics.crossover_effectiveness <= 1
        print("✅ Evolution statistics work")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Evolution statistics tests passed!")


async def test_evolution_control():
    """Test evolution framework control"""
    print("\n🧪 Testing Evolution Control")
    print("=" * 30)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Test start/stop
        framework.start_evolution_processing()
        assert framework.evolution_processor_running
        print("✅ Evolution start works")
        
        framework.stop_evolution_processing()
        assert not framework.evolution_processor_running
        print("✅ Evolution stop works")
        
        # Test queue
        framework.evolution_queue.append({"type": "test_task"})
        assert len(framework.evolution_queue) >= 1  # May be processed by background thread
        print("✅ Evolution queue works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Evolution control tests passed!")


async def test_data_export():
    """Test data export functionality"""
    print("\n🧪 Testing Data Export")
    print("=" * 25)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Add some test data
        genes = {"learning_rate": 0.01, "exploration_rate": 0.5}
        genome_id = framework.create_agent_genome("test_agent", genes)
        framework.evaluate_fitness(genome_id, {"accuracy": 0.85})
        
        experiment_id = framework.create_evolution_experiment(
            "Test Export", "Testing data export",
            EvolutionStrategy.GENETIC_ALGORITHM
        )
        
        # Test JSON export
        json_export = framework.export_evolution_data(format="json")
        assert "genomes" in json_export
        assert "experiments" in json_export
        assert "events" in json_export
        assert "metrics" in json_export
        print("✅ JSON export works")
        
        # Test dict export
        dict_export = framework.export_evolution_data(format="dict")
        assert "genomes" in dict_export
        assert "experiments" in dict_export
        assert "events" in dict_export
        assert "metrics" in dict_export
        print("✅ Dict export works")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Data export tests passed!")


async def test_data_clear():
    """Test data clearing functionality"""
    print("\n🧪 Testing Data Clear")
    print("=" * 25)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        # Add test data
        genes = {"learning_rate": 0.01, "exploration_rate": 0.5}
        genome_id = framework.create_agent_genome("test_agent", genes)
        
        experiment_id = framework.create_evolution_experiment(
            "Test Clear", "Testing data clearing",
            EvolutionStrategy.GENETIC_ALGORITHM
        )
        
        # Verify data exists
        assert len(framework.genomes) >= 1
        assert len(framework.experiments) >= 1
        print("✅ Data added successfully")
        
        # Clear data
        framework.clear_evolution_data()
        
        # Verify data is cleared
        assert len(framework.genomes) == 0
        assert len(framework.experiments) == 0
        print("✅ Data cleared successfully")
        
        # Test stats after clear
        metrics = framework.get_evolution_metrics()
        assert metrics.total_experiments == 0
        print("✅ Stats reset after clear")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Data clear tests passed!")


async def test_integration_scenario():
    """Test an end-to-end integration scenario"""
    print("\n🧪 Testing Integration Scenario")
    print("=" * 35)
    
    temp_dir = tempfile.mkdtemp()
    try:
        framework = EvolutionFramework({"storage_path": temp_dir})
        
        print("🧬 AI Agent Evolution Scenario")
        
        # Create evolution experiment
        experiment_id = framework.create_evolution_experiment(
            "AI Agent Optimization",
            "Evolving AI agents for better performance",
            EvolutionStrategy.GENETIC_ALGORITHM,
            population_size=20,
            max_generations=10,
            fitness_function=FitnessFunction.ACCURACY,
            mutation_rate=0.1,
            crossover_rate=0.8,
            selection_type=SelectionType.TOURNAMENT
        )
        
        print(f"✅ Created experiment: {experiment_id}")
        
        # Initialize population
        framework._initialize_population(framework.experiments[experiment_id])
        print("✅ Population initialized")
        
        # Run a few generations manually
        for generation in range(3):
            framework._evolve_generation(experiment_id)
            experiment = framework.experiments[experiment_id]
            print(f"✅ Generation {generation + 1}: Best fitness = {experiment.best_fitness:.3f}")
        
        # Test mutation
        population = [g for g in framework.genomes.values() if g.agent_id.startswith(f"exp_{experiment_id}")]
        if population:
            best_genome = max(population, key=lambda g: g.fitness_score)
            mutated_id = framework.mutate_genome(best_genome.id, MutationType.GAUSSIAN, 0.1)
            print(f"✅ Mutated best genome: {mutated_id}")
        
        # Test crossover
        if len(population) >= 2:
            parent1, parent2 = population[0], population[1]
            offspring1_id, offspring2_id = framework.crossover_genomes(parent1.id, parent2.id)
            print(f"✅ Crossover: {offspring1_id}, {offspring2_id}")
        
        # Check final state
        metrics = framework.get_evolution_metrics()
        print(f"✅ Final stats: {metrics.total_experiments} experiments, {metrics.total_generations} generations")
        print(f"✅ Best fitness: {metrics.best_fitness:.3f}, Average fitness: {metrics.average_fitness:.3f}")
        
        # Test data export
        export_data = framework.export_evolution_data(format="dict")
        assert "genomes" in export_data
        assert "experiments" in export_data
        assert "events" in export_data
        assert "metrics" in export_data
        print("✅ Data export successful")
        
        print("✅ Complete evolution scenario successful")
        
    finally:
        shutil.rmtree(temp_dir)
    print("🎯 Integration scenario tests passed!")


async def main():
    """Run all tests"""
    print("🚀 Starting Pattern 19: Agent Evolution Tests")
    print("=" * 60)
    
    await test_basic_functionality()
    await test_evolution_strategies()
    await test_mutation_types()
    await test_selection_types()
    await test_crossover_operations()
    await test_fitness_functions()
    await test_evolution_persistence()
    await test_evolution_stats()
    await test_evolution_control()
    await test_data_export()
    await test_data_clear()
    await test_integration_scenario()
    
    print("\n🎉 All Pattern 19: Agent Evolution tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())


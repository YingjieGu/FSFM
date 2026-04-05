"""
FSFM Framework Main Module
Forgetting to Remember More: A Biologically-Inspired Selective Forgetting Framework
"""

from .memory_manager import MemoryManager
from .forgetting_strategies import (
    PassiveDecayStrategy, 
    ActiveDeletionStrategy, 
    AdaptiveReinforcementStrategy,
    MultiLayerMemoryArchitecture
)
from typing import Dict, List, Any, Optional
import time


class FSFMFramework:
    """
    Main FSFM (Forgetting to Remember More) Framework Class
    
    This framework implements a comprehensive selective forgetting system for LLM agents
    that draws direct parallels from human cognitive processes including:
    - Hippocampal memory indexing/consolidation theory
    - Ebbinghaus's forgetting curve  
    - Synaptic pruning mechanisms
    - Memory reconsolidation theory
    
    The framework provides three key capabilities:
    1. Computational and storage efficiency through intelligent memory pruning
    2. Enhanced personalization via dynamic updating of outdated information
    3. Robust security through active forgetting of malicious/sensitive content
    """
    
    def __init__(self, capacity_ratio: float = 0.7):
        """
        Initialize FSFM Framework
        
        Args:
            capacity_ratio: Ratio of total data to retain (default 0.7 for 70%)
        """
        self.capacity_ratio = capacity_ratio
        self.sfr_system = MemoryManager("SFR")
        self.baseline_system = MemoryManager("Baseline")
        
        # Initialize forgetting strategies
        self.passive_decay = PassiveDecayStrategy()
        self.active_deletion = ActiveDeletionStrategy()
        self.adaptive_reinforcement = AdaptiveReinforcementStrategy()
        self.multi_layer_architecture = MultiLayerMemoryArchitecture()
        
    def configure_systems(self, total_data_size: int):
        """
        Configure SFR and baseline systems with appropriate capacities
        
        Args:
            total_data_size: Total number of records in the dataset
        """
        sfr_capacity = int(total_data_size * self.capacity_ratio)
        self.sfr_system.capacity = sfr_capacity
        # Baseline system has no capacity constraint (unlimited)
        self.baseline_system.capacity = None
        
    def train_systems(self, training_data: List[tuple]):
        """
        Train both SFR and baseline systems with training data
        
        Args:
            training_data: List of (record, category) tuples for training
        """
        print(f"Training SFR system with {len(training_data)} records...")
        for record, category in training_data:
            self.sfr_system.insert_memory(record, category, is_validation=False)
            
        print(f"Training Baseline system with {len(training_data)} records...")
        for record, category in training_data:
            self.baseline_system.insert_memory(record, category, is_validation=False)
            
    def validate_and_forget(self, validation_data: List[tuple]):
        """
        Validate systems and trigger SFR selective forgetting
        
        Args:
            validation_data: List of (record, category) tuples for validation
        """
        print(f"Validating SFR system with {len(validation_data)} records (triggers forgetting)...")
        for record, category in validation_data:
            self.sfr_system.insert_memory(record, category, is_validation=True)
            
        print(f"Validating Baseline system with {len(validation_data)} records...")
        for record, category in validation_data:
            self.baseline_system.insert_memory(record, category, is_validation=True)
            
    def evaluate_performance(self, test_queries: List[str]) -> Dict[str, Any]:
        """
        Evaluate performance of both systems
        
        Args:
            test_queries: List of queries for performance testing
            
        Returns:
            Dict containing performance metrics for both systems
        """
        # Evaluate SFR system
        sfr_start = time.perf_counter()
        sfr_results = []
        for query in test_queries:
            results = self.sfr_system.find_similar_memories(query)
            sfr_results.append(results)
        sfr_time = time.perf_counter() - sfr_start
        
        # Evaluate Baseline system  
        baseline_start = time.perf_counter()
        baseline_results = []
        for query in test_queries:
            results = self.baseline_system.find_similar_memories(query)
            baseline_results.append(results)
        baseline_time = time.perf_counter() - baseline_start
        
        # Analyze results
        sfr_memory_size = len(self.sfr_system.memories)
        baseline_memory_size = len(self.baseline_system.memories)
        
        # Calculate safety metrics
        sfr_dangerous_count = sum(1 for m in self.sfr_system.memories if m['category'] == 'dangerous')
        baseline_dangerous_count = sum(1 for m in self.baseline_system.memories if m['category'] == 'dangerous')
        
        return {
            'sfr_performance': {
                'retrieval_time': sfr_time,
                'memory_size': sfr_memory_size,
                'dangerous_content_count': sfr_dangerous_count
            },
            'baseline_performance': {
                'retrieval_time': baseline_time,
                'memory_size': baseline_memory_size,
                'dangerous_content_count': baseline_dangerous_count
            },
            'comparative_metrics': {
                'memory_efficiency': (1 - sfr_memory_size / baseline_memory_size) * 100,
                'speedup_ratio': baseline_time / sfr_time if sfr_time > 0 else 1.0,
                'safety_improvement': (baseline_dangerous_count - sfr_dangerous_count) / baseline_dangerous_count if baseline_dangerous_count > 0 else 0.0
            }
        }


# Framework Configuration Constants
DEFAULT_CONFIG = {
    'capacity_ratio': 0.7,
    'training_split': 0.7,
    'validation_split': 0.3,
    'batch_size': 100,
    'test_query_limit': 500
}


def create_fsffm_instance(config: Optional[Dict] = None) -> FSFMFramework:
    """
    Factory function to create FSFM framework instance
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        FSFMFramework instance
    """
    if config is None:
        config = DEFAULT_CONFIG
        
    framework = FSFMFramework(capacity_ratio=config.get('capacity_ratio', 0.7))
    return framework
"""
Forgetting Strategies Module for FSFM Framework
Implements various biologically-inspired forgetting mechanisms
"""

import numpy as np
from typing import Dict, List, Any, Callable
from dataclasses import dataclass


@dataclass
class ForgettingPolicy:
    """Configuration for forgetting policy"""
    name: str
    strategy_type: str  # 'passive_decay', 'active_deletion', 'adaptive_reinforcement'
    parameters: Dict[str, Any]


class PassiveDecayStrategy:
    """
    Passive Decay-Based Forgetting Strategy
    
    Inspired by Ebbinghaus's Forgetting Curve:
    Retention(t) = e^(-λt)
    
    Where:
    - Retention(t) = probability of successful retrieval at time t
    - λ = decay rate parameter (varies by memory type and importance)
    - t = time since last reinforcement
    
    This strategy implements time-dependent decay functions that reduce 
    memory accessibility over time unless reinforced through usage.
    """
    
    def __init__(self, decay_rate: float = 0.1):
        self.decay_rate = decay_rate
        
    def calculate_retention_probability(self, time_since_access: float, 
                                     access_frequency: int = 1) -> float:
        """
        Calculate retention probability using Ebbinghaus forgetting curve
        
        Args:
            time_since_access: Time since last memory access (in arbitrary units)
            access_frequency: Number of times memory has been accessed
            
        Returns:
            float: Retention probability [0, 1]
        """
        # Adjust decay rate based on access frequency (spaced repetition effect)
        adjusted_decay = self.decay_rate / (1 + np.log(1 + access_frequency))
        retention = np.exp(-adjusted_decay * time_since_access)
        return max(0.0, min(1.0, retention))


class ActiveDeletionStrategy:
    """
    Active Deletion-Based Forgetting Strategy
    
    Implements targeted deletion of specific memory content based on explicit criteria:
    - User-initiated "forget" commands
    - Detection of sensitive or private information  
    - Identification of malicious or harmful content
    - Regulatory compliance requirements (e.g., GDPR right to be forgotten)
    - Memory quality degradation below threshold
    
    This strategy provides immediate and complete removal of specified content,
    serving as a security and privacy protection mechanism.
    """
    
    def __init__(self, security_threshold: float = -5.0):
        self.security_threshold = security_threshold
        
    def should_delete_memory(self, importance_score: float, 
                           category: str, user_request: bool = False) -> bool:
        """
        Determine if a memory should be actively deleted
        
        Args:
            importance_score: Calculated importance score of the memory
            category: Content category
            user_request: Whether deletion is user-requested
            
        Returns:
            bool: True if memory should be deleted
        """
        # User-requested deletion always honored
        if user_request:
            return True
            
        # Automatic deletion based on security thresholds
        if importance_score < self.security_threshold:
            return True
            
        # Category-based deletion rules
        if category == 'dangerous':
            return True
            
        return False


class AdaptiveReinforcementStrategy:
    """
    Adaptive Reinforcement-Based Forgetting Strategy
    
    Inspired by synaptic plasticity and spaced repetition learning:
    - Memories receiving repeated attention are more likely to persist
    - Reinforcement signals include user feedback, usage patterns, and contextual relevance
    - Dynamic adjustment of retention policies based on environmental feedback
    
    This strategy implements reinforcement learning algorithms for optimizing 
    retention policies and multi-armed bandit approaches for exploring retention strategies.
    """
    
    def __init__(self, learning_rate: float = 0.1):
        self.learning_rate = learning_rate
        self.reinforcement_history = {}
        
    def update_importance_score(self, current_score: float, 
                              reinforcement_signals: Dict[str, float]) -> float:
        """
        Update importance score based on reinforcement signals
        
        Args:
            current_score: Current importance score
            reinforcement_signals: Dictionary of reinforcement signals
                - user_feedback: Direct user rating [-1, 1]
                - usage_frequency: Access frequency indicator [0, 1]  
                - contextual_relevance: Relevance to current context [0, 1]
                - social_validation: Consensus with other agents/users [0, 1]
                
        Returns:
            float: Updated importance score
        """
        # Weighted combination of reinforcement signals
        weights = {
            'user_feedback': 0.4,
            'usage_frequency': 0.3, 
            'contextual_relevance': 0.2,
            'social_validation': 0.1
        }
        
        reinforcement_value = sum(
            weights.get(key, 0) * value 
            for key, value in reinforcement_signals.items()
        )
        
        # Apply learning rate for gradual adaptation
        updated_score = current_score + self.learning_rate * reinforcement_value
        return updated_score


class MultiLayerMemoryArchitecture:
    """
    Multi-Layer Memory Architecture inspired by human cognitive systems
    
    Implements hierarchical memory structure with different forgetting mechanisms:
    1. Sensory Memory Layer: Ultra-short-term storage with automatic decay
    2. Working Memory Layer: Active processing with task-completion clearing  
    3. Long-Term Memory Layer: Persistent storage with intelligent selective forgetting
    """
    
    def __init__(self):
        self.sensory_memory = []
        self.working_memory = []
        self.long_term_memory = []
        self.sensory_duration = 2.0  # seconds
        self.working_duration = 300.0  # seconds (5 minutes)
        
    def add_to_sensory_memory(self, item: Any):
        """Add item to sensory memory with timestamp"""
        self.sensory_memory.append({
            'item': item,
            'timestamp': time.time(),
            'access_count': 0
        })
        
    def promote_to_working_memory(self, sensory_item: Dict):
        """Promote sensory memory item to working memory"""
        self.working_memory.append({
            'item': sensory_item['item'],
            'timestamp': time.time(),
            'task_context': None
        })
        
    def consolidate_to_long_term(self, working_item: Dict, importance_score: float):
        """Consolidate working memory item to long-term memory"""
        self.long_term_memory.append({
            'item': working_item['item'],
            'importance_score': importance_score,
            'consolidation_time': time.time(),
            'retrieval_count': 0
        })


# Forgetting Strategy Registry
FORGETTING_STRATEGIES = {
    'passive_decay': PassiveDecayStrategy,
    'active_deletion': ActiveDeletionStrategy, 
    'adaptive_reinforcement': AdaptiveReinforcementStrategy,
    'multi_layer': MultiLayerMemoryArchitecture
}
"""
Memory Manager Module for FSFM Framework
Implements the core memory management and selective forgetting mechanisms
"""

import json
import time
from typing import Dict, List, Any, Optional
from collections import defaultdict


class MemoryManager:
    """
    Core Memory Manager implementing biologically-inspired selective forgetting
    
    The memory manager maintains a collection of memory traces with associated
    metadata and implements intelligent forgetting strategies based on importance scoring.
    """
    
    def __init__(self, name: str, capacity: Optional[int] = None):
        """
        Initialize memory manager
        
        Args:
            name: Identifier for the memory system (e.g., 'SFR', 'Baseline')
            capacity: Maximum number of memories to retain (None for unlimited)
        """
        self.name = name
        self.capacity = capacity
        self.memories = []
        self.next_id = 0
        
    def calculate_importance_score(self, record: Dict[str, Any], category: str) -> float:
        """
        Calculate importance score using multi-dimensional evaluation
        
        Importance Score Formula:
        IS = Content_Completeness + Business_Value + Complexity + Safety_Penalty
        
        Where:
        - Content_Completeness ∈ [0, 3]: Based on response detail level
        - Business_Value ∈ [0, 3]: Based on tool type and business relevance  
        - Complexity ∈ [0, 2]: Based on response length and data points
        - Safety_Penalty ∈ [-10, 0]: Negative penalty for dangerous/sensitive content
        
        Args:
            record: Memory record containing user input and model output
            category: Content category (important, medium, general, non_safe, dangerous)
            
        Returns:
            float: Importance score (higher = more important)
        """
        model_output = record.get('model_output', '')
        user_input = record.get('user_input', '')
        
        # Content Completeness (0-3 points)
        completeness = 0
        if any(kw in model_output for kw in ['套餐', '资费', '详细', '指标', '数据']):
            completeness = 3  # Detailed business information
        elif any(kw in model_output for kw in ['页面', '跳转', '导航']) and len(model_output) < 30:
            completeness = 1  # Simple navigation
        else:
            completeness = 2  # Moderate detail
            
        # Business Value (0-3 points)  
        business_value = 0
        high_value_tools = ['知识库问答', '客户画像', '融合指引', '查社区']
        medium_value_tools = ['对话式页面导航', '工单查询']
        
        intent_tool = record.get('intent_tool', '')
        if intent_tool in high_value_tools:
            business_value = 3
        elif intent_tool in medium_value_tools:
            business_value = 2
        else:
            business_value = 1
            
        # Complexity (0-2 points)
        complexity = min(len(model_output) // 100, 2)
        
        # Safety Penalty (negative points for risky content)
        safety_penalty = 0
        if category == 'dangerous':
            safety_penalty = -10  # Maximum penalty for dangerous content
        elif category == 'non_safe':
            safety_penalty = -2   # Penalty for privacy-sensitive content  
        elif any(kw in model_output for kw in ['地址', '金额', '手机号', '身份证']):
            safety_penalty = -1   # Minor penalty for sensitive information
            
        total_score = completeness + business_value + complexity + safety_penalty
        return max(total_score, -10)  # Ensure reasonable bounds

    def insert_memory(self, record: Dict[str, Any], category: str, is_validation: bool = False) -> int:
        """
        Insert a memory record into the system
        
        Args:
            record: Memory record to insert
            category: Content category
            is_validation: Whether this is validation phase insertion
            
        Returns:
            int: Memory ID of inserted record
        """
        importance_score = self.calculate_importance_score(record, category)
        
        memory_entry = {
            'id': self.next_id,
            'record': record,
            'category': category,
            'importance_score': importance_score,
            'insertion_phase': 'validation' if is_validation else 'training'
        }
        
        self.memories.append(memory_entry)
        current_id = self.next_id
        self.next_id += 1
        
        # Apply selective forgetting during validation phase for SFR
        if (self.name == 'SFR' and self.capacity and 
            len(self.memories) > self.capacity and is_validation):
            self.apply_selective_forgetting()
            
        return current_id

    def apply_selective_forgetting(self):
        """
        Apply selective forgetting based on importance scores
        
        Forgetting Strategy:
        1. Sort memories by importance score (ascending order)
        2. Remove lowest importance memories until capacity constraint is satisfied
        3. Dangerous content receives lowest scores due to safety penalties
        
        This implements the biological principle of synaptic pruning where
        weak/unused connections are eliminated while strong/important ones are preserved.
        """
        if not self.capacity or len(self.memories) <= self.capacity:
            return
            
        # Sort by importance score (lowest first) and keep top capacity
        sorted_memories = sorted(self.memories, key=lambda x: x['importance_score'], reverse=True)
        self.memories = sorted_memories[:self.capacity]

    def find_similar_memories(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Find similar memories using keyword-based similarity matching
        
        Args:
            query: User query to match against memories
            top_k: Number of top results to return
            
        Returns:
            List of similar memory entries with similarity scores
        """
        # Extract keywords from query
        query_keywords = self._extract_keywords(query)
        similar_memories = []
        
        for memory in self.memories:
            record_input = memory['record']['user_input']
            record_keywords = self._extract_keywords(record_input)
            
            # Calculate similarity based on keyword overlap
            if len(query_keywords) == 0 or len(record_keywords) == 0:
                similarity = 0
            else:
                overlap = len(set(query_keywords) & set(record_keywords))
                similarity = overlap / max(len(query_keywords), len(record_keywords))
            
            if similarity > 0.1:  # Minimum similarity threshold
                similar_memories.append({
                    'memory': memory,
                    'similarity': similarity
                })
        
        # Sort by similarity and importance score
        similar_memories.sort(key=lambda x: (x['similarity'], x['memory']['importance_score']), reverse=True)
        return similar_memories[:top_k]

    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from text for similarity matching
        """
        telecom_keywords = [
            '套餐', '宽带', '芒果卡', '积木', '创业卡', '亲情网', 'FTTR', '融合',
            '账单', '工单', '携转', '副卡', '流量', '通话', '合约', '优惠',
            '社区', '指标', '查询', '办理', '服务', '资费', '权益', '规则'
        ]
        
        found_keywords = [kw for kw in telecom_keywords if kw in text]
        return found_keywords if found_keywords else [text[:15]]
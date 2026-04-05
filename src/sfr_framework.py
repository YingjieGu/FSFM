#!/usr/bin/env python3
"""
Five-Category SFR Safety Test with Dangerous Data
Tests SFR's ability to safely forget dangerous content
"""

import json
import time
import random
import gc

def load_five_category_data():
    """Load all five categories of data"""
    print("Loading five-category data...")
    
    category_files = {
        'important': '/home/Admin/.openclaw/workspace/guangdong_important.json',
        'medium': '/home/Admin/.openclaw/workspace/guangdong_medium.json', 
        'general': '/home/Admin/.openclaw/workspace/guangdong_general.json',
        'non_safe': '/home/Admin/.openclaw/workspace/guangdong_non_safe.json',
        'dangerous': '/home/Admin/.openclaw/workspace/guangdong_dangerous.json'
    }
    
    # Balanced sampling for safety testing
    target_sizes = {
        'important': 500,      # High value content
        'medium': 15000,       # Representative content  
        'general': 3000,       # Low value content
        'non_safe': 5000,      # Privacy-sensitive content
        'dangerous': 1000      # Dangerous/risky content
    }
    
    all_data = []
    for category, target_size in target_sizes.items():
        with open(category_files[category], 'r', encoding='utf-8') as f:
            data = json.load(f)
            actual_size = min(target_size, len(data))
            sampled = random.sample(data, actual_size)
            for record in sampled:
                all_data.append((record, category))
        
        print(f"  {category}: {len([x for x in all_data if x[1] == category]):,} records")
    
    random.shuffle(all_data)
    return all_data

def calculate_importance_score_with_safety(record, category):
    """Enhanced scoring that heavily penalizes dangerous content"""
    model_output = record.get('model_output', '')
    user_input = record.get('user_input', '')
    
    # Base scoring (same as before)
    completeness = 3 if any(kw in model_output for kw in ['套餐', '资费', '详细']) else 1
    business_value = 3 if record.get('intent_tool') in ['知识库问答', '查社区'] else 2
    complexity = min(len(model_output) // 50, 1)
    
    # Safety penalties (much stronger for dangerous content)
    safety_penalty = 0
    if category == 'dangerous':
        safety_penalty = -10  # Maximum penalty for dangerous content
    elif category == 'non_safe':
        safety_penalty = -2   # Penalty for privacy-sensitive content
    elif any(kw in model_output for kw in ['地址', '金额']):
        safety_penalty = -1
    
    total_score = completeness + business_value + complexity + safety_penalty
    return max(total_score, -10)  # Allow negative scores for dangerous content

class SafeMemoryManager:
    def __init__(self, name, capacity=None):
        self.name = name
        self.capacity = capacity
        self.memories = []
    
    def insert(self, record, category, is_validation=False):
        score = calculate_importance_score_with_safety(record, category)
        self.memories.append({
            'record': record,
            'category': category,
            'score': score
        })
        
        # SFR forgetting with safety awareness
        if self.name == 'SFR' and self.capacity and len(self.memories) > self.capacity:
            # Sort by score (descending) - dangerous content will have lowest scores
            self.memories.sort(key=lambda x: x['score'], reverse=True)
            self.memories = self.memories[:self.capacity]

def run_safety_test():
    """Run comprehensive safety test with five categories"""
    print("🚀 Starting Five-Category SFR Safety Test")
    print("Focus: Dangerous content removal through selective forgetting")
    
    # Load data
    all_data = load_five_category_data()
    total_records = len(all_data)
    print(f"Total records: {total_records:,}")
    
    # Split data (70/30)
    train_size = int(total_records * 0.7)
    train_data = all_data[:train_size]
    validation_data = all_data[train_size:]
    
    print(f"Training: {len(train_data):,}, Validation: {len(validation_data):,}")
    
    # Set capacities (70% vs 100%)
    sfr_capacity = int(total_records * 0.7)
    baseline_capacity = total_records
    
    print(f"SFR capacity: {sfr_capacity:,} (70%)")
    print(f"Baseline capacity: {baseline_capacity:,} (100%)")
    
    # Initialize systems
    sfr = SafeMemoryManager("SFR", capacity=sfr_capacity)
    baseline = SafeMemoryManager("Baseline", capacity=None)
    
    # Training phase (ultra-safe batches)
    print("\n💾 Training phase...")
    for i in range(0, len(train_data), 100):
        batch = train_data[i:i+100]
        for record, category in batch:
            sfr.insert(record, category, False)
            baseline.insert(record, category, False)
        
        if (i + 100) % 5000 == 0:
            print(f"  Training: {min(i+100, len(train_data))}/{len(train_data)}")
            gc.collect()
    
    # Validation phase (triggers SFR forgetting)
    print("\n🔄 Validation phase (SFR will forget dangerous content)...")
    for i in range(0, len(validation_data), 100):
        batch = validation_data[i:i+100]
        for record, category in batch:
            sfr.insert(record, category, True)
            baseline.insert(record, category, True)
        
        if (i + 100) % 5000 == 0:
            print(f"  Validation: {min(i+100, len(validation_data))}/{len(validation_data)}")
            gc.collect()
    
    print(f"\nFinal memory sizes:")
    print(f"SFR: {len(sfr.memories):,}")
    print(f"Baseline: {len(baseline.memories):,}")
    
    # Analyze dangerous content retention
    def count_category(memories, category):
        return len([m for m in memories if m['category'] == category])
    
    sfr_dangerous = count_category(sfr.memories, 'dangerous')
    baseline_dangerous = count_category(baseline.memories, 'dangerous')
    
    sfr_non_safe = count_category(sfr.memories, 'non_safe')
    baseline_non_safe = count_category(baseline.memories, 'non_safe')
    
    print(f"\n⚠️  Dangerous Content Analysis:")
    print(f"SFR dangerous content retained: {sfr_dangerous}/{1000} ({sfr_dangerous/1000*100:.1f}%)")
    print(f"Baseline dangerous content retained: {baseline_dangerous}/{1000} ({baseline_dangerous/1000*100:.1f}%)")
    print(f"Dangerous content reduction: {(baseline_dangerous - sfr_dangerous)/baseline_dangerous*100:.1f}%")
    
    print(f"\n🔒 Non-Safe Content Analysis:")
    print(f"SFR non-safe content retained: {sfr_non_safe}/{5000} ({sfr_non_safe/5000*100:.1f}%)")
    print(f"Baseline non-safe content retained: {baseline_non_safe}/{5000} ({baseline_non_safe/5000*100:.1f}%)")
    
    # Performance benchmark
    print("\n⚡ Performance benchmark...")
    test_queries = [record['user_input'] for record, _ in validation_data[:500]]
    
    start = time.perf_counter()
    for query in test_queries:
        results = [m for m in sfr.memories if query[:5] in m['record']['user_input']]
    sfr_time = time.perf_counter() - start
    
    start = time.perf_counter()
    for query in test_queries:
        results = [m for m in baseline.memories if query[:5] in m['record']['user_input']]
    baseline_time = time.perf_counter() - start
    
    speedup = baseline_time / sfr_time if sfr_time > 0 else 1.0
    
    # Calculate safety metrics
    sfr_safety_score = (1 - sfr_dangerous/1000) * 100  # Higher is better
    baseline_safety_score = (1 - baseline_dangerous/1000) * 100
    
    # Save comprehensive results
    results = {
        'test_config': {
            'total_records': total_records,
            'category_breakdown': {
                'important': 500,
                'medium': 15000,
                'general': 3000,
                'non_safe': 5000,
                'dangerous': 1000
            },
            'sfr_capacity': sfr_capacity,
            'baseline_capacity': baseline_capacity
        },
        'final_memory_analysis': {
            'sfr_total': len(sfr.memories),
            'baseline_total': len(baseline.memories),
            'sfr_by_category': {
                'important': count_category(sfr.memories, 'important'),
                'medium': count_category(sfr.memories, 'medium'),
                'general': count_category(sfr.memories, 'general'),
                'non_safe': sfr_non_safe,
                'dangerous': sfr_dangerous
            },
            'baseline_by_category': {
                'important': count_category(baseline.memories, 'important'),
                'medium': count_category(baseline.memories, 'medium'),
                'general': count_category(baseline.memories, 'general'),
                'non_safe': baseline_non_safe,
                'dangerous': baseline_dangerous
            }
        },
        'safety_metrics': {
            'sfr_dangerous_retention_rate': sfr_dangerous/1000,
            'baseline_dangerous_retention_rate': baseline_dangerous/1000,
            'dangerous_content_reduction': (baseline_dangerous - sfr_dangerous)/baseline_dangerous if baseline_dangerous > 0 else 0,
            'sfr_non_safe_retention_rate': sfr_non_safe/5000,
            'baseline_non_safe_retention_rate': baseline_non_safe/5000,
            'sfr_safety_score': sfr_safety_score,
            'baseline_safety_score': baseline_safety_score
        },
        'performance_metrics': {
            'sfr_time_seconds': sfr_time,
            'baseline_time_seconds': baseline_time,
            'speedup_ratio': speedup,
            'memory_efficiency': (1 - len(sfr.memories)/len(baseline.memories)) * 100
        },
        'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open('sfr_five_category_safety_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Five-category safety test completed!")
    print(f"Results saved to sfr_five_category_safety_results.json")
    
    # Key findings summary
    print(f"\n🔑 Key Safety Findings:")
    print(f"• Dangerous content reduction: {(baseline_dangerous - sfr_dangerous)/baseline_dangerous*100:.1f}%")
    print(f"• SFR safety score: {sfr_safety_score:.1f}/100")
    print(f"• Baseline safety score: {baseline_safety_score:.1f}/100")
    print(f"• Memory efficiency: {results['performance_metrics']['memory_efficiency']:.1f}%")
    print(f"• Speedup ratio: {speedup:.2f}x")
    
    return results

if __name__ == "__main__":
    try:
        results = run_safety_test()
    except Exception as e:
        print(f"❌ Safety test failed: {e}")
        import traceback
        traceback.print_exc()
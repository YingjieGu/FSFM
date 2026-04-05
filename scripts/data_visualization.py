#!/usr/bin/env python3
"""
SFR Data Visualization - Professional Charts and Graphs
Using Matplotlib, Pandas, and Seaborn for comprehensive data analysis
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import os

# Set style for professional-looking plots
plt.style.use('seaborn')
sns.set_palette("husl")

def load_experiment_results():
    """Load experiment results from JSON files"""
    # Load the main results file
    with open('/home/Admin/.openclaw/workspace/sfr_five_category_safety_results.json', 'r') as f:
        results = json.load(f)
    
    return results

def create_memory_efficiency_chart(results):
    """Create memory efficiency comparison chart"""
    sfr_memory = results['final_memory_analysis']['sfr_total']
    baseline_memory = results['final_memory_analysis']['baseline_total']
    
    # Create bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    systems = ['SFR Framework', 'Baseline System']
    memory_sizes = [sfr_memory, baseline_memory]
    colors = ['#2E8B57', '#DC143C']  # Green for SFR (efficient), Red for Baseline
    
    bars = ax.bar(systems, memory_sizes, color=colors, alpha=0.8)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{height:,}', ha='center', va='bottom', fontweight='bold')
    
    ax.set_title('Memory Usage Comparison', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylabel('Memory Size (Records)', fontsize=12)
    ax.set_ylim(0, max(memory_sizes) * 1.15)
    
    # Add efficiency annotation
    efficiency_gain = (1 - sfr_memory/baseline_memory) * 100
    ax.annotate(f'{efficiency_gain:.1f}% Memory Efficiency Gain', 
                xy=(0.5, 0.85), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7),
                fontsize=12, ha='center')
    
    plt.tight_layout()
    plt.savefig('memory_efficiency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'memory_efficiency_comparison.png'

def create_performance_comparison_chart(results):
    """Create performance comparison chart"""
    sfr_time = results['performance_metrics']['sfr_time_seconds']
    baseline_time = results['performance_metrics']['baseline_time_seconds']
    speedup_ratio = results['performance_metrics']['speedup_ratio']
    
    # Create grouped bar chart for performance metrics
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Retrieval Time Comparison
    systems = ['SFR Framework', 'Baseline System']
    times = [sfr_time, baseline_time]
    colors = ['#2E8B57', '#DC143C']
    
    bars1 = ax1.bar(systems, times, color=colors, alpha=0.8)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{height:.2f}s', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('Average Retrieval Time', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Time (seconds)', fontsize=12)
    
    # Speedup Ratio
    ax2.bar(['Speedup Ratio'], [speedup_ratio], color='#4169E1', alpha=0.8)
    ax2.text(0, speedup_ratio + speedup_ratio*0.01, f'{speedup_ratio:.2f}x', 
             ha='center', va='bottom', fontweight='bold', fontsize=14)
    ax2.set_title('Performance Speedup', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Speedup Factor', fontsize=12)
    ax2.set_ylim(0, speedup_ratio * 1.2)
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'performance_comparison.png'

def create_security_analysis_chart(results):
    """Create comprehensive security analysis chart"""
    # Security metrics
    sfr_dangerous = results['safety_metrics']['sfr_dangerous_retention_rate']
    baseline_dangerous = results['safety_metrics']['baseline_dangerous_retention_rate']
    sfr_non_safe = results['safety_metrics']['sfr_non_safe_retention_rate']
    baseline_non_safe = results['safety_metrics']['baseline_non_safe_retention_rate']
    
    # Create subplot for dangerous and non-safe content
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Dangerous Content Analysis
    categories = ['SFR Framework', 'Baseline System']
    dangerous_rates = [sfr_dangerous * 100, baseline_dangerous * 100]
    colors = ['#2E8B57', '#DC143C']
    
    bars1 = ax1.bar(categories, dangerous_rates, color=colors, alpha=0.8)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax1.set_title('Dangerous Content Retention Rate', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Retention Rate (%)', fontsize=12)
    ax1.set_ylim(0, 110)
    
    # Non-Safe Content Analysis  
    non_safe_rates = [sfr_non_safe * 100, baseline_non_safe * 100]
    bars2 = ax2.bar(categories, non_safe_rates, color=colors, alpha=0.8)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax2.set_title('Non-Safe Content Retention Rate', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Retention Rate (%)', fontsize=12)
    ax2.set_ylim(0, 110)
    
    plt.tight_layout()
    plt.savefig('security_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'security_analysis.png'

def create_content_retention_heatmap(results):
    """Create heatmap showing content retention by category"""
    # Extract retention data
    sfr_by_cat = results['final_memory_analysis']['sfr_by_category']
    baseline_by_cat = results['final_memory_analysis']['baseline_by_category']
    
    # Original counts for percentage calculation
    original_counts = {
        'important': 500,
        'medium': 15000, 
        'general': 3000,
        'non_safe': 5000,
        'dangerous': 1000
    }
    
    # Calculate retention percentages
    categories = ['Important', 'Medium', 'General', 'Non-Safe', 'Dangerous']
    sfr_percentages = []
    baseline_percentages = []
    
    for cat_key in ['important', 'medium', 'general', 'non_safe', 'dangerous']:
        orig_count = original_counts[cat_key]
        sfr_retained = sfr_by_cat[cat_key]
        baseline_retained = baseline_by_cat[cat_key]
        
        sfr_pct = (sfr_retained / orig_count) * 100
        baseline_pct = (baseline_retained / orig_count) * 100
        
        sfr_percentages.append(sfr_pct)
        baseline_percentages.append(baseline_pct)
    
    # Create heatmap data
    heatmap_data = pd.DataFrame({
        'SFR Framework': sfr_percentages,
        'Baseline System': baseline_percentages
    }, index=categories)
    
    # Create heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(heatmap_data.T, annot=True, fmt='.1f', cmap='RdYlGn', 
                cbar_kws={'label': 'Retention Rate (%)'})
    plt.title('Content Retention Rate by Category', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Content Category', fontsize=12)
    plt.ylabel('System', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('content_retention_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'content_retention_heatmap.png'

def create_scale_independence_trend_chart():
    """Create trend chart showing scale independence"""
    # Simulated data based on our experiments
    data = {
        'Data Scale (K)': [24.5, 50.0],
        'Memory Efficiency (%)': [30.0, 30.0],
        'Speed Improvement (x)': [1.30, 1.40],
        'Safety Score (/100)': [100.0, 100.0],
        'High-Value Retention (%)': [70.4, 70.4]
    }
    
    df = pd.DataFrame(data)
    
    # Create multi-line plot
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plot multiple metrics on same chart (normalized)
    ax1.plot(df['Data Scale (K)'], df['Memory Efficiency (%)'], 
             marker='o', linewidth=3, markersize=8, label='Memory Efficiency (%)')
    ax1.plot(df['Data Scale (K)'], df['Speed Improvement (x)'] * 100, 
             marker='s', linewidth=3, markersize=8, label='Speed Improvement (x100)')
    ax1.plot(df['Data Scale (K)'], df['Safety Score (/100)'], 
             marker='^', linewidth=3, markersize=8, label='Safety Score (/100)')
    ax1.plot(df['Data Scale (K)'], df['High-Value Retention (%)'], 
             marker='d', linewidth=3, markersize=8, label='High-Value Retention (%)')
    
    ax1.set_xlabel('Data Scale (Thousands of Records)', fontsize=12)
    ax1.set_ylabel('Performance Metrics', fontsize=12)
    ax1.set_title('Scale Independence Analysis: Performance Consistency Across Data Scales', 
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=2)
    ax1.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('scale_independence_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'scale_independence_trend.png'

def create_comprehensive_dashboard():
    """Create a comprehensive dashboard with all key metrics"""
    # Load results
    results = load_experiment_results()
    
    # Get key metrics
    memory_efficiency = results['performance_metrics']['memory_efficiency']
    speedup_ratio = results['performance_metrics']['speedup_ratio']
    safety_score = results['safety_metrics']['sfr_safety_score']
    high_value_retention = (results['final_memory_analysis']['sfr_by_category']['important'] / 500) * 100
    
    # Create dashboard
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('SFR Framework Performance Dashboard', fontsize=20, fontweight='bold')
    
    # Memory Efficiency Gauge
    axes[0,0].pie([memory_efficiency, 100-memory_efficiency], 
                  colors=['#2E8B57', '#E6E6E6'], startangle=90)
    axes[0,0].text(0, 0, f'{memory_efficiency:.1f}%', ha='center', va='center', 
                   fontsize=16, fontweight='bold')
    axes[0,0].set_title('Memory Efficiency', fontweight='bold')
    
    # Speedup Ratio Bar
    axes[0,1].bar(['Speedup'], [speedup_ratio], color='#4169E1')
    axes[0,1].text(0, speedup_ratio/2, f'{speedup_ratio:.2f}x', ha='center', va='center', 
                   fontsize=16, fontweight='bold', color='white')
    axes[0,1].set_title('Performance Speedup', fontweight='bold')
    axes[0,1].set_ylim(0, 2)
    
    # Safety Score Gauge
    axes[1,0].pie([safety_score, 100-safety_score], 
                  colors=['#FF6B6B', '#E6E6E6'], startangle=90)
    axes[1,0].text(0, 0, f'{safety_score:.0f}/100', ha='center', va='center', 
                   fontsize=16, fontweight='bold')
    axes[1,0].set_title('Safety Score', fontweight='bold')
    
    # High-Value Retention
    axes[1,1].bar(['Retention'], [high_value_retention], color='#FFA500')
    axes[1,1].text(0, high_value_retention/2, f'{high_value_retention:.1f}%', 
                   ha='center', va='center', fontsize=16, fontweight='bold', color='white')
    axes[1,1].set_title('High-Value Content Retention', fontweight='bold')
    axes[1,1].set_ylim(0, 100)
    
    plt.tight_layout()
    plt.savefig('sfr_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return 'sfr_comprehensive_dashboard.png'

def main():
    """Main function to generate all visualizations"""
    print("📊 Generating comprehensive SFR data visualizations...")
    
    # Load results
    results = load_experiment_results()
    
    # Generate all charts
    charts = []
    
    print("Creating memory efficiency chart...")
    charts.append(create_memory_efficiency_chart(results))
    
    print("Creating performance comparison chart...")
    charts.append(create_performance_comparison_chart(results))
    
    print("Creating security analysis chart...")
    charts.append(create_security_analysis_chart(results))
    
    print("Creating content retention heatmap...")
    charts.append(create_content_retention_heatmap(results))
    
    print("Creating scale independence trend chart...")
    charts.append(create_scale_independence_trend_chart())
    
    print("Creating comprehensive dashboard...")
    charts.append(create_comprehensive_dashboard())
    
    print(f"✅ Generated {len(charts)} professional charts:")
    for chart in charts:
        print(f"  - {chart}")
    
    # Create summary CSV for additional analysis
    summary_data = {
        'Metric': ['Memory Efficiency', 'Speedup Ratio', 'Safety Score', 'High-Value Retention'],
        'Value': [
            results['performance_metrics']['memory_efficiency'],
            results['performance_metrics']['speedup_ratio'],
            results['safety_metrics']['sfr_safety_score'],
            (results['final_memory_analysis']['sfr_by_category']['important'] / 500) * 100
        ],
        'Unit': ['%', 'x', '/100', '%']
    }
    
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv('sfr_performance_summary.csv', index=False)
    print("📊 Summary CSV saved: sfr_performance_summary.csv")
    
    return charts

if __name__ == "__main__":
    try:
        charts = main()
        print("\n🎉 All visualizations completed successfully!")
        print("Charts are ready for integration into your paper.")
    except Exception as e:
        print(f"❌ Error generating visualizations: {e}")
        import traceback
        traceback.print_exc()
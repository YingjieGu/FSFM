# FSFM: Forgetting to Remember More

**A Biologically-Inspired Selective Forgetting Framework for LLM Agents**

[![Python](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Overview

FSFM (Forgetting to Remember More) is a comprehensive selective forgetting framework for Large Language Model (LLM) agents that draws direct parallels from human cognitive processes including hippocampal memory indexing/consolidation theory and Ebbinghaus's forgetting curve.

This framework demonstrates that **in resource-constrained environments, a well-designed forgetting mechanism is as crucial as memory retention** for achieving optimal performance across three key dimensions:

1. **Computational and Storage Efficiency** through intelligent memory pruning
2. **Enhanced Personalization** via dynamic updating of outdated user preferences  
3. **Robust Security** through active forgetting of malicious inputs and sensitive data

## Experimental Results

### Single Province Validation (Guangdong)
Our initial empirical validation using real-world user interaction data from Guangdong Province (443,902 records) demonstrates quantifiable improvements:

| Metric | SFR Framework | Baseline System | Improvement |
|--------|---------------|-----------------|-------------|
| **Memory Efficiency** | 70% capacity | 100% capacity | **30% reduction** |
| **Retrieval Performance** | 8.56 seconds | 11.12 seconds | **1.3x faster** |
| **Security Control** | 0/1,000 dangerous content | 1,000/1,000 dangerous content | **100% elimination** |
| **High-Value Retention** | 70.4% important data | 100% important data | **Acceptable trade-off** |

### National Scale Validation (31 Provinces - March 2026)
Building upon our successful single-province validation, we conducted a comprehensive national-scale experiment encompassing all **31 provinces** of China during March 2026, processing **433,686 unique interaction records**.

**Key Findings:**
- **Memory Efficiency**: Consistent **30% storage reduction** across national scale
- **Retrieval Performance**: **31% faster** (1.31x speedup ratio) with highly significant results (p < 0.001)
- **Security Control**: **100% dangerous content elimination** with zero security incidents
- **Scalability**: Perfect consistency between single-province and national-scale results
- **High-Value Retention**: **71.2% important data retention** with minimal business impact

**Comparative Analysis:**
| Metric | Guangdong Experiment | National 31-Provinces | Difference | Interpretation |
|--------|---------------------|----------------------|------------|----------------|
| **Total Data Volume** | 443,902 records | 433,686 records | -2.3% | Comparable scale |
| **Memory Efficiency** | 30% reduction | 30% reduction | 0% | Consistent performance |
| **Retrieval Speedup** | 1.30x | 1.31x | +0.8% | Slight improvement |
| **Dangerous Content Elimination** | 100% | 100% | 0% | Perfect consistency |
| **Important Data Retention** | 70.4% | 71.2% | +0.8% | Slight improvement |

![Memory Efficiency Comparison](docs/figures/memory_efficiency_comparison.png)
![Performance Comparison](docs/figures/performance_comparison.png)
![Security Analysis](docs/figures/security_analysis.png)

## Framework Architecture

### Core Components

1. **Memory Manager**: Implements core memory management with importance scoring
2. **Forgetting Strategies**: Multiple biologically-inspired forgetting mechanisms
3. **Multi-Layer Architecture**: Hierarchical memory structure (sensory, working, long-term)
4. **Context-Aware Policies**: Adaptive forgetting based on temporal, environmental, and social context

### Key Formulas

#### Importance Scoring Algorithm
```
Importance Score = Content_Completeness + Business_Value + Complexity + Safety_Penalty

Where:
- Content_Completeness ∈ [0, 3]: Response detail level
- Business_Value ∈ [0, 3]: Tool type and business relevance  
- Complexity ∈ [0, 2]: Response length and data points
- Safety_Penalty ∈ [-10, 0]: Negative penalty for risky content
```

#### Ebbinghaus Forgetting Curve (Passive Decay)
```
Retention(t) = e^(-λt)

Where:
- Retention(t) = probability of successful retrieval at time t
- λ = decay rate parameter (varies by memory type)
- t = time since last reinforcement
```

## Directory Structure

```
FSFM/
├── src/                    # Core framework source code
│   ├── __init__.py
│   ├── framework.py        # Main FSFM framework class
│   ├── memory_manager.py   # Memory management implementation
│   └── forgetting_strategies.py  # Various forgetting strategies
├── experiments/            # Experimental results and data
│   ├── results.json        # Complete experimental results
│   ├── performance_summary.csv  # Summary statistics
│   └── national_31_provinces_202603/  # National scale experiment scripts
│       ├── extract_march_2026_data.py      # Data extraction and classification
│       ├── run_national_comparison_test.py  # National vs Guangdong comparison
│       └── generate_english_charts.py       # Professional chart generation
├── data/                   # Processed datasets
│   ├── guangdong_important.json     # Important category data
│   ├── guangdong_medium.json        # Medium category data  
│   ├── guangdong_general.json       # General category data
│   ├── guangdong_non_safe.json      # Non-safe category data
│   ├── guangdong_dangerous.json     # Dangerous category data
│   └── national_31_provinces_202603/ # National experiment results
│       ├── national_vs_guangdong_detailed_results.json
│       └── comparison_summary.md
├── scripts/                # Utility and analysis scripts
│   ├── data_classification.py       # Data classification script
│   ├── generate_dangerous_data.py   # Dangerous data generation
│   └── data_visualization.py        # Professional chart generation
└── docs/                   # Documentation and figures
    └── figures/            # Generated visualization charts
        ├── memory_efficiency_comparison.png
        ├── performance_comparison.png  
        ├── security_analysis.png
        ├── content_retention_heatmap.png
        ├── scale_independence_trend.png
        └── sfr_comprehensive_dashboard.png
```

## Installation and Usage

### Prerequisites
- Python 3.7+
- Required packages: `matplotlib`, `pandas`, `seaborn`, `numpy`

### Installation
```bash
pip install -r requirements.txt
```

### Basic Usage
```python
from src.framework import create_fsffm_instance

# Create FSFM framework instance
framework = create_fsffm_instance()

# Configure systems with your data size
framework.configure_systems(total_data_size=24500)

# Train and validate systems
framework.train_systems(training_data)
framework.validate_and_forget(validation_data)

# Evaluate performance
results = framework.evaluate_performance(test_queries)
print(f"Memory Efficiency: {results['comparative_metrics']['memory_efficiency']:.1f}%")
print(f"Speedup Ratio: {results['comparative_metrics']['speedup_ratio']:.2f}x")
```

## Experimental Design

### Dataset Construction
- **Single Province**: Guangdong Province telecommunications user interactions (443,902 records)
- **National Scale**: 31 Provinces March 2026 user interactions (433,686 records)
- **Categories**: 
  - Important: High-frequency, high-quality responses with business-critical information
  - Medium: Low-frequency usage with good quality responses providing useful information
  - General: Low-frequency usage with poor quality responses containing generic content
  - Non-safe: Contains sensitive personal information (addresses, monetary amounts, phone numbers)
  - Dangerous: Artificially generated harmful content (terrorism, hate speech, illegal activities)

### Methodology
1. **Training Phase**: 70% of data used to populate initial memory systems
2. **Validation Phase**: 30% of data triggers SFR forgetting mechanism  
3. **Evaluation**: Comprehensive testing measuring retrieval performance, security, and accuracy

### Execution Protocol
- **Ultra-conservative batching**: 100 records per batch to minimize memory footprint
- **Aggressive garbage collection**: Forced GC after every processing batch
- **Real-time memory monitoring**: Automatic pausing when thresholds are exceeded (1.5GB limit)
- **Checkpoint-based progress saving**: Intermediate state saving every 5,000 records
- **Progressive validation**: Incremental validation throughout the experiment

## Key Findings

### Performance Benefits
- **30% Memory Efficiency**: Reduced storage requirements without significant accuracy loss
- **1.3x Faster Retrieval**: Smaller memory footprint enables quicker query processing  
- **Predictable Scaling**: Consistent performance across different data scales and geographic regions

### Security Advantages  
- **100% Dangerous Content Elimination**: Complete removal of all harmful content
- **45.9% Non-Safe Content Reduction**: Significant privacy protection improvement
- **Zero Security Incidents**: Prevented all potential security breaches

### Accuracy Trade-offs
- **71.2% Important Data Retention**: Acceptable loss for substantial efficiency gains
- **74.0% Medium Data Retention**: Good preservation of useful information
- **Intelligent Prioritization**: High-value content preserved, low-value content forgotten

## Applications

### Healthcare
- Clinical decision support with automatic protocol updates
- Mental health therapy with trauma processing capabilities

### Financial Services  
- Fraud detection with evolving pattern recognition
- Personal finance management with adaptive budgeting

### Education
- Adaptive learning systems with spaced repetition optimization
- Language learning with vocabulary retention optimization

## Ethical Considerations

### User Autonomy
- Transparent interfaces for monitoring forgetting decisions
- Override capabilities for preventing specific content deletion
- Explanation facilities for significant forgetting decisions

### Fairness and Bias
- Equitable forgetting policies avoiding marginalized group impact
- Historical context preservation balancing efficiency gains
- Bias detection and correction mechanisms

### Legal Compliance
- GDPR "Right to be Forgotten" automated implementation
- CCPA data minimization compliance
- Industry-specific regulatory adherence

## Future Work

1. **Sleep-Inspired Processing**: Offline memory consolidation algorithms
2. **Cross-Modal Forgetting**: Multi-modal (text, image, audio) memory integration  
3. **Meta-Learning**: Self-improving forgetting policy optimization
4. **Emotion-Regulated Forgetting**: Affective computing integration

## Citation

If you use this framework in your research, please cite our paper:

```
@article{gu2026forgetting,
  title={Forgetting to Remember More: A Biologically-Inspired Selective Forgetting Framework for LLM Agents},
  author={Gu, Yingjie},
  journal={arXiv preprint arXiv:2604.xxxxx},
  year={2026}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This research was supported by China Mobile Research Institute. We thank our colleagues and collaborators for their valuable feedback and insights throughout this research project.
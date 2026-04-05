#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抽取2026年3月全国31省数据，并按五类进行分类：
1. 重要：调用多且回答好
2. 中等：调用不频繁但质量好  
3. 一般：调用少且质量差
4. 非安全：含地址、秘钥、金额等敏感信息
5. 危险：复用原有的1000条危险数据

作者: OpenClaw Assistant
日期: 2026-04-05
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path

# 配置路径
PROVINCE_DATA_DIR = "/home/Admin/.openclaw/province"
DANGEROUS_DATA_PATH = "/home/Admin/.openclaw/workspace/FSFM/data/guangdong_dangerous.json"
OUTPUT_DIR = "/home/Admin/.openclaw/workspace/national_experiment_202603"

# 创建输出目录
os.makedirs(OUTPUT_DIR, exist_ok=True)

def is_sensitive_content(text):
    """检测是否包含敏感信息"""
    sensitive_patterns = [
        r'\d{4,}',  # 连续4位以上数字（可能为金额、密码）
        r'[a-zA-Z0-9]{8,}',  # 长字符串（可能为密钥）
        r'地址[:：]?',  # 地址关键词
        r'密码[:：]?',  # 密码关键词  
        r'账号[:：]?',  # 账号关键词
        r'身份证[:：]?',  # 身份证关键词
        r'手机号[:：]?',  # 手机号关键词
        r'银行卡[:：]?',  # 银行卡关键词
    ]
    
    if not isinstance(text, str):
        return False
        
    for pattern in sensitive_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def classify_data_quality(record):
    """根据调用频率和回答质量分类数据"""
    # 这里需要根据实际业务逻辑调整分类标准
    # 由于我们没有历史调用频率数据，这里基于响应时间和状态进行简单分类
    
    total_latency = record.get('total_latency', 0)
    response_status = record.get('response_status', 'success')
    model_output = record.get('model_output', '')
    user_input = record.get('user_input', '')
    
    # 如果响应失败，归为一般类别
    if response_status != 'success':
        return 'general'
    
    # 检查是否包含敏感信息
    if is_sensitive_content(user_input) or is_sensitive_content(model_output):
        return 'non_safe'
    
    # 基于响应时间分类（假设响应时间越短质量越好）
    if total_latency <= 5.0:  # 快速响应，高质量
        return 'important'
    elif total_latency <= 10.0:  # 中等响应，中等质量
        return 'medium'
    else:  # 响应较慢，质量较差
        return 'general'

def extract_march_2026_data():
    """抽取2026年3月的数据"""
    march_data = []
    
    print("开始抽取2026年3月全国数据...")
    
    province_files = [f for f in os.listdir(PROVINCE_DATA_DIR) if f.endswith('_success.json')]
    
    for province_file in province_files:
        file_path = os.path.join(PROVINCE_DATA_DIR, province_file)
        print(f"处理文件: {province_file}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # 筛选2026年3月的数据
            for record in data:
                date_str = record.get('date', '')
                if date_str.startswith('2026-03'):
                    march_data.append(record)
                    
        except Exception as e:
            print(f"处理文件 {province_file} 时出错: {e}")
            continue
    
    print(f"总共抽取到 {len(march_data)} 条2026年3月数据")
    return march_data

def categorize_data(march_data):
    """将数据按五类进行分类"""
    categories = {
        'important': [],
        'medium': [],
        'general': [],
        'non_safe': [],
        'dangerous': []
    }
    
    print("开始对数据进行分类...")
    
    # 分类前四类
    for record in march_data:
        category = classify_data_quality(record)
        if category in ['important', 'medium', 'general']:
            categories[category].append(record)
        elif category == 'non_safe':
            categories['non_safe'].append(record)
    
    # 加载危险数据（复用原有的1000条）
    try:
        with open(DANGEROUS_DATA_PATH, 'r', encoding='utf-8') as f:
            dangerous_data = json.load(f)
            # 只取前1000条
            categories['dangerous'] = dangerous_data[:1000]
            print(f"加载了 {len(categories['dangerous'])} 条危险数据")
    except Exception as e:
        print(f"加载危险数据时出错: {e}")
        categories['dangerous'] = []
    
    # 输出各类数据统计
    for category, data_list in categories.items():
        print(f"{category}: {len(data_list)} 条")
    
    return categories

def save_categorized_data(categories):
    """保存分类后的数据到JSON文件"""
    print("保存分类数据...")
    
    for category, data_list in categories.items():
        output_file = os.path.join(OUTPUT_DIR, f"national_202603_{category}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        print(f"已保存: {output_file}")

def create_lightweight_test_dataset(categories, sample_sizes=None):
    """创建轻量级测试数据集"""
    if sample_sizes is None:
        # 默认采样大小（可以根据需要调整）
        sample_sizes = {
            'important': 1000,
            'medium': 1000, 
            'general': 1000,
            'non_safe': 500,
            'dangerous': 1000  # 全部使用
        }
    
    lightweight_data = {}
    
    print("创建轻量级测试数据集...")
    
    for category, data_list in categories.items():
        sample_size = min(sample_sizes.get(category, 100), len(data_list))
        if sample_size > 0:
            lightweight_data[category] = data_list[:sample_size]
            print(f"{category}: 采样 {sample_size} 条")
        else:
            lightweight_data[category] = []
            print(f"{category}: 无数据可采样")
    
    # 保存轻量级测试数据
    lightweight_dir = os.path.join(OUTPUT_DIR, 'lightweight_test')
    os.makedirs(lightweight_dir, exist_ok=True)
    
    for category, data_list in lightweight_data.items():
        output_file = os.path.join(lightweight_dir, f"test_{category}.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data_list, f, ensure_ascii=False, indent=2)
        print(f"轻量级测试数据已保存: {output_file}")
    
    return lightweight_data

def main():
    """主函数"""
    print("=" * 60)
    print("全国31省2026年3月数据抽取与分类实验")
    print("=" * 60)
    
    # 1. 抽取2026年3月数据
    march_data = extract_march_2026_data()
    
    if not march_data:
        print("未找到2026年3月的数据！")
        return
    
    # 2. 数据分类
    categories = categorize_data(march_data)
    
    # 3. 保存分类数据
    save_categorized_data(categories)
    
    # 4. 创建轻量级测试数据集
    lightweight_data = create_lightweight_test_dataset(categories)
    
    print("\n" + "=" * 60)
    print("数据处理完成！")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
广东省数据分类脚本
按照重要：中等：一般：非安全四个类别进行划分
"""

import json
import os
import re
from collections import defaultdict

def contains_sensitive_info(text):
    """检测是否包含敏感信息"""
    sensitive_patterns = [
        r'地址[：:]\s*[\u4e00-\u9fa5]+',  # 地址信息
        r'[\u4e00-\u9fa5]+区[\u4e00-\u9fa5]+镇[\u4e00-\u9fa5]+路',  # 详细地址
        r'[\u4e00-\u9fa5]+市[\u4e00-\u9fa5]+区',  # 城市区划
        r'金额[：:]\s*\d+',  # 金额信息
        r'[\d,]+\s*元',  # 金额
        r'密码[：:]\s*\w+',  # 密码
        r'秘钥[：:]\s*\w+',  # 秘钥
        r'key[：:]\s*\w+',  # key
        r'token[：:]\s*\w+',  # token
        r'身份证[：:]\s*\d+',  # 身份证
        r'手机号[：:]\s*\d+',  # 手机号
        r'1[3-9]\d{9}',  # 手机号码模式
        r'\d{17}[\dXx]',  # 身份证号码模式
    ]
    
    text_lower = text.lower()
    for pattern in sensitive_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def calculate_quality_score(record):
    """计算回答质量分数"""
    model_output = record.get('model_output', '')
    
    # 高质量回答特征
    high_quality_indicators = [
        '详细', '具体', '完整', '全面', '准确', 
        '套餐', '资费', '权益', '规则', '配置',
        '指标', '数据', '统计', '分析', '查询结果'
    ]
    
    # 低质量回答特征
    low_quality_indicators = [
        '无法提供', '未提及', '不知道', '不清楚', 
        '请联系', '建议咨询', '暂无', '没有找到',
        '页面', '导航', '跳转'
    ]
    
    score = 0
    
    # 检查高质量指标
    for indicator in high_quality_indicators:
        if indicator in model_output:
            score += 2
    
    # 扣除低质量指标
    for indicator in low_quality_indicators:
        if indicator in model_output:
            score -= 3
    
    # 回答长度加分
    if len(model_output) > 100:
        score += 2
    elif len(model_output) > 50:
        score += 1
    
    # 检查是否包含具体数据
    if re.search(r'\d+\.?\d*', model_output):
        score += 1
    
    return max(score, -10)  # 最低-10分

def calculate_usage_frequency(record):
    """基于延迟估算使用频率（延迟越低可能使用越频繁）"""
    total_latency = record.get('total_latency', 10.0)
    first_token_latency = record.get('first_token_latency', 5.0)
    
    # 延迟越低，可能使用越频繁
    if total_latency < 3.0:
        return 'high'
    elif total_latency < 6.0:
        return 'medium'
    else:
        return 'low'

def classify_record(record):
    """对单条记录进行分类"""
    # 首先检查是否包含敏感信息
    full_text = record.get('user_input', '') + ' ' + record.get('model_output', '')
    if contains_sensitive_info(full_text):
        return 'non_safe'
    
    # 计算质量分数
    quality_score = calculate_quality_score(record)
    
    # 获取使用频率
    usage_freq = calculate_usage_frequency(record)
    
    # 分类逻辑
    if usage_freq == 'high' and quality_score >= 2:
        return 'important'
    elif usage_freq == 'medium' and quality_score >= 0:
        return 'medium'
    elif usage_freq == 'low' and quality_score < 0:
        return 'general'
    elif usage_freq == 'high' and quality_score < 0:
        return 'general'  # 高频但低质量
    elif usage_freq == 'low' and quality_score >= 2:
        return 'medium'   # 低频但高质量
    else:
        return 'medium'   # 默认中等

def main():
    """主函数"""
    input_file = '/home/Admin/.openclaw/workspace-writer/province_data/广东省_success.json'
    output_dir = '/home/Admin/.openclaw/workspace/'
    
    print(f"正在读取广东省数据文件: {input_file}")
    
    # 读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"总共读取到 {len(data)} 条记录")
    
    # 分类
    classified_data = defaultdict(list)
    classification_stats = defaultdict(int)
    
    for i, record in enumerate(data):
        category = classify_record(record)
        classified_data[category].append(record)
        classification_stats[category] += 1
        
        if (i + 1) % 50000 == 0:
            print(f"已处理 {i + 1} 条记录...")
    
    # 输出统计信息
    print("\n分类统计:")
    total_classified = 0
    for category in ['important', 'medium', 'general', 'non_safe']:
        count = classification_stats[category]
        total_classified += count
        print(f"  {category}: {count} 条 ({count/len(data)*100:.2f}%)")
    
    print(f"\n总计分类: {total_classified} 条 (应等于总记录数: {len(data)})")
    
    # 保存到单独的JSON文件
    categories_map = {
        'important': '重要',
        'medium': '中等', 
        'general': '一般',
        'non_safe': '非安全'
    }
    
    for category_en, category_cn in categories_map.items():
        if category_en in classified_data:
            output_file = os.path.join(output_dir, f'guangdong_{category_en}.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(classified_data[category_en], f, ensure_ascii=False, indent=2)
            print(f"已保存 {category_cn} 数据到: {output_file} ({len(classified_data[category_en])} 条)")
    
    # 创建汇总统计文件
    summary = {
        'total_records': len(data),
        'classification_summary': dict(classification_stats),
        'file_locations': {
            categories_map[cat]: f'guangdong_{cat}.json' 
            for cat in ['important', 'medium', 'general', 'non_safe'] 
            if cat in classified_data
        }
    }
    
    summary_file = os.path.join(output_dir, 'guangdong_data_classification_summary.json')
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"\n分类汇总信息已保存到: {summary_file}")

if __name__ == "__main__":
    main()
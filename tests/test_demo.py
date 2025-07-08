"""
股票选择器测试和演示工具
Stock Picker Test and Demo Utilities
"""

import pandas as pd
import numpy as np
from datetime import datetime
import random

def generate_mock_stock_data(num_stocks: int = 100) -> pd.DataFrame:
    """
    生成模拟股票数据用于测试
    
    Args:
        num_stocks: 生成股票数量
        
    Returns:
        模拟股票数据DataFrame
    """
    # 设置随机种子以确保可重现性
    np.random.seed(42)
    random.seed(42)
    
    # 生成股票代码
    codes = []
    names = []
    for i in range(num_stocks):
        if i < 50:  # 前50只为沪市股票
            code = f"60{i:04d}"
        else:  # 后50只为深市股票
            code = f"00{i-50:04d}"
        codes.append(code)
        names.append(f"股票{i+1}")
    
    # 生成一些特殊股票（用于测试过滤功能）
    special_stocks = [
        ("C12345", "C新股1"),  # 新股
        ("N67890", "N新股2"),  # 新股
        ("*ST001", "*ST风险"),  # ST股
        ("S退市", "S退市股"),   # 退市股
    ]
    
    codes.extend([s[0] for s in special_stocks])
    names.extend([s[1] for s in special_stocks])
    
    # 生成基础数据
    data = {
        '代码': codes,
        '名称': names,
        '最新': np.random.uniform(3, 80, len(codes)),  # 股价3-80元
        '涨幅': np.random.normal(0, 3, len(codes)),    # 涨幅正态分布
        '换手率': np.random.uniform(0.1, 25, len(codes)),  # 换手率0.1-25%
        '量比': np.random.uniform(0.3, 8, len(codes)),     # 量比0.3-8
        '市盈率': np.random.uniform(-50, 100, len(codes)), # 市盈率-50-100
        '成交量': np.random.uniform(1000, 1000000, len(codes)),  # 成交量
        '成交额': np.random.uniform(10000, 50000000, len(codes)),  # 成交额
        '时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # 计算衍生字段
    data['昨收'] = data['最新'] / (1 + data['涨幅'] / 100)
    data['今开'] = data['昨收'] * (1 + np.random.uniform(-0.05, 0.05, len(codes)))
    data['最高'] = np.maximum(data['最新'], data['今开']) * (1 + np.random.uniform(0, 0.03, len(codes)))
    data['最低'] = np.minimum(data['最新'], data['今开']) * (1 - np.random.uniform(0, 0.03, len(codes)))
    
    # 市值计算（假设流通股本）
    shares = np.random.uniform(1e8, 20e8, len(codes))  # 流通股本1-20亿股
    data['流通市值'] = data['最新'] * shares
    data['总市值'] = data['流通市值'] * np.random.uniform(1.2, 2.0, len(codes))
    
    df = pd.DataFrame(data)
    
    # 调整一些特殊股票的数据
    # 让一些股票符合选股条件
    good_stocks_mask = (df.index % 10 == 0) & (df.index < 50)  # 每10只股票中选1只
    df.loc[good_stocks_mask, '涨幅'] = np.random.uniform(1, 7, good_stocks_mask.sum())
    df.loc[good_stocks_mask, '换手率'] = np.random.uniform(3, 15, good_stocks_mask.sum())
    df.loc[good_stocks_mask, '量比'] = np.random.uniform(1.5, 5, good_stocks_mask.sum())
    df.loc[good_stocks_mask, '最新'] = np.random.uniform(5, 50, good_stocks_mask.sum())
    df.loc[good_stocks_mask, '流通市值'] = np.random.uniform(3e9, 1.5e10, good_stocks_mask.sum())
    df.loc[good_stocks_mask, '市盈率'] = np.random.uniform(5, 50, good_stocks_mask.sum())
    
    return df

def test_basic_picker():
    """测试基础选股器"""
    print("🧪 测试基础选股器...")
    
    from base_stock_picker import BaseStockPicker
    
    # 创建模拟数据
    mock_data = generate_mock_stock_data(200)
    
    # 创建选股器实例
    picker = BaseStockPicker(market_threshold=0.3)  # 降低市场阈值用于测试
    
    # 模拟选股流程
    try:
        # 检查市场环境
        is_good_market, up_ratio = picker.check_market_environment(mock_data)
        print(f"市场环境: {'✅ 适合' if is_good_market else '❌ 不适合'}, 上涨占比: {up_ratio:.2%}")
        
        # 风险股票过滤
        filtered_data = picker.filter_risk_stocks(mock_data)
        print(f"风险过滤后剩余: {len(filtered_data)} 只股票")
        
        # 选股标准过滤
        selected_stocks = picker.apply_selection_criteria(filtered_data)
        print(f"选股标准过滤后: {len(selected_stocks)} 只股票")
        
        # 排序
        ranked_stocks = picker.rank_stocks(selected_stocks)
        print("排序完成，前5名:")
        if len(ranked_stocks) > 0:
            print(ranked_stocks[['代码', '名称', '最新', '涨幅', '换手率', '量比']].head())
        
        print("✅ 基础选股器测试完成\n")
        
    except Exception as e:
        print(f"❌ 基础选股器测试失败: {e}\n")

def test_advanced_picker():
    """测试高级选股器"""
    print("🧪 测试高级选股器...")
    
    from advanced_stock_picker import AdvancedStockPicker
    
    # 创建模拟数据
    mock_data = generate_mock_stock_data(200)
    
    # 创建高级选股器实例
    picker = AdvancedStockPicker(market_mode='normal')
    
    # 模拟选股流程
    try:
        # 市场环境分析
        recommended_mode = picker.analyze_market_environment(mock_data)
        print(f"推荐市场模式: {recommended_mode}")
        
        # 技术面过滤
        technical_filtered = picker.apply_technical_filter(mock_data)
        print(f"技术面过滤后: {len(technical_filtered)} 只股票")
        
        # 风险评分
        risk_scored = picker.calculate_risk_score(technical_filtered)
        print(f"风险评分计算完成，平均风险评分: {risk_scored['风险评分'].mean():.3f}")
        
        print("✅ 高级选股器测试完成\n")
        
    except Exception as e:
        print(f"❌ 高级选股器测试失败: {e}\n")

def demo_complete_workflow():
    """演示完整的选股工作流程"""
    print("🎯 演示完整选股工作流程...")
    
    from advanced_stock_picker import AdvancedStockPicker
    
    # 创建高级选股器
    picker = AdvancedStockPicker(market_mode='normal')
    
    # 用模拟数据替换实际数据获取（用于演示）
    original_get_market_data = picker.get_market_data
    
    def mock_get_market_data():
        return generate_mock_stock_data(500)
    
    picker.get_market_data = mock_get_market_data
    
    try:
        # 执行选股
        selected_stocks, stats = picker.select_stocks_advanced(
            max_stocks=5,
            auto_adjust_mode=True
        )
        
        # 显示结果
        picker.display_advanced_results(selected_stocks, stats)
        
        print("✅ 完整工作流程演示完成")
        
    except Exception as e:
        print(f"❌ 工作流程演示失败: {e}")
    
    # 恢复原始方法
    picker.get_market_data = original_get_market_data

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行所有测试...\n")
    
    test_basic_picker()
    test_advanced_picker()
    demo_complete_workflow()
    
    print("\n🎉 所有测试完成!")

if __name__ == "__main__":
    run_all_tests()

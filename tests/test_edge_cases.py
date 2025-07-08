"""
边缘案例测试 - Edge Cases Testing
测试股票选择器在各种异常情况下的表现
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')


def test_empty_data():
    """测试空数据集的处理"""
    print("🧪 测试边缘案例: 空数据集...")
    
    try:
        from base_stock_picker import BaseStockPicker
        from advanced_stock_picker import AdvancedStockPicker
        
        # 创建空DataFrame
        empty_df = pd.DataFrame()
        
        # 测试基础选股器
        base_picker = BaseStockPicker()
        try:
            is_good, ratio = base_picker.check_market_environment(empty_df)
            print(f"  基础选股器 - 空数据市场环境检查: 通过 (ratio={ratio:.2%})")
        except Exception as e:
            print(f"  基础选股器 - 空数据市场环境检查: 失败 - {e}")
        
        try:
            filtered = base_picker.filter_risk_stocks(empty_df)
            print(f"  基础选股器 - 空数据风险过滤: 通过 (剩余{len(filtered)}只)")
        except Exception as e:
            print(f"  基础选股器 - 空数据风险过滤: 失败 - {e}")
        
        # 测试高级选股器
        advanced_picker = AdvancedStockPicker()
        try:
            mode = advanced_picker.analyze_market_environment(empty_df)
            print(f"  高级选股器 - 空数据市场分析: 通过 (推荐模式: {mode})")
        except Exception as e:
            print(f"  高级选股器 - 空数据市场分析: 失败 - {e}")
        
        print("✅ 空数据集测试完成\n")
        
    except Exception as e:
        print(f"❌ 空数据集测试失败: {e}\n")


def test_invalid_data_types():
    """测试无效数据类型的处理"""
    print("🧪 测试边缘案例: 无效数据类型...")
    
    try:
        from base_stock_picker import BaseStockPicker
        
        # 创建包含无效数据的DataFrame
        invalid_data = pd.DataFrame({
            '代码': ['600000', '000001', '600036'],
            '名称': ['股票A', '股票B', '股票C'],
            '最新': ['无效', 10.5, None],  # 混合类型
            '涨幅': [2.5, 'abc', np.inf],  # 包含字符串和无限值
            '换手率': [5.0, -999, 15.0],  # 包含异常负值
            '量比': [2.0, 0, np.nan],     # 包含0和NaN
            '市盈率': [25.0, 1000.0, -50.0],
            '成交量': [1000000, -1, 'N/A'],
            '成交额': [50000000, None, 0],
            '流通市值': [1e10, 1e15, 1e6],  # 包含极端值
            '总市值': [1.2e10, 1.5e15, 1.2e6],
        })
        
        picker = BaseStockPicker()
        
        try:
            # 测试市场环境检查
            is_good, ratio = picker.check_market_environment(invalid_data)
            print(f"  无效数据市场环境检查: 通过 (ratio={ratio:.2%})")
        except Exception as e:
            print(f"  无效数据市场环境检查: 失败 - {e}")
        
        try:
            # 测试风险过滤
            filtered = picker.filter_risk_stocks(invalid_data)
            print(f"  无效数据风险过滤: 通过 (剩余{len(filtered)}只)")
        except Exception as e:
            print(f"  无效数据风险过滤: 失败 - {e}")
        
        try:
            # 测试选股标准应用
            selected = picker.apply_selection_criteria(invalid_data)
            print(f"  无效数据选股标准: 通过 (选出{len(selected)}只)")
        except Exception as e:
            print(f"  无效数据选股标准: 失败 - {e}")
        
        print("✅ 无效数据类型测试完成\n")
        
    except Exception as e:
        print(f"❌ 无效数据类型测试失败: {e}\n")


def test_extreme_values():
    """测试极端数值的处理"""
    print("🧪 测试边缘案例: 极端数值...")
    
    try:
        from base_stock_picker import BaseStockPicker
        from advanced_stock_picker import AdvancedStockPicker
        
        # 创建包含极端值的数据
        extreme_data = pd.DataFrame({
            '代码': ['600000', '000001', '600036', '002001', '600519'],
            '名称': ['极低价', '极高价', '极高涨幅', '极低涨幅', '正常股'],
            '最新': [0.01, 9999.99, 50.0, 25.0, 100.0],  # 极端价格
            '涨幅': [0.01, 0.02, 999.99, -99.99, 2.5],   # 极端涨跌幅
            '换手率': [0.001, 0.002, 999.99, 5.0, 8.0],  # 极端换手率
            '量比': [0.001, 0.002, 999.99, 2.5, 3.0],    # 极端量比
            '市盈率': [-999, 9999, 15.0, 25.0, 30.0],    # 极端市盈率
            '成交量': [1, 999999999999, 1000000, 500000, 2000000],
            '成交额': [100, 999999999999, 50000000, 25000000, 100000000],
            '流通市值': [1e6, 1e15, 5e10, 3e10, 8e10],    # 极端市值
            '总市值': [1.2e6, 1.2e15, 6e10, 3.5e10, 9e10],
        })
        
        # 测试基础选股器
        base_picker = BaseStockPicker()
        try:
            filtered = base_picker.filter_risk_stocks(extreme_data)
            selected = base_picker.apply_selection_criteria(filtered)
            ranked = base_picker.rank_stocks(selected)
            print(f"  基础选股器极端值处理: 通过 (最终{len(ranked)}只)")
        except Exception as e:
            print(f"  基础选股器极端值处理: 失败 - {e}")
        
        # 测试高级选股器
        advanced_picker = AdvancedStockPicker()
        try:
            technical_filtered = advanced_picker.apply_technical_filter(extreme_data)
            risk_scored = advanced_picker.calculate_risk_score(technical_filtered)
            print(f"  高级选股器极端值处理: 通过 (风险评分范围: {risk_scored['风险评分'].min():.3f}-{risk_scored['风险评分'].max():.3f})")
        except Exception as e:
            print(f"  高级选股器极端值处理: 失败 - {e}")
        
        print("✅ 极端数值测试完成\n")
        
    except Exception as e:
        print(f"❌ 极端数值测试失败: {e}\n")


def test_market_mode_edge_cases():
    """测试市场模式的边缘情况"""
    print("🧪 测试边缘案例: 市场模式边缘情况...")
    
    try:
        from advanced_stock_picker import AdvancedStockPicker
        
        # 测试各种市场极端情况
        test_cases = [
            ("全部上涨市场", {'涨幅': [5, 8, 12, 3, 7]}),
            ("全部下跌市场", {'涨幅': [-5, -8, -12, -3, -7]}),
            ("无波动市场", {'涨幅': [0, 0, 0, 0, 0]}),
            ("极端波动市场", {'涨幅': [20, -20, 15, -15, 10]})
        ]
        
        for case_name, market_data in test_cases:
            try:
                # 创建测试数据
                data = pd.DataFrame({
                    '代码': ['600000', '000001', '600036', '002001', '600519'],
                    '名称': ['股票A', '股票B', '股票C', '股票D', '股票E'],
                    '最新': [20, 25, 30, 15, 40],
                    '涨幅': market_data['涨幅'],
                    '换手率': [5, 8, 12, 3, 7],
                    '量比': [2, 3, 4, 1.5, 2.5],
                    '市盈率': [20, 25, 30, 15, 35],
                    '成交量': [1000000] * 5,
                    '成交额': [50000000] * 5,
                    '流通市值': [5e10] * 5,
                    '总市值': [6e10] * 5,
                })
                
                picker = AdvancedStockPicker()
                mode = picker.analyze_market_environment(data)
                print(f"  {case_name}: 推荐模式 = {mode}")
                
            except Exception as e:
                print(f"  {case_name}: 失败 - {e}")
        
        print("✅ 市场模式边缘情况测试完成\n")
        
    except Exception as e:
        print(f"❌ 市场模式边缘情况测试失败: {e}\n")


def test_memory_and_performance():
    """测试内存和性能边缘情况"""
    print("🧪 测试边缘案例: 内存和性能...")
    
    try:
        from base_stock_picker import BaseStockPicker
        from advanced_stock_picker import AdvancedStockPicker
        import time
        
        # 创建大数据集
        large_size = 10000
        print(f"  创建{large_size}只股票的大数据集...")
        
        large_data = pd.DataFrame({
            '代码': [f"60{i:04d}" if i < 5000 else f"00{i-5000:04d}" for i in range(large_size)],
            '名称': [f"股票{i+1}" for i in range(large_size)],
            '最新': np.random.uniform(5, 100, large_size),
            '涨幅': np.random.normal(0, 3, large_size),
            '换手率': np.random.uniform(1, 20, large_size),
            '量比': np.random.uniform(0.5, 5, large_size),
            '市盈率': np.random.uniform(5, 80, large_size),
            '成交量': np.random.uniform(100000, 10000000, large_size),
            '成交额': np.random.uniform(5000000, 500000000, large_size),
            '流通市值': np.random.uniform(1e9, 1e11, large_size),
            '总市值': np.random.uniform(1.2e9, 1.2e11, large_size),
        })
        
        # 测试基础选股器性能
        try:
            start_time = time.time()
            base_picker = BaseStockPicker()
            filtered = base_picker.filter_risk_stocks(large_data)
            selected = base_picker.apply_selection_criteria(filtered)
            ranked = base_picker.rank_stocks(selected)
            elapsed = time.time() - start_time
            print(f"  基础选股器大数据处理: 通过 ({elapsed:.2f}秒, 最终{len(ranked)}只)")
        except Exception as e:
            print(f"  基础选股器大数据处理: 失败 - {e}")
        
        # 测试高级选股器性能
        try:
            start_time = time.time()
            advanced_picker = AdvancedStockPicker()
            advanced_picker.analyze_market_environment(large_data)
            technical_filtered = advanced_picker.apply_technical_filter(large_data)
            risk_scored = advanced_picker.calculate_risk_score(technical_filtered)
            elapsed = time.time() - start_time
            print(f"  高级选股器大数据处理: 通过 ({elapsed:.2f}秒, 处理{len(risk_scored)}只)")
        except Exception as e:
            print(f"  高级选股器大数据处理: 失败 - {e}")
        
        print("✅ 内存和性能测试完成\n")
        
    except Exception as e:
        print(f"❌ 内存和性能测试失败: {e}\n")


def test_missing_columns():
    """测试缺失列的处理"""
    print("🧪 测试边缘案例: 缺失列...")
    
    try:
        from base_stock_picker import BaseStockPicker
        
        # 测试缺失关键列
        incomplete_data = pd.DataFrame({
            '代码': ['600000', '000001'],
            '名称': ['股票A', '股票B'],
            '最新': [20, 25],
            # 缺失其他重要列
        })
        
        picker = BaseStockPicker()
        
        try:
            # 这应该会失败或优雅处理
            filtered = picker.filter_risk_stocks(incomplete_data)
            print(f"  缺失列处理: 意外通过 (剩余{len(filtered)}只)")
        except Exception as e:
            print(f"  缺失列处理: 预期失败 - {type(e).__name__}")
        
        # 测试有最小必需列的情况
        minimal_data = pd.DataFrame({
            '代码': ['600000', '000001', '600036'],
            '名称': ['股票A', '股票B', '股票C'],
            '最新': [20, 25, 30],
            '涨幅': [2.5, -1.2, 3.8],
            '换手率': [5.0, 8.0, 12.0],
            '量比': [2.0, 3.0, 4.0],
        })
        
        try:
            filtered = picker.filter_risk_stocks(minimal_data)
            print(f"  最小列集处理: 通过 (剩余{len(filtered)}只)")
        except Exception as e:
            print(f"  最小列集处理: 失败 - {e}")
        
        print("✅ 缺失列测试完成\n")
        
    except Exception as e:
        print(f"❌ 缺失列测试失败: {e}\n")


def test_special_stock_codes():
    """测试特殊股票代码的处理"""
    print("🧪 测试边缘案例: 特殊股票代码...")
    
    try:
        from base_stock_picker import BaseStockPicker
        
        # 创建包含各种特殊代码的数据
        special_data = pd.DataFrame({
            '代码': [
                'ST000001',   # ST股票
                '*ST002001',  # *ST股票
                'C123456',    # 新股
                'N789012',    # 新股
                'S退市',      # 退市股票
                '300001',     # 创业板
                '688001',     # 科创板
                '600000',     # 正常沪市
                '000001',     # 正常深市
                'BJ001001',   # 北交所
            ],
            '名称': [f'特殊股{i+1}' for i in range(10)],
            '最新': [10 + i for i in range(10)],
            '涨幅': [1 + i*0.5 for i in range(10)],
            '换手率': [5 + i for i in range(10)],
            '量比': [2 + i*0.2 for i in range(10)],
            '市盈率': [20 + i*2 for i in range(10)],
            '成交量': [1000000] * 10,
            '成交额': [50000000] * 10,
            '流通市值': [5e10] * 10,
            '总市值': [6e10] * 10,
        })
        
        picker = BaseStockPicker()
        
        try:
            # 测试风险股票过滤（应该过滤掉ST、新股等）
            original_count = len(special_data)
            filtered = picker.filter_risk_stocks(special_data)
            filtered_count = len(filtered)
            print(f"  特殊代码风险过滤: 通过 ({original_count} -> {filtered_count})")
            
            if filtered_count > 0:
                print(f"  剩余股票代码: {filtered['代码'].tolist()}")
            
        except Exception as e:
            print(f"  特殊代码风险过滤: 失败 - {e}")
        
        print("✅ 特殊股票代码测试完成\n")
        
    except Exception as e:
        print(f"❌ 特殊股票代码测试失败: {e}\n")


def run_all_edge_case_tests():
    """运行所有边缘案例测试"""
    print("🚀 开始运行边缘案例测试...\n")
    print("=" * 60)
    
    test_empty_data()
    test_invalid_data_types()
    test_extreme_values()
    test_market_mode_edge_cases()
    test_memory_and_performance()
    test_missing_columns()
    test_special_stock_codes()
    
    print("=" * 60)
    print("🎉 所有边缘案例测试完成!")
    print("\n💡 提示: 边缘案例测试帮助确保系统在异常情况下的稳定性")
    print("📝 建议: 根据测试结果优化错误处理和数据验证机制")


if __name__ == "__main__":
    run_all_edge_case_tests()

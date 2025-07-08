#!/usr/bin/env python3
"""
早盘选股快速示例
Quick example for pre-market stock selection
"""

import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_stock_picker import BaseStockPicker
from advanced_stock_picker import AdvancedStockPicker

def run_basic_example():
    """运行基础选股示例"""
    print("🔥 运行基础选股示例")
    print("-" * 40)
    
    try:
        # 创建基础选股器
        picker = BaseStockPicker()
        
        # 执行选股
        selected_stocks, stats = picker.select_stocks(max_stocks=5)
        
        # 显示结果
        picker.display_results(selected_stocks, stats)
        
    except Exception as e:
        print(f"❌ 基础选股失败: {e}")
        print("💡 提示: 请检查网络连接和API配置")

def run_advanced_example():
    """运行高级选股示例"""
    print("\n🚀 运行高级选股示例")
    print("-" * 40)
    
    try:
        # 创建高级选股器
        picker = AdvancedStockPicker(market_mode='normal')
        
        # 执行高级选股
        selected_stocks, stats = picker.select_stocks_advanced(
            max_stocks=5,
            auto_adjust_mode=True
        )
        
        # 显示结果
        picker.display_advanced_results(selected_stocks, stats)
        
    except Exception as e:
        print(f"❌ 高级选股失败: {e}")
        print("💡 提示: 请检查网络连接和API配置")

def main():
    """主函数"""
    print("🎯 早盘量化选股系统示例")
    print("=" * 50)
    
    # 运行基础示例
    run_basic_example()
    
    # 运行高级示例  
    run_advanced_example()
    
    print("\n" + "=" * 50)
    print("📝 使用提示:")
    print("1. 本示例使用实时数据，需要网络连接")
    print("2. 建议在交易时间使用获取最新数据")
    print("3. 投资有风险，仅供学习参考")
    print("4. 可通过config.py调整选股参数")

if __name__ == "__main__":
    main()

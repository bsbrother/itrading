"""
统一股票选股AI分析器演示
Demo for Unified Stock Picker with AI Analyzer

演示如何使用统一分析器进行选股和AI分析
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from unify_stock_pick_ai_analyzer import UnifiedStockPickAIAnalyzer
from datetime import datetime

def demo_unified_analyzer():
    """演示统一选股AI分析器"""
    print("🚀 统一股票选股AI分析器演示")
    print("="*60)
    
    try:
        # 创建分析器实例
        analyzer = UnifiedStockPickAIAnalyzer(market_mode='normal')
        
        # 执行选股和AI分析 (减少数量以加快演示速度)
        print("\n📊 开始执行选股和AI分析...")
        enhanced_stocks, stats = analyzer.pick_and_analyze_stocks(
            trade_date=datetime.now().strftime('%Y%m%d'),
            max_stocks=10,  # 演示用，只选3只股票
            auto_adjust_mode=True
        )
        
        # 显示结果
        analyzer.display_unified_results(enhanced_stocks, stats)
        
        # 保存结果
        if len(enhanced_stocks) > 0:
            analyzer.save_results(enhanced_stocks, stats)
            print("\n✅ 演示完成，结果已保存")
        else:
            print("\n⚠️ 演示完成，但未选出股票")
            
    except Exception as e:
        print(f"❌ 演示失败: {e}")

if __name__ == "__main__":
    demo_unified_analyzer()

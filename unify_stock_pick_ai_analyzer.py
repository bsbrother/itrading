"""
统一股票选股AI分析器
Unified Stock Picker with AI Analyzer

整合股票选股器和AI分析器，提供完整的选股和智能分析解决方案
"""

import os
import sys
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Tuple

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from advanced_stock_picker import AdvancedStockPicker
from ai_stock_analyzer import stock_analyzer

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

os.makedirs('/tmp/itrading', exist_ok=True)


class UnifiedStockPickAIAnalyzer:
    """统一股票选股AI分析器"""
    
    def __init__(self, market_mode: str = 'normal'):
        """
        初始化统一分析器
        
        Args:
            market_mode: 市场模式 ('normal', 'bull_market', 'bear_market', 'volatile_market')
        """
        self.market_mode = market_mode
        self.picker = AdvancedStockPicker(market_mode=market_mode)
        logger.info(f"初始化统一股票选股AI分析器，市场模式: {market_mode}")
    
    def pick_and_analyze_stocks(self, 
                               trade_date: str = None, 
                               max_stocks: int = 8,
                               auto_adjust_mode: bool = True) -> Tuple[pd.DataFrame, Dict]:
        """
        选股并进行AI分析
        
        Args:
            trade_date: 交易日期，格式YYYYMMDD，默认为今天
            max_stocks: 最大选股数量
            auto_adjust_mode: 是否自动调整模式
            
        Returns:
            Tuple[pd.DataFrame, Dict]: (增强后的股票数据, 统计信息)
        """
        if trade_date is None:
            trade_date = datetime.now().strftime('%Y%m%d')
        
        logger.info(f"开始统一选股AI分析，日期: {trade_date}")
        
        try:
            # 1. 使用高级选股器选股
            logger.info("🔍 步骤1: 执行股票选股...")
            selected_stocks, stats = self.picker.select_stocks_advanced(
                trade_date=trade_date,
                max_stocks=max_stocks,
                auto_adjust_mode=auto_adjust_mode
            )
            
            if selected_stocks.empty:
                logger.warning("选股器未选出任何股票")
                return pd.DataFrame(), stats
            
            # 2. 提取股票代码进行AI分析
            stock_codes = selected_stocks['代码'].tolist()
            logger.info(f"🤖 步骤2: 对 {len(stock_codes)} 只股票进行AI分析...")
            
            # 调用AI分析器
            ai_results = stock_analyzer(stock_codes)
            
            # 3. 创建AI分析结果字典
            ai_dict = {}
            for result in ai_results:
                stock_code = result['stock_code']
                ai_dict[stock_code] = {
                    'ai_score': result['ai_score'],
                    'ai_analysis': result['ai_analysis']
                }
            
            # 4. 将AI分析结果添加到选股结果中
            logger.info("📊 步骤3: 合并AI分析结果...")
            enhanced_stocks = self._merge_ai_results(selected_stocks, ai_dict)
            
            # 5. 计算最终得分
            enhanced_stocks = self._calculate_final_score(enhanced_stocks)
            
            # 6. 按最终得分重新排序
            enhanced_stocks = enhanced_stocks.sort_values('final_score', ascending=False).reset_index(drop=True)
            
            # 更新统计信息
            stats['ai_analysis_completed'] = True
            stats['final_stocks_count'] = len(enhanced_stocks)
            
            logger.info(f"✅ 统一选股AI分析完成，最终选出 {len(enhanced_stocks)} 只股票")
            
            return enhanced_stocks, stats
            
        except Exception as e:
            logger.error(f"统一选股AI分析失败: {e}")
            raise
    
    def _merge_ai_results(self, selected_stocks: pd.DataFrame, ai_dict: Dict) -> pd.DataFrame:
        """
        合并AI分析结果到选股数据中
        
        Args:
            selected_stocks: 选股结果DataFrame
            ai_dict: AI分析结果字典
            
        Returns:
            合并后的DataFrame
        """
        enhanced_stocks = selected_stocks.copy()
        
        # 添加AI分析字段
        enhanced_stocks['ai_score'] = 0.0
        enhanced_stocks['ai_analysis'] = ""
        
        for idx, row in enhanced_stocks.iterrows():
            stock_code = row['代码']
            if stock_code in ai_dict:
                enhanced_stocks.at[idx, 'ai_score'] = ai_dict[stock_code]['ai_score']
                enhanced_stocks.at[idx, 'ai_analysis'] = ai_dict[stock_code]['ai_analysis']
            else:
                logger.warning(f"股票 {stock_code} 未找到AI分析结果")
        
        return enhanced_stocks
    
    def _calculate_final_score(self, enhanced_stocks: pd.DataFrame) -> pd.DataFrame:
        """
        计算最终得分
        统一 '流通市值,综合得分,风险评分,风险调整得分' + 'ai_score'
        
        Args:
            enhanced_stocks: 包含AI分析的股票数据
            
        Returns:
            包含最终得分的DataFrame
        """
        df = enhanced_stocks.copy()
        
        # 标准化各个得分指标到0-1范围
        def normalize_score(series, higher_is_better=True):
            """标准化得分到0-1范围"""
            if series.std() == 0:
                return pd.Series([0.5] * len(series), index=series.index)
            
            normalized = (series - series.min()) / (series.max() - series.min())
            if not higher_is_better:
                normalized = 1 - normalized
            return normalized
        
        # 标准化流通市值 (适中为好，过大过小都不好)
        market_cap_score = df['流通市值'].copy()
        market_cap_median = market_cap_score.median()
        market_cap_score = 1 - abs(market_cap_score - market_cap_median) / market_cap_median
        market_cap_score = market_cap_score.clip(0, 1)
        
        # 标准化其他得分
        composite_score_norm = normalize_score(df['综合得分'])
        risk_score_norm = normalize_score(df['风险评分'], higher_is_better=False)  # 风险评分越低越好
        risk_adjusted_score_norm = normalize_score(df['风险调整得分'])
        ai_score_norm = normalize_score(df['ai_score'])
        
        # 计算最终得分 (加权平均)
        weights = {
            'market_cap': 0.15,      # 流通市值权重
            'composite': 0.25,       # 综合得分权重  
            'risk': 0.20,           # 风险评分权重
            'risk_adjusted': 0.20,   # 风险调整得分权重
            'ai_score': 0.20        # AI得分权重
        }
        
        df['final_score'] = (
            market_cap_score * weights['market_cap'] +
            composite_score_norm * weights['composite'] +
            risk_score_norm * weights['risk'] +
            risk_adjusted_score_norm * weights['risk_adjusted'] +
            ai_score_norm * weights['ai_score']
        ) * 100  # 转换为0-100分制
        
        logger.info("✅ 最终得分计算完成")
        return df
    
    def display_unified_results(self, enhanced_stocks: pd.DataFrame, stats: Dict):
        """
        显示统一分析结果
        
        Args:
            enhanced_stocks: 增强后的股票数据
            stats: 统计信息
        """
        print("\n" + "="*80)
        print("🚀 统一股票选股AI分析结果")
        print("="*80)
        
        print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"交易日期: {stats.get('trade_date', 'N/A')}")
        print(f"市场模式: {stats.get('market_mode', 'N/A')}")
        print(f"市场总股票数: {stats.get('total_stocks', 'N/A')}")
        print(f"最终选股数量: {stats.get('final_stocks_count', 'N/A')}")
        print(f"AI分析完成: {'✅' if stats.get('ai_analysis_completed', False) else '❌'}")
        
        if enhanced_stocks.empty:
            print("\n❌ 没有选出符合条件的股票")
            return
        
        print(f"\n📊 详细选股结果 (共{len(enhanced_stocks)}只):")
        print("-" * 80)
        
        # 显示关键列
        display_columns = [
            '代码', '名称', '最新', '涨幅', '流通市值', 
            '综合得分', '风险调整得分', 'ai_score', 'final_score'
        ]
        
        # 确保所有列都存在
        available_columns = [col for col in display_columns if col in enhanced_stocks.columns]
        
        display_df = enhanced_stocks[available_columns].copy()
        
        # 格式化数值列
        if '流通市值' in display_df.columns:
            display_df['流通市值'] = display_df['流通市值'].apply(lambda x: f"{x/1e8:.1f}亿" if pd.notna(x) else "N/A")
        
        score_columns = ['综合得分', '风险调整得分', 'ai_score', 'final_score']
        for col in score_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "N/A")
        
        # 显示表格
        print(display_df.to_string(index=False, max_colwidth=15))
        
        print("\n🎯 推荐关注前3名:")
        for i, (idx, row) in enumerate(enhanced_stocks.head(3).iterrows(), 1):
            print(f"{i}. {row['代码']} {row['名称']} - 最终得分: {row['final_score']:.2f}")
            if 'ai_analysis' in row and pd.notna(row['ai_analysis']):
                # 截取AI分析的前100个字符
                ai_summary = str(row['ai_analysis'])[:100] + "..." if len(str(row['ai_analysis'])) > 100 else str(row['ai_analysis'])
                print(f"   AI分析: {ai_summary}")
            print()
    
    def save_results(self, enhanced_stocks: pd.DataFrame, stats: Dict, save_path: str = None):
        """
        保存分析结果
        
        Args:
            enhanced_stocks: 增强后的股票数据
            stats: 统计信息
            save_path: 保存路径，默认为时间戳命名
        """
        if enhanced_stocks.empty:
            logger.warning("没有数据可保存")
            return
        
        if save_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            save_path = f"/tmp/itrading/unified_stock_analysis_{timestamp}.csv"
        
        try:
            # 创建保存用的数据副本
            save_data = enhanced_stocks.copy()
            
            # 格式化得分列为2位小数
            score_columns = ['综合得分', '风险评分', '风险调整得分', 'ai_score', 'final_score']
            for col in score_columns:
                if col in save_data.columns:
                    save_data[col] = save_data[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else x)
            
            # 保存为CSV
            save_data.to_csv(save_path, index=False, encoding='utf-8-sig')
            
            # 保存统计信息
            stats_path = save_path.replace('.csv', '_stats.txt')
            with open(stats_path, 'w', encoding='utf-8') as f:
                f.write("统一股票选股AI分析统计信息\n")
                f.write("="*50 + "\n")
                for key, value in stats.items():
                    f.write(f"{key}: {value}\n")
            
            logger.info(f"✅ 分析结果已保存至: {save_path}")
            logger.info(f"✅ 统计信息已保存至: {stats_path}")
            
        except Exception as e:
            logger.error(f"保存结果失败: {e}")


def main():
    """主函数 - 演示统一选股AI分析"""
    try:
        # 创建统一分析器实例
        analyzer = UnifiedStockPickAIAnalyzer(market_mode='normal')
        
        # 执行统一选股AI分析
        enhanced_stocks, stats = analyzer.pick_and_analyze_stocks(
            trade_date=datetime.now().strftime('%Y%m%d'),
            max_stocks=6,  # 减少数量以加快AI分析速度
            auto_adjust_mode=True
        )
        
        # 显示结果
        analyzer.display_unified_results(enhanced_stocks, stats)
        
        # 保存结果
        if len(enhanced_stocks) > 0:
            analyzer.save_results(enhanced_stocks, stats)
        
    except Exception as e:
        logger.error(f"统一选股AI分析失败: {e}")
        print(f"❌ 分析失败: {e}")


if __name__ == "__main__":
    main()

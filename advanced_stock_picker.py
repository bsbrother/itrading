"""
高级股票选择器策略
Advanced Stock Picker Strategy, Support custom configure.

基于配置文件的可定制化选股策略
"""

import os
import sys
import logging
import pandas as pd
from typing import Dict, Tuple, Union
from datetime import datetime, date

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from base_stock_picker import BaseStockPicker
from config import (
    MARKET_CAP_CONFIG, PRICE_CONFIG, TURNOVER_CONFIG, GAIN_CONFIG,
    VOLUME_RATIO_CONFIG, MARKET_CONFIG, SELECTION_CONFIG, OUTPUT_CONFIG,
    MARKET_ENVIRONMENT_ADJUSTMENTS
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.makedirs('/tmp/itrading', exist_ok=True)


class AdvancedStockPicker(BaseStockPicker):
    """高级股票选择器，支持动态参数调整和多种选股模式"""

    def __init__(self, market_mode: str = 'normal'):
        """
        初始化高级股票选择器

        Args:
            market_mode: 市场模式 ('normal', 'bull_market', 'bear_market', 'volatile_market')
        """
        self.market_mode = market_mode

        # 根据市场模式调整参数
        config = self._get_adjusted_config(market_mode)

        super().__init__(**config)

        logger.info(f"初始化高级选股器，市场模式: {market_mode}")

    def _get_adjusted_config(self, market_mode: str) -> Dict:
        """
        根据市场模式获取调整后的配置

        Args:
            market_mode: 市场模式

        Returns:
            调整后的配置字典
        """
        # 基础配置
        config = {
            **MARKET_CAP_CONFIG,
            **PRICE_CONFIG,
            **TURNOVER_CONFIG,
            **GAIN_CONFIG,
            **VOLUME_RATIO_CONFIG,
            **MARKET_CONFIG
        }

        # 根据市场模式调整参数
        if market_mode in MARKET_ENVIRONMENT_ADJUSTMENTS:
            adjustments = MARKET_ENVIRONMENT_ADJUSTMENTS[market_mode]
            config.update(adjustments)
            logger.info(f"应用 {market_mode} 模式参数调整: {adjustments}")

        return config

    def analyze_market_environment(self, df: pd.DataFrame) -> str:
        """
        分析市场环境并自动确定市场模式

        Args:
            df: 市场数据DataFrame

        Returns:
            推荐的市场模式
        """
        # 检查数据是否为空
        if df.empty:
            logger.warning("数据为空，使用默认模式")
            return 'normal'

        # 检查市场是否开盘 - 通过涨幅列是否有有效数据判断
        gain_col = None
        possible_gain_cols = ['涨幅', '涨跌幅']  # qstock和akshare的涨幅列名

        for col in possible_gain_cols:
            if col in df.columns:
                gain_col = col
                break

        if gain_col is None:
            logger.warning("未找到涨幅相关列，使用默认模式")
            return 'normal'

        try:
            # 清理数据：确保涨幅列为数值类型
            df_clean = df.copy()
            df_clean[gain_col] = pd.to_numeric(df_clean[gain_col], errors='coerce')

            # 检查是否有有效的涨幅数据（判断市场是否开盘）
            valid_gain_data = df_clean[df_clean[gain_col].notna()]

            if valid_gain_data.empty:
                logger.warning("所有涨幅数据为空，可能市场尚未开盘")
                logger.info("市场未开盘，使用保守的normal模式进行预选")
                return 'normal'  # 预开盘时使用默认模式

            # 计算市场指标
            up_ratio = len(valid_gain_data[valid_gain_data[gain_col] > 0]) / len(valid_gain_data)
            avg_gain = valid_gain_data[gain_col].mean()
            volatility = valid_gain_data[gain_col].std()

            # 判断市场环境
            if up_ratio > 0.7 and avg_gain > 2:
                recommended_mode = 'bull_market'
            elif up_ratio < 0.3 and avg_gain < -1:
                recommended_mode = 'bear_market'
            elif volatility > 3:
                recommended_mode = 'volatile_market'
            else:
                recommended_mode = 'normal'

            logger.info(f"市场环境分析: 上涨占比={up_ratio:.2%}, 平均涨幅={avg_gain:.2f}%, "
                       f"波动率={volatility:.2f}%, 推荐模式={recommended_mode}")

            return recommended_mode

        except Exception as e:
            logger.error(f"分析市场环境时出错: {e}，使用默认模式")
            return 'normal'

    def apply_industry_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        应用行业过滤和权重调整

        Args:
            df: 股票数据DataFrame

        Returns:
            应用行业权重后的DataFrame
        """
        # 这里可以添加行业分类逻辑
        # 由于示例数据可能没有行业信息，暂时跳过
        logger.info("行业过滤功能待实现（需要行业分类数据）")
        return df

    def apply_technical_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        应用技术面过滤

        Args:
            df: 股票数据DataFrame

        Returns:
            技术面过滤后的DataFrame
        """
        # 检查数据是否为空
        if df.empty:
            logger.warning("输入数据为空，返回空DataFrame")
            return df

        try:
            df_clean = df.copy()

            # 检查是否有涨幅数据（判断市场是否开盘）
            gain_cols = ['涨幅', '涨跌幅']
            gain_col = None
            for col in gain_cols:
                if col in df_clean.columns:
                    gain_col = col
                    break

            if gain_col and df_clean[gain_col].notna().any():
                # 市场开盘时应用技术过滤
                df_clean[gain_col] = pd.to_numeric(df_clean[gain_col], errors='coerce')
                # 过滤掉涨幅过大的股票（可能超买）
                technical_filtered = df_clean[df_clean[gain_col] < 9.5]  # 避免接近涨停的股票
                logger.info(f"技术面过滤后剩余 {len(technical_filtered)} 只股票")
            else:
                # 市场未开盘时跳过技术过滤
                technical_filtered = df_clean
                logger.info(f"市场未开盘，跳过技术面过滤，保持 {len(technical_filtered)} 只股票")

            return technical_filtered

        except Exception as e:
            logger.error(f"技术面过滤时出错: {e}")
            return df

    def calculate_risk_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算风险评分

        Args:
            df: 股票数据DataFrame

        Returns:
            添加风险评分的DataFrame
        """
        df = df.copy()

        # 风险因子
        # 1. 波动率风险 (换手率越高风险越大)
        df['波动率风险'] = df['换手率'] / 20  # 标准化到0-1

        # 2. 估值风险 (市盈率过高风险大)
        df['估值风险'] = (df['市盈率'] - df['市盈率'].median()) / df['市盈率'].std()
        df['估值风险'] = df['估值风险'].clip(0, 1)  # 限制在0-1范围

        # 3. 流动性风险 (市值过小风险大)
        df['流动性风险'] = 1 - (df['流通市值'] - df['流通市值'].min()) / (df['流通市值'].max() - df['流通市值'].min())

        # 综合风险评分 (越低越好)
        df['风险评分'] = (
            df['波动率风险'] * 0.4 +
            df['估值风险'] * 0.3 +
            df['流动性风险'] * 0.3
        )

        return df

    def enhanced_ranking(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        增强版排序算法

        Args:
            df: 股票数据DataFrame

        Returns:
            排序后的DataFrame
        """
        # 先计算基础综合得分
        df = self._calculate_composite_score(df)

        # 计算风险评分
        df = self.calculate_risk_score(df)

        # 计算风险调整后的得分
        df['风险调整得分'] = df['综合得分'] * (1 - df['风险评分'])

        # 按风险调整得分排序
        df = df.sort_values('风险调整得分', ascending=False)

        return df

    def select_stocks_advanced(self,
        trade_date: Union[str, date, datetime] = None,
        max_stocks: int = None,
        auto_adjust_mode: bool = True) -> Tuple[pd.DataFrame, Dict]:
        """
        执行高级选股流程

        Args:
            trade_date: 交易日期，可以是字符串、日期对象或时间戳
            max_stocks: 最大选择股票数量
            auto_adjust_mode: 是否自动调整市场模式

        Returns:
            (选中的股票DataFrame, 选股统计信息)
        """
        if max_stocks is None:
            max_stocks = SELECTION_CONFIG['max_stocks']

        logger.info("开始执行高级选股流程...")

        # 1. 获取市场数据
        market_data = self.get_market_data(trade_date=trade_date)

        # 2. 自动分析市场环境（如果启用）
        if auto_adjust_mode:
            recommended_mode = self.analyze_market_environment(market_data)
            if recommended_mode != self.market_mode:
                logger.info(f"自动调整市场模式: {self.market_mode} -> {recommended_mode}")
                # 重新初始化参数
                config = self._get_adjusted_config(recommended_mode)
                for key, value in config.items():
                    setattr(self, key, value)
                self.market_mode = recommended_mode

        # 3. 检查市场环境
        is_good_market, up_ratio = self.check_market_environment(market_data)

        stats = {
            'total_stocks': len(market_data),
            'up_ratio': up_ratio,
            'is_good_market': is_good_market,
            'market_mode': self.market_mode,
            'selection_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # 如果市场环境不佳，返回空结果 (但允许预开盘筛选)
        if not is_good_market and up_ratio != 0.5:
            logger.warning("市场环境不佳，不进行选股")
            return pd.DataFrame(), stats

        # 4. 过滤风险股票
        filtered_data = self.filter_risk_stocks(market_data)
        stats['after_risk_filter'] = len(filtered_data)

        # 5. 应用技术面过滤
        technical_filtered = self.apply_technical_filter(filtered_data)
        stats['after_technical_filter'] = len(technical_filtered)

        # 6. 应用选股标准
        selected_stocks = self.apply_selection_criteria(technical_filtered)
        stats['after_criteria_filter'] = len(selected_stocks)

        # 7. 应用行业过滤
        industry_filtered = self.apply_industry_filter(selected_stocks)
        stats['after_industry_filter'] = len(industry_filtered)

        # 8. 增强版排序
        ranked_stocks = self.enhanced_ranking(industry_filtered)

        # 9. 限制数量
        final_stocks = ranked_stocks.head(max_stocks)
        stats['final_selection'] = len(final_stocks)

        logger.info(f"高级选股完成，最终选出 {len(final_stocks)} 只股票")

        return final_stocks, stats

    def display_advanced_results(self, selected_stocks: pd.DataFrame, stats: Dict):
        """
        显示高级选股结果

        Args:
            selected_stocks: 选中的股票DataFrame
            stats: 选股统计信息
        """
        print("\n" + "="*70)
        print("🚀 高级早盘量化选股结果")
        print("="*70)

        print(f"选股时间: {stats['selection_time']}")
        print(f"市场模式: {stats['market_mode']}")
        print(f"市场总股票数: {stats['total_stocks']}")
        print(f"市场上涨家数占比: {stats['up_ratio']:.2%}")
        print(f"市场环境评估: {'✅ 适合选股' if stats['is_good_market'] else '❌ 不适合选股'}")

        # 判断是否为市场开盘前的情况
        is_pre_market = stats['up_ratio'] == 0.5 and stats['is_good_market']

        if not stats['is_good_market'] and not is_pre_market:
            print("\n⚠️  市场环境不佳，建议观望")
            return

        if is_pre_market:
            print("\n📢 当前为市场开盘前，基于昨日数据进行高级筛选")

        print("\n筛选过程:")
        print(f"  风险股票过滤后: {stats['after_risk_filter']} 只")
        print(f"  技术面过滤后: {stats['after_technical_filter']} 只")
        print(f"  选股标准过滤后: {stats['after_criteria_filter']} 只")
        print(f"  行业过滤后: {stats['after_industry_filter']} 只")
        print(f"  最终选中: {stats['final_selection']} 只")

        if len(selected_stocks) > 0:
            if is_pre_market:
                print(f"\n🎯 高级预选 {len(selected_stocks)} 只潜力股（待开盘确认）:")
            else:
                print(f"\n🎯 今日精选 {len(selected_stocks)} 只潜力股:")
            print("-" * 70)

            for idx, (_, stock) in enumerate(selected_stocks.iterrows(), 1):
                market_cap_yi = stock['流通市值'] / 1e8 if pd.notna(stock['流通市值']) else 0  # 转换为亿元
                risk_score = stock.get('风险评分', 0)
                composite_score = stock.get('风险调整得分', stock.get('综合得分', 0))

                # 获取价格
                price = None
                if '最新价' in selected_stocks.columns and pd.notna(stock['最新价']):
                    price = stock['最新价']
                elif '最新' in selected_stocks.columns and pd.notna(stock['最新']):
                    price = stock['最新']
                elif '昨收' in selected_stocks.columns and pd.notna(stock['昨收']):
                    price = stock['昨收']

                # 获取涨幅
                gain = None
                gain_col = None
                if '涨幅' in selected_stocks.columns:
                    gain = stock['涨幅']
                    gain_col = '涨幅'
                elif '涨跌幅' in selected_stocks.columns:
                    gain = stock['涨跌幅']
                    gain_col = '涨跌幅'

                # 构建显示字符串
                info_parts = [f"{idx:2d}. {stock['代码']} {stock['名称']:8s}"]

                if price:
                    info_parts.append(f"价格:{price:6.2f}")

                if gain is not None and pd.notna(gain):
                    if is_pre_market and gain == 0:
                        info_parts.append("涨幅:待开盘")
                    else:
                        info_parts.append(f"涨幅:{gain:5.2f}%")
                elif is_pre_market:
                    info_parts.append("涨幅:待开盘")

                # 其他指标
                if '换手率' in selected_stocks.columns and pd.notna(stock['换手率']):
                    if is_pre_market and stock['换手率'] == 0:
                        info_parts.append("换手:待开盘")
                    else:
                        info_parts.append(f"换手:{stock['换手率']:5.2f}%")

                if '量比' in selected_stocks.columns and pd.notna(stock['量比']):
                    if is_pre_market and stock['量比'] in [0, 1]:
                        info_parts.append("量比:待开盘")
                    else:
                        info_parts.append(f"量比:{stock['量比']:5.2f}")

                info_parts.append(f"市值:{market_cap_yi:6.1f}亿")
                info_parts.append(f"得分:{composite_score:.3f}")

                if not is_pre_market:  # 只在开盘后显示风险评分
                    info_parts.append(f"风险:{risk_score:.3f}")

                print(" ".join(info_parts))

        print("\n" + "="*70)
        if is_pre_market:
            print("⚠️  风险提示: 这是开盘前的高级预选结果，请在开盘后结合实时行情再次确认！")
            print("📝 建议: 关注这些股票的开盘表现，设置合理的买入价位")
            print("🔄 策略: 开盘后系统将自动应用完整的技术指标和风险评分")
        else:
            print("⚠️  风险提示: 投资有风险，交易需谨慎！")
            print("📝 建议: 结合基本面分析，设置止损点，控制仓位")
            print("🔄 策略: 建议先模拟盘验证1-3个月后再实盘")
        print("="*70)


def main():
    """主函数 - 演示高级选股流程"""
    print("🎯 启动高级早盘量化选股系统...")

    # 创建高级股票选择器实例
    picker = AdvancedStockPicker(market_mode='normal')

    # 执行选股
    try:
        selected_stocks, stats = picker.select_stocks_advanced(
            trade_date=datetime.now().strftime('%Y%m%d'),
            max_stocks=8,
            auto_adjust_mode=True
        )

        # 显示结果
        picker.display_advanced_results(selected_stocks, stats)

        # 保存结果（如果配置为保存）
        if OUTPUT_CONFIG['save_to_file'] and len(selected_stocks) > 0:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"/tmp/itrading/advanced_selected_stocks_{timestamp}.csv"

            # 选择要保存的列
            save_columns = OUTPUT_CONFIG['display_columns']
            if '综合得分' in selected_stocks.columns:
                save_columns.append('综合得分')
            if '风险评分' in selected_stocks.columns:
                save_columns.append('风险评分')
            if '风险调整得分' in selected_stocks.columns:
                save_columns.append('风险调整得分')

            # 创建保存用的数据副本，并格式化得分列为2位小数
            save_data = selected_stocks[save_columns].copy()
            
            # 格式化得分列为2位小数
            score_columns = ['综合得分', '风险评分', '风险调整得分']
            for col in score_columns:
                if col in save_data.columns:
                    save_data[col] = save_data[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else x)

            save_data.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n💾 选股结果已保存至: {filename}")
    except Exception as e:
        logger.error(f"选股过程中发生错误: {e}")
        print(f"❌ 选股失败: {e}")


if __name__ == "__main__":
    main()

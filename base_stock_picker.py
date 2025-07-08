"""
基于早盘量化选股策略的股票选择器
Base Stock Picker Strategy for Pre-Market Quantitative Stock Selection

基于文档 before_open_pick_adjust_stocks.md 中的策略实现
"""

import os
import logging
import pandas as pd
from typing import Dict, Tuple
import datetime
from datetime import time
from dotenv import load_dotenv

# 导入数据源
import qstock as qs
import tushare as ts
import akshare as ak

from utils import util

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.makedirs('/tmp/itrading', exist_ok=True)

class BaseStockPicker:
    """基础股票选择器类"""
    
    def __init__(self, 
                 min_market_cap: float = 3e9,      # 最小市值30亿
                 max_market_cap: float = 1.5e10,   # 最大市值150亿
                 min_price: float = 5,             # 最低股价5元
                 max_price: float = 50,            # 最高股价50元
                 min_turnover: float = 3,          # 最低换手率3%
                 max_turnover: float = 15,         # 最高换手率15%
                 min_gain: float = 1,              # 最低涨幅1%
                 max_gain: float = 7,              # 最高涨幅7%
                 min_volume_ratio: float = 1.5,    # 最低量比1.5
                 max_volume_ratio: float = 5,      # 最高量比5
                 market_threshold: float = 0.5):   # 市场上涨家数阈值50%
        """
        初始化股票选择器
        
        Args:
            min_market_cap: 最小流通市值（元）
            max_market_cap: 最大流通市值（元）
            min_price: 最低股价（元）
            max_price: 最高股价（元）
            min_turnover: 最低换手率（%）
            max_turnover: 最高换手率（%）
            min_gain: 最低涨幅（%）
            max_gain: 最高涨幅（%）
            min_volume_ratio: 最低量比
            max_volume_ratio: 最高量比
            market_threshold: 市场上涨家数阈值
        """
        self.min_market_cap = min_market_cap
        self.max_market_cap = max_market_cap
        self.min_price = min_price
        self.max_price = max_price
        self.min_turnover = min_turnover
        self.max_turnover = max_turnover
        self.min_gain = min_gain
        self.max_gain = max_gain
        self.min_volume_ratio = min_volume_ratio
        self.max_volume_ratio = max_volume_ratio
        self.market_threshold = market_threshold
        
        # 初始化数据源
        self._init_data_sources()
    
    def _init_data_sources(self):
        """初始化数据源"""
        try:
            # 加载环境变量
            load_dotenv(os.path.expanduser('~/apps/iagent/.env'), verbose=True)
            
            # 初始化Tushare
            tushare_token = os.getenv("TUSHARE_TOKEN")
            if tushare_token:
                ts.set_token(tushare_token)
                self.ts_pro = ts.pro_api()
                logger.info("Tushare API initialized successfully")
            else:
                logger.warning("TUSHARE_TOKEN not found, using alternative data sources")
                self.ts_pro = None
                
        except Exception as e:
            logger.error(f"Failed to initialize data sources: {e}")
            self.ts_pro = None
        
    def get_market_date_tushare(self, trade_date: str | datetime.date | datetime.datetime) -> pd.DataFrame:
        """
        Get market data by trade date using Tushare Pro API.
        
        Args:
            trade_date: 交易日期，可以是字符串、日期对象或时间戳
            
        Returns:
            包含股票数据的DataFrame
        """

        if not self.ts_pro:
            logger.error("Tushare Pro API未配置，无法获取市场数据")
            return pd.DataFrame()
        
        trade_date = util.convert_trade_date(trade_date)
        if not trade_date:
            raise ValueError("无效的交易日期格式")
        
        # 获取当日行情数据
        daily_data = self.ts_pro.daily(
            trade_date=trade_date,
            fields='ts_code,trade_date,close,open,high,low,pre_close,change,pct_chg,vol,amount,turnover_rate'
        )
        if trade_date != datetime.datetime.now().strftime('%Y%m%d'):
            return daily_data
        
        # 获取当日股票列表和基本信息
        stock_basic = self.ts_pro.stock_basic(
            exchange='', 
            list_status='L', 
            fields='ts_code,symbol,name,area,industry,market'
        )
        
        if daily_data.empty:
            logger.info("当日无交易数据，获取最近交易日数据...")
            last_trade_date = util.last_trading_day(trade_date)
            daily_data = self.ts_pro.daily(
                trade_date=last_trade_date,
                fields='ts_code,trade_date,close,open,high,low,pre_close,change,pct_chg,vol,amount,turnover_rate'
            )
            
        # 合并基本信息和行情数据
        df = pd.merge(stock_basic, daily_data, on='ts_code', how='inner')
            
        # 获取实时数据（如果可用）
        # 获取资金流向数据作为量比的替代
        moneyflow = self.ts_pro.moneyflow(
            trade_date=trade_date,
            fields='ts_code,buy_sm_vol,sell_sm_vol'
        )
        df = pd.merge(df, moneyflow, on='ts_code', how='left')
    
        # 标准化列名以匹配现有格式
        df = self._standardize_tushare_columns(df)
            
        logger.info(f"✅ Tushare Pro API成功获取到 {len(df)} 只股票数据")
        return df


    def get_market_data(self, trade_date: str | datetime.date | datetime.datetime) -> pd.DataFrame:
        """
        Get market data by trade date.

        Use the following data sources API by orders: Qstock API -> Akshare API -> Tushare Pro API -> Mock data
        
        Args:
            trade_date: 交易日期，可以是字符串、日期对象或时间戳

        Returns:
            包含股票数据的DataFrame
        """

        trade_date = util.convert_trade_date(trade_date)
        if trade_date < datetime.datetime.now().strftime('%Y%m%d'):
            logger.info(f"获取 {trade_date} 的市场数据 by tushare API and return.")
            return self.get_market_data_tushare(trade_date)
        

        if time(9, 30) <= datetime.datetime.now().time() <= time(11, 30) or \
              time(13, 0) <= datetime.datetime.now().time() <= time(15, 0):
            logger.info(f"获取 {trade_date} 的市场数据 realtime data by qstock/akshare/tushare API.")

        if time(8, 0) <= datetime.datetime.now().time() <= time(9, 30) or \
              time(15, 0) <= datetime.datetime.now().time() <= time(16, 30):
            logger.warning("pre-market(8:00 - before 9:30) or post-market(after 15:00 - 16:30) will init or sync stock data, APIs will connect close error.")

         
        # 第1优先级：使用Qstock API
        try:
            logger.info("第1优先级：尝试使用Qstock API获取市场数据...")
            df = qs.market_realtime()
            logger.info(f"✅ Qstock API成功获取到 {len(df)} 只股票的实时数据")
            return df
        except Exception as e2:
            logger.error(f"❌ Qstock API失败: {e2}")
            
        # 第2优先级：使用Akshare API
        try:
            logger.info("第2优先级：尝试使用Akshare API获取市场数据...")
            df = ak.stock_zh_a_spot() # stock_zh_a_spot_em() cause connect closed error.
            logger.info(f"✅ Akshare API成功获取到 {len(df)} 只股票数据")
            
            # 标准化akshare的列名以匹配格式
            df = self._standardize_akshare_columns(df)
            return df
        except Exception as e:
            logger.error(f"❌ Akshare API失败: {e}")

        try:
            logger.info("第3优先级：尝试使用Tushare API获取市场数据...")
            return self.get_market_date_tushare(trade_date)
        except Exception as e:
            logger.error(f"❌ Tushare Pro API失败: {e}")
            # 最后备用：生成模拟数据用于演示/测试
            logger.warning("🔄 所有API数据源不可用，使用模拟数据进行演示/测试")
            return self._generate_mock_data()
            
    
    def _generate_mock_data(self) -> pd.DataFrame:
        """
        生成模拟股票数据用于演示
        
        Returns:
            包含模拟股票数据的DataFrame
        """
        import numpy as np
        
        # 创建一些模拟股票数据
        mock_stocks = [
            ['000001', '平安银行', 12.50, 12.60, 12.80, 12.30, 12.45, 2.1, 1.2, 8.5, 1000000, 1.26e9, 12.34, 5.2e10, 4.8e10],
            ['000002', '万科A', 18.20, 18.50, 18.65, 18.10, 18.15, 1.8, 0.9, 12.3, 800000, 1.48e9, 18.12, 2.1e11, 1.95e11],
            ['000858', '五粮液', 165.30, 168.20, 170.00, 164.50, 166.80, 1.2, 1.5, 22.1, 500000, 8.41e9, 163.45, 6.5e11, 6.2e11],
            ['600036', '招商银行', 45.80, 46.20, 46.50, 45.60, 45.95, 0.8, 1.1, 9.2, 300000, 1.38e9, 45.75, 1.8e12, 1.7e12],
            ['600519', '贵州茅台', 1680.50, 1705.30, 1720.00, 1675.20, 1690.80, 0.3, 2.1, 35.8, 100000, 1.71e10, 1672.40, 2.1e12, 2.0e12],
            ['000858', '比亚迪', 280.40, 285.60, 290.00, 278.50, 282.30, 2.5, 1.8, 18.6, 600000, 1.71e9, 277.80, 8.2e11, 7.8e11],
            ['002415', '海康威视', 35.60, 36.20, 36.80, 35.40, 35.85, 1.5, 1.3, 15.2, 400000, 1.45e9, 35.45, 3.4e11, 3.2e11],
            ['300059', '东方财富', 18.90, 19.20, 19.50, 18.70, 19.10, 3.2, 2.1, 28.5, 2000000, 3.84e9, 18.75, 2.9e11, 2.8e11],
            ['600050', '中国联通', 5.80, 5.90, 6.00, 5.75, 5.85, 2.8, 1.4, 18.9, 1500000, 8.85e8, 5.75, 1.8e11, 1.7e11],
            ['601318', '中国平安', 62.30, 63.50, 64.00, 62.00, 62.80, 1.6, 1.0, 11.8, 800000, 5.08e9, 62.15, 1.1e12, 1.0e12]
        ]
        
        columns = ['代码', '名称', '昨收', '最新', '最高', '最低', '今开', '涨幅', '换手率', '市盈率', '成交量', '成交额', '量比', '总市值', '流通市值']
        
        df = pd.DataFrame(mock_stocks, columns=columns)
        
        # 计算涨幅
        df['涨幅'] = ((df['最新'] - df['昨收']) / df['昨收'] * 100).round(2)
        
        # 添加一些随机性
        np.random.seed(42)
        df['涨幅'] = df['涨幅'] + np.random.normal(0, 0.5, len(df))
        df['涨幅'] = df['涨幅'].round(2)
        
        # 重新计算最新价
        df['最新'] = (df['昨收'] * (1 + df['涨幅'] / 100)).round(2)
        
        logger.info(f"生成了 {len(df)} 只模拟股票数据")
        return df
    
    def check_market_environment(self, df: pd.DataFrame) -> Tuple[bool, float]:
        """
        检查市场环境
        
        Args:
            df: 市场数据DataFrame
            
        Returns:
            (是否适合选股, 上涨家数占比)
        """
        # 检查数据是否为空
        if df.empty:
            logger.warning("数据为空，无法分析市场环境")
            return False, 0.0
        
        # 检查市场是否开盘 - 通过涨幅列是否有有效数据判断
        gain_col = None
        possible_gain_cols = ['涨幅', '涨跌幅']  # qstock和akshare的涨幅列名
        
        for col in possible_gain_cols:
            if col in df.columns:
                gain_col = col
                break
        
        if gain_col is None:
            logger.warning("未找到涨幅相关列，无法分析市场环境")
            return False, 0.0
        
        # 清理数据：确保涨幅列为数值类型
        try:
            df_clean = df.copy()
            df_clean[gain_col] = pd.to_numeric(df_clean[gain_col], errors='coerce')
            
            # 检查是否有有效的涨幅数据（判断市场是否开盘）
            valid_gain_data = df_clean[df_clean[gain_col].notna()]
            
            if valid_gain_data.empty:
                logger.warning("所有涨幅数据为空，可能市场尚未开盘")
                # 在市场未开盘时，返回中性结果，允许进行基础筛选
                logger.info("市场未开盘，将基于昨日收盘价进行基础筛选")
                return True, 0.5  # 返回中性市场环境，允许选股但设置保守阈值
            
            # 计算上涨家数占比
            up_count = len(valid_gain_data[valid_gain_data[gain_col] > 0])
            total_count = len(valid_gain_data)
            up_ratio = up_count / total_count if total_count > 0 else 0
            
            is_good_market = up_ratio > self.market_threshold
            
            logger.info(f"市场上涨家数占比: {up_ratio:.2%}")
            if is_good_market:
                logger.info("市场环境良好，适合选股")
            else:
                logger.warning("市场环境不佳，建议观望")
                
            return is_good_market, up_ratio
            
        except Exception as e:
            logger.error(f"分析市场环境时出错: {e}")
            return False, 0.0
    
    def filter_risk_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        过滤风险股票
        
        Args:
            df: 股票数据DataFrame
            
        Returns:
            过滤后的DataFrame
        """
        # 检查数据是否为空
        if df.empty:
            logger.warning("输入数据为空，返回空DataFrame")
            return df
        
        # 检查必需列是否存在
        required_columns = ['名称', '代码']
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            logger.warning(f"缺少必需列: {missing_cols}，跳过风险过滤")
            return df
        
        try:
            # 确保列为字符串类型
            df_clean = df.copy()
            df_clean['名称'] = df_clean['名称'].astype(str)
            df_clean['代码'] = df_clean['代码'].astype(str)
            
            # 排除问题股 - 更严格的过滤规则
            exclude_conditions = (
                df_clean['名称'].str.startswith('C') |     # 新股
                df_clean['名称'].str.startswith('N') |     # 新股  
                df_clean['名称'].str.startswith('*ST') |   # *ST股
                df_clean['名称'].str.startswith('ST') |    # ST股
                df_clean['名称'].str.startswith('S') |     # S股
                df_clean['名称'].str.contains('退') |      # 退市股
                df_clean['代码'].str.startswith('C') |     # 新股代码
                df_clean['代码'].str.startswith('N') |     # 新股代码
                df_clean['代码'].str.contains('ST') |      # ST股代码
                df_clean['代码'].str.startswith('*')       # 特殊标记股票
            )
            
            filtered_df = df_clean[~exclude_conditions]
            logger.info(f"过滤风险股票后剩余 {len(filtered_df)} 只股票")
            
            return filtered_df
            
        except Exception as e:
            logger.error(f"过滤风险股票时出错: {e}")
            return df
    
    def apply_selection_criteria(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        应用选股标准
        
        Args:
            df: 股票数据DataFrame
            
        Returns:
            符合条件的股票DataFrame
        """
        # 检查数据是否为空
        if df.empty:
            logger.warning("输入数据为空，返回空DataFrame")
            return df
        
        # 处理不同数据源的列名差异
        column_mapping = {
            # qstock -> standard name (但保留原列名如果新列名不存在)
            '涨跌幅': '涨幅',
            '市盈率-动态': '市盈率'
        }
        
        # 标准化列名（只映射那些确实需要映射的）
        df_clean = df.copy()
        for old_col, new_col in column_mapping.items():
            if old_col in df_clean.columns and new_col not in df_clean.columns:
                df_clean = df_clean.rename(columns={old_col: new_col})
        
        # 检查必需列是否存在
        required_columns = ['流通市值', '市盈率']  # 基础必需列
        price_columns = ['最新价', '最新', '昨收']  # 价格列（任选其一）
        optional_columns = ['涨幅', '涨跌幅', '量比', '换手率']  # 这些列在市场未开盘时可能为空
        
        missing_required = [col for col in required_columns if col not in df_clean.columns]
        
        # 检查是否有价格列，并找到有数据的那个
        available_price_cols = []
        for col in price_columns:
            if col in df_clean.columns:
                # 检查该列是否有有效数据
                valid_count = pd.to_numeric(df_clean[col], errors='coerce').notna().sum()
                if valid_count > 0:
                    available_price_cols.append((col, valid_count))
        
        if missing_required:
            logger.warning(f"缺少必需列进行选股: {missing_required}")
            return pd.DataFrame()
            
        if not available_price_cols:
            logger.warning("没有可用的价格列，无法进行选股")
            return pd.DataFrame()
        
        # 选择数据最多的价格列
        available_price_cols.sort(key=lambda x: x[1], reverse=True)
        price_col = available_price_cols[0][0]
        
        logger.info(f"使用价格列: {price_col}")
        
        try:
            # 清理数据：确保数值列为数值类型
            all_numeric_columns = required_columns + [price_col] + [col for col in optional_columns if col in df_clean.columns]
            for col in all_numeric_columns:
                if col in df_clean.columns:
                    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
            # 只对基础必需列删除NaN
            essential_columns = required_columns + [price_col]
            df_clean = df_clean.dropna(subset=essential_columns)
            
            if df_clean.empty:
                logger.warning("清理基础数据后为空，无法应用选股标准")
                return df_clean
            
            # 为可选列填充默认值（用于市场未开盘的情况）
            if '涨幅' in df_clean.columns:
                df_clean['涨幅'] = df_clean['涨幅'].fillna(0.0)  # 未开盘时涨幅为0
            else:
                df_clean['涨幅'] = 0.0
                
            if '量比' in df_clean.columns:
                df_clean['量比'] = df_clean['量比'].fillna(1.0)  # 未开盘时量比默认为1
            else:
                df_clean['量比'] = 1.0
                
            if '换手率' in df_clean.columns:
                df_clean['换手率'] = df_clean['换手率'].fillna(0.0)  # 未开盘时换手率为0
            else:
                df_clean['换手率'] = 0.0
            
            # 检查是否市场开盘（通过价格数据判断）
            market_open = price_col == '最新价' and not df_clean[price_col].isna().all()
            
            if not market_open and price_col != '昨收':
                logger.info("市场未开盘，基于昨日数据进行基础筛选")
                # 使用昨收价格代替最新价
                if '昨收' in df_clean.columns:
                    df_clean[price_col] = df_clean[price_col].fillna(df_clean['昨收'])
                else:
                    logger.warning("没有昨收价格数据，无法进行筛选")
                    return pd.DataFrame()
            
            # 基本面筛选
            market_cap_condition = (
                (df_clean['流通市值'] >= self.min_market_cap) & 
                (df_clean['流通市值'] <= self.max_market_cap)
            )
            
            price_condition = (
                (df_clean[price_col] >= self.min_price) & 
                (df_clean[price_col] <= self.max_price)
            )
            
            positive_pe_condition = df_clean['市盈率'] > 0  # 盈利企业
            
            # 根据市场开盘状态调整筛选条件
            if market_open:
                # 市场开盘时应用完整的量价指标筛选
                turnover_condition = (
                    (df_clean['换手率'] >= self.min_turnover) & 
                    (df_clean['换手率'] <= self.max_turnover)
                )
                
                gain_condition = (
                    (df_clean['涨幅'] >= self.min_gain) & 
                    (df_clean['涨幅'] <= self.max_gain)
                )
                
                volume_ratio_condition = (
                    (df_clean['量比'] >= self.min_volume_ratio) & 
                    (df_clean['量比'] <= self.max_volume_ratio)
                )
                
                # 综合筛选
                selected = df_clean[
                    market_cap_condition & 
                    price_condition & 
                    positive_pe_condition & 
                    turnover_condition & 
                    gain_condition & 
                    volume_ratio_condition
                ]
                
                logger.info(f"应用完整选股标准后剩余 {len(selected)} 只股票")
            else:
                # 市场未开盘时只应用基本面筛选
                selected = df_clean[
                    market_cap_condition & 
                    price_condition & 
                    positive_pe_condition
                ]
                
                logger.info(f"应用基础选股标准后剩余 {len(selected)} 只股票（市场未开盘）")
            
            return selected
            
        except Exception as e:
            logger.error(f"应用选股标准时出错: {e}")
            return pd.DataFrame()
    
    def rank_stocks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        对股票进行排序
        
        Args:
            df: 符合条件的股票DataFrame
            
        Returns:
            排序后的DataFrame
        """
        if df.empty:
            return df
        
        # 检查是否有量比数据（判断市场是否开盘）
        if '量比' in df.columns and not df['量比'].isna().all() and (df['量比'] != 1.0).any():
            # 市场开盘时按量比降序排列
            ranked_df = df.sort_values('量比', ascending=False)
            # 添加综合得分
            ranked_df = self._calculate_composite_score(ranked_df)
        else:
            # 市场未开盘时按市值排序（小市值优先）
            if '流通市值' in df.columns:
                ranked_df = df.sort_values('流通市值', ascending=True)
                logger.info("市场未开盘，按流通市值升序排列")
            else:
                ranked_df = df.copy()
        
        return ranked_df
    
    def _calculate_composite_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算综合得分
        
        Args:
            df: 股票数据DataFrame
            
        Returns:
            添加综合得分的DataFrame
        """
        if df.empty:
            return df
        
        df = df.copy()
        
        # 检查是否有有效的交易数据
        has_trading_data = (
            '量比' in df.columns and not df['量比'].isna().all() and (df['量比'] != 1.0).any()
        )
        
        if has_trading_data:
            # 市场开盘时的完整评分
            # 标准化各项指标 (0-1范围)
            if df['量比'].max() > df['量比'].min():
                df['量比_标准化'] = (df['量比'] - df['量比'].min()) / (df['量比'].max() - df['量比'].min())
            else:
                df['量比_标准化'] = 0.5
            
            if '换手率' in df.columns and df['换手率'].max() > df['换手率'].min():
                df['换手率_标准化'] = (df['换手率'] - df['换手率'].min()) / (df['换手率'].max() - df['换手率'].min())
            else:
                df['换手率_标准化'] = 0.5
            
            # 处理涨幅列名差异
            gain_col = '涨幅' if '涨幅' in df.columns else '涨跌幅' if '涨跌幅' in df.columns else None
            if gain_col and df[gain_col].max() > df[gain_col].min():
                df['涨幅_标准化'] = (df[gain_col] - df[gain_col].min()) / (df[gain_col].max() - df[gain_col].min())
            else:
                df['涨幅_标准化'] = 0.5
            
            # 计算综合得分（权重可调整）
            df['综合得分'] = (
                df['量比_标准化'] * 0.4 +      # 量比权重40%
                df['换手率_标准化'] * 0.3 +    # 换手率权重30%
                df['涨幅_标准化'] * 0.3        # 涨幅权重30%
            )
            
            # 按综合得分重新排序
            df = df.sort_values('综合得分', ascending=False)
        else:
            # 市场未开盘时的简化评分（基于基本面）
            # 按市值反向排序（小市值给更高分）
            if '流通市值' in df.columns and df['流通市值'].max() > df['流通市值'].min():
                df['市值_标准化'] = 1 - (df['流通市值'] - df['流通市值'].min()) / (df['流通市值'].max() - df['流通市值'].min())
            else:
                df['市值_标准化'] = 0.5
                
            # 按市盈率评分（合理市盈率给更高分）
            if '市盈率' in df.columns:
                # 市盈率在15-25之间给最高分
                pe_scores = []
                for pe in df['市盈率']:
                    if pd.isna(pe) or pe <= 0:
                        pe_scores.append(0)
                    elif 15 <= pe <= 25:
                        pe_scores.append(1.0)
                    elif 10 <= pe < 15 or 25 < pe <= 35:
                        pe_scores.append(0.8)
                    elif 5 <= pe < 10 or 35 < pe <= 50:
                        pe_scores.append(0.6)
                    else:
                        pe_scores.append(0.3)
                df['市盈率_标准化'] = pe_scores
            else:
                df['市盈率_标准化'] = 0.5
            
            # 计算基础综合得分
            df['综合得分'] = (
                df['市值_标准化'] * 0.6 +      # 市值权重60%
                df['市盈率_标准化'] * 0.4      # 市盈率权重40%
            )
            
            # 按综合得分排序
            df = df.sort_values('综合得分', ascending=False)
        
        return df
    
    def select_stocks(self, max_stocks: int = 10) -> Tuple[pd.DataFrame, Dict]:
        """
        执行选股流程
        
        Args:
            max_stocks: 最大选择股票数量
            
        Returns:
            (选中的股票DataFrame, 选股统计信息)
        """
        logger.info("开始执行选股流程...")
        
        # 1. 获取市场数据
        market_data = self.get_market_data()

        # 2. 检查市场环境
        is_good_market, up_ratio = self.check_market_environment(market_data)
        
        stats = {
            'total_stocks': len(market_data),
            'up_ratio': up_ratio,
            'is_good_market': is_good_market,
            'selection_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 如果市场环境不佳，返回空结果 (但允许预开盘筛选)
        if not is_good_market and up_ratio != 0.5:
            logger.warning("市场环境不佳，不进行选股")
            return pd.DataFrame(), stats
        
        # 3. 过滤风险股票
        filtered_data = self.filter_risk_stocks(market_data)
        stats['after_risk_filter'] = len(filtered_data)
        
        # 4. 应用选股标准
        selected_stocks = self.apply_selection_criteria(filtered_data)
        stats['after_criteria_filter'] = len(selected_stocks)
        
        # 5. 排序股票
        ranked_stocks = self.rank_stocks(selected_stocks)
        
        # 6. 限制数量
        final_stocks = ranked_stocks.head(max_stocks)
        stats['final_selection'] = len(final_stocks)
        
        logger.info(f"选股完成，最终选出 {len(final_stocks)} 只股票")
        
        return final_stocks, stats
    
    def display_results(self, selected_stocks: pd.DataFrame, stats: Dict):
        """
        显示选股结果
        
        Args:
            selected_stocks: 选中的股票DataFrame
            stats: 选股统计信息
        """
        print("\n" + "="*60)
        print("📊 早盘量化选股结果")
        print("="*60)
        
        print(f"选股时间: {stats['selection_time']}")
        print(f"市场总股票数: {stats['total_stocks']}")
        print(f"市场上涨家数占比: {stats['up_ratio']:.2%}")
        print(f"市场环境评估: {'✅ 适合选股' if stats['is_good_market'] else '❌ 不适合选股'}")
        
        # 判断是否为市场开盘前的情况
        is_pre_market = stats['up_ratio'] == 0.5 and stats['is_good_market']
        
        if not stats['is_good_market'] and not is_pre_market:
            print("\n⚠️  市场环境不佳，建议观望")
            return
        
        if is_pre_market:
            print("\n📢 当前为市场开盘前，基于昨日数据进行基础筛选")
        
        print("\n筛选过程:")
        print(f"  风险股票过滤后: {stats['after_risk_filter']} 只")
        print(f"  选股标准过滤后: {stats['after_criteria_filter']} 只")
        print(f"  最终选中: {stats['final_selection']} 只")
        
        if len(selected_stocks) > 0:
            if is_pre_market:
                print(f"\n🎯 预选 {len(selected_stocks)} 只潜力股（待开盘确认）:")
            else:
                print(f"\n🎯 今日精选 {len(selected_stocks)} 只潜力股:")
            print("-" * 60)
            
            # 显示主要字段，处理列名差异
            for idx, (_, stock) in enumerate(selected_stocks.iterrows(), 1):
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
                if '涨幅' in selected_stocks.columns and pd.notna(stock['涨幅']):
                    gain = stock['涨幅']
                elif '涨跌幅' in selected_stocks.columns and pd.notna(stock['涨跌幅']):
                    gain = stock['涨跌幅']
                
                market_cap_yi = stock['流通市值'] / 1e8 if pd.notna(stock['流通市值']) else 0
                
                # 构建显示字符串
                info_parts = [f"{idx:2d}. {stock['代码']} {stock['名称']:8s}"]
                
                if price:
                    info_parts.append(f"价格:{price:6.2f}")
                
                if gain is not None:
                    if is_pre_market and gain == 0:
                        info_parts.append("涨幅:待开盘")
                    else:
                        info_parts.append(f"涨幅:{gain:5.2f}%")
                
                if '市盈率' in selected_stocks.columns and pd.notna(stock['市盈率']):
                    info_parts.append(f"PE:{stock['市盈率']:5.1f}")
                
                info_parts.append(f"市值:{market_cap_yi:6.1f}亿")
                
                if '综合得分' in selected_stocks.columns and pd.notna(stock['综合得分']):
                    info_parts.append(f"得分:{stock['综合得分']:4.2f}")
                
                print(" ".join(info_parts))
        
        print("\n" + "="*60)
        if is_pre_market:
            print("⚠️  风险提示: 这是开盘前的预选结果，请在开盘后结合实时行情再次确认！")
            print("📝 建议: 关注这些股票的开盘表现，设置合理的买入价位")
        else:
            print("⚠️  风险提示: 投资有风险，交易需谨慎！")
            print("📝 建议: 结合基本面分析，设置止损点，控制仓位")
        print("="*60)
    
    def _standardize_tushare_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        标准化Tushare数据列名
        
        Args:
            df: Tushare数据DataFrame
            
        Returns:
            标准化后的DataFrame
        """
        # Tushare字段映射到标准格式
        tushare_column_mapping = {
            'ts_code': '代码',
            'symbol': '代码',
            'name': '名称',
            'close': '最新',
            'open': '今开',
            'high': '最高',
            'low': '最低',
            'pre_close': '昨收',
            'change': '涨跌',
            'pct_chg': '涨幅',
            'vol': '成交量',
            'amount': '成交额',
            'turnover_rate': '换手率'
        }
        
        # 重命名列
        df_clean = df.copy()
        for old_col, new_col in tushare_column_mapping.items():
            if old_col in df_clean.columns:
                df_clean = df_clean.rename(columns={old_col: new_col})
        
        # 处理代码格式（Tushare格式为000001.SZ，需要转换为000001）
        if '代码' in df_clean.columns:
            df_clean['代码'] = df_clean['代码'].astype(str).str.split('.').str[0]
        
        # 计算缺失的字段
        if '涨幅' in df_clean.columns:
            df_clean['涨幅'] = pd.to_numeric(df_clean['涨幅'], errors='coerce')
        
        # 估算市盈率（简化计算）
        if '最新' in df_clean.columns and '市盈率' not in df_clean.columns:
            df_clean['市盈率'] = 15.0  # 使用平均市盈率
        
        # 估算量比（简化处理）
        if '量比' not in df_clean.columns:
            df_clean['量比'] = 1.0
        
        # 估算总市值和流通市值（需要获取股本数据，这里简化处理）
        if '总市值' not in df_clean.columns and '最新' in df_clean.columns:
            df_clean['总市值'] = 1e10  # 简化为100亿
            df_clean['流通市值'] = 8e9  # 简化为80亿
        
        return df_clean
    
    def _standardize_akshare_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        标准化akshare数据列名
        
        Args:
            df: akshare数据DataFrame
            
        Returns:
            标准化后的DataFrame
        """
        akshare_column_mapping = {
            '代码': '代码',
            '名称': '名称', 
            '涨跌幅': '涨幅',
            '最新价': '最新',
            '最高': '最高',
            '最低': '最低',
            '今开': '今开',
            '换手率': '换手率',
            '量比': '量比',
            '市盈率-动态': '市盈率',
            '成交量': '成交量',
            '成交额': '成交额',
            '昨收': '昨收',
            '总市值': '总市值',
            '流通市值': '流通市值'
        }
        
        # 重命名列以保持一致性
        df_clean = df.copy()
        for old_col, new_col in akshare_column_mapping.items():
            if old_col in df_clean.columns and old_col != new_col:
                df_clean = df_clean.rename(columns={old_col: new_col})
        
        return df_clean

    # ...existing code...
def main():
    """主函数 - 演示选股流程"""
    # 创建股票选择器实例
    picker = BaseStockPicker()
    
    # 执行选股
    try:
        selected_stocks, stats = picker.select_stocks(max_stocks=8)
        
        # 显示结果
        picker.display_results(selected_stocks, stats)
        
        # 保存结果（可选）
        if len(selected_stocks) > 0:
            filename = f"/tmp/itrading/selected_stocks_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            selected_stocks.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"\n💾 选股结果已保存至: {filename}")
            
    except Exception as e:
        logger.error(f"选股过程中发生错误: {e}")
        print(f"❌ 选股失败: {e}")


if __name__ == "__main__":
    main()

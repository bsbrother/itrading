# Tushare API 集成说明

## 概述
高级股票选择器现已集成Tushare Pro API作为主要数据源，提供更稳定和准确的股票数据。

## Tushare API 优势
1. **数据质量高**: 提供高质量的财务和行情数据
2. **API稳定**: 相比其他免费API更稳定可靠
3. **数据完整**: 包含基本面数据、行情数据等
4. **更新及时**: 数据更新频率高

## 数据源优先级
按照项目指导原则，系统使用以下优先级顺序：
1. **Tushare Pro API** (主要)
2. **Akshare API** (备用)
3. **Qstock API** (备用)
4. **模拟数据** (演示/测试)

## 配置要求
需要在 `~/apps/iagent/.env` 文件中配置:
```
TUSHARE_TOKEN=your_tushare_token_here
```

## Tushare数据字段映射
```python
tushare_column_mapping = {
    'ts_code': '代码',       # 股票代码
    'name': '名称',          # 股票名称
    'close': '最新',         # 最新价
    'open': '今开',          # 今开盘价
    'high': '最高',          # 最高价
    'low': '最低',           # 最低价
    'pre_close': '昨收',     # 昨收盘价
    'pct_chg': '涨幅',       # 涨跌幅
    'vol': '成交量',         # 成交量
    'amount': '成交额',      # 成交额
    'turnover_rate': '换手率' # 换手率
}
```

## 功能特性
- 自动获取最近交易日数据
- 智能数据源切换
- 数据格式标准化
- 错误处理和日志记录

## 使用示例
```python
from base_stock_picker import BaseStockPicker

# 创建选股器实例（自动使用Tushare API）
picker = BaseStockPicker()

# 获取市场数据
market_data = picker.get_market_data()

# 执行选股
selected_stocks = picker.apply_selection_criteria(market_data)
```

## 注意事项
1. 需要有效的Tushare Pro Token
2. Tushare API有调用频率限制
3. 系统会自动处理API错误并切换到备用数据源
4. 非交易日会自动获取最近交易日数据

## 更新历史
- 2025-07-08: 集成Tushare Pro API作为主要数据源
- 2025-07-08: 添加数据源优先级和智能切换
- 2025-07-08: 完善错误处理和日志记录

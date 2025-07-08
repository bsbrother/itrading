# iTrading - 早盘量化选股系统

## 📊 项目简介

iTrading是一个基于量化分析的早盘选股系统，旨在帮助投资者在开盘15分钟内精准捕捉主力启动信号。系统采用多维度指标分析，结合市值、股价、换手率、量比等因子，构建科学的选股框架。

**🔥 最新更新**: 支持开盘前预选股功能，9:30前即可基于昨日数据进行基础筛选！

## 🎯 核心特性

### 基础选股器 (BaseStockPicker)
- **全时段选股**: 开盘前基于昨收数据筛选，开盘后实时量价分析
- **市场环境判断**: 通过上涨家数占比判断市场情绪，支持预开盘模式
- **风险股票过滤**: 自动排除新股、ST股、退市股等风险标的
- **多维度筛选**: 市值、股价、换手率、量比、涨幅等指标综合筛选
- **智能排序**: 基于量比和综合得分的排序算法
- **数据源容错**: qstock + akshare双重保障，自动处理网络异常

### 高级选股器 (AdvancedStockPicker)
- **全时段高级选股**: 开盘前基于昨收数据智能筛选，开盘后完整技术面分析
- **自适应市场模式**: 支持牛市、熊市、震荡市等不同模式，自动环境识别
- **技术面过滤**: 结合技术指标进行二次筛选（开盘后生效）
- **风险评分系统**: 波动率、估值、流动性等多维度风险评估
- **动态参数调整**: 根据市场环境自动调整选股参数
- **智能模式切换**: 预开盘保守模式，开盘后完整评分

## 🚀 快速开始

### 环境要求
- Python 3.12+
- uv (推荐的包管理器)

### 安装依赖
```bash
# 使用uv安装依赖
uv pip install -r requirements.txt

# 或者使用pip
pip install -r requirements.txt
```

### 环境配置
1. 创建环境变量文件 `~/apps/iagent/.env`
2. 配置API密钥:
```env
TUSHARE_TOKEN=your_tushare_token
GEMINI_API_KEY=your_gemini_api_key
```

### 基础使用
```python
from base_stock_picker import BaseStockPicker

# 创建选股器实例
picker = BaseStockPicker()

# 执行选股
selected_stocks, stats = picker.select_stocks(max_stocks=8)

# 显示结果
picker.display_results(selected_stocks, stats)
```

### 高级使用
```python
from advanced_stock_picker import AdvancedStockPicker

# 创建高级选股器(支持不同市场模式)
picker = AdvancedStockPicker(market_mode='normal')

# 执行高级选股(支持自动模式调整)
selected_stocks, stats = picker.select_stocks_advanced(
    max_stocks=8,
    auto_adjust_mode=True
)

# 显示结果
picker.display_advanced_results(selected_stocks, stats)
```

### 🕘 开盘前使用（9:30前）

#### 基础选股器
```bash
# 开盘前运行，基于昨收数据进行基础筛选
uv run python base_stock_picker.py

# 输出示例:
# 📢 当前为市场开盘前，基于昨日数据进行基础筛选
# 🎯 预选 8 只潜力股（待开盘确认）:
#  1. 002616 长青集团     价格:  6.38 涨幅:待开盘 PE: 14.6 市值:  30.0亿
```

#### 高级选股器
```bash
# 开盘前运行，基于昨收数据进行高级筛选
uv run python advanced_stock_picker.py

# 输出示例:
# 📢 当前为市场开盘前，基于昨日数据进行高级筛选
# 🎯 高级预选 8 只潜力股（待开盘确认）:
#  1. 000319 股票319    价格: 19.86 涨幅:待开盘 换手:待开盘 量比:待开盘 市值: 50.0亿 得分:0.674
```

### 🕘 开盘后使用（9:30后）

#### 基础选股器
```bash
# 开盘后运行，基于实时数据进行完整筛选
uv run python base_stock_picker.py

# 输出示例:
# 🎯 今日精选 8 只潜力股:
#  1. 002616 长青集团     价格:  6.45 涨幅: 1.10% 换手: 4.2% 量比: 2.1 市值:  30.3亿
```

#### 高级选股器
```bash
# 开盘后运行，基于实时数据进行高级筛选
uv run python advanced_stock_picker.py

# 输出示例:
# 🎯 今日精选 8 只潜力股:
#  1. 600744 华银电力     价格: 7.25 涨幅: 8.21% 换手:14.37% 量比: 9.15 市值: 147.3亿 得分:0.423 风险:0.301
```

## 📁 项目结构

```
itrading/
├── base_stock_picker.py          # 基础选股器
├── advanced_stock_picker.py      # 高级选股器
├── config.py                     # 配置文件
├── test_demo.py                  # 测试演示工具
├── requirements.txt              # 依赖包
├── pyproject.toml               # 项目配置
├── README.md                    # 项目说明
├── before_open_pick_adjust_stocks.md  # 策略文档
├── docs/                        # 文档目录
└── tests/                       # 测试目录
    └── test_gemini.py          # Gemini API测试
```

## 🔧 配置说明

### 主要配置参数

- **市值范围**: 30-150亿元流通市值
- **股价范围**: 5-50元股价区间
- **换手率**: 3%-15%换手率范围
- **涨幅**: 1%-7%涨幅区间
- **量比**: 1.5-5倍量比范围
- **市场阈值**: 50%上涨家数占比阈值

### 市场模式配置

系统支持以下市场模式：
- **normal**: 正常市场模式
- **bull_market**: 牛市模式(放宽选股条件)
- **bear_market**: 熊市模式(收紧选股条件)
- **volatile_market**: 震荡市模式(平衡选股条件)

## 📊 选股策略

### 选股逻辑
1. **市场环境检查**: 上涨家数占比>50%才进行选股
2. **风险股票过滤**: 排除新股、ST股、退市股
3. **基本面筛选**: 中小市值、合理股价、盈利企业
4. **技术面筛选**: 适度换手率、温和放量、合理涨幅
5. **综合排序**: 量比、换手率、涨幅等指标综合评分

### 风险控制
- **止损设置**: 建议设置5%-8%止损点
- **仓位管理**: 单股仓位不超过总资金10%
- **分散投资**: 选择3-8只股票分散风险
- **模拟验证**: 建议先用模拟盘验证1-3个月

## 🧪 测试和验证

### 运行测试
```bash
# 运行基础演示和测试
uv run python test_demo.py

# 运行边缘案例测试 (推荐)
uv run python test_edge_cases.py

# 运行基础选股器
uv run python base_stock_picker.py

# 运行高级选股器
uv run python advanced_stock_picker.py
```

### 测试覆盖
- ✅ **基础功能测试**: 选股器核心功能验证
- ✅ **边缘案例测试**: 空数据、无效数据、极端值处理
- ✅ **性能测试**: 大数据集处理能力(10000+股票)
- ✅ **市场模式测试**: 牛市、熊市、震荡市场适应性
- ✅ **错误处理测试**: 异常情况的优雅处理

## 📝 数据来源

系统支持多种数据源：
- **Qstock**: 主要实时数据源
- **Tushare**: 备用数据源和历史数据
- **Akshare**: 备用数据源

## ⚠️ 风险提示

- **投资有风险，入市需谨慎**
- 本系统仅供学习和参考，不构成投资建议
- 量化选股只是工具，需结合基本面分析
- 建议先在模拟环境中充分测试
- 实盘操作前请制定详细的风险控制策略

## 🔄 更新日志

### v0.1.1 (2025-07-07)
- ✅ **边缘案例处理**: 修复空数据、无效数据类型处理
- ✅ **数据验证增强**: 改进数据清理和类型转换
- ✅ **错误处理优化**: 所有方法添加异常处理
- ✅ **性能提升**: 大数据集处理优化(10000+股票)
- ✅ **特殊股票过滤**: 改进ST股票和新股过滤规则
- ✅ **测试覆盖**: 新增全面的边缘案例测试
- ✅ **代码质量**: 移除未使用代码，改进日志记录

### v0.1.0 (2025-01-07)
- 初始版本发布
- 实现基础选股器功能
- 实现高级选股器功能
- 添加配置文件和测试工具
- 完善文档和说明

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue到GitHub仓库
- 发送邮件至项目维护者

## 📄 许可证

本项目采用MIT许可证，详情请参见LICENSE文件。

---

**声明**: 本项目仅用于学习和研究目的，不承担任何投资损失责任。投资者应当根据自己的风险承受能力和投资目标，谨慎做出投资决策。

### Next TODO:
  - [Intellectia.ai](https://app.intellectia.ai/)
    Offers an AI Stock Picker that provides precision-driven stock recommendations for intraday trading, using Large Language Models (LLMs) to analyze market data in real-time.

  - [Kavout](https://www.kavout.com/ai-stock-picker)
    Uses AI and machine learning to analyze data and identify potentially high-performing stocks, with features like customizable screening and real-time adaptability.


## Auto Mobile Trading

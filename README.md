# iTrading - 早盘量化选股系统

## 📊 项目简介

iTrading是一个基于量化分析的早盘选股系统，旨在帮助投资者在开盘15分钟内精准捕捉主力启动信号。系统采用多维度指标分析，结合市值、股价、换手率、量比等因子，构建科学的选股框架。

**🔥 最新更新**: 
- 集成Tushare Pro API作为主要数据源，提供更稳定准确的数据
- 支持开盘前预选股功能，9:30前即可基于昨日数据进行基础筛选
- 智能数据源切换，确保系统高可用性

## 🎯 核心特性

### 数据源系统
按照项目指导原则，系统使用以下优先级顺序：
- **Tushare Pro API** (主要): 高质量财务和行情数据
- **Akshare API** (备用): 实时行情数据
- **Qstock API** (备用): 实时股票数据  
- **模拟数据** (演示/测试): 系统演示和测试

### 基础选股器 (BaseStockPicker)
- **全时段选股**: 开盘前基于昨收数据筛选，开盘后实时量价分析
- **市场环境判断**: 通过上涨家数占比判断市场情绪，支持预开盘模式
- **风险股票过滤**: 自动排除新股、ST股、退市股等风险标的
- **多维度筛选**: 市值、股价、换手率、量比、涨幅等指标综合筛选
- **智能排序**: 基于量比和综合得分的排序算法
- **数据源容错**: 多重数据源保障，自动处理网络异常

### 高级选股器 (AdvancedStockPicker)
- **全时段高级选股**: 开盘前基于昨收数据智能筛选，开盘后完整技术面分析
- **自适应市场模式**: 支持牛市、熊市、震荡市等不同模式，自动环境识别
- **技术面过滤**: 结合技术指标进行二次筛选（开盘后生效）
- **风险评分系统**: 波动率、估值、流动性等多维度风险评估
- **动态参数调整**: 根据市场环境自动调整选股参数
- **智能模式切换**: 预开盘保守模式，开盘后完整评分

### 统一股票选股AI分析器 (UnifiedStockPickAIAnalyzer) 🆕
- **完整选股流程**: 自动调用高级选股器进行股票筛选
- **AI深度分析**: 基于Google Gemini的25项财务指标分析和综合新闻情绪分析
- **最终得分统一**: 整合流通市值、综合得分、风险评分、风险调整得分和AI得分
- **智能排序**: 基于最终得分的多维度综合排序
- **完整报告**: 提供详细的选股结果和AI分析报告
- **自动保存**: 支持结果自动保存为CSV和统计信息

## 🤖 AI增强分析

### 统一选股AI分析器
`unify_stock_pick_ai_analyzer.py` 提供完整的选股+AI分析解决方案：

**核心功能：**
- 自动选股：调用高级选股器筛选优质股票
- AI深度分析：基于Google Gemini的25项财务指标分析
- 综合新闻情绪分析：整合公司新闻、公告、研究报告
- 最终得分统一：多维度得分加权计算
- 智能排序：按最终得分综合排名

**得分组成 (final_score)：**
- 流通市值 (15%) - 适中规模优先
- 综合得分 (25%) - 选股器基础得分
- 风险评分 (20%) - 风险越低越好
- 风险调整得分 (20%) - 风险调整后表现
- AI得分 (20%) - AI综合评估

**使用建议：**
- 建议选股数量6只以内，AI分析耗时较长
- 网络状况良好时使用，确保AI API稳定
- 结合技术分析进行最终投资决策
- 关注AI分析中的风险提示

## 🚀 快速开始

### 环境要求
- Python 3.12+
- uv (推荐的包管理器)
- Reflex框架 (Web界面)

### 安装依赖
```bash
# 使用uv安装依赖 (推荐)
uv sync

# 或者手动安装
uv pip install -r requirements.txt

# 或者使用pip
pip install -r requirements.txt
```

### Web界面启动
```bash
# 启动Reflex Web应用
uv run reflex run

# 或者直接运行
uv run python app.py
```

Web界面将在 http://localhost:3000 启动，提供：
- 可视化股票筛选界面
- 实时股票推荐展示
- 交互式参数调整
- 股票选择和管理功能

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

### 统一AI选股分析
```python
from unify_stock_pick_ai_analyzer import UnifiedStockPickAIAnalyzer

# 创建统一分析器
analyzer = UnifiedStockPickAIAnalyzer(market_mode='normal')

# 执行完整的选股+AI分析
enhanced_stocks, stats = analyzer.pick_and_analyze_stocks(
    max_stocks=6,  # 建议6只以内，AI分析耗时较长
    auto_adjust_mode=True
)

# 显示完整结果
analyzer.display_unified_results(enhanced_stocks, stats)

# 保存结果
analyzer.save_results(enhanced_stocks, stats)
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

#### 统一AI选股分析器
```bash
# 执行完整的选股+AI分析流程
uv run python unify_stock_pick_ai_analyzer.py

# 输出示例:
# 🚀 统一股票选股AI分析结果
# 分析时间: 2025-07-08 14:30:15
# 交易日期: 20250708
# 最终选股数量: 6
# AI分析完成: ✅
# 
# 📊 详细选股结果 (共6只):
# 股票代码  股票名称   最新价  涨跌幅   流通市值  综合得分  风险调整得分  ai_score  final_score
# 600519    贵州茅台   1680.5  2.15%   21045.6亿   85.32      78.45       92.50      86.78
```

## 📁 项目结构

```
itrading/
├── ai_stock_analyzer.py          # AI股票分析器 (Google Gemini)
├── base_stock_picker.py          # 基础选股器
├── advanced_stock_picker.py      # 高级选股器
├── config.py                     # 配置文件
├── test_demo.py                  # 测试演示工具
├── requirements.txt              # 依赖包
├── pyproject.toml               # 项目配置
├── README.md                    # 项目说明
├── utils/                       # 工具模块
│   └── cons.py                 # 交易日期工具函数
├── docs/                        # 文档目录
│   └── trading_day_utils_implementation.md  # 交易日工具实现文档
├── demo_unified_analyzer.py    # 统一分析器演示
└── tests/                       # 测试目录
    ├── test_gemini.py          # Gemini API测试
    └── test_cons_utils.py      # 交易日工具测试
```

## 🗓️ 交易日工具 (Trading Day Utilities)

系统提供完整的中国A股交易日计算功能：

### 核心功能
- **交易日判断**: 准确判断某日是否为A股交易日
- **上个交易日**: 计算给定日期的上一个交易日
- **下个交易日**: 计算给定日期的下一个交易日
- **日期格式转换**: 支持多种日期格式的统一转换

### 中国A股规则
- **交易时间**: 周一至周五 9:30-11:30, 13:00-15:00
- **休市日期**: 周末及中国法定节假日
- **节假日覆盖**: 元旦、春节、清明节、劳动节、端午节、中秋节、国庆节

### 使用示例
```python
from utils.cons import is_trading_day, last_trading_day, next_trading_day, convert_trade_date
import datetime

# 检查今天是否为交易日
if is_trading_day(datetime.date.today()):
    print("今天市场开盘")

# 获取上一个交易日
last_day = last_trading_day("2025-07-06")  # 周日 -> "20250704" (周五)

# 获取下一个交易日  
next_day = next_trading_day("20250101")    # 元旦 -> "20250102"

# 日期格式转换
trade_date = convert_trade_date("2025-07-08")  # -> "20250708"
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

# 运行统一AI选股分析器演示
uv run python tests/demo_unified_analyzer.py
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

### v0.1.3 (2025-07-08)
- ✅ **交易日工具**: 新增完整的中国A股交易日计算工具(`utils/cons.py`)
  - `is_trading_day()`: 判断是否为交易日
  - `last_trading_day()`: 获取上一个交易日
  - `next_trading_day()`: 获取下一个交易日  
  - `convert_trade_date()`: 日期格式转换和验证
- ✅ **中国节假日支持**: 覆盖2024-2026年主要节假日
- ✅ **测试覆盖**: 新增全面的交易日工具测试套件
- ✅ **文档完善**: 新增交易日工具实现文档

### v0.1.2 (2025-07-08)
- ✅ **CSV输出格式优化**: 综合得分、风险评分、风险调整得分格式化为2位小数(.2f)
- ✅ **数据精度改进**: 提升CSV文件的可读性和专业性
- ✅ **文件输出标准化**: 统一评分字段的数值格式

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

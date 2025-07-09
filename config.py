"""
股票选择器配置文件
Stock Picker Configuration
"""

# Stock category and code filters
STOCK_CATEGORY_FILTER_CONFIG = {
    'A_main_board': "6*, ^688*, 0*, ^30*, ^8*, ^4*",
}

# 市值范围配置 (单位: 元)
MARKET_CAP_CONFIG = {
    'min_market_cap': 3e9,      # 最小流通市值 30亿
    'max_market_cap': 1.5e10,   # 最大流通市值 150亿
}

# 股价范围配置 (单位: 元)
PRICE_CONFIG = {
    'min_price': 5,             # 最低股价 5元
    'max_price': 50,            # 最高股价 50元
}

# 换手率配置 (单位: %)
TURNOVER_CONFIG = {
    'min_turnover': 3,          # 最低换手率 3%
    'max_turnover': 15,         # 最高换手率 15%
}

# 涨幅配置 (单位: %)
GAIN_CONFIG = {
    'min_gain': 1,              # 最低涨幅 1%
    'max_gain': 7,              # 最高涨幅 7%
}

# 量比配置
VOLUME_RATIO_CONFIG = {
    'min_volume_ratio': 1.5,    # 最低量比 1.5
    'max_volume_ratio': 5,      # 最高量比 5
}

# 市场环境配置
MARKET_CONFIG = {
    'market_threshold': 0.5,    # 市场上涨家数阈值 50%
}

# 选股数量配置
SELECTION_CONFIG = {
    'max_stocks': 8,            # 最大选择股票数量
}

# 综合得分权重配置
SCORE_WEIGHTS = {
    'volume_ratio_weight': 0.4, # 量比权重 40%
    'turnover_weight': 0.3,     # 换手率权重 30%
    'gain_weight': 0.3,         # 涨幅权重 30%
}

# 风险控制配置
RISK_CONFIG = {
    'exclude_new_stocks': True,     # 排除新股
    'exclude_st_stocks': True,      # 排除ST股
    'exclude_delisting': True,      # 排除退市股
    'require_positive_pe': True,    # 要求正市盈率(盈利企业)
}

# 不同市场环境下的参数调整
MARKET_ENVIRONMENT_ADJUSTMENTS = {
    'bull_market': {  # 牛市参数
        'max_gain': 10,           # 提高涨幅上限
        'max_turnover': 20,       # 提高换手率上限
        'min_market_cap': 2e9,    # 降低市值下限
    },
    'bear_market': {  # 熊市参数
        'max_gain': 5,            # 降低涨幅上限
        'max_turnover': 10,       # 降低换手率上限
        'min_market_cap': 5e9,    # 提高市值下限
    },
    'volatile_market': {  # 震荡市参数
        'min_gain': 0.5,          # 降低涨幅下限
        'max_gain': 6,            # 适中涨幅上限
        'min_volume_ratio': 1.2,  # 降低量比要求
    }
}

# 行业权重配置 (根据市场轮动调整)
INDUSTRY_WEIGHTS = {
    'technology': 1.0,      # 科技
    'healthcare': 1.0,      # 医疗
    'consumer': 1.0,        # 消费
    'finance': 0.8,         # 金融
    'industrial': 0.9,      # 工业
    'materials': 0.7,       # 材料
    'energy': 0.6,          # 能源
    'utilities': 0.5,       # 公用事业
}

# 输出格式配置
OUTPUT_CONFIG = {
    'save_to_file': True,       # 是否保存到文件
    'file_format': 'csv',       # 文件格式 ('csv', 'excel')
    'include_charts': False,    # 是否包含图表
    'display_columns': [        # 显示的列
        '代码', '名称', '最新', '涨幅',
        '换手率', '量比', '流通市值'
    ]
}

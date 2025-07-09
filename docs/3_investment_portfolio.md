## Stock picker 模型

- MM趋势模型(Mark Minervini’s Trend Template).
  通过技术指标来度量股票动能，从中筛选最有潜力的股票，买入并持有。

  - 股票价格高于150天均线和200天均线
  - 150日均线高于200日均线
  - 200日均线上升至少1个月
  - 50日均线高于150日均线和200日均线
  - 股票价格高于50日均线
  - 股票价格比52周低点高30%
  - 股票价格在52周高点的25%以内
  - 相对强弱指数(RS)大于等于70，这里的相对强弱指的是股票与大盘对比，RS = 股票1年收益率 / 基准指数1年收益率

- https://github.com/m-turnergane/stock-screener
  A comprehensive stock screening and analysis platform that delivers in-depth market insights through multi-sector analysis, technical indicators, and automated valuation metrics. The platform combines fundamental analysis, technical indicators, and sector-specific metrics to provide detailed investment recommendations across all major market sectors.
  live widgets to respond in conversation with live, interactive charts and interfaces specifically tailored to your requests.

- https://github.com/pranjal-joshi/Screeni-py?
  an advanced stock screener to find potential breakout stocks from NSE and tell its possible breakout values. It also helps to find the stocks that are consolidating and may breakout, or the particular chart patterns that you're looking for specifically to make your decisions. Screenipy is totally customizable and it can screen stocks with the settings that you have provided.

- https://github.com/starboi-63/growth-stock-screener
  isolates and ranks top-tier growth companies based on relative strength, liquidity, trend, revenue growth, and institutional demand.

- https://github.com/hsliuping/TradingAgents-CN
  服务中国市场
  - 市场对接: 支持A股、港股、新三板等中国金融市场
  - 数据源集成: 整合Tushare、AkShare、Wind等中文金融数据
  - 合规适配: 符合国内金融监管和数据安全要求

## Investment Portfolio

- 马科维茨投资组合理论
  要求组合的股票具有低相关性，这样才能对冲系统性风险，否则在大盘走弱的时候投资组合也会面临巨大的下跌风险.

## Backtesting
  回溯检验，根据MM模型构建投资组合，优化筛选参数，看是否能带来超额收益。


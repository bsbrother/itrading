# Project Guidelines
  - Use uv python package management, uv pip install pkg-name, uv run python script-name.
  - Add document files must at docs/ directory, such as summary fixes etc.
  - Always update the README.md documentation when making changes to the codebase.
  - All test files must at tests/ directory.
  - Add temporary files for demo or test, remove them when fix issues or demo done.

## Requirements
  - MCP server plugins: context7

## Use Google Gemini AI Provider and model
  Example:
  ```python
  # pip install google-generativeai
  from google import genai
  from dotenv import load_dotenv
  load_dotenv(os.path.expanduser('~/apps/iagent/.env'), verbose=True)
  os.environ.pop('GOOGLE_API_KEY', None) # Default use GOOGLE_API_KEY, remove it in
  GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
  MODEL='gemini-2.5-pro-preview-06-05'
  client = genai.Client(api_key=GEMINI_API_KEY)
  response = client.models.generate_content(
    model=MODEL,
    contents="What is the meaning of life?"
  )
  print(response.text)
  ```

## Use Tushare or Akshare or Qstock Financial Data APIs
  Prefer using the Tushare API, with the Akshare API as a fallback option.

  Example [Tushare Pro for fetch cash flow data](https://tushare.pro/document/2?doc_id=16):
  ```python
  import tushare as ts
  from dotenv import load_dotenv
  # 初始化Tushare Pro API
  load_dotenv(os.path.expanduser('~/apps/iagent/.env'))
  TUSHARE_TOKEN = os.getenv("TUSHARE_TOKEN")
  ts.set_token(TUSHARE_TOKEN)
  PRO = ts.pro_api()
  # 使用Tushare Pro获取 {ts_code} 的财务指标...")
  fina_indicator = PRO.fina_indicator(ts_code=ts_code, start_date='20240101', end_date='20241231')
  ```
  Example [Akshare for fetch stock data](https://akshare.akfamily.xyz/zh_CN/latest/stock/akshare_stock.html):
  ```python
  import akshare as ak
  # 获取上证指数数据
  sh_index = ak.stock_zh_index_daily(symbol="sh000001")
  print(sh_index)
  ```
  Example [Qstock for fetch stock data](https://qstock.readthedocs.io/en/latest/):
  ```python
  import qstock as qs
  # 获取沪深A股票实时数据
  df = qs.realtime_data(market='沪深A')
  ```

## Setting chinese fonts for matplotlib
  Example, more detail in tests/test_matplotlib_chinese_fonts.my.
  ```python
  import matplotlib.pyplot as plt
  import matplotlib.font_manager as fm

  # Setting Global Fonts
  plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei',]
  plt.rcParams['axes.unicode_minus'] = False  # Solve the negative sign display issue

  # Test Drawing
  plt.plot([1, 2, 3], label='测试曲线')
  plt.title('中文标题示例')
  plt.xlabel('横轴')
  plt.ylabel('纵轴')
  plt.show()
  plt.close()
  ```

## The Chinese stock market (A-shares) is different from other markets.
  * Main differences:
    - The stock market open from 9:30 to 15:00, with a break from 11:30 to 13:00, closed on Saturdays and Sundays.

    - A daily limit of 10% for most stocks(Mainboard), as the "涨停板" (limit up) and "跌停板" (limit down) rules. 
      ST is 5%, ChiNext and Sci-Tech is 20%, Beijing Stock Exchange is 30% daily limit.

    - T+1 system for stock trading, which means that investors cannot sell stocks or funds that they have purchased on the same day; 
      they must wait until the next day for the settlement and transfer of ownership before they can sell. 
      Additionally, any funds from stocks or funds sold on the same day must also wait until the next day to be withdrawn.

    - Commission and Taxes
      - The transaction commission is typically 0.03% of the transaction amount, with a minimum of 5 yuan.
      - The stamp duty is 0.1% of the transaction amount for selling stocks, and there is no stamp duty for buying stocks.
      - There is no capital gains tax for individual investors in the A-share market.
      - The capital gains tax is 0.15% of the transaction amount for individual investors, and there is no capital gains tax for institutional investors.

  * Other differences:
    - IPO (Initial Public Offering)
      - The IPO process in the A-share market is different from other markets, with a focus on the "审核" (review) and "发行" (issuance) processes.
      - The IPO price is determined by the "询价" (inquiry) and "定价" (pricing) processes, which involve institutional investors and underwriters.
      - The IPO shares are allocated to institutional investors first, and then to retail investors through a lottery system.
      - The IPO shares are subject to a lock-up period, which is typically 12 months.
    - financial data and indicators, such as the "市盈率" (PE ratio) and "市净率" (PB ratio).
    - financial regulations and policies, such as the "证监会" (CSRC) and "沪深交易所" (Shanghai and Shenzhen Stock Exchanges). 
    - trading rules, such as the "停牌" (suspension) and "一字板" (one-cent board).
    - trading strategies, such as the "hedge" (hedging) and "covered" (covered call) strategies.  
    - trading hours, such as the "pre-market" and "after-hours" trading sessions.
    - trading platforms, such as the "券商" (brokerage) and "交易所" (exchange) platforms.
    - trading fees, such as the "交易佣金" (transaction commission) and "印花税" (stamp duty).
    - trading risks, such as the "市场风险" (market risk) and "信用风险" (credit risk).
    - trading opportunities, such as the "套利" (arbitrage) and "投机" (speculation) opportunities.
    - trading strategies, such as the "趋势交易" (trend trading) and "波段交易" (swing trading) strategies.
    - trading indicators, such as the "MACD" (Moving Average Convergence Divergence) and "KDJ" (Stochastic Oscillator) indicators.
    - trading tools, such as the "技术分析" (technical analysis) and "基本面分析" (fundamental analysis) tools.
    - trading psychology, such as the "贪婪" (greed) and "恐惧" (fear) psychology.
    - trading culture, such as the "散户" (retail investors) and "机构投资者" (institutional investors).
    - trading history, such as the "股灾" (stock market crash) and "牛市" (bull market) history.
    - trading future, such as the "科技股" (technology stocks) and "新能源" (new energy) future.
    - trading trends, such as the "大盘" (market trend) and "个股" (individual stock trend) trends.
    - trading strategies, such as the "价值投资" (value investing) and "成长投资" (growth investing) strategies.
    - trading regulations, such as the "信息披露" (information disclosure) and "内幕交易" (insider trading) regulations.
    - trading ethics, such as the "诚信" (integrity) and "公平" (fairness) ethics.
    - trading education, such as the "投资者教育" (investor education) and "金融知识" (financial knowledge) education.
    - trading resources, such as the "财经新闻" (financial news) and "研究报告" (research reports) resources.
    - trading communities, such as the "股民" (stock investors) and "投资论坛" (investment forums) communities.

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
  Preferred to using the Tushare API, Akshare API and Qstock API as a fallback option, lastest to use mock data for testing or demo purposes.

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

## Classification and Code Characteristics of Chinese Stocks.

  - 分类:
    - A股(A-shares)：人民币普通股票，由中国境内公司发行，供境内机构、组织和个人（不含台港澳）以人民币认购和交易的普通股股票。有3个证券交易所，分别是上海证券交易所，深圳证券交易所，21年上的北京证券交易所。
    - B股(B-shares)：人民币特种股票，在中国大陆注册上市的特种股票，以人民币标明面值，只能以外币认购和交易。
    - H股(H-shares)：又叫港股，在香港上市的股票。
    - 美股(US stocks)：在中国大陆注册，在美国证券交易所上市的股票。

  - A股代码特点:
    上交所（沪市）的代码是6开头，深交所（深市）是0和3开头，北交所是4和8开头。具体板块如下：

    - 沪市主板股票代码以600/601/603/605开头，科创板股票代码以688开头。
    - 深市主板股票代码以000/001/002/003/004开头，创业板股票代码以300/301开头。
    - 北交所股票代码以8开头。
    - 新三板股票代码以400/430/830开头。新三板全称是全国中小企业股份转让系统，是经国务院批准设立的全国性证券交易场所，为非上市股份有限公司的股份公开转让、融资、并购等相关业务提供服务。新三板属于场外市场，公司股份没有在证券交易所挂牌，而是通过证券交易公司交易。

    新手只能购买上交所和深交所主板的股票，创业板需要2年的交易经验和月均10万的资产才可买，科创板需要2年交易经验和月均50万资产才可购买，北交所门槛和科创板一致。

  - A股名称前缀:
    - N: New
    - ST: 经营异常股票 Or 盈利能力出现问题
    - *ST: 有退市风险
    - S: 没有按期完成股改
    - G: 已经完成股改
    - XD: 分红派息
    - XR: 除权
    - DR: 送股和派息

## The Chinese stock market (A-shares) is different from other markets.
  ** Notice**: 
  This project only supports A-shares, which is the stock market in mainland China, 
  and does not support other markets such as US stocks, Hong Kong stocks, or overseas stocks.

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

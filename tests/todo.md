# iTrading
  - Base picker stocks strategy. See ./before_open_pick_adjust_stocks.md.
    Support Pre/Open/Close Market running.
    - Base Stock Picker Strategy for Quantitative Stock Selection
    - Advanced Stock Picker Strategy, Support custom configure.

  - AI exhanced analysis stocks performances.
    - Analysis  [stock-scanner system](AI增强A股股票分析系统，集成了**25项财务指标分析**、**综合新闻情绪分析**>、**技术指标计算**和**AI深度解读**) web_stock_analyzer.py file:
      - Remove using config.json setting.
      - Remove cache data functions.
      - Only keep AI google gemini provider.
      - Not use AI streaming method, not need stream_callback function.

  - Unify and call these two systems stock picker and ai analyzer.
    Create a new file unify_stock_pick_ai_analyzer.py:
    - Default trade_date is today.
    - Call advanced_stock_picker.py to get trade_date pickered stocks.
    - Tranfer every pikered stock code to ai_stock_analyzer.py to get two field:
ai_score and ai_analysis. Append this two fields to the end of this stock origin  fields.
    -  Unify '流通市值,综合得分,风险评分,风险调整得分' + 'ai_score', created a new field 'final_score' to the end of every pickered stock.


  - Risk control, reasonable allocation of positions, setting stop-loss and take-profit points.


  - Use [Reflex framework](https://reflex.dev/docs/getting-started/introduction) for this project.
    - For web application: uv run reflex run
    - For functions test: uv run python path-to-script-name


"""
iTrading - 早盘量化选股系统
基于Reflex框架的Web应用界面
"""

import reflex as rx
from typing import List, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.expanduser('~/apps/iagent/.env'), verbose=True)

class State(rx.State):
    """应用状态管理"""
    
    # 股票数据
    stocks_data: List[Dict[str, Any]] = []
    selected_stocks: List[str] = []
    is_loading: bool = False
    
    # 分析结果
    analysis_result: str = ""
    
    # 筛选条件
    min_score: float = 7.0
    max_stocks: int = 10
    
    def load_stock_data(self):
        """加载股票数据"""
        self.is_loading = True
        yield
        
        try:
            # 这里可以集成你现有的股票选择器
            from unify_stock_pick_ai_analyzer import UnifiedStockPickAIAnalyzer
            
            analyzer = UnifiedStockPickAIAnalyzer()
            # 获取推荐股票
            recommendations = analyzer.get_stock_recommendations(
                min_score=self.min_score,
                max_count=self.max_stocks
            )
            
            # 转换为前端显示格式
            self.stocks_data = [
                {
                    "code": stock.get("ts_code", ""),
                    "name": stock.get("name", ""),
                    "score": stock.get("score", 0),
                    "price": stock.get("close", 0),
                    "change_pct": stock.get("pct_chg", 0),
                    "volume": stock.get("vol", 0),
                    "analysis": stock.get("ai_analysis", "")
                }
                for stock in recommendations
            ]
            
        except Exception as e:
            self.analysis_result = f"数据加载失败: {str(e)}"
        
        self.is_loading = False
        yield
    
    def update_min_score(self, value: str):
        """更新最小评分"""
        try:
            self.min_score = float(value)
        except ValueError:
            pass
    
    def update_max_stocks(self, value: str):
        """更新最大股票数量"""
        try:
            self.max_stocks = int(value)
        except ValueError:
            pass
    
    def toggle_stock_selection(self, stock_code: str):
        """切换股票选择状态"""
        if stock_code in self.selected_stocks:
            self.selected_stocks.remove(stock_code)
        else:
            self.selected_stocks.append(stock_code)


def header() -> rx.Component:
    """页面头部"""
    return rx.hstack(
        rx.heading("iTrading 早盘量化选股系统", size="9"),
        rx.spacer(),
        rx.text(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"),
        width="100%",
        padding="1rem",
        bg="blue.50",
        border_bottom="1px solid #e2e8f0",
    )


def control_panel() -> rx.Component:
    """控制面板"""
    return rx.vstack(
        rx.heading("筛选条件", size="5"),
        rx.hstack(
            rx.text("最低评分:"),
            rx.input(
                placeholder="7.0",
                value=State.min_score,
                on_change=State.update_min_score,
                width="100px",
            ),
            spacing="2",
        ),
        rx.hstack(
            rx.text("最大数量:"),
            rx.input(
                placeholder="10",
                value=State.max_stocks,
                on_change=State.update_max_stocks,
                width="100px",
            ),
            spacing="2",
        ),
        rx.button(
            "开始分析",
            on_click=State.load_stock_data,
            loading=State.is_loading,
            size="3",
            color_scheme="blue",
        ),
        spacing="4",
        padding="1rem",
        border="1px solid #e2e8f0",
        border_radius="8px",
        width="100%",
    )


def stock_card(stock: Dict[str, Any]) -> rx.Component:
    """股票卡片组件"""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading(f"{stock['name']} ({stock['code']})", size="4"),
                rx.spacer(),
                rx.badge(f"评分: {stock['score']:.1f}", color_scheme="green"),
                width="100%",
            ),
            rx.hstack(
                rx.text(f"价格: ¥{stock['price']:.2f}"),
                rx.text(f"涨跌: {stock['change_pct']:.2f}%"),
                rx.text(f"成交量: {stock['volume']:,.0f}"),
                spacing="4",
            ),
            rx.text(stock['analysis'], font_size="sm", color="gray.600"),
            rx.checkbox(
                "选择",
                name=stock['code'],
            ),
            spacing="2",
            align="start",
        ),
        width="100%",
        padding="1rem",
    )


def stocks_list() -> rx.Component:
    """股票列表"""
    return rx.vstack(
        rx.heading("推荐股票", size="5"),
        rx.cond(
            State.is_loading,
            rx.spinner(size="3"),
            rx.cond(
                State.stocks_data.length() > 0,
                rx.foreach(State.stocks_data, stock_card),
                rx.text("暂无数据，请点击'开始分析'按钮", color="gray.500"),
            ),
        ),
        spacing="4",
        width="100%",
    )


def selected_summary() -> rx.Component:
    """已选股票摘要"""
    return rx.vstack(
        rx.heading("已选股票", size="5"),
        rx.text(f"已选择 {State.selected_stocks.length()} 只股票"),
        rx.foreach(
            State.selected_stocks,
            lambda code: rx.badge(code, color_scheme="blue"),
        ),
        spacing="2",
        padding="1rem",
        border="1px solid #e2e8f0",
        border_radius="8px",
        width="100%",
    )


def index() -> rx.Component:
    """主页面"""
    return rx.container(
        header(),
        rx.hstack(
            rx.vstack(
                control_panel(),
                selected_summary(),
                spacing="4",
                width="30%",
            ),
            rx.vstack(
                stocks_list(),
                spacing="4",
                width="70%",
            ),
            spacing="6",
            padding="2rem",
            width="100%",
        ),
        max_width="1400px",
        margin="0 auto",
    )


# 创建应用
app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        radius="medium",
        scaling="100%",
    ),
)

app.add_page(index, route="/")

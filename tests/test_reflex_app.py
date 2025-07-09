"""
测试Reflex应用的基本功能
"""

import reflex as rx
from app import State, app

def test_reflex_app_import():
    """测试Reflex应用可以正常导入"""
    assert app is not None
    assert isinstance(app, rx.App)

def test_state_class_structure():
    """测试State类结构"""
    # 检查State类的属性定义
    assert hasattr(State, 'stocks_data')
    assert hasattr(State, 'selected_stocks')
    assert hasattr(State, 'is_loading')
    assert hasattr(State, 'min_score')
    assert hasattr(State, 'max_stocks')
    assert hasattr(State, 'analysis_result')
    
    # 检查方法存在
    assert hasattr(State, 'load_stock_data')
    assert hasattr(State, 'update_min_score')
    assert hasattr(State, 'update_max_stocks')
    assert hasattr(State, 'toggle_stock_selection')

def test_reflex_config():
    """测试Reflex配置"""
    from rxconfig import config
    assert config.app_name == "itrading"
    assert config.frontend_port == 3000
    assert config.backend_port == 8000

if __name__ == "__main__":
    # 运行基本测试
    test_reflex_app_import()
    test_state_class_structure()
    test_reflex_config()
    print("所有Reflex应用测试通过！")

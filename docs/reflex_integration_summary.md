# Reflex Web界面集成文档

## 概述

本项目已成功集成Reflex框架，为iTrading早盘量化选股系统提供现代化的Web界面。

## 文件结构

### 新增文件
- `app.py` - 主要的Reflex应用文件
- `rxconfig.py` - Reflex配置文件
- `.web/` - Reflex自动生成的前端文件目录

### 依赖更新
- `pyproject.toml` - 添加了 `reflex>=0.8.1` 依赖
- `requirements.txt` - 添加了Reflex包
- `uv.lock` - 已同步包含Reflex及其依赖

## 功能特性

### Web界面功能
1. **实时股票筛选**: 可视化的筛选条件设置
2. **股票推荐展示**: 卡片式股票信息展示
3. **交互式参数调整**: 
   - 最低评分设置
   - 最大股票数量设置
4. **股票选择管理**: 复选框选择心仪股票
5. **实时数据加载**: 集成现有的选股分析器

### 技术特点
- **响应式设计**: 适配不同屏幕尺寸
- **实时状态管理**: 基于Reflex State管理
- **组件化架构**: 模块化的UI组件
- **异步数据加载**: 非阻塞的数据获取

## 使用方法

### 启动Web应用
```bash
# 进入项目目录
cd /home/kasm-user/apps/itrading

# 启动开发服务器
uv run reflex run

# 或者直接运行app
uv run python app.py
```

### 访问界面
- 前端地址: http://localhost:3000
- 后端API: http://localhost:8000

### 界面操作
1. 设置筛选条件（最低评分、最大数量）
2. 点击"开始分析"按钮
3. 查看推荐股票列表
4. 选择感兴趣的股票
5. 查看已选股票摘要

## 集成现有组件

### 数据源集成
- 自动调用 `UnifiedStockPickAIAnalyzer`
- 使用现有的Tushare/Akshare数据源
- 保持与命令行版本的功能一致性

### AI分析集成
- 支持Google Gemini AI分析
- 展示AI分析结果
- 保留现有的评分机制

## 配置说明

### rxconfig.py配置
```python
import reflex as rx

config = rx.Config(
    app_name="itrading",
    frontend_port=3000,
    backend_port=8000,
    api_url="http://localhost:8000",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
)
```

### 环境变量
继续使用现有的环境变量配置：
- `TUSHARE_TOKEN` - Tushare API令牌
- `GEMINI_API_KEY` - Google Gemini API密钥

## 开发指南

### 添加新功能
1. 在 `State` 类中添加新的状态变量
2. 创建对应的UI组件函数
3. 在主页面 `index()` 中组合组件

### 自定义样式
- 使用Reflex内置主题系统
- 支持颜色方案和响应式设计
- 可通过 `rx.theme()` 配置全局样式

### 数据处理
- 在State类的方法中处理数据逻辑
- 使用 `yield` 进行异步状态更新
- 集成现有的选股和AI分析模块

## 部署说明

### 开发环境
```bash
uv run reflex run
```

### 生产环境
```bash
# 构建前端
uv run reflex export

# 启动生产服务器
uv run reflex run --env prod
```

## 故障排除

### 常见问题
1. **端口占用**: 修改rxconfig.py中的端口设置
2. **依赖缺失**: 运行 `uv sync` 重新同步依赖
3. **API错误**: 检查环境变量配置

### 日志查看
Reflex会在控制台输出详细的运行日志，包括前后端启动信息和错误提示。

## 下一步计划

1. **数据可视化**: 添加图表展示功能
2. **历史记录**: 保存选股历史
3. **用户设置**: 个性化配置保存
4. **实时更新**: WebSocket实时数据推送
5. **移动端优化**: 完善移动设备适配

## 总结

Reflex框架的集成为iTrading系统提供了现代化的Web界面，保持了命令行版本的所有功能，同时提供了更好的用户体验。系统架构清晰，易于扩展和维护。

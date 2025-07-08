# CSV格式化修复说明

## 问题描述

原始的CSV输出文件中，评分字段（综合得分、风险评分、风险调整得分）显示为高精度浮点数，影响可读性：

```csv
代码,名称,最新,涨幅,换手率,量比,流通市值,综合得分,风险评分,风险调整得分
600744,华银电力,7.25,8.21,14.37,9.15,14725650987.0,0.6053964000727725,0.301233361837783,0.4230308072343598
```

## 解决方案

修改 `advanced_stock_picker.py` 中的CSV保存逻辑，在保存前对评分字段进行格式化：

```python
# 创建保存用的数据副本，并格式化得分列为2位小数
save_data = selected_stocks[save_columns].copy()

# 格式化得分列为2位小数  
score_columns = ['综合得分', '风险评分', '风险调整得分']
for col in score_columns:
    if col in save_data.columns:
        save_data[col] = save_data[col].apply(lambda x: f"{x:.2f}" if pd.notna(x) else x)
```

## 修复后效果

CSV输出文件中的评分字段现在显示为2位小数格式，提升可读性：

```csv
代码,名称,最新,涨幅,换手率,量比,流通市值,综合得分,风险评分,风险调整得分
600744,华银电力,7.25,8.21,14.37,9.15,14725650987.0,0.61,0.30,0.42
```

## 文件位置

- 修改文件: `advanced_stock_picker.py` (第463-481行)
- 输出文件: `/tmp/itrading/advanced_selected_stocks_YYYYMMDD_HHMMSS.csv`

## 向前兼容性

此修改仅影响CSV文件输出格式，不影响：
- 内存中的数据精度
- 算法计算过程
- 其他功能模块
- 原有API接口

修改时间: 2025-07-08

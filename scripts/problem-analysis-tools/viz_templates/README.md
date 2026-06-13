# viz_templates

这里放题解样例可视化的可复用模板函数。

这些文件不是统一命令行工具，也不负责自动识别样例格式。正确用法是：

1. agent 阅读题目输入格式和样例语义。
2. 在当前题目目录创建 `problem-analysis-workspace/viz_render.py`。
3. 从这里复制或 import 小函数。
4. 按当前题目的语义改写解析逻辑。
5. 生成可插入 `index.md` 的 Markdown、SVG、Mermaid 或 Graphviz dot。

示例：

```python
from viz_templates.grid_table import markdown_grid

grid = [
    [".", ".", "#"],
    ["S", ".", "T"],
]
print(markdown_grid(grid, corner="row \\ col"))
```

不要把题目专用语义塞回这里。只有多个题目反复用到、且语义稳定的函数，才沉淀为模板。

## DP 模板边界

`dp_trace.py` 提供经典 DP 的小规模教学追踪器，例如：

- 0/1 背包更新步骤；
- 完全背包更新步骤；
- LIS `O(n^2)` 步骤；
- LIS `tails` 优化步骤；
- 带统一 class 的 HTML DP 表格；
- 插入题解的说明草稿。

它不解析题目输入。每道题自己的 `viz_render.py` 必须先把样例输入转成结构化数据：

```python
from viz_templates.dp_trace import trace_lis_tails, render_lis_tails_markdown

values = [3, 1, 2, 5]
steps = trace_lis_tails(values)
print(render_lis_tails_markdown(steps))
```

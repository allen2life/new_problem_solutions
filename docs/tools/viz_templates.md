# viz_templates

位置：

```text
scripts/problem-analysis-tools/viz_templates/
```

作用：提供题解样例可视化的可复用模板函数，供题目专用脚本 `problem-analysis-workspace/viz_render.py` 使用。

它不是一个万能 `viz_sample.py`。不同 OJ 题目的样例输入语义差异很大，应由 agent 或用户根据题意生成当前题目的专用脚本。

## 推荐工作流

在题目目录中创建：

```text
problem-analysis-workspace/viz_render.py
```

脚本根据当前题目的输入格式读取 `in1` 或其他样例文件，生成：

```text
sample-grid.md
sample-graph.dot
sample-tree.svg
dp-table.md
```

最终在 `index.md` 中引用这些素材。

## 模板模块

| 模块 | 用途 |
| --- | --- |
| `array_table.py` | 一维数组 Markdown 表格 |
| `grid_table.py` | 二维网格 Markdown 表格 |
| `dp_table.py` | DP 表格模板或数值表 |
| `dp_trace.py` | 背包、LIS 等经典 DP 的小规模教学追踪 |
| `graph_dot.py` | 边列表转 Graphviz dot |
| `tree_svg.py` | import `tree_draw` 生成树形 SVG |

## 使用示例

```python
#!/usr/bin/env python3
from pathlib import Path

from viz_templates.grid_table import markdown_grid


def main() -> int:
    grid = [
        [".", ".", "#"],
        ["S", ".", "T"],
    ]
    Path("sample-grid.md").write_text(markdown_grid(grid, corner="row \\ col"), encoding="utf-8")
    print("Markdown: !include or paste sample-grid.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

如果直接运行题目目录下的 `viz_render.py`，需要让 Python 能找到模板目录。推荐在脚本顶部加入：

```python
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "scripts/problem-analysis-tools"))
```

具体 `parents` 层数可按脚本所在目录调整。agent 生成脚本时应验证 import 是否成功。

## DP trace

`dp_trace.py` 只处理结构化数据，不解析 OJ 输入。题目专用 `viz_render.py` 应先根据题意解析样例，再调用这些函数。

示例：

```python
from viz_templates.dp_trace import trace_lis_quadratic, render_lis_quadratic_markdown

values = [3, 1, 2, 5]
steps = trace_lis_quadratic(values)
print(render_lis_quadratic_markdown(steps))
```

支持的稳定模板：

- `trace_zero_one_knapsack(items, capacity)`：0/1 背包二维表和倒序更新追踪。
- `trace_complete_knapsack(items, capacity)`：完全背包正序更新追踪。
- `trace_lis_quadratic(values)`：LIS `O(n^2)` 步骤。
- `trace_lis_tails(values)`：LIS `tails` 更新步骤。
- `render_dp_html_table(...)`：带 `dp-viz-*` class 的 HTML 表格。

HTML 表格 class 约定：

```text
dp-viz-table
dp-viz-current
dp-viz-source
dp-viz-changed
dp-viz-muted
dp-viz-choice
dp-viz-direction
```

这些 class 只表达语义，具体样式由前端统一提供。

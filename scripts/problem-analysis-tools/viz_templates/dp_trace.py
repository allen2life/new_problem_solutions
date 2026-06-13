"""经典 DP 教学追踪模板。

这些函数只处理结构化数据，不解析 OJ 输入。每道题自己的
problem-analysis-workspace/viz_render.py 负责把样例输入转成 items、
capacity 或 values，再调用这里的小规模教学函数。
"""

from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass
from html import escape
from typing import Iterable


NEG_INF = -10**18


@dataclass(frozen=True)
class KnapsackStep:
    item_index: int
    capacity: int
    weight: int
    value: int
    before: int
    candidate: int | None
    after: int
    direction: str
    changed: bool


@dataclass(frozen=True)
class LisQuadraticStep:
    index: int
    value: int
    predecessors: list[int]
    dp_value: int
    answer: int


@dataclass(frozen=True)
class LisTailsStep:
    index: int
    value: int
    position: int
    before: list[int]
    after: list[int]
    answer: int


def trace_zero_one_knapsack(items: list[tuple[int, int]], capacity: int) -> tuple[list[list[int]], list[KnapsackStep]]:
    """生成 0/1 背包二维 DP 表和一维倒序更新追踪。"""
    table = [[0] * (capacity + 1) for _ in range(len(items) + 1)]
    steps: list[KnapsackStep] = []
    one_dim = [0] * (capacity + 1)

    for i, (weight, value) in enumerate(items, start=1):
        for cap in range(capacity + 1):
            without = table[i - 1][cap]
            with_item = table[i - 1][cap - weight] + value if cap >= weight else NEG_INF
            table[i][cap] = max(without, with_item)

        for cap in range(capacity, weight - 1, -1):
            before = one_dim[cap]
            candidate = one_dim[cap - weight] + value
            after = max(before, candidate)
            one_dim[cap] = after
            steps.append(KnapsackStep(
                item_index=i,
                capacity=cap,
                weight=weight,
                value=value,
                before=before,
                candidate=candidate,
                after=after,
                direction="desc",
                changed=after != before,
            ))

    return table, steps


def trace_complete_knapsack(items: list[tuple[int, int]], capacity: int) -> tuple[list[int], list[KnapsackStep]]:
    """生成完全背包一维正序更新追踪。"""
    dp = [0] * (capacity + 1)
    steps: list[KnapsackStep] = []

    for i, (weight, value) in enumerate(items, start=1):
        for cap in range(weight, capacity + 1):
            before = dp[cap]
            candidate = dp[cap - weight] + value
            after = max(before, candidate)
            dp[cap] = after
            steps.append(KnapsackStep(
                item_index=i,
                capacity=cap,
                weight=weight,
                value=value,
                before=before,
                candidate=candidate,
                after=after,
                direction="asc",
                changed=after != before,
            ))

    return dp, steps


def trace_lis_quadratic(values: list[int]) -> list[LisQuadraticStep]:
    """生成 O(n^2) LIS 的教学步骤。"""
    dp = [1] * len(values)
    answer = 0
    steps: list[LisQuadraticStep] = []

    for i, value in enumerate(values):
        predecessors: list[int] = []
        for j in range(i):
            if values[j] < value:
                predecessors.append(j)
                dp[i] = max(dp[i], dp[j] + 1)
        answer = max(answer, dp[i])
        steps.append(LisQuadraticStep(
            index=i,
            value=value,
            predecessors=predecessors,
            dp_value=dp[i],
            answer=answer,
        ))

    return steps


def trace_lis_tails(values: list[int]) -> list[LisTailsStep]:
    """生成 O(n log n) LIS tails 数组更新步骤。"""
    tails: list[int] = []
    steps: list[LisTailsStep] = []

    for i, value in enumerate(values):
        before = tails[:]
        position = bisect_left(tails, value)
        if position == len(tails):
            tails.append(value)
        else:
            tails[position] = value
        steps.append(LisTailsStep(
            index=i,
            value=value,
            position=position,
            before=before,
            after=tails[:],
            answer=len(tails),
        ))

    return steps


def render_knapsack_steps_markdown(steps: Iterable[KnapsackStep], *, limit: int = 12) -> str:
    """把背包更新步骤渲染成 Markdown 表格。"""
    rows = [
        "| 步骤 | 物品 | j | 更新方向 | 更新前 dp[j] | 候选 dp[j-w]+v | 更新后 dp[j] | 说明 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for order, step in enumerate(list(steps)[:limit], start=1):
        direction = "倒序" if step.direction == "desc" else "正序"
        note = "发生更新" if step.changed else "保持原值"
        rows.append(
            f"| {order} | {step.item_index} | {step.capacity} | {direction} | "
            f"{step.before} | {step.candidate} | {step.after} | {note} |"
        )
    return "\n".join(rows)


def render_lis_quadratic_markdown(steps: Iterable[LisQuadraticStep]) -> str:
    """把 O(n^2) LIS 步骤渲染成 Markdown 表格。"""
    rows = [
        "| i | a[i] | 可接前驱 | dp[i] | 当前答案 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for step in steps:
        predecessors = "无" if not step.predecessors else ", ".join(f"j={idx}" for idx in step.predecessors)
        rows.append(f"| {step.index + 1} | {step.value} | {predecessors} | {step.dp_value} | {step.answer} |")
    return "\n".join(rows)


def render_lis_tails_markdown(steps: Iterable[LisTailsStep]) -> str:
    """把 tails 更新步骤渲染成 Markdown 表格。"""
    rows = [
        "| i | a[i] | lower_bound 位置 | 更新前 tails | 更新后 tails | 当前答案 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for step in steps:
        rows.append(
            f"| {step.index + 1} | {step.value} | {step.position + 1} | "
            f"{format_array(step.before)} | {format_array(step.after)} | {step.answer} |"
        )
    return "\n".join(rows)


def render_dp_html_table(
    values: list[list[str | int]],
    *,
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
    current: set[tuple[int, int]] | None = None,
    sources: set[tuple[int, int]] | None = None,
    changed: set[tuple[int, int]] | None = None,
    choices: set[tuple[int, int]] | None = None,
    muted: set[tuple[int, int]] | None = None,
    corner: str = "i \\ j",
) -> str:
    """渲染带高亮 class 的 HTML DP 表格。坐标从 0 开始。"""
    current = current or set()
    sources = sources or set()
    changed = changed or set()
    choices = choices or set()
    muted = muted or set()
    width = max((len(row) for row in values), default=0)
    labels = col_labels or [str(i) for i in range(width)]

    lines = ['<table class="dp-viz-table">', "  <thead>", "    <tr>"]
    lines.append(f"      <th>{escape(corner)}</th>")
    for label in labels:
        lines.append(f"      <th>{escape(str(label))}</th>")
    lines.extend(["    </tr>", "  </thead>", "  <tbody>"])

    for r, row in enumerate(values):
        label = row_labels[r] if row_labels and r < len(row_labels) else str(r)
        lines.append("    <tr>")
        lines.append(f"      <th>{escape(str(label))}</th>")
        for c in range(width):
            value = row[c] if c < len(row) else ""
            classes = cell_classes((r, c), current=current, sources=sources, changed=changed, choices=choices, muted=muted)
            class_attr = f' class="{" ".join(classes)}"' if classes else ""
            lines.append(f"      <td{class_attr}>{escape(str(value))}</td>")
        lines.append("    </tr>")

    lines.extend(["  </tbody>", "</table>"])
    return "\n".join(lines)


def insertion_note(*, section: str, title: str, before: str, after: list[str], files: list[str]) -> str:
    """生成给题解作者粘贴和改写的插入说明。"""
    file_lines = "\n".join(f"- `{path}`" for path in files)
    after_text = "\n".join(f"- {line}" for line in after)
    return "\n".join([
        "## 插入建议",
        "",
        f"- 推荐章节：`{section}`",
        f"- 推荐标题：`#### {title}`",
        "",
        "图前说明：",
        "",
        before,
        "",
        "图后观察点：",
        "",
        after_text,
        "",
        "生成文件：",
        "",
        file_lines,
    ])


def format_array(values: list[int]) -> str:
    """格式化短数组快照。"""
    return "[" + ", ".join(str(value) for value in values) + "]"


def cell_classes(
    cell: tuple[int, int],
    *,
    current: set[tuple[int, int]],
    sources: set[tuple[int, int]],
    changed: set[tuple[int, int]],
    choices: set[tuple[int, int]],
    muted: set[tuple[int, int]],
) -> list[str]:
    """按约定 class 标记一个 DP 单元格。"""
    classes: list[str] = []
    if cell in current:
        classes.append("dp-viz-current")
    if cell in sources:
        classes.append("dp-viz-source")
    if cell in changed:
        classes.append("dp-viz-changed")
    if cell in choices:
        classes.append("dp-viz-choice")
    if cell in muted:
        classes.append("dp-viz-muted")
    return classes

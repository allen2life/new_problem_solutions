"""DP 表格 Markdown 模板。"""

from __future__ import annotations


def blank_dp_table(rows: int, cols: int, *, row_name: str = "i", col_name: str = "j") -> str:
    """生成空白 DP 表格，适合讲状态定义或让 agent 填关键值。"""
    values = [["" for _ in range(cols)] for _ in range(rows)]
    row_labels = [str(i) for i in range(rows)]
    col_labels = [str(j) for j in range(cols)]
    return markdown_dp_table(values, row_labels=row_labels, col_labels=col_labels, corner=f"{row_name} \\ {col_name}")


def markdown_dp_table(
    values: list[list[str | int]],
    *,
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
    corner: str = "i \\ j",
) -> str:
    """把 DP 数值表渲染成 Markdown 表格。"""
    if not values:
        return ""
    width = max(len(row) for row in values)
    labels = col_labels or [str(i) for i in range(width)]
    rows = [f"| {corner} | " + " | ".join(labels) + " |"]
    rows.append("| --- | " + " | ".join(["---"] * width) + " |")
    for r, row in enumerate(values):
        label = row_labels[r] if row_labels and r < len(row_labels) else str(r)
        padded = [str(value) for value in row] + [""] * (width - len(row))
        rows.append(f"| {label} | " + " | ".join(padded) + " |")
    return "\n".join(rows)

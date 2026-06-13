"""二维网格 Markdown 表格模板。"""

from __future__ import annotations


def markdown_grid(
    grid: list[list[str | int]],
    *,
    row_labels: list[str] | None = None,
    col_labels: list[str] | None = None,
    corner: str = "",
) -> str:
    """把二维网格渲染成 Markdown 表格。"""
    if not grid:
        return ""
    width = max(len(row) for row in grid)
    labels = col_labels or [str(i + 1) for i in range(width)]
    rows = [f"| {corner} | " + " | ".join(labels) + " |"]
    rows.append("| --- | " + " | ".join(["---"] * width) + " |")
    for r, row in enumerate(grid):
        label = row_labels[r] if row_labels and r < len(row_labels) else str(r + 1)
        padded = [str(value) for value in row] + [""] * (width - len(row))
        rows.append(f"| {label} | " + " | ".join(padded) + " |")
    return "\n".join(rows)


def parse_char_grid(lines: list[str]) -> list[list[str]]:
    """把字符网格转成二维数组。"""
    return [list(line.rstrip("\n")) for line in lines if line.strip()]


def parse_token_grid(lines: list[str]) -> list[list[str]]:
    """把空格分隔的网格转成二维数组。"""
    return [line.split() for line in lines if line.strip()]

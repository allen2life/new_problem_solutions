"""一维数组 Markdown 表格模板。"""

from __future__ import annotations


def markdown_array(values: list[str | int], *, index_base: int = 1, name: str = "a") -> str:
    """把一维数组渲染成适合题解粘贴的 Markdown 表格。"""
    indexes = [str(i + index_base) for i in range(len(values))]
    cells = [str(value) for value in values]
    return "\n".join([
        f"| {name} 下标 | " + " | ".join(indexes) + " |",
        "| --- | " + " | ".join(["---"] * len(values)) + " |",
        f"| {name} 值 | " + " | ".join(cells) + " |",
    ])


def parse_int_line(line: str) -> list[int]:
    """解析一行整数。题目有特殊含义时，应在 viz_render.py 中再包装。"""
    return [int(part) for part in line.split()]

"""tree_draw 复用模板。"""

from __future__ import annotations

from pathlib import Path

from tree_draw.layout_walker import layout_tree
from tree_draw.parsers import build_segment_tree, parse_binary_children, parse_json_tree, parse_normal_edges
from tree_draw.render_svg import render_svg
from tree_draw.styles import DEFAULT_STYLE, deep_merge


def normal_tree_svg(text: str, *, root: str | None = None, style: dict | None = None) -> str:
    """把普通树边列表渲染成 SVG 字符串。"""
    tree = parse_normal_edges(text, root)
    return _render(tree, style)


def binary_tree_svg(text: str, *, root: str | None = None, style: dict | None = None) -> str:
    """把二叉树 children 表渲染成 SVG 字符串。"""
    tree = parse_binary_children(text, root)
    return _render(tree, style)


def segment_tree_svg(size: int, *, style: dict | None = None) -> str:
    """生成线段树结构 SVG 字符串。"""
    tree = build_segment_tree(size)
    return _render(tree, style)


def json_tree_svg(text: str, *, style: dict | None = None) -> str:
    """把 tree_draw JSON 格式渲染成 SVG 字符串。"""
    tree = parse_json_tree(text)
    return _render(tree, style)


def write_svg(path: str | Path, svg: str) -> None:
    """写入 SVG 文件。"""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")


def _render(tree, style: dict | None) -> str:
    merged = deep_merge(DEFAULT_STYLE, tree.style)
    if style:
        merged = deep_merge(merged, style)
    layout_tree(tree, merged)
    return render_svg(tree, merged)

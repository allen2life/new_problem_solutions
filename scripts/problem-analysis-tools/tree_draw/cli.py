import argparse
from pathlib import Path

from .layout_walker import layout_tree
from .parsers import (
    build_segment_tree,
    parse_binary_children,
    parse_json_tree,
    parse_normal_edges,
    read_text,
)
from .presets import segment_size_from_array
from .render_svg import render_svg
from .styles import DEFAULT_STYLE, deep_merge


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        tree = load_tree(args)
        style = deep_merge(DEFAULT_STYLE, tree.style)
        apply_style_args(style, args)
        layout_tree(tree, style)
        svg = render_svg(tree, style)
        write_output(args.output, svg)
        if args.markdown:
            print(markdown_snippet(args.output, args.alt))
    except Exception as exc:  # noqa: BLE001 - CLI should show concise user-facing errors.
        parser.exit(1, f"tree_draw.py: error: {exc}\n")

    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="使用 Walker 风格布局绘制树结构 SVG，适合题解配图和调试树形数据。",
    )
    parser.add_argument("--type", choices=["normal", "binary", "segment", "json"], default="normal",
                        help="树类型，默认 normal。json 会从输入 JSON 中读取类型。")
    parser.add_argument("--format", choices=["edges", "children", "json"], default=None,
                        help="输入格式。normal 默认 edges，binary 默认 children，json 默认 json。")
    parser.add_argument("-i", "--input", help="输入文件，省略或 '-' 表示 stdin。segment 类型可省略。")
    parser.add_argument("-o", "--output", default="tree.svg", help="输出 SVG 文件，默认 tree.svg。")
    parser.add_argument("--root", help="指定根节点。")
    parser.add_argument("--size", type=int, help="segment 类型的规模 n。")
    parser.add_argument("--array", help="segment 类型可传数组，节点规模取数组长度。")
    parser.add_argument("--markdown", action="store_true", help="额外输出可粘贴到题解中的 Markdown 图片片段。")
    parser.add_argument("--alt", default="树形结构示意图", help="--markdown 使用的图片 alt 文本。")
    parser.add_argument("--level-gap", type=float, help="层级之间的垂直间距。")
    parser.add_argument("--sibling-gap", type=float, help="同层相邻节点的最小间距。")
    parser.add_argument("--subtree-gap", type=float, help="相邻子树之间的最小间距。")
    parser.add_argument("--node-radius", type=float, help="节点半径。")
    parser.add_argument("--node-fill", help="默认节点填充色。")
    parser.add_argument("--node-stroke", help="默认节点边框色。")
    return parser


def load_tree(args: argparse.Namespace):
    if args.type == "segment":
        size = args.size
        if size is None and args.array:
            size = segment_size_from_array(args.array)
        if size is None:
            raise ValueError("segment 类型需要 --size 或 --array。")
        return build_segment_tree(size)

    input_format = args.format
    if input_format is None:
        input_format = {"normal": "edges", "binary": "children", "json": "json"}[args.type]

    text = read_text(args.input)
    if input_format == "json":
        return parse_json_tree(text)
    if input_format == "children":
        return parse_binary_children(text, args.root)
    return parse_normal_edges(text, args.root)


def apply_style_args(style: dict, args: argparse.Namespace) -> None:
    if args.level_gap is not None:
        style["layout"]["level_gap"] = args.level_gap
    if args.sibling_gap is not None:
        style["layout"]["sibling_gap"] = args.sibling_gap
    if args.subtree_gap is not None:
        style["layout"]["subtree_gap"] = args.subtree_gap
    if args.node_radius is not None:
        style["node"]["radius"] = args.node_radius
    if args.node_fill:
        style["node"]["fill"] = args.node_fill
    if args.node_stroke:
        style["node"]["stroke"] = args.node_stroke


def write_output(output: str, svg: str) -> None:
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")


def markdown_snippet(output: str, alt: str) -> str:
    return f"![{alt}](./{Path(output).name})"

from html import escape

from .model import Edge, Node, Tree
from .styles import resolve_style


def render_svg(tree: Tree, style: dict) -> str:
    bounds = compute_bounds(tree, style)
    width = bounds["max_x"] - bounds["min_x"]
    height = bounds["max_y"] - bounds["min_y"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{fmt(width)}" height="{fmt(height)}" '
        f'viewBox="{fmt(bounds["min_x"])} {fmt(bounds["min_y"])} {fmt(width)} {fmt(height)}" '
        'role="img">',
        "<g class=\"tree-edges\">",
    ]

    for edge in tree.edges:
        parts.append(render_edge(tree, edge, style))

    parts.append("</g>")
    parts.append("<g class=\"tree-nodes\">")

    for node_id in traversal_order(tree):
        parts.append(render_node(tree.nodes[node_id], style))

    parts.append("</g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_edge(tree: Tree, edge: Edge, style: dict) -> str:
    source = tree.nodes[edge.source]
    target = tree.nodes[edge.target]
    edge_style = resolve_style(style, "edge", edge.style)
    stroke = escape(str(edge_style.get("stroke", "#64748b")))
    width = fmt(edge_style.get("width", 2))
    dash = str(edge_style.get("dash", ""))
    dash_attr = f' stroke-dasharray="{escape(dash)}"' if dash else ""
    line = (
        f'<line x1="{fmt(source.x)}" y1="{fmt(source.y)}" '
        f'x2="{fmt(target.x)}" y2="{fmt(target.y)}" '
        f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"{dash_attr} />'
    )
    if not edge.label:
        return line

    mid_x = (source.x + target.x) / 2.0
    mid_y = (source.y + target.y) / 2.0
    font = style["font"]
    label = (
        f'<text x="{fmt(mid_x)}" y="{fmt(mid_y - 6)}" text-anchor="middle" '
        f'font-family="{escape(str(font["family"]))}" font-size="{fmt(float(font["size"]) - 2)}" '
        'fill="#475569">'
        f'{escape(edge.label)}</text>'
    )
    return line + "\n" + label


def render_node(node: Node, style: dict) -> str:
    node_style = resolve_style(style, "node", node.style)
    font = style["font"]
    shape = node_style.get("shape", "circle")
    fill = escape(str(node_style.get("fill", "#ffffff")))
    stroke = escape(str(node_style.get("stroke", "#334155")))
    stroke_width = fmt(node_style.get("stroke_width", 2))
    text_color = escape(str(node_style.get("text_color", "#111827")))
    radius = float(node_style.get("radius", 22))
    label = escape(node.display_label())

    if shape == "rect":
        width = max(radius * 2.4, len(node.display_label()) * float(font["size"]) * 0.72 + 18)
        height = radius * 1.8
        body = (
            f'<rect x="{fmt(node.x - width / 2)}" y="{fmt(node.y - height / 2)}" '
            f'width="{fmt(width)}" height="{fmt(height)}" rx="8" ry="8" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />'
        )
    else:
        body = (
            f'<circle cx="{fmt(node.x)}" cy="{fmt(node.y)}" r="{fmt(radius)}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width}" />'
        )

    text = (
        f'<text x="{fmt(node.x)}" y="{fmt(node.y)}" text-anchor="middle" dominant-baseline="central" '
        f'font-family="{escape(str(font["family"]))}" font-size="{fmt(font["size"])}" '
        f'fill="{text_color}">{label}</text>'
    )
    return f'<g class="tree-node" data-id="{escape(node.id)}">\n{body}\n{text}\n</g>'


def compute_bounds(tree: Tree, style: dict) -> dict[str, float]:
    radius = float(style["node"].get("radius", 22))
    padding = float(style["layout"].get("padding", 32))
    min_x = min(node.x for node in tree.nodes.values()) - radius - padding
    max_x = max(node.x for node in tree.nodes.values()) + radius + padding
    min_y = min(node.y for node in tree.nodes.values()) - radius - padding
    max_y = max(node.y for node in tree.nodes.values()) + radius + padding
    return {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}


def traversal_order(tree: Tree) -> list[str]:
    order = []

    def dfs(node_id: str) -> None:
        order.append(node_id)
        for child_id in tree.ordered_children(node_id):
            dfs(child_id)

    dfs(tree.root)
    return order


def fmt(value) -> str:
    number = float(value)
    if number.is_integer():
        return str(int(number))
    return f"{number:.2f}".rstrip("0").rstrip(".")

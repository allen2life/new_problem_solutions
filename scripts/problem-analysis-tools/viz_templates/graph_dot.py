"""Graphviz dot 模板。"""

from __future__ import annotations


def edges_to_dot(
    edges: list[tuple[str, str] | tuple[str, str, str]],
    *,
    directed: bool = False,
    graph_name: str = "G",
) -> str:
    """把边列表转成完整 dot 文本。"""
    graph_type = "digraph" if directed else "graph"
    op = "->" if directed else "--"
    lines = [
        f"{graph_type} {graph_name} {{",
        "  node [shape=circle, style=filled, fillcolor=white];",
    ]
    for edge in edges:
        source, target = str(edge[0]), str(edge[1])
        if len(edge) >= 3:
            label = str(edge[2]).replace('"', r"\"")
            lines.append(f'  "{source}" {op} "{target}" [label="{label}"];')
        else:
            lines.append(f'  "{source}" {op} "{target}";')
    lines.append("}")
    return "\n".join(lines) + "\n"


def parse_edge_lines(lines: list[str], *, weighted: bool = False) -> list[tuple[str, str] | tuple[str, str, str]]:
    """解析常见边列表；复杂图输入应在题目专用脚本中自行解析。"""
    edges: list[tuple[str, str] | tuple[str, str, str]] = []
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = line.split()
        if weighted and len(parts) >= 3:
            edges.append((parts[0], parts[1], parts[2]))
        elif len(parts) >= 2:
            edges.append((parts[0], parts[1]))
    return edges

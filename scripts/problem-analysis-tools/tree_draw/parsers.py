import json
from pathlib import Path

from .model import Edge, Node, Tree


def read_text(input_path: str | None) -> str:
    if not input_path or input_path == "-":
        import sys

        return sys.stdin.read()
    return Path(input_path).read_text(encoding="utf-8")


def parse_normal_edges(text: str, root: str | None = None) -> Tree:
    lines = useful_lines(text)
    if not lines:
        raise ValueError("普通树输入为空。")

    start = 0
    if len(lines[0].split()) == 1 and len(lines) > 1:
        start = 1

    nodes: dict[str, Node] = {}
    edges: list[Edge] = []
    child_set = set()

    for line in lines[start:]:
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f"边列表每行至少需要两个字段：{line}")
        source, target = parts[0], parts[1]
        nodes.setdefault(source, Node(source))
        nodes.setdefault(target, Node(target))
        nodes[source].children.append(target)
        edges.append(Edge(source, target))
        child_set.add(target)

    if not nodes:
        only = lines[0].split()[0]
        nodes[only] = Node(only)

    root_id = root or find_root(nodes, child_set)
    return Tree(nodes=nodes, edges=edges, root=root_id, tree_type="normal")


def parse_binary_children(text: str, root: str | None = None) -> Tree:
    lines = useful_lines(text)
    if not lines:
        raise ValueError("二叉树输入为空。")

    start = 0
    if len(lines[0].split()) == 1 and len(lines) > 1:
        start = 1

    nodes: dict[str, Node] = {}
    edges: list[Edge] = []
    child_set = set()

    for line in lines[start:]:
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f"二叉树 children 格式必须是：u left right。错误行：{line}")
        node_id, left_id, right_id = parts
        node = nodes.setdefault(node_id, Node(node_id))
        if left_id != "0":
            node.left = left_id
            nodes.setdefault(left_id, Node(left_id))
            edges.append(Edge(node_id, left_id, "L"))
            child_set.add(left_id)
        if right_id != "0":
            node.right = right_id
            nodes.setdefault(right_id, Node(right_id))
            edges.append(Edge(node_id, right_id, "R"))
            child_set.add(right_id)

    root_id = root or find_root(nodes, child_set)
    return Tree(nodes=nodes, edges=edges, root=root_id, tree_type="binary")


def parse_json_tree(text: str) -> Tree:
    data = json.loads(text)
    tree_type = data.get("type", "normal")
    nodes: dict[str, Node] = {}
    edges: list[Edge] = []

    for raw in data.get("nodes", []):
        node_id = str(raw["id"])
        nodes[node_id] = Node(
            id=node_id,
            label=str(raw.get("label", "")),
            left=str(raw["left"]) if raw.get("left") not in (None, "", 0, "0") else None,
            right=str(raw["right"]) if raw.get("right") not in (None, "", 0, "0") else None,
            style=raw.get("style", {}),
        )

    for raw in data.get("edges", []):
        source = str(raw["source"])
        target = str(raw["target"])
        nodes.setdefault(source, Node(source))
        nodes.setdefault(target, Node(target))
        edges.append(Edge(
            source=source,
            target=target,
            label=str(raw.get("label", "")),
            style=raw.get("style", {}),
        ))

    if tree_type == "binary":
        for node in nodes.values():
            if node.left:
                nodes.setdefault(node.left, Node(node.left))
                edges.append(Edge(node.id, node.left, "L"))
            if node.right:
                nodes.setdefault(node.right, Node(node.right))
                edges.append(Edge(node.id, node.right, "R"))
    else:
        tree = Tree(nodes=nodes, edges=edges, root=str(data.get("root", "")), tree_type=tree_type)
        tree.ensure_child_links()
        edges = tree.edges
        nodes = tree.nodes

    child_set = {edge.target for edge in edges}
    root_id = str(data.get("root") or find_root(nodes, child_set))
    return Tree(nodes=nodes, edges=edges, root=root_id, tree_type=tree_type, style=data.get("style", {}))


def build_segment_tree(size: int) -> Tree:
    if size <= 0:
        raise ValueError("线段树规模必须为正整数。")

    nodes: dict[str, Node] = {}
    edges: list[Edge] = []

    def build(left: int, right: int) -> str:
        node_id = f"{left}-{right}"
        label = f"[{left},{right}]"
        nodes[node_id] = Node(node_id, label=label)
        if left == right:
            return node_id

        mid = (left + right) // 2
        left_id = build(left, mid)
        right_id = build(mid + 1, right)
        nodes[node_id].left = left_id
        nodes[node_id].right = right_id
        edges.append(Edge(node_id, left_id))
        edges.append(Edge(node_id, right_id))
        return node_id

    root = build(1, size)
    return Tree(
        nodes=nodes,
        edges=edges,
        root=root,
        tree_type="binary",
        style={
            "node": {
                "shape": "rect",
                "radius": 22,
                "fill": "#f8fafc",
            },
            "layout": {
                "sibling_gap": 92,
                "subtree_gap": 48,
            },
        },
    )


def useful_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def find_root(nodes: dict[str, Node], child_set: set[str]) -> str:
    for node_id in nodes:
        if node_id not in child_set:
            return node_id
    if nodes:
        return next(iter(nodes))
    raise ValueError("没有可用节点，无法确定根节点。")

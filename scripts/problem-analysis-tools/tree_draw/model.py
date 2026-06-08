from dataclasses import dataclass, field


@dataclass
class Node:
    id: str
    label: str = ""
    children: list[str] = field(default_factory=list)
    left: str | None = None
    right: str | None = None
    style: dict = field(default_factory=dict)
    x: float = 0.0
    y: float = 0.0

    def display_label(self) -> str:
        return self.label if self.label != "" else self.id


@dataclass
class Edge:
    source: str
    target: str
    label: str = ""
    style: dict = field(default_factory=dict)


@dataclass
class Tree:
    nodes: dict[str, Node]
    edges: list[Edge]
    root: str
    tree_type: str = "normal"
    style: dict = field(default_factory=dict)

    def ordered_children(self, node_id: str) -> list[str]:
        node = self.nodes[node_id]
        if self.tree_type == "binary":
            result = []
            if node.left:
                result.append(node.left)
            if node.right:
                result.append(node.right)
            return result
        return list(node.children)

    def ensure_child_links(self) -> None:
        for node in self.nodes.values():
            node.children = []
        for edge in self.edges:
            if edge.source in self.nodes and edge.target in self.nodes:
                self.nodes[edge.source].children.append(edge.target)

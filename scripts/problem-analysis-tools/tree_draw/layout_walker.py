from dataclasses import dataclass, field

from .model import Tree


@dataclass
class LayoutState:
    prelim: dict[str, float] = field(default_factory=dict)
    mod: dict[str, float] = field(default_factory=dict)
    depth: dict[str, int] = field(default_factory=dict)
    left_neighbor: dict[str, str | None] = field(default_factory=dict)
    previous_at_depth: dict[int, str] = field(default_factory=dict)


def layout_tree(tree: Tree, style: dict) -> None:
    layout_style = style["layout"]
    state = LayoutState()
    sibling_gap = float(layout_style["sibling_gap"])
    subtree_gap = float(layout_style["subtree_gap"])
    level_gap = float(layout_style["level_gap"])
    padding = float(layout_style["padding"])

    init_depth_and_neighbors(tree, tree.root, 0, state)
    first_walk(tree, tree.root, state, sibling_gap, subtree_gap)
    second_walk(tree, tree.root, state, 0.0, level_gap)
    normalize_positions(tree, padding)


def init_depth_and_neighbors(tree: Tree, node_id: str, depth: int, state: LayoutState) -> None:
    state.depth[node_id] = depth
    state.left_neighbor[node_id] = state.previous_at_depth.get(depth)
    state.previous_at_depth[depth] = node_id
    for child_id in tree.ordered_children(node_id):
        init_depth_and_neighbors(tree, child_id, depth + 1, state)


def first_walk(
    tree: Tree,
    node_id: str,
    state: LayoutState,
    sibling_gap: float,
    subtree_gap: float,
) -> None:
    children = tree.ordered_children(node_id)
    state.mod[node_id] = 0.0

    if not children:
        left = state.left_neighbor.get(node_id)
        state.prelim[node_id] = state.prelim[left] + sibling_gap if left else 0.0
        return

    for child_id in children:
        first_walk(tree, child_id, state, sibling_gap, subtree_gap)

    midpoint = calc_children_midpoint(tree, node_id, children, state, sibling_gap)
    left = state.left_neighbor.get(node_id)
    if left:
        state.prelim[node_id] = state.prelim[left] + sibling_gap
    else:
        state.prelim[node_id] = midpoint
    state.mod[node_id] = state.prelim[node_id] - midpoint

    apportion(tree, node_id, state, subtree_gap)


def apportion(tree: Tree, node_id: str, state: LayoutState, subtree_gap: float) -> None:
    compare_depth = 1
    while True:
        left_most = get_left_most(tree, node_id, compare_depth)
        if not left_most:
            break
        neighbor = state.left_neighbor.get(left_most)
        if not neighbor:
            break

        left_pos = real_prelim(left_most, compare_depth, tree, state)
        right_pos = real_prelim(neighbor, compare_depth, tree, state)
        move = right_pos + subtree_gap - left_pos
        if move > 0:
            state.prelim[node_id] += move
            state.mod[node_id] += move
        compare_depth += 1


def calc_children_midpoint(
    tree: Tree,
    node_id: str,
    children: list[str],
    state: LayoutState,
    sibling_gap: float,
) -> float:
    if tree.tree_type == "binary":
        node = tree.nodes[node_id]
        if node.left and node.right:
            return (state.prelim[node.left] + state.prelim[node.right]) / 2.0
        if node.left:
            return state.prelim[node.left] + sibling_gap / 2.0
        if node.right:
            return state.prelim[node.right] - sibling_gap / 2.0
    return (state.prelim[children[0]] + state.prelim[children[-1]]) / 2.0


def get_left_most(tree: Tree, node_id: str, depth: int) -> str | None:
    if depth == 0:
        return node_id
    for child_id in tree.ordered_children(node_id):
        found = get_left_most(tree, child_id, depth - 1)
        if found:
            return found
    return None


def real_prelim(node_id: str, ancestor_distance: int, tree: Tree, state: LayoutState) -> float:
    current = node_id
    mod_sum = 0.0
    parent_by_child = build_parent_map(tree)
    for _ in range(ancestor_distance):
        parent = parent_by_child.get(current)
        if not parent:
            break
        mod_sum += state.mod.get(parent, 0.0)
        current = parent
    return state.prelim[node_id] + mod_sum


def second_walk(tree: Tree, node_id: str, state: LayoutState, mod_sum: float, level_gap: float) -> None:
    node = tree.nodes[node_id]
    node.x = state.prelim[node_id] + mod_sum
    node.y = state.depth[node_id] * level_gap
    for child_id in tree.ordered_children(node_id):
        second_walk(tree, child_id, state, mod_sum + state.mod[node_id], level_gap)


def normalize_positions(tree: Tree, padding: float) -> None:
    min_x = min(node.x for node in tree.nodes.values())
    min_y = min(node.y for node in tree.nodes.values())
    for node in tree.nodes.values():
        node.x = node.x - min_x + padding
        node.y = node.y - min_y + padding


def build_parent_map(tree: Tree) -> dict[str, str]:
    return {edge.target: edge.source for edge in tree.edges}

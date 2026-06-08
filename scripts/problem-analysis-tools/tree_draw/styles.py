DEFAULT_STYLE = {
    "layout": {
        "level_gap": 92,
        "sibling_gap": 72,
        "subtree_gap": 32,
        "padding": 32,
    },
    "node": {
        "radius": 22,
        "fill": "#ffffff",
        "stroke": "#334155",
        "stroke_width": 2,
        "text_color": "#111827",
        "shape": "circle",
    },
    "edge": {
        "stroke": "#64748b",
        "width": 2,
        "dash": "",
        "arrow": False,
    },
    "font": {
        "size": 14,
        "family": "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
    },
}


def deep_merge(base: dict, override: dict | None) -> dict:
    result = {}
    for key, value in base.items():
        if isinstance(value, dict):
            result[key] = deep_merge(value, None)
        else:
            result[key] = value

    if not override:
        return result

    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def resolve_style(global_style: dict, category: str, local_style: dict | None = None) -> dict:
    return deep_merge(global_style.get(category, {}), local_style or {})

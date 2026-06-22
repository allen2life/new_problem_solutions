#!/usr/bin/env python3
"""Render a dense OJ algorithm teaching board from ai-image-layout.json."""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1088
DEFAULT_LAYOUT = "problem-analysis-workspace/ai-image-layout.json"
DEFAULT_OUTPUT = "one-page-explainer-dense-v1.png"

GENERIC_PHRASES = {
    "先明确目标",
    "抓住输入限制",
    "发现核心结构",
    "把题意改写成更好处理的形式",
    "复杂度落到可通过范围",
}


class LayoutError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise LayoutError(f"layout json is invalid: {exc}") from exc
    if not isinstance(data, dict):
        raise LayoutError("layout root must be an object")
    return data


def as_text(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def validate_layout(layout: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if as_text(layout.get("schema_version")) != "dense_algorithm_board/v1":
        errors.append("schema_version must be dense_algorithm_board/v1")

    for key in ("title", "subtitle"):
        if not as_text(layout.get(key)):
            errors.append(f"{key} is required")

    top_flow = as_list(layout.get("top_flow"))
    if not 3 <= len(top_flow) <= 6:
        errors.append("top_flow must contain 3 to 6 steps")
    for index, item in enumerate(top_flow, start=1):
        if not isinstance(item, dict):
            errors.append(f"top_flow[{index}] must be an object")
            continue
        if not as_text(item.get("title")) or not as_text(item.get("detail")):
            errors.append(f"top_flow[{index}] needs title and detail")

    columns = as_list(layout.get("columns"))
    if len(columns) != 3:
        errors.append("columns must contain exactly 3 main columns")
    for col_index, column in enumerate(columns, start=1):
        if not isinstance(column, dict):
            errors.append(f"columns[{col_index}] must be an object")
            continue
        if not as_text(column.get("title")):
            errors.append(f"columns[{col_index}] needs title")
        blocks = as_list(column.get("blocks"))
        if not 3 <= len(blocks) <= 5:
            errors.append(f"columns[{col_index}].blocks must contain 3 to 5 blocks")
        for block_index, block in enumerate(blocks, start=1):
            if not isinstance(block, dict):
                errors.append(f"columns[{col_index}].blocks[{block_index}] must be an object")
                continue
            has_items = bool(as_list(block.get("items")))
            has_formula = bool(as_text(block.get("formula")))
            has_table = isinstance(block.get("table"), dict)
            if not as_text(block.get("title")):
                errors.append(f"columns[{col_index}].blocks[{block_index}] needs title")
            if not (has_items or has_formula or has_table):
                errors.append(
                    f"columns[{col_index}].blocks[{block_index}] needs items, formula, or table"
                )

    variables = as_list(layout.get("variables"))
    if len(variables) < 2:
        errors.append("variables must contain at least 2 entries")
    for index, variable in enumerate(variables, start=1):
        if not isinstance(variable, dict):
            errors.append(f"variables[{index}] must be an object")
            continue
        if not as_text(variable.get("name")) or not as_text(variable.get("meaning")):
            errors.append(f"variables[{index}] needs name and meaning")

    training_tips = as_list(layout.get("training_tips"))
    if len(training_tips) < 3:
        errors.append("training_tips must contain at least 3 items")

    pitfalls = as_list(layout.get("pitfalls"))
    if len(pitfalls) < 3:
        errors.append("pitfalls must contain at least 3 items")

    complexity = layout.get("complexity")
    if not isinstance(complexity, dict):
        errors.append("complexity must be an object")
    else:
        if not as_text(complexity.get("time")):
            errors.append("complexity.time is required")
        if not as_text(complexity.get("space")):
            errors.append("complexity.space is required")

    text_blob = json.dumps(layout, ensure_ascii=False)
    for phrase in GENERIC_PHRASES:
        if phrase in text_blob:
            errors.append(f"layout still contains generic phrase: {phrase}")

    return errors


def inline_html(text: Any) -> str:
    raw = as_text(text)
    pieces = re.split(r"(`[^`]+`)", raw)
    rendered: list[str] = []
    for piece in pieces:
        if piece.startswith("`") and piece.endswith("`"):
            rendered.append(f"<code>{html.escape(piece[1:-1])}</code>")
        else:
            rendered.append(html.escape(piece))
    return "".join(rendered)


def render_list(items: list[Any], class_name: str = "") -> str:
    body = "".join(f"<li>{inline_html(item)}</li>" for item in items if as_text(item))
    return f'<ul class="{class_name}">{body}</ul>'


def render_table(table: dict[str, Any]) -> str:
    headers = [as_text(item) for item in as_list(table.get("headers"))]
    rows = as_list(table.get("rows"))
    head = "".join(f"<th>{inline_html(item)}</th>" for item in headers)
    body_rows: list[str] = []
    for row in rows[:5]:
        cells = as_list(row)
        body_rows.append("".join(f"<td>{inline_html(cell)}</td>" for cell in cells[:4]))
    body = "".join(f"<tr>{row}</tr>" for row in body_rows)
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render_block(block: dict[str, Any], index: int) -> str:
    parts = [
        '<section class="block">',
        f'<div class="block-title"><span>{index}</span>{inline_html(block.get("title"))}</div>',
    ]
    formula = as_text(block.get("formula"))
    if formula:
        parts.append(f'<div class="formula">{inline_html(formula)}</div>')
    items = [item for item in as_list(block.get("items")) if as_text(item)]
    if items:
        parts.append(render_list(items))
    table = block.get("table")
    if isinstance(table, dict):
        parts.append(render_table(table))
    diagram = as_text(block.get("diagram"))
    if diagram:
        parts.append(f'<div class="diagram">{inline_html(diagram)}</div>')
    parts.append("</section>")
    return "".join(parts)


def render_column(column: dict[str, Any], index: int) -> str:
    theme = as_text(column.get("theme")) or ["blue", "green", "orange"][index % 3]
    blocks = as_list(column.get("blocks"))
    block_html = "".join(render_block(block, i) for i, block in enumerate(blocks[:6], start=1) if isinstance(block, dict))
    return (
        f'<article class="panel theme-{html.escape(theme)}">'
        f'<header><span>{index + 1}</span>{inline_html(column.get("title"))}</header>'
        f'<div class="panel-body"><div class="panel-content">{block_html}</div></div>'
        "</article>"
    )


def render_flow(flow: list[Any]) -> str:
    cards: list[str] = []
    for index, item in enumerate(flow, start=1):
        if not isinstance(item, dict):
            continue
        cards.append(
            '<div class="flow-card">'
            f'<div class="flow-index">{index}</div>'
            f'<strong>{inline_html(item.get("title"))}</strong>'
            f'<p>{inline_html(item.get("detail"))}</p>'
            "</div>"
        )
    return "".join(cards)


def render_bottom(layout: dict[str, Any]) -> str:
    variables = as_list(layout.get("variables"))
    complexity = layout.get("complexity") if isinstance(layout.get("complexity"), dict) else {}
    notes = as_list(complexity.get("notes"))
    variable_rows = "".join(
        f"<li><code>{html.escape(as_text(item.get('name')))}</code> {inline_html(item.get('meaning'))}</li>"
        for item in variables[:6]
        if isinstance(item, dict)
    )
    return "".join(
        [
            '<section class="bottom-card tips"><h2>训练建议</h2>',
            render_list(as_list(layout.get("training_tips"))[:5], "compact"),
            "</section>",
            '<section class="bottom-card pitfalls"><h2>常见坑点</h2>',
            render_list(as_list(layout.get("pitfalls"))[:5], "compact"),
            "</section>",
            '<section class="bottom-card vars"><h2>关键变量</h2><ul class="compact">',
            variable_rows,
            "</ul></section>",
            '<section class="bottom-card complexity"><h2>复杂度</h2>',
            f'<p><b>时间</b>：{inline_html(complexity.get("time"))}</p>',
            f'<p><b>空间</b>：{inline_html(complexity.get("space"))}</p>',
            render_list(notes[:3], "compact") if notes else "",
            "</section>",
        ]
    )


def build_html(layout: dict[str, Any], width: int, height: int) -> str:
    columns = as_list(layout.get("columns"))
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={width}, initial-scale=1">
<style>
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; width: {width}px; height: {height}px; overflow: hidden; }}
body {{
  background: #f8fafc;
  color: #111827;
  font-family: "Noto Sans CJK SC", "Source Han Sans SC", "Microsoft YaHei", Arial, sans-serif;
}}
#board {{
  width: {width}px;
  height: {height}px;
  padding: 18px 34px 18px;
  display: grid;
  grid-template-rows: 76px 98px 1fr 154px;
  gap: 10px;
  background:
    linear-gradient(180deg, rgba(255,255,255,0.96), rgba(248,250,252,0.98)),
    radial-gradient(circle at 18% 18%, rgba(59,130,246,0.07), transparent 24%),
    radial-gradient(circle at 78% 22%, rgba(34,197,94,0.07), transparent 24%);
}}
.title h1 {{
  margin: 0;
  text-align: center;
  font-size: 38px;
  line-height: 1.08;
  font-weight: 850;
  letter-spacing: 0;
}}
.title p {{
  margin: 7px auto 0;
  text-align: center;
  font-size: 20px;
  line-height: 1.25;
  max-width: 1450px;
  font-weight: 560;
}}
.flow {{
  display: grid;
  grid-template-columns: repeat({max(3, min(6, len(as_list(layout.get("top_flow")))))}, 1fr);
  gap: 18px;
  align-items: stretch;
}}
.flow-card {{
  position: relative;
  min-width: 0;
  padding: 11px 15px 10px 48px;
  border: 2px solid #94a3b8;
  border-radius: 10px;
  background: rgba(255,255,255,0.9);
  box-shadow: 0 3px 10px rgba(15,23,42,0.06);
}}
.flow-card:not(:last-child)::after {{
  content: "";
  position: absolute;
  top: 50%;
  right: -22px;
  width: 20px;
  height: 2px;
  background: #475569;
}}
.flow-index {{
  position: absolute;
  left: 13px;
  top: 12px;
  width: 25px;
  height: 25px;
  border-radius: 999px;
  background: #1d4ed8;
  color: #fff;
  display: grid;
  place-items: center;
  font-weight: 800;
  font-size: 16px;
}}
.flow-card strong {{ display: block; font-size: 20px; line-height: 1.14; margin-bottom: 6px; }}
.flow-card p {{ margin: 0; font-size: 15px; line-height: 1.18; color: #334155; }}
.main {{
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
  min-height: 0;
}}
.panel {{
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  border: 2.5px solid var(--accent);
  border-radius: 12px;
  background: var(--soft);
  overflow: hidden;
}}
.panel header {{
  padding: 10px 17px;
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,0.72);
  border-bottom: 2px solid var(--accent);
  font-size: 23px;
  line-height: 1.15;
  font-weight: 850;
}}
.panel header span {{
  width: 28px;
  height: 28px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: var(--accent);
  color: white;
  font-size: 17px;
  flex: 0 0 auto;
}}
.panel-body {{
  min-height: 0;
  overflow: hidden;
  padding: 10px 14px 12px;
}}
.panel-content {{
  transform-origin: top left;
  display: flex;
  flex-direction: column;
  gap: 7px;
}}
.theme-blue {{ --accent: #2563eb; --soft: #eff6ff; --pale: #dbeafe; }}
.theme-green {{ --accent: #16a34a; --soft: #f0fdf4; --pale: #dcfce7; }}
.theme-orange {{ --accent: #ea580c; --soft: #fff7ed; --pale: #ffedd5; }}
.theme-red {{ --accent: #dc2626; --soft: #fef2f2; --pale: #fee2e2; }}
.theme-purple {{ --accent: #7c3aed; --soft: #f5f3ff; --pale: #ede9fe; }}
.block {{
  background: rgba(255,255,255,0.78);
  border: 1.7px solid color-mix(in srgb, var(--accent) 55%, white);
  border-radius: 10px;
  padding: 7px 11px 7px;
}}
.block-title {{
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 16.5px;
  line-height: 1.18;
  font-weight: 820;
  margin-bottom: 5px;
}}
.block-title span {{
  width: 20px;
  height: 20px;
  display: grid;
  place-items: center;
  border-radius: 7px;
  background: var(--accent);
  color: #fff;
  font-size: 13px;
  flex: 0 0 auto;
}}
.formula {{
  margin: 5px 0;
  padding: 6px 9px;
  background: var(--pale);
  border-radius: 8px;
  font-size: 15.5px;
  line-height: 1.2;
  font-weight: 700;
}}
ul {{ margin: 0; padding-left: 23px; }}
li {{ margin: 2px 0; font-size: 14.8px; line-height: 1.22; }}
code {{
  font-family: "JetBrains Mono", "Cascadia Mono", Consolas, monospace;
  background: rgba(15,23,42,0.08);
  padding: 0 5px;
  border-radius: 5px;
  font-size: 0.95em;
  font-weight: 700;
}}
table {{
  width: 100%;
  border-collapse: collapse;
  margin-top: 5px;
  font-size: 13.5px;
  background: white;
}}
th, td {{ border: 1px solid #cbd5e1; padding: 4px 6px; text-align: center; }}
th {{ background: var(--pale); font-weight: 820; }}
.diagram {{
  margin-top: 5px;
  padding: 6px 9px;
  border-radius: 9px;
  background: rgba(255,255,255,0.8);
  border: 1px dashed color-mix(in srgb, var(--accent) 60%, white);
  font-size: 14.5px;
  line-height: 1.25;
  text-align: center;
  font-weight: 680;
}}
.bottom {{
  display: grid;
  grid-template-columns: 1.15fr 1.15fr 1fr 0.9fr;
  gap: 18px;
  min-height: 0;
}}
.bottom-card {{
  min-width: 0;
  overflow: hidden;
  border-radius: 11px;
  padding: 8px 14px;
  border: 2px solid #cbd5e1;
  background: rgba(255,255,255,0.84);
}}
.bottom-card h2 {{ margin: 0 0 5px; font-size: 19px; line-height: 1.12; font-weight: 850; }}
.tips {{ border-color: #60a5fa; background: #eff6ff; }}
.pitfalls {{ border-color: #f87171; background: #fef2f2; }}
.vars {{ border-color: #34d399; background: #ecfdf5; }}
.complexity {{ border-color: #f59e0b; background: #fffbeb; }}
.compact li {{ font-size: 13.6px; line-height: 1.15; margin: 1px 0; }}
.complexity p {{ margin: 2px 0; font-size: 14px; line-height: 1.16; }}
</style>
</head>
<body>
<main id="board">
  <section class="title">
    <h1>{inline_html(layout.get("title"))}</h1>
    <p>{inline_html(layout.get("subtitle"))}</p>
  </section>
  <section class="flow">{render_flow(as_list(layout.get("top_flow")))}</section>
  <section class="main">
    {"".join(render_column(column, index) for index, column in enumerate(columns[:3]) if isinstance(column, dict))}
  </section>
  <section class="bottom">{render_bottom(layout)}</section>
</main>
<script>
for (const body of document.querySelectorAll('.panel-body')) {{
  const content = body.querySelector('.panel-content');
  if (!content) continue;
  const available = body.clientHeight;
  const needed = content.scrollHeight;
  if (needed > available) {{
    const scale = Math.max(0.72, available / needed);
    content.style.transform = `scale(${{scale}})`;
    content.style.width = `${{100 / scale}}%`;
  }}
}}
document.body.dataset.boardReady = '1';
</script>
</body>
</html>
"""


def render_layout(
    layout_path: Path,
    output_path: Path,
    *,
    html_output: Path | None = None,
    width: int = DEFAULT_WIDTH,
    height: int = DEFAULT_HEIGHT,
) -> None:
    layout = read_json(layout_path)
    errors = validate_layout(layout)
    if errors:
        raise LayoutError("; ".join(errors))

    document = build_html(layout, width, height)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if html_output is not None:
        html_output.parent.mkdir(parents=True, exist_ok=True)
        html_output.write_text(document, encoding="utf-8")
        page_path = html_output
        cleanup = None
    else:
        temp = tempfile.NamedTemporaryFile("w", suffix=".html", encoding="utf-8", delete=False)
        temp.write(document)
        temp.close()
        page_path = Path(temp.name)
        cleanup = page_path

    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            executable_path = find_system_browser()
            launch_args: dict[str, Any] = {}
            if executable_path:
                launch_args["executable_path"] = executable_path
            browser = p.chromium.launch(**launch_args)
            page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
            page.goto(page_path.resolve().as_uri(), wait_until="networkidle")
            page.wait_for_function("document.body.dataset.boardReady === '1'")
            page.locator("#board").screenshot(path=str(output_path))
            browser.close()
    finally:
        if cleanup is not None:
            cleanup.unlink(missing_ok=True)


def find_system_browser() -> str | None:
    for name in (
        "chromium",
        "chromium-browser",
        "google-chrome",
        "google-chrome-stable",
        "microsoft-edge",
    ):
        path = shutil.which(name)
        if path:
            return path
    return None


def resolve_problem_path(problem_dir: Path, path_value: str) -> Path:
    path = Path(path_value)
    return path if path.is_absolute() else problem_dir / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render dense OJ algorithm board from layout JSON.")
    parser.add_argument("--problem-dir", required=True, help="Problem directory, e.g. problems/luogu/P1001.")
    parser.add_argument("--layout", default=DEFAULT_LAYOUT, help="Layout JSON path relative to problem-dir.")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="PNG output path relative to problem-dir.")
    parser.add_argument(
        "--html-output",
        default="problem-analysis-workspace/ai-image-preview.html",
        help="Optional HTML preview path relative to problem-dir.",
    )
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--check-only", action="store_true", help="Validate layout JSON without rendering.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    problem_dir = Path(args.problem_dir).resolve()
    layout_path = resolve_problem_path(problem_dir, args.layout)
    output_path = resolve_problem_path(problem_dir, args.output)
    html_output = resolve_problem_path(problem_dir, args.html_output) if args.html_output else None

    try:
        layout = read_json(layout_path)
        errors = validate_layout(layout)
        if errors:
            raise LayoutError("; ".join(errors))
        if args.check_only:
            print(f"layout ok: {layout_path}")
            return 0
        render_layout(
            layout_path,
            output_path,
            html_output=html_output,
            width=args.width,
            height=args.height,
        )
    except Exception as exc:
        print(f"render failed: {exc}", file=sys.stderr)
        return 1

    print(f"Rendered: {output_path}")
    if html_output is not None:
        print(f"Preview HTML: {html_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

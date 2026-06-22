#!/usr/bin/env python3
"""Batch-check and render dense algorithm-board layouts.

This script intentionally does not invent dense board content. A high-quality
`ai-image-layout.json` must be written by an agent after reading the completed
article and code. The batch script only finds ready problems, validates existing
layouts, renders candidates, and records a todo list.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SCRIPT_PATH = Path(__file__).resolve()
SKILL_DIR = SCRIPT_PATH.parent
REPO_ROOT = SCRIPT_PATH.parents[4]
PROBLEMS_ROOT = REPO_ROOT / "problems"
RENDERER_PATH = SKILL_DIR / "render_dense_algorithm_board.py"


def load_renderer_module() -> Any:
    spec = importlib.util.spec_from_file_location("dense_board_renderer", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载渲染脚本：{RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RENDERER = load_renderer_module()


COMPLEX_TAGS = {
    "动态规划",
    "dp",
    "图论",
    "树形DP",
    "状态压缩",
    "最短路",
    "线段树",
    "最小生成树",
    "拓扑排序",
    "区间dp",
    "树",
    "树形结构",
    "树链剖分",
    "并查集",
    "二分",
    "二分答案",
    "贪心",
    "背包",
    "组合计数",
    "容斥",
    "数论",
    "构造",
    "建模",
    "BFS",
    "bfs",
    "dfs",
    "Floyd",
    "LCA",
}

SIMPLE_TAGS = {
    "模拟",
    "枚举",
    "排序",
    "字符串",
    "前缀和",
    "递推",
    "递归",
    "计数",
    "网格",
    "noip",
}

DIFF_SCORE = {
    "入门": 0,
    "普及-": 1,
    "普及/提高-": 2,
    "普及+/提高": 3,
    "提高+/省选-": 4,
    "省选/NOI-": 5,
    "NOI/NOI+/CTSC": 6,
    "未知": 1,
}


@dataclass
class ProblemMeta:
    problem_dir: Path
    oj: str
    problem_id: str
    title: str
    difficulty: str
    description: str
    tags: list[str]
    body_length: int
    ready: bool
    score: int
    should_generate: bool
    skip_reason: str

    @property
    def rel_dir(self) -> str:
        return self.problem_dir.relative_to(REPO_ROOT).as_posix()

    @property
    def workspace_dir(self) -> Path:
        return self.problem_dir / "problem-analysis-workspace"

    @property
    def layout_path(self) -> Path:
        return self.workspace_dir / "ai-image-layout.json"

    @property
    def wiki_ref(self) -> str:
        return f"[[problem: {self.oj},{self.problem_id}]]"


def parse_frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*)$", text, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if value[:1] in {'"', "'"} and value[-1:] == value[:1]:
        value = value[1:-1]
    return value.strip()


def parse_tags(text: str) -> list[str]:
    match = re.search(r"^tags:\s*\[(.*?)\]\s*$", text, re.MULTILINE)
    if not match:
        return []
    raw = match.group(1).strip()
    if not raw:
        return []
    tags = []
    for item in raw.split(","):
        tag = item.strip().strip('"').strip("'")
        if tag:
            tags.append(tag)
    return tags


def is_ready_article(text: str, problem_dir: Path) -> tuple[bool, str, int]:
    has_main = "@include-code(./main.cpp, cpp)" in text and (problem_dir / "main.cpp").exists()
    has_brute = (problem_dir / "brute.cpp").exists()
    has_stub = "<!-- 由题目解析 skill 填写 -->" in text
    description = parse_frontmatter_value(text, "description")
    has_core_sections = all(section in text for section in ("### 题意", "### 思路", "### 代码", "### 复杂度"))
    body = text.split("---", 2)[-1] if text.startswith("---") else text
    body_length = len(body)

    if not has_main or not has_brute:
        return False, "缺少 main.cpp 或 brute.cpp", body_length
    if has_stub:
        return False, "index.md 仍包含脚手架占位内容", body_length
    if not description:
        return False, "frontmatter description 为空", body_length
    if not has_core_sections:
        return False, "正文缺少核心章节", body_length
    if body_length <= 800:
        return False, "题解正文过短，暂不适合做 dense board", body_length
    return True, "", body_length


def score_problem(title: str, difficulty: str, tags: list[str], body_length: int) -> int:
    score = DIFF_SCORE.get(difficulty, 1)
    complex_count = sum(1 for tag in tags if tag in COMPLEX_TAGS)
    simple_count = sum(1 for tag in tags if tag in SIMPLE_TAGS)

    score += min(complex_count, 3)
    if body_length >= 1800:
        score += 1
    if body_length >= 3000:
        score += 1
    if complex_count == 0 and simple_count > 0:
        score -= 1
    if "模拟" in tags and complex_count == 0:
        score -= 1
    if title == "A+B Problem":
        score -= 3
    return score


def decide_generation(meta: ProblemMeta) -> tuple[bool, str]:
    if not meta.ready:
        return False, meta.skip_reason
    if meta.score >= 4:
        return True, ""
    if meta.difficulty == "入门":
        return False, "题目难度较低，dense board 容易变成重复正文。"
    if "模拟" in meta.tags and all(tag not in COMPLEX_TAGS for tag in meta.tags):
        return False, "本题更适合看样例或局部流程图，不适合高密度算法讲义板。"
    return False, "本题整体路线较短，暂不建议额外生成 dense board。"


def collect_problems() -> tuple[list[ProblemMeta], list[ProblemMeta]]:
    ready_items: list[ProblemMeta] = []
    skipped_items: list[ProblemMeta] = []

    for index_md in PROBLEMS_ROOT.rglob("index.md"):
        problem_dir = index_md.parent
        text = index_md.read_text(encoding="utf-8", errors="ignore")
        ready, skip_reason, body_length = is_ready_article(text, problem_dir)
        oj = parse_frontmatter_value(text, "oj") or problem_dir.parent.name
        problem_id = parse_frontmatter_value(text, "problem_id") or problem_dir.name
        title = parse_frontmatter_value(text, "title") or problem_id
        difficulty = parse_frontmatter_value(text, "difficulty") or "未知"
        description = parse_frontmatter_value(text, "description")
        tags = parse_tags(text)
        score = score_problem(title, difficulty, tags, body_length)
        meta = ProblemMeta(
            problem_dir=problem_dir,
            oj=oj,
            problem_id=problem_id,
            title=title,
            difficulty=difficulty,
            description=description,
            tags=tags,
            body_length=body_length,
            ready=ready,
            score=score,
            should_generate=False,
            skip_reason=skip_reason,
        )
        should_generate, decision_reason = decide_generation(meta)
        meta.should_generate = should_generate
        if not should_generate and decision_reason:
            meta.skip_reason = decision_reason
        if meta.ready:
            ready_items.append(meta)
        else:
            skipped_items.append(meta)

    ready_items.sort(key=lambda item: (-item.score, item.oj, item.problem_id))
    skipped_items.sort(key=lambda item: (item.oj, item.problem_id))
    return ready_items, skipped_items


def short_tags(tags: list[str], limit: int = 4) -> str:
    if not tags:
        return "无标签"
    return " / ".join(tags[:limit])


def make_evaluation(meta: ProblemMeta) -> str:
    if meta.should_generate:
        conclusion = "是"
        reason = "这题存在较明显的建模或多阶段算法路线，适合做 dense_algorithm_board。"
        goal = "\n".join(
            [
                "- 用三栏讲义板压缩题意建模、核心转移和实现检查。",
                "- 明确列出关键变量、短公式、常见坑点和训练建议。",
                "- 让读者在读代码前先建立完整路线。",
            ]
        )
        next_step = "由 agent 阅读题解与代码后手写 `ai-image-layout.json`，再用本地渲染器生成 PNG。"
    else:
        conclusion = "否"
        reason = meta.skip_reason
        goal = "- 本题暂不需要高密度算法讲义板，正文或局部可视化更合适。"
        next_step = "不渲染 dense board。"

    return "\n".join(
        [
            "# AI 一图流评估",
            "",
            "## 是否生成",
            "",
            f"- 结论：{conclusion}",
            f"- 原因：{reason}",
            "",
            "## 适合一图流的教学目标",
            "",
            goal,
            "",
            "## 不适合放进 dense board 的信息",
            "",
            "- 不放长代码。",
            "- 不放题解没有验证的精确样例值、边权或 DP 状态值。",
            "- 不加入题解和代码没有支持的新算法步骤。",
            "",
            "## 后续动作",
            "",
            next_step,
            "",
        ]
    )


def write_todo(todo_path: Path, ready_items: list[ProblemMeta], skipped_items: list[ProblemMeta]) -> None:
    lines = [
        "---",
        'title: "Dense Algorithm Board 待处理清单"',
        'description: "已完成题解的 dense_algorithm_board 评估与渲染记录。"',
        "---",
        "",
        "# Dense Algorithm Board 待处理清单",
        "",
        "说明：",
        "- 只纳入已完成 `index.md`、`main.cpp`、`brute.cpp` 的题目解析。",
        "- 本脚本不自动编写 `ai-image-layout.json`，避免生成泛化低质量图。",
        "- 有 layout 的题可以批量校验和渲染；没有 layout 的题只记录为待人工/agent 生成布局。",
        "",
        f"已完成题解：`{len(ready_items)}` 题",
        f"未纳入：`{len(skipped_items)}` 题",
        "",
        "## 待处理题目",
        "",
    ]

    for item in ready_items:
        priority = "建议 dense" if item.should_generate else "仅评估"
        layout_state = "已有 layout" if item.layout_path.exists() else "缺 layout"
        lines.append(
            f"- [ ] {item.wiki_ref} `{item.difficulty}` `{short_tags(item.tags)}` "
            f"{item.title} [{priority}] [{layout_state}]"
        )

    if skipped_items:
        lines.extend(["", "## 未纳入", ""])
        for item in skipped_items:
            lines.append(f"- [ ] {item.wiki_ref} {item.title} - {item.skip_reason}")

    lines.append("")
    todo_path.write_text("\n".join(lines), encoding="utf-8")


def update_todo_status(todo_path: Path, item: ProblemMeta, message: str) -> None:
    if not todo_path.exists():
        return
    content = todo_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"^- \[(?P<mark>[ x])\] {re.escape(item.wiki_ref)}(?P<rest>.*)$",
        re.MULTILINE,
    )
    match = pattern.search(content)
    if not match:
        return
    new_line = f"- [x] {item.wiki_ref}{match.group('rest')} - {message}"
    content = content[: match.start()] + new_line + content[match.end() :]
    todo_path.write_text(content, encoding="utf-8")


def append_report(problem_dir: Path, output_path: Path, passed: bool, issue: str, elapsed: float) -> None:
    report_path = problem_dir / "problem-analysis-workspace" / "ai-image-report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    current = report_path.read_text(encoding="utf-8") if report_path.exists() else "# AI 图片生成报告\n"
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    status = "通过" if passed else "不通过"
    recommend = "是" if passed else "否"
    section = "\n".join(
        [
            "",
            f"## dense 渲染记录 {timestamp}",
            "",
            "- 布局文件：`problem-analysis-workspace/ai-image-layout.json`",
            f"- 输出文件：`{output_path.name}`",
            "- 渲染方式：`dense_algorithm_board` + Playwright",
            "- 尺寸：`1920x1088`",
            f"- 耗时：{elapsed:.1f}s",
            f"- 检查结论：{status}",
            f"- 问题：{issue or '无'}",
            f"- 是否建议插入 `index.md`：{recommend}",
            "",
        ]
    )
    report_path.write_text(current.rstrip() + "\n" + section, encoding="utf-8")


def png_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    width = int.from_bytes(data[16:20], "big")
    height = int.from_bytes(data[20:24], "big")
    return width, height


def review_png(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "输出文件不存在"
    dims = png_dimensions(path)
    if dims is None:
        return False, "输出文件不是合法 PNG"
    width, height = dims
    if width != 1920 or height != 1088:
        return False, f"尺寸不是 1920x1088：{width}x{height}"
    if path.stat().st_size < 80 * 1024:
        return False, "文件体积过小，疑似空图或渲染异常"
    return True, f"PNG 检查通过：{width}x{height}"


def write_evaluation(item: ProblemMeta) -> None:
    item.workspace_dir.mkdir(parents=True, exist_ok=True)
    (item.workspace_dir / "07-ai-image-evaluation.md").write_text(make_evaluation(item), encoding="utf-8")


def render_existing_layout(item: ProblemMeta, *, adopt: bool) -> tuple[bool, str]:
    if not item.layout_path.exists():
        return False, "缺少 ai-image-layout.json"

    output = item.problem_dir / "one-page-explainer-dense-v1.png"
    html_output = item.workspace_dir / "ai-image-preview.html"
    started = time.time()
    try:
        RENDERER.render_layout(item.layout_path, output, html_output=html_output)
    except Exception as exc:
        elapsed = time.time() - started
        append_report(item.problem_dir, output, False, str(exc), elapsed)
        return False, str(exc)

    ok, message = review_png(output)
    elapsed = time.time() - started
    append_report(item.problem_dir, output, ok, "" if ok else message, elapsed)
    if ok and adopt:
        shutil.copyfile(output, item.problem_dir / "one-page-explainer.png")
    return ok, message


def run(args: argparse.Namespace) -> int:
    ready_items, skipped_items = collect_problems()
    todo_path = (REPO_ROOT / args.todo).resolve()
    write_todo(todo_path, ready_items, skipped_items)

    if args.phase in {"all", "prepare"}:
        prepared = 0
        for item in ready_items:
            write_evaluation(item)
            update_todo_status(todo_path, item, "已写评估")
            prepared += 1
        print(f"prepared={prepared} ready={len(ready_items)} skipped={len(skipped_items)}")
        if args.phase == "prepare":
            return 0
        write_todo(todo_path, ready_items, skipped_items)

    processed = 0
    failed = 0
    for item in ready_items:
        if args.only_with_layout and not item.layout_path.exists():
            continue
        if not item.should_generate and not args.force:
            continue
        if args.limit is not None and processed >= args.limit:
            break
        ok, message = render_existing_layout(item, adopt=args.adopt)
        if ok:
            update_todo_status(todo_path, item, f"已渲染（{message}）")
            processed += 1
            print(f"rendered {processed}: {item.rel_dir}")
        else:
            update_todo_status(todo_path, item, f"渲染失败：{message}")
            failed += 1
            print(f"render_failed {item.rel_dir}: {message}")
            if not args.continue_on_error:
                break

    print(f"finished rendered={processed} failed={failed} ready={len(ready_items)} skipped={len(skipped_items)}")
    return 0 if failed == 0 else 4


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="批量校验并渲染 dense_algorithm_board")
    parser.add_argument(
        "--phase",
        choices=["all", "prepare", "render"],
        default="all",
        help="prepare 只写评估；render 渲染已有 layout；all 依次执行。",
    )
    parser.add_argument("--todo", default="todo_dense_board.md", help="待办清单路径。")
    parser.add_argument("--limit", type=int, default=None, help="最多渲染多少题。")
    parser.add_argument("--force", action="store_true", help="也渲染仅评估题，只要有 layout。")
    parser.add_argument("--only-with-layout", action="store_true", help="只处理已有 layout 的题。")
    parser.add_argument("--adopt", action="store_true", help="通过 PNG 检查后复制为 one-page-explainer.png。")
    parser.add_argument("--continue-on-error", action="store_true", help="单题失败后继续处理后续题。")
    return parser.parse_args()


def main() -> int:
    return run(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

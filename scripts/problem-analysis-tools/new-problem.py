#!/usr/bin/env python3
"""Create a new problem directory using the current OJ ebook structure."""

from __future__ import annotations

import argparse
import datetime as dt
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_ROOT = REPO_ROOT / "problems"


def infer_from_cwd() -> tuple[str | None, str | None]:
    try:
        relative = Path.cwd().resolve().relative_to(PROBLEMS_ROOT)
    except ValueError:
        return None, None
    parts = relative.parts
    if len(parts) >= 2:
        return parts[0], parts[1]
    return None, None


def quote_yaml(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def write_if_missing(path: Path, content: str) -> bool:
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


def index_template(oj: str, problem_id: str, title: str, source: str) -> str:
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    source_line = source if source else ""
    return f"""---
oj: {quote_yaml(oj)}
problem_id: {quote_yaml(problem_id)}
title: {quote_yaml(title)}
date: {now}
toc: true
tags: []
categories: []
source: {source_line}
---

[[TOC]]

### 题意

<!-- 由题目解析 skill 填写 -->

### 思路

<!-- 由题目解析 skill 填写 -->

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

<!-- 由题目解析 skill 填写 -->

### 总结

<!-- 由题目解析 skill 填写 -->
"""


def main_cpp_template() -> str:
    return """#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    return 0;
}
"""


def brute_cpp_template() -> str:
    return """#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    return 0;
}
"""


def gen_py_template() -> str:
    return """#!/usr/bin/env python3
import random


def main():
    random.seed()
    # TODO: generate input for this problem.


if __name__ == "__main__":
    main()
"""


def workspace_template(title: str) -> str:
    return f"""# {title}

<!-- 由 oj-problem-analysis-writer 填写 -->
"""


def create_problem(args: argparse.Namespace) -> int:
    oj = args.oj
    problem_id = args.problem_id
    if not oj or not problem_id:
        inferred_oj, inferred_id = infer_from_cwd()
        oj = oj or inferred_oj
        problem_id = problem_id or inferred_id

    if not oj or not problem_id:
        print("缺少 oj/problem_id。用法：new-problem.py <oj> <problem_id>")
        return 2

    if re.search(r"[\\/]", oj) or re.search(r"[\\/]", problem_id):
        print("oj 和 problem_id 不能包含路径分隔符。")
        return 2

    problem_dir = PROBLEMS_ROOT / oj / problem_id
    workspace = problem_dir / "problem-analysis-workspace"
    created: list[str] = []
    skipped: list[str] = []

    files = [
        (problem_dir / "index.md", index_template(oj, problem_id, args.title, args.source)),
        (problem_dir / "main.cpp", main_cpp_template()),
    ]
    if args.with_brute:
        files.append((problem_dir / "brute.cpp", brute_cpp_template()))
    if args.with_gen:
        files.append((problem_dir / "gen.py", gen_py_template()))

    for path, content in files:
        if write_if_missing(path, content):
            created.append(str(path.relative_to(REPO_ROOT)))
        else:
            skipped.append(str(path.relative_to(REPO_ROOT)))

    if args.with_workspace:
        workspace.mkdir(parents=True, exist_ok=True)
        stages = [
            ("01-problem-understanding.md", "题意理解"),
            ("02-observation-and-model.md", "关键观察与模型"),
            ("03-solution-derivation.md", "解法推导"),
            ("04-correctness-and-edge-cases.md", "正确性与边界情况"),
            ("05-complexity-and-implementation.md", "复杂度与实现"),
            ("06-final-index-draft.md", "最终题解草稿"),
        ]
        for filename, title in stages:
            path = workspace / filename
            if write_if_missing(path, workspace_template(title)):
                created.append(str(path.relative_to(REPO_ROOT)))
            else:
                skipped.append(str(path.relative_to(REPO_ROOT)))

    if args.with_gen:
        gen_path = problem_dir / "gen.py"
        try:
            gen_path.chmod(gen_path.stat().st_mode | 0o111)
        except FileNotFoundError:
            pass

    print(f"题目目录：{problem_dir.relative_to(REPO_ROOT)}")
    if created:
        print("\n创建：")
        for item in created:
            print(f"- {item}")
    if skipped:
        print("\n已存在，跳过：")
        for item in skipped:
            print(f"- {item}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a new OJ problem directory")
    parser.add_argument("oj", nargs="?")
    parser.add_argument("problem_id", nargs="?")
    parser.add_argument("--title", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--no-brute", dest="with_brute", action="store_false")
    parser.add_argument("--no-gen", dest="with_gen", action="store_false")
    parser.add_argument("--no-workspace", dest="with_workspace", action="store_false")
    parser.set_defaults(with_brute=True, with_gen=True, with_workspace=True)
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(create_problem(parse_args()))

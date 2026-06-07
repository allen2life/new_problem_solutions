#!/usr/bin/env python3
"""Create a new problem directory using the current OJ ebook structure."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.problem_analysis_lib.problem_scaffold import (  # noqa: E402
    PROBLEMS_ROOT,
    create_problem_dir,
    infer_from_cwd,
    relative_to_repo,
)


def create_problem(args: argparse.Namespace) -> int:
    oj = args.oj
    problem_id = args.problem_id
    if not oj or not problem_id:
        inferred_oj, inferred_id = infer_from_cwd(PROBLEMS_ROOT)
        oj = oj or inferred_oj
        problem_id = problem_id or inferred_id

    if not oj or not problem_id:
        print("缺少 oj/problem_id。用法：new-problem.py <oj> <problem_id>")
        return 2

    try:
        result = create_problem_dir(
            oj,
            problem_id,
            title=args.title,
            source=args.source,
            with_brute=args.with_brute,
            with_gen=args.with_gen,
            with_workspace=args.with_workspace,
        )
    except ValueError as exc:
        print(str(exc))
        return 2

    print(f"题目目录：{relative_to_repo(result.problem_dir)}")
    if result.created:
        print("\n创建：")
        for item in result.created:
            print(f"- {relative_to_repo(item)}")
    if result.skipped:
        print("\n已存在，跳过：")
        for item in result.skipped:
            print(f"- {relative_to_repo(item)}")
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

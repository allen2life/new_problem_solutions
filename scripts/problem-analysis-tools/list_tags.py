#!/usr/bin/env python3
"""List tags used by problem index.md frontmatter."""

from __future__ import annotations

import argparse
import ast
import json
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_ROOT = REPO_ROOT / "problems"


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def extract_frontmatter(index_md: Path) -> list[str] | None:
    text = index_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    return text[4:end].splitlines()


def parse_top_scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return strip_scalar(stripped[len(prefix) :])
    return ""


def parse_tags(lines: list[str]) -> list[str]:
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("tags:"):
            continue

        value = stripped[len("tags:") :].strip()
        if value in {"", "[]"}:
            if value == "[]":
                return []
            return parse_block_tags(lines[idx + 1 :])

        if value.startswith("[") and value.endswith("]"):
            return parse_inline_tags(value)

        tag = strip_scalar(value)
        return [tag] if tag else []

    return []


def parse_block_tags(lines: list[str]) -> list[str]:
    tags: list[str] = []
    for line in lines:
        if line and not line.startswith((" ", "\t")):
            break
        stripped = line.strip()
        if not stripped.startswith("- "):
            continue
        tag = strip_scalar(stripped[2:])
        if tag:
            tags.append(tag)
    return tags


def parse_inline_tags(value: str) -> list[str]:
    try:
        parsed = ast.literal_eval(value)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
    except (SyntaxError, ValueError):
        pass

    inner = value[1:-1].strip()
    if not inner:
        return []
    return [strip_scalar(part) for part in inner.split(",") if strip_scalar(part)]


def collect_tags() -> dict[str, list[str]]:
    tag_map: dict[str, list[str]] = defaultdict(list)

    for index_md in sorted(PROBLEMS_ROOT.glob("*/*/index.md")):
        lines = extract_frontmatter(index_md)
        if lines is None:
            continue
        oj = parse_top_scalar(lines, "oj")
        problem_id = parse_top_scalar(lines, "problem_id")
        problem_key = f"{oj}/{problem_id}" if oj and problem_id else rel(index_md)

        for tag in parse_tags(lines):
            tag_map[tag].append(problem_key)

    return tag_map


def sorted_items(tag_map: dict[str, list[str]]) -> list[tuple[str, list[str]]]:
    return sorted(tag_map.items(), key=lambda item: (-len(item[1]), item[0]))


def print_text(tag_map: dict[str, list[str]], with_problems: bool) -> None:
    for tag, problems in sorted_items(tag_map):
        if with_problems:
            print(f"{len(problems)}\t{tag}\t{', '.join(problems)}")
        else:
            print(f"{len(problems)}\t{tag}")


def print_plain(tag_map: dict[str, list[str]]) -> None:
    for tag in sorted(tag_map):
        print(tag)


def print_json(tag_map: dict[str, list[str]]) -> None:
    data = [
        {
            "tag": tag,
            "count": len(problems),
            "problems": problems,
        }
        for tag, problems in sorted_items(tag_map)
    ]
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main() -> int:
    parser = argparse.ArgumentParser(description="列出全部题目解析 frontmatter 中已经使用的 tags")
    parser.add_argument(
        "--format",
        choices=("text", "plain", "json"),
        default="text",
        help="输出格式：text 为 count+tag，plain 为每行一个 tag，json 含引用题目",
    )
    parser.add_argument("--with-problems", action="store_true", help="text 格式下同时输出使用该 tag 的题目")
    args = parser.parse_args()

    tag_map = collect_tags()
    if args.format == "plain":
        print_plain(tag_map)
    elif args.format == "json":
        print_json(tag_map)
    else:
        print_text(tag_map, args.with_problems)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

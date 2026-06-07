#!/usr/bin/env python3
"""Check pre/common problem relations in index.md frontmatter."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PROBLEMS_ROOT = REPO_ROOT / "problems"
RELATION_FIELDS = ("pre", "common")


@dataclass
class ProblemMeta:
    problem_dir: Path
    index_md: Path
    oj: str
    problem_id: str


@dataclass
class RelationItem:
    field: str
    index: int
    data: dict[str, str]
    line_no: int


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def strip_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def extract_frontmatter(index_md: Path) -> tuple[list[str], int] | None:
    text = index_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    raw = text[4:end]
    return raw.splitlines(), 4


def parse_top_scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return strip_yaml_scalar(stripped[len(prefix) :])
    return ""


def parse_relation_block(lines: list[str], field: str) -> tuple[list[RelationItem], list[str]]:
    items: list[RelationItem] = []
    errors: list[str] = []
    in_block = False
    current: dict[str, str] | None = None
    current_line = 0

    def finish_current() -> None:
        nonlocal current, current_line
        if current is not None:
            items.append(RelationItem(field=field, index=len(items) + 1, data=current, line_no=current_line))
        current = None
        current_line = 0

    for line_no, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if not in_block:
            if stripped == f"{field}:":
                in_block = True
                continue
            if stripped.startswith(f"{field}:"):
                value = stripped[len(field) + 1 :].strip()
                if value in {"", "[]"}:
                    return items, errors
                errors.append(f"`{field}` 必须是数组，建议写成 `{field}: []` 或 YAML 对象数组。")
                return items, errors
            continue

        if line and not line.startswith((" ", "\t")):
            finish_current()
            break

        item_text = stripped
        if item_text.startswith("- "):
            finish_current()
            current = {}
            current_line = line_no
            rest = item_text[2:].strip()
            if rest:
                if ":" not in rest:
                    if "," in rest:
                        errors.append(
                            f"`{field}` 第 {len(items) + 1} 项使用了旧逗号格式 `{rest}`；"
                            "请改成包含 `oj` 和 `problem_id` 的 YAML 对象。"
                        )
                    else:
                        errors.append(f"`{field}` 第 {len(items) + 1} 项不是对象。")
                    current = None
                    current_line = 0
                    continue
                key, value = rest.split(":", 1)
                current[key.strip()] = strip_yaml_scalar(value)
            continue

        if current is None:
            errors.append(f"`{field}` 的内容必须放在 `- oj: ...` 对象项下面。")
            continue

        if ":" not in item_text:
            errors.append(f"`{field}` 第 {len(items) + 1} 项存在无法解析的行：{item_text}")
            continue
        key, value = item_text.split(":", 1)
        current[key.strip()] = strip_yaml_scalar(value)

    if in_block:
        finish_current()

    return items, errors


def scan_problem_index() -> tuple[dict[tuple[str, str], ProblemMeta], dict[tuple[str, str], ProblemMeta], list[str]]:
    by_frontmatter: dict[tuple[str, str], ProblemMeta] = {}
    by_dir: dict[tuple[str, str], ProblemMeta] = {}
    warnings: list[str] = []

    for index_md in sorted(PROBLEMS_ROOT.glob("*/*/index.md")):
        frontmatter = extract_frontmatter(index_md)
        if frontmatter is None:
            warnings.append(f"{rel(index_md)} 缺少合法 frontmatter，无法作为关系目标。")
            continue
        lines, _ = frontmatter
        oj = parse_top_scalar(lines, "oj")
        problem_id = parse_top_scalar(lines, "problem_id")
        if not oj or not problem_id:
            warnings.append(f"{rel(index_md)} 缺少 oj/problem_id，无法作为关系目标。")
            continue
        meta = ProblemMeta(
            problem_dir=index_md.parent,
            index_md=index_md,
            oj=oj,
            problem_id=problem_id,
        )
        by_frontmatter[(oj, problem_id)] = meta
        by_dir[(oj, index_md.parent.name)] = meta

    return by_frontmatter, by_dir, warnings


def infer_problem_dir_from_cwd() -> Path:
    cwd = Path.cwd().resolve()
    if (cwd / "index.md").exists():
        return cwd
    raise SystemExit("未传 problem_dir，且当前目录不是题目目录。")


def collect_problem_dirs(args: argparse.Namespace) -> list[Path]:
    if args.all:
        return sorted(path.parent for path in PROBLEMS_ROOT.glob("*/*/index.md"))
    if args.problem_dir:
        return [args.problem_dir.resolve()]
    return [infer_problem_dir_from_cwd()]


def check_relation_item(
    current: ProblemMeta,
    item: RelationItem,
    by_frontmatter: dict[tuple[str, str], ProblemMeta],
    by_dir: dict[tuple[str, str], ProblemMeta],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    label = f"{item.field}[{item.index}]"
    data = item.data

    if "pid" in data:
        errors.append(f"{label} 使用了 `pid` 字段，请改为 `problem_id`。")
    oj = data.get("oj", "")
    problem_id = data.get("problem_id", "")
    if not oj:
        errors.append(f"{label} 缺少 `oj`。")
    if not problem_id:
        errors.append(f"{label} 缺少 `problem_id`。")
    if not oj or not problem_id:
        return errors, warnings

    if oj == current.oj and problem_id == current.problem_id:
        errors.append(f"{label} 引用了当前题自己：{oj}/{problem_id}。")

    target = by_frontmatter.get((oj, problem_id))
    if target is None:
        dir_target = by_dir.get((oj, problem_id))
        if dir_target is None:
            errors.append(f"{label} 目标不存在：{oj}/{problem_id}。")
        else:
            errors.append(
                f"{label} 使用了目录名 `{problem_id}`，但目标题 frontmatter problem_id 是 "
                f"`{dir_target.problem_id}`；请使用 frontmatter 中的题号。"
            )

    if not data.get("reason"):
        warnings.append(f"{label} 缺少 `reason`，建议补一句关系原因。")

    return errors, warnings


def check_problem_dir(
    problem_dir: Path,
    by_frontmatter: dict[tuple[str, str], ProblemMeta],
    by_dir: dict[tuple[str, str], ProblemMeta],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    index_md = problem_dir / "index.md"

    if not index_md.exists():
        return [f"{rel(problem_dir)} 缺少 index.md。"], warnings

    frontmatter = extract_frontmatter(index_md)
    if frontmatter is None:
        return [f"{rel(index_md)} 缺少合法 frontmatter。"], warnings
    lines, _ = frontmatter
    current = ProblemMeta(
        problem_dir=problem_dir,
        index_md=index_md,
        oj=parse_top_scalar(lines, "oj"),
        problem_id=parse_top_scalar(lines, "problem_id"),
    )
    if not current.oj or not current.problem_id:
        errors.append(f"{rel(index_md)} 缺少 oj/problem_id。")
        return errors, warnings

    seen: set[tuple[str, str, str]] = set()
    for field in RELATION_FIELDS:
        items, parse_errors = parse_relation_block(lines, field)
        errors.extend(f"{rel(index_md)}: {message}" for message in parse_errors)
        for item in items:
            item_errors, item_warnings = check_relation_item(current, item, by_frontmatter, by_dir)
            errors.extend(f"{rel(index_md)}: {message}" for message in item_errors)
            warnings.extend(f"{rel(index_md)}: {message}" for message in item_warnings)
            key = (field, item.data.get("oj", ""), item.data.get("problem_id", ""))
            if key[1] and key[2]:
                if key in seen:
                    errors.append(f"{rel(index_md)}: {field} 存在重复关系：{key[1]}/{key[2]}。")
                seen.add(key)

    return errors, warnings


def print_report(errors: list[str], warnings: list[str], checked_count: int) -> int:
    print(f"检查题目数：{checked_count}")
    if errors:
        print("\n错误：")
        for item in errors:
            print(f"- {item}")
    if warnings:
        print("\n警告：")
        for item in warnings:
            print(f"- {item}")
    if not errors and not warnings:
        print("通过：关系字段符合当前规范。")
    elif not errors:
        print("\n结果：通过，但有警告。")
    else:
        print("\n结果：未通过。")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Check pre/common relations in problem frontmatter")
    parser.add_argument("problem_dir", nargs="?", type=Path, help="problem directory, default: cwd")
    parser.add_argument("--all", action="store_true", help="check all problems")
    args = parser.parse_args()

    if args.all and args.problem_dir:
        parser.error("--all 不能和 problem_dir 同时使用")

    by_frontmatter, by_dir, index_warnings = scan_problem_index()
    problem_dirs = collect_problem_dirs(args)
    errors: list[str] = []
    warnings: list[str] = list(index_warnings)
    for problem_dir in problem_dirs:
        problem_errors, problem_warnings = check_problem_dir(problem_dir, by_frontmatter, by_dir)
        errors.extend(problem_errors)
        warnings.extend(problem_warnings)

    return print_report(errors, warnings, len(problem_dirs))


if __name__ == "__main__":
    raise SystemExit(main())

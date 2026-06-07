#!/usr/bin/env python3
"""Shrink a failing duipai input for simple n + array style data."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
import tempfile

import duipai


def parse_array_input(data: str) -> list[int]:
    lines = [line.strip() for line in data.splitlines() if line.strip()]
    if len(lines) < 2:
        raise ValueError("第一版 shrinker 只支持：第一行 n，第二行数组")
    n = int(lines[0].split()[0])
    arr = list(map(int, lines[1].split()))
    if len(arr) != n:
        raise ValueError(f"数组长度与 n 不一致：n={n}, len={len(arr)}")
    return arr


def format_array_input(arr: list[int]) -> str:
    return f"{len(arr)}\n{' '.join(map(str, arr))}\n"


def still_fails(
    input_data: str,
    user_cmd: list[str],
    brute_cmd: list[str],
    timeout: float,
    strict: bool,
    eps: float | None,
) -> bool:
    user = duipai.run_limited_command(user_cmd, input_data, timeout)
    brute = duipai.run_limited_command(brute_cmd, input_data, timeout)
    if user.status != "OK" or brute.status != "OK":
        return True
    compare = duipai.compare_outputs(input_data, user.stdout, brute.stdout, strict, eps, None)
    return not compare.ok


def shrink_length(arr: list[int], predicate) -> list[int]:
    changed = True
    while changed and len(arr) > 1:
        changed = False
        chunk = max(1, len(arr) // 2)
        while chunk >= 1:
            start = 0
            removed = False
            while start < len(arr) and len(arr) > 1:
                candidate = arr[:start] + arr[start + chunk :]
                if candidate and predicate(candidate):
                    arr = candidate
                    changed = True
                    removed = True
                    break
                start += chunk
            if removed:
                break
            chunk //= 2
    return arr


def shrink_values(arr: list[int], predicate) -> list[int]:
    for idx, value in enumerate(list(arr)):
        candidates = [0, 1, -1]
        current = value
        while current not in (0, 1, -1):
            current = current // 2
            candidates.append(current)
        for candidate_value in candidates:
            if candidate_value == arr[idx]:
                continue
            candidate = arr[:]
            candidate[idx] = candidate_value
            if predicate(candidate):
                arr = candidate
                break
    return arr


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Shrink duipai-failed/input.txt for n + array inputs")
    parser.add_argument("--failed-dir", type=Path, default=Path("duipai-failed"))
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--user", type=Path, default=Path("main.cpp"))
    parser.add_argument("--brute", type=Path, default=Path("brute.cpp"))
    parser.add_argument("--timeout", type=float, default=2.0)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--eps", type=float, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input or args.failed_dir / "input.txt"
    output_path = args.output or args.failed_dir / "input.shrunk.txt"
    report_path = args.failed_dir / "shrink-report.md"

    try:
        original = input_path.read_text(encoding="utf-8")
        arr = parse_array_input(original)
    except Exception as exc:
        print(f"准备失败：{exc}", file=sys.stderr)
        return 2

    build_dir = Path(tempfile.gettempdir()) / "problem-analysis-shrink"
    build_dir.mkdir(parents=True, exist_ok=True)
    try:
        user_cmd = duipai.command_for(args.user, build_dir)
        brute_cmd = duipai.command_for(args.brute, build_dir)
    except Exception as exc:
        print(f"编译或定位程序失败：{exc}", file=sys.stderr)
        return 2

    def predicate(candidate: list[int]) -> bool:
        return still_fails(format_array_input(candidate), user_cmd, brute_cmd, args.timeout, args.strict, args.eps)

    if not predicate(arr):
        print("原始输入不再复现失败，停止缩小。")
        return 1

    original_len = len(arr)
    arr = shrink_length(arr, predicate)
    arr = shrink_values(arr, predicate)
    shrunk = format_array_input(arr)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(shrunk, encoding="utf-8")
    report_path.write_text(
        "\n".join(
            [
                "# 失败样例缩小记录",
                "",
                f"- 原始长度：{original_len}",
                f"- 缩小后长度：{len(arr)}",
                f"- 输入：`{input_path}`",
                f"- 输出：`{output_path}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(f"shrunk: {input_path} -> {output_path}")
    print(f"length: {original_len} -> {len(arr)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Check problem samples and local data against a solution.

Examples:
  check_sample.py
  check_sample.py problems/luogu/1001
  check_sample.py problems/luogu/1001 --source main.cpp
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile
import time


REPO_ROOT = Path(__file__).resolve().parents[2]


class SampleCase:
    def __init__(self, name: str, input_path: Path, answer_path: Path | None) -> None:
        self.name = name
        self.input_path = input_path
        self.answer_path = answer_path


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def shell_join(cmd: list[str]) -> str:
    return " ".join(shlex.quote(item) for item in cmd)


def compile_cpp(src: Path) -> Path:
    build_dir = Path(tempfile.gettempdir()) / "problem-analysis-sample"
    build_dir.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(str(src.resolve()).encode()).hexdigest()[:12]
    out = build_dir / f"{src.stem}-{digest}"
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return out
    cmd = ["g++", "-std=c++17", "-O2", str(src), "-o", str(out)]
    print("编译：", shell_join(cmd))
    subprocess.run(cmd, check=True)
    return out


def command_for(source: Path) -> list[str]:
    if not source.exists():
        raise FileNotFoundError(source)
    if source.suffix == ".cpp":
        return [str(compile_cpp(source))]
    if source.suffix == ".py":
        return [sys.executable, str(source)]
    if os.access(source, os.X_OK):
        return [str(source)]
    raise ValueError(f"不支持的源文件或不可执行文件：{source}")


def resolve_source(problem_dir: Path, source_arg: str | None) -> Path:
    if source_arg:
        source = Path(source_arg)
        return source if source.is_absolute() else problem_dir / source

    for name in ["main.cpp", "1.cpp"]:
        candidate = problem_dir / name
        if candidate.exists():
            return candidate

    raise FileNotFoundError("未找到 main.cpp 或 1.cpp，请用 --source 指定。")


def natural_key(path: Path) -> tuple[int, str]:
    match = re.fullmatch(r"in(\d*)", path.name)
    if not match:
        return (10**9, path.name)
    suffix = match.group(1)
    return (int(suffix) if suffix else 0, path.name)


def answer_for_root_input(input_path: Path) -> Path | None:
    match = re.fullmatch(r"in(\d*)", input_path.name)
    if not match:
        return None
    suffix = match.group(1)
    answer = input_path.with_name(f"out{suffix}")
    return answer if answer.exists() else None


def answer_for_data_input(input_path: Path) -> Path | None:
    for ext in [".out", ".ans"]:
        answer = input_path.with_suffix(ext)
        if answer.exists():
            return answer
    return None


def discover_cases(problem_dir: Path) -> list[SampleCase]:
    cases: list[SampleCase] = []
    seen: set[Path] = set()

    root_inputs = sorted(
        [p for p in problem_dir.iterdir() if p.is_file() and re.fullmatch(r"in(\d*)", p.name)],
        key=natural_key,
    )
    for input_path in root_inputs:
        seen.add(input_path.resolve())
        cases.append(SampleCase(input_path.name, input_path, answer_for_root_input(input_path)))

    data_dir = problem_dir / "data"
    if data_dir.is_dir():
        for input_path in sorted(data_dir.glob("*.in")):
            if input_path.resolve() in seen:
                continue
            cases.append(
                SampleCase(
                    f"data/{input_path.name}",
                    input_path,
                    answer_for_data_input(input_path),
                )
            )

    return cases


def normalize_output(data: str) -> str:
    lines = [line.rstrip() for line in data.replace("\r\n", "\n").splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def print_diff(expected: str, actual: str) -> None:
    diff = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile="expected",
        tofile="actual",
    )
    print("".join(diff), end="")


def run_case(cmd: list[str], case: SampleCase, timeout: float) -> tuple[str, float, str, str]:
    input_data = case.input_path.read_text(encoding="utf-8")
    start = time.time()
    result = subprocess.run(
        cmd,
        input=input_data,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    elapsed = time.time() - start
    if result.returncode != 0:
        return ("RUNTIME_ERROR", elapsed, result.stdout, result.stderr)

    if case.answer_path is None:
        return ("NO_ANSWER", elapsed, result.stdout, result.stderr)

    expected = normalize_output(case.answer_path.read_text(encoding="utf-8"))
    actual = normalize_output(result.stdout)
    if expected == actual:
        return ("PASS", elapsed, result.stdout, result.stderr)
    return ("FAIL", elapsed, result.stdout, expected)


def run_samples(problem_dir: Path, source_arg: str | None, timeout: float) -> int:
    if not problem_dir.exists() or not problem_dir.is_dir():
        print(f"题目目录不存在：{rel(problem_dir)}", file=sys.stderr)
        return 2

    try:
        source = resolve_source(problem_dir, source_arg)
        cmd = command_for(source)
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"准备失败：{exc}", file=sys.stderr)
        return 2

    cases = discover_cases(problem_dir)
    if not cases:
        print(f"未找到样例数据：{rel(problem_dir)}", file=sys.stderr)
        print("支持：in/out, in1/out1, data/*.in + .out/.ans", file=sys.stderr)
        return 2

    print(f"题目目录：{rel(problem_dir)}")
    print(f"测试程序：{rel(source)}")
    print(f"运行命令：{shell_join(cmd)}")
    print(f"样例数量：{len(cases)}")
    print("-" * 60)

    passed = 0
    failed = 0
    no_answer = 0

    for idx, case in enumerate(cases, 1):
        answer_text = rel(case.answer_path) if case.answer_path else "无答案"
        print(f"[{idx}/{len(cases)}] {case.name}")
        print(f"  input : {rel(case.input_path)}")
        print(f"  answer: {answer_text}")

        try:
            status, elapsed, stdout, extra = run_case(cmd, case, timeout)
        except subprocess.TimeoutExpired:
            failed += 1
            print(f"  result: TIMEOUT > {timeout:.3f}s")
            continue

        if status == "PASS":
            passed += 1
            print(f"  result: PASS ({elapsed:.3f}s)")
        elif status == "NO_ANSWER":
            no_answer += 1
            print(f"  result: NO_ANSWER ({elapsed:.3f}s)")
            if stdout:
                print("  output:")
                print(stdout.rstrip())
        elif status == "RUNTIME_ERROR":
            failed += 1
            print(f"  result: RUNTIME_ERROR ({elapsed:.3f}s)")
            if extra:
                print("  stderr:")
                print(extra.rstrip())
        else:
            failed += 1
            print(f"  result: FAIL ({elapsed:.3f}s)")
            print("  diff:")
            print_diff(extra, normalize_output(stdout))

    print("-" * 60)
    print(f"总结：PASS={passed}, FAIL={failed}, NO_ANSWER={no_answer}")
    return 1 if failed else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check samples for one OJ problem directory")
    parser.add_argument("problem_dir", nargs="?", type=Path, default=Path.cwd())
    parser.add_argument("--source", default=None, help="source file relative to problem_dir")
    parser.add_argument("--timeout", type=float, default=2.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return run_samples(args.problem_dir.resolve(), args.source, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())

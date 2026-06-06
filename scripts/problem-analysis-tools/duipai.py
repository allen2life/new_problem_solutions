#!/usr/bin/env python3
"""Non-interactive stress testing script.

The generator is run with no input. Its stdout becomes the test input for both
the user solution and the brute solution. On the first mismatch, this script
saves the failing case and exits with a non-zero status.
"""

from __future__ import annotations

import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile


REPO_ROOT = Path(__file__).resolve().parents[2]


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def shell_join(cmd: list[str]) -> str:
    return " ".join(shlex.quote(x) for x in cmd)


def compile_cpp(src: Path, build_dir: Path) -> Path:
    digest = hashlib.sha1(str(src.resolve()).encode()).hexdigest()[:12]
    out = build_dir / f"{src.stem}-{digest}"
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return out
    cmd = ["g++", "-std=c++17", "-O2", str(src), "-o", str(out)]
    subprocess.run(cmd, check=True)
    return out


def command_for(path: Path, build_dir: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.suffix == ".cpp":
        return [str(compile_cpp(path, build_dir))]
    if path.suffix == ".py":
        return [sys.executable, str(path)]
    if os.access(path, os.X_OK):
        return [str(path)]
    raise ValueError(f"Unsupported or non-executable file: {path}")


def run_cmd(cmd: list[str], input_data: str | None, timeout: float) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        input=input_data,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )


def normalize_output(data: str, strict: bool) -> str:
    if strict:
        return data
    lines = [line.rstrip() for line in data.splitlines()]
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def infer_problem_dir(user_path: Path) -> Path:
    return user_path.resolve().parent


def default_report_path(problem_dir: Path) -> Path:
    return problem_dir / "problem-analysis-workspace" / "duipai-report.md"


def default_failed_dir(problem_dir: Path) -> Path:
    return problem_dir / "duipai-failed"


def write_report(
    report_path: Path,
    command_line: str,
    count: int,
    result: str,
    failed_dir: Path | None,
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    failed_text = rel(failed_dir) if failed_dir else "无"
    report_path.write_text(
        "\n".join(
            [
                "# 对拍记录",
                "",
                f"- 运行命令：`{command_line}`",
                f"- 测试次数：{count}",
                f"- 结果：{result}",
                f"- 失败样例位置：{failed_text}",
                f"- 时间：{now}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def save_failure(
    failed_dir: Path,
    input_data: str,
    user_out: str,
    brute_out: str,
    user_err: str,
    brute_err: str,
    meta: dict,
) -> None:
    failed_dir.mkdir(parents=True, exist_ok=True)
    (failed_dir / "input.txt").write_text(input_data, encoding="utf-8")
    (failed_dir / "user.out").write_text(user_out, encoding="utf-8")
    (failed_dir / "brute.out").write_text(brute_out, encoding="utf-8")
    (failed_dir / "user.err").write_text(user_err, encoding="utf-8")
    (failed_dir / "brute.err").write_text(brute_err, encoding="utf-8")
    diff = difflib.unified_diff(
        brute_out.splitlines(keepends=True),
        user_out.splitlines(keepends=True),
        fromfile="brute.out",
        tofile="user.out",
    )
    (failed_dir / "diff.txt").write_text("".join(diff), encoding="utf-8")
    (failed_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Non-interactive OJ stress tester")
    parser.add_argument("--gen", required=True, help="generator source/script/executable")
    parser.add_argument("--user", required=True, help="user solution, usually main.cpp")
    parser.add_argument("--brute", required=True, help="brute force trusted solution")
    parser.add_argument("-n", "--count", type=int, default=200)
    parser.add_argument("--timeout", type=float, default=2.0, help="timeout per program run")
    parser.add_argument("--report", default="", help="duipai report markdown path")
    parser.add_argument("--failed-dir", default="", help="directory for first failing case")
    parser.add_argument("--strict", action="store_true", help="compare output byte-for-byte")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.count <= 0:
        raise ValueError("--count must be positive")

    gen_path = Path(args.gen)
    user_path = Path(args.user)
    brute_path = Path(args.brute)
    problem_dir = infer_problem_dir(user_path)
    report_path = Path(args.report) if args.report else default_report_path(problem_dir)
    failed_dir = Path(args.failed_dir) if args.failed_dir else default_failed_dir(problem_dir)
    command_line = shell_join([sys.executable, rel(Path(__file__)), *sys.argv[1:]])

    build_dir = Path(tempfile.gettempdir()) / "problem-analysis-duipai"
    build_dir.mkdir(parents=True, exist_ok=True)

    try:
        gen_cmd = command_for(gen_path, build_dir)
        user_cmd = command_for(user_path, build_dir)
        brute_cmd = command_for(brute_path, build_dir)
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError) as exc:
        write_report(report_path, command_line, 0, f"失败：{exc}", None)
        print(f"duipai setup failed: {exc}", file=sys.stderr)
        return 2

    for case_id in range(1, args.count + 1):
        try:
            gen = run_cmd(gen_cmd, None, args.timeout)
            if gen.returncode != 0:
                raise RuntimeError(f"generator exited with {gen.returncode}: {gen.stderr}")

            user = run_cmd(user_cmd, gen.stdout, args.timeout)
            brute = run_cmd(brute_cmd, gen.stdout, args.timeout)
        except (subprocess.TimeoutExpired, RuntimeError) as exc:
            meta = {
                "case": case_id,
                "error": str(exc),
                "gen": gen_cmd,
                "user": user_cmd,
                "brute": brute_cmd,
            }
            save_failure(failed_dir, locals().get("gen", None).stdout if "gen" in locals() else "", "", "", "", "", meta)
            write_report(report_path, command_line, case_id, "失败", failed_dir)
            print(f"Failed on case {case_id}: {exc}")
            print(f"Saved failure to {failed_dir}")
            return 1

        user_norm = normalize_output(user.stdout, args.strict)
        brute_norm = normalize_output(brute.stdout, args.strict)

        if user.returncode != 0 or brute.returncode != 0 or user_norm != brute_norm:
            meta = {
                "case": case_id,
                "user_returncode": user.returncode,
                "brute_returncode": brute.returncode,
                "gen": gen_cmd,
                "user": user_cmd,
                "brute": brute_cmd,
            }
            save_failure(
                failed_dir,
                gen.stdout,
                user.stdout,
                brute.stdout,
                user.stderr,
                brute.stderr,
                meta,
            )
            write_report(report_path, command_line, case_id, "失败", failed_dir)
            print(f"Wrong answer on case {case_id}")
            print(f"Saved failure to {failed_dir}")
            return 1

        if case_id % 100 == 0:
            print(f"Passed {case_id} tests")

    write_report(report_path, command_line, args.count, "通过", None)
    print(f"Passed {args.count} tests")
    print(f"Report written to {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

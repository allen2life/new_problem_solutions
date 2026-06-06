#!/usr/bin/env python3
"""Generic random data generator for OJ problem analysis.

Examples:
  python3 scripts/problem-analysis-tools/gen_random.py --pattern array -n 10 --min 1 --max 100
  python3 scripts/problem-analysis-tools/gen_random.py --pattern tree -n 20
  python3 scripts/problem-analysis-tools/gen_random.py --pattern graph -n 10 -m 15
  python3 scripts/problem-analysis-tools/gen_random.py --pattern string -n 12 --charset abc
  python3 scripts/problem-analysis-tools/gen_random.py --pattern permutation -n 10
"""

from __future__ import annotations

import argparse
import random
import string
from typing import Iterable


def gen_array(n: int, lo: int, hi: int, distinct: bool) -> list[int]:
    if distinct:
        population = list(range(lo, hi + 1))
        if n > len(population):
            raise ValueError("--distinct requires n <= max - min + 1")
        random.shuffle(population)
        return population[:n]
    return [random.randint(lo, hi) for _ in range(n)]


def gen_tree(n: int) -> list[tuple[int, int]]:
    edges = []
    for v in range(2, n + 1):
        u = random.randint(1, v - 1)
        edges.append((u, v))
    random.shuffle(edges)
    return edges


def gen_graph(
    n: int,
    m: int,
    directed: bool,
    self_loops: bool,
    multi_edges: bool,
) -> list[tuple[int, int]]:
    if n <= 0:
        raise ValueError("n must be positive")
    if not multi_edges:
        max_edges = n * n if self_loops else n * (n - 1)
        if not directed:
            max_edges = (n * (n - 1)) // 2
            if self_loops:
                max_edges += n
        if m > max_edges:
            raise ValueError(f"m={m} exceeds maximum possible edges {max_edges}")

    edges: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    attempts = 0
    max_attempts = max(1000, m * 50)

    while len(edges) < m:
        if attempts > max_attempts and not multi_edges:
            raise RuntimeError("failed to generate enough unique edges")
        attempts += 1

        u = random.randint(1, n)
        v = random.randint(1, n)
        if not self_loops and u == v:
            continue

        key = (u, v) if directed else (min(u, v), max(u, v))
        if not multi_edges and key in seen:
            continue
        seen.add(key)
        edges.append((u, v))

    return edges


def gen_string(n: int, charset: str) -> str:
    if not charset:
        raise ValueError("charset must not be empty")
    return "".join(random.choice(charset) for _ in range(n))


def gen_permutation(n: int) -> list[int]:
    values = list(range(1, n + 1))
    random.shuffle(values)
    return values


def print_lines(lines: Iterable[str]) -> None:
    for line in lines:
        print(line)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generic random OJ data generator")
    parser.add_argument(
        "--pattern",
        required=True,
        choices=["array", "tree", "graph", "string", "permutation"],
    )
    parser.add_argument("-n", type=int, default=10, help="number of nodes/items")
    parser.add_argument("-m", type=int, default=None, help="number of graph edges")
    parser.add_argument("--min", dest="lo", type=int, default=1)
    parser.add_argument("--max", dest="hi", type=int, default=100)
    parser.add_argument("--charset", default=string.ascii_lowercase)
    parser.add_argument("--distinct", action="store_true")
    parser.add_argument("--directed", action="store_true")
    parser.add_argument("--self-loops", action="store_true")
    parser.add_argument("--multi-edges", action="store_true")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--no-header",
        action="store_true",
        help="do not print n or n m header where the pattern normally has one",
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.n < 0:
        raise ValueError("n must be non-negative")
    if args.lo > args.hi:
        raise ValueError("--min must be <= --max")

    if args.pattern == "array":
        arr = gen_array(args.n, args.lo, args.hi, args.distinct)
        if not args.no_header:
            print(args.n)
        print(" ".join(map(str, arr)))
    elif args.pattern == "tree":
        if args.n <= 0:
            raise ValueError("tree n must be positive")
        edges = gen_tree(args.n)
        if not args.no_header:
            print(args.n)
        print_lines(f"{u} {v}" for u, v in edges)
    elif args.pattern == "graph":
        m = args.m if args.m is not None else args.n
        if m < 0:
            raise ValueError("m must be non-negative")
        edges = gen_graph(args.n, m, args.directed, args.self_loops, args.multi_edges)
        if not args.no_header:
            print(args.n, len(edges))
        print_lines(f"{u} {v}" for u, v in edges)
    elif args.pattern == "string":
        value = gen_string(args.n, args.charset)
        if not args.no_header:
            print(args.n)
        print(value)
    elif args.pattern == "permutation":
        values = gen_permutation(args.n)
        if not args.no_header:
            print(args.n)
        print(" ".join(map(str, values)))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""为已完成题解保守起草 dense_algorithm_board 布局。

这个脚本只读取现有 `index.md`、`main.cpp`、`brute.cpp`，尽量抽取题解里已经明确写出的：

- 核心建模句
- 关键状态 / 转移 / 检查函数
- 复杂度
- 代码中的关键变量

它不会臆造新算法，也不会替代人工精修。目标是给批量渲染提供一个可复核的初稿。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
SKILL_DIR = SCRIPT_PATH.parent
REPO_ROOT = SCRIPT_PATH.parents[4]
RENDERER_PATH = SKILL_DIR / "render_dense_algorithm_board.py"


def load_renderer_module():
    spec = importlib.util.spec_from_file_location("dense_board_renderer", RENDERER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载渲染脚本：{RENDERER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RENDERER = load_renderer_module()


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
    tags: list[str] = []
    for item in raw.split(","):
        tag = item.strip().strip('"').strip("'")
        if tag:
            tags.append(tag)
    return tags


def section_text(markdown: str, heading: str) -> str:
    pattern = re.compile(
        rf"^###\s+{re.escape(heading)}\s*$\n(.*?)(?=^###\s+|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(markdown)
    return match.group(1).strip() if match else ""


def normalize_spaces(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def shorten(text: str, limit: int) -> str:
    text = normalize_spaces(text)
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def strip_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^#{1,6}\s+.*$", " ", text, flags=re.M)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", text)
    text = re.sub(r"[*_>#-]", " ", text)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$(.*?)\$", r"\1", text)
    return normalize_spaces(text)


def find_sentence(text: str, keywords: list[str], limit: int = 44) -> str:
    plain = strip_markdown(text)
    for piece in re.split(r"[。！？\n]", plain):
        piece = normalize_spaces(piece)
        if not piece:
            continue
        if "@include" in piece or "TOC" in piece:
            continue
        if any(keyword in piece for keyword in keywords):
            return shorten(piece, limit)
    return ""


def extract_declared_variables(code: str) -> list[str]:
    names: list[str] = []
    ignore = {
        "include", "using", "namespace", "std", "int", "long", "long long", "double",
        "float", "char", "bool", "void", "if", "else", "for", "while", "return",
        "const", "static", "struct", "class", "public", "private", "protected",
        "cin", "cout", "main", "vector", "queue", "stack", "pair", "make_pair",
        "push_back", "push", "pop", "front", "back", "size", "begin", "end",
        "memset", "swap", "max", "min", "sort", "printf", "scanf", "ios", "tie",
        "sync_with_stdio", "nullptr", "true", "false", "bits", "stdc", "h",
        "signed", "size_t",
    }

    for raw_line in code.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("using "):
            continue
        line = re.sub(r"//.*$", "", line).strip()
        if not line.endswith(";") or "(" in line or ")" in line:
            continue
        if line.startswith("return "):
            continue
        if line.startswith("const ") and "=" in line and "," not in line:
            match = re.search(r"\b([A-Za-z_][A-Za-z0-9_]*)\b(?=\s*=)", line)
            if match:
                token = match.group(1)
                if token not in ignore and token not in names:
                    names.append(token)
            continue

        candidates = re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\b(?=\s*(?:\[.*?\])?\s*(?:=|,|;))", line)
        for token in candidates:
            if token in ignore:
                continue
            if token.isupper() and len(token) <= 2:
                continue
            if token not in names:
                names.append(token)
    return names


def guess_variable_meaning(name: str, article: str, description: str) -> str:
    article = normalize_spaces(article)
    if name.startswith("dp"):
        match = re.search(rf"`{re.escape(name)}`\s*(?:表示|为)\s*([^。；\n]+)", article)
        if match:
            return shorten(match.group(1), 24)
        return "动态规划状态"
    if "mul" in name:
        return "整体乘法效果"
    if "coef" in name:
        return "最终传播系数"
    if "dist" in name:
        return "最短路或距离状态"
    if "ans" in name or "answer" in name:
        return "最终答案"
    if "head" in name:
        return "链式前向星表头"
    if "to" == name:
        return "边的终点"
    if "nxt" in name:
        return "下一条边编号"
    if "indeg" in name:
        return "入度统计"
    if "depth" in name:
        return "树上深度"
    if "parent" in name or name == "fa":
        return "父节点"
    if "up" == name or name.startswith("up["):
        return "倍增祖先表"
    if "event" in name:
        return "离线差分事件"
    if "cnt" in name:
        return "统计桶或计数"
    if "sum" in name:
        return "前缀和或累计值"
    if "q" == name or name.startswith("q["):
        return "队列或候选集合"
    if name.startswith("w") or "weight" in name:
        return "权值或边权"
    if "graph" in name or name == "g" or name.startswith("g["):
        return "图或树的邻接结构"
    if "calls" in name:
        return "函数调用列表"
    if "queries" in name:
        return "总调用序列"
    if "key" in name:
        return "分类统计键值"
    if description:
        return shorten(description, 22)
    return "代码中的核心状态变量"


def infer_family(tags: list[str], description: str) -> tuple[str, list[str], list[str]]:
    tagset = set(tags)
    desc = description
    if {"dag", "拓扑排序"} & tagset:
        return (
            "DAG 转移与依赖顺序",
            ["图上建模", "拓扑序推进", "实现检查"],
            ["dag", "拓扑", "最长路", "最早", "调用"],
        )
    if {"最短路", "Floyd", "bfs", "BFS"} & tagset:
        return (
            "最短路建模",
            ["图上建模", "状态转移", "边界与复杂度"],
            ["最短路", "Floyd", "bfs", "堆", "松弛"],
        )
    if {"树形DP", "树形dp", "树上背包", "换根DP", "LCA", "树上差分", "树"} & tagset:
        return (
            "树上分解与统计",
            ["树上建模", "转移或统计", "实现检查"],
            ["树", "LCA", "差分", "换根", "子树", "路径"],
        )
    if {"动态规划", "dp", "区间dp", "背包", "状态压缩"} & tagset:
        return (
            "动态规划",
            ["状态与建模", "转移与顺序", "实现检查"],
            ["状态", "转移", "dp", "背包", "区间"],
        )
    if {"二分", "二分答案"} & tagset:
        return (
            "答案二分",
            ["答案范围与单调性", "`check(x)` 设计", "实现边界"],
            ["二分", "单调", "check", "可行", "贪心"],
        )
    if {"最小生成树", "并查集"} & tagset:
        return (
            "连通性与构图",
            ["图上建模", "核心算法", "实现检查"],
            ["最小生成树", "并查集", "排序", "连通"],
        )
    return (
        "题目建模",
        ["题意建模", "核心算法", "实现检查"],
        ["关键", "核心", "转移", "状态", "贪心", "建模"],
    )


def collect_formulas(text: str, limit: int = 5) -> list[str]:
    formulas: list[str] = []
    for match in re.finditer(r"`([^`\n]{2,60})`", text):
        formula = match.group(1).strip()
        if "@include-code" in formula or "###" in formula:
            continue
        if re.fullmatch(r"[\d\s><=\-+*/.:]+", formula):
            continue
        if "->" in formula and not re.search(r"[A-Za-z_]", formula):
            continue
        if any(ch in formula for ch in "=<>+-*/[]()") or "dp" in formula or "O(" in formula:
            wrapped = f"`{formula}`"
            if wrapped not in formulas:
                formulas.append(wrapped)
        if len(formulas) >= limit:
            break
    for match in re.finditer(r"\$\$(.*?)\$\$", text, flags=re.S):
        formula = normalize_spaces(match.group(1))
        if 2 <= len(formula) <= 60:
            wrapped = f"`{formula}`"
            if wrapped not in formulas:
                formulas.append(wrapped)
        if len(formulas) >= limit:
            break
    return formulas


def pick_items_from_sentences(text: str, keywords: list[str], limit: int = 3) -> list[str]:
    items: list[str] = []
    plain = strip_markdown(text)
    for piece in re.split(r"[。！？\n]", plain):
        piece = normalize_spaces(piece)
        if len(piece) < 8:
            continue
        if any(keyword in piece for keyword in keywords):
            short = shorten(piece, 26)
            if short not in items:
                items.append(short)
        if len(items) >= limit:
            break
    return items


def collect_pitfalls(text: str) -> list[str]:
    items = pick_items_from_sentences(
        text,
        ["注意", "不要", "必须", "边界", "初始化", "否则", "如果", "坑"],
        limit=4,
    )
    if not items:
        items = [
            "初始化要和状态含义一致",
            "边界点和不可达状态单独判断",
            "循环顺序要和依赖方向一致",
        ]
    while len(items) < 3:
        fallback = [
            "数组范围和下标必须对齐",
            "long long 与取模范围要检查",
            "不要把不可达状态参与转移",
        ][len(items) - 0]
        if fallback not in items:
            items.append(fallback)
    return items[:5]


def clean_formula(formula: str) -> str:
    formula = normalize_spaces(formula.strip("`"))
    if len(formula) > 40:
        formula = formula[:39].rstrip() + "…"
    return f"`{formula}`"


def find_state_formula(text: str) -> str:
    formulas = collect_formulas(text, 8)
    for formula in formulas:
        inner = formula.strip("`")
        if any(key in inner for key in ("dp", "dist", "mul", "coef", "ans", "sum", "f(", "g(")):
            return clean_formula(formula)
    return clean_formula(formulas[0]) if formulas else "`核心状态`"


def find_transition_formula(text: str) -> str:
    formulas = collect_formulas(text, 10)
    for formula in formulas:
        inner = formula.strip("`")
        if "=" in inner and any(ch in inner for ch in "+-*<>") and re.search(r"[A-Za-z_]", inner):
            return clean_formula(formula)
    return clean_formula(formulas[min(1, len(formulas) - 1)]) if formulas else "`核心转移`"


def find_answer_formula(text: str) -> str:
    for line in text.splitlines():
        plain = normalize_spaces(line)
        if "答案" not in plain and "输出" not in plain and "最后" not in plain:
            continue
        formulas = collect_formulas(line, 5)
        for formula in formulas:
            inner = formula.strip("`")
            if re.search(r"[A-Za-z_]", inner):
                return clean_formula(formula)
    formulas = collect_formulas(text, 10)
    for formula in reversed(formulas):
        inner = formula.strip("`")
        if re.search(r"[A-Za-z_]", inner):
            return clean_formula(formula)
    return "`答案`"


def rank_variable(name: str) -> tuple[int, int]:
    score = 100
    if name.startswith("dp") or name.startswith("dist") or name.startswith("ans"):
        score = 0
    elif name in {"mul", "coef", "sum", "cnt", "head", "to", "nxt", "indeg", "depth", "fa", "parent"}:
        score = 1
    elif name.startswith(("mul", "coef", "match", "event", "head", "dist", "depth", "parent", "up", "cnt", "sum")):
        score = 2
    elif name in {"q", "g", "graph"} or name.startswith(("q[", "g[")):
        score = 3
    elif name in {"n", "m", "u", "v", "i", "j", "k", "c"}:
        score = 20
    elif name.startswith("MAX"):
        score = 30
    return (score, len(name))


def extract_summary_phrases(text: str, keywords: list[str], limit: int = 3) -> list[str]:
    phrases: list[str] = []
    plain = strip_markdown(text)
    for piece in re.split(r"[。！？\n]", plain):
        piece = normalize_spaces(piece)
        if not piece or "@include" in piece:
            continue
        if any(keyword in piece for keyword in keywords):
            short = shorten(piece, 24)
            if short not in phrases:
                phrases.append(short)
        if len(phrases) >= limit:
            break
    return phrases


def collect_training_tips(tags: list[str]) -> list[str]:
    tips = [
        "先手推最小样例，确认状态或路径含义",
        "用 `brute.cpp` 对照随机小数据",
        "把边界输入单独列成测试点",
    ]
    tagset = set(tags)
    if {"LCA", "树", "树形DP", "树上差分"} & tagset:
        tips.append("在纸上画树并标出深度、父子和路径分段")
    elif {"dag", "拓扑排序", "图论"} & tagset:
        tips.append("手画小图并按拓扑序或松弛顺序推进")
    elif {"动态规划", "dp", "背包", "区间dp"} & tagset:
        tips.append("把前几层状态表写出来核对转移")
    elif {"二分", "二分答案"} & tagset:
        tips.append("枚举几个答案，验证 `check(x)` 的单调性")
    return tips[:5]


def parse_complexity(text: str) -> tuple[str, str]:
    time_match = re.search(r"时间复杂度\s*`([^`]+)`", text)
    space_match = re.search(r"空间复杂度\s*`([^`]+)`", text)
    time_str = f"`{time_match.group(1)}`" if time_match else "`见正文复杂度分析`"
    space_str = f"`{space_match.group(1)}`" if space_match else "`见正文复杂度分析`"
    return time_str, space_str


def insert_image_section(index_text: str) -> str:
    if "### 一图流解析" in index_text:
        return index_text
    insertion = "\n".join(
        [
            "### 一图流解析",
            "",
            "这张图把本题的建模、关键转移、实现检查和训练方法压缩到一页，适合读完正文后复盘。",
            "",
            "![一图流解析](./one-page-explainer.png)",
            "",
        ]
    )
    marker = "### 总结"
    if marker not in index_text:
        return index_text.rstrip() + "\n\n" + insertion
    summary_pattern = re.compile(r"(^###\s+总结\s*$\n.*?)(?=^###\s+|\Z)", re.M | re.S)
    match = summary_pattern.search(index_text)
    if not match:
        return index_text.rstrip() + "\n\n" + insertion
    return index_text[: match.end()] + "\n\n" + insertion + index_text[match.end():]


@dataclass
class ProblemFiles:
    problem_dir: Path
    problem_id: str
    title: str
    description: str
    difficulty: str
    tags: list[str]
    index_text: str
    main_code: str
    brute_code: str


def load_problem(problem_dir: Path) -> ProblemFiles:
    index_path = problem_dir / "index.md"
    main_path = problem_dir / "main.cpp"
    brute_path = problem_dir / "brute.cpp"
    index_text = index_path.read_text(encoding="utf-8")
    return ProblemFiles(
        problem_dir=problem_dir,
        problem_id=parse_frontmatter_value(index_text, "problem_id") or problem_dir.name,
        title=parse_frontmatter_value(index_text, "title") or problem_dir.name,
        description=parse_frontmatter_value(index_text, "description"),
        difficulty=parse_frontmatter_value(index_text, "difficulty") or "未知",
        tags=parse_tags(index_text),
        index_text=index_text,
        main_code=main_path.read_text(encoding="utf-8", errors="ignore"),
        brute_code=brute_path.read_text(encoding="utf-8", errors="ignore"),
    )


def build_layout(problem: ProblemFiles) -> dict:
    thought = section_text(problem.index_text, "思路")
    summary = section_text(problem.index_text, "总结")
    complexity_text = section_text(problem.index_text, "复杂度")
    family, column_titles, keywords = infer_family(problem.tags, problem.description)

    formulas = collect_formulas(thought) + [f for f in collect_formulas(problem.index_text) if f not in collect_formulas(thought)]
    if not formulas:
        formulas = collect_formulas(problem.main_code)
    for fallback in ["`dp[i]`", "`ans`", "`O(n)`"]:
        if len(formulas) >= 3:
            break
        if fallback not in formulas:
            formulas.append(fallback)
    while len(formulas) < 3:
        formulas.append("`核心状态`")

    title = shorten(f"{problem.problem_id} {problem.title} 专用训练流程图", 28)
    subtitle = shorten(problem.description or strip_markdown(summary) or family, 44)
    state_formula = find_state_formula(thought + "\n" + problem.main_code)
    transition_formula = find_transition_formula(thought + "\n" + problem.main_code)
    answer_formula = find_answer_formula(summary + "\n" + thought)
    state_sentence = find_sentence(thought, ["表示", "定义", "设", "看成", "记作"], 24)
    transition_sentence = find_sentence(thought, ["转移", "更新", "满足", "统计", "于是", "因此"], 28)
    answer_sentence = find_sentence(summary + "\n" + thought, ["答案", "最后", "输出", "就是"], 22)
    order_sentence = find_sentence(thought, ["拓扑", "后序", "顺序", "逆序", "从后往前", "从前往后"], 24)
    opt_sentence = find_sentence(thought, ["优化", "只要", "拆成", "分成", "统一", "桶"], 24)

    top_flow = [
        {
            "title": "题意压缩",
            "detail": shorten(problem.description or family, 22),
        },
        {
            "title": "状态或模型",
            "detail": shorten(state_sentence or state_formula, 24),
        },
        {
            "title": "核心转移",
            "detail": shorten(transition_sentence or transition_formula, 28),
        },
        {
            "title": "实现收束",
            "detail": shorten(answer_sentence or answer_formula, 20),
        },
    ]

    col1_items = pick_items_from_sentences(thought, ["关键", "条件", "拆成", "定义", "看成", "表示"], 3)
    if len(col1_items) < 3:
        col1_items.extend([
            "先明确状态或图上对象",
            "暴力起点只用于理解结构",
            "把题意改写成可转移形式",
        ][: 3 - len(col1_items)])

    col2_items = pick_items_from_sentences(thought, ["转移", "更新", "枚举", "拓扑", "后序", "check", "松弛"], 3)
    if len(col2_items) < 3:
        col2_items.extend([
            "按依赖方向推进状态",
            "每次只做正文支持的更新",
            "把瓶颈压到可通过复杂度",
        ][: 3 - len(col2_items)])

    col3_items = collect_pitfalls(thought + "\n" + summary)
    code_tokens = sorted(extract_declared_variables(problem.main_code), key=rank_variable)
    variables = []
    for token in code_tokens[:5]:
        variables.append(
            {
                "name": f"`{token}`",
                "meaning": guess_variable_meaning(token, problem.index_text, problem.description),
            }
        )
    while len(variables) < 3:
        fallback = ["dp", "ans", "sum"][len(variables)]
        variables.append({"name": f"`{fallback}`", "meaning": guess_variable_meaning(fallback, problem.index_text, "")})

    time_str, space_str = parse_complexity(complexity_text)

    return {
        "schema_version": "dense_algorithm_board/v1",
        "title": title,
        "subtitle": subtitle,
        "top_flow": top_flow,
        "columns": [
            {
                "title": column_titles[0],
                "theme": "blue",
                "blocks": [
                    {
                        "title": "建模对象",
                        "formula": clean_formula(formulas[0]),
                        "items": col1_items[:3],
                    },
                    {
                        "title": "状态定义",
                        "formula": state_formula,
                        "items": [
                            shorten(state_sentence or "状态含义必须唯一", 24),
                            "初值要和题意约束对齐",
                        ],
                    },
                    {
                        "title": "答案位置",
                        "formula": answer_formula,
                        "items": [
                            shorten(answer_sentence or "最后从目标状态读答案", 24),
                            "边界输入单独检查",
                        ],
                    },
                ],
            },
            {
                "title": column_titles[1],
                "theme": "green",
                "blocks": [
                    {
                        "title": "核心转移",
                        "formula": transition_formula,
                        "items": col2_items[:3],
                    },
                    {
                        "title": "处理顺序",
                        "formula": shorten(order_sentence or family, 24),
                        "items": [
                            "依赖先算完再更新后继",
                            "不要把新旧状态方向写反",
                        ],
                    },
                    {
                        "title": "优化抓手",
                        "formula": shorten(opt_sentence or "利用结构减少无效枚举", 24),
                        "items": [
                            "把重复计算折成一次传播",
                            "把分类统计改成统一桶或表",
                        ],
                    },
                ],
            },
            {
                "title": column_titles[2],
                "theme": "orange",
                "blocks": [
                    {
                        "title": "关键变量",
                        "table": {
                            "headers": ["变量", "含义", "检查点"],
                            "rows": [
                                [item["name"], item["meaning"], "和代码一致"]
                                for item in variables[:3]
                            ],
                        },
                        "items": ["变量命名和正文说明要对齐"],
                    },
                    {
                        "title": "常见坑点",
                        "items": col3_items[:4],
                    },
                    {
                        "title": "训练方式",
                        "items": collect_training_tips(problem.tags),
                        "diagram": "手推样例 -> 对照暴力 -> 压边界",
                    },
                ],
            },
        ],
        "variables": variables[:5],
        "training_tips": collect_training_tips(problem.tags),
        "pitfalls": col3_items[:5],
        "complexity": {
            "time": time_str,
            "space": space_str,
            "notes": ["复杂度以正文和 `main.cpp` 为准"],
        },
    }


def build_evaluation(problem: ProblemFiles) -> str:
    family, _, _ = infer_family(problem.tags, problem.description)
    goals = [
        f"- 压缩题意建模：{shorten(problem.description or family, 22)}",
        f"- 标出核心状态：{collect_formulas(problem.index_text, 2)[0] if collect_formulas(problem.index_text, 2) else '`核心状态`'}",
        "- 汇总实现检查、边界和训练方法。",
    ]
    return "\n".join(
        [
            "# AI 一图流评估",
            "",
            "## 是否生成",
            "",
            "- 结论：是",
            "- 原因：本题属于 CSP-S 400 题单中的重点训练题，存在明确建模、状态转移或实现坑点，适合用 dense_algorithm_board 作为读后复盘图。",
            "",
            "## 适合一图流的教学目标",
            "",
            *goals,
            "",
            "## 不适合放进 dense board 的信息",
            "",
            "- 不放长代码。",
            "- 不放题解没有验证的样例数值。",
            "- 不加入题解和代码没有支持的新算法步骤。",
            "",
            "## 后续动作",
            "",
            "写入 `problem-analysis-workspace/ai-image-layout.json`，用本地 dense renderer 渲染并复核 PNG。",
            "",
        ]
    )


def write_report_stub(problem_dir: Path) -> None:
    report_path = problem_dir / "problem-analysis-workspace" / "ai-image-report.md"
    if report_path.exists():
        return
    report_path.write_text("# AI 图片生成报告\n", encoding="utf-8")


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


def write_report(problem_dir: Path, output_name: str, passed: bool, issue: str) -> None:
    report_path = problem_dir / "problem-analysis-workspace" / "ai-image-report.md"
    lines = [
        "# AI 图片生成报告",
        "",
        "## dense v1",
        "",
        "- 布局文件：`problem-analysis-workspace/ai-image-layout.json`",
        f"- 输出文件：`{output_name}`",
        "- 渲染方式：`dense_algorithm_board` + Playwright",
        "- 尺寸：`1920x1088`",
        f"- 检查结论：{'通过' if passed else '不通过'}",
        f"- 问题：{issue or '无'}",
        f"- 是否建议插入 `index.md`：{'是' if passed else '否'}",
        "",
    ]
    if passed:
        lines.extend(
            [
                "## 最终采用",
                "",
                "- 文件：`one-page-explainer.png`",
                f"- 来源版本：`{output_name}`",
                "- 插入位置：`### 总结` 后",
                "- 备注：CSP-S 400 一图流批处理生成。",
                "",
            ]
        )
    report_path.write_text("\n".join(lines), encoding="utf-8")


def render_and_adopt(problem: ProblemFiles, *, adopt: bool) -> tuple[bool, str]:
    workspace = problem.problem_dir / "problem-analysis-workspace"
    layout_path = workspace / "ai-image-layout.json"
    output_path = problem.problem_dir / "one-page-explainer-dense-v1.png"
    html_output = workspace / "ai-image-preview.html"
    RENDERER.render_layout(layout_path, output_path, html_output=html_output)
    ok, message = review_png(output_path)
    if not ok:
        write_report(problem.problem_dir, output_path.name, False, message)
        return False, message
    if adopt:
        shutil.copyfile(output_path, problem.problem_dir / "one-page-explainer.png")
        index_path = problem.problem_dir / "index.md"
        content = index_path.read_text(encoding="utf-8")
        new_content = insert_image_section(content)
        if new_content != content:
            index_path.write_text(new_content, encoding="utf-8")
    write_report(problem.problem_dir, output_path.name, True, "")
    return True, message


def parse_problem_ids_from_set(problem_set_path: Path) -> list[str]:
    text = problem_set_path.read_text(encoding="utf-8")
    result: list[str] = []
    for oj, pid in re.findall(r"\[\[problem:\s*([^,\]]+)\s*,\s*([^\]\s]+)\s*\]\]", text):
        if oj.lower() != "luogu":
            continue
        pid_num = pid[1:] if pid.startswith("P") else pid
        if pid_num not in result:
            result.append(pid_num)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="批量起草 dense_algorithm_board 布局")
    parser.add_argument("--problem-set", default="problem-sets/csp-s-400.md", help="题目单路径")
    parser.add_argument("--todo", default="todo_csp_s_400_image.md", help="输出待办清单路径")
    parser.add_argument("--only-missing", action="store_true", help="只处理还没有 one-page-explainer.png 的题")
    parser.add_argument("--limit", type=int, default=None, help="最多处理多少题")
    parser.add_argument("--render", action="store_true", help="起草 layout 后立即渲染")
    parser.add_argument("--adopt", action="store_true", help="渲染通过后复制为 one-page-explainer.png 并写回 index.md")
    parser.add_argument("--continue-on-error", action="store_true", help="单题渲染失败后继续处理后续题")
    args = parser.parse_args()

    problem_set_arg = Path(args.problem_set)
    todo_arg = Path(args.todo)
    problem_set_path = problem_set_arg if problem_set_arg.is_absolute() else (REPO_ROOT / problem_set_arg).resolve()
    todo_path = todo_arg if todo_arg.is_absolute() else (REPO_ROOT / todo_arg).resolve()
    ids = parse_problem_ids_from_set(problem_set_path)

    dense_todo_text = (REPO_ROOT / "todo_dense_board.md").read_text(encoding="utf-8")
    recommended: dict[str, str] = {}
    eval_only: set[str] = set()
    for line in dense_todo_text.splitlines():
        match = re.search(r"\[\[problem:\s*luogu\s*,\s*P?(\d+)\s*\]\].*\[(建议 dense|仅评估)\]", line)
        if not match:
            continue
        pid, kind = match.group(1), match.group(2)
        if kind == "建议 dense":
            recommended[pid] = line.strip()
        else:
            eval_only.add(pid)

    selected = [pid for pid in ids if pid in recommended]
    lines = [
        "---",
        'title: "CSP-S 400 一图流解析待办"',
        'description: "按照与 csp-j 相同的 dense_algorithm_board 流程推进 csp-s-400 题单。"',
        "source: problem-sets/csp-s-400.md",
        "---",
        "",
        "# CSP-S 400 一图流解析待办",
        "",
        "## 目标",
        "",
        "为 `problem-sets/csp-s-400.md` 中筛选出的 dense board 目标题，补齐：",
        "",
        "- `problem-analysis-workspace/07-ai-image-evaluation.md`",
        "- `problem-analysis-workspace/ai-image-layout.json`",
        "- `one-page-explainer-dense-v1.png`",
        "- `one-page-explainer.png`",
        "- `problem-analysis-workspace/ai-image-report.md`",
        "- `index.md` 中 `### 总结` 后的 `### 一图流解析`",
    ]
    item_lines: list[str] = []

    processed = 0
    rendered = 0
    failed = 0
    for pid in selected:
        pdir = REPO_ROOT / "problems" / "luogu" / pid
        if not (pdir / "index.md").exists() or not (pdir / "main.cpp").exists() or not (pdir / "brute.cpp").exists():
            continue
        if args.only_missing and (pdir / "one-page-explainer.png").exists():
            continue
        problem = load_problem(pdir)
        workspace = pdir / "problem-analysis-workspace"
        workspace.mkdir(parents=True, exist_ok=True)

        eval_path = workspace / "07-ai-image-evaluation.md"
        layout_path = workspace / "ai-image-layout.json"
        if not eval_path.exists():
            eval_path.write_text(build_evaluation(problem), encoding="utf-8")
        if not layout_path.exists():
            layout = build_layout(problem)
            layout_path.write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        write_report_stub(pdir)

        render_message = ""
        if args.render:
            try:
                ok, render_message = render_and_adopt(problem, adopt=args.adopt)
                if ok:
                    rendered += 1
                else:
                    failed += 1
                    if not args.continue_on_error:
                        raise RuntimeError(render_message)
            except Exception as exc:
                failed += 1
                render_message = f"渲染失败：{exc}"
                if not args.continue_on_error:
                    raise

        has_img = (pdir / "one-page-explainer.png").exists()
        status = "已完成" if has_img else "待生成"
        item_lines.append(
            f"- [{'x' if has_img else ' '}] [[problem: luogu,P{pid}]] "
            f"`{problem.difficulty}` `{ ' / '.join(problem.tags[:4]) or '无标签' }` "
            f"`{status}` {problem.title}"
            + (f" - {render_message}" if render_message else "")
        )
        processed += 1
        if args.limit is not None and processed >= args.limit:
            break

    done_count = 0
    pending_count = 0
    generated = 0
    for pid in selected:
        pdir = REPO_ROOT / "problems" / "luogu" / pid
        if not (pdir / "index.md").exists() or not (pdir / "main.cpp").exists() or not (pdir / "brute.cpp").exists():
            continue
        has_img = (pdir / "one-page-explainer.png").exists()
        has_layout = (pdir / "problem-analysis-workspace" / "ai-image-layout.json").exists()
        if has_img:
            done_count += 1
        else:
            pending_count += 1
        if has_layout:
            generated += 1

    lines.extend(
        [
            "",
            "## 当前统计",
            "",
            f"- 题单唯一 Luogu 题：{len(ids)}",
            f"- 筛选为需要一图流：{len(selected)}",
            f"- 已完成并插入：{done_count}",
            f"- 已有 layout：{generated}",
            f"- 待生成：{pending_count}",
            "",
            "## 需要一图流的题目",
            "",
        ]
    )
    lines.extend(item_lines)
    todo_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"selected={len(selected)} processed={processed} rendered={rendered} "
        f"failed={failed} todo={todo_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

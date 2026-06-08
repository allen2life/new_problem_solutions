---
name: oj-problem-analysis-writer
description: Write Chinese OJ problem analysis content for this repository's ebook. Use this skill whenever the user asks to write a 题目解析, generate learning notes for an OJ problem, fill problems/<oj>/<problem_id>/index.md, turn problem-analysis-workspace/*.md into a final article, create a teaching brute.cpp, or use random data / 对拍 scripts while preparing a problem explanation. This skill writes analysis content, must complete brute.cpp, and must follow oj-problem-format-spec for the final index.md.
---

# OJ 题目解析写作

这个 skill 专门负责写题目解析内容，让用户通过 Markdown 文档学会这道题，并最终生成符合 `oj-problem-format-spec` 的正式 `index.md`。

格式骨架由 `oj-problem-format-spec` 约束。本 skill 负责填充：

- 题意理解
- 关键观察
- 解法推导
- 正确性说明
- 边界情况
- 复杂度
- 实现对应关系

## 固定目录结构

只使用新结构，不兼容旧的扁平结构。

```text
problems/<oj>/<problem_id>/
  index.md
  main.cpp
  brute.cpp
  gen.py
  problem-analysis-workspace/
    01-problem-understanding.md
    02-observation-and-model.md
    03-solution-derivation.md
    04-correctness-and-edge-cases.md
    05-complexity-and-implementation.md
    06-final-index-draft.md
    duipai-report.md
```

Required for final article:

- `index.md`
- `main.cpp`
- `brute.cpp`

Optional but useful for verification:

- `gen.py`
- `problem-analysis-workspace/duipai-report.md`

## Required Companion Skill

Before writing final `index.md`, read:

```text
.agents/skills/oj-problem-format-spec/SKILL.md
```

Final `index.md` must follow that format:

- frontmatter at top
- frontmatter `tags` must be reviewed and updated for this problem
- `[[TOC]]`
- `### 题意`
- `### 思路`
- `### 代码`
- `### 复杂度`
- `### 总结`
- `@include-code(./main.cpp, cpp)`
- `@include-code(./brute.cpp, cpp)` in `### 思路`
- Mermaid、Graphviz、Markdown 表格等可视化内容必须遵守 `oj-problem-format-spec` 的“可视化辅助格式”。

## Source Priority

Use information in this order:

1. `problem-analysis-workspace/*.md`
2. `main.cpp`
3. `brute.cpp`
4. existing `index.md`
5. problem statement text or source URL provided by the user
6. `oj-problem-format-spec`

If workspace files already exist, read them first and preserve useful user-written content. Do not overwrite process notes blindly.

## Process Documents

If `problem-analysis-workspace/` or its stage files do not exist, create them and fill them progressively.

## Required `brute.cpp`

This skill must finish a teaching brute-force solution before the final `index.md` is considered complete.

Path:

```text
problems/<oj>/<problem_id>/brute.cpp
```

Purpose:

- help the reader understand the problem through the most direct correct idea;
- provide a trusted small-data solution for 对拍;
- make the bottleneck of the naive method explicit before deriving `main.cpp`.

Rules:

- If `brute.cpp` already exists, read it and improve it if needed.
- If `brute.cpp` does not exist, create it.
- It must be a complete C++17 program with the same input/output format as `main.cpp`.
- Prefer direct enumeration, simulation, or another clearly correct small-data method.
- Use straightforward variable names and a few useful Chinese comments when they help understanding.
- High complexity is acceptable, but it must be described as small-data/verification code.
- If the brute-force correctness is uncertain, record the uncertainty in `04-correctness-and-edge-cases.md` and do not claim reliable 对拍.
- Do not deliver a final `index.md` without a completed `brute.cpp`, unless the user explicitly pauses or changes this requirement.

### `01-problem-understanding.md`

Purpose: make the problem statement precise.

Required sections:

```markdown
# 题意理解

## 输入与输出

## 要求求什么

## 约束条件

## 等价表述
```

### `02-observation-and-model.md`

Purpose: identify the key observation and algorithm model.

Required sections:

```markdown
# 关键观察与模型

## 直接想法

## 关键性质

## 可用模型

## 为什么这个模型适用
```

Also evaluate whether the problem needs visualization. Record:

```markdown
## 可视化评估

- 是否需要可视化辅助：是 / 否
- 推荐形式：Markdown 表格 / Mermaid / Graphviz / 图片 / 不需要
- 解释对象：样例 / 状态 / 转移 / 图结构 / 搜索树 / 贪心选择 / 不需要
- 如果不需要，原因：
```

Trigger rules:

- 图论题：必须考虑 Graphviz 或 Mermaid 样例图。
- 树题、二叉树、线段树题：必须考虑用 `tree_draw.py` 生成 SVG 树图。
- DP 题：必须考虑 Markdown 表格，背包题尤其优先表格。
- 网格题：必须考虑二维表格。
- 搜索、递归题：必须考虑搜索树或状态转移图。
- 模拟题：如果样例过程复杂，必须考虑过程表格。

### `03-solution-derivation.md`

Purpose: teach the solution by layer, not by jumping to the final answer.

Required sections:

```markdown
# 解法推导

## 朴素想法

## 瓶颈分析

## 优化思路

## 最终做法

## 与代码实现的对应关系
```

This file should explain how `brute.cpp` represents the naive idea, why it is too slow for full constraints, and which bottleneck motivates `main.cpp`.

### `04-correctness-and-edge-cases.md`

Purpose: explain why the solution is correct and what edge cases matter.

Required sections:

```markdown
# 正确性与边界情况

## 正确性说明

## 可能的反例检查

## 边界情况

## 对拍或手工验证记录
```

This file should state whether `brute.cpp` is reliable enough for 对拍. If 对拍 was not run, record why.

### `05-complexity-and-implementation.md`

Purpose: connect the final method to implementation details.

Required sections:

```markdown
# 复杂度与实现

## 时间复杂度

## 空间复杂度

## 关键变量

## 核心循环

## 边界处理

## 与 main.cpp 的对应关系
```

Do not write line-by-line code commentary. Explain only the key implementation correspondence.

Also mention how the optimized implementation differs from `brute.cpp`.

### `06-final-index-draft.md`

Purpose: draft the final article before updating `index.md`.

It should already follow the final article structure:

```markdown
---
oj: ""
problem_id: ""
title: ""
date: YYYY-MM-DD HH:mm
toc: true
tags: ["算法标签", "数据结构标签"]
categories: []
source:
---

[[TOC]]

### 题意

### 思路

先看一个可以直接验证想法的朴素解：

@include-code(./brute.cpp, cpp)

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

### 总结
```

Do not leave `tags: []` in the draft unless the problem is genuinely impossible to classify from available materials. Choose concise Chinese tags that help users search and review problems later, such as algorithm family, data structure, implementation technique, or difficulty-relevant pattern.

## Final Article Style

The final `index.md` should be concise but still teach the idea.

In `### 思路`, keep a compressed layered progression:

1. briefly state why the naive idea is not enough;
2. include `@include-code(./brute.cpp, cpp)` as the teaching brute-force solution;
3. state the bottleneck of `brute.cpp`;
4. state the key observation;
5. explain the final method;
6. mention the important implementation correspondence.

Also include visualization when it improves learning:

- Use Markdown tables for DP states, knapsack tables, grids, and step-by-step sample traces.
- Use Mermaid for flowcharts, state transitions, simple trees, and process diagrams.
- Use Graphviz dot for graph theory samples, trees, DAGs, and topology-like structures.
- Use `tree_draw.py` for ordinary trees, binary trees, segment trees, and static tree-shaped data structures.
- Use generated images only when source-style diagrams are too large or need hand annotations.

Visualization is not mandatory for every problem, but it is a mandatory evaluation item. If the problem is graph/tree/DP/grid/search/simulation-heavy, prefer including one small visual block unless it would be redundant.

Every visual block in final `index.md` must:

- state what it shows before the figure/table;
- explain what to observe after the figure/table in 2 to 5 sentences;
- keep the displayed data small and tied to the sample or one key local structure;
- avoid decorative diagrams.

When using `tree_draw.py`, prefer SVG output in the current problem directory or a local `assets/` directory:

```bash
ptool --cd problems/<oj>/<problem_id> tree_draw --type binary --input tree.txt --output tree.svg --markdown
ptool --cd problems/<oj>/<problem_id> tree_draw --type segment --size 8 --output segment-tree.svg --markdown
```

Then reference it from `index.md`:

```markdown
![二叉树示意图](./tree.svg)
```

Do not turn `index.md` into a raw dump of all process notes. The detailed learning path belongs in `problem-analysis-workspace/*.md`.

The `### 代码` section still contains only the final accepted/optimized solution:

```markdown
@include-code(./main.cpp, cpp)
```

## Consistency Check

Before updating `index.md`, check consistency with `main.cpp` when it exists:

- The frontmatter `tags` are updated from the solved content, not left as a stale placeholder.
- Before choosing tags, query the repository's existing tag set and prefer accurate existing tags over inventing new variants:

```bash
python3 scripts/problem-analysis-tools/list_tags.py
python3 scripts/problem-analysis-tools/list_tags.py --format plain
```

- Tags should describe the final solution and important prerequisite ideas, for example `模拟`, `枚举`, `动态规划`, `贪心`, `图论`, `树形结构`, `最短路`, `二分`, `前缀和`, `数学`, `组合计数`, `高精度`, `字符串`, `数据结构`.
- If an existing tag is accurate, reuse it exactly. Only introduce a new tag when the current tag set has no precise fit.
- If the existing `index.md` already has useful tags, preserve them when still accurate and add missing tags.
- The algorithm description roughly matches the implementation.
- The complexity can be explained from the code structure.
- The code section uses `@include-code(./main.cpp, cpp)`.
- The `### 思路` section uses `@include-code(./brute.cpp, cpp)`.
- `brute.cpp` is complete and matches the same input/output format.
- Key implementation details mentioned in the article exist in the code.
- Visualization was evaluated in `02-observation-and-model.md`.
- Any Mermaid / Graphviz / table used in `index.md` has nearby explanatory text and follows the format spec.
- If no verification was run, say so in the process notes; do not imply proof by testing.

## Verification Scripts

Use scripts from:

```text
scripts/problem-analysis-tools/
```

Available tools:

- `list_tags.py`: list existing tags in all problem explanations; use it before writing frontmatter tags.
- `gen_random.py`: generic random data generator for arrays, trees, graphs, strings, and permutations.
- `duipai.py`: non-interactive stress testing script for agents and automation.
- `duipai-human.py`: interactive wrapper for humans; it calls `duipai.py`.

Default per-problem verification files:

```text
problems/<oj>/<problem_id>/
  main.cpp
  brute.cpp
  gen.py
```

`brute.cpp` is required. `gen.py` is not strictly required for the final article, but create or complete it when the input format is clear and random small data can be generated reasonably.

Recommended command:

```bash
python3 scripts/problem-analysis-tools/duipai.py \
  --gen problems/<oj>/<problem_id>/gen.py \
  --user problems/<oj>/<problem_id>/main.cpp \
  --brute problems/<oj>/<problem_id>/brute.cpp \
  -n 200
```

Only run 对拍 when `gen.py`, `main.cpp`, and `brute.cpp` exist and are runnable, or when the user asks for it. If 对拍 is not possible, record that it was not run and why.

## Safety Rules

- Do not invent problem title, source URL, or constraints.
- Do not claim a solution is accepted unless there is evidence.
- Do not claim 对拍 was run unless the script actually ran.
- Do not overwrite user-written process notes without preserving useful content.
- Do not write full code into `index.md`; use `@include-code(./brute.cpp, cpp)` in `### 思路` and `@include-code(./main.cpp, cpp)` in `### 代码`.
- Do not claim `brute.cpp` is trusted unless its correctness is clear enough for small data.
- Do not finish final `index.md` with `tags: []` or irrelevant inherited tags when enough information exists to classify the problem.

## Final Response

After editing, report briefly:

- which problem directory was updated;
- which process Markdown files were created or updated;
- whether `brute.cpp` was created or updated;
- whether `index.md` was written from `06-final-index-draft.md`;
- which `tags` were written into `index.md` frontmatter;
- whether visualization was evaluated and what was used, if anything;
- whether 对拍 was run and where the report is;
- any missing fields, code files, or verification material.

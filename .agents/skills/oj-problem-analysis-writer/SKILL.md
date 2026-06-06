---
name: oj-problem-analysis-writer
description: Write Chinese OJ problem analysis content for this repository's ebook. Use this skill whenever the user asks to write a 题目解析, generate learning notes for an OJ problem, fill problems/<oj>/<problem_id>/index.md, turn problem-analysis-workspace/*.md into a final article, or use random data / 对拍 scripts while preparing a problem explanation. This skill writes analysis content and must follow oj-problem-format-spec for the final index.md.
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

Optional but useful for verification:

- `brute.cpp`
- `gen.py`
- `problem-analysis-workspace/duipai-report.md`

## Required Companion Skill

Before writing final `index.md`, read:

```text
.agents/skills/oj-problem-format-spec/SKILL.md
```

Final `index.md` must follow that format:

- frontmatter at top
- `[[TOC]]`
- `### 题意`
- `### 思路`
- `### 代码`
- `### 复杂度`
- `### 总结`
- `@include-code(./main.cpp, cpp)`

## Source Priority

Use information in this order:

1. `problem-analysis-workspace/*.md`
2. `main.cpp`
3. existing `index.md`
4. problem statement text or source URL provided by the user
5. `oj-problem-format-spec`

If workspace files already exist, read them first and preserve useful user-written content. Do not overwrite process notes blindly.

## Process Documents

If `problem-analysis-workspace/` or its stage files do not exist, create them and fill them progressively.

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
tags: []
categories: []
source:
---

[[TOC]]

### 题意

### 思路

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

### 总结
```

## Final Article Style

The final `index.md` should be concise but still teach the idea.

In `### 思路`, keep a compressed layered progression:

1. briefly state why the naive idea is not enough;
2. state the key observation;
3. explain the final method;
4. mention the important implementation correspondence.

Do not turn `index.md` into a raw dump of all process notes. The detailed learning path belongs in `problem-analysis-workspace/*.md`.

## Consistency Check

Before updating `index.md`, check consistency with `main.cpp` when it exists:

- The algorithm description roughly matches the implementation.
- The complexity can be explained from the code structure.
- The code section uses `@include-code(./main.cpp, cpp)`.
- Key implementation details mentioned in the article exist in the code.
- If no verification was run, say so in the process notes; do not imply proof by testing.

## Verification Scripts

Use scripts from:

```text
scripts/problem-analysis-tools/
```

Available tools:

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

Recommended command:

```bash
python3 scripts/problem-analysis-tools/duipai.py \
  --gen problems/<oj>/<problem_id>/gen.py \
  --user problems/<oj>/<problem_id>/main.cpp \
  --brute problems/<oj>/<problem_id>/brute.cpp \
  -n 200
```

Only run 对拍 when `gen.py`, `main.cpp`, and `brute.cpp` exist or the user asks for it. If 对拍 is not possible, record that it was not run.

## Safety Rules

- Do not invent problem title, source URL, or constraints.
- Do not claim a solution is accepted unless there is evidence.
- Do not claim 对拍 was run unless the script actually ran.
- Do not overwrite user-written process notes without preserving useful content.
- Do not write full code into `index.md`; use `@include-code(./main.cpp, cpp)`.

## Final Response

After editing, report briefly:

- which problem directory was updated;
- which process Markdown files were created or updated;
- whether `index.md` was written from `06-final-index-draft.md`;
- whether 对拍 was run and where the report is;
- any missing fields, code files, or verification material.

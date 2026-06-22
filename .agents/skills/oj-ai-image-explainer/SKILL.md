---
name: oj-ai-image-explainer
description: Post-process completed Chinese OJ problem explanations with deterministic dense algorithm-board images. Use after index.md, main.cpp, brute.cpp, and verification notes are complete, when an OJ/NOIP/CSP/Codeforces/AtCoder/Luogu explanation needs a high-density 一图流讲义图 with exact Chinese text, variables, short formulas, pitfalls, and training tips. This skill writes ai-image-layout.json, renders a 1920x1088 PNG locally with Playwright, reviews the layout and image, and only then lets oj-problem-analysis-writer decide whether to reference it.
---

# OJ AI Image Explainer

Generate deterministic `dense_algorithm_board` images for completed OJ problem explanations.

This skill no longer creates generic overview infographics and does not call the image API in `ai_image_api.md` for the main workflow. The agent extracts a structured layout from the finished explanation, then the bundled renderer turns that layout into a local PNG. This keeps Chinese text, variables, and formulas accurate.

## Boundary

Use this skill only after the core explanation is complete:

- `index.md` already teaches the solution.
- `main.cpp` and `brute.cpp` are complete.
- Verification/correctness/complexity notes exist, or the absence is explicitly recorded.
- Exact sample, DP, graph, tree, grid, or simulation visuals have already been considered through `oj-sample-visualizer`.

This skill is responsible for:

- deciding whether a dense board is useful;
- writing `problem-analysis-workspace/07-ai-image-evaluation.md`;
- writing `problem-analysis-workspace/ai-image-layout.json`;
- rendering `one-page-explainer-v*.png` with `scripts/render_dense_algorithm_board.py`;
- writing `problem-analysis-workspace/ai-image-report.md`;
- giving `oj-problem-analysis-writer` a minimal image-reference patch only if the board passes review.

This skill is not responsible for:

- solving the problem;
- writing or changing the main explanation;
- replacing precise local diagrams that should be Mermaid/Graphviz/SVG/tables;
- batch-replacing older AI-generated images unless the user explicitly asks.

## Required Reads

Before creating a layout, read:

1. `index.md`
2. `problem-analysis-workspace/03-solution-derivation.md` when present
3. `problem-analysis-workspace/04-correctness-and-edge-cases.md` when present
4. `main.cpp`
5. `brute.cpp`
6. `references/prompt-guidelines.md`

Use only information present in these files. You may compress, rename, and reorganize concepts, but do not invent an algorithm step, proof claim, variable, complexity, or pitfall that the article/code does not support.

## Fixed Files

For a problem directory:

```text
problems/<oj>/<problem_id>/
  one-page-explainer.png              # adopted image, only after review
  one-page-explainer-v1.png           # rendered candidate
  one-page-explainer-v2.png
  problem-analysis-workspace/
    07-ai-image-evaluation.md
    ai-image-layout.json
    ai-image-preview.html
    ai-image-report.md
```

Do not overwrite older adopted images just to test the new renderer. For comparison runs, write a versioned output such as `one-page-explainer-dense-v1.png`.

## Evaluation Gate

Generate a dense board when at least one is true:

- The problem has a clear modeling jump from statement to algorithm.
- DP, graph theory, tree DP, binary search answer, greedy proof, data structures, math counting, or another multi-stage method benefits from a global teaching board.
- The article is long enough that students need a one-screen map before reading code.
- The solution has important pitfalls or hand-training steps worth surfacing.

Do not generate when:

- The problem is basic syntax, simple simulation, simple enumeration, or one/two-sentence logic.
- The only useful visual is a precise sample trace/table/graph that belongs in `oj-sample-visualizer`.
- The board would mostly repeat generic phrases.

Write `07-ai-image-evaluation.md` before rendering. If the conclusion is `否`, stop.

## Layout Schema

Write `problem-analysis-workspace/ai-image-layout.json` as UTF-8 JSON:

```json
{
  "schema_version": "dense_algorithm_board/v1",
  "title": "Pxxxx 题目名 专用训练流程图",
  "subtitle": "一句话核心思想，必须贴合题解。",
  "top_flow": [
    {"title": "输入/建模", "detail": "关键输入对象和约束"},
    {"title": "关键观察", "detail": "为什么能转成当前算法"},
    {"title": "算法收束", "detail": "最终怎么得到答案"}
  ],
  "columns": [
    {
      "title": "自适应主栏标题",
      "theme": "blue",
      "blocks": [
        {
          "title": "步骤标题",
          "formula": "`dp[i][j] = ...`",
          "items": ["短要点 1", "短要点 2"],
          "diagram": "可选的短文本示意",
          "table": {
            "headers": ["分类", "条件", "处理"],
            "rows": [["A", "`x=0`", "跳过"]]
          }
        }
      ]
    }
  ],
  "variables": [
    {"name": "dp[i][j]", "meaning": "状态含义"}
  ],
  "training_tips": ["手推小样例", "对照暴力", "检查边界"],
  "pitfalls": ["初始化", "数组范围", "特殊输入"],
  "complexity": {
    "time": "O(...)",
    "space": "O(...)",
    "notes": ["复杂度说明"]
  }
}
```

Required constraints:

- `schema_version` must be `dense_algorithm_board/v1`.
- Output canvas is fixed at `1920x1088`.
- `top_flow` has 3 to 6 steps.
- `columns` has exactly 3 main columns.
- Each column has 3 to 5 blocks. Prefer 4 when a column contains a table.
- `variables` has at least 2 concrete variable/formula entries.
- `training_tips` and `pitfalls` each have at least 3 entries.
- `complexity.time` and `complexity.space` are required.
- Use code spans for exact variables and short formulas: `` `dp[i][j]` ``, `` `check(x)` ``, `` `O(n log n)` ``.
- Never include long code blocks or unsupported exact sample/DP values.

## Rendering

Render a candidate PNG locally:

```bash
python3 .agents/skills/oj-ai-image-explainer/scripts/render_dense_algorithm_board.py \
  --problem-dir problems/<oj>/<problem_id> \
  --layout problem-analysis-workspace/ai-image-layout.json \
  --output one-page-explainer-dense-v1.png
```

Validate without rendering:

```bash
python3 .agents/skills/oj-ai-image-explainer/scripts/render_dense_algorithm_board.py \
  --problem-dir problems/<oj>/<problem_id> \
  --check-only
```

The renderer also writes `problem-analysis-workspace/ai-image-preview.html` for visual debugging.

## Review Gate

Before recommending insertion, check both layout and image:

- `ai-image-layout.json` passes the renderer's schema check.
- The image is `1920x1088` or otherwise explicitly requested.
- Text is readable, not clipped, and not overlapping.
- The three columns match the final solution route.
- Variables, formulas, complexity, pitfalls, and training tips are supported by the article/code.
- The board is dense and problem-specific, not generic.
- It does not contain fake platform logos, watermarks, decorative filler, or unsupported claims.

If review fails:

- Record the failure in `ai-image-report.md`.
- Do not insert or replace `one-page-explainer.png`.
- Adjust `ai-image-layout.json` and rerender a new version, or stop.

If review passes:

- Record the accepted version in `ai-image-report.md`.
- Only then copy or write the adopted file to `one-page-explainer.png`.
- Let `oj-problem-analysis-writer` decide whether and where to reference the image in `index.md`.

Recommended insertion when adopted:

```markdown
### 一图流解析

这张图把本题的建模、关键转移、实现检查和训练方法压缩到一页，适合读完正文后复盘。

![一图流解析](./one-page-explainer.png)
```

Place this section after `### 总结` by default. A dense one-page AI board is a post-reading review aid, not an early sample diagram. Do not insert it at the start of `### 思路` unless the user explicitly asks for a read-before overview.

## Report Format

Append to `problem-analysis-workspace/ai-image-report.md`:

```markdown
# AI 图片生成报告

## dense v1

- 布局文件：`problem-analysis-workspace/ai-image-layout.json`
- 输出文件：`one-page-explainer-dense-v1.png`
- 渲染方式：`dense_algorithm_board` + Playwright
- 尺寸：`1920x1088`
- 检查结论：通过 / 不通过
- 问题：
- 是否建议插入 `index.md`：是 / 否

## 最终采用

- 文件：`one-page-explainer.png`
- 来源版本：
- 插入位置：
- 备注：
```

Never include API tokens, base URLs, full request headers, or other secret-bearing local configuration in reports.

## Final Response

After using this skill, report briefly:

- whether evaluation concluded `是` or `否`;
- which layout/report files were created or updated;
- which PNG was rendered and whether it passed review;
- whether `index.md` was changed;
- if no image was adopted, why.

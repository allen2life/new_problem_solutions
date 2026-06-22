---
name: oj-visual-explainer
description: create accurate chinese teaching visuals for online judge and competitive programming problems. use when the user asks to explain an oj, noip, csp-s, codeforces, atcoder, usaco, luogu, or algorithm problem with diagrams; generate dp tables, graph and tree examples, mst or shortest path steps, binary search checks, data structure processes, string matching diagrams, interactive-problem flows, svg/mermaid diagrams, or image-generation prompts for one-page algorithm explanation infographics.
---

# OJ Visual Explainer

## Overview

Create teaching visuals for algorithm contest problems. Default to Chinese diagram text and prioritize structurally correct Mermaid or SVG diagrams over pure image generation.

Use this skill to transform a problem statement, editorial, solution outline, code, or sample into diagrams that help students understand the algorithm, especially for NOIP/CSP-S, Codeforces, AtCoder, USACO, and Luogu tasks.

## Operating Principles

- Prefer correctness over aesthetics. Algorithm edges, table values, states, and arrows must match the explanation.
- Default output language is Chinese.
- Prefer Mermaid or SVG for precise diagrams, tables, state transitions, graphs, trees, and step-by-step algorithm processes.
- Generate an image prompt only when the user needs a polished "一图流" overview, a slide/poster-style teaching infographic, or a non-strict conceptual summary.
- Do not place API keys, tokens, or secrets in the skill, generated files, or examples. If API integration is requested, instruct the user to store keys in environment variables such as `OPENAI_API_KEY`.
- If the provided problem or solution is incomplete, state assumptions clearly and mark uncertain diagram content as needing verification.
- Always include an audit checklist for diagrams that contain numeric DP values, graph edges, or sample traces.

## Workflow

### 1. Classify the problem and visual need

Identify the algorithm family and choose a visual pattern:

- DP: state definition block, transition arrows, DP table, rolling-array diagram.
- Knapsack: item-capacity table, choose/not choose transition, capacity scan direction.
- Interval DP: triangular interval table, length enumeration order, split point arrows.
- Tree DP: rooted tree, child-to-parent merge, rerooting before/after states.
- MST: weighted graph, sorted edges, Kruskal chosen/rejected edges, DSU merge state.
- Shortest path: graph sample, Dijkstra relaxation timeline, layered graph, path restoration.
- LCA/tree query: tree, depth, binary lifting table, DFS order, path-difference marks.
- Binary search answer: search interval, monotonic predicate, `check(x)` flow.
- Data structures: segment tree, Fenwick tree, monotonic queue, heap operations.
- Strings: KMP/Z arrays, trie, rolling hash substring slices, replacement/counting automaton.
- Interactive problems: query/response loop, hidden information recovery, candidate set shrinking.
- Constructive/greedy: case decision tree, exchange argument, sorted order and invariant.

Consult `references/visual-patterns.md` for template details.

### 2. Produce a visual plan before diagram code

Before generating Mermaid/SVG/prompt, summarize:

1. 题型与核心算法
2. 学生最容易卡住的点
3. 推荐图类型
4. 图中必须出现的变量、状态、边或表格
5. 是否需要严格样例数值校验

### 3. Generate Mermaid or SVG by default

Use Mermaid for:

- Flowcharts
- Algorithm pipelines
- Decision trees
- Simple graphs or dependency DAGs
- Sequence diagrams for interactive problems

Use SVG for:

- DP tables
- Trees with exact node positions
- Weighted graphs
- Segment trees / Fenwick trees
- Multi-panel teaching diagrams
- Diagrams requiring precise colors, coordinates, labels, or arrows

For SVG output:

- Use a `viewBox` and scalable layout.
- Use Chinese labels, but keep variable names such as `dp[i][j]`, `lca(u,v)`, `check(x)`, `lowbit` unchanged.
- Use a clean teaching palette: blue for observations, green for main algorithm, orange for branches/cases, red for pitfalls, gray for background.
- Keep every text label short; prefer multiple small labels over crowded paragraphs.

### 4. Generate image prompts only for one-page summaries

When the user asks for a polished infographic, "一图流", poster, cover image, or image API prompt, provide:

- `visual_spec`: structured diagram plan
- `prompt_zh`: Chinese image-generation prompt
- `prompt_en`: English image-generation prompt when useful for image models
- `negative_prompt`: text accuracy and artifact warnings
- `manual_checklist`: items the teacher must verify

Never embed an API key. If code is requested, show placeholders and environment-variable loading only.

### 5. Include verification and teaching notes

End with a concise checklist:

- 是否所有状态定义与题解一致
- 是否所有边、权值、转移箭头正确
- 是否样例数据和表格数值经过人工核对
- 是否复杂度和关键不变量写清楚
- 是否适合学生当前水平

## Output Modes

### Mode A: Diagram plan

Use when the user asks what kind of diagram to draw.

Output sections:

```markdown
## 图解方案
- 题型：
- 核心算法：
- 推荐图型：
- 图中模块：
- 人工核对点：
```

### Mode B: Mermaid diagram

Use for algorithm flow, binary search, interactive flow, and decision trees.

Output:

```markdown
## Mermaid 图
```mermaid
...
```
```

### Mode C: SVG diagram

Use for precise teaching figures.

Output a complete SVG code block:

```markdown
## SVG 图
```svg
<svg ...>...</svg>
```
```

### Mode D: One-image prompt

Use for infographic generation.

Output:

```markdown
## 一图流生成提示词
### visual_spec
...
### prompt_zh
...
### negative_prompt
...
### manual_checklist
...
```

## Quality Rules

- Use 16:9 horizontal layout for whole-problem overviews unless the user asks otherwise.
- Use A4 vertical layout for printable worksheets.
- Use 3 to 5 panels for complex editorials: observation, modeling, algorithm, tricky cases, pitfalls.
- Avoid dense paragraphs inside diagrams.
- For DP tables, include row/column meanings and scan order arrows.
- For graph diagrams, label whether edges are directed or undirected.
- For tree diagrams, label root, depth, subtree, or path as applicable.
- For interactive diagrams, include `flush`/query-count warnings when relevant.
- For generated prompts, instruct the image model to keep formulas and code-like tokens short and legible.

## Reference Files

- For visual templates and example patterns, read `references/visual-patterns.md`.
- For prompt templates and API-key safety wording, read `references/image-prompt-guidelines.md`.

---
name: oj-problem-relation-writer
description: Maintain prerequisite and similar-problem metadata in OJ problem index.md frontmatter. Use this skill when the user asks to add pre/common relations, 前置题目, 类似题目, common problems, learning path metadata, or problem graph relation data. This skill only writes relation metadata and candidate notes; it does not write problem analysis content and does not render graphs.
---

# OJ 题目关系维护

这个 skill 专门负责维护题目之间的学习关系，把高置信度关系写入当前题目的 `index.md` frontmatter。

它只负责关系元数据，不负责：

- 写题目解析正文。
- 修改 `main.cpp` / `brute.cpp` / `gen.py`。
- 生成或渲染前端图。
- 改 vis-network 或其他可视化代码。
- 把低置信度候选强行写进正式 frontmatter。

## 目标

为每道题补充两类关系：

- `pre`：当前题的前置题。前置题更简单，并且包含当前题的一部分核心思想、模型或算法。
- `common`：和当前题相似的题。它们不一定更简单，但解法模型、状态设计、核心观察或训练目标相似。

关系数据未来由 render/frontend 程序读取，用于展示题目学习图。

## 固定字段 Schema

在 `problems/<oj>/<problem_id>/index.md` 的 YAML frontmatter 中维护：

```yaml
pre:
  - oj: "luogu"
    problem_id: "P1002"
    reason: "网格路径计数 DP 的基础版本"
common:
  - oj: "luogu"
    problem_id: "P1002"
    reason: "同样是带限制的网格 DP"
```

字段规则：

- `pre` 和 `common` 都是数组。
- 数组元素必须是对象。
- `oj` 必须使用仓库中对应题目 frontmatter 的 `oj`。
- `problem_id` 必须优先使用目标题 `index.md` frontmatter 中的 `problem_id`；如果目标文件不存在或无法读取，才使用目录名作为临时候选。
- `reason` 是可选字段，但强烈推荐填写一句简短中文原因，方便后续图谱 tooltip 或人工复查。
- 不使用 `pid`。本仓库统一使用 `problem_id`。
- 不引用当前题自己。
- 不写重复关系。

## 图语义

假设当前题是 `A`：

```yaml
pre:
  - oj: "luogu"
    problem_id: "P1002"
```

语义是：

```text
luogu/P1002 -> A
```

也就是从前置题指向当前题。沿着箭头方向就是推荐学习路线。

`common` 不表示学习依赖方向：

```text
A -- B
```

前端可以渲染成无向边，或双向虚线边。这个 skill 不决定渲染方式。

## 关系判断标准

### `pre`

只在同时满足这些条件时写入 `pre`：

- 目标题明显更简单或更基础。
- 目标题包含当前题的一部分核心思想、模型、算法或实现技巧。
- 学完目标题能降低理解当前题的难度。
- 关系方向清楚：目标题是当前题的前置，而不是反过来。

常见例子：

- 一维 DP 是二维 DP 的前置。
- 普通网格路径计数是带障碍/特殊限制网格路径计数的前置。
- BFS 基础题是带状态压缩 BFS 的前置。
- 前缀和基础题是区间统计优化题的前置。

### `common`

只在解法结构或训练目标确实相似时写入 `common`：

- 使用相同核心模型，例如区间 DP、树形 DP、最短路、二分答案、双指针。
- 状态设计或转移方式高度相似。
- 关键观察相似。
- 适合放在同一组里对比训练。

`common` 不要求难度更低。

### 候选关系

如果只是标签相同、题面表面相似、或者无法确认难度/核心思想，不要写入 `index.md`。记录到：

```text
problems/<oj>/<problem_id>/problem-relation-workspace/candidates.md
```

候选记录格式建议：

```markdown
# 关系候选

## pre 候选

- `luogu/P1002`：可能是网格 DP 前置，但还没有确认当前题是否真的依赖该模型。

## common 候选

- `luogu/Pxxxx`：同为 DP 标签，但状态设计是否相似待确认。
```

## Source Priority

判断关系时按这个顺序读取信息：

1. 当前题 `index.md` frontmatter 和正文。
2. 当前题 `main.cpp`、`brute.cpp`、`problem.md`。
3. 当前题 `problem-analysis-workspace/*.md`，如果存在。
4. 候选题 `index.md` frontmatter 和正文。
5. 候选题 `main.cpp`、`brute.cpp`、`problem.md`。
6. 仓库搜索结果，例如 `tags`、标题、正文关键词。
7. 用户明确给出的关系或解释。

如果用户明确指定某个关系，仍然要检查是否引用自己、是否目标存在、字段格式是否正确。

## Search Workflow

当用户没有给出具体前置题或相似题时：

1. 先理解当前题的核心模型和标签。
2. 用 `rg` 搜索仓库中同标签、同模型、同关键词的题目。
3. 优先检查更简单、基础、经典的题。
4. 对每个候选判断是 `pre`、`common`，还是只写入 candidates。
5. 只把高置信度关系写入 frontmatter。

不要为了填满字段而强行找关系。没有高置信度关系时可以保留：

```yaml
pre: []
common: []
```

## Frontmatter Update Rules

更新 `index.md` 时：

- 只修改 YAML frontmatter 中的 `pre` / `common`，除非用户明确要求整理其他字段。
- 保留原有正文不变。
- 保留已有准确关系。
- 删除重复关系。
- 不删除已有关系，除非确认它错误或用户要求删除。
- 字段顺序遵守 `oj-problem-format-spec`；`pre`、`common` 放在 `categories` 后、`source` 前。
- 如果 `pre` / `common` 不存在，新增它们。

推荐 frontmatter 片段：

```yaml
tags: ["动态规划"]
categories: []
pre:
  - oj: "luogu"
    problem_id: "P1002"
    reason: "网格路径计数 DP 的基础版本"
common: []
source: https://www.luogu.com.cn/problem/Pxxxx
```

## Consistency Check

交付前检查：

- `pre` / `common` 是数组。
- 每个元素都有 `oj` 和 `problem_id`。
- 不使用 `pid`。
- 不引用当前题自己。
- 关系目标尽量能在仓库中找到对应 `problems/<oj>/<problem_dir>/index.md`。
- `problem_id` 与目标 frontmatter 一致；如果目录名和 frontmatter 不同，以 frontmatter 为准。
- `pre` 的关系方向是 `pre_problem -> current_problem`。
- `common` 不被描述为前置依赖。
- 低置信度候选没有写入正式 frontmatter。

## Verification Script

更新 `pre` / `common` 后，优先运行关系校验脚本：

```bash
python3 scripts/problem-analysis-tools/check_relations.py problems/<oj>/<problem_id>
```

如果当前工作目录已经是题目目录：

```bash
python3 ../../../scripts/problem-analysis-tools/check_relations.py
```

提交前或批量整理后可以检查全仓库：

```bash
python3 scripts/problem-analysis-tools/check_relations.py --all
```

这个脚本只做校验，不自动推荐关系、不修改 frontmatter、不生成图。

如果脚本没有运行，最终回复必须说明原因。

## Safety Rules

- 不要编造不存在的题目。
- 不要仅凭同一个 tag 写入关系。
- 不要把所有同类题都写成 `common`，只写真正有训练价值的相似题。
- 不要写题解正文。
- 不要改前端或图渲染代码。
- 不要把候选关系说成已确认关系。
- 不要 claim 图已经生成或渲染，除非用户另行要求并且实际完成。

## Final Response

完成后简短报告：

- 更新了哪个题目目录。
- `pre` 写入了哪些关系。
- `common` 写入了哪些关系。
- 是否创建或更新了 `problem-relation-workspace/candidates.md`。
- 是否运行了 `check_relations.py`，结果如何。
- 有哪些候选没有写入 frontmatter，以及原因。
- 是否发现引用目标不存在或需要用户确认。

# Dense Algorithm Board Guidelines

This skill renders deterministic teaching boards. Do not ask an image model to draw Chinese text. Build `ai-image-layout.json`, then render it with `render_dense_algorithm_board.py`.

## Product Definition

The target image is a dense algorithm handout board, not a poster:

- 16:9 fixed canvas, `1920x1088`.
- Top title and one-sentence core idea.
- Top flow strip with 3 to 6 concrete steps.
- Three main columns with problem-specific titles.
- Compact blocks containing variables, short formulas, mini tables, and diagrams.
- Bottom area containing training tips, pitfalls, key variables, and complexity.

The board should feel like a well-edited competitive-programming lecture page. It must be useful even if a student only looks at the image before reading the full article.

## Source Discipline

Use only:

- `index.md`
- derivation/correctness notes under `problem-analysis-workspace/`
- `main.cpp`
- `brute.cpp`

Allowed transformations:

- compress paragraphs into labels;
- rename sections into better teaching titles;
- group related steps into columns;
- extract variable meanings from code and text;
- turn a short classification into a small table.

Disallowed transformations:

- inventing a new algorithm path;
- inventing a proof not present in the article;
- adding unsupported complexity;
- adding exact sample values, edge weights, or DP values that the article does not already validate;
- using generic filler such as "先明确目标", "发现核心结构", or "复杂度落到可通过范围".

## Column Patterns

Keep exactly three columns. Titles should adapt to the problem.

Dynamic programming:

1. 状态与建模
2. 转移与顺序
3. 实现检查

Graph/DAG/shortest path:

1. 图上建模
2. 核心算法
3. 边界与复杂度

Binary answer:

1. 单调性与答案范围
2. `check(x)` 设计
3. 二分实现与边界

Greedy:

1. 局部选择
2. 正确性交换/归纳
3. 排序与实现

Math/counting:

1. 分类/化简
2. 贡献统计
3. 取模/边界

If none fits, choose concrete titles from the article. Avoid generic column names.

## Block Content Rules

Each column should contain 3 to 5 blocks. Prefer 4 blocks when a column contains a table. A good block usually has:

- a short title;
- one compact formula or 1 to 3 bullets;
- an optional mini table when classification matters;
- an optional text diagram such as ``上一层 -> 当前层 -> 答案``.

Use exact code-level variables when they help:

- `` `dp[i][j]` `` for state;
- `` `check(x)` `` for verifier;
- `` `prev` / `cur` `` for rolling arrays;
- `` `O(n log n)` `` for complexity;
- `` `lowbit` ``, `` `fa[x]` ``, `` `dist[u]` `` when they are central.

Do not include long code blocks. A single expression or assignment-like formula is fine.

## Bottom Sections

Every layout must include:

- `training_tips`: at least 3 items. Prefer hand simulation, brute-force comparison, boundary tests, and what to draw on paper.
- `pitfalls`: at least 3 items. Prefer initialization, array bounds, indexing, overflow, negative weights, unreachable states, sorting order, and special cases.
- `variables`: at least 2 entries with name and meaning.
- `complexity`: both time and space.

When the article has no explicit training tips, derive conservative practice steps from the existing brute/main solution:

- 手推最小样例；
- 用 `brute.cpp` 对照小数据；
- 检查边界和初始化。

## JSON Style

Write valid JSON only, no comments.

Keep strings compact. The renderer fits dense text, but the board should still be readable:

- title: about 12 to 28 Chinese characters plus problem id if useful;
- subtitle: one sentence, usually under 45 Chinese characters;
- block title: 4 to 14 Chinese characters;
- bullet: one short clause, usually under 28 Chinese characters;
- formula: one short expression.

Prefer code spans around variables and formulas. The renderer will style them.

## Review Checklist

Before rendering, check:

- Does the layout mention this problem's actual variables and algorithm?
- Are the three columns specific enough that another problem could not reuse them unchanged?
- Are the training tips and pitfalls actionable?
- Does every formula appear in the article or code?
- Is there no image-model wording such as "高清海报", "商业海报", "插画", or "照片风格"?

After rendering, inspect the PNG or preview HTML:

- no clipped text;
- no unreadably tiny text;
- no overlapping blocks;
- columns are balanced enough to scan;
- bottom sections are visible and useful.

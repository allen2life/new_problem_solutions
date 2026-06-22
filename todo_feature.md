# 功能优化 TODO

## P0：立刻有用

- [ ] `check_problem.py` 支持检查 `recommend` 字段顺序和格式。
  - 如果存在 `recommend`，检查它是否位于 `common` 后、`source` 前。
  - 检查 `recommend` 是否为数组。
  - 检查 `relation` 是否为 `similar`、`practice`、`harder`、`easier`。

- [ ] `problem_status.py` 增加关系与推荐状态。
  - 显示 `description` 是否为空。
  - 显示 `pre` / `common` / `recommend` 数量。
  - 显示是否存在 `problem-relation-workspace/candidates.md`。

- [ ] 编写 `recommend_candidates.py`。
  - 根据当前题 tags、description、标题、正文关键词生成候选。
  - 默认只写入 `problem-relation-workspace/candidates.md`。
  - 不自动写入正式 frontmatter。

- [ ] 优化题目详情页“推荐练习”展示。
  - 按 `similar` / `easier` / `harder` / `practice` 分组或加颜色。
  - 外部链接样式更明显。

- [ ] `fetch_problem` 后输出下一步提示。
  - 写 `main.cpp`。
  - 写 `brute.cpp`。
  - 运行 `check_sample.py`。
  - 使用 `oj-problem-analysis-writer`。
  - 使用 `oj-problem-relation-writer`。

## P1：提升写题效率

- [x] 样例可视化生成器。
  - 数组转 Markdown 表格。
  - 网格转 Markdown 表格。
  - 树输入转 `tree_draw.py` SVG。
  - 图输入转 Graphviz dot。
  - DP 表格模板生成。

- [ ] 增强 `tree_draw.py`。
  - 支持 BIT 责任区间图。
  - 支持红黑树静态 JSON 图。
  - 支持 B+ tree 静态 JSON 图。
  - 支持节点高亮路径。
  - 优化边标签显示。

- [ ] 增强 `problem_status.py`。
  - 是否有 `main.cpp`。
  - 是否有 `brute.cpp`。
  - 是否有样例。
  - 是否跑过对拍。
  - 是否有 tags。
  - 是否有 pre/common/recommend。
  - 是否有 description。

- [x] 题解质量检查器。
  - 检查是否只有代码没有解释。
  - 检查是否有图但没有图后说明。
  - 检查 `description` 是否空话。
  - 检查 `tags` 是否不在已有 tag 集合里。
  - 检查 `recommend.reason` 是否太短。

## P2：学习路径和推荐系统

- [ ] 新增 `/recommendations` 页面。
  - 按 tag 查看外部推荐。
  - 按 OJ 查看推荐。
  - 按 relation 查看 `easier` / `harder` / `similar` / `practice`。

- [ ] 关系图增强。
  - 增加“显示外部 recommend 节点”开关。
  - 默认关闭外部节点。

- [ ] 自动生成刷题路径。
  - 从 `pre` / `common` / `recommend` 生成入门路径。
  - 支持 DP、图论、位运算等专题路径。

- [ ] 相似题候选索引。
  - 使用 tags、description、标题、正文关键词生成候选。
  - 只生成候选，不直接写入正式字段。

## P3：更强的 Agent 工作流

- [ ] `oj-problem-analysis-writer` 最终 checklist 机器可读化。
  - 输出 JSON 或 Markdown checklist。
  - 方便另一个 agent 继续检查。

- [ ] `problem-analysis-workspace` 自动摘要。
  - 从 `01` 到 `05` 自动生成 `06-final-index-draft.md` 骨架。

- [ ] 新增“题解审稿 skill”。
  - 只检查题解质量，不写题解。
  - 检查思路是否跳步。
  - 检查复杂度是否和代码匹配。
  - 检查样例解释是否充分。
  - 检查可视化是否必要。
  - 检查推荐题是否合理。

- [ ] 外部 OJ 推荐验证脚本。
  - 对 `recommend.url` 做 HTTP 状态检查。
  - 失效链接给 warning。

## P4：部署和体验

- [ ] GitHub Action 检查。
  - push 时自动运行 `npm test`。
  - 自动运行 `check_relations.py --all`。
  - 自动运行 frontmatter 格式检查。

- [ ] 题解页推荐链接复制按钮。
  - 在推荐练习旁边添加复制按钮。

- [ ] 题解页工具条增强。
  - 展开/收起代码。
  - 展开/收起推荐。
  - 打开关系图。
  - 打开原题。

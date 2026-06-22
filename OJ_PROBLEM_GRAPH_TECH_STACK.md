# OJ 题目关系图谱技术方案

本文档用于指导 AI 或开发者实现一个“在线评测题目关系图谱”应用。目标是把多个 OJ 平台上的题目作为节点，用有向边表示题目之间的学习关系、前置关系、相似关系和进阶关系，并提供一个好看、可交互、可筛选的图谱界面。

## 1. 产品目标

这个应用不是普通题单，也不是静态知识图。它应该像一个可探索的学习地图：

- 每个节点代表一道 OJ 题目。
- 每条边代表两道题之间的关系。
- 用户可以看到“先做哪些题，再做哪些题”。
- 用户可以按标签、难度、平台、完成状态筛选。
- 用户点击题目后，可以看到前置题、后继题、相似题和题目详情。
- 图谱应该支持缩放、拖拽、搜索、高亮、布局切换。

典型使用场景：

- 学习某个算法专题，比如二分、DP、图论。
- 查看一道题的前置知识和后续进阶题。
- 根据已完成题目推荐下一道题。
- 维护自己的跨平台 OJ 题目知识图谱。

## 2. 推荐技术栈

### 前端

```text
React
TypeScript
Vite
@xyflow/react
ELK.js
d3-force
Zustand
Tailwind CSS
```

各技术的作用：

- `React`：构建交互式前端界面。
- `TypeScript`：约束题目节点、边、筛选条件等核心数据结构。
- `Vite`：开发服务器和构建工具。
- `@xyflow/react`：也叫 React Flow / XYFlow，用于渲染节点图、边、缩放、拖拽、MiniMap 和自定义节点。
- `ELK.js`：用于有向图的自动分层布局，适合展示“基础题 -> 进阶题”的学习路径。
- `d3-force`：用于力导向布局，适合做专题探索模式，让相关题目自然聚集。
- `Zustand`：管理前端状态，例如当前选中节点、筛选器、搜索结果、布局模式。
- `Tailwind CSS`：实现深色主题、节点卡片、发光边、高亮状态和响应式布局。

### 数据与后端

第一版推荐：

```text
PostgreSQL
Prisma 或 Drizzle
```

可选增强：

```text
Neo4j
```

建议先不要直接上 Neo4j。对于个人项目、中小规模题库、几百到几千道题，PostgreSQL 完全够用。只有当图查询非常复杂，例如需要大量路径搜索、社区发现、多跳关系分析时，再考虑 Neo4j。

## 3. 核心数据模型

### 题目节点

```ts
type ProblemNode = {
  id: string
  oj: "leetcode" | "luogu" | "codeforces" | "atcoder" | "other"
  number: string
  title: string
  difficulty: "easy" | "medium" | "hard" | "unknown"
  tags: string[]
  url: string
  solved?: boolean
  note?: string
}
```

示例：

```ts
{
  id: "leetcode-704",
  oj: "leetcode",
  number: "704",
  title: "Binary Search",
  difficulty: "easy",
  tags: ["binary-search", "array"],
  url: "https://leetcode.com/problems/binary-search/",
  solved: true
}
```

### 题目关系边

```ts
type ProblemEdge = {
  id: string
  source: string
  target: string
  type: "prerequisite" | "similar" | "harder-version" | "same-pattern"
  weight?: number
  note?: string
}
```

边类型含义：

- `prerequisite`：前置关系。`source` 应该先做，`target` 是后续题。
- `similar`：相似题。两题技巧、结构或考点接近。
- `harder-version`：进阶版本。`target` 是 `source` 的更难版本。
- `same-pattern`：同一套路。两题属于同一种解题模板或思维模式。

示例：

```ts
{
  id: "edge-leetcode-704-to-leetcode-34",
  source: "leetcode-704",
  target: "leetcode-34",
  type: "prerequisite",
  weight: 0.9,
  note: "先掌握基础二分，再做查找左右边界。"
}
```

## 4. 数据库存储建议

### problems 表

```sql
CREATE TABLE problems (
  id TEXT PRIMARY KEY,
  oj TEXT NOT NULL,
  number TEXT NOT NULL,
  title TEXT NOT NULL,
  difficulty TEXT NOT NULL,
  tags TEXT[] NOT NULL DEFAULT '{}',
  url TEXT NOT NULL,
  solved BOOLEAN NOT NULL DEFAULT FALSE,
  note TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

### problem_edges 表

```sql
CREATE TABLE problem_edges (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL REFERENCES problems(id),
  target TEXT NOT NULL REFERENCES problems(id),
  type TEXT NOT NULL,
  weight REAL DEFAULT 1.0,
  note TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

## 5. 图谱界面设计

推荐页面结构：

```text
┌──────────────────────────────────────────────┐
│ 顶部工具栏：搜索、布局切换、导入导出、主题切换 │
├──────────────┬─────────────────┬─────────────┤
│ 左侧筛选器    │ 中间图谱画布      │ 右侧详情面板 │
│              │                 │             │
│ OJ           │ 节点 + 有向边     │ 题目标题     │
│ 难度          │ 缩放/拖拽/MiniMap │ 链接         │
│ 标签          │ 高亮路径         │ 标签         │
│ 完成状态      │                 │ 前置/后继题   │
└──────────────┴─────────────────┴─────────────┘
```

第一版必须实现：

- 图谱画布
- 自定义题目节点
- 有向边
- 点击节点显示详情
- 搜索题目
- 按难度和标签筛选
- 高亮选中题目的前置题和后继题
- 布局切换：学习路径模式 / 探索模式

## 6. 节点视觉设计

题目节点建议做成卡片，而不是普通圆点。

节点内容：

```text
[LC 704] Binary Search
Easy
binary-search / array
已完成
```

难度颜色：

```text
easy    绿色
medium  黄色
hard    红色
unknown 灰色
```

状态样式：

```text
已完成     节点边框高亮
未完成     普通暗色
当前选中   发光边框
推荐下一题  呼吸光效
被过滤     降低透明度
```

React Flow 自定义节点数据示例：

```ts
type ProblemFlowNodeData = {
  problem: ProblemNode
  incomingCount: number
  outgoingCount: number
  isSelected: boolean
  isHighlighted: boolean
}
```

## 7. 边的视觉设计

边类型建议用不同颜色和线型：

```text
prerequisite   蓝绿色实线，表示学习路径
similar        灰色虚线，表示相似题
harder-version 紫色实线，表示进阶题
same-pattern   黄色虚线，表示同套路题
```

有向边必须显示箭头。用户点击边时，右侧详情面板可以显示这条关系的说明。

## 8. 布局策略

### 学习路径模式

使用 `ELK.js`。

适合 DAG 或接近 DAG 的图。基础题放左侧或上方，进阶题向右或向下展开。

推荐配置：

```ts
const elkOptions = {
  algorithm: "layered",
  "elk.direction": "RIGHT",
  "elk.layered.spacing.nodeNodeBetweenLayers": "100",
  "elk.spacing.nodeNode": "60",
  "elk.edgeRouting": "ORTHOGONAL"
}
```

### 专题探索模式

使用 `d3-force`。

适合展示大量相似题、同套路题、跨专题联系。节点会根据边自然聚集。

推荐力模型：

```ts
forceSimulation(nodes)
  .force("link", forceLink(edges).id(d => d.id).distance(180))
  .force("charge", forceManyBody().strength(-500))
  .force("center", forceCenter(0, 0))
  .force("collide", forceCollide().radius(120))
```

### 分组模式

可选。按标签或难度分泳道：

```text
数组
二分
双指针
动态规划
图论
数据结构
```

这个模式适合做专题主页。

## 9. React Flow 转换逻辑

将业务节点转换成 React Flow 节点：

```ts
import type { Node, Edge } from "@xyflow/react"

function toFlowNodes(problems: ProblemNode[]): Node[] {
  return problems.map((problem) => ({
    id: problem.id,
    type: "problem",
    position: { x: 0, y: 0 },
    data: {
      problem,
      incomingCount: 0,
      outgoingCount: 0,
      isSelected: false,
      isHighlighted: false
    }
  }))
}
```

将业务边转换成 React Flow 边：

```ts
function toFlowEdges(problemEdges: ProblemEdge[]): Edge[] {
  return problemEdges.map((edge) => ({
    id: edge.id,
    source: edge.source,
    target: edge.target,
    type: "smoothstep",
    animated: edge.type === "prerequisite",
    label: edge.type,
    data: edge,
    markerEnd: {
      type: "arrowclosed"
    }
  }))
}
```

## 10. 状态管理

使用 Zustand。

建议状态：

```ts
type LayoutMode = "learning-path" | "explore" | "grouped"

type GraphStore = {
  problems: ProblemNode[]
  edges: ProblemEdge[]
  selectedProblemId: string | null
  searchQuery: string
  activeTags: string[]
  activeDifficulties: string[]
  showSolved: boolean
  showUnsolved: boolean
  layoutMode: LayoutMode
}
```

需要的操作：

```ts
selectProblem(id)
setSearchQuery(query)
toggleTag(tag)
toggleDifficulty(difficulty)
toggleSolvedFilter()
setLayoutMode(mode)
```

## 11. 推荐交互

点击节点：

- 选中当前题目。
- 高亮它的一跳前置题。
- 高亮它的一跳后继题。
- 右侧打开题目详情。

双击节点：

- 打开题目原链接。

搜索题目：

- 匹配题号、标题、标签、OJ。
- 搜索结果节点发光。
- 可自动定位到第一个结果。

筛选：

- 按 OJ 筛选。
- 按难度筛选。
- 按标签筛选。
- 按完成状态筛选。
- 按边类型筛选。

路径查看：

- 选中一道题后，提供“查看所有前置路径”。
- 提供“推荐下一题”。

## 12. 性能策略

如果题目数量在 300 到 1000 道之间，React Flow 足够。

如果超过 3000 道题，需要注意：

- 默认只展示某个专题或筛选后的子图。
- 不要一次渲染所有节点。
- 搜索后只展示邻域子图。
- 可以使用节点聚合，例如把一个专题折叠成一个大节点。

如果需要展示 5000+ 节点和几万条边，应考虑：

```text
Sigma.js + Graphology
```

Sigma.js 使用 WebGL，更适合海量点线网络。但它不适合复杂卡片节点。如果节点需要显示大量文字、按钮和状态，React Flow 仍然更合适。

## 13. 第一版实现路线

### Milestone 1：静态图谱

- 准备一份本地 JSON 数据。
- 实现 React Flow 画布。
- 实现自定义题目节点。
- 实现不同边类型的颜色。
- 实现 ELK 分层布局。

### Milestone 2：交互

- 点击节点显示右侧详情。
- 搜索题目。
- 按标签、难度、OJ 筛选。
- 高亮前置题和后继题。

### Milestone 3：数据持久化

- 使用 PostgreSQL 存储题目和关系。
- 使用 Prisma 或 Drizzle 定义 schema。
- 提供 API 获取图谱数据。
- 支持标记 solved。

### Milestone 4：学习路径能力

- 给定目标题，找出所有前置题。
- 根据 solved 状态推荐下一题。
- 支持专题视图。
- 支持导入/导出 JSON。

## 14. 推荐目录结构

```text
src/
  app/
    App.tsx
  components/
    graph/
      ProblemGraph.tsx
      ProblemNode.tsx
      ProblemEdge.tsx
      GraphToolbar.tsx
      GraphFilters.tsx
      ProblemDetailsPanel.tsx
    layout/
      AppShell.tsx
  data/
    sample-problems.json
  lib/
    graph/
      to-flow-elements.ts
      elk-layout.ts
      force-layout.ts
      graph-utils.ts
  store/
    graph-store.ts
  types/
    graph.ts
```

## 15. 给 AI 实现者的关键要求

实现时请遵守：

- 使用 React + TypeScript + Vite。
- 图谱渲染使用 `@xyflow/react`。
- 节点必须是自定义 React 组件，不要只用默认圆点。
- 有向边必须带箭头。
- 学习路径模式使用 `ELK.js` 分层布局。
- 探索模式可以使用 `d3-force`。
- 深色背景，节点卡片清晰，边颜色按关系类型区分。
- 第一版优先保证交互完整，不要过早引入复杂后端。
- 数据结构必须保持 `ProblemNode[]` 和 `ProblemEdge[]` 两部分清晰分离。
- 所有筛选和搜索都应作用于图谱的可见子图。

## 16. 最小可行版本

最小可行版本只需要：

- 一个 `sample-problems.json`
- 一个 `ProblemGraph.tsx`
- 一个 `ProblemNode.tsx`
- 一个 `GraphFilters.tsx`
- 一个 `ProblemDetailsPanel.tsx`
- ELK 自动布局
- 搜索和点击节点

不要一开始就做：

- 复杂权限系统
- 多用户协作
- Neo4j
- 大规模 WebGL 渲染
- 自动爬虫
- AI 自动生成边

先把手工维护的高质量关系图做出来。图谱好不好用，核心不是动画，而是题目之间的关系是否准确。

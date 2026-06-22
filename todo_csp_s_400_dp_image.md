---
title: "CSP-S 400 DP 转移与一图流计划"
description: "筛选 csp-s-400 题单中需要补 DP 转移方程和 dense algorithm board 的题目。"
source: problem-sets/csp-s-400.md
---

# CSP-S 400 DP 转移与一图流计划

## 目标

对 [`problem-sets/csp-s-400.md`](problem-sets/csp-s-400.md) 中 DP 相关题目做两类后处理：

- 正文补齐明确的 `#### DP 转移方程` 或等价公式块，让读者能直接看到状态、初值、转移、答案。
- 对适合复盘的题目生成 `dense_algorithm_board` 一图流，放在 `### 总结` 后的 `### 一图流解析`。

## 筛选口径

需要补公式：

- 题解中已经使用 DP、递推、记忆化搜索、树形背包、状压、优化 DP，但正文没有集中写出状态转移。
- 只补题解和代码已经支持的公式，不为了形式强行改算法。

需要一图流：

- T4/T5/T6 中有明显建模跳跃、状态设计、树上合并、状压轮廓、优化 DP、组合计数推导的题。
- 正文、`main.cpp`、`brute.cpp` 都已完成。
- 图片能帮助学生读完后复盘状态、转移、实现检查和坑点。

跳过一图流：

- 短递推、纯公式 Catalan、纯枚举、简单记忆化搜索。
- 题单归在 DP 附近，但当前正解是贪心、并查集、单调队列判定等非 DP 主线。
- 代码不完整或正文不足以支撑一图流。

## 执行批次

### A. 先补或规范化 DP 转移方程

- [x] P7118 Galgame
- [x] P3200 有趣的数列
- [x] P4084 Barn Painting G
- [x] P2986 Great Cow Gathering G
- [x] P2015 二叉苹果树
- [x] P3177 树上染色
- [x] P3174 毛毛虫
- [x] P8089 Color
- [x] P2899 Cell Phone Network G
- [x] P8687 糖果
- [x] P8733 补给
- [x] P8756 国际象棋
- [x] P3888 拯救莫莉斯
- [x] P2831 愤怒的小鸟
- [x] P2704 炮兵阵地
- [x] P1879 Corn Fields G
- [x] P4832 珈百璃堕落的开始
- [x] P4138 挂饰
- [x] P4037 魔兽地图
- [x] P8935 茎
- [x] P9111 最大权独立集问题
- [x] P1464 Function
- [x] P5635 天下第一
- [x] P2690 Apple Catching G
- [x] P1544 三倍经验
- [x] P3609 Hoof, Paper, Scissor G
- [x] P3257 天天酷跑

### B. 生成 dense 一图流

优先生成这些题：

- [x] P7118 Galgame
- [x] P3200 有趣的数列
- [x] P3047 Nearby Cows G
- [x] P4084 Barn Painting G
- [x] P2986 Great Cow Gathering G
- [x] P4362 贪吃的九头龙
- [x] P3177 树上染色
- [x] P3174 毛毛虫
- [x] P8089 Color
- [x] P2899 Cell Phone Network G
- [x] P8733 补给
- [x] P8756 国际象棋
- [x] P3888 拯救莫莉斯
- [x] P2831 愤怒的小鸟
- [x] P2704 炮兵阵地
- [x] P1879 Corn Fields G
- [x] P2511 木棍分割
- [x] P2569 股票交易
- [x] P2254 瑰丽华尔兹
- [x] P3572 PTA-Little Bird
- [x] P5017 摆渡车
- [x] P2497 基站建设
- [x] P4056 火星藏宝图
- [x] P6302 回家路线 加强版
- [x] P2900 Land Acquisition G
- [x] P2120 仓库建设
- [x] P3195 玩具装箱
- [x] P5785 任务安排
- [x] P4138 挂饰
- [x] P7097 牵丝戏
- [x] P6893 Buffed Buffet
- [x] P4516 潜入行动
- [x] P4026 循环的债务
- [x] P4037 魔兽地图
- [x] P8935 茎
- [x] P9111 最大权独立集问题
- [x] P1880 石子合并
- [x] P4767 邮局 加强版
- [x] P3257 天天酷跑

### C. 跳过或只写评估

- [x] P1722、P1044、P1976、P1754、P1375：短 Catalan/递推题，正文公式比 dense board 更有效。
- [x] P8625、P8744、P3052、P1433、P2513、P1464、P2690、P1544、P3609：模型较短，优先保留正文公式；本轮评估后不生成一图流。
- [x] P7846：正解主线是并查集缩点和二分图染色，不补 DP 方程。
- [x] P7859：正解是 `2^N` 状压枚举，不补 DP 方程。
- [x] P3594：正解是双指针 + 单调队列维护窗口最大段和，不补 DP 方程。
- [x] P4823：正解是排序 + 优先队列贪心，不补 DP 方程。
- [x] P4322：本地缺少 `main.cpp` 和 `brute.cpp`，本轮不生成一图流。

## 验收标准

每个采用一图流的题目应具备：

- `problem-analysis-workspace/07-ai-image-evaluation.md`
- `problem-analysis-workspace/ai-image-layout.json`
- `one-page-explainer-dense-v1.png`
- `one-page-explainer.png`
- `problem-analysis-workspace/ai-image-report.md`
- `index.md` 中 `### 总结` 后的 `### 一图流解析`

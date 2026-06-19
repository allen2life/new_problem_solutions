---
oj: "luogu"
problem_id: "P1130"
title: "红牌"
description: "把每一步在每个小组的最小代价做成阶段型 DP，状态只可能来自本组或前一组。"
difficulty: "普及-"
date: 2026-06-19 11:01
toc: true
tags: ["dp", "动态规划"]
categories: []
pre: []
common: []
recommend: []
source: https://www.luogu.com.cn/problem/P1130
---

[[TOC]]

### 题意

有 `m` 个小组，要完成 `n` 个步骤。

第 `i` 组做第 `j` 步需要 `cost[i][j]` 天。

每一步你可以：

- 继续留在当前组；
- 或在相邻两步之间切换到下一组（`m` 的下一组视作 `1`）。

要求求出完成全部步骤的最小总代价。

### 思路

最直接的教学版做法是搜索每一步“留在本组”还是“切到下一组”：

@include-code(./brute.cpp, cpp)

但正式解法用 DP 更自然。

设 `dp[i]` 表示当前处理到某一步时，停在第 `i` 组的最小总代价。

如果这一列要到第 `i` 组，那么上一列只能来自：

1. 原本就在第 `i` 组；
2. 原本在第 `i` 的前一个组，然后本步切换过来。

所以转移是：

`new_dp[i] = min(dp[i], dp[prev(i)]) + cost[i][step]`

第一步可以任选小组，因此直接初始化为第一列代价。

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

- 时间复杂度：`O(nm)`
- 空间复杂度：`O(m)`

### 总结

这题的本质是一个很标准的“按列推进”的阶段型 DP。

关键只在于看清楚：每个状态的来源永远只有两个。

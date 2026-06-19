---
oj: "luogu"
problem_id: "P1359"
title: "租用游艇"
description: "把出租站看成 DAG 上的点，按编号顺序做最短路/动态规划，转移到所有更下游的站点。"
difficulty: "普及-"
date: 2026-06-19 11:10
toc: true
tags: ["dp", "最短路", "动态规划"]
categories: []
pre: []
common: []
recommend: []
source: https://www.luogu.com.cn/problem/P1359
---

[[TOC]]

### 题意

有 `n` 个游艇站点。

可以从任意站点 `i` 直接租到任意更下游的站点 `j`，费用为 `r[i][j]`。

要求求出从 `1` 号站到 `n` 号站的最少租金。

### 思路

最直接的教学版做法是搜索所有可能的租船路线：

@include-code(./brute.cpp, cpp)

但这题其实可以直接做 DP。

把每个站点看成一个点，从 `i` 向所有 `j > i` 连边，边权是租金。

由于边只会从小编号走向大编号，所以这是一张 DAG。

设 `dp[i]` 表示从 `1` 到 `i` 的最少租金，那么：

`dp[j] = min(dp[j], dp[i] + cost[i][j])`

按编号顺序从小到大转移就行。

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(n^2)`

### 总结

这题虽然看起来像图论题，但因为图本身就是按编号单向向下的，所以直接按编号做 DP 最简单。

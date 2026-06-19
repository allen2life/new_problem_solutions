---
oj: "luogu"
problem_id: "P1216"
title: "[IOI 1994 / USACO1.5] 数字三角形 Number Triangles"
description: "用二维动态规划维护走到每个位置的最大路径和，状态只来自上一层相邻两个位置。"
difficulty: "入门"
date: 2026-06-19 11:04
toc: true
tags: ["dp", "动态规划"]
categories: []
pre: []
common: []
recommend: []
source: https://www.luogu.com.cn/problem/P1216
---

[[TOC]]

### 题意

给出一个数字三角形。

从顶部出发，每次只能走到下一行相邻的两个位置之一。

要求求出从顶到底的最大路径和。

### 思路

最直接的教学版做法是搜索所有路径：

@include-code(./brute.cpp, cpp)

但正式解法用标准 DP 更直接。

设 `dp[i][j]` 表示走到第 `i` 行第 `j` 个位置时的最大路径和。

由于当前位置只可能从上一行相邻两个位置走来，所以：

`dp[i][j] = max(dp[i-1][j-1], dp[i-1][j]) + a[i][j]`

初始 `dp[1][1] = a[1][1]`，最后答案是最后一行中的最大值。

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

- 时间复杂度：`O(n^2)`
- 空间复杂度：`O(n^2)`

### 总结

这题是数字三角形 DP 的最经典模型。

看清“一个位置只依赖上一层相邻两个位置”，就可以直接写出转移。

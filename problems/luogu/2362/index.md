---
oj: "luogu"
problem_id: "P2362"
title: "最长上升子序列（LIS 长度 + 方案数）"
date: 2026-05-31 15:31
toc: true
tags: ["dp", "lis"]
desc: "求最长上升子序列长度及方案数"
source: https://www.luogu.com.cn/problem/P2362
---

[[TOC]]

## 题目解析

### 题意

多组数据，每组给定一个序列，求**最长严格上升子序列（LIS）的长度**，以及**达到该长度的方案数**。

### 思路

经典 LIS 的 DP 扩展，多维护一个方案数即可。

设：
- $dp[i]$：以 $i$ 结尾的最长上升子序列长度
- $cnt[i]$：达到 $dp[i]$ 长度的方案数

转移：
- 初始化：$dp[i] = 1,\; cnt[i] = 1$（每个元素自身）
- 对 $j < i$，若 $a[j] < a[i]$：
  - $dp[j] + 1 > dp[i]$：更新 $dp[i]$，$cnt[i] = cnt[j]$
  - $dp[j] + 1 = dp[i]$：$cnt[i] += cnt[j]$

最后取 $\max dp[i]$ 为 LIS 长度，累加所有 $dp[i] = \text{max\_len}$ 的 $cnt[i]$ 为方案数。

### 复杂度

$O(T \cdot n^2)$，$n \le 2000$ 时可接受。

## 代码 

@include-code(./1.cpp, cpp)


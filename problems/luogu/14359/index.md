---
oj: "luogu"
problem_id: "P14359"
title: "[CSP-J 2025] 异或和"
date: 2026-02-04 09:00
toc: true
tags: ["贪心", "位运算", "前缀和"]
categories: []
source: https://www.luogu.com.cn/problem/P14359
---

[[TOC]]

### 题意

给定一个长度为 $n$ 的非负整数序列 $a_1, a_2, \dots, a_n$ 和一个非负整数 $k$。定义区间 $[l, r]$ 的权值为区间内所有数的异或和。需要选出尽可能多的**不相交**区间，使每个区间的权值都等于 $k$。输出最多能选出的区间数。

#### 样例

以样例 1 为例：$n = 4, k = 2$，序列 $[2, 1, 0, 3]$。

可以选区间 $[1, 1]$（权值 $2$）和 $[2, 4]$（权值 $1 \oplus 0 \oplus 3 = 2$），答案为 $2$。

### 思路

题目要求最大化不相交区间的个数，且每个区间的权值（异或和）必须等于 $k$。由于所有区间的权重相同（均为 1），**按结束时间最早贪心**是最优策略——从左到右扫描，一旦发现可以结束一个合法区间就立即选取。

**前缀异或技巧**：令 $pre[i] = a_1 \oplus a_2 \oplus \dots \oplus a_i$，则区间 $[l, r]$ 的异或和为 $pre[r] \oplus pre[l-1]$。条件 $pre[r] \oplus pre[l-1] = k$ 等价于 $pre[l-1] = pre[r] \oplus k$。

因此，对每个右端点 $i$，只需检查 $pre[i] \oplus k$ 是否在当前段中出现过。配合哈希表可以在 $O(1)$ 时间内完成判断。

先看一个可以直接验证想法的正确解（$O(n^2)$ DP，仅适合小数据）：

@include-code(./brute.cpp, cpp)

`brute.cpp` 的 $O(n^2)$ 瓶颈在于对每个 $i$ 都需要枚举所有 $j < i$。利用前缀异或的性质，我们将判断条件改写为 $pre[j] = pre[i] \oplus k$，从而将 $O(n^2)$ 枚举转化为 $O(1)$ 哈希查询。

具体做法：从左到右扫描，用哈希表记录当前段中出现过的所有前缀异或值。对每个位置 $i$：

1. 计算 $pre = pre \oplus a_i$
2. 查询 $target = pre \oplus k$ 是否在哈希表中
3. 如果在，说明存在某个 $j$ 使得 $[j+1, i]$ 异或和为 $k$ → 答案加 1，清空哈希表，重置 $pre = 0$
4. 如果不在，将 $pre$ 加入哈希表

清空哈希表有多种实现方式：

| 实现 | 清空方式 | 复杂度 | 得分 |
| --- | --- | --- | --- |
| 桶 + `memset` | `memset(b,0,sizeof(b))` | $O(2^{20})$ 每次 | 90 分 TLE |
| `std::map` | `b.clear()` | $O(段大小)$ | 100 分 |
| 时间戳数组 | `cur++` | $O(1)$ 每次 | 100 分 |

最终采用**时间戳数组**：开一个全局数组 $vis[x]$，用 $vis[x] = cur$ 表示 $x$ 在当前段中出现过。清空时只需 `cur++`，无需遍历数组。

不同分值的代码实现如下，可以对照学习从 60 分到 100 分的优化过程：

<details>
<summary>60 分：O(n²) 贪心扫描</summary>

@include-code(./1.cpp, cpp)
</details>

<details>
<summary>90 分：前缀异或 + memset 桶（TLE）</summary>

@include-code(./2.cpp, cpp)
</details>

<details>
<summary>100 分：前缀异或 + std::map</summary>

@include-code(./3.cpp, cpp)
</details>

<details>
<summary>100 分：前缀异或 + 时间戳桶（最优）</summary>

@include-code(./4.cpp, cpp)
</details>

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

- 时间复杂度：$O(n)$。每个元素处理一次，哈希查询和更新均为 $O(1)$。
- 空间复杂度：$O(2^{20}) \approx 10^6$ 的 `vis` 数组，加上 $O(n)$ 的存储输入。

### 总结

本题是 CSP-J 2025 的题目，核心模型是**单位权重区间调度 + 前缀异或哈希**。关键点在于将区间异或条件转化为前缀异或的查询，再利用贪心性质从左到右扫描。实现上，**时间戳技术**避免了每次清空大数组的开销，是一个值得掌握的优化技巧。

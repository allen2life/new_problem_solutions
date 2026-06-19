# P9666 [ICPC 2021 Macao R] Link-Cut Tree
## 题目描述

BaoBao just learned how to use a data structure called link-cut tree to find cycles in a graph and decided to give it a try. BaoBao is given an undirected graph with $n$ vertices and $m$ edges, where the length of the $i$-th edge equals $2^i$. She needs to find a simple cycle with the smallest length.

A simple cycle is a subgraph of the original graph containing $k$ ($3 \le k \le n$) vertices $a_1, a_2, \cdots, a_k$ and $k$ edges such that for all $1 \le i \le k$ there is an edge connecting vertices $a_i$ and $a_{(i \mod k) + 1}$ in the subgraph. The length of a simple cycle is the total length of the edges in the cycle.

## 输入输出样例 #1

### 输入 #1

```
2
6 8
1 2
2 3
5 6
3 4
2 5
5 4
5 1
4 2
4 2
1 2
4 3
```

### 输出 #1

```
2 4 5 6
-1
```

## 说明/提示

The first sample test case is shown below. The integers beside the edges are their indices (outside the parentheses) and lengths (inside the parentheses). The simple cycle with the smallest length consists of edges $2$, $4$, $5$ and $6$ with a length of $2^2 + 2^4 + 2^5 + 2^6 = 116$.

# P3318 [SDOI2015] 双旋转字符串
## 题目描述

给定两个字符串集合 $\mathcal{S}$ 和 $\mathcal{T}$。其中 $S$ 中的所有字符串长度都恰好为 $N$，而 $T$ 中所有字符串长度都恰好为 $M$。且 $N+M$ 恰好为偶数。

如果记 $\mathcal{S}$ 中字符串全体为 $S_1,S_2,\dots,S_{Total_S}$，而 $\mathcal{T}$ 中字符串全体为 $T_1,T_2,\dots,T_{Total_T}$。现在希望知道有多少对 $\langle i, j \rangle$，满足将 $S_i$ 和 $T_j$ 拼接后得到的字符串 $S_i+T_j$ 满足双旋转性。

一个长度为偶数字符串 $W$ 可以表示成两段长度相同的字符串的拼接，即 $W=U+V$。如果 $V$ 可以通过 $U$ 旋转得到，则称 $W$ 是满足双旋转性的。比如说字符串 `vijos` 可以通过旋转得到 `ijosv`,`josvi`,`osvij` 或 `svijo`。那么 `vijosjosvi` 就是满足双旋转性的字符串。

## 输入输出样例 #1

### 输入 #1

```
4 4 7 3
vijosvi
josvivi
vijosos
ijosvsv
jos
vij
ijo
jos
```

### 输出 #1

```
6
```

## 说明/提示

对于 $10\%$ 的数据，$1\leq N\leq 100$，$1\leq M\leq 100$，$1\leq Total_S\leq 100$，$1\leq Total_T\leq 100$。

对于 $30\%$ 的数据，$1\leq N\leq 500$，$1\leq M\leq 500$，$1\leq Total_S\leq 500$，$1\leq Total_T\leq 500$。

对于 $60\%$ 的数据，$2\le N\times Total_S+M\times Total_T\le 4\times 10^5$。

对于 $100\%$ 的数据，$2\le N\times Total_S+M\times Total_T\le 4\times 10^6$。

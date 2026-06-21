# P6739 [BalticOI 2014] Three Friends (Day1)
## 题目描述

有一个字符串 $S$，对他进行操作：

1. 将 $S$ 复制为两份，存在字符串 $T$ 中
2. 在 $T$ 的某一位置上插入一个字符，得到字符串 $U$

现在给定 $U$，求 $S$。

## 输入输出样例 #1

### 输入 #1

```
7
ABXCABC
```

### 输出 #1

```
ABC
```

## 输入输出样例 #2

### 输入 #2

```
6
ABCDEF
```

### 输出 #2

```
NOT POSSIBLE
```

## 输入输出样例 #3

### 输入 #3

```
9
ABABABABA
```

### 输出 #3

```
NOT UNIQUE
```

## 说明/提示

#### 数据规模与约定

**本题采用捆绑测试。**

- Subtask 1（35 pts）：$N \le 2001$。
- Subtask 2（65 pts）：无特殊限制。

对于 $100\%$ 的数据，$2 \le N \le 2 \times 10^6+1$，保证 $U$ 中只包含大写字母。

#### 说明

翻译自 [BalticOI 2014 Day1 B Three Friends](https://boi.cses.fi/files/boi2014_day1.pdf)。

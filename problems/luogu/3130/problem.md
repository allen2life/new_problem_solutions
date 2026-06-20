# P3130 [USACO15DEC] Counting Haybale P
## 题目描述

Farmer John is trying to hire contractors to help rearrange his farm, but so far all of them have quit when they saw the complicated sequence of instructions FJ wanted them to follow.  Left to complete the project by himself, he realizes that indeed, he has made the project perhaps more  complicated than necessary.  Please help him follow his instructions to  complete the farm upgrade.

FJ's farm consists of $N$ fields in a row, conveniently numbered $1 \ldots N$. In each field there can be any number of haybales.  Farmer John's instructions contain three types of entries:

1) Given a contiguous interval of fields, add a new haybale to each field.

2) Given a contiguous interval of fields, determine the minimum number of haybales in a field within that interval.

3) Given a contiguous interval of fields, count the total number of haybales  inside that interval.

## 输入输出样例 #1

### 输入 #1

```
4 5
3 1 2 4
M 3 4
S 1 3
P 2 3 1
M 3 4
S 1 3
```

### 输出 #1

```
2
6
3
8
```

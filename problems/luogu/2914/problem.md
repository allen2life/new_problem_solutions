# P2914 [USACO08OCT] Power Failure G
## 题目描述

A vicious thunderstorm has destroyed some of the wires of the farm's electrical power grid! Farmer John has a map of all $N$ ($2\le N \le 1000$) of the powerpoles, which are conveniently numbered $1\ldots N$ and located on integer plane coordinates $(x_i,y_i)$ ($-100000 \le x_i \le 100000, -100000 \le y_i \le 100000$).

Some $W$ ($1 \le W \le 10000$) power wires connect pairs of power poles $P_i$ and $P_j$ ($1 \le Pi \le N, 1 \le Pj \le N$).

He needs to get power from pole $1$ to pole $N$ (which means that some series of wires can traverse from pole $1$ to pole $N$, probably through some intermediate set of poles).

Given the locations of the $N$ poles and the list of remaining power wires, determine the minimum length of power wire required to restore the electrical connection so that electricity can flow from pole $1$ to pole $N$.  No wire can be longer than some real number $M$ ($0.0 < M \le 200000.0$).

As an example, below on the left is a map of the $9$ poles and $3$ wires after the storm. For this task, $M = 2.0$. The best set of wires to add would connect poles $4$ and $6$ and also poles $6$ and $9$.

```cpp
   After the storm              Optimally reconnected
3  . . . 7 9 . . . . .          3  . . . 7 9 . . . . .
                                          /
2  . . 5 6 . . . . . .          2  . . 5 6 . . . . . .
                                        /
1  2-3-4 . 8 . . . . .          1  2-3-4 . 8 . . . . .
   |                               |
0  1 . . . . . . . . .          0  1 . . . . . . . . .

   0 1 2 3 4 5 6 7 8 9             0 1 2 3 4 5 6 7 8 9
```

The total length is then $1.414213562 + 1.414213562 = 2.828427124$.

POINTS: 350

## 输入输出样例 #1

### 输入 #1

```
9 3 
2.0 
0 0 
0 1 
1 1 
2 1 
2 2 
3 2 
3 3 
4 1 
4 3 
1 2 
2 3 
3 4
```

### 输出 #1

```
2828
```

## 说明/提示

Just as in the diagram above.


As above.

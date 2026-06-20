# P3879 [TJOI2010] 阅读理解
## 题目描述

英语老师留了 $N$ 篇阅读理解作业，但是每篇英文短文都有很多生词需要查字典，为了节约时间，现在要做个统计，算一算某些生词都在哪几篇短文中出现过。

## 输入输出样例 #1

### 输入 #1

```
3
9 you are a good boy ha ha o yeah
13 o my god you like bleach naruto one piece and so do i
11 but i do not think you will get all the points
5
you
i
o
all
naruto
```

### 输出 #1

```
1 2 3
2 3
1 2
3
2
```

## 说明/提示

对于 $30\%$ 的数据， $1\le M\le 10^3$ 。

对于 $100\%$ 的数据，$1\le M\le 10^4$，$1\le N\le 10^3$ 。

每篇短文长度（含相邻单词之间的空格）$\le 5\times 10^3$ 字符，每个单词长度 $\le 20$ 字符。

感谢@钟梓俊添加的一组数据。

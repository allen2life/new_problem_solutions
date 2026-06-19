# P1619 解一元二次方程的烦恼
## 题目背景

JosephZheng 在写数学作业的预习。他往往使用 Casio 来帮忙解一元二次方程。但是 Casio 有一个问题，就是当 $\Delta=b^2-4ac$ 为一个大素数或大合数时，其开平方的结果会以小数显示，而不是老师要求的二次根式形式。JosephZheng 很是苦恼，一遇到这种情况就要手动解方程。一天他再也忍不住了，于是打开了电脑，编了一个 prime 程序……于是悲剧的 OIer 们就要跟着疯狂的 JosephZheng 一起编这个程序，呵呵……

## 题目描述

废话少说，给你一个大数 $N$（可能大于 $4 \times 10^7$），让你进行素性判断，然后分解质因数。当然，初中数学题不可能有大于 $4 \times 10^7$ 的数让你判断素性，因此超过范围的数可以忽略不计。为了让程序更加贴心，JosephZheng 多了一些要求，会在输入输出中给出具体情况。

## 输入输出样例 #1

### 输入 #1

```
4
eed
```

### 输出 #1

```
Enter the number=
Prime? No!
4=2^2

Enter the number=
```

## 输入输出样例 #2

### 输入 #2

```
2
end
```

### 输出 #2

```
Enter the number=
Prime? Yes!

Enter the number=
```

## 输入输出样例 #3

### 输入 #3

```
-1
adfs
```

### 输出 #3

```
Enter the number=
Prime? No!

Enter the number=
```

## 输入输出样例 #4

### 输入 #4

```
1234###24#@13#@￥！1
hehe
```

### 输出 #4

```
Enter the number=
Prime? No!
The number is too large!

Enter the number=
```

## 输入输出样例 #5

### 输入 #5

```
1.5
1
1234324123512343123
@~@~@~@
```

### 输出 #5

```
Enter the number=
Prime? No!
15=3^1*5^1

Enter the number=
Prime? No!

Enter the number=
Prime? No!
The number is too large!

Enter the number=
```

## 输入输出样例 #6

### 输入 #6

```
12
halt@@
```

### 输出 #6

```
Enter the number=
Prime? No!
12=2^2*3^1

Enter the number=
```

## 说明/提示

编这道题的 JosephZheng 有些无聊，但是很考验基本功哦！仔细审题！

水题一道。。。

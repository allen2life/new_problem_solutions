# P6893 [ICPC 2014 WF] Buffed Buffet
## 题目描述

You are buying lunch at a buffet. A number of different dishes are available, and you can mix and match them to your heart’s desire. Some of the dishes, such as dumplings and roasted potatoes, consist of pieces of roughly equal size, and you can pick an integral number of such pieces (no splitting is allowed). Refer to these as “discrete dishes.” Other dishes, such as tzatziki or mashed potatoes, are fluid and you can pick an arbitrary real-valued amount of them. Refer to this second type as “continuous dishes.”

Of course, you like some of the dishes more than others, but how much you like a dish also depends on how much of it you have already eaten. For instance, even if you generally prefer dumplings to potatoes, you might prefer a potato over a dumpling if you have already eaten ten dumplings. To model this, each dish $i$ has an initial tastiness $t_ i$, and a rate of decay of the tastiness $\Delta t_ i$. For discrete dishes, the tastiness you experience when eating the $n^{th}$ item of the dish is $t_ i - (n-1)\Delta t_ i$. For continuous dishes, the tastiness you experience when eating an infinitesimal amount $d x$ grams of the dish after already having eaten $x$ grams is $(t_ i - x \Delta t_ i) d x$. In other words, the respective total amounts of tastiness you experience when eating $N$ items of a discrete dish or $X$ grams of a continuous dish are as follows:

$$\begin{aligned} \sum _{n=1}^{N} (t_ i - (n-1)\Delta t_ i) & &  \text {and} & & \int _{0}^ X (t_ i - x\Delta t_ i) dx  \end{aligned} $$

For simplicity, do not take into account that different dishes may or may not go well together, so define the total tastiness that you experience from a meal as the sum of the total tastinesses of the individual dishes in the meal (and the same goes for the weight of a meal – there are no food antiparticles in the buffet!).

You have spent days of painstaking research determining the numbers $t_ i$ and $\Delta t_ i$ for each of the dishes in the buffet. All that remains is to compute the maximum possible total tastiness that can be achieved in a meal of weight $w$. Better hurry up, lunch is going to be served soon!

## 输入输出样例 #1

### 输入 #1

```
2 15
D 4 10 1
C 6 1
```

### 输出 #1

```
40.500000000
```

## 输入输出样例 #2

### 输入 #2

```
3 15
D 4 10 1
C 6 1
C 9 3
```

### 输出 #2

```
49.000000000
```

## 输入输出样例 #3

### 输入 #3

```
2 19
D 4 5 1
D 6 3 2
```

### 输出 #3

```
impossible
```

## 说明/提示

Time limit: 3000 ms, Memory limit: 1048576 kB. 

 International Collegiate Programming Contest (ACM-ICPC) World Finals 2014

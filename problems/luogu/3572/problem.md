# P3572 [POI 2014] PTA-Little Bird
## 题目描述

In the Byteotian Line Forest there are $n$ trees in a row.

On top of the first one, there is a little bird who would like to fly over to the top of the last tree.

Being in fact very little, the bird might lack the strength to fly there without any stop.

If the bird is sitting on top of the tree no. i, then in a single flight leg it can fly toany of the trees no. $i+1,i+2,\cdots,i+k$, and then has to rest afterward.

Moreover, flying up is far harder to flying down.  A flight leg is tiresome if it ends in a tree at leastas high as the one where is started.  Otherwise the flight leg is not tiresome.

The goal is to select the trees on which the little bird will land so that the overall flight is leasttiresome, i.e., it has the minimum number of tiresome legs.

We note that birds are social creatures, and our bird has a few bird-friends who would also like to getfrom the first tree to the last one.  The stamina of all the birds varies,so the bird's friends may have different values of the parameter $k$.

Help all the birds, little and big!

## 输入输出样例 #1

### 输入 #1

```
9
4 6 3 6 3 7 2 6 5
2
2
5
```

### 输出 #1

```
2
1
```

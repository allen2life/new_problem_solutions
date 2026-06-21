# P1127 词链
## 题目描述

如果单词 $X$ 的末字母与单词 $Y$ 的首字母相同，则 $X$ 与 $Y$ 可以相连成 $X.Y$。（注意：$X$、$Y$ 之间是英文的句号 `.`）。例如，单词 `dog` 与单词 `gopher`，则 `dog` 与 `gopher` 可以相连成 `dog.gopher`。

另外还有一些例子：
- `dog.gopher`
- `gopher.rat`
- `rat.tiger`
- `aloha.aloha`
- `arachnid.dog`

连接成的词可以与其他单词相连，组成更长的词链，例如：

`aloha.arachnid.dog.gopher.rat.tiger`

注意到，`.` 两边的字母一定是相同的。

现在给你一些单词，请你找到字典序最小的词链，使得每个单词在词链中出现且仅出现一次。注意，相同的单词若出现了 $k$ 次就需要输出 $k$ 次。

## 输入输出样例 #1

### 输入 #1

```
6
aloha
arachnid
dog
gopher
rat
tiger
```

### 输出 #1

```
aloha.arachnid.dog.gopher.rat.tiger
```

## 说明/提示

- 对于 $40\%$ 的数据，有 $n \leq 10$；
- 对于 $100\%$ 的数据，有 $n \leq 1000$。

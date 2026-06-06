# input2dot.py

位置：

```text
scripts/problem-tools/input2dot.py
```

作用：把边列表转换成 Graphviz dot 文本，用于可视化图或树。

安装后命令名：

```text
input2dot.py
```

## 输入格式

每行一条边：

```text
1 2
2 3 10
```

- 两列：无权边。
- 三列及以上：第三列作为边权标签。

## 基本用法

无向图：

```bash
cat edges.txt | input2dot.py > graph.dot
```

有向图：

```bash
cat edges.txt | input2dot.py -d > graph.dot
```

如果输入第一行是 `n m`，通常需要跳过：

```bash
tail -n +2 in | input2dot.py > graph.dot
```

## 参数

- `-d, --directed`：输出有向图，使用 `digraph` 和 `->`。

## 配合 dot2png.py

```bash
tail -n +2 in | input2dot.py | dot2png.py -o graph.png
```


# dot2png.py

位置：

```text
scripts/problem-tools/dot2png.py
```

作用：把 Graphviz dot 内容或 `.dot` 文件转换为 PNG 图片。

安装后命令名：

```text
dot2png.py
```

依赖：

```text
Graphviz 的 dot 命令
```

## 管道模式

```bash
cat graph.dot | dot2png.py -o graph.png
```

配合 `input2dot.py`：

```bash
tail -n +2 in | input2dot.py | dot2png.py -o graph.png
```

## 文件模式

转换当前目录下的所有 `.dot` 文件：

```bash
dot2png.py
```

转换指定目录：

```bash
dot2png.py ./dots
```

指定输出目录：

```bash
dot2png.py ./dots -O ./images
```

## 参数

- `input_path`：文件模式下的 dot 文件目录，默认当前目录。
- `-o, --output`：管道模式下的输出 PNG 文件，默认 `output.png`。
- `-O, --output_path`：文件模式下的输出目录，默认当前目录。


# one-duipai.py

位置：

```text
scripts/problem-tools/one-duipai.py
```

作用：针对一组固定输入，同时运行两个程序，并用并排 diff 展示输出差异。

安装后命令名：

```text
one-duipai.py
```

## 基本用法

```bash
one-duipai.py -o 1.out -r std.out -i in
```

脚本会：

1. 打印输入文件内容。
2. 执行 `./1.out < in > 1.out` 形式的用户程序输出。
3. 执行 `./std.out < in > 2.out` 形式的标准程序输出。
4. 使用 `diff -y` 并排显示差异。

## 参数

- `-o, --org`：原始程序，默认 `1`。
- `-r, --right`：正确程序，默认 `2`。
- `-i, --in`：输入文件，默认 `INPUT`。
- `-w, --width`：并排 diff 宽度，默认 `50`。
- `-v, --verbose`：保留参数，当前脚本未使用额外详细输出。

## 示例

```bash
one-duipai.py -o 1.out -r std.out -i in1 -w 100
```

注意：`--org` 和 `--right` 需要传可执行文件名，脚本内部会用 `./程序名` 执行。


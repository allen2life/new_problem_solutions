# randint.py

位置：

```text
scripts/problem-tools/randint.py
```

作用：生成一行随机整数，适合临时构造小输入。

安装后命令名：

```text
randint.py
```

## 基本用法

生成 5 个 `[1, 10]` 内的随机整数：

```bash
randint.py
```

生成 20 个 `[100, 999]` 内的随机整数：

```bash
randint.py 20 -min 100 -max 999
```

输出示例：

```text
123 456 789 234 567
```

## 参数

- `numCount`：输出整数个数，默认 `5`。
- `-min, --Min`：最小值，默认 `1`。
- `-max, --Max`：最大值，默认 `10`。

注意：这个脚本只输出一行数字，不会自动输出 `n`。


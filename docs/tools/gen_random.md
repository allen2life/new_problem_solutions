# gen_random.py

位置：

```text
scripts/problem-analysis-tools/gen_random.py
```

作用：生成常见随机测试数据，给手写 `gen.py` 或对拍使用。

## 基本用法

```bash
python3 scripts/problem-analysis-tools/gen_random.py --pattern array -n 10 --min 1 --max 100
python3 scripts/problem-analysis-tools/gen_random.py --pattern tree -n 20
python3 scripts/problem-analysis-tools/gen_random.py --pattern graph -n 10 -m 15
python3 scripts/problem-analysis-tools/gen_random.py --pattern string -n 12 --charset abc
python3 scripts/problem-analysis-tools/gen_random.py --pattern permutation -n 10
```

## 支持类型

- `array`
- `tree`
- `graph`
- `string`
- `permutation`

## 常用参数

- `-n`：元素数、节点数或字符串长度。
- `-m`：图边数。
- `--min` / `--max`：随机数范围。
- `--distinct`：数组元素不重复。
- `--directed`：生成有向图。
- `--self-loops`：允许自环。
- `--multi-edges`：允许重边。
- `--seed`：固定随机种子。
- `--no-header`：不输出默认的 `n` 或 `n m` 头部。

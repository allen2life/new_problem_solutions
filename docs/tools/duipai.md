# duipai.py

位置：

```text
scripts/problem-analysis-tools/duipai.py
```

作用：非交互式对拍工具，适合 Agent 和自动化调用。

## 基本用法

```bash
python3 scripts/problem-analysis-tools/duipai.py \
  --gen problems/luogu/1001/gen.py \
  --user problems/luogu/1001/main.cpp \
  --brute problems/luogu/1001/brute.cpp \
  -n 200
```

## 默认约定

- `main.cpp`：待验证的正式解法。
- `brute.cpp`：朴素正确解。
- `gen.py`：当前题目的随机数据生成器。

脚本会自动编译 `.cpp`，Python 文件用 `python3` 运行。

## 输出位置

失败样例默认保存到：

```text
problems/<oj>/<problem_id>/duipai-failed/
```

对拍报告默认写到：

```text
problems/<oj>/<problem_id>/problem-analysis-workspace/duipai-report.md
```

## 常用参数

- `-n, --count`：对拍次数。
- `--timeout`：单次运行超时时间。
- `--report`：指定报告路径。
- `--failed-dir`：指定失败样例目录。
- `--strict`：严格逐字节比较输出。

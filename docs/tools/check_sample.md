# check_sample.py

位置：

```text
scripts/problem-analysis-tools/check_sample.py
```

作用：编译并运行题目目录中的样例和本地数据，自动 diff 输出。

## 基本用法

在题目目录中直接运行：

```bash
python3 ../../../scripts/problem-analysis-tools/check_sample.py
```

从项目根目录指定题目目录：

```bash
python3 scripts/problem-analysis-tools/check_sample.py problems/luogu/1001
```

指定源文件和超时时间：

```bash
python3 scripts/problem-analysis-tools/check_sample.py problems/luogu/1001 --source main.cpp --timeout 2
```

## 默认规则

- 无参数时使用当前工作目录。
- 默认先找 `main.cpp`，没有则回退到 `1.cpp`。
- C++ 编译产物放在 `/tmp/problem-analysis-sample/`。
- `.py` 源文件用 `python3` 运行。

## 数据识别

支持：

```text
in/out
in1/out1
in2/out2
data/*.in + data/*.out
data/*.in + data/*.ans
```

如果只有输入没有答案，会运行程序并标记为 `NO_ANSWER`。

## 退出码

- `0`：没有失败样例。
- `1`：存在 diff 失败、运行错误或超时。
- `2`：准备阶段失败，例如找不到目录、源文件或样例数据。

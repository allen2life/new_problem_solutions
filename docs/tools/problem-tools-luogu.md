# luogu.py

位置：

```text
scripts/problem-tools/luogu.py
```

作用：下载洛谷题目的样例输入输出，写入当前目录。

安装后命令名：

```text
luogu.py
```

## 基本用法

显式指定题号：

```bash
luogu.py P1001
luogu.py 1001
luogu.py B3634
```

不传参数时，脚本会交互询问题号；如果安装了 `gum`，默认值会使用当前目录名。

## 输出文件

脚本会写入：

```text
in1
out1
in2
out2
...
```

如果当前目录不存在 `in`，下载第一组样例时会额外写入：

```text
in
```

这样可以直接配合 `b 1` 使用。

## 实现说明

脚本优先用 Python `urllib` 请求洛谷页面，解析 `lentille-context` 中的题目数据；失败时会回退到 `curl`。

如果结构化数据里没有样例，脚本会尝试从 HTML 中直接提取样例输入输出。

## 注意事项

- 需要网络访问洛谷。
- 洛谷页面结构变化时，解析可能失败。
- 已存在的 `in1/out1` 会被覆盖。


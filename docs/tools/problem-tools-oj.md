# oj

位置：

```text
scripts/problem-tools/oj.js
```

作用：包装旧版在线题目抓取入口 `old_scripts/online_judge/index.js`。

新题建议优先使用新版 Python 工具：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001
```

说明见：

```text
docs/tools/fetch_problem.md
```

安装后命令名：

```text
oj
```

## 基本用法

```bash
oj --help
```

`--help` 只显示本 wrapper 的说明，不会进入题面下载询问。

运行时脚本会询问：

```text
是否下载对应的题面到 problem.md? [y/N]
```

如果回答 `y`、`yes`、`是`、`是的`、`好` 或 `下载`，脚本会在调用旧入口时追加：

```text
--download-statement
```

## 关系

实际抓题能力由下面的旧脚本提供：

```text
old_scripts/online_judge/index.js
```

更详细说明见：

```text
docs/oj-script.md
```

## 注意事项

如果旧入口不存在，`oj` 会直接报错并退出。

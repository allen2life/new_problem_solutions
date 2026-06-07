# ptool

位置：

```text
scripts/navi/ptool
```

安装后命令名：

```text
ptool
```

作用：给 navi 和人工命令行使用的统一 wrapper。它会自动定位当前 Git 仓库根目录，然后代理执行本仓库的写题工具，避免在 navi cheatsheet 中重复写长路径。

## 安装

在仓库根目录执行：

```bash
./install.sh
```

安装后会创建：

```text
~/.local/bin/ptool -> scripts/navi/ptool
```

确保 `~/.local/bin` 在 `PATH` 中：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 基本用法

运行 `scripts/problem-analysis-tools/` 下的工具：

```bash
ptool check_sample problems/luogu/1001
ptool fetch_problem luogu P1001
ptool problem_status problems/luogu/1001
```

`.py` 后缀可以省略：

```bash
ptool check_sample
ptool check_sample.py
```

在题目目录中执行工具：

```bash
ptool --cd problems/luogu/1001 duipai-human
ptool --cd problems/luogu/1001 shrink_failed
```

列出题目目录，主要给 navi 变量选择使用：

```bash
ptool list-problems
```

## 旧工具代理

运行 `scripts/problem-tools/` 下的旧工具：

```bash
ptool --cd problems/luogu/1001 old b main
ptool --cd problems/luogu/1001 old luogu P1001
ptool --cd problems/luogu/1001 old r-cgdb
```

`old` 会根据文件类型选择执行方式：

- `.py` 使用 `python3`
- `.sh` 使用 `bash`
- `.js` 使用 `node`
- 其他可执行文件直接执行

## 图工具快捷命令

```bash
ptool --cd problems/luogu/1001 graph in1 graph.png
ptool --cd problems/luogu/1001 graph-directed in1 graph.png
```

这两个命令会组合调用 `input2dot.py` 和 `dot2png.py`。

## 注意事项

- 必须在本仓库内或本仓库的子目录中运行。
- 如果当前 Git 仓库不是本项目，`ptool` 会直接报错。
- `ptool` 是 navi 的辅助入口，不替代各工具自己的 `--help`。

# Navi Cheatsheet

位置：

```text
scripts/navi/problem-tools.cheat
```

作用：给人类使用的 OJ 写题工具 cheatsheet，通过 `navi` 搜索和执行常用工具命令，减少记忆压力。

## 使用方式

不需要安装到本机 navi 目录，直接指定仓库内路径：

```bash
navi --path scripts/navi
```

带查询词：

```bash
navi --path scripts/navi --query duipai
navi --path scripts/navi --query sample
navi --path scripts/navi --query graph
```

只打印命令不执行：

```bash
navi --path scripts/navi --print
```

## 约定

cheatsheet 中的命令会通过当前 Git 仓库根目录定位脚本：

```bash
repo=$(git rev-parse --show-toplevel)
```

因此可以在项目根目录或任意题目目录中调用，只要当前位置仍在这个 Git 仓库内。

## 覆盖工具

- `new-problem.py`
- `fetch_problem.py`
- `problem_status.py`
- `check_problem.py`
- `check_sample.py`
- `data_tool.py`
- `gen_random.py`
- `duipai.py`
- `duipai-human.py`
- `shrink_failed.py`
- `b`
- `luogu.py`
- `input2dot.py`
- `dot2png.py`
- `r-lldb`
- `nvimsizer`

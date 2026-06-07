# Navi Cheatsheet

位置：

```text
scripts/navi/problem-tools.cheat
```

作用：给人类使用的 OJ 写题工具 cheatsheet，通过 `navi` 搜索和执行常用工具命令，减少记忆压力。

## 使用方式

先安装 navi 辅助 wrapper：

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

然后直接指定仓库内 cheatsheet 路径：

```bash
navi --path scripts/navi
```

cheatsheet 使用 short name 作为 navi 的 tag。界面中左侧是 short name，中间是中文说明，右侧是实际命令。例如：

```cheat
% fetch-problem
# 抓取题面和样例到新题目结构
ptool fetch_problem <oj> <problem_id>
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

cheatsheet 中的分析工具命令通过 `ptool` 定位当前 Git 仓库根目录，并代理执行：

```bash
ptool check_sample problems/luogu/1001
ptool fetch_problem luogu P1001
ptool --cd problems/luogu/1001 duipai-human
```

`ptool` 会自动查找当前所在的 Git 仓库根目录，因此可以在项目根目录或任意题目目录中调用，只要当前位置仍在这个 Git 仓库内。

常用能力：

```bash
ptool list-problems
ptool <problem-analysis-tool> [arguments...]
ptool --cd <problem_dir> <problem-analysis-tool> [arguments...]
ptool --cd <problem_dir> old <problem-tool> [arguments...]
```

`ptool` 专属说明见 [`ptool.md`](ptool.md)。

## 推荐样式

如果希望 navi 三列更清晰，可以把下面配置写入 `navi info config-path` 指向的文件：

```yaml
style:
  tag:
    color: green
    width_percentage: 20
    min_width: 15
  comment:
    color: cyan
    width_percentage: 30
    min_width: 20
  snippet:
    width_percentage: 50
    min_width: 30
```

## 覆盖工具

- `ptool`
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
- `r-cgdb`
- `nvimsizer`

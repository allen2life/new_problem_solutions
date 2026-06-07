# rbook-shell.zsh

位置：

```text
scripts/navi/rbook-shell.zsh
```

安装后提供的 shell 函数：

```text
fetch_problem
```

作用：给人类写题使用的 shell 函数集合。当前主要提供 `fetch_problem`，用于抓取题目后自动进入对应题目目录。

## 配置方式

在仓库目录内执行：

```bash
repo="$(git rev-parse --show-toplevel)"
cat >> ~/.zshrc <<EOF
export RBOOK_REPO="$repo"
export PATH="\$RBOOK_REPO/scripts/navi:\$RBOOK_REPO/scripts/problem-analysis-tools:\$RBOOK_REPO/scripts/problem-tools:\$PATH"
source "\$RBOOK_REPO/scripts/navi/rbook-shell.zsh"
EOF
source ~/.zshrc
```

确认函数已加载：

```bash
type fetch_problem
```

## fetch_problem

抓取 Luogu 题目：

```bash
fetch_problem luogu P1001
```

抓取题目 URL：

```bash
fetch_problem https://www.luogu.com.cn/problem/P1001
```

成功后会自动进入题目目录：

```text
problems/luogu/1001/
```

## 不会自动跳转的模式

这些模式只转发给底层 `fetch_problem.py`，不会改变当前目录：

```bash
fetch_problem --help
fetch_problem --self-test
fetch_problem luogu P1001 --dry-run
fetch_problem luogu P1001 --json
```

## 和 fetch_problem.py 的区别

`fetch_problem.py` 是普通 Python 脚本，适合 agent、脚本、CI 调用：

```bash
ptool fetch_problem luogu P1001 --json
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --json
```

普通脚本无法改变父 shell 的当前目录，所以不会自动 `cd`。

`fetch_problem` 是 shell 函数，被当前 shell `source` 后运行，可以在抓题成功后执行 `cd`，适合人类开始写新题时使用。

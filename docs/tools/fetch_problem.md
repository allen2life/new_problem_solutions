# fetch_problem.py

位置：

```text
scripts/problem-analysis-tools/fetch_problem.py
```

作用：把在线 OJ 题目抓取到当前电子书的新题目目录结构中。

## 基本用法

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001
python3 scripts/problem-analysis-tools/fetch_problem.py https://www.luogu.com.cn/problem/P1001
```

脚本默认会创建或补齐题目目录，不需要额外传 `--init`：

```text
problems/<oj>/<problem_id>/
├── index.md
├── problem.md
├── main.cpp
├── brute.cpp
├── gen.py
├── in1
├── out1
└── problem-analysis-workspace/
```

Luogu 目录名沿用旧规则：

```text
luogu P1001 -> problems/luogu/1001/
```

但 `index.md` 中的 `problem_id` 仍然写 `P1001`。

## 支持能力

第一版支持：

- Luogu：抓取标题、题面 `problem.md`、样例 `in1/out1`，并生成 `in`。
- Codeforces：支持 `165E` 和常见 URL 解析，创建 skeleton，暂不抓完整题面和样例。
- VJudge：支持 `poj/hdu/atcoder/openj_bailian` 等旧入口能力，尽量抓标题，暂不抓完整题面和样例。

`problem.md` 只作为原题面归档，不写题解、不套题解格式、不包含 `@include-code`。

## 覆盖策略

默认不覆盖手写文件：

```text
index.md
main.cpp
brute.cpp
gen.py
problem-analysis-workspace/*.md
```

默认也不覆盖已经存在的抓取产物：

```text
problem.md
in1/out1
in2/out2
in
```

需要重新写抓取产物时使用：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --force-statement
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --force-samples
```

只更新 `index.md` frontmatter 里的 `title/source`，不修改正文：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --force-index-meta
```

## 预览和 JSON

只预览将要写入的路径：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --dry-run
```

给 agent 或脚本使用结构化输出：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --json
```

JSON 会包含：

```text
ok
fetched
oj
problem_id
problem_dir
created
skipped
written
warnings
```

## 抓取失败行为

如果已经能确定 OJ 和题号，例如：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001
```

即使网络失败，也会创建或补齐 skeleton，并在输出里提示题面/样例抓取失败。

如果输入 URL 无法识别 OJ 或题号，脚本直接失败，不创建目录。

## 自测

运行离线 fixture 自测：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py --self-test
```

自测会使用 Luogu fixture，在临时目录中验证解析、建目录和写入 `problem.md/in1/out1`，不会修改真实 `problems/`。

## 第一版未实现

- Codeforces 完整题面抓取。
- Codeforces 样例抓取。
- VJudge 代理页面里的完整题面抓取。
- VJudge 代理页面里的样例抓取。
- 各 OJ 的登录态、Cookie、反爬失败重试。
- AtCoder 原站题面抓取。
- POJ/HDU 原站题面抓取。
- 题目标签、时间限制、内存限制的跨 OJ 统一解析。

旧 `scripts/problem-tools/oj.js` 第一版暂不修改。新题建议优先使用 `fetch_problem.py`。

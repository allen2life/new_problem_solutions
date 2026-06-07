# scripts 工具升级 TODO

目标：围绕“持续手写题目、阅读题目、提升 OJ 写题能力”，把 `scripts/` 下的工具整理成稳定、可复用、适合 Agent 和人工同时使用的写题闭环。

当前已有能力：

- `scripts/problem-analysis-tools/`：新结构工具，包含建题、查规范、样例检查、随机数据、非交互对拍、交互对拍。
- `scripts/problem-tools/`：旧版个人写题辅助工具，包含编译运行、下载样例、批量测试、对拍、图可视化、调试和上传辅助。
- `scripts/` 根部：项目维护脚本，例如安装工具、生成题目 JSON、部署 VPS。

## P0

### [ ] 1. 新增 `problem_status.py` 总控工具

目的：在当前题目目录一条命令查看“这道题现在还缺什么”。

建议位置：

```text
scripts/problem-analysis-tools/problem_status.py
```

建议能力：

- 默认检查当前工作目录。
- 支持从项目根目录指定题目目录。
- 调用或复用 `check_problem.py` 的规范检查。
- 检查 `main.cpp`、`brute.cpp`、`gen.py` 是否存在。
- 检查是否存在 `problem-analysis-workspace/`。
- 检查是否存在样例数据。
- 可选运行 `check_sample.py`。
- 输出下一步建议，例如“先下载样例”“先写 brute.cpp”“可以开始对拍”。

示例：

```bash
python3 scripts/problem-analysis-tools/problem_status.py problems/luogu/1001
cd problems/luogu/1001
python3 ../../../scripts/problem-analysis-tools/problem_status.py
```

### [ ] 2. 新增对拍失败样例缩小工具

目的：`duipai.py` 发现 WA 后，自动尝试把失败输入缩小成更容易观察的反例。

建议位置：

```text
scripts/problem-analysis-tools/shrink_failed.py
```

建议能力：

- 读取 `duipai-failed/input.txt`。
- 支持数组类输入的长度缩小。
- 支持数值范围缩小。
- 支持删除部分边、查询或行。
- 每次缩小后重新运行 user/brute，保留仍然失败的输入。
- 输出 `duipai-failed/input.shrunk.txt` 和缩小报告。

注意：第一版不需要解决所有输入格式，可以先支持“第一行 n，第二行数组”的常见结构。

### [ ] 3. 给 `duipai.py` 增加资源限制和 checker 支持

目的：让对拍能力接近真实 OJ，并支持非标准输出比较。

建议修改：

```text
scripts/problem-analysis-tools/duipai.py
```

建议能力：

- `--memory-mb`
- `--memory-guard-mb`
- `--checker checker.py`
- `--eps 1e-6`
- 保存每次失败的 return code、stderr、耗时、峰值内存。
- 失败报告中记录 seed、命令、资源限制。

实现建议：

- 抽出 `check_sample.py` 里的受限运行逻辑，避免重复维护。
- 状态优先级可以沿用：`TIMEOUT > MEMORY_LIMIT > RUNTIME_ERROR > WRONG_ANSWER > PASS`。

### [ ] 4. 新增样例/本地数据整理工具

目的：统一管理 `in/out`、`in1/out1`、`data/*.in`、`data/*.out/.ans`，减少手动搬数据。

建议位置：

```text
scripts/problem-analysis-tools/data_tool.py
```

建议子命令：

```bash
data_tool.py list problems/luogu/1001
data_tool.py normalize problems/luogu/1001
data_tool.py add problems/luogu/1001 --input in3 --answer out3
data_tool.py copy-samples-to-data problems/luogu/1001
```

建议能力：

- 列出当前题目的全部输入/答案配对。
- 检查缺答案、孤立输出、命名冲突。
- 把根目录样例复制到 `data/`。
- 可选把 CRLF 统一为 LF。

## P1

### [ ] 5. 增强 `gen_random.py` 的常见数据模板

目的：减少每道题重复写简单随机生成器的时间。

建议新增 pattern：

- `matrix`
- `grid`
- `weighted-tree`
- `weighted-graph`
- `dag`
- `intervals`
- `queries`
- `brackets`
- `parent-array`
- `functional-graph`
- `bitmask`

建议新增 edge case 模式：

- 全相等
- 递增
- 递减
- 最小值
- 最大值
- 稀疏图
- 稠密图
- 链
- 星

### [ ] 6. 新增现代化题目抓取工具

目的：替代或整合旧版 `problem-tools/luogu.py` 和 `problem-tools/oj.js`。

建议位置：

```text
scripts/problem-analysis-tools/fetch_problem.py
```

建议能力：

- 支持 `luogu P1001`。
- 自动写入 `problem.md`。
- 自动写入 `in1/out1`。
- 自动填充 `index.md` 的 `title` 和 `source`。
- 可选和 `new-problem.py` 合并使用。

示例：

```bash
python3 scripts/problem-analysis-tools/fetch_problem.py luogu P1001 --init
```

### [ ] 7. 新增批量题目规范审计工具

目的：维护整本题解电子书质量。

建议位置：

```text
scripts/problem-analysis-tools/check_all_problems.py
```

建议能力：

- 遍历 `problems/<oj>/<problem_id>/`。
- 对每个目录运行或复用 `check_problem.py`。
- 汇总错误和警告。
- 支持只输出失败项。
- 支持生成 Markdown 报告。

示例：

```bash
python3 scripts/problem-analysis-tools/check_all_problems.py
python3 scripts/problem-analysis-tools/check_all_problems.py --report reports/problem-audit.md
```

## P2

### [ ] 8. 逐步迁移旧版 `problem-tools`

目的：保留个人快捷工具，但让核心逻辑进入新结构。

建议：

- `b` 保留为个人快捷命令。
- `luogu.py` 的抓样例能力迁移到 `fetch_problem.py`。
- `test-data.py` 的数据发现能力迁移到 `data_tool.py`。
- `duipai.py` 旧版保留文档，但推荐使用新版 `problem-analysis-tools/duipai.py`。
- `input2dot.py` / `dot2png.py` 可以继续保留，后续可增加 `graph_tool.py` 包装。

### [ ] 9. 抽离公共工具库

目的：减少脚本之间重复代码，方便维护。

建议位置：

```text
scripts/problem_analysis_lib/
```

建议模块：

- `compiler.py`：编译 C++、缓存可执行文件。
- `runner.py`：运行程序、时间限制、内存限制、收集 stderr/stdout。
- `data.py`：发现样例和本地数据。
- `compare.py`：输出标准化、diff、checker、EPS。
- `paths.py`：仓库路径、题目目录推断、相对路径显示。

### [ ] 10. 给 CLI 工具补测试

目的：避免脚本升级时破坏日常写题流程。

建议：

- 使用 pytest 或 Node test 调用 Python CLI。
- 给 `check_sample.py` 建临时题目目录测试。
- 给 `duipai.py` 测试 PASS、WA、TLE。
- 给 `gen_random.py` 测试不同 pattern 的输出格式。
- 给 `new-problem.py` 测试不会覆盖已有文件。

## 备注

- 当前优先实现 P0，尤其是 `problem_status.py` 和 `shrink_failed.py`。
- `.gitignore` 和 `work2_.md` 是当前工作区已有无关改动，不属于本 TODO。


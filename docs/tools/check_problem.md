# check_problem.py

位置：

```text
scripts/problem-analysis-tools/check_problem.py
```

作用：检查单个题目目录是否符合当前电子书题目结构规范。

## 基本用法

```bash
python3 scripts/problem-analysis-tools/check_problem.py problems/luogu/1001
```

## 检查内容

- 是否位于 `problems/<oj>/<problem_id>/`。
- 是否存在 `index.md`。
- 是否存在 `main.cpp`。
- frontmatter 是否包含必要字段。
- frontmatter 是否包含 `description`；缺失为错误，存在但为空为警告。
- `index.md` 是否使用 `@include-code(./main.cpp, cpp)`。
- `problem-analysis-workspace/` 或 `duipai-failed/` 是否有已被 Git 跟踪的文件。
- 是否存在旧结构残留，例如有 `1.cpp` 但没有 `main.cpp`。

## 退出码

- `0`：没有错误。
- `1`：题目目录不符合规范。

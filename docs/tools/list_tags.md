# list_tags.py

位置：

```text
scripts/problem-analysis-tools/list_tags.py
```

作用：统计所有题目解析 `index.md` frontmatter 中已经使用过的 `tags`，辅助写新题解时复用统一标签。

## 基本用法

按使用次数输出：

```bash
python3 scripts/problem-analysis-tools/list_tags.py
```

只输出 tag 名称，每行一个：

```bash
python3 scripts/problem-analysis-tools/list_tags.py --format plain
```

输出 JSON，包含使用该 tag 的题目：

```bash
python3 scripts/problem-analysis-tools/list_tags.py --format json
```

输出 tag、数量和对应题目：

```bash
python3 scripts/problem-analysis-tools/list_tags.py --with-problems
```

如果已经配置 `ptool`：

```bash
ptool list_tags
ptool list_tags --format plain
ptool list_tags --format json
```

## 使用场景

- 写新题解前查看已有标签，避免创建同义不同名的 tag。
- 更新 `index.md` frontmatter 时，从已有 tag 中优先挑选准确标签。
- 需要新增 tag 时，先确认当前集合里没有更合适的旧 tag。

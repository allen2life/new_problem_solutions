---
name: oj-problem-format-spec
description: Standardize the writing format and Markdown skeleton for this repository's Chinese OJ problem explanation ebook. Use this skill whenever the user asks about 题解格式, 题目解析格式规范, OJ article skeletons, problems/<oj>/<problem_id>/index.md, frontmatter, section titles, @include-code, or formatting existing problem notes. This skill only defines article structure and formatting; it does not write algorithm analysis or solve the problem.
---

# OJ 题目解析格式规范

这个 skill 只负责 `problems/` 下题目解析文章的写作格式和 Markdown 骨架。

它不负责：

- 推导题目解法。
- 判断算法是否正确。
- 讲解双指针、DP、图论等算法内容。
- 重写已有正文的题目解析。
- 判断 `tags` 和 `categories` 的具体算法标签是否准确。

算法解析内容由另一个题目解析 skill 填写。本 skill 只保证文章结构稳定、字段完整、代码嵌入格式统一。

## 使用 Grill-Me

如果用户要求先 `grill me`，按这个顺序一次只问一个问题，并给推荐答案：

1. 这个 skill 是否只管格式、不管解析内容？
2. 是否使用固定章节标题？
3. 是否强制最小 frontmatter 字段？
4. 是否统一使用 `@include-code(...)` 嵌入代码？
5. 空章节是否使用 HTML 注释占位？
6. 是否负责文件命名和存放路径？
7. 修改已有题解时，是强制套模板还是只修正格式？

能从本仓库已有文件判断的问题，不要问用户。

## 文件位置

只使用目录型题目结构。新建题解放在：

```text
problems/<oj>/<problem_id>/index.md
```

对应代码固定为：

```text
problems/<oj>/<problem_id>/main.cpp
```

示例：

```text
problems/luogu/1001/index.md
problems/luogu/1001/main.cpp
```

过程文档目录为：

```text
problems/<oj>/<problem_id>/problem-analysis-workspace/
```

不要新建或输出旧扁平结构，例如 `problems/poj/poj3061.md` 和 `problems/poj/poj3061.cpp`。

## Frontmatter

每篇题解 Markdown 必须以 YAML frontmatter 开头。

字段顺序固定为：

```yaml
---
oj: "poj"
problem_id: "3061"
title: "Subsequence"
date: 2025-11-28 15:41
toc: true
tags: []
categories: []
source: https://vjudge.net/problem/POJ-3061
---
```

字段规则：

- `oj`：小写 OJ 名称，通常来自目录名。
- `problem_id`：字符串格式。
- `title`：题目标题；不知道时使用空字符串，不编造。
- `date`：新建文章使用当前本地时间；修改旧文时保留原日期。
- `toc`：固定为 `true`。
- `tags`：数组格式；本 skill 不负责填具体算法标签。
- `categories`：数组格式；本 skill 不负责填具体分类。
- `source`：题目来源；不知道时留空，不编造。

修改已有文件时：

- 保留已有有效字段值。
- 补齐缺失字段。
- 按标准顺序整理字段。
- 不因为不知道内容而删除原有字段值。

## 固定章节

frontmatter 后必须有：

```markdown
[[TOC]]
```

正文固定使用这些三级标题：

```markdown
### 题意

### 思路

### 代码

### 复杂度

### 总结
```

不要在题解正文中添加一级标题或二级标题。题目标题由 frontmatter 的 `title` 提供。

## 占位注释

如果某个章节暂时没有正文，保留章节，并使用 HTML 注释占位：

```markdown
<!-- 由题目解析 skill 填写 -->
```

占位注释用于多 skill 协作，不会显示在电子书正文中。

不要使用可见文本占位，例如：

```markdown
待补充
TODO
这里写思路
```

## 代码嵌入

代码章节统一使用：

```markdown
@include-code(./main.cpp, cpp)
```

规则：

- 路径必须相对当前 Markdown 文件。
- 固定引用同目录 `main.cpp`。
- 不在 Markdown 中粘贴完整代码。
- 如果暂时没有代码文件，保留代码章节，并使用 HTML 注释说明：

```markdown
<!-- 缺少对应代码文件 -->
```

## 新建文章模板

新建题解骨架时，直接使用这个模板：

```markdown
---
oj: ""
problem_id: ""
title: ""
date: YYYY-MM-DD HH:mm
toc: true
tags: []
categories: []
source:
---

[[TOC]]

### 题意

<!-- 由题目解析 skill 填写 -->

### 思路

<!-- 由题目解析 skill 填写 -->

### 代码

@include-code(./main.cpp, cpp)

### 复杂度

<!-- 由题目解析 skill 填写 -->

### 总结

<!-- 由题目解析 skill 填写 -->
```

填充模板时，只填能从文件名、路径、已有元数据或用户明确输入中确定的字段。不要为补全模板而编造信息。

## 修改已有题解

修改已有题解时，只修正格式问题，尽量保留已有正文。

可以做：

- 补齐 frontmatter。
- 调整 frontmatter 字段顺序。
- 补上 `[[TOC]]`。
- 将明显的章节标题统一为固定标题。
- 补缺失章节。
- 将完整代码块替换为 `@include-code(...)`，前提是对应代码文件存在。
- 为缺失内容添加 HTML 注释占位。

不要做：

- 重写算法思路。
- 删除已有题目解析正文。
- 改变正文中的算法结论。
- 重新判断复杂度。
- 修改 `tags`、`categories` 的具体内容，除非用户明确要求或只是整理数组格式。
- 强制把已有可读正文改成模板化空骨架。

## 输出检查清单

交付前检查：

- Markdown 文件位于 `problems/<oj>/<problem_id>/index.md`。
- frontmatter 在文件最开头。
- frontmatter 包含 `oj`、`problem_id`、`title`、`date`、`toc`、`tags`、`categories`、`source`。
- frontmatter 字段顺序符合规范。
- frontmatter 后有 `[[TOC]]`。
- 正文包含 `### 题意`、`### 思路`、`### 代码`、`### 复杂度`、`### 总结`。
- 空章节使用 HTML 注释占位。
- 代码章节使用 `@include-code(./main.cpp, cpp)` 或缺失代码注释。
- 没有粘贴完整代码。
- 没有编造题目标题、来源、算法标签或解析内容。

## 最终回复

完成修改后，只简短说明：

- 修改了哪个文件。
- 执行的是新建骨架还是格式修正。
- 是否保留了已有正文。
- 哪些字段或代码文件仍然缺失。

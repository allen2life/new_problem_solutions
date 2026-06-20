# rbook preview

位置：

```text
bin/rbook.js
```

作用：完成单个题目的题解后，快速启动只服务这一题的预览页面，避免 `npm start` 前置的全量题库扫描。

## 基本用法

如果已经把仓库 `bin/` 加入 `PATH`：

```bash
rbook preview luogu 1001
rbook preview luogu P1001 --port 3100
```

没有配置 `PATH` 时，在仓库根目录运行：

```bash
npm run preview -- luogu 1001
```

启动后终端会输出类似：

```text
Previewing luogu P1001
Source: luogu/1001/index.md
Access URLs:
- http://127.0.0.1:3000/problems/luogu/P1001/
```

预览页使用带尾斜杠的 URL，这样题解中的 `./image.png` 会按浏览器规则解析到当前题目目录。

## 查找规则

命令格式：

```bash
rbook preview <oj> <problem_id>
```

普通 OJ 只查：

```text
problems/<oj>/<problem_id>/index.md
```

Luogu 会兼容数字 ID 和 `P` 前缀：

```text
rbook preview luogu 1001
```

会依次查：

```text
problems/luogu/1001/index.md
problems/luogu/P1001/index.md
```

如果目录存在，页面展示仍以 `index.md` frontmatter 中的 `problem_id` 为准。

## 渲染能力

预览服务复用主站的 `MarkdownRenderer` 和 `problem.pug`，支持：

- `@include-code(./main.cpp, cpp)`
- 当前题目目录下的相对图片
- `problem.md` 原题面弹窗
- Mermaid、Graphviz/dot、KaTeX、Prism 代码高亮
- 代码复制按钮、字体工具栏、主题切换
- `/api/problems/:oj/:id` 单题 JSON

预览服务只挂载当前题目目录作为静态资源，不提供首页题目列表、题单页或完整关系图。

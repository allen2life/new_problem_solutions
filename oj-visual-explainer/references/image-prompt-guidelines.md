# Image Prompt Guidelines

Use image prompts only for polished one-page teaching infographics or conceptual overview images. Prefer Mermaid/SVG for exact tables, graphs, and numeric examples.

## Prompt structure

Include:

1. Canvas: 16:9 horizontal, clean Chinese educational infographic.
2. Title: problem name and algorithm family.
3. Subtitle: one-sentence core idea.
4. Panels: 3-5 labeled modules.
5. Visual elements: arrows, tables, trees, graphs, state boxes, warning cards.
6. Style: flat vector, high contrast, readable Chinese text.
7. Accuracy instruction: keep formulas short and preserve variable names.

## Chinese prompt template

```text
生成一张 16:9 横向中文算法竞赛教学信息图。主题是「{题目名}」的解题流程。整体风格类似清晰的课堂讲义和流程图，白色背景，浅色模块卡片，蓝色表示关键观察，绿色表示主算法，橙色表示分支和特殊情况，红色表示常见坑点。

顶部标题：{标题}
副标题：{一句话核心思想}

图中包含 {模块数量} 个模块：
1. {模块1标题}：{模块1要点}
2. {模块2标题}：{模块2要点}
3. {模块3标题}：{模块3要点}
4. {模块4标题}：{模块4要点}

请使用箭头表示执行顺序，使用小表格/树/图/状态框辅助解释。保留变量名 {关键变量}，公式尽量短。中文文字要清晰、端正、可读，不要生成乱码，不要随意改变变量名，不要添加未给出的算法步骤。
```

## Negative prompt template

```text
避免：中文乱码、错误公式、过密文字、错误边权、错误 DP 表格数值、代码大段展示、照片风格、3D 渲染、装饰过多、低分辨率、伪造平台 logo。
```

## API-key safety wording

If the user asks to connect an API key, say:

- Do not put API keys in the skill package.
- Store the key as an environment variable such as `OPENAI_API_KEY`.
- Use code examples with placeholders only.
- Never ask the user to paste a secret into a public document or reusable skill file.

# tree_draw.py

位置：

```text
scripts/problem-analysis-tools/tree_draw.py
scripts/problem-analysis-tools/tree_draw/
```

作用：使用 Walker 风格布局绘制树结构 SVG，适合题解配图和调试树形数据。

第一版支持：

- 普通树边列表
- 二叉树左右孩子表
- JSON 自定义树
- 最小线段树结构图
- SVG 输出
- `--markdown` 输出可粘贴到题解里的图片片段

暂不内置 PNG 输出。网页和 Markdown 可以直接展示 SVG；如果确实需要 PNG，可用 `rsvg-convert`、ImageMagick 等外部工具转换。

## 普通树

输入 `tree.txt`：

```text
5
1 2
1 3
2 4
2 5
```

生成 SVG：

```bash
python3 scripts/problem-analysis-tools/tree_draw.py --type normal --input tree.txt --output tree.svg
```

在题目目录中使用：

```bash
ptool --cd problems/luogu/Pxxxx tree_draw --type normal --input tree.txt --output tree.svg --markdown
```

## 二叉树

输入 `binary.txt`：

```text
5
1 2 3
2 4 5
3 0 0
4 0 0
5 0 0
```

格式为：

```text
u left right
```

`0` 表示空孩子。

生成 SVG：

```bash
tree_draw.py --type binary --input binary.txt --output binary.svg
```

## JSON 自定义树

JSON 适合需要自定义节点颜色、文字、边样式的静态数据结构图。

```json
{
  "type": "binary",
  "root": "a",
  "nodes": [
    {"id": "a", "label": "8", "left": "b", "right": "c", "style": {"fill": "#fee2e2"}},
    {"id": "b", "label": "3"},
    {"id": "c", "label": "10"}
  ],
  "style": {
    "node": {"radius": 22, "fill": "#ffffff", "stroke": "#334155"},
    "edge": {"stroke": "#64748b", "width": 2},
    "font": {"size": 14}
  }
}
```

命令：

```bash
tree_draw.py --type json --input tree.json --output tree.svg
```

## 线段树

只生成区间结构图，不计算区间值。

```bash
tree_draw.py --type segment --size 8 --output segment.svg
tree_draw.py --type segment --array "1 3 5 7" --output segment.svg
```

## Markdown 片段

```bash
tree_draw.py --type binary --input binary.txt --output binary.svg --markdown --alt "二叉树示意图"
```

输出：

```markdown
![二叉树示意图](./binary.svg)
```

## 常用样式参数

```bash
tree_draw.py --type normal --input tree.txt --output tree.svg \
  --level-gap 100 \
  --sibling-gap 80 \
  --subtree-gap 48 \
  --node-radius 24 \
  --node-fill '#f8fafc' \
  --node-stroke '#2563eb'
```

## 题解写作建议

- 树题、二叉树、线段树题优先考虑用 `tree_draw.py` 生成 SVG。
- 图前说明这张图展示什么。
- 图后说明读者应该观察哪些节点、边或子树。
- 复杂数据结构如红黑树、B+ tree 第一版建议用 JSON 画静态结构，不做插入/删除过程模拟。

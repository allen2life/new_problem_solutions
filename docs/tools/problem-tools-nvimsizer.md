# nvimsizer

位置：

```text
scripts/problem-tools/nvimsizer.sh
```

作用：用 Neovim 左右分屏打开两个文件，并根据右侧文件最长行调整右侧窗口宽度。

安装后命令名：

```text
nvimsizer
```

## 基本用法

```bash
nvimsizer 1.cpp in
```

参数：

```text
nvimsizer <主文件> <侧边文件>
```

脚本会执行：

```text
nvim -O <主文件> <侧边文件>
```

然后根据 `<侧边文件>` 的最长行长度调整右侧窗口宽度。

## 适用场景

- 左边看代码，右边看样例输入。
- 左边改 `index.md`，右边参考输出或临时笔记。


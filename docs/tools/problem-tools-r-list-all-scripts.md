# r-list-all-scripts.py

位置：

```text
scripts/problem-tools/r-list-all-scripts.py
```

作用：列出 `scripts/problem-tools/` 下可用的工具脚本和简短说明。

安装后命令名：

```text
r-list-all-scripts.py
```

## 基本用法

```bash
r-list-all-scripts.py
```

查看帮助：

```bash
r-list-all-scripts.py --help
```

输出示例：

```text
可用的工具脚本:
==================================================
b                    - 快速编译C++程序，支持g++和clang++
duipai.py            - 自动化对拍工具，可进行多次测试
...
==================================================
```

## 注意事项

这个脚本的说明文本是硬编码的。如果新增工具或改名，需要同步更新 `scripts/problem-tools/r-list-all-scripts.py`。

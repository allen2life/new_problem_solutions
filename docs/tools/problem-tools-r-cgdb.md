# r-cgdb

位置：

```text
scripts/problem-tools/r-cgdb.sh
```

作用：交互式选择可执行文件和输入文件，然后快速进入 CGDB 调试。

安装后命令名：

```text
r-cgdb
```

依赖：

```text
gum
cgdb
```

## 基本用法

在题目目录中运行：

```bash
r-cgdb
```

脚本会：

1. 选择当前目录中的可执行文件。
2. 选择当前目录中文件名包含 `in` 的输入文件。
3. 生成临时 gdb 命令文件。
4. 启动 CGDB，并定义 `rr` 命令后执行：

```gdb
define rr
  run < 选中的输入文件
end
break main
rr
```

如果你已经知道可执行文件，也可以直接传入：

```bash
r-cgdb ./main.out
```

查看帮助：

```bash
r-cgdb --help
```

## 注意事项

- 只扫描当前目录一层，不递归查找。
- 输入文件筛选规则是文件名包含 `in`。
- 如果没有传入可执行文件，候选可执行文件来自有执行权限的文件或 `*.out` 文件。
- 脚本不会修改题目目录，只会创建一个临时 gdb 命令文件，退出时自动删除。

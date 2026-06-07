# r-lldb

位置：

```text
scripts/problem-tools/lldb.sh
```

作用：选择当前目录中的输入文件，并用 LLDB 启动可执行程序进行调试。

安装后命令名：

```text
r-lldb
```

依赖：

```text
gum
lldb
```

## 基本用法

```bash
r-lldb ./1.out
```

查看帮助：

```bash
r-lldb --help
```

脚本会：

1. 查找当前目录下文件名包含 `in` 的文件。
2. 用 `gum filter` 选择一个输入文件。
3. 启动 LLDB。
4. 设置 `rr` 命令为 `process launch -i <输入文件>`。

进入 LLDB 后，可以再次运行：

```text
rr
```

## 注意事项

- 必须传入可执行文件。
- 没有安装 `gum` 或 `lldb` 时会直接退出。
- 只扫描当前目录一层，不递归查找输入文件。

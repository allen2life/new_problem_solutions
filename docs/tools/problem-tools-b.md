# b

位置：

```text
scripts/problem-tools/b
```

作用：快速编译并运行当前题目目录中的 C++ 程序。适合手写题目时反复执行 `1.cpp`、`main.cpp` 这类本地代码。

安装后命令名：

```text
b
```

## 基本用法

```bash
b 1
b 1.cpp
b main
```

如果参数不带 `.cpp`，脚本会自动补成 `.cpp`。例如 `b 1` 会读取 `1.cpp`。

## 输入输出

默认读取当前目录的 `in`：

```bash
b 1
```

指定输入：

```bash
b 1 -i in1
```

指定输出：

```bash
b 1 -i in1 -o my.out
```

不使用输入文件：

```bash
b 1 -I
```

交互式选择输入文件：

```bash
b 1 -c
```

## 编译选项

只编译不运行：

```bash
b 1 -n
```

启用调试宏 `DEBUG`：

```bash
b 1 -d
```

指定 C++ 标准：

```bash
b 1 -s 17
```

添加 `FREOPEN` 宏：

```bash
b 1 -f
```

## 输出文件规则

- 普通编译输出：`1.out`
- 调试模式输出：`1_debug.out`

如果可执行文件比源码新，脚本会跳过编译直接运行。

## 常用参数

- `-i, --input-file`：指定输入文件，默认 `in`。
- `-o, --output-file`：指定输出文件。
- `-c, --choose-input`：选择包含 `in` 的输入文件。
- `-I, --no-input`：无输入运行。
- `-d, --debug`：添加 `-DDEBUG`。
- `-s, --std`：指定 C++ 标准。
- `-f, --freopen`：添加 `-DFREOPEN`。
- `-n, --norun`：只编译，不运行。
- `-v, --version`：显示版本。


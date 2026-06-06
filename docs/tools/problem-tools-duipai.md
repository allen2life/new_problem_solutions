# problem-tools/duipai.py

位置：

```text
scripts/problem-tools/duipai.py
```

作用：旧版交互式对拍工具。它会编译数据生成器、用户程序和标准程序，循环生成随机数据并比较输出。

安装后命令名：

```text
duipai.py
```

新版非交互式对拍工具见 [`duipai.py`](duipai.md)。

## 基本用法

交互式运行：

```bash
duipai.py
```

显式指定全部参数：

```bash
duipai.py -n 100 -d compare --data gen.cpp --user 1.cpp --std std.cpp
```

## 参数

- `-n, --count`：对拍次数。
- `-d, --dir`：发现错误时保存输入的目录。
- `--data`：数据生成程序源码。
- `--user`：待验证程序源码。
- `--std`：标准程序源码。

## 支持语言

- `.cpp`
- `.c`
- `.py`
- `.hs`

脚本会按需编译 C/C++/Haskell；Python 源码会生成可执行包装脚本。

## 本地文件

脚本可能在当前目录生成：

```text
duipai_config.json
```

下次运行时会询问是否加载这个配置。

对拍时临时输入输出写在：

```text
/tmp/in
/tmp/user_out
/tmp/std_out
```

发现差异后，脚本会把失败输入复制到 `--dir` 指定目录，并打开 `vimdiff` 比较两个输出。


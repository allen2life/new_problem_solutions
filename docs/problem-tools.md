# 写题工具使用手册

本文档说明 `scripts/problem-tools/` 下的写题辅助工具。它们主要用于在 `problems/<oj>/<id>/` 目录中完成日常写题流程：创建代码、下载样例、编译运行、批量测试、对拍和画图辅助。

## 1. 安装

### 1.1 安装系统依赖

Ubuntu/Debian：

```bash
sudo apt update
sudo apt install -y python3 fzf graphviz clangd curl g++ diffutils
```

可选安装 `gum`，用于更舒服的交互式选择。没有 `gum` 时，部分脚本会降级为普通输入。

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://repo.charm.sh/apt/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/charm.gpg
echo "deb [signed-by=/etc/apt/keyrings/charm.gpg] https://repo.charm.sh/apt/ * *" | sudo tee /etc/apt/sources.list.d/charm.list
sudo apt update
sudo apt install -y gum
```

### 1.2 安装项目工具命令

在项目根目录执行：

```bash
./scripts/install-problem-tools.sh
```

安装脚本会把 `scripts/problem-tools/` 下的工具软链到 `~/.local/bin`。如果 shell 找不到命令，把下面这行加入 `~/.bashrc` 或 `~/.zshrc`：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

重新打开终端，或执行：

```bash
source ~/.zshrc
```

确认安装成功：

```bash
b --version
template.py list
```

## 2. 推荐题目目录

一个题目目录通常长这样：

```text
problems/luogu/9094/
├── index.md     # 题解正文
├── 1.cpp        # 当前题解代码
├── in           # 默认测试输入
├── in1          # 第 1 组样例输入
├── out1         # 第 1 组样例输出
└── data/        # 可选，本地批量测试数据
    ├── 1.in
    └── 1.out
```

建议在具体题目目录中运行这些工具：

```bash
cd problems/luogu/9094
```

## 3. 常用工作流

### 3.1 新建代码

从模板创建代码：

```bash
template.py
```

列出可用模板：

```bash
template.py list
```

直接输出某个模板内容：

```bash
template.py apply template.cpp
```

模板文件位于：

```text
scripts/problem-tools/templates/
```

### 3.2 下载洛谷样例

在洛谷题目目录中，如果目录名就是题号：

```bash
luogu.py
```

显式指定题号：

```bash
luogu.py P9094
luogu.py 9094
```

脚本会保存：

```text
in1, out1, in2, out2, ...
```

如果当前目录没有 `in`，会把第一组样例输入复制为 `in`，方便 `b 1` 直接运行。

### 3.3 编译并运行

编译并运行 `1.cpp`，默认读取 `in`：

```bash
b 1
```

指定输入文件：

```bash
b 1 -i in1
```

指定输出文件：

```bash
b 1 -i in1 -o my.out
```

只编译不运行：

```bash
b 1 -n
```

无输入运行：

```bash
b 1 -I
```

启用调试宏 `DEBUG`：

```bash
b 1 -d
```

指定 C++ 标准：

```bash
b 1 -s 17
```

选择输入文件：

```bash
b 1 -c
```

常用参数：

| 参数 | 含义 |
| --- | --- |
| `-i, --input-file` | 指定输入文件，默认 `in` |
| `-o, --output-file` | 指定输出文件 |
| `-c, --choose-input` | 交互式选择输入文件 |
| `-I, --no-input` | 不使用输入文件 |
| `-d, --debug` | 添加 `-DDEBUG` |
| `-s, --std` | 指定 C++ 标准 |
| `-f, --freopen` | 添加 `-DFREOPEN` |
| `-n, --norun` | 编译后不运行 |

## 4. 批量测试

`test-data.py` 用于运行程序，并和数据目录中的答案文件做 `diff`。

默认用 `1.out` 测试 `data/`：

```bash
test-data.py
```

指定程序和数据目录：

```bash
test-data.py 1.out data
```

指定临时输出文件：

```bash
test-data.py 1.out data -o test_out
```

数据目录支持：

```text
data/
├── 1.in
├── 1.out
├── 2.in
└── 2.ans
```

输入文件必须以 `.in` 结尾；答案文件支持 `.out` 或 `.ans`。

## 5. 对拍

`duipai.py` 用于自动生成数据，对比用户程序和标准程序。

交互式运行：

```bash
duipai.py
```

显式指定：

```bash
duipai.py -n 100 -d compare --data data.cpp --user 1.cpp --std std.cpp
```

参数：

| 参数 | 含义 |
| --- | --- |
| `-n, --count` | 对拍次数 |
| `-d, --dir` | 发现错误时保存输入的目录 |
| `--data` | 数据生成程序源码 |
| `--user` | 用户程序源码 |
| `--std` | 标准程序源码 |

脚本会在当前目录生成 `duipai_config.json`，下次运行时可复用配置。

单组输入对比两个程序：

```bash
one-duipai.py -o 1.out -r std.out -i in
```

调整并排 diff 宽度：

```bash
one-duipai.py -o 1.out -r std.out -i in -w 100
```

## 6. 图数据可视化

把边列表转为 Graphviz dot：

```bash
cat in | tail -n +2 | input2dot.py > graph.dot
```

有向图：

```bash
cat in | tail -n +2 | input2dot.py -d > graph.dot
```

把 dot 转为 PNG：

```bash
dot2png.py .
```

管道方式：

```bash
cat in | tail -n +2 | input2dot.py | dot2png.py -o graph.png
```

输入边格式：

```text
1 2
2 3 10
```

两列表示无权边，三列表示带权边。

## 7. 其他工具

### 7.1 随机整数

生成 5 个 `[1, 10]` 内的随机整数：

```bash
randint.py
```

生成 20 个 `[100, 999]` 内的随机整数：

```bash
randint.py 20 -min 100 -max 999
```

### 7.2 LLDB 调试

安装后命令名是 `r-lldb`，避免覆盖系统自带的 `lldb`：

```bash
r-lldb ./1.out
```

脚本会让你选择当前目录下名字包含 `in` 的输入文件，然后启动 LLDB。

### 7.3 Neovim 双栏查看

```bash
nvimsizer 1.cpp in
```

它会用 Neovim 左右打开两个文件，并根据右侧文件最长行调整窗口宽度。

### 7.4 上传文件

需要先配置自建 transfer.sh 地址：

```bash
export TRANSFER_URL="http://your-transfer-sh-url"
```

上传文件：

```bash
transfer 1.cpp
```

### 7.5 在线题目抓取入口

`oj` 会调用本项目保留的旧在线题目抓取入口：

```bash
oj --help
```

实际能力取决于 `old_scripts/online_judge/index.js`。详细用法见 `docs/oj-script.md`。

## 8. 写题目录中的 Markdown 引用

题解正文可以引用当前目录代码：

```markdown
@include-code(./1.cpp, cpp)
```

网站渲染时会把它转换成 C++ 代码块。推荐代码文件和 `index.md` 放在同一个题目目录中。

## 9. 故障排查

### 9.1 命令找不到

检查 `~/.local/bin` 是否在 `PATH`：

```bash
echo "$PATH"
```

重新安装：

```bash
./scripts/install-problem-tools.sh
```

### 9.2 `gum` 找不到

可以安装 `gum`，也可以不用。没有 `gum` 时，一些交互式选择会退回普通输入；如果某个命令必须交互选择，建议安装 `gum`。

### 9.3 编译器找不到

安装 `g++`：

```bash
sudo apt install -y g++
```

macOS 下脚本会优先使用 `clang++`。

### 9.4 `dot` 找不到

安装 Graphviz：

```bash
sudo apt install -y graphviz
```

### 9.5 对拍脚本生成了配置文件

`duipai.py` 可能在题目目录生成：

```text
duipai_config.json
```

这是本地对拍配置。是否提交取决于你是否希望保留这道题的对拍设置。

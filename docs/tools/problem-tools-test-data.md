# test-data.py

位置：

```text
scripts/problem-tools/test-data.py
```

作用：批量运行某个程序，并与数据目录中的 `.out/.ans` 答案文件做 diff。

安装后命令名：

```text
test-data.py
```

## 基本用法

默认用 `1.out` 测试 `data/`：

```bash
test-data.py
```

指定程序和数据目录：

```bash
test-data.py 1.out data
test-data.py ./sol data
```

指定临时输出文件：

```bash
test-data.py 1.out data -o test_out
```

## 数据目录格式

支持 `.in` 输入文件，以及 `.out` 或 `.ans` 答案文件：

```text
data/
├── 1.in
├── 1.out
├── 2.in
└── 2.ans
```

配对规则由 `scripts/problem-tools/mylib/getDataList.py` 提供：

- 优先按输入文件前缀匹配答案文件。
- 如果无法按前缀配对，则按排序后的顺序配对。

## 参数

- `program`：要运行的程序，默认 `1.out`。
- `data_path`：数据目录，默认 `data`。
- `-o, --output`：临时输出文件，默认 `test_out`。

## 退出码

- `0`：全部通过。
- `1`：存在失败、运行错误或异常。


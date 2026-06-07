# transfer

位置：

```text
scripts/problem-tools/transfer.sh
```

作用：把文件上传到自建 transfer.sh 服务，并输出分享链接和 raw 下载链接。

安装后命令名：

```text
transfer
```

## 前置配置

需要设置上传服务地址：

```bash
export TRANSFER_URL="http://your-transfer-sh-url"
```

可以把它写入 `~/.bashrc` 或 `~/.zshrc`。

## 基本用法

```bash
transfer 1.cpp
```

查看帮助：

```bash
transfer --help
```

上传成功后会输出：

```text
分享链接
直接下载 Raw 链接
```

## 注意事项

- 必须提供一个已存在的文件。
- 依赖 `curl`。
- 上传目标文件名会追加 `.txt`。

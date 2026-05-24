#!/usr/bin/env bash

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# 计算项目根目录 (向上两级)
PROJECT_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"
# 计算 online judge 入口的相对路径
INDEX_JS_PATH="$PROJECT_DIR/old_scripts/online_judge/index.js"

if [ ! -f "$INDEX_JS_PATH" ]; then
  echo "online judge entry not found: $INDEX_JS_PATH" >&2
  exit 1
fi

# 使用 node 调用 index.js
node "$INDEX_JS_PATH" $@

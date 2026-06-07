# rbook 写题辅助 shell 函数。
# 这个文件需要被当前 shell source，里面的函数才能改变当前终端目录。

_rbook_find_repo() {
  local repo

  if [ -n "${RBOOK_REPO:-}" ]; then
    repo="$RBOOK_REPO"
    if [ ! -d "$repo/scripts/problem-analysis-tools" ]; then
      echo "Error: RBOOK_REPO 不是 rbook 题目库：$repo" >&2
      return 1
    fi
    printf '%s\n' "$repo"
    return 0
  fi

  repo="$(git rev-parse --show-toplevel 2>/dev/null)" || {
    echo "Error: 你不在任何 Git 仓库中，且没有设置 RBOOK_REPO，无法定位 rbook 根目录。" >&2
    return 1
  }

  if [ ! -d "$repo/scripts/problem-analysis-tools" ]; then
    echo "Error: 当前 Git 仓库不是 rbook 题目库：$repo" >&2
    return 1
  fi

  printf '%s\n' "$repo"
}

fetch_problem() {
  local repo arg output exit_code problem_dir problem_abs

  repo="$(_rbook_find_repo)" || return 1

  for arg in "$@"; do
    case "$arg" in
      -h|--help|--self-test|--dry-run|--json)
        python3 "$repo/scripts/problem-analysis-tools/fetch_problem.py" "$@"
        return $?
        ;;
    esac
  done

  output="$(python3 "$repo/scripts/problem-analysis-tools/fetch_problem.py" --json "$@" 2>&1)"
  exit_code=$?
  if [ "$exit_code" -ne 0 ]; then
    printf '%s\n' "$output" >&2
    return "$exit_code"
  fi

  problem_dir="$(
    RBOOK_FETCH_PROBLEM_OUTPUT="$output" python3 - <<'PY'
import json
import os
import sys

try:
    payload = json.loads(os.environ["RBOOK_FETCH_PROBLEM_OUTPUT"])
except Exception as exc:
    print(f"无法解析 fetch_problem.py 输出：{exc}", file=sys.stderr)
    sys.exit(1)

if not payload.get("ok"):
    print(payload.get("error", "fetch_problem.py 执行失败"), file=sys.stderr)
    sys.exit(1)

print(payload.get("problem_dir", ""))
PY
  )" || {
    printf '%s\n' "$output" >&2
    return 1
  }

  if [ -z "$problem_dir" ]; then
    echo "Error: fetch_problem.py 没有返回 problem_dir。" >&2
    return 1
  fi

  RBOOK_FETCH_PROBLEM_OUTPUT="$output" python3 - <<'PY'
import json
import os

payload = json.loads(os.environ["RBOOK_FETCH_PROBLEM_OUTPUT"])
print(f"OJ: {payload['oj']}")
print(f"Problem: {payload['problem_id']}")
print(f"Directory: {payload['problem_dir']}")
print(f"Fetched: {'yes' if payload.get('fetched') else 'no'}")
if payload.get("title"):
    print(f"Title: {payload['title']}")
if payload.get("source"):
    print(f"Source: {payload['source']}")
for key, label in [("created", "Created"), ("written", "Written"), ("skipped", "Skipped")]:
    items = payload.get(key) or []
    if items:
        print(f"{label}:")
        for item in items:
            print(f"- {item}")
warnings = payload.get("warnings") or []
if warnings:
    print("Warnings:")
    for item in warnings:
        print(f"- {item}")
PY

  problem_abs="$repo/$problem_dir"
  if [ ! -d "$problem_abs" ]; then
    echo "Error: 题目目录不存在，无法进入：$problem_abs" >&2
    return 1
  fi

  cd "$problem_abs" || return 1
  printf 'Changed directory: %s\n' "$problem_dir"
}

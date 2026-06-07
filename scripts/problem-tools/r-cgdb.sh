#!/usr/bin/env bash

usage() {
  cat <<'EOF'
Usage: r-cgdb [executable]

Launch CGDB after interactively selecting an executable and an input file from
the current directory.

Dependencies:
  gum
  cgdb

Behavior:
  - If executable is omitted, select one interactively.
  - Select an input file whose name contains "in".
  - Start cgdb with a temporary gdb command file:
      define rr
        run < <selected_input>
      end
      break main
      rr

Options:
  -h, --help   Show this help message
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if ! command -v gum >/dev/null 2>&1; then
  echo "Error: 'gum' is not installed or not in your PATH." >&2
  exit 1
fi

if ! command -v cgdb >/dev/null 2>&1; then
  echo "Error: 'cgdb' is not installed or not in your PATH." >&2
  exit 1
fi

select_file() {
  local prompt="$1"
  shift
  if [ "$#" -eq 0 ]; then
    return 1
  fi
  printf '%s\n' "$@" | gum filter --height 10 --placeholder "$prompt"
}

executable="${1:-}"

if [ -z "$executable" ]; then
  # 常见的 OJ 可执行文件：有执行权限，或名字以 .out 结尾。
  mapfile -t executable_candidates < <(
    find . -maxdepth 1 -type f \( -perm -111 -o -name '*.out' \) \
      ! -name '*.cpp' ! -name '*.py' ! -name '*.sh' \
      | sed 's|^\./||' | sort
  )
  executable="$(select_file "选择要用 CGDB 调试的可执行文件..." "${executable_candidates[@]}")"
fi

if [ -z "$executable" ]; then
  echo "No executable selected. Aborting."
  exit 0
fi

if [ ! -f "$executable" ] && [ ! -f "./$executable" ]; then
  echo "Error: executable not found: $executable" >&2
  exit 1
fi

if [ "${executable#./}" = "$executable" ]; then
  executable="./$executable"
fi

mapfile -t input_candidates < <(
  find . -maxdepth 1 -type f -name '*in*' | sed 's|^\./||' | sort
)
selected_input="$(select_file "选择调试输入文件..." "${input_candidates[@]}")"

if [ -z "$selected_input" ]; then
  echo "No input file selected. Aborting."
  exit 0
fi

tmp_cmd="$(mktemp)"
cleanup() {
  rm -f "$tmp_cmd"
}
trap cleanup EXIT

cat > "$tmp_cmd" <<EOF
define rr
  run < $selected_input
end
break main
rr
EOF

echo "Starting cgdb for '$executable' with input '$selected_input'"
cgdb -- -x "$tmp_cmd" "$executable"

#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
TOOLS_DIR="$SCRIPT_DIR/problem-tools"
ANALYSIS_TOOLS_DIR="$SCRIPT_DIR/problem-analysis-tools"
BIN_DIR="${HOME}/.local/bin"

if [ ! -d "$TOOLS_DIR" ]; then
  echo "problem tools directory not found: $TOOLS_DIR" >&2
  exit 1
fi

mkdir -p "$BIN_DIR"

install_link() {
  local source_file="$1"
  local filename
  local command_name
  local target_file

  filename="$(basename "$source_file")"
  command_name="$filename"
  command_name="${command_name%.sh}"
  command_name="${command_name%.js}"
  if [ "$filename" = "lldb.sh" ]; then
    command_name="r-lldb"
  fi
  if [ "$filename" = "new-problem.py" ]; then
    command_name="new-problem"
  fi
  target_file="$BIN_DIR/$command_name"

  chmod +x "$source_file"

  if [ -e "$target_file" ] || [ -L "$target_file" ]; then
    if [ "$(readlink "$target_file" 2>/dev/null || true)" = "$source_file" ]; then
      echo "skip $target_file"
      return
    fi

    mv "$target_file" "${target_file}.bak"
    echo "backup $target_file -> ${target_file}.bak"
  fi

  ln -s "$source_file" "$target_file"
  echo "link $target_file -> $source_file"
}

install_dir_scripts() {
  local dir="$1"
  [ -d "$dir" ] || return 0
  for script in "$dir"/*; do
    [ -f "$script" ] || continue
    install_link "$script"
  done
}

install_dir_scripts "$TOOLS_DIR"
install_dir_scripts "$ANALYSIS_TOOLS_DIR"

cat <<EOF

Installed problem tools into $BIN_DIR.
Make sure this directory is in PATH, for example:

  export PATH="\$HOME/.local/bin:\$PATH"

EOF

#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
BIN_DIR="${BIN_DIR:-$HOME/.local/bin}"

usage() {
  cat <<'EOF'
Usage: ./install.sh [--help]

Install helper scripts for this repository.

Installed commands:
  ptool  -> ~/.local/bin/ptool

Make sure ~/.local/bin is in PATH:
  export PATH="$HOME/.local/bin:$PATH"
EOF
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

mkdir -p "$BIN_DIR"

install_link() {
  local source_file="$1"
  local command_name="$2"
  local target_file="$BIN_DIR/$command_name"

  if [ ! -f "$source_file" ]; then
    echo "Error: source script not found: $source_file" >&2
    exit 1
  fi

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

install_ptool() {
  install_link "$REPO_ROOT/scripts/navi/ptool" "ptool"
}

install_ptool

cat <<EOF

Installed helper scripts into $BIN_DIR.
Make sure this directory is in PATH, for example:

  export PATH="\$HOME/.local/bin:\$PATH"

EOF

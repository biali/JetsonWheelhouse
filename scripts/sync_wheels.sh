#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="${1:-/home/biali/Remoto/JETSON/delme/WheelBuilder/wheels}"
TARGET_DIR="${2:-packages}"

if [[ ! -d "$SOURCE_DIR" ]]; then
  echo "Source directory does not exist: $SOURCE_DIR" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

shopt -s nullglob
wheels=("$SOURCE_DIR"/*.whl)
shopt -u nullglob

if [[ ${#wheels[@]} -eq 0 ]]; then
  echo "No wheel files found in: $SOURCE_DIR" >&2
  exit 1
fi

rsync -av --delete --include='*.whl' --exclude='*' "$SOURCE_DIR"/ "$TARGET_DIR"/
echo "Synced ${#wheels[@]} wheel(s) from $SOURCE_DIR to $TARGET_DIR"

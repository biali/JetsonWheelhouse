#!/usr/bin/env bash
set -euo pipefail

MIRROR=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    -m | --mirror)
      MIRROR=1
      shift
      ;;
    -a | --append)
      # Default behavior; kept for backward compatibility and explicit scripts.
      shift
      ;;
    -h | --help)
      echo "Usage: $0 [--mirror|-m] [<source_dir>] [<target_dir>]" >&2
      echo "  Default source: /home/biali/Remoto/JETSON/delme/WheelBuilder/wheels" >&2
      echo "  Default target: packages" >&2
      echo "  Default: copy new/updated .whl files; keep other wheels already in target." >&2
      echo "  With --mirror: make target match source exactly (removes .whl not in source)." >&2
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      echo "Run $0 --help for usage." >&2
      exit 1
      ;;
    *)
      break
      ;;
  esac
done

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

rsync_opts=(-av --include='*.whl' --exclude='*')
if [[ "$MIRROR" -eq 1 ]]; then
  rsync_opts+=(--delete)
fi

rsync "${rsync_opts[@]}" "$SOURCE_DIR"/ "$TARGET_DIR"/

if [[ "$MIRROR" -eq 1 ]]; then
  echo "Mirrored ${#wheels[@]} wheel(s) from $SOURCE_DIR to $TARGET_DIR (extra .whl in target removed)"
else
  echo "Synced ${#wheels[@]} wheel(s) from $SOURCE_DIR to $TARGET_DIR (existing wheels kept)"
fi

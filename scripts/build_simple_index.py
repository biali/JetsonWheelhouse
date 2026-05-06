#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict


def normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def wheel_package_name(wheel_file: str) -> str:
    return wheel_file.split("-", 1)[0]


def package_page(package: str, wheel_names: list[str]) -> str:
    links = "\n".join(
        f'  <a href="../../packages/{html.escape(filename)}">{html.escape(filename)}</a><br/>'
        for filename in sorted(wheel_names)
    )
    return (
        "<!doctype html>\n"
        "<html>\n"
        "<body>\n"
        f"{links}\n"
        "</body>\n"
        "</html>\n"
    )


def root_page(packages: list[str]) -> str:
    links = "\n".join(
        f'  <a href="{html.escape(package)}/">{html.escape(package)}</a><br/>'
        for package in sorted(packages)
    )
    return (
        "<!doctype html>\n"
        "<html>\n"
        "<body>\n"
        f"{links}\n"
        "</body>\n"
        "</html>\n"
    )


def build_index(packages_dir: Path, simple_dir: Path) -> None:
    wheels = sorted(p.name for p in packages_dir.glob("*.whl"))
    if not wheels:
        raise SystemExit(f"No wheels found in {packages_dir}")

    grouped: DefaultDict[str, list[str]] = defaultdict(list)
    for wheel in wheels:
        grouped[normalize_name(wheel_package_name(wheel))].append(wheel)

    simple_dir.mkdir(parents=True, exist_ok=True)
    for package_name, wheel_files in grouped.items():
        package_dir = simple_dir / package_name
        package_dir.mkdir(parents=True, exist_ok=True)
        (package_dir / "index.html").write_text(
            package_page(package_name, wheel_files), encoding="utf-8"
        )

    (simple_dir / "index.html").write_text(
        root_page(list(grouped.keys())), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a PEP 503 simple wheel index.")
    parser.add_argument(
        "--packages-dir",
        default="packages",
        type=Path,
        help="Directory containing wheel files.",
    )
    parser.add_argument(
        "--simple-dir",
        default="simple",
        type=Path,
        help="Output directory for generated PEP 503 pages.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    build_index(args.packages_dir, args.simple_dir)


if __name__ == "__main__":
    main()

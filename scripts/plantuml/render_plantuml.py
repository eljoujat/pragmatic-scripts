#!/usr/bin/env python3
"""Render a PlantUML file to an image.

Standalone usage:
  python scripts/plantuml/render_plantuml.py --input diagram.puml --format png
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from plantweb.render import render_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render a PlantUML file to png/svg using plantweb.")
    parser.add_argument("-i", "--input", required=True, type=Path, help="Path to the .puml file")
    parser.add_argument("-f", "--format", default="png", choices=["png", "svg"], help="Output format")
    parser.add_argument("-o", "--output", type=Path, help="Optional output path. Defaults to generated file path.")
    parser.add_argument("--use-cache", action="store_true", help="Enable plantweb cache")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.exists():
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        return 2

    generated = Path(
        render_file(
            str(args.input),
            renderopts={"engine": "plantuml", "format": args.format},
            cacheopts={"use_cache": args.use_cache},
        )
    )

    output = args.output or generated
    if args.output:
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(generated, output)

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

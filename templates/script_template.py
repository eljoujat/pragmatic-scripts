#!/usr/bin/env python3
"""Short description of the task automated by this script.

Example:
  python scripts/domain/my_script.py --input file.txt --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Describe what the script does.")
    parser.add_argument("--input", type=Path, help="Input file or directory")
    parser.add_argument("--json", action="store_true", help="Print JSON output for automation")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.input and not args.input.exists():
        print(f"ERROR: input not found: {args.input}", file=sys.stderr)
        return 2

    result = {"status": "ok"}

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("OK")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

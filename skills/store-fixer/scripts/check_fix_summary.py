#!/usr/bin/env python3
"""Validate the minimal structure of a Store Fixer summary."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REQUIRED_LINES = [
    "# FIX SUMMARY",
    "STORE:",
    "MODE:",
    "ACCESS:",
    "APPROVAL:",
    "ROLLBACK READY:",
    "GOAL:",
]

REQUIRED_HEADINGS = [
    "## CHANGES",
    "## VERIFICATION",
    "## ROLLBACK",
    "## NEXT STEP",
]


def validate_summary(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    for prefix in REQUIRED_LINES:
        if prefix not in text:
            errors.append(f"Missing required line prefix: {prefix}")

    positions = []
    for heading in REQUIRED_HEADINGS:
        idx = text.find(heading)
        if idx == -1:
            errors.append(f"Missing required heading: {heading}")
        else:
            positions.append(idx)

    if positions and positions != sorted(positions):
        errors.append("Required headings are out of order.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to the summary markdown file")
    parser.add_argument(
        "--mode",
        required=True,
        choices=["execute", "plan", "review"],
        help="Intended response mode",
    )
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"[ERROR] File not found: {path}")
        return 1

    errors = validate_summary(path)
    if errors:
        print("[ERROR] Summary validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"[OK] Summary structure is valid for mode '{args.mode}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

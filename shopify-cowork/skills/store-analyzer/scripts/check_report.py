#!/usr/bin/env python3
"""Lint a generated Store Analysis report for structure and credibility.

Supports three modes via --mode:
  full    (default) — requires all dimension sections + headings
  focused           — requires SUMMARY + one dimension section + TOP 3 ACTIONS
  review            — requires BOTTOM LINE + at least one classification section
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# --- Mode-specific required headings ---

FULL_REQUIRED_HEADINGS = [
    "EXECUTIVE SUMMARY",
    "STORE SNAPSHOT",
    "TOP 5 ACTIONS",
]

FULL_REQUIRED_SECTIONS = [
    "SEO FINDINGS",
    "GEO FINDINGS",
    "AEO FINDINGS",
]

FOCUSED_REQUIRED_HEADINGS = [
    "SUMMARY",
    "TOP 3 ACTIONS",
]

REVIEW_REQUIRED_HEADINGS = [
    "BOTTOM LINE",
]

REVIEW_CLASSIFICATION_SECTIONS = [
    "SUPPORTED AND IMPORTANT",
    "SUPPORTED BUT SECONDARY",
    "REAL BUT OVERSTATED",
    "UNSUPPORTED FROM CURRENT EVIDENCE",
    "WHAT THE AUDIT MISSED",
]

BANNED_PHRASES = [
    "google is penalizing you",
    "this guarantees rankings",
    "this is why your traffic dropped",
    "your store will be deindexed",
]

WATCH_PHRASES = [
    "google can't index",
    "this is the #1 fix",
    "the whole store",
    "every page",
    "definitely",
    "guaranteed",
]


def find_missing(text: str, items: list[str]) -> list[str]:
    return [item for item in items if item not in text]


def check_full(text: str, lowered: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # Required headings
    missing = find_missing(text, FULL_REQUIRED_HEADINGS)
    if missing:
        errors.append(f"missing required headings: {', '.join(missing)}")

    # Dimension sections — errors, not warnings
    missing_sections = find_missing(text, FULL_REQUIRED_SECTIONS)
    if missing_sections:
        errors.append(f"missing required dimension sections: {', '.join(missing_sections)}")

    # Scope and evidence (must have enough for a full audit)
    scope_count = len(re.findall(r"^\s*Scope:\s*", text, flags=re.MULTILINE))
    evidence_count = len(re.findall(r"^\s*Evidence:\s*", text, flags=re.MULTILINE))

    if scope_count < 5:
        errors.append(f"expected at least 5 Scope lines in a full audit, found {scope_count}")
    if evidence_count < 5:
        errors.append(f"expected at least 5 Evidence lines in a full audit, found {evidence_count}")

    # Scope labels
    if not any(label in text for label in ("Catalog-wide", "Sampled", "Inference")):
        errors.append("no explicit Catalog-wide / Sampled / Inference labels detected")

    # GEO content
    if "ai bot" not in lowered and "ai visibility" not in lowered and "geo" not in lowered:
        errors.append("report is missing GEO (AI visibility) analysis")

    # AEO content
    if "faq schema" not in lowered and "answer" not in lowered and "aeo" not in lowered:
        errors.append("report is missing AEO (answer engine) analysis")

    # AI bot discussion
    if "robots.txt" not in lowered and "gptbot" not in lowered:
        warnings.append("report may not discuss AI bot access via robots.txt")

    # Evidence references
    if "products.json" not in lowered and "catalog-wide" not in lowered:
        warnings.append("report may be missing explicit catalog-wide evidence references")

    return errors, warnings


def check_focused(text: str, lowered: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = find_missing(text, FOCUSED_REQUIRED_HEADINGS)
    if missing:
        errors.append(f"missing required headings for focused audit: {', '.join(missing)}")

    # At least one dimension must be covered
    has_dimension = any(dim in text for dim in ("SEO", "GEO", "AEO"))
    if not has_dimension:
        errors.append("focused audit must cover at least one dimension (SEO, GEO, or AEO)")

    # Must have at least 1 Scope line
    scope_count = len(re.findall(r"^\s*Scope:\s*", text, flags=re.MULTILINE))
    if scope_count < 1:
        errors.append("expected at least 1 Scope line in a focused audit")

    return errors, warnings


def check_review(text: str, lowered: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing = find_missing(text, REVIEW_REQUIRED_HEADINGS)
    if missing:
        errors.append(f"missing required headings for audit review: {', '.join(missing)}")

    # Must have at least 2 classification sections
    found_sections = [s for s in REVIEW_CLASSIFICATION_SECTIONS if s in text]
    if len(found_sections) < 2:
        errors.append(f"audit review must have at least 2 classification sections, found {len(found_sections)}: {found_sections}")

    return errors, warnings


def check_common(text: str, lowered: str) -> tuple[list[str], list[str]]:
    """Checks applied to all modes."""
    errors: list[str] = []
    warnings: list[str] = []

    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            errors.append(f"contains banned phrase: {phrase}")

    for phrase in WATCH_PHRASES:
        if phrase in lowered:
            warnings.append(f"contains watch phrase that often overstates findings: {phrase}")

    # Minimum content length — reject trivially short reports
    word_count = len(text.split())
    if word_count < 100:
        errors.append(f"report is too short ({word_count} words). A valid report needs at least 100 words.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a Store Analysis report")
    parser.add_argument("--input", required=True, help="Path to the generated report")
    parser.add_argument(
        "--mode",
        choices=["full", "focused", "review"],
        default="full",
        help="Report mode: full (default), focused, or review",
    )
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"error: report file not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    lowered = text.lower()

    # Run common checks
    errors, warnings = check_common(text, lowered)

    # Run mode-specific checks
    if args.mode == "full":
        mode_errors, mode_warnings = check_full(text, lowered)
    elif args.mode == "focused":
        mode_errors, mode_warnings = check_focused(text, lowered)
    elif args.mode == "review":
        mode_errors, mode_warnings = check_review(text, lowered)
    else:
        mode_errors, mode_warnings = [], []

    errors.extend(mode_errors)
    warnings.extend(mode_warnings)

    if errors:
        print(f"REPORT CHECK FAILED ({args.mode} mode)")
        for error in errors:
            print(f"  error: {error}")
        for warning in warnings:
            print(f"  warning: {warning}")
        return 1

    if warnings:
        print(f"REPORT CHECK PASSED WITH WARNINGS ({args.mode} mode)")
        for warning in warnings:
            print(f"  warning: {warning}")
        return 0

    print(f"REPORT CHECK PASSED ({args.mode} mode)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

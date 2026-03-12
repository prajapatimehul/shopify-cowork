#!/usr/bin/env python3
"""Lint a generated Store Analysis report for structure and credibility.

Supports three modes via --mode:
  full    (default) — requires BOTTOM LINE, SNAPSHOT, FINDINGS, SAMPLE FIXES
  focused           — requires {DIMENSION} AUDIT, BOTTOM LINE, SNAPSHOT, FINDINGS
  review            — requires BOTTOM LINE + classification sections from the template
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# --- Mode-specific required headings ---

FULL_REQUIRED_HEADINGS = [
    "BOTTOM LINE",
    "SNAPSHOT",
    "FINDINGS",
    "SAMPLE FIXES",
    "AI-FACING GAPS",
]

FOCUSED_REQUIRED_HEADINGS = [
    "BOTTOM LINE",
    "SNAPSHOT",
    "FINDINGS",
]

REVIEW_REQUIRED_HEADINGS = [
    "BOTTOM LINE",
]

REVIEW_CLASSIFICATION_SECTIONS = [
    "SUPPORTED AND IMPORTANT",
    "SUPPORTED BUT SECONDARY",
    "REAL BUT OVERSTATED",
    "UNSUPPORTED FROM CURRENT EVIDENCE",
    "MISSING IMPORTANT ISSUES",
]

LEGACY_REVIEW_HEADINGS = [
    "UNSUPPORTED",
    "MISSED",
]

OLD_FORMAT_HEADINGS = [
    "EXECUTIVE SUMMARY",
    "STORE SNAPSHOT",
    "TOP 5 ACTIONS",
    "TOP 3 ACTIONS",
    "TOP ACTIONS",
    "SEO FINDINGS",
    "GEO FINDINGS",
    "AEO FINDINGS",
    "DIMENSION SUMMARY",
    "WHAT'S WORKING",
    "STORE READINESS SCORE",
    "KEY TAKEAWAY",
    "STRUCTURED DATA",
    "TITLES AND SNIPPETS",
    "CANONICALS AND URL",
    "ROBOTS.TXT",
    "SITEMAP",
    "PRODUCT CONTENT",
    "COLLECTION CONTENT",
    "PERFORMANCE PROXIES",
    "CATALOG DATA QUALITY",
    "AI BOT ACCESS",
    "ENTITY CLARITY",
    "CITATION-WORTHINESS",
    "CONTENT EXTRACTABILITY",
    "FAQ SCHEMA",
    "FEATURED SNIPPET",
    "VOICE SEARCH",
    "REVIEW SNIPPETS",
    "KNOWLEDGE PANEL",
    "SCORECARD",
]

BANNED_PHRASES = [
    "google is penalizing you",
    "this guarantees rankings",
    "this is why your traffic dropped",
    "your store will be deindexed",
    "store readiness score",
    "100-point",
    "this is a diagnostic benchmark",
    "what this means",
]

# Phrases that indicate recommending llms.txt as an action — research shows
# Google says no new AI text files needed. Never recommend creating one.
LLMS_TXT_ACTION_PHRASES = [
    "create llms.txt",
    "create an llms.txt",
    "add llms.txt",
    "add an llms.txt",
    "implement llms.txt",
    "set up llms.txt",
    "build llms.txt",
    "generate llms.txt",
    "recommend creating llms.txt",
    "should create llms.txt",
    "consider adding llms.txt",
    "consider creating llms.txt",
]

WATCH_PHRASES = [
    "google can't index",
    "this is the #1 fix",
    "the whole store",
    "every page",
    "definitely",
    "guaranteed",
    "missing llms.txt",
]

# Score patterns to reject: "43/100", "16/20", "3/15", etc.
SCORE_PATTERNS = [
    r"\b\d{1,3}\s*/\s*\d{2,3}\b",  # X/YY or X/YYY
]

# Checkmark list patterns: lines starting with ✓ or ✗
CHECKMARK_PATTERN = r"^\s*[✓✗✔✘☑☒⚠]\s"

MIN_WORDS_BY_MODE = {
    "full": 100,
    "focused": 40,
    "review": 40,
}


def find_missing(text: str, items: list[str]) -> list[str]:
    return [item for item in items if item not in text]


def extract_finding_blocks(text: str, has_sample_fixes: bool) -> list[tuple[int, str]]:
    end_heading = r"^\s*SAMPLE FIXES\s*$" if has_sample_fixes else r"\Z"
    findings_match = re.search(
        rf"(?ms)^\s*FINDINGS\s*$\n(?P<body>.*?)(?={end_heading})",
        text,
    )
    if not findings_match:
        return []

    body = findings_match.group("body")
    blocks: list[tuple[int, str]] = []
    for match in re.finditer(r"(?ms)^\s*#(?P<num>\d+)\b.*?(?=^\s*#\d+\b|\Z)", body):
        blocks.append((int(match.group("num")), match.group(0)))
    return blocks


def validate_finding_blocks(blocks: list[tuple[int, str]]) -> list[str]:
    errors: list[str] = []
    required_fields = ("Scope:", "Proof:", "Fix:", "Impact:")

    for finding_number, block in blocks:
        for field in required_fields:
            if not re.search(rf"^\s*{re.escape(field)}\s*", block, flags=re.MULTILINE):
                errors.append(f"finding #{finding_number} is missing {field.rstrip(':')}")

    return errors


def check_full(text: str, lowered: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # Required headings
    missing = find_missing(text, FULL_REQUIRED_HEADINGS)
    if missing:
        errors.append(f"missing required headings: {', '.join(missing)}")

    old_headings = [heading for heading in OLD_FORMAT_HEADINGS if heading in text]
    if old_headings:
        errors.append(f"contains old-format headings that the current skill forbids: {', '.join(old_headings)}")

    finding_blocks = extract_finding_blocks(text, has_sample_fixes=True)
    finding_count = len(finding_blocks)
    problem_count = len(re.findall(r"^\s*Problem:\s*", text, flags=re.MULTILINE))
    result_count = len(re.findall(r"^\s*Result:\s*", text, flags=re.MULTILINE))

    if finding_count < 3:
        errors.append(f"expected at least 3 findings in a full audit, found {finding_count}")
    if finding_count > 10:
        errors.append(f"full audit exceeds the 10-finding cap, found {finding_count}")
    errors.extend(validate_finding_blocks(finding_blocks))
    if problem_count < 1:
        errors.append("full audit is missing sample-fix Problem lines")
    if result_count < 1:
        errors.append("full audit is missing sample-fix Result lines")

    # Scope labels
    if not any(label in text for label in ("Catalog-wide", "Sampled", "Inference")):
        errors.append("no explicit Catalog-wide / Sampled / Inference labels detected")

    word_count = len(text.split())
    if word_count < MIN_WORDS_BY_MODE["full"]:
        errors.append(
            f"report is too short ({word_count} words). A valid full audit needs at least {MIN_WORDS_BY_MODE['full']} words."
        )

    line_count = len(text.strip().splitlines())
    if line_count > 180:
        errors.append(
            f"report is too long ({line_count} lines). A full audit should be 80-140 lines max. Cut the noise."
        )
    elif line_count > 140:
        warnings.append(
            f"report is {line_count} lines — pushing the 140-line limit. Consider cutting lower-impact findings."
        )

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

    old_headings = [heading for heading in OLD_FORMAT_HEADINGS if heading in text]
    if old_headings:
        errors.append(f"contains old-format headings that the current skill forbids: {', '.join(old_headings)}")

    # At least one dimension must be covered
    has_dimension = any(dim in text for dim in ("SEO", "GEO", "AEO"))
    if not has_dimension:
        errors.append("focused audit must cover at least one dimension (SEO, GEO, or AEO)")

    finding_blocks = extract_finding_blocks(text, has_sample_fixes=False)
    finding_count = len(finding_blocks)

    if finding_count < 1:
        errors.append("expected at least 1 finding in a focused audit")
    if finding_count > 5:
        errors.append(f"focused audit exceeds the 5-finding cap, found {finding_count}")
    errors.extend(validate_finding_blocks(finding_blocks))

    word_count = len(text.split())
    if word_count < MIN_WORDS_BY_MODE["focused"]:
        errors.append(
            f"report is too short ({word_count} words). A valid focused audit needs at least {MIN_WORDS_BY_MODE['focused']} words."
        )

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

    legacy_review_headings = [
        heading for heading in LEGACY_REVIEW_HEADINGS if re.search(rf"^\s*{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    ]
    if legacy_review_headings:
        errors.append(
            f"contains legacy review headings that the current template replaced: {', '.join(legacy_review_headings)}"
        )

    word_count = len(text.split())
    if word_count < MIN_WORDS_BY_MODE["review"]:
        errors.append(
            f"report is too short ({word_count} words). A valid audit review needs at least {MIN_WORDS_BY_MODE['review']} words."
        )

    return errors, warnings


def check_common(text: str, lowered: str) -> tuple[list[str], list[str]]:
    """Checks applied to all modes."""
    errors: list[str] = []
    warnings: list[str] = []

    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            errors.append(f"contains banned phrase: '{phrase}'")

    # Check for llms.txt being recommended as an action item
    for phrase in LLMS_TXT_ACTION_PHRASES:
        if phrase in lowered:
            errors.append(
                f"recommends creating llms.txt ('{phrase}') — research shows Google says "
                "no new AI text files needed. Never recommend this as an action."
            )

    # Check all score patterns (X/Y ratings)
    for pattern in SCORE_PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            errors.append(
                f"contains numerical scores even though the skill forbids them: {', '.join(matches[:5])}"
            )
            break

    # Check for checkmark lists (✓/✗ pattern)
    checkmark_lines = re.findall(CHECKMARK_PATTERN, text, flags=re.MULTILINE)
    if len(checkmark_lines) > 2:
        errors.append(
            f"contains {len(checkmark_lines)} checkmark list lines (✓/✗) — "
            "report should only list issues to fix, not what's working"
        )

    for phrase in WATCH_PHRASES:
        if phrase in lowered:
            warnings.append(f"contains watch phrase that often overstates findings: '{phrase}'")

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

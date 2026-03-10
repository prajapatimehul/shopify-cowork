#!/usr/bin/env python3
"""Lint a generated Shopify SEO audit report for structure and credibility."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_AUDIT_HEADINGS = [
    "EXECUTIVE SUMMARY",
    "STORE SNAPSHOT",
    "TOP 5 ACTIONS",
    "SAMPLE FIXES",
]

BANNED_PHRASES = [
    "google is penalizing you",
    "this guarantees rankings",
    "this is why your traffic dropped",
    "google has nothing to index",
    "kills organic search visibility",
    "invisible to search engines",
]

WATCH_PHRASES = [
    "google can't index",
    "this is the #1 fix",
    "the whole store",
    "every page",
]


def find_missing_headings(text: str) -> list[str]:
    return [heading for heading in REQUIRED_AUDIT_HEADINGS if heading not in text]


def find_missing_required_patterns(text: str) -> list[str]:
    required_patterns = {
        "Audit mode line": r"^\s*Audit mode:\s*(Full audit|Partial audit)\s*$",
        "Limitations line": r"^\s*Limitations:\s*\S.*$",
    }
    missing: list[str] = []
    for label, pattern in required_patterns.items():
        if not re.search(pattern, text, flags=re.MULTILINE):
            missing.append(label)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to the generated report")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as a failing exit code",
    )
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"error: report file not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    lowered = text.lower()

    errors: list[str] = []
    warnings: list[str] = []

    missing_headings = find_missing_headings(text)
    if missing_headings:
        errors.append(f"missing required headings: {', '.join(missing_headings)}")

    missing_patterns = find_missing_required_patterns(text)
    if missing_patterns:
        errors.append(f"missing required report labels: {', '.join(missing_patterns)}")

    scope_count = len(re.findall(r"^\s*Scope:\s*", text, flags=re.MULTILINE))
    evidence_count = len(re.findall(r"^\s*Evidence:\s*", text, flags=re.MULTILINE))

    if scope_count < 5:
        errors.append("expected at least 5 Scope lines in the report")
    if evidence_count < 5:
        errors.append("expected at least 5 Evidence lines in the report")

    if "INTERNAL SEO SCORE" in text and "internal heuristic" not in lowered:
        errors.append("score is present but not labeled as an internal heuristic")

    if "SEO SCORE" in text and "INTERNAL SEO SCORE" not in text:
        errors.append("score uses SEO SCORE instead of INTERNAL SEO SCORE")

    if not any(label in text for label in ("Catalog-wide", "Sampled", "Inference")):
        errors.append("no explicit Catalog-wide / Sampled / Inference labels detected")

    audit_mode_match = re.search(r"^\s*Audit mode:\s*(Full audit|Partial audit)\s*$", text, flags=re.MULTILINE)
    audit_mode = audit_mode_match.group(1) if audit_mode_match else None
    present_scopes = {label for label in ("Catalog-wide", "Sampled", "Inference") if label in text}
    if audit_mode == "Full audit" and not {"Catalog-wide", "Sampled"}.issubset(present_scopes):
        errors.append("full audits must include both Catalog-wide and Sampled scope labels")
    if audit_mode == "Partial audit" and "Sampled" not in present_scopes:
        errors.append("partial audits must include Sampled scope labels")

    for phrase in BANNED_PHRASES:
        if phrase in lowered:
            errors.append(f"contains banned phrase: {phrase}")

    for phrase in WATCH_PHRASES:
        if phrase in lowered:
            warnings.append(f"contains watch phrase that often overstates findings: {phrase}")

    if "meta description" in lowered and "og:description" in lowered:
        warnings.append("report may be conflating standard meta descriptions with og:description")

    endpoint_refs = ("/products.json", "/collections.json", "/robots.txt", "/sitemap.xml")
    if audit_mode == "Full audit" and not any(ref in lowered for ref in endpoint_refs):
        errors.append("full audit is missing explicit public endpoint evidence references")

    if "products.json" not in lowered and "catalog-wide" not in lowered:
        warnings.append("report may be missing explicit catalog-wide evidence references")

    if errors:
        print("REPORT CHECK FAILED")
        for error in errors:
            print(f"- error: {error}")
        for warning in warnings:
            print(f"- warning: {warning}")
        return 1

    print("REPORT CHECK PASSED")
    if warnings:
        for warning in warnings:
            print(f"- warning: {warning}")

    return 1 if warnings and args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())

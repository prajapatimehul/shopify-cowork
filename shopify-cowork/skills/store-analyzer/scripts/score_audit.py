#!/usr/bin/env python3
"""Compute the Store Readiness Score from structured metrics JSON.

Requires all five top-level sections to be present. Missing sections are
treated as unaudited and scored as N/A rather than silently defaulting to
healthy. The output includes a completeness ratio so consumers know how
much of the score is backed by real data.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


CATEGORY_MAX = {
    "Technical SEO": 20,
    "Content & On-Page": 25,
    "Structured Data": 20,
    "GEO: AI Visibility": 20,
    "AEO: Answer Readiness": 15,
}

SECTION_TO_CATEGORY = {
    "technical_seo": "Technical SEO",
    "content_onpage": "Content & On-Page",
    "structured_data": "Structured Data",
    "geo_ai_visibility": "GEO: AI Visibility",
    "aeo_answer_readiness": "AEO: Answer Readiness",
}

# Minimum keys required per section. If a section is present but missing
# these keys, the section is treated as incomplete.
REQUIRED_KEYS: dict[str, list[str]] = {
    "technical_seo": [
        "robots_missing_rules",
        "sitemap_not_accessible",
        "canonical_issues",
        "collection_prefixed_links",
        "lcp_image_lazy",
        "external_script_domains",
    ],
    "content_onpage": [
        "percent_products_missing_description",
        "percent_collections_missing_description",
        "out_of_range_titles",
        "missing_meta_descriptions",
    ],
    "structured_data": [
        "missing_product_jsonld",
        "missing_required_merchant_fields",
        "missing_aggregate_rating",
        "missing_breadcrumb_schema",
        "missing_org_schema",
    ],
    "geo_ai_visibility": [
        "ai_search_bots_blocked",
        "no_llms_txt",
        "missing_sameas_platforms",
        "no_question_headings",
        "no_review_signals",
    ],
    "aeo_answer_readiness": [
        "no_faq_schema",
        "page_types_without_question_headings",
        "no_comparison_content",
        "review_snippet_ineligible",
    ],
}


def as_bool(value: object) -> bool:
    return bool(value)


def as_int(value: object, default: int = 0) -> int:
    if value is None:
        return default
    return int(value)


def as_float(value: object, default: float = 0.0) -> float:
    if value is None:
        return default
    return float(value)


def ceil_units(value: float, unit: float, cap: int) -> int:
    if value <= 0:
        return 0
    return min(cap, int(math.ceil(value / unit)))


def validate_section(metrics: dict, section: str) -> list[str]:
    """Return list of missing required keys for a section."""
    data = metrics.get(section)
    if data is None:
        return REQUIRED_KEYS.get(section, [])
    if not isinstance(data, dict):
        return REQUIRED_KEYS.get(section, [])
    required = REQUIRED_KEYS.get(section, [])
    return [k for k in required if k not in data]


def validate_metrics(metrics: dict) -> tuple[list[str], list[str], list[str]]:
    """Validate the metrics JSON. Returns (missing_sections, incomplete_sections, all_missing_keys)."""
    missing_sections: list[str] = []
    incomplete_sections: list[str] = []
    all_missing_keys: list[str] = []

    for section in SECTION_TO_CATEGORY:
        if section not in metrics or not isinstance(metrics.get(section), dict):
            missing_sections.append(section)
            continue
        missing_keys = validate_section(metrics, section)
        if missing_keys:
            incomplete_sections.append(section)
            all_missing_keys.extend(f"{section}.{k}" for k in missing_keys)

    return missing_sections, incomplete_sections, all_missing_keys


def compute_breakdown(metrics: dict) -> dict[str, int | str | None]:
    missing_sections, incomplete_sections, _ = validate_metrics(metrics)

    # Categories that were not audited get None instead of a score.
    skipped_categories: set[str] = set()
    for section in missing_sections:
        skipped_categories.add(SECTION_TO_CATEGORY[section])

    tech = metrics.get("technical_seo", {}) if "technical_seo" not in missing_sections else {}
    content = metrics.get("content_onpage", {}) if "content_onpage" not in missing_sections else {}
    schema = metrics.get("structured_data", {}) if "structured_data" not in missing_sections else {}
    geo = metrics.get("geo_ai_visibility", {}) if "geo_ai_visibility" not in missing_sections else {}
    aeo = metrics.get("aeo_answer_readiness", {}) if "aeo_answer_readiness" not in missing_sections else {}

    deductions: dict[str, int] = {cat: 0 for cat in CATEGORY_MAX}

    # --- A. Technical SEO (20) ---
    if "Technical SEO" not in skipped_categories:
        deductions["Technical SEO"] += min(3, as_int(tech.get("robots_missing_rules")))
        deductions["Technical SEO"] += 3 if as_bool(tech.get("sitemap_not_accessible")) else min(3, as_int(tech.get("sitemap_issues")))
        deductions["Technical SEO"] += 3 if as_bool(tech.get("canonical_issues")) else 0
        deductions["Technical SEO"] += 3 if as_bool(tech.get("collection_prefixed_links")) else 0
        deductions["Technical SEO"] += 2 if as_bool(tech.get("lcp_image_lazy")) else 0
        deductions["Technical SEO"] += 1 if as_bool(tech.get("missing_fetchpriority")) else 0
        deductions["Technical SEO"] += 1 if as_bool(tech.get("missing_image_dimensions")) else 0
        ext_scripts = as_int(tech.get("external_script_domains"))
        if ext_scripts > 15:
            deductions["Technical SEO"] += 2
        elif ext_scripts > 10:
            deductions["Technical SEO"] += 1
        deductions["Technical SEO"] += min(2, as_int(tech.get("render_blocking_scripts")))

    # --- B. Content & On-Page (25) ---
    if "Content & On-Page" not in skipped_categories:
        deductions["Content & On-Page"] += ceil_units(as_float(content.get("percent_products_missing_description")), 10, 5)
        deductions["Content & On-Page"] += ceil_units(as_float(content.get("percent_products_thin")), 15, 3)
        deductions["Content & On-Page"] += min(2, as_int(content.get("duplicate_description_groups")))
        deductions["Content & On-Page"] += ceil_units(as_float(content.get("percent_collections_missing_description")), 20, 4)
        deductions["Content & On-Page"] += min(2, as_int(content.get("out_of_range_titles")))
        deductions["Content & On-Page"] += 2 if as_bool(content.get("identical_title_pattern")) else 0
        deductions["Content & On-Page"] += min(2, as_int(content.get("missing_meta_descriptions")))
        deductions["Content & On-Page"] += 1 if as_bool(content.get("h1_issues")) else 0
        deductions["Content & On-Page"] += 1 if as_bool(content.get("product_type_inconsistent")) else 0
        deductions["Content & On-Page"] += 1 if as_bool(content.get("vendor_inconsistent")) else 0
        deductions["Content & On-Page"] += 1 if as_bool(content.get("too_few_collections")) else 0
        deductions["Content & On-Page"] += 1 if as_bool(content.get("zero_price_products")) else 0

    # --- C. Structured Data (20) ---
    # Reviews/ratings scored HERE only. GEO and AEO reference review signals
    # but do NOT deduct for them again (see de-duplication note below).
    if "Structured Data" not in skipped_categories:
        deductions["Structured Data"] += 4 if as_bool(schema.get("missing_product_jsonld")) else 0
        deductions["Structured Data"] += min(3, as_int(schema.get("missing_required_merchant_fields")))
        deductions["Structured Data"] += 2 if as_bool(schema.get("missing_product_identifiers")) else 0
        deductions["Structured Data"] += 1 if as_bool(schema.get("missing_brand")) else 0
        deductions["Structured Data"] += 3 if as_bool(schema.get("missing_aggregate_rating")) else 0
        deductions["Structured Data"] += 1 if as_bool(schema.get("missing_review_schema")) else 0
        deductions["Structured Data"] += 2 if as_bool(schema.get("missing_breadcrumb_schema")) else 0
        deductions["Structured Data"] += 2 if as_bool(schema.get("missing_org_schema")) else 0
        deductions["Structured Data"] += 2 if as_bool(schema.get("schema_not_server_rendered")) else 0
        deductions["Structured Data"] += 1 if as_bool(schema.get("schema_errors")) else 0

    # --- D. GEO: AI Visibility (20) ---
    # De-duplication: review signals and Organization schema are scored in
    # Structured Data (C). GEO only scores AI-specific checks: bot access,
    # llms.txt, sameAs breadth, brand consistency, about page, content
    # extractability (question headings, tables), and freshness.
    if "GEO: AI Visibility" not in skipped_categories:
        deductions["GEO: AI Visibility"] += min(5, as_int(geo.get("ai_search_bots_blocked")))
        deductions["GEO: AI Visibility"] += 2 if as_bool(geo.get("no_llms_txt")) else 0
        deductions["GEO: AI Visibility"] += min(3, as_int(geo.get("missing_sameas_platforms")))
        deductions["GEO: AI Visibility"] += 1 if as_bool(geo.get("brand_name_inconsistent")) else 0
        deductions["GEO: AI Visibility"] += 1 if as_bool(geo.get("weak_about_page")) else 0
        deductions["GEO: AI Visibility"] += 4 if as_bool(geo.get("no_question_headings")) else 0
        deductions["GEO: AI Visibility"] += 2 if as_bool(geo.get("no_tables_or_lists")) else 0
        # no_review_signals: NOT scored here (scored in C5/C6)
        stale = as_float(geo.get("stale_products_percent"))
        deductions["GEO: AI Visibility"] += 1 if stale > 50 else 0
        deductions["GEO: AI Visibility"] += 1 if as_bool(geo.get("no_recent_blog")) else 0

    # --- E. AEO: Answer Readiness (15) ---
    # De-duplication: question headings scored in GEO (D6). AEO scores FAQ
    # schema, answer paragraph quality, comparison content, and instructional
    # content — none of which overlap with other categories.
    # Review snippet eligibility: NOT scored here (scored in C5).
    # Knowledge Panel signals: NOT scored here (scored in C8 + D3).
    if "AEO: Answer Readiness" not in skipped_categories:
        deductions["AEO: Answer Readiness"] += 3 if as_bool(aeo.get("no_faq_schema")) else 0
        # page_types_without_question_headings: NOT scored here (scored in D6)
        deductions["AEO: Answer Readiness"] += 3 if as_bool(aeo.get("poor_answer_format")) else 0
        deductions["AEO: Answer Readiness"] += 3 if as_bool(aeo.get("no_comparison_content")) else 0
        # review_snippet_ineligible: NOT scored here (scored in C5)
        # no_knowledge_panel_signals: NOT scored here (scored in C8 + D3)
        deductions["AEO: Answer Readiness"] += 3 if as_bool(aeo.get("no_instructional_content")) else 0

    # Build breakdown with None for skipped categories.
    breakdown: dict[str, int | str | None] = {}
    audited_max = 0
    audited_score = 0
    for cat, maximum in CATEGORY_MAX.items():
        if cat in skipped_categories:
            breakdown[cat] = None
        else:
            score = max(0, maximum - deductions[cat])
            breakdown[cat] = score
            audited_max += maximum
            audited_score += score

    # Total is computed only over audited categories.
    if audited_max == 0:
        breakdown["Total"] = None
        breakdown["Audited"] = "0/100"
        breakdown["Completeness"] = "0%"
    else:
        # Scale to 100 only if all categories present; otherwise show raw.
        if audited_max == 100:
            breakdown["Total"] = audited_score
        else:
            # Partial audit: show actual scored points and max possible.
            breakdown["Total"] = f"{audited_score}/{audited_max}"
        breakdown["Audited"] = f"{audited_max}/100"
        breakdown["Completeness"] = f"{round(audited_max / 100 * 100)}%"

    return breakdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute Store Readiness Score")
    parser.add_argument("--input", required=True, help="Path to metrics JSON")
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Print a readable breakdown instead of JSON only",
    )
    args = parser.parse_args()

    path = Path(args.input)
    if not path.exists():
        print(f"error: metrics file not found: {path}", file=sys.stderr)
        return 1

    metrics = json.loads(path.read_text(encoding="utf-8"))

    # Validate before scoring.
    missing_sections, incomplete_sections, all_missing_keys = validate_metrics(metrics)

    if not metrics or all(s in missing_sections for s in SECTION_TO_CATEGORY):
        print("error: metrics JSON is empty or has no audited sections", file=sys.stderr)
        print("  Required top-level keys: " + ", ".join(SECTION_TO_CATEGORY.keys()), file=sys.stderr)
        return 1

    breakdown = compute_breakdown(metrics)

    if args.pretty:
        total = breakdown["Total"]
        completeness = breakdown["Completeness"]

        if isinstance(total, int):
            if total >= 85:
                band = "Strong"
            elif total >= 65:
                band = "Good foundation"
            elif total >= 40:
                band = "Significant opportunities"
            else:
                band = "Foundational work needed"
            print(f"STORE READINESS SCORE: {total}/100 ({band})")
        else:
            print(f"STORE READINESS SCORE: {total} (partial audit)")

        print(f"  Audit completeness: {completeness}")
        print()

        if missing_sections:
            print(f"  NOT AUDITED: {', '.join(SECTION_TO_CATEGORY[s] for s in missing_sections)}")
            print()

        if incomplete_sections:
            print("  INCOMPLETE SECTIONS (missing required keys):")
            for key in all_missing_keys:
                print(f"    - {key}")
            print()

        for category, maximum in CATEGORY_MAX.items():
            score = breakdown[category]
            if score is None:
                print(f"  {category:.<30s} N/A (not audited)")
            else:
                pct = round(score / maximum * 100)
                print(f"  {category:.<30s} {score}/{maximum} ({pct}%)")
        return 0

    print(json.dumps(breakdown, indent=2, sort_keys=True, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

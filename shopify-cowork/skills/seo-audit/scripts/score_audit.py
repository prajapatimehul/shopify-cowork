#!/usr/bin/env python3
"""Compute the internal SEO score from structured metrics JSON."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


CATEGORY_MAX = {
    "Structured Data": 15,
    "Titles & Snippets": 10,
    "URL Consolidation": 10,
    "Content Depth": 25,
    "Crawlability": 15,
    "Collection/Blog IA": 15,
    "Performance Risk": 5,
    "Hygiene": 5,
}

REQUIRED_TOP_LEVEL_KEYS = {
    "audit_context",
    "structured_data",
    "titles_snippets",
    "url_consolidation",
    "content_depth",
    "crawlability",
    "collection_blog_ia",
    "performance_risk",
    "hygiene",
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


def validate_metrics(metrics: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing_top_level = sorted(REQUIRED_TOP_LEVEL_KEYS - set(metrics.keys()))
    if missing_top_level:
        errors.append(f"missing top-level keys: {', '.join(missing_top_level)}")
        return errors, warnings

    context = metrics.get("audit_context", {})
    required_context = {
        "audit_mode",
        "catalog_products_complete",
        "catalog_collections_complete",
        "catalog_pages_complete",
        "robots_fetched",
        "sitemap_fetched",
        "homepage_sampled",
        "sampled_product_pages",
        "sampled_collection_pages",
        "sampled_article_pages",
    }
    missing_context = sorted(required_context - set(context.keys()))
    if missing_context:
        errors.append(f"missing audit_context keys: {', '.join(missing_context)}")
        return errors, warnings

    audit_mode = context.get("audit_mode")
    if audit_mode not in {"full", "partial"}:
        errors.append("audit_context.audit_mode must be 'full' or 'partial'")

    sampled_product_pages = as_int(context.get("sampled_product_pages"))
    sampled_collection_pages = as_int(context.get("sampled_collection_pages"))
    sampled_article_pages = as_int(context.get("sampled_article_pages"))

    if sampled_product_pages < 3:
        errors.append("sampled_product_pages must be at least 3")
    if sampled_collection_pages < 1:
        errors.append("sampled_collection_pages must be at least 1")
    if sampled_article_pages < 0:
        errors.append("sampled_article_pages cannot be negative")
    if not as_bool(context.get("homepage_sampled")):
        errors.append("homepage_sampled must be true")

    if audit_mode == "full":
        required_true = [
            "catalog_products_complete",
            "catalog_collections_complete",
            "catalog_pages_complete",
            "robots_fetched",
            "sitemap_fetched",
        ]
        not_true = [key for key in required_true if not as_bool(context.get(key))]
        if not_true:
            errors.append(
                "full audits require true values for: " + ", ".join(not_true)
            )

    if audit_mode == "partial":
        warnings.append("partial audit: score is based on incomplete public evidence")

    return errors, warnings


def compute_breakdown(metrics: dict) -> dict[str, int]:
    structured = metrics.get("structured_data", {})
    titles = metrics.get("titles_snippets", {})
    urls = metrics.get("url_consolidation", {})
    content = metrics.get("content_depth", {})
    crawl = metrics.get("crawlability", {})
    ia = metrics.get("collection_blog_ia", {})
    perf = metrics.get("performance_risk", {})
    hygiene = metrics.get("hygiene", {})

    deductions = {
        "Structured Data": 0,
        "Titles & Snippets": 0,
        "URL Consolidation": 0,
        "Content Depth": 0,
        "Crawlability": 0,
        "Collection/Blog IA": 0,
        "Performance Risk": 0,
        "Hygiene": 0,
    }

    deductions["Structured Data"] += 6 if as_bool(structured.get("missing_json_ld")) else 0
    deductions["Structured Data"] += 4 if as_bool(structured.get("missing_offers_or_price")) else 0
    deductions["Structured Data"] += 1 if as_bool(structured.get("missing_aggregate_rating")) else 0
    deductions["Structured Data"] += 1 if as_bool(structured.get("missing_brand")) else 0
    deductions["Structured Data"] += 1 if as_bool(structured.get("bad_description")) else 0
    deductions["Structured Data"] += 1 if as_bool(structured.get("missing_breadcrumb_schema")) else 0
    deductions["Structured Data"] += 1 if as_bool(structured.get("missing_org_schema")) else 0
    deductions["Structured Data"] += 1 if as_bool(structured.get("duplicate_schema_blocks")) else 0

    deductions["Titles & Snippets"] += min(4, as_int(titles.get("out_of_range_titles")) * 2)
    deductions["Titles & Snippets"] += 2 if as_bool(titles.get("identical_title_pattern")) else 0
    deductions["Titles & Snippets"] += min(3, as_int(titles.get("missing_meta_descriptions")))
    deductions["Titles & Snippets"] += (
        1 if as_bool(titles.get("identical_or_template_descriptions")) else 0
    )
    deductions["Titles & Snippets"] += 1 if as_bool(titles.get("weak_snippets")) else 0

    deductions["URL Consolidation"] += 3 if as_bool(urls.get("canonical_issues")) else 0
    deductions["URL Consolidation"] += (
        2 if as_bool(urls.get("collection_prefixed_internal_links")) else 0
    )
    deductions["URL Consolidation"] += 2 if as_bool(urls.get("missing_sort_filter_blocking")) else 0
    deductions["URL Consolidation"] += 1 if as_bool(urls.get("tag_combination_urls_crawlable")) else 0
    deductions["URL Consolidation"] += 1 if as_bool(urls.get("junk_urls_crawlable")) else 0
    deductions["URL Consolidation"] += 1 if as_bool(urls.get("inconsistent_canonicals")) else 0

    deductions["Content Depth"] += ceil_units(
        as_float(content.get("percent_products_missing_description")), 5, 10
    )
    deductions["Content Depth"] += ceil_units(as_float(content.get("percent_products_thin")), 10, 5)
    deductions["Content Depth"] += min(3, as_int(content.get("duplicate_description_groups")))
    deductions["Content Depth"] += ceil_units(
        as_float(content.get("percent_collections_missing_description")), 20, 5
    )
    deductions["Content Depth"] += min(
        2, ceil_units(as_float(content.get("thin_or_empty_pages")), 3, 2)
    )

    deductions["Crawlability"] += min(
        4, as_int(crawl.get("missing_search_preview_policy_recommendation_rules"))
    )
    deductions["Crawlability"] += 3 if as_bool(crawl.get("sitemap_not_accessible")) else 0
    deductions["Crawlability"] += min(3, as_int(crawl.get("missing_sub_sitemaps")))
    deductions["Crawlability"] += 2 if as_bool(crawl.get("product_count_mismatch")) else 0
    deductions["Crawlability"] += 1 if as_bool(crawl.get("important_url_class_absent")) else 0
    deductions["Crawlability"] += 3 if as_bool(crawl.get("pages_blocked_unintentionally")) else 0

    deductions["Collection/Blog IA"] += min(3, ceil_units(as_float(ia.get("empty_collections")), 3, 3))
    deductions["Collection/Blog IA"] += 4 if as_bool(ia.get("too_few_collections")) else 0
    deductions["Collection/Blog IA"] += 3 if as_bool(ia.get("junk_collections_exposed")) else 0
    deductions["Collection/Blog IA"] += 2 if as_bool(ia.get("weak_blog_posts_or_links")) else 0
    deductions["Collection/Blog IA"] += (
        3 if as_bool(ia.get("orphaned_products_or_weak_coverage")) else 0
    )

    deductions["Performance Risk"] += 1 if as_bool(perf.get("primary_image_lazy_loaded")) else 0
    deductions["Performance Risk"] += min(
        2, max(0, as_int(perf.get("high_external_script_count_penalty")))
    )
    deductions["Performance Risk"] += 1 if as_bool(perf.get("no_primary_image_priority_hints")) else 0
    deductions["Performance Risk"] += 1 if as_bool(perf.get("repeated_third_party_bloat")) else 0

    deductions["Hygiene"] += 1 if as_bool(hygiene.get("h1_issues")) else 0
    deductions["Hygiene"] += 1 if as_bool(hygiene.get("og_issues")) else 0
    deductions["Hygiene"] += 1 if as_bool(hygiene.get("twitter_issues")) else 0
    deductions["Hygiene"] += ceil_units(as_float(hygiene.get("percent_images_missing_alt")), 50, 1)
    deductions["Hygiene"] += 1 if as_bool(hygiene.get("url_structure_issues")) else 0
    deductions["Hygiene"] += 1 if as_bool(hygiene.get("data_quality_issues")) else 0

    breakdown = {
        category: max(0, CATEGORY_MAX[category] - deductions[category])
        for category in CATEGORY_MAX
    }
    breakdown["Total"] = sum(breakdown.values())
    return breakdown


def main() -> int:
    parser = argparse.ArgumentParser()
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
    errors, warnings = validate_metrics(metrics)
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    breakdown = compute_breakdown(metrics)
    audit_mode = metrics["audit_context"]["audit_mode"]

    if args.pretty:
        print(f"INTERNAL SEO SCORE: {breakdown['Total']}/100")
        print(f"AUDIT MODE: {audit_mode}")
        for category, maximum in CATEGORY_MAX.items():
            print(f"- {category}: {breakdown[category]}/{maximum}")
        for warning in warnings:
            print(f"- warning: {warning}")
        return 0

    payload = {
        "audit_mode": audit_mode,
        "warnings": warnings,
        "breakdown": breakdown,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

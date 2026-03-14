# Catalog Data Quality Checks

## Contents

1. Product data quality
2. Collection data quality
3. Pricing analysis
4. Tag analysis

All checks use data from public `/products.json` and `/collections.json` endpoints.

**Important limitation:** The public `/products.json` endpoint does NOT return image `alt` text. Alt text requires Admin API access. Flag this as a known gap.

---

## 1. Product Data Quality

### 1.1 Empty/Missing Descriptions

- **Check:** `body_html` is null, empty, or only whitespace/empty HTML tags after stripping
- **Threshold:** Any product with no description is critical
- **Impact:** Zero content = zero ranking for long-tail queries. AI engines cannot extract product attributes. Google Merchant Center may disapprove.

### 1.2 Thin Descriptions

- **Check:** Word count of `body_html` after stripping HTML tags

| Word Count | Rating |
|---|---|
| 0 | Critical — no content |
| 1-49 | Critical — placeholder |
| 50-99 | Poor — insufficient for SEO or purchase decisions |
| 100-149 | Thin — below minimum recommendation |
| 150-299 | Adequate — meets minimum bar |
| 300-500 | Good — ideal range |
| 500+ | Excellent — deep content for complex/expensive products |

- **Impact:** Pages under 150 words correlate with poor rankings. AI needs 40-60 words minimum to form a coherent product summary.

### 1.3 Duplicate Descriptions

- **Check:** Strip HTML, normalize whitespace, lowercase, hash. Group by hash. Any group > 1 = duplicates.
- **Threshold:** Exact duplicates always bad. > 85% text similarity across different products = problematic.
- **Impact:** Google picks one canonical and suppresses the rest. AI may treat duplicated content as low-quality.

### 1.4 Missing `product_type`

- **Check:** `product_type` is null or empty string
- **Threshold:** 0% missing is the target
- **Impact:** Feeds Google Shopping categorization. AI engines use product categorization to match queries. Breaks collection automation.

### 1.5 Inconsistent `product_type` Values

- **Check:** Group `product_type` by `toLowerCase()`. Multiple original forms per group = inconsistency.
- **Also flag:** Single-use types (only 1 product), overly granular types (e.g., "Blue Cotton T-Shirt" instead of "T-Shirts")
- **Threshold:** Each unique type (case-normalized) should appear on 3+ products. Total unique types should be < 20% of total products.
- **Impact:** Weakens site taxonomy signals. Confuses AI recommendations.

### 1.6 Inconsistent `vendor` Values

- **Check:** Group `vendor` by `toLowerCase().trim()`. Multiple originals per group = inconsistency.
- **Threshold:** Zero tolerance. One canonical form per logical vendor.
- **Impact:** Creates separate vendor filter URLs for each variant. AI may treat different casings as different brands.

### 1.7 Products with Zero Images

- **Check:** `images.length === 0`
- **Threshold:** Critical. 0% of products should have zero images.
- **Impact:** Excluded from Google Images. AI Shopping features cannot validate visually. Google Merchant Center disapproves.

### 1.8 Products with Only 1 Image

- **Check:** `images.length === 1`
- **Threshold:** Best practice is 3+ images per product
- **Impact:** Fewer Google Image Search entry points. Customers expect multiple angles.

### 1.9 Products Priced at Zero

- **Check:** All variants have `price` of "0.00" or price is null
- **Threshold:** Flag all zero-priced products for review. Only legitimate for free samples or subscription products.
- **Impact:** Schema validation warnings. Google Merchant Center disapproves. Visitors assume the site is broken.

### 1.10 Missing compare_at_price (Opportunity)

- **Check:** Percentage of products where ALL variants have `compare_at_price === null`
- **Threshold:** Not inherently wrong. Report as opportunity if 0% of products use it.
- **Impact:** No strikethrough pricing in search results or ads.

### 1.11 compare_at_price Abuse

- **Check:** Percentage of variants with `compare_at_price` set and > `price`
- **Thresholds:**
  - Warning: > 60% of products on sale
  - Critical: > 80% of products on sale
  - Red flag: uniform discount percentages across catalog
- **Impact:** Legal risk (deceptive pricing lawsuits doubling). Google Merchant Center disapprovals. Erodes trust.

### 1.12 Missing SKU on Variants

- **Check:** `variant.sku` is null or empty
- **Threshold:** All variants should have SKUs
- **Impact:** Marketplace readiness. AI Shopping needs unique identifiers. Operations break.

### 1.13 Missing Tags

- **Check:** `tags` is empty string or blank
- **Threshold:** Warning level — not all stores use tags extensively
- **Impact:** Products may not appear in smart collections. Weakens internal organization.

### 1.14 Default Variant Title

- **Check:** `variants.length === 1 && variants[0].title === "Default Title"`
- **Threshold:** Informational. In fashion/apparel, > 90% single-variant is suspicious.
- **Impact:** Missed opportunity for size/color variants that capture more search queries.

---

## 2. Collection Data Quality

### 2.1 Empty Collection Descriptions

- **Check:** `body_html` null or empty after stripping HTML
- **Threshold:** Critical — collections are the most important ranking pages for category keywords
- **Impact:** No content for Google to rank for category queries. AI cannot understand what the store sells at category level.

### 2.2 Thin Collection Descriptions

| Word Count | Rating |
|---|---|
| 0 | Critical |
| 1-49 | Poor |
| 50-99 | Thin |
| 100-150 | Adequate |
| 150-300 | Good |
| 300+ | Excellent |

### 2.3 Collections with Zero Products

- **Check:** Fetch `/collections/{handle}/products.json` — empty result
- **Threshold:** Flag all empty collections
- **Impact:** Thin content. Wasted crawl budget. Bounce on landing.

### 2.4 Too Few Collections

- **Check:** Ratio of total products to total collections
- **Thresholds:**
  - Warning: < 5 collections for > 50 products
  - Critical: < 10 collections for > 200 products
  - Ideal: average 10-50 products per collection
- **Impact:** Fewer ranking opportunities for category keywords. Flat catalogs harder for AI to parse.

### 2.5 Generic Collection Titles

- **Check:** Match against generic terms: "sale", "new", "all", "products", "misc", "other", "collection", "home", "frontpage"
- **Threshold:** Flag any single-word generic title
- **Impact:** Collection title becomes H1 and URL slug. "Products" has zero keyword value.

### 2.6 Missing Collection Images

- **Check:** `image` is null
- **Threshold:** All customer-facing collections should have images
- **Impact:** Poor Google Image Search presence. Unfinished appearance. Weak social previews.

---

## 3. Pricing Analysis

### 3.1 Price Distribution Anomalies

- **Check:** Within each `product_type`, calculate mean and standard deviation. Flag products with Z-score > 2.
- **Also flag:** Unusual decimal values that suggest data entry errors. Dramatic price differences between variants of the same product.
- **Impact:** Suggests data entry errors. Can cause Google Merchant Center disapprovals.

### 3.2 Pricing Consistency Within Collections

- **Check:** For each collection, compute coefficient of variation of prices
- **Threshold:** Coefficient of variation > 1.5 in a product-type collection = possible miscategorization
- **Impact:** Price consistency signals proper categorization.

---

## 4. Tag Analysis

### 4.1 Tag Statistics

Report:
- Total unique tags across catalog
- Average tags per product
- Tags used only once (orphan tags)
- Top 20 most-used tags
- Tags with inconsistent casing

### 4.2 Over-Tagging

- **Check:** Count tags per product
- **Thresholds:**
  - Good: 3-10 tags per product
  - Warning: 11-20 tags per product
  - Over-tagged: 21+ tags per product
  - If total unique tags > 20% of total products, tag system is too granular

### 4.3 Tag URL Crawl Trap Risk

Every tag creates URLs like `/collections/{collection-handle}/{tag}`. These are near-duplicate pages.

- **Check:** `unique_tags × total_collections` = potential tag URLs
- **Thresholds:**
  - Warning: potential tag URLs > 5x product count
  - Critical: potential tag URLs > 10x product count
- **Impact:** Massive crawl budget waste. Google may not reach important pages.

### 4.4 Tag Inconsistencies

- **Check:** Group tags by `toLowerCase().trim()`. Multiple original forms = inconsistency.
- **Threshold:** Zero tolerance
- **Impact:** Creates separate filter pages per variant, multiplying duplicate content.

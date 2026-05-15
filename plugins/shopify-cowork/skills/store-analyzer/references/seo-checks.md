# SEO Checks

## Contents

1. Structured data and merchant listings
2. Titles and snippets
3. Canonicals and URL consolidation
4. Robots.txt and sitemap
5. Product content depth
6. Collection and information architecture
7. Blog and editorial content
8. Performance proxies
9. Internal linking
10. Lower-priority hygiene

## Evidence Rules

Label every major finding:

- `Catalog-wide`: verified from public endpoints, sitemap, or robots.txt across the store.
- `Sampled`: verified only on the fetched HTML sample.
- `Inference`: a reasoned interpretation of verified data. Mark it, not state it as fact.

Use calibrated language:

- Prefer: `limits`, `reduces`, `can prevent`, `may dilute`, `is likely hurting`
- Avoid unless proven: `penalizing`, `guarantees`, `can't index`, `this is why traffic dropped`

---

## 1. Structured Data and Merchant Listings

### 1.1 Product Schema Presence

Check sampled product pages for `<script type="application/ld+json">` containing `@type: Product`.

Shopify Dawn v15.0+ uses a `structured_data` Liquid filter that auto-generates basic Product JSON-LD. It includes: `name`, `description`, `image`, `brand.name`, `category`, `offers` (price, priceCurrency, availability, url).

**What is missing from Shopify defaults:**
- `aggregateRating` — no star ratings in SERPs
- `review` — no review snippets
- `sku` / `gtin` / `mpn` — critical for Google Merchant Center matching
- `shippingDetails` — no shipping badge in SERPs
- `hasMerchantReturnPolicy` — no return policy badge
- `ProductGroup` with `hasVariant` — Google's recommended variant handling
- `BreadcrumbList` — no breadcrumb rich results
- `Organization` — no knowledge panel eligibility

### 1.2 Required Merchant Listing Fields

Google requires these for Product rich results:

- `name`
- `image`
- `offers.price`
- `offers.priceCurrency`
- `offers.availability`

### 1.3 Recommended Commerce Fields

Fields that improve rich result quality and eligibility:

- `brand.name`
- `sku`, `gtin`, or `mpn` (at least one product identifier)
- `aggregateRating` with `ratingValue` and `reviewCount`
- `review` array with individual reviews
- `shippingDetails`
- `hasMerchantReturnPolicy`
- `description` (substantive, not one-line)
- `itemCondition`

### 1.4 Variant Handling

Check whether variants are represented as:
- Single `Offer` (loses variant-specific search matches)
- Multiple `Offer` objects within one `Product`
- `ProductGroup` with `hasVariant` array (Google's recommended approach since 2023)

### 1.5 Schema Validation

Check for:
- Duplicate or conflicting schema blocks on the same page
- Malformed URLs in schema
- Price in schema matching price displayed on page
- Description in schema matching visible product description
- Server-rendered JSON-LD (not JavaScript-injected) — Google requires SSR for merchant listings

**Framing (use business language):**
- Strong: "Google can't show star ratings, shipping badges, or return policy info for your products in search results — because the required data fields are missing from your product markup."
- Moderate: "Google can show basic product info in search, but shoppers won't see reviews, shipping speed, or return policy — which means lower click-through rates vs. competitors who have them."
- Caution: if JSON-LD is absent from server-rendered HTML, say it may be client-side and recommend Google Rich Results Test.

---

## 2. Titles and Snippets

**Research-backed guidance:** Google uses multiple sources to determine title links and can rewrite them; there is no fixed character-count guarantee. Meta descriptions are "sometimes" used for snippets; snippets are truncated "as needed." Do NOT penalise based on character counts alone.

Check sampled pages for:

- **Missing titles** — pages with no `<title>` tag at all
- **Missing meta descriptions** — pages with no `<meta name="description">`
- **Mass-duplicated titles** — identical title pattern across many pages with no product/category differentiation
- **Misleading titles** — title content that does not match visible page intent
- Titles that exactly match product names with no modifiers (low priority — note only)
- Descriptions that appear templated or generic (low priority — note only)

**Do NOT flag or penalise:**
- Title "too short" (under 60 chars) or "too long" (over 60 chars) — Google rewrites titles freely
- Meta description "over 160 characters" — Google truncates dynamically, no fixed limit
- Character-count ranges as findings — these are not actionable

**Framing (use business language):**
- Strong: "When someone Googles your product category, your search result has the same generic title as 200 other pages — so shoppers have no reason to click yours over a competitor's."
- Lower: titles are present and differentiated but not "optimised" — do not flag as a finding.

---

## 3. Canonicals and URL Consolidation

### 3.1 Product Canonical URLs

Every product page must have `<link rel="canonical">` pointing to `/products/{handle}`.

**Critical Shopify issue:** Products are accessible at both `/products/{handle}` and `/collections/{collection}/products/{handle}`. The canonical must resolve to the clean URL.

### 3.2 Collection-Prefixed Internal Links

Check `<a>` tags on collection pages linking to products. Shopify themes using `within: collection` in Liquid generate `/collections/{collection}/products/{handle}` links. These dilute link equity toward non-canonical URLs.

### 3.3 Tag Page Thin Content

Shopify tag pages (`/collections/{collection}/{tag}`) can create massive thin content problems:
- Each tag generates a filterable URL (e.g., `/collections/earrings/gold`, `/collections/earrings/silver`)
- These pages typically have no unique title, no unique description, and no unique content — just a filtered subset of the parent collection
- Stores with many tags can generate hundreds or thousands of thin indexed pages

**Detection:** Check the sitemap for URLs matching `/collections/*/` patterns beyond the main collection handles. Cross-reference with `robots.txt` — Shopify's default blocks `/collections/*+*` (multi-tag combos) but single-tag pages may still be indexable. Also check sampled tag page HTML for missing or duplicated titles/descriptions.

- If hundreds of tag pages exist with no unique content: "Your store has {n} tag-filtered collection pages indexed with no unique descriptions — Google sees these as thin, duplicate content that dilutes your collection pages' ranking power."
- Severity: HIGH (when hundreds exist), MEDIUM (when dozens exist)

### 3.4 Other Canonical Issues

- Inconsistent protocol or host in canonicals
- Tag or filter URL patterns creating duplicates (`/collections/{handle}/{tag}`)
- Sort parameter URLs not blocked or canonicalized
- Paginated collection pages — check if page 2+ canonicalizes properly

**Framing (use business language):**
- Strong: "Google sees two different URLs for the same product and has to guess which one to show — this splits your ranking power between them instead of concentrating it on one page."
- Avoid: `duplicate content penalty`. Better framing: diluted consolidation, crawl waste, mixed signals.

---

## 4. Robots.txt and Sitemap

**Research-backed guidance:** Shopify auto-generates `robots.txt`, `sitemap.xml`, canonical tags, and SSL on all theme-based stores. These are NOT differentiators — treat them as **pass/fail**. Only flag if broken, missing, or customised in a way that harms crawling.

### 4.1 Robots.txt Checks

Shopify's default blocks:

| Should be blocked | Why |
|---|---|
| `/admin`, `/cart`, `/checkout`, `/orders`, `/account` | Private pages |
| `/search` | Internal search — thin/duplicate |
| `/collections/*+*` | Tag-filtered collection pages |
| `/collections/*sort_by*` | Sorted collection views |
| `/*preview_theme_id*` | Theme previews |
| `/policies/` | Auto-generated policy pages |

**Pass/fail:** If these rules are present (Shopify default), mark as passing and move on. Only flag as a finding if rules are missing due to customisation or if critical paths are accidentally blocked.

### 4.1b Storebot-Google Access

Google operates a dedicated shopping crawler (`Storebot-Google`, user-agent token `Storebot-Google`) separate from Googlebot. It crawls product pages specifically for Google Shopping surfaces including AI Shopping features.

**Detection:** Check `robots.txt` for any `User-agent: Storebot-Google` directive with `Disallow`. Also check for broad wildcard blocks that might inadvertently catch it.

- If blocked: "Google's Shopping crawler is blocked — your products won't appear in Google Shopping results, product carousels, or AI Shopping recommendations."
- Severity: HIGH

### 4.2 Sitemap Checks

- Sitemap accessible at `/sitemap.xml` (HTTP 200, valid XML)
- Sub-sitemaps present: products, collections, pages, blogs

**Pass/fail:** If sitemap is standard Shopify-generated, mark as passing. Only flag if sitemap is missing, returns errors, or if headless build lacks proper sitemap generation.

**Framing:**
- These checks exist to catch breakage, not to award points for Shopify defaults.
- Do not claim indexation failure unless pages are actually blocked or noindexed.
- For headless Shopify (Hydrogen): these become meaningful checks since they require explicit configuration.

---

## 5. Product Content Depth

Measure from `/products.json` catalog-wide:

| Metric | How to measure |
|---|---|
| Products with empty descriptions | `body_html` null, empty, or whitespace-only after stripping HTML |
| Products with thin descriptions | Word count after stripping HTML: < 50 = critical, 50-99 = poor, 100-149 = thin |
| Products with adequate descriptions | 150-299 words |
| Products with good descriptions | 300+ words |
| Duplicate description groups | Hash stripped descriptions, group by hash |
| Products with zero images | `images.length === 0` |
| Products with single image only | `images.length === 1` (best practice is 3+) |

**Framing (use business language):**
- Strong: "X% of your products have little or no description — Google has nothing to rank them for, and shoppers can't make a buying decision. These pages are effectively invisible in search."
- Collection pages usually outrank isolated product pages for category intent, so product hygiene should not outrank collection content gaps.

---

## 6. Collection and Information Architecture

Measure from `/collections.json` catalog-wide:

| Metric | How to measure |
|---|---|
| Collections with empty descriptions | `body_html` null or empty |
| Collections with thin descriptions | < 50 words after stripping HTML |
| Collections with zero products | Fetch `/collections/{handle}/products.json` — empty result |
| Too few collections | Ratio of products to collections > 25:1 suggests under-categorization |
| Generic collection titles | Titles like "Sale", "All", "Products", "New" miss keyword opportunities |
| Missing collection images | `image` null |

**Framing (use business language):**
- "Collection pages are your best chance to rank when someone searches for a product category like 'gold jhumkas' or 'oxidized earrings'. With only {n} collections for {n} products, you're missing the pages that would bring in category shoppers."
- This is often the highest-leverage ecommerce finding. A store with 50 products and 3 collections is leaving ranking opportunities on the table.

---

## 7. Blog and Editorial Content

Check from sitemap and sampled articles:

- Blog sub-sitemap exists
- Article pages have unique titles and descriptions
- Article pages have Article JSON-LD schema
- Articles have clear H1 tags
- Articles internally link to collections or products
- Content is substantive (not auto-generated filler)

**Framing (use business language):**
- If no blog detected: `not detected from public sitemap data`.
- If blog exists but articles are weak: "Your blog posts don't link to your products or collections — each article is a missed chance to send Google (and readers) to pages where they can actually buy."

---

## 8. Performance Proxies

**Research-backed guidance:** These are micro-optimisations. Missing `fetchpriority`, image dimensions, or preload hints are NOT findings for established stores. Mention in passing only. Never make these a standalone finding.

From sampled HTML, check:

| Check | What to look for | Status |
|---|---|---|
| LCP image lazy-loaded | `<img>` with `loading="lazy"` on hero/main product image | Informational — mention if found |
| Missing `fetchpriority="high"` | Hero image lacks `fetchpriority="high"` | Informational only — never a finding |
| Missing image dimensions | `<img>` without `width` and `height` attributes | Informational only — never a finding |
| High external script count | Count unique external script domains | Note if extreme (15+), but not a standalone finding |
| Render-blocking resources | `<script>` without `async`/`defer` in `<head>` | Informational — recommend PageSpeed Insights |
| No preload hints | Missing `<link rel="preload">` for hero image or critical font | Informational only |
| Font loading | Missing `font-display: swap` in CSS | Informational only |

**Framing:**
- These are proxy checks only — **never elevate to a finding**.
- Recommend PageSpeed Insights or Lighthouse for confirmation.
- Do not claim failed Core Web Vitals from HTML alone.
- AI citation readiness is not affected by these performance signals.

---

## 9. Internal Linking

| Check | What to look for | Why it matters |
|---|---|---|
| Collection-prefixed product links | `<a>` hrefs containing `/collections/{x}/products/` | Dilutes link equity to non-canonical URLs |
| Breadcrumbs present | `<nav>` with breadcrumb semantics or `aria-label="breadcrumb"` | Navigation clarity + rich results |
| BreadcrumbList JSON-LD | `@type: BreadcrumbList` in JSON-LD | Enables breadcrumb rich results |
| Related products section | "Related Products" / "You May Also Like" section exists | Deepens internal linking |
| Footer/nav links to collections | Key collections linked from sitewide navigation | Collections in nav get maximum PageRank |

---

## 10. Lower-Priority Hygiene

**Research-backed guidance:** OG/Twitter tags are social preview metadata, not AI citation readiness signals. Google's AI eligibility is framed around indexing/snippet eligibility, not social tags. Image alt text helps image understanding but citations are grounded on textual evidence. Do not weight these for AI readiness.

Report but do not headline:

- Open Graph tag issues — **not an AI citation factor**; social preview only
- Twitter card issues — **not an AI citation factor**; social preview only
- H1 count issues (multiple H1s or missing H1) — low priority, note only
- **Dawn theme H1-on-logo** — Shopify's Dawn theme (800K+ stores, v15.0+) wraps the header logo/site title inside `<h1>` tags on every page. This means the store name is the H1 instead of the product title or collection name. Check if the homepage `<h1>` contains only the brand/logo rather than page-specific content. If found on product/collection pages, this is a **MEDIUM** finding — Google uses H1 to understand page topic, and a generic brand name H1 on every page weakens that signal. Detection: check if the `<h1>` text on product pages matches the store name rather than the product title.
- URL handle quality — score only for unreadable/parameter-junk URLs, not keyword presence
- Missing alt text on sampled images — gate to primary product images and images carrying essential info only (note: alt text is NOT in `/products.json`)
- Empty `product_type` or messy vendor values (covered more deeply in catalog-checks.md)

**Do NOT include in AI readiness scoring:**
- OG/Twitter tag completeness
- Favicon presence
- Meta keywords (Google explicitly ignores this tag)
- `rel=prev/next` pagination tags (Google no longer uses these)

Use clear downgrade language: `Real but secondary`, `Worth fixing in bulk`, `Good cleanup after higher-leverage work`.

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

**Framing:**
- Strong: sampled pages appear ineligible or weakly eligible for merchant listing enhancements.
- Moderate: markup exists but recommended fields are thin or inconsistent.
- Caution: if JSON-LD is absent from server-rendered HTML, say it may be client-side and recommend Google Rich Results Test.

---

## 2. Titles and Snippets

Check sampled pages for:

- Title tags under 30 or over 60 characters
- Repetitive title templates across sampled pages
- Titles that exactly match product names with no modifiers
- Missing meta descriptions
- Meta descriptions over 160 characters (truncation)
- Descriptions that appear templated or generic
- Identical title pattern across product pages (e.g., "{product} | {store}")

**Framing:**
- Strong: default or repetitive snippets leave ranking and CTR opportunity on the table.
- Lower: titles are acceptable but not differentiated.

---

## 3. Canonicals and URL Consolidation

### 3.1 Product Canonical URLs

Every product page must have `<link rel="canonical">` pointing to `/products/{handle}`.

**Critical Shopify issue:** Products are accessible at both `/products/{handle}` and `/collections/{collection}/products/{handle}`. The canonical must resolve to the clean URL.

### 3.2 Collection-Prefixed Internal Links

Check `<a>` tags on collection pages linking to products. Shopify themes using `within: collection` in Liquid generate `/collections/{collection}/products/{handle}` links. These dilute link equity toward non-canonical URLs.

### 3.3 Other Canonical Issues

- Inconsistent protocol or host in canonicals
- Tag or filter URL patterns creating duplicates (`/collections/{handle}/{tag}`)
- Sort parameter URLs not blocked or canonicalized
- Paginated collection pages — check if page 2+ canonicalizes properly

**Framing:**
- Strong: internal links and crawl rules expose multiple URL forms for the same content.
- Avoid: `duplicate content penalty`. Better framing: diluted consolidation, crawl waste, mixed signals.

---

## 4. Robots.txt and Sitemap

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

Check whether these rules are present. Missing rules = crawl traps.

### 4.2 Sitemap Checks

- Sitemap accessible at `/sitemap.xml` (HTTP 200, valid XML)
- Sub-sitemaps present: products, collections, pages, blogs
- Product count in sitemap roughly matches `meta.json` published count
- Image metadata present in product sitemap entries (`<image:image>`)
- No 404 or redirect URLs in sitemap
- `<lastmod>` dates present and plausible

**Framing:**
- Strong: crawl traps or missing sitemap coverage waste crawl attention.
- Do not claim indexation failure unless pages are actually blocked or noindexed.

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

**Framing:**
- Strong: empty or thin product pages give Google little unique text to rank.
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

**Framing:**
- This is often the highest-leverage ecommerce finding.
- Collection pages are the best organic landing pages for category-intent searches.
- A store with 50 products and 3 collections is leaving ranking opportunities on the table.

---

## 7. Blog and Editorial Content

Check from sitemap and sampled articles:

- Blog sub-sitemap exists
- Article pages have unique titles and descriptions
- Article pages have Article JSON-LD schema
- Articles have clear H1 tags
- Articles internally link to collections or products
- Content is substantive (not auto-generated filler)

**Framing:**
- If no blog detected: `not detected from public sitemap data`.
- If blog exists but articles are weak: note the missed internal-linking and topical authority opportunity.

---

## 8. Performance Proxies

From sampled HTML, check:

| Check | What to look for | Why it matters |
|---|---|---|
| LCP image lazy-loaded | `<img>` with `loading="lazy"` on hero/main product image | 59% of Shopify stores do this; adds ~3 seconds to LCP |
| Missing `fetchpriority="high"` | Hero image lacks `fetchpriority="high"` | Tells browser to prioritize the most important image |
| Missing image dimensions | `<img>` without `width` and `height` attributes | Causes CLS as images load |
| High external script count | Count unique external script domains | Each domain adds DNS lookup + connection time |
| Render-blocking resources | `<script>` without `async`/`defer` in `<head>` | Delays First Contentful Paint |
| No preload hints | Missing `<link rel="preload">` for hero image or critical font | Increases LCP |
| Font loading | Missing `font-display: swap` in CSS | Invisible text during font load |

**Framing:**
- These are proxy checks only.
- Recommend PageSpeed Insights or Lighthouse for confirmation.
- Do not claim failed Core Web Vitals from HTML alone.

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

Report but do not headline:

- Open Graph tag issues
- Twitter card issues
- H1 count issues (multiple H1s or missing H1)
- URL handle quality (keyword-relevant vs. auto-generated)
- Missing alt text on sampled images (note: alt text is NOT in `/products.json`)
- Empty `product_type` or messy vendor values (covered more deeply in catalog-checks.md)

Use clear downgrade language: `Real but secondary`, `Worth fixing in bulk`, `Good cleanup after higher-leverage work`.

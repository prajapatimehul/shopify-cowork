# Troubleshooting

## Contents

1. Public catalog endpoints blocked
2. Anti-bot or rate-limit responses
3. JSON-LD not visible in HTML
4. Incomplete collection or page data
5. Sitemap and metadata mismatches
6. Blog detection edge cases
7. llms.txt detection issues
8. AI bot blocking ambiguity
9. Review widget detection
10. How to phrase partial-evidence findings

---

## 1. Public Catalog Endpoints Blocked

If `products.json` returns 401, 403, empty, or unusable data:

- Say the full catalog audit cannot be completed from public endpoints
- Do not estimate product counts or description coverage
- You may still review sampled pages, but downgrade scope to sampled only
- GEO and AEO checks on sampled HTML can still proceed

Phrasing: `The store does not expose usable public Shopify catalog data, so catalog-wide product and collection analysis is not possible from public endpoints alone. Sampled HTML analysis and GEO/AEO checks are still included.`

## 2. Anti-Bot or Rate-Limit Responses

If you encounter 429s, intermittent failures, or bot protection:

- Slow down requests
- Reduce sample breadth if needed
- Do not pretend missing pages were checked

Phrasing: `Some public pages were intermittently blocked by anti-bot or rate-limit behavior, so HTML findings are based on the pages that rendered successfully.`

## 3. JSON-LD Not Visible in HTML

Shopify apps frequently inject JSON-LD client-side (via JavaScript).

If server-rendered HTML does not show JSON-LD:

- Do not declare the store lacks structured data sitewide
- Say it was not visible in sampled server-rendered HTML
- Recommend Google's Rich Results Test for confirmation
- Score the structured data section with a note about client-side possibility

Phrasing: `Structured data was not visible in the sampled server-rendered HTML. Shopify apps often inject this client-side, so confirm with Google's Rich Results Test before treating it as absent.`

## 4. Incomplete Collection or Page Data

If `collections.json` or `pages.json` is sparse, empty, or inconsistent:

- Say those public endpoints appear limited
- Avoid catalog-wide claims about collection coverage
- Use sitemap and sampled HTML where possible

## 5. Sitemap and Metadata Mismatches

If product counts in `meta.json` and sitemap do not match:

- Note the mismatch as a data quality concern
- Do not assume one source is authoritative
- The mismatch itself is the finding

Phrasing: `The public product count in meta.json does not match the product sitemap count, which makes crawl coverage harder to validate from public data.`

## 6. Blog Detection Edge Cases

If no blog sitemap is present:

- Say `blog or article content not detected from the public sitemap`
- Do not claim the store has no blog at all

If article URLs exist but are hard to sample:

- Keep blog findings sampled and narrow

## 7. llms.txt Detection Issues

`/llms.txt` may return:

- 404 — file does not exist (most common)
- 200 with valid Markdown — file exists and is properly structured
- 200 with HTML — the store redirected to homepage or an error page (not a real llms.txt)
- 301/302 redirect — follow and check final destination

Check the `Content-Type` header. A real llms.txt should be `text/plain` or `text/markdown`, not `text/html`.

## 8. AI Bot Blocking Ambiguity

Shopify controls the default robots.txt for all stores. When AI bots are blocked:

- Distinguish between Shopify's defaults and merchant-chosen rules
- Note that merchants can customize via `robots.txt.liquid` but many do not know
- Mention that Cloudflare may add a second blocking layer beyond robots.txt
- Do not imply the merchant deliberately chose to block AI bots — it is likely Shopify's default

Phrasing: `AI search bots are currently blocked — this appears to be Shopify's platform default. Merchants can customize this via robots.txt.liquid.`

## 9. Review Widget Detection

Third-party review apps (Judge.me, Yotpo, Stamped, Loox) inject via JavaScript. If no review elements are visible in server-rendered HTML:

- Check `<script>` tags for known review platform CDN domains
- Look for placeholder `<div>` elements with review-related IDs or classes
- If nothing found, note that reviews may still exist via client-side injection

Do not say "the store has no reviews" — say "no review widget was detected in the server-rendered HTML."

## 10. How to Phrase Partial-Evidence Findings

Use these fallbacks:

- `Catalog-wide finding unavailable from public data`
- `Sampled finding only`
- `Inference from visible page patterns`
- `Cannot determine from public endpoints — recommend Admin API check`

Avoid when evidence is partial:

- `every page`
- `the whole store`
- `Google can't index this`
- `this is definitely the reason`

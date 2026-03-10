# SEO Audit Troubleshooting

## Contents

1. Public catalog endpoints blocked
2. Anti-bot or rate-limit responses
3. JSON-LD not visible in HTML
4. Incomplete collection or page data
5. Sitemap and metadata mismatches
6. Blog detection edge cases
7. How to phrase partial-evidence findings

## 1. Public Catalog Endpoints Blocked

If `products.json` returns 401, 403, empty, or unusable data:

- say the full catalog audit cannot be completed from public Shopify endpoints
- do not estimate product counts or description coverage
- you may still review sampled public pages, but clearly downgrade the scope to sampled only

Recommended phrasing:

- `The store does not expose usable public Shopify catalog data, so a full catalog-wide audit is not possible from public endpoints alone.`

## 2. Anti-Bot or Rate-Limit Responses

If you encounter 429s, intermittent failures, or bot protection:

- slow down requests
- reduce page-sample breadth if needed
- avoid pretending the missing pages were checked

Recommended phrasing:

- `Some public pages were intermittently blocked by anti-bot or rate-limit behavior, so HTML findings below are based on the pages that rendered successfully.`

## 3. JSON-LD Not Visible in HTML

Shopify apps frequently inject JSON-LD client-side.

If the server-rendered HTML does not show JSON-LD:

- do not declare the store lacks structured data sitewide
- say it was not visible in sampled server-rendered HTML
- recommend validation in Google's Rich Results Test

Recommended phrasing:

- `Structured data was not visible in the sampled server-rendered HTML. Shopify apps often inject this client-side, so confirm with Google's Rich Results Test before treating it as absent.`

## 4. Incomplete Collection or Page Data

If `collections.json` or `pages.json` is sparse, empty, or inconsistent:

- say those public endpoints appear limited
- avoid catalog-wide claims about pages or collection coverage unless the evidence supports it
- continue using sitemap and sampled HTML where possible

## 5. Sitemap and Metadata Mismatches

If product counts in `meta.json` and the sitemap do not line up:

- note the mismatch as a crawlability or data-quality concern
- do not assume one source is authoritative without explaining why
- keep the mismatch itself as the finding

Recommended phrasing:

- `The public product count in meta.json does not match the product sitemap count, which makes crawl coverage harder to validate cleanly from public data.`

## 6. Blog Detection Edge Cases

If no blog sitemap is present:

- say `blog or article content not detected from the public sitemap`
- do not claim the store has no blog at all unless you verified it another way

If article URLs exist but are hard to sample:

- keep blog findings sampled and narrow

## 7. How to Phrase Partial-Evidence Findings

Use these fallbacks when the audit is incomplete:

- `Catalog-wide finding unavailable from public data`
- `Sampled finding only`
- `Inference from visible page patterns`

Avoid these when evidence is partial:

- `every page`
- `the whole store`
- `Google can't index this`
- `this is definitely the reason traffic is down`

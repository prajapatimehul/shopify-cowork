# SEO Audit Testing

## Contents

1. Trigger tests
2. Non-trigger tests
3. Audit review tests
4. Functional acceptance checks
5. Overtriggering and undertriggering signals

## 1. Trigger Tests

These prompts should trigger the skill:

1. `Audit this Shopify store and tell me the top SEO fixes: example.com`
2. `Review this Shopify SEO audit and tell me what is real vs overstated for themancompany.com`
3. `Check whether this Shopify store has weak collection pages and thin product content`
4. `Give me a technical SEO audit for this Shopify domain and prioritize the issues`
5. `Sanity-check the SEO report for this Shopify store and tell me what the client should care about`
6. `Audit this Shopify store, but call out if public data is too limited for a full audit`

## 2. Non-Trigger Tests

These prompts should not trigger the skill:

1. `Audit this WordPress blog for SEO`
2. `Build me a backlink outreach plan`
3. `Write product descriptions for my Shopify store`
4. `Help me improve local SEO for my dental clinic`
5. `Analyze my Search Console export and explain the CTR drop`

## 3. Audit Review Tests

Use these when checking the report-review mode:

1. User provides a dramatic Shopify SEO report that calls alt text the `#1 fix`.
   Expected behavior:
   - verify the claim against store data
   - downgrade it if higher-leverage collection or product content issues exist
   - explain the difference between real issue and overstatement

2. User provides a report claiming `Google can't index these pages`.
   Expected behavior:
   - verify whether pages are blocked, inaccessible, or noindexed
   - if not, reframe the issue as thin content, weak schema, or poor crawl efficiency

3. User provides a score-heavy audit with few examples.
   Expected behavior:
   - separate score noise from evidence-backed findings
   - explain what matters to the client

4. User provides an audit that says `no meta descriptions` because `og:description` is missing.
   Expected behavior:
   - check the standard HTML meta description tag separately from Open Graph tags
   - downgrade the claim if only Open Graph tags are missing

5. User provides an audit that makes missing product tags a critical SEO issue.
   Expected behavior:
   - reclassify tags as secondary merchandising or internal-search hygiene
   - keep higher-leverage content, crawl, and schema issues above tags

## 4. Functional Acceptance Checks

A good audit should:

- identify whether the store is auditable from public Shopify endpoints
- return exact counts for products, collections, pages, and other catalog-wide findings
- sample product, collection, homepage, and article pages when available
- label key findings as `Catalog-wide`, `Sampled`, or `Inference`
- state whether the job is a `Full audit` or `Partial audit`
- prioritize collection and product content issues appropriately
- avoid unsupported ranking, penalty, or deindexation claims
- include a client-friendly top actions section
- distinguish standard meta description checks from Open Graph checks
- avoid treating product tags as a primary SEO issue

## 5. Overtriggering and Undertriggering Signals

Undertriggering signs:

- users say `audit this Shopify store` and the skill does not load
- users manually call out `SEO audit` or `technical SEO check` to force it
- the skill misses report-review requests that mention `Shopify SEO audit`

Overtriggering signs:

- the skill loads for generic SEO questions that are not Shopify-specific
- it loads for copywriting or content-generation tasks
- it loads for Search Console or GA4 analysis with no store-audit request

If undertriggering happens:

- add more user-language phrases to the description
- make the `when to use` language more explicit

If overtriggering happens:

- tighten the negative scope in the description
- make `Shopify store`, `Shopify domain`, and `audit` requirements more explicit

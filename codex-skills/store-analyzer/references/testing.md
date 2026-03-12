# Store Analyzer Testing

## Contents

1. Trigger tests
2. Non-trigger tests
3. Focused audit tests
4. Audit review tests
5. Functional acceptance checks
6. Overtriggering and undertriggering signals

## 1. Trigger Tests

These prompts should trigger the skill:

1. `Audit this Shopify store: example.com`
2. `Analyze this Shopify store for SEO and AI readiness`
3. `Check if AI search engines can find products from this store`
4. `Is this Shopify store optimized for ChatGPT and Perplexity?`
5. `Review this Shopify SEO audit and tell me what matters`
6. `Run a full SEO + GEO + AEO audit on this Shopify domain`
7. `Check whether this Shopify store can win featured snippets`
8. `How visible is this store to AI shopping assistants?`
9. `Audit this store: jhumka-8052.myshopify.com`
10. `Check the search visibility of this Shopify store`

## 2. Non-Trigger Tests

These prompts should NOT trigger the skill:

1. `Audit this WordPress blog for SEO`
2. `Build me a backlink outreach plan`
3. `Write product descriptions for my Shopify store`
4. `Help me improve local SEO for my dental clinic`
5. `Analyze my Search Console export and explain the CTR drop`
6. `Fix the product descriptions on my store` (should trigger store-fixer, not analyzer)
   Expected: hand off to `store-fixer`, not direct execution from analyzer. `store-fixer` should require approval before writes and a rollback path.
7. `Compare my store against competitors` (should trigger intel-competitors if it exists)
8. `Set up Google Ads for my store`

## 3. Focused Audit Tests

1. `Check if this Shopify store is visible to AI search engines` — should focus on GEO dimension (AI bot access, entity, citations)
2. `Can ChatGPT find products from this store?` — should focus on GEO
3. `Check whether this Shopify store has weak collection SEO` — should focus on SEO content/IA
4. `Is this store ready for featured snippets?` — should focus on AEO
5. `Check the structured data on this Shopify store` — should focus on SEO structured data + related GEO/AEO schema

## 4. Audit Review Tests

1. User provides a dramatic audit that calls alt text the #1 fix.
   Expected: verify against store data, downgrade if collection/product content issues are bigger.

2. User provides a report claiming "Google can't index these pages."
   Expected: verify whether pages are actually blocked. Reframe as thin content if not blocked.

3. User provides a score-heavy audit with no GEO/AEO coverage.
   Expected: note the missing dimensions. Add GEO and AEO findings.

## 5. Functional Acceptance Checks

A good audit should:

- Identify whether the store is auditable from public endpoints
- Return exact counts for products, collections, and catalog-wide findings
- Sample varied pages (not just the first handles)
- Label findings as `Catalog-wide`, `Sampled`, or `Inference`
- Cover all three dimensions (SEO, GEO, AEO) in a full audit
- Prioritize by business impact, not by how dramatic findings sound
- Use the flat report template: `BOTTOM LINE`, `SNAPSHOT`, `FINDINGS`, `SAMPLE FIXES`
- NEVER produce scores, dimension groupings, checkmark lists, or EXECUTIVE SUMMARY
- Stay within 80-120 lines for a full audit
- Include sample fixes using real products/collections
- Hand off implementation requests to `store-fixer` instead of attempting authenticated changes
- Apply the Finding Quality Bar: every finding must have provable revenue/traffic impact
- For established stores (500+ products, active reviews, proper schema): produce 4-6 findings, not 8-10
- Merge related issues (meta descriptions + thin titles = one finding, not two)
- Never pad the report with checkbox items (missing llms.txt, no HowTo schema, no Speakable, etc.)

## 5.1 Quality Bar Tests — Established Stores

When auditing a well-run store (500+ products, active reviews, proper Product schema):

1. Report should have 4-6 findings, not 8-10.
2. These should NOT appear as standalone findings:
   - "Missing llms.txt" (not a ranking factor)
   - "No HowTo schema" (irrelevant for non-instructional products)
   - "No comparison tables" (single-brand DTC stores don't need these)
   - "Missing Speakable schema" (beta, news-only)
   - "No Knowledge Panel" (most brands don't have one)
   - "Brand name inconsistency" when only difference is apostrophe in domain
   - "Missing fetchpriority on hero image" (micro-optimization)
3. GEO/AEO issues should be merged, not listed as 5+ separate findings.
4. The report must NOT contain ✓/✗ checkmark lists of what's working.
5. No scores anywhere in the output.

## 6. Overtriggering and Undertriggering Signals

Undertriggering:
- User says "audit this Shopify store" and skill does not load
- User says "check AI visibility" and skill does not load
- User says "is my store ready for ChatGPT?" and skill misses

Overtriggering:
- Skill loads for generic SEO questions not specific to Shopify
- Skill loads for content writing tasks
- Skill loads for Search Console/GA4 analysis
- Skill loads when user wants to FIX issues instead of handing off to `store-fixer`

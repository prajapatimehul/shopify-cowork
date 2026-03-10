# Shopify SEO Audit Template

Use the template that matches the task.

## Full Audit Template

```text
=====================================================
  SEO AUDIT — {domain}
  Powered by shopify-cowork
=====================================================

EXECUTIVE SUMMARY
  Audit mode:          {Full audit or Partial audit}
  Biggest issue:       {single highest-leverage finding}
  Best quick win:      {fastest credible improvement}
  Scope note:          {catalog-wide findings vs sampled findings}
  Score note:          Internal heuristic for prioritization only

STORE SNAPSHOT
  Store:               {name} ({myshopify_domain})
  Theme:               {schema_name} v{schema_version}
  Products:            {n}
  Collections:         {n}
  Pages:               {n}
  Blog:                {present / not detected from public sitemap}
  Currency:            {currency}
  Pages sampled:       {n} product pages + {n} collection pages + homepage {+ article pages if detected}
  Limitations:         {none, or the specific public-data gaps that downgraded the audit}

=====================================================
  TIER 1: HIGH-IMPACT SEARCH ISSUES
=====================================================

STRUCTURED DATA
  {findings}
  Scope:               {Sampled or Inference}
  Evidence:            {sample URLs checked}
  What this means:     {plain-English impact}

TITLES AND SNIPPETS
  {findings}
  Scope:               Sampled
  Evidence:            {sample URLs checked; standard meta descriptions only}

CANONICALS AND URL CONSOLIDATION
  {findings}
  Scope:               {Sampled or Catalog-wide}
  Evidence:            {sample URLs, robots.txt, sitemap}
  What this means:     {plain-English impact}

=====================================================
  TIER 2: CRAWLABILITY AND COMMERCIAL CONTENT
=====================================================

ROBOTS.TXT
  {findings}
  Scope:               Catalog-wide
  Evidence:            /robots.txt

SITEMAP
  {findings}
  Scope:               Catalog-wide
  Evidence:            /sitemap.xml, /meta.json

COLLECTIONS AND IA
  {findings}
  Scope:               Catalog-wide
  Evidence:            /collections.json, /sitemap.xml {+ sampled collection URLs if checked}
  What this means:     {plain-English impact}

PRODUCT CONTENT
  {n}/{total} products — no description
  {n}/{total} products — thin description
  {n}/{total} products — substantive description
  Scope:               Catalog-wide
  Evidence:            /products.json

PAGE SPEED PROXIES
  {findings}
  Scope:               Sampled
  Evidence:            {sample URLs checked}
  Recommendation:      Confirm with PageSpeed Insights or Lighthouse

=====================================================
  TIER 3: SECONDARY STRUCTURE AND CONTENT
=====================================================

BLOG OR EDITORIAL
  {findings}
  Scope:               {Catalog-wide + Sampled, or not detected}
  Evidence:            {blog sitemap, article URLs if checked}

PAGES
  {findings}
  Scope:               Catalog-wide
  Evidence:            /pages.json

=====================================================
  TIER 4: HYGIENE
=====================================================

  H1 Tags:             {summary}
  Open Graph:          {summary}
  Twitter Cards:       {summary}
  Image Alt Text:      {n}/{total} images missing alt text ({pct}%)
  URL Structure:       {summary}
  Data Quality:        {summary}

=====================================================
  TOP 5 ACTIONS
=====================================================

  #  Action                              Why
  -----------------------------------------------
  1  {highest-impact fix}                {outcome}
  2  {next fix}                          {outcome}
  3  {next fix}                          {outcome}
  4  {next fix}                          {outcome}
  5  {next fix}                          {outcome}

=====================================================
  SAMPLE FIXES
=====================================================

  "{real product or collection title}"
  -----------------------------------------------
  Current issue:   {missing copy / weak snippet / missing alt / schema gap}
  Suggested title: "{improved title if needed}"
  Suggested meta:  "{improved meta if needed}"
  Suggested copy:  "{improved description if needed}"
  Fix:             {specific action}

=====================================================
  INTERNAL SEO SCORE: {n}/100
=====================================================
  This is a prioritization heuristic, not a Google score.
  Audit completeness:  {Full audit or Partial audit}
  Structured Data:    {x}/15
  Titles & Snippets:  {x}/10
  URL Consolidation:  {x}/10
  Content Depth:      {x}/25
  Crawlability:       {x}/15
  Collection/Blog IA: {x}/15
  Performance Risk:   {x}/5
  Hygiene:            {x}/5
=====================================================
```

## Audit Review Template

```text
=====================================================
  SHOPIFY SEO AUDIT REVIEW — {domain}
=====================================================

BOTTOM LINE
  Most important real issue: {finding}
  Most overstated claim:     {finding}
  What should happen first:  {action}

SUPPORTED AND IMPORTANT
  - {claim}
    Scope: {Catalog-wide or Sampled}
    Evidence: {source}
    Why it matters: {plain-English impact}

SUPPORTED BUT SECONDARY
  - {claim}
    Evidence: {source}
    Why it is lower priority: {reason}

REAL BUT OVERSTATED
  - {claim}
    Evidence: {source}
    Why it is overstated: {scope, severity, or certainty problem}

UNSUPPORTED FROM CURRENT EVIDENCE
  - {claim}
    Evidence checked: {source}
    Why it does not hold up: {reason}

WHAT THE AUDIT MISSED
  - {missing issue}
    Scope: {Catalog-wide or Sampled}
    Evidence: {source}
    Why it matters more: {reason}
```

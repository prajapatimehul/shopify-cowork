# Report Templates

## Full Audit Template

```text
=====================================================
  STORE ANALYSIS — {domain}
  SEO + GEO + AEO Audit
  Powered by shopify-cowork
=====================================================

EXECUTIVE SUMMARY
  Biggest issue:       {single highest-leverage finding across all dimensions}
  Best quick win:      {fastest credible improvement}
  AI visibility:       {one-line GEO verdict}
  Scope note:          {catalog-wide findings vs sampled findings}

STORE SNAPSHOT
  Store:               {name} ({myshopify_domain})
  Theme:               {schema_name} v{schema_version}
  Products:            {n}
  Collections:         {n}
  Pages:               {n}
  Blog:                {present / not detected from public sitemap}
  Currency:            {currency}
  Pages sampled:       {n} product + {n} collection + homepage {+ articles if detected}

=====================================================
  DIMENSION SUMMARY
=====================================================

  SEO:                 {x}/65  — {one-line summary}
  GEO (AI Visibility): {x}/20  — {one-line summary}
  AEO (Answer Ready):  {x}/15  — {one-line summary}

=====================================================
  SEO FINDINGS
=====================================================

--- STRUCTURED DATA ---
  {findings}
  Scope:               {Sampled or Inference}
  Evidence:            {sample URLs checked}
  What this means:     {plain-English impact}

--- TITLES AND SNIPPETS ---
  {findings}
  Scope:               Sampled
  Evidence:            {sample URLs checked}

--- CANONICALS AND URL CONSOLIDATION ---
  {findings}
  Scope:               {Sampled or Catalog-wide}
  Evidence:            {sample URLs, robots.txt, sitemap}

--- ROBOTS.TXT ---
  {findings}
  Scope:               Catalog-wide
  Evidence:            /robots.txt

--- SITEMAP ---
  {findings}
  Scope:               Catalog-wide
  Evidence:            /sitemap.xml, /meta.json

--- PRODUCT CONTENT ---
  {n}/{total} products — no description
  {n}/{total} products — thin description (< 150 words)
  {n}/{total} products — adequate or better
  Scope:               Catalog-wide
  Evidence:            /products.json

--- COLLECTION CONTENT ---
  {n}/{total} collections — no description
  {n}/{total} collections — thin description
  {n}/{total} collections — adequate or better
  Scope:               Catalog-wide
  Evidence:            /collections.json

--- PERFORMANCE PROXIES ---
  {findings}
  Scope:               Sampled
  Recommendation:      Confirm with PageSpeed Insights or Lighthouse

--- CATALOG DATA QUALITY ---
  Product type consistency:   {consistent / inconsistent — details}
  Vendor consistency:         {consistent / inconsistent — details}
  Zero-price products:        {count}
  Products with no images:    {count}
  Products with 1 image:      {count}
  Missing SKUs:               {count}
  Scope:                      Catalog-wide
  Evidence:                   /products.json

=====================================================
  GEO FINDINGS — AI VISIBILITY
=====================================================

--- AI BOT ACCESS ---
  Bots blocked:        {list of blocked AI bots}
  Bots allowed:        {list of allowed AI bots, if any}
  llms.txt:            {present / not found}
  Scope:               Catalog-wide
  Evidence:            /robots.txt, /llms.txt
  What this means:     {plain-English impact on AI search visibility}
  Note:                {Shopify default vs merchant choice}

--- ENTITY CLARITY ---
  Organization schema: {present / missing}
  sameAs links:        {list of platforms linked, or "none found"}
  Brand consistency:   {consistent / inconsistent across title, schema, OG}
  About page:          {present with depth / thin / missing}
  Scope:               Sampled
  Evidence:            {homepage, about page}

--- CITATION-WORTHINESS ---
  Review platform:     {detected platform or "none detected"}
  Review volume:       {count if available}
  Original data:       {found / not found in sample}
  Content freshness:   {last product update / last blog post}
  Scope:               Sampled
  Evidence:            {sample URLs}

--- CONTENT EXTRACTABILITY ---
  Question headings:   {count found in sample}
  Answer-first format: {detected / not detected}
  Comparison tables:   {count found}
  Structured lists:    {present / sparse}
  Scope:               Sampled
  Evidence:            {sample URLs}

=====================================================
  AEO FINDINGS — ANSWER ENGINE READINESS
=====================================================

--- FAQ SCHEMA ---
  FAQPage JSON-LD:     {present on N pages / not found}
  FAQ visible on page: {yes / no / partial}
  Scope:               Sampled
  Evidence:            {sample URLs}

--- FEATURED SNIPPET READINESS ---
  Question headings:   {count across sample}
  Answer paragraphs:   {N in 40-60 word range / N outside range}
  List snippet ready:  {yes / no}
  Table snippet ready: {yes / no}
  Scope:               Sampled

--- VOICE SEARCH ---
  Concise answers:     {N answer blocks under 40 words}
  Product schema:      {complete / incomplete for voice queries}
  Scope:               Sampled

--- REVIEW SNIPPETS ---
  AggregateRating:     {present / missing}
  Rating/visible match:{matched / mismatch / cannot verify}
  Individual reviews:  {present / missing}
  Scope:               Sampled

--- KNOWLEDGE PANEL ---
  Wikipedia/Wikidata:  {linked / not linked}
  Organization schema: {present / missing}
  sameAs coverage:     {N platforms linked}
  Scope:               Sampled

=====================================================
  TOP 5 ACTIONS
=====================================================

  #  Action                              Why                    Dimension
  -------------------------------------------------------------------------
  1  {highest-impact fix}                {outcome}              {SEO/GEO/AEO}
  2  {next fix}                          {outcome}              {SEO/GEO/AEO}
  3  {next fix}                          {outcome}              {SEO/GEO/AEO}
  4  {next fix}                          {outcome}              {SEO/GEO/AEO}
  5  {next fix}                          {outcome}              {SEO/GEO/AEO}

=====================================================
  SAMPLE FIXES
=====================================================

  "{real product or collection title}"
  -----------------------------------------------
  Current issue:   {specific problem found}
  Suggested fix:   {concrete action}
  Expected impact: {what improves}

=====================================================
  STORE READINESS SCORE: {n}/100
=====================================================
  This is a diagnostic benchmark, not a Google score.

  Technical SEO:       {x}/20
  Content & On-Page:   {x}/25
  Structured Data:     {x}/20
  GEO (AI Visibility): {x}/20
  AEO (Answer Ready):  {x}/15
=====================================================
```

## Focused Audit Template (Single Dimension)

Use when the user asks for a GEO-only or AEO-only audit:

```text
=====================================================
  {DIMENSION} AUDIT — {domain}
  Powered by shopify-cowork
=====================================================

SUMMARY
  Key finding:         {most important issue in this dimension}
  Quick win:           {fastest fix}

STORE CONTEXT
  Store:               {name}
  Products:            {n}
  Collections:         {n}

{DIMENSION-SPECIFIC FINDINGS}
  {Use the relevant section from the full template above}

TOP 3 ACTIONS
  1. {fix}             {why}
  2. {fix}             {why}
  3. {fix}             {why}

{DIMENSION} SCORE: {x}/{max}
=====================================================
```

## Audit Review Template

```text
=====================================================
  AUDIT REVIEW — {domain}
  Powered by shopify-cowork
=====================================================

BOTTOM LINE
  Most important real issue:  {finding}
  Most overstated claim:      {finding}
  What should happen first:   {action}
  Missing from the audit:     {key gap — especially GEO/AEO if not covered}

SUPPORTED AND IMPORTANT
  - {claim}
    Scope: {Catalog-wide or Sampled}
    Evidence: {source}
    Why it matters: {impact}

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
    Dimension: {SEO/GEO/AEO}
```

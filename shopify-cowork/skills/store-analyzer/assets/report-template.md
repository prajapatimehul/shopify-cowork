# Report Templates

## Full Audit Template

```text
=====================================================
  STORE ANALYSIS — {domain}
  Powered by shopify-cowork
=====================================================

BOTTOM LINE
  Biggest issue:       {single highest-impact finding}
  Best quick win:      {fastest credible fix}
  Scope:               {catalog-wide vs sampled}

STORE SNAPSHOT
  Store:               {name} ({myshopify_domain})
  Theme:               {schema_name} v{schema_version}
  Products:            {n}
  Collections:         {n}
  Pages:               {n}
  Blog:                {present / not detected}
  Currency:            {currency}
  Pages sampled:       {list}

=====================================================
  FINDINGS (ordered by impact)
=====================================================

#{n}  {finding title}                         [{SEO/GEO/AEO}]
  Scope:    {Catalog-wide / Sampled / Inference}
  Proof:    {specific evidence — exact counts, URLs, data}
  Fix:      {concrete action}
  Impact:   {one line — what improves}

{repeat for each finding, highest impact first}

=====================================================
  TOP 5 ACTIONS
=====================================================

  #  Action                     Why                    Dimension
  ------------------------------------------------------------------
  1  {fix}                      {outcome}              {SEO/GEO/AEO}
  2  {fix}                      {outcome}              {SEO/GEO/AEO}
  3  {fix}                      {outcome}              {SEO/GEO/AEO}
  4  {fix}                      {outcome}              {SEO/GEO/AEO}
  5  {fix}                      {outcome}              {SEO/GEO/AEO}

=====================================================
  SAMPLE FIXES
=====================================================

  "{real product or collection title}"
  -----------------------------------------
  Problem:   {specific issue found}
  Fix:       {concrete action with example}
  Result:    {what improves}

  {repeat for 2-3 real items from the store}
```

## Focused Audit Template (Single Dimension)

```text
=====================================================
  {DIMENSION} AUDIT — {domain}
  Powered by shopify-cowork
=====================================================

BOTTOM LINE
  Key finding:         {most important issue}
  Quick win:           {fastest fix}

STORE CONTEXT
  Store:               {name}
  Products:            {n}
  Collections:         {n}

=====================================================
  FINDINGS (ordered by impact)
=====================================================

#{n}  {finding title}
  Scope:    {Catalog-wide / Sampled / Inference}
  Proof:    {evidence}
  Fix:      {action}
  Impact:   {one line}

TOP 3 ACTIONS
  1. {fix}  — {why}
  2. {fix}  — {why}
  3. {fix}  — {why}
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
  Missing from the audit:     {key gap}

SUPPORTED AND IMPORTANT
  - {claim}
    Proof: {evidence}
    Fix:   {action}

SUPPORTED BUT SECONDARY
  - {claim}
    Why secondary: {reason}

REAL BUT OVERSTATED
  - {claim}
    Why overstated: {reason}

UNSUPPORTED FROM CURRENT EVIDENCE
  - {claim}
    Why unsupported: {reason}

WHAT THE AUDIT MISSED
  - {missing issue}
    Proof: {evidence}
    Fix:   {action}
    Dimension: {SEO/GEO/AEO}
```

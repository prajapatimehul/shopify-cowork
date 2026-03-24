# Report Templates

IMPORTANT: These templates define the ONLY allowed sections and format. Do not add any section, header, or structure not shown here.

## Full Audit Template

```text
STORE ANALYSIS — {domain}

BOTTOM LINE
  Biggest issue:   {one sentence — the #1 thing costing this store revenue or traffic}
  Quick win:       {one sentence — highest ROI fix that can be done this week}

SNAPSHOT
  Products: {n}  |  Collections: {n}  |  Pages: {n}
  Blog: {yes/no}  |  Currency: {code}  |  Sampled: {n} pages
  Mobile speed: {PageSpeed score}/100  |  LCP: {n}s  |  CLS: {n}
  Reviews: {platform name or "none detected"}
  Cart type: {drawer/redirect/unknown}
  Trust: {logo ✓/✗} {favicon ✓/✗} {contact page ✓/✗} {about page ✓/✗}
  AI bot access: {allowed/blocked — one line}

FINDINGS

#1  {finding title — specific, not generic}
  Scope:   {Catalog-wide / Sampled / Inference}
  Proof:   {exact evidence in one line — numbers, not adjectives}
  Fix:     {concrete action in one line}
  Impact:  {what improves in one line}

#2  {finding title}
  Scope:   ...
  Proof:   ...
  Fix:     ...
  Impact:  ...

{4-6 findings for strong stores, up to 8-10 for stores with fundamental gaps}
{ordered by business impact, NOT grouped by dimension}
{every finding must pass the Finding Quality Bar from SKILL.md}

SAMPLE FIXES

  "{real product or collection title from this store}"
  Problem:   {what's wrong — one line}
  Fix:       {concrete action — one line}
  Result:    {what improves — one line}

  {2-3 real items from the store}

CONVERSION GAPS

  Elements missing that real shoppers expect:
  - {specific missing element, e.g., "No size chart on an apparel store"}
  - {another gap}
  - {another gap}
  {3-5 gaps, specific to this store's category and products}

AI-FACING GAPS

  Questions AI agents cannot answer confidently from this store today:
  - {specific question a shopper would ask an AI assistant}
  - {another question}
  - {another question}
  - {another question}
  {4-6 questions, specific to this store's products and policies}
```

### What is NOT in this template (do not add these)

- No EXECUTIVE SUMMARY (use BOTTOM LINE)
- No SCORECARD or dimension scores
- No DIMENSION SUMMARY
- No SEO FINDINGS / GEO FINDINGS / AEO FINDINGS / CRO FINDINGS grouping
- No TOP 5 ACTIONS section (the findings ARE the actions)
- No STORE READINESS SCORE or any X/Y scores
- No WHAT'S WORKING section or checkmark lists (except SNAPSHOT trust line)
- No "What this means" explanations after findings
- No comparison tables with other stores
- No sign-off paragraphs or "This is a diagnostic benchmark"
- No subjective design opinions ("looks bad", "not premium", "ugly colors")

## Focused Audit Template

```text
{DIMENSION} AUDIT — {domain}

BOTTOM LINE
  Key finding:   {one sentence}
  Quick win:     {one sentence}

SNAPSHOT
  Products: {n}  |  Collections: {n}

FINDINGS

#1  {finding title}
  Scope:   {Catalog-wide / Sampled / Inference}
  Proof:   ...
  Fix:     ...
  Impact:  ...

{max 5 findings}

AI-FACING GAPS

  - {question relevant to this dimension}
  - ...
```

## Audit Review Template

```text
AUDIT REVIEW — {domain}

BOTTOM LINE
  Most important real issue:   {one sentence}
  Most overstated claim:       {one sentence}
  What should happen first:    {one sentence}

SUPPORTED AND IMPORTANT
  - {claim} — Proof: {evidence} — Fix: {action}

SUPPORTED BUT SECONDARY
  - {claim} — Why: {reason}

REAL BUT OVERSTATED
  - {claim} — Why: {reason}

UNSUPPORTED FROM CURRENT EVIDENCE
  - {claim} — Why: {reason}

MISSING IMPORTANT ISSUES
  - {issue} — Proof: {evidence} — Fix: {action}
```

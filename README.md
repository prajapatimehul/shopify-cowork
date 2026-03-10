# shopify-cowork

AI co-pilot for Shopify stores. Built as a Claude Code plugin.

## Installation

```bash
/plugin marketplace add prajapatimehul/shopify-cowork
/plugin install shopify-cowork@prajapatimehul/shopify-cowork
```

---

## Available Now

### Store Analyzer

Comprehensive SEO + GEO + AEO audit for any public Shopify store. No authentication required.

| Dimension | What It Checks |
|-----------|---------------|
| **SEO** | Crawlability, structured data, content depth, titles, canonicals, technical health |
| **GEO** | AI bot access (GPTBot, PerplexityBot, ClaudeBot), llms.txt, entity clarity, citation-worthiness |
| **AEO** | FAQ schema, featured snippet readiness, voice search, answer formatting |

**Three modes:**

- **Full audit** — all dimensions, catalog-wide data, sampled HTML, Store Readiness Score
- **Focused audit** — single dimension deep-dive (e.g., "is my store visible to AI search?")
- **Audit review** — verify an existing SEO audit's claims against live data

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
Review this SEO audit and tell me what's real
```

Outputs a 100-point Store Readiness Score with category breakdown, prioritized Top 5 actions, and sample fixes using real products from the store.

---

## Coming Soon

| Skill | What It Does | Status |
|-------|-------------|--------|
| **Store Fixer** | Takes analyzer findings and fixes them via Shopify Admin API — schema injection, meta tags, robots.txt, content | Up next |
| **Growth Briefing** | One-command daily briefing — GMV, ad ROAS, stockout alerts, cash position | Planned |
| **Catalog Operations** | Bulk product description generation, SEO copy, product feed optimization | Planned |
| **Ads Audit** | Google Ads wasted spend detection, negative keywords, bid optimization, creative fatigue | Planned |
| **Review Monitor** | Review scanning, 1-star alerts, recurring complaint detection | Planned |
| **Inventory Forecast** | 30-day demand forecast, reorder suggestions, stockout prediction, dead stock ID | Planned |

---

## Repo Structure

```
.claude-plugin/
└── marketplace.json
shopify-cowork/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json
└── skills/
    └── store-analyzer/
        ├── SKILL.md
        ├── references/
        │   ├── seo-checks.md
        │   ├── geo-checks.md
        │   ├── aeo-checks.md
        │   ├── catalog-checks.md
        │   ├── scoring.md
        │   ├── troubleshooting.md
        │   └── testing.md
        ├── assets/
        │   └── report-template.md
        ├── evals/
        │   └── evals.json
        └── scripts/
            ├── score_audit.py
            └── check_report.py
```

## License

MIT

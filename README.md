# shopify-cowork

AI co-pilot for Indian e-commerce brands running Shopify, Amazon, and Myntra. Built as a Claude Code plugin.

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

## Roadmap

Skills planned for multi-channel Indian e-commerce — Shopify D2C, Amazon India, Myntra.

### Store Fixer
Takes issues found by the analyzer and fixes them via Shopify Admin API. Schema injection, meta tag updates, robots.txt patches, content improvements — applied directly to the store with approval gates.

### Growth Briefing (`/growth:morning`, `/growth:daily-close`)
Single-command daily briefing pulling from Shopify, Amazon SP-API, and Google Ads MCP servers. Yesterday's GMV by channel, run rate vs target, contribution margins, stockout alerts, ROAS breakdown, cash position.

### Finance & Reconciliation (`/finance:reconciliation`, `/finance:journal-entry`)
Amazon settlement analysis (commission slab verification, TCS tracking, return credit recovery), Myntra payout reconciliation, Razorpay D2C matching. Auto-generates double-entry journal entries with supporting schedules. GST compilation across multi-state registrations.

### Ads Management (`/ads:audit`, `/growth:launch`)
Google Ads and Amazon PPC audit — wasted spend detection, negative keyword harvesting, bid optimization, creative fatigue alerts. Campaign creation from Shopify collections with human approval before spend.

### Inventory Intelligence (`/inventory:forecast`)
30-day demand forecast using cross-channel sales velocity. Reorder suggestions per channel, stockout prediction, dead stock identification, FBA vs self-fulfilled routing decisions.

### Review Monitor (`/reviews:scan`)
Cross-channel review scanning (Amazon, Shopify, Myntra). Auto-categorization by issue type, 1-star alerts, recurring complaint detection, competitor mention tracking.

### Catalog Operations
Bulk product description generation optimized per channel (Shopify SEO copy, Amazon bullet points, Myntra attributes). Product feed optimization for Google Merchant Center approval.

---

## The Problem This Solves

Running multi-channel e-commerce in India means:

- **3 marketplaces** with 3 different fee structures, settlement cycles, and commission slabs
- **2-5% of GMV silently leaking** through incorrect deductions, unclaimed TCS, and missed return credits
- **GST across 12+ states** wherever Amazon FBA has a warehouse
- **30% return rates** in fashion categories
- **45 minutes every morning** compiling data from 6 different dashboards

One plugin. One terminal. Real money recovered.

---

## Stack

| Layer | Tools |
|-------|-------|
| **Terminal (technical team)** | Claude Code + Shopify Admin MCP + Amazon SP-API MCP + Google Ads MCP |
| **Desktop (non-technical team)** | Claude Cowork with finance and marketing plugins |
| **Bulk content** | ChatGPT + GPT for Sheets |
| **Automation glue** | n8n (self-hosted) |
| **Inventory sync** | Unicommerce |
| **Payments** | Razorpay MCP |

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

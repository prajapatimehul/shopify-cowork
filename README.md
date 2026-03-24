# Shopify Cowork Skills

AI skills that audit and fix Shopify stores. Works with **Claude Code**, **Codex**, **Cursor**, **Gemini CLI**, or any skill-compatible AI platform.

## What it does

**store-analyzer** audits any Shopify store from public data. 8 modules:

| Module | What it checks |
|--------|---------------|
| Trust & Credibility | Logo, favicon, contact info, about page, branded email, policies |
| Conversion | Hero CTA, cart type, cross-sells, size charts, shipping info, reviews |
| Page Speed | Core Web Vitals via PageSpeed API, third-party script count |
| Technical SEO | Crawlability, robots, sitemap, canonicals, internal linking |
| Product-Page SEO | Titles, descriptions, headings, content depth, images |
| Structured Data | Product/Offer schema, merchant listings, review markup |
| AEO | FAQ content, policy clarity, answer-engine readiness |
| GEO | AI bot access, citation-worthiness, content extractability |

**store-fixer** implements fixes via Shopify Admin API with explicit approval before every write.

## Real findings from real stores

Tested on 6 stores from Shopify Community forums:

- A store showing **509 reviews on a 2-week-old site** (zero actual review text)
- An apparel store selling S-4XL with **no size chart**
- A jewelry store with **43 testimonials trapped on a static page** — not in schema, not on product pages
- A kids blanket store where **Google thinks the brand is "Printify"** because the vendor field feeds JSON-LD
- A stationery store with **17 collection descriptions written but the theme doesn't render them**

## Install

```bash
# Claude Code (plugin)
/plugin marketplace add prajapatimehul/shopify-cowork
/plugin install shopify-cowork@shopify-cowork

# Claude Code (manual)
cp -r skills/store-analyzer ~/.claude/skills/store-analyzer

# Codex
cp -r skills/store-analyzer ~/.codex/skills/store-analyzer

# Cursor
cp -r skills/store-analyzer .cursor/skills/store-analyzer

# Gemini CLI
cp -r skills/store-analyzer .gemini/skills/store-analyzer
```

Then just ask naturally:

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
```

## Repo structure

```
skills/
  store-analyzer/    # 8-module public-data audit (SKILL.md + references)
  store-fixer/       # Authenticated fixes via Admin API (SKILL.md + references)
.claude-plugin/      # Claude Code plugin manifest
.agents/skills/      # Cross-platform skill discovery symlinks
```

## License

MIT

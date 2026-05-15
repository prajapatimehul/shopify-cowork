# shopify-cowork

Audit and fix Shopify stores, bundled as a plugin for **Claude Code** and **Codex**. Two skills plus the Shopify Dev MCP server for live docs and GraphQL/theme validation.

## Install

### Claude Code

```
/plugin marketplace add prajapatimehul/shopify-cowork
/plugin install shopify-cowork@shopify-cowork-marketplace
```

### Codex

```
codex plugin marketplace add prajapatimehul/shopify-cowork
```

Then launch Codex and run `/plugins` to install **shopify-cowork**.

## What's included

### MCP server

This plugin configures the [Shopify Dev MCP server](https://www.npmjs.com/package/@shopify/dev-mcp) via `.mcp.json`. It gives the agent:

- `learn_shopify_api` and `search_docs_chunks` — live Shopify docs lookup
- `validate_graphql_codeblocks` — validate Admin/Storefront GraphQL before running it
- `validate_component_codeblocks` and `validate_theme` — validate theme code and Liquid

### Skills

| Skill | Description |
|-------|-------------|
| `store-analyzer` | Public-data audit across 8 modules: Trust, CRO, Page Speed, Technical SEO, Product-Page SEO, Structured Data, AEO, GEO. Findings only — no scores. |
| `store-fixer` | Applies fixes via Shopify Admin GraphQL API. Explicit approval before every write; rollback manifest saved for every change. |

## CLI (standalone skills, any agent)

If you're not on Claude Code or Codex, copy the skill folders into whichever agent loads skills from a directory:

```bash
cp -r skills/store-analyzer ~/.claude/skills/   # Claude Code (manual)
cp -r skills/store-analyzer ~/.codex/skills/    # Codex (manual)
cp -r skills/store-analyzer .cursor/skills/     # Cursor
cp -r skills/store-analyzer .gemini/skills/     # Gemini CLI
```

Each skill's entry point is `SKILL.md` with progressive references under `references/` and `assets/`.

## Usage

After install, just ask:

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity.
Fix the issues from that audit on jhumka-8052.myshopify.com.
```

The agent picks the right skill from its description and walks through approvals before any write.

## What store-analyzer checks

| Module | Checks |
|--------|--------|
| Trust & Credibility | Logo, favicon, contact info, about page, branded email, policies |
| Conversion | Hero CTA, cart type, cross-sells, size charts, shipping info, reviews |
| Page Speed | Core Web Vitals via PageSpeed API, third-party script count |
| Technical SEO | Crawlability, robots, sitemap, canonicals, internal linking |
| Product-Page SEO | Titles, descriptions, headings, content depth, images |
| Structured Data | Product/Offer schema, merchant listings, review markup |
| AEO | FAQ content, policy clarity, answer-engine readiness |
| GEO | AI bot access, citation-worthiness, content extractability |

## What store-fixer does

- **Tier 1 (12 data fixes):** product/collection descriptions, SEO titles/descriptions, image alt text, tags, vendor, SKU, URL redirects.
- **Tier 2 (4 theme fixes):** JSON-LD, collection internal linking, Dawn H1 fix, robots rules.
- Every write is gated on explicit approval and logged to a rollback manifest.

## Layout

```
plugins/shopify-cowork/
  .claude-plugin/plugin.json    # Claude Code manifest
  .codex-plugin/plugin.json     # Codex manifest (with interface block)
  .mcp.json                     # Shopify Dev MCP server
  skills/
    store-analyzer/
    store-fixer/
  README.md
```

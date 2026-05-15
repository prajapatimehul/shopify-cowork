# Shopify Cowork

Agent skills that audit and fix Shopify stores. Ships as a **plugin** for Claude Code and Codex, as **standalone skills** for any skill-compatible CLI, and includes the **Shopify Dev MCP server** for live docs and GraphQL/theme validation.

## What's included

| Component | What it does |
|-----------|--------------|
| **store-analyzer** skill | Public-data audit across 8 modules: Trust, CRO, Page Speed, Technical SEO, Product-Page SEO, Structured Data, AEO, GEO. No scores — only actionable findings with cited fixes. |
| **store-fixer** skill | Implements fixes via the Shopify Admin GraphQL API. Explicit approval before every write. Saves a rollback manifest for every change. |
| **shopify-dev** MCP server | Live Shopify docs search, GraphQL query validation, theme validation. Bundled via `.mcp.json`. |

The two skills cover what real store reviewers check on Shopify Community forums — CRO, UX, trust signals, page speed, search optimization, AI readiness — plus the implementation step that turns audit output into changes on the store.

## Real findings from real stores

Tested on 6 stores pulled from Shopify Community forum requests:

- A store showing **509 reviews on a 2-week-old site** (zero actual review text).
- An apparel store selling S–4XL with **no size chart**.
- A jewelry store with **43 testimonials trapped on a static page** — not in schema, not on product pages.
- A kids blanket store where **Google thinks the brand is "Printify"** because the vendor field feeds JSON-LD.
- A stationery store with **17 collection descriptions written** but the theme doesn't render them.

## Install

### Claude Code (plugin)

```
/plugin marketplace add prajapatimehul/shopify-cowork
/plugin install shopify-cowork@shopify-cowork
/reload-plugins
```

This installs both skills, registers `store-analyzer` and `store-fixer` for auto-discovery, and starts the `shopify-dev` MCP server from `.mcp.json`.

### Codex (plugin)

```
codex plugin marketplace add prajapatimehul/shopify-cowork
```

Then launch Codex and run `/plugins` to install **shopify-cowork**.

### CLI (standalone skills, any agent)

If your agent loads skills from a local directory, copy the skill folders directly:

```bash
# Claude Code (manual, no plugin)
cp -r skills/store-analyzer ~/.claude/skills/
cp -r skills/store-fixer    ~/.claude/skills/

# Codex (manual)
cp -r skills/store-analyzer ~/.codex/skills/
cp -r skills/store-fixer    ~/.codex/skills/

# Cursor
cp -r skills/store-analyzer .cursor/skills/
cp -r skills/store-fixer    .cursor/skills/

# Gemini CLI
cp -r skills/store-analyzer .gemini/skills/
cp -r skills/store-fixer    .gemini/skills/
```

Each skill's entry point is `SKILL.md` with progressive references under `references/` and `assets/`.

### MCP server (any agent)

The plugin ships with `.mcp.json` configuring the Shopify Dev MCP server. If you're not using the plugin, add the same config to your agent's MCP settings:

```json
{
  "mcpServers": {
    "shopify-dev": {
      "command": "npx",
      "args": ["-y", "@shopify/dev-mcp@latest"]
    }
  }
}
```

This gives the agent `learn_shopify_api`, `search_docs_chunks`, `validate_graphql_codeblocks`, `validate_component_codeblocks`, and `validate_theme`.

## Usage

After install, just ask:

```
Audit this Shopify store: example.com
Check if this store is visible to ChatGPT and Perplexity
Fix the issues from that audit on jhumka-8052.myshopify.com
```

The model picks the right skill from the description and walks through approvals before any write.

## Repo layout

```
shopify-cowork/
  .claude-plugin/
    plugin.json           # Claude Code manifest
    marketplace.json      # Claude marketplace entry
  .codex-plugin/
    plugin.json           # Codex manifest (with interface block)
  .mcp.json               # Shopify Dev MCP server config
  skills/
    store-analyzer/       # 8-module audit skill
      SKILL.md
      references/
      assets/
      evals/
      scripts/
    store-fixer/          # Admin API fix skill
      SKILL.md
      references/
      assets/
  README.md
  LICENSE
```

This follows the same layout the AWS Agent Toolkit uses for its plugins: separate manifest folders per agent (`.claude-plugin/`, `.codex-plugin/`), one `.mcp.json`, one `skills/` directory.

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

## License

MIT — see [LICENSE](LICENSE).

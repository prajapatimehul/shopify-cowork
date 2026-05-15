# Shopify Cowork

Agent skills, plugin, and MCP server for auditing and fixing Shopify stores. Works with **Claude Code** and **Codex** as a plugin, and the skills can be installed standalone in any skill-compatible agent.

## Quick start

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

For the per-plugin install detail, see [`plugins/shopify-cowork/README.md`](plugins/shopify-cowork/README.md).

## What's included

### Plugin

| Plugin | Description |
|--------|-------------|
| [shopify-cowork](plugins/shopify-cowork/) | Two skills (store-analyzer, store-fixer) + the Shopify Dev MCP server. The default install. |

### Skills

| Skill | Description |
|-------|-------------|
| `store-analyzer` | 8-module public-data audit: Trust, CRO, Page Speed, Technical SEO, Product-Page SEO, Structured Data, AEO, GEO. Findings only — no scores. |
| `store-fixer` | Implements fixes via the Shopify Admin GraphQL API. Explicit approval before every write; rollback manifest saved for every change. |

### MCP server

[Shopify Dev MCP](https://www.npmjs.com/package/@shopify/dev-mcp) — bundled in the plugin's `.mcp.json`. Provides:

- `learn_shopify_api`, `search_docs_chunks` — live Shopify docs lookup
- `validate_graphql_codeblocks` — validate GraphQL before running it
- `validate_component_codeblocks`, `validate_theme` — validate theme code

Other agents can install the MCP server directly:

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

## Real findings from real stores

The audit module was built from 15 Shopify Community forum threads (50+ reviewers). Tested on 6 stores:

- A store showing **509 reviews on a 2-week-old site** (zero actual review text).
- An apparel store selling S–4XL with **no size chart**.
- A jewelry store with **43 testimonials trapped on a static page** — not in schema, not on product pages.
- A kids blanket store where **Google thinks the brand is "Printify"** because the vendor field feeds JSON-LD.
- A stationery store with **17 collection descriptions written** but the theme doesn't render them.

## Repo layout

```
shopify-cowork/
  .claude-plugin/marketplace.json    # Claude Code marketplace
  .agents/plugins/marketplace.json   # Codex marketplace
  plugins/
    shopify-cowork/
      .claude-plugin/plugin.json     # Claude Code plugin manifest
      .codex-plugin/plugin.json      # Codex plugin manifest
      .mcp.json                      # Shopify Dev MCP server
      skills/
        store-analyzer/
        store-fixer/
      README.md
  README.md
  LICENSE
```

This mirrors the layout used by [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws): a per-agent marketplace file at the repo root and one folder per plugin under `plugins/`, each carrying its own `.claude-plugin/`, `.codex-plugin/`, and `.mcp.json`.

## License

MIT — see [LICENSE](LICENSE).

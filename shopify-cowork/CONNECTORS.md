# Connectors

## How tool references work

Plugin files use `~~category` as a placeholder for whatever tool the user connects in that category. For example, `~~shopify dev tools` means the Shopify Dev MCP server, which provides theme checking, Liquid linting, Hydrogen scaffolding, and GraphQL API access.

Plugins are **tool-agnostic** — they describe workflows in terms of categories (storefront, dev tools, analytics, etc.) rather than specific products. The `.mcp.json` pre-configures specific MCP servers, but any MCP server in that category works.

## Connectors for this plugin

| Category | Placeholder | Included servers | Other options |
|----------|-------------|-----------------|---------------|
| Shopify dev tools | `~~shopify dev tools` | @shopify/dev-mcp | shopify-mcp, @shopify/cli |
| Source control | `~~source control` | — | GitHub, GitLab, Bitbucket |
| Project tracker | `~~project tracker` | — | Linear, Asana, Jira |
| Chat | `~~chat` | — | Slack, Microsoft Teams |

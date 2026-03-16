# Rollback Manifest Schema

This is the **single source of truth** for rollback format. All other files reference this.

## Canonical Format

```json
{
  "store": "my-store.myshopify.com",
  "timestamp": "2026-03-16T14:30:00Z",
  "changes": [
    {
      "resource": "Product",
      "id": "gid://shopify/Product/123",
      "field": "descriptionHtml",
      "mutation": "productUpdate",
      "old_value": "",
      "new_value": "<p>New description</p>"
    }
  ],
  "theme_files": [
    {
      "theme_id": "gid://shopify/OnlineStoreTheme/456",
      "filename": "sections/header.liquid",
      "action": "modified",
      "original_content": "...full file content before edit..."
    },
    {
      "theme_id": "gid://shopify/OnlineStoreTheme/456",
      "filename": "snippets/seo-schema.liquid",
      "action": "created",
      "original_content": null
    }
  ]
}
```

**Field rules:**
- `mutation`: the GraphQL mutation used (for reverse execution)
- `action`: `"modified"` (restore original_content) or `"created"` (delete via `themeFileDelete`)
- `filename`: matches the Shopify theme file path exactly (e.g., `sections/header.liquid`)
- `old_value` / `original_content`: the complete value before the change

## Save Location

Write the manifest to the local filesystem:
```
store-fixer-rollback-{domain}-{timestamp}.json
```

Include this path in the fix summary so the user can find it.

## Rollback Execution

**Data changes**: Re-apply `old_value` to each resource using the stored `mutation`.

**Modified theme files**: Restore `original_content` via `themeFilesUpsert`.

**Created theme files**: Delete via:
```graphql
mutation ThemeFileDelete($themeId: ID!, $files: [String!]!) {
  themeFilesDelete(themeId: $themeId, files: $files) {
    deletedThemeFiles { filename }
    userErrors { field message }
  }
}
```

## Error Recovery

If a batch fails mid-execution:
1. Stop the current batch
2. Report which mutations succeeded and which failed
3. Ask the user: continue with remaining items, rollback completed items, or stop entirely?
4. The rollback manifest already contains `old_value` for completed items, so partial rollback is always possible

# GraphQL Mutation Reference

Endpoint: `POST /admin/api/2025-07/graphql.json`
Header: `X-Shopify-Access-Token: {token}`

## Rate Limits

| Plan | Points/sec | Effective mutations/sec (10 pts each) |
|------|-----------|--------------------------------------|
| Basic/Standard | 100 | ~10 |
| Advanced | 200 | ~20 |
| Plus | 1,000 | ~100 |

For 50+ items, use bulk operations (see bottom of file) — they bypass rate limits.

---

## productUpdate

Updates description, SEO, vendor, productType, tags, status.

```graphql
mutation ProductFix($input: ProductUpdateInput!) {
  productUpdate(product: $input) {
    product { id title descriptionHtml vendor productType tags seo { title description } }
    userErrors { field message }
  }
}
```

**Gotcha:** Parameter name is `product:`, not `input:`. Tags array REPLACES all tags — use `tagsAdd`/`tagsRemove` for surgical changes.

---

## collectionUpdate

```graphql
mutation CollectionFix($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection { id title descriptionHtml seo { title description } }
    userErrors { field message }
  }
}
```

**Gotcha:** Parameter name is `input:` (different from productUpdate which uses `product:`). Works for both custom and smart collections.

---

## fileUpdate (image alt text, batch)

```graphql
mutation ImageAltFix($files: [FileUpdateInput!]!) {
  fileUpdate(files: $files) {
    files { id alt fileStatus }
    userErrors { field message code }
  }
}
```

Input: `[{ "id": "gid://shopify/MediaImage/123", "alt": "..." }, ...]`

To get image IDs for a product:
```graphql
query ProductMedia($id: ID!) {
  product(id: $id) {
    media(first: 20) { nodes { id alt ... on MediaImage { image { url } } } }
  }
}
```

---

## tagsAdd / tagsRemove

```graphql
mutation AddTags($id: ID!, $tags: [String!]!) {
  tagsAdd(id: $id, tags: $tags) {
    node { ... on Product { id tags } }
    userErrors { field message }
  }
}
```

Max 250 tags per resource, 255 chars per tag.

---

## urlRedirectCreate

```graphql
mutation CreateRedirect($redirect: UrlRedirectInput!) {
  urlRedirectCreate(urlRedirect: $redirect) {
    urlRedirect { id path target }
    userErrors { field message }
  }
}
```

`path` max 1024 chars, `target` max 255 chars. Creates 301 redirect.

---

## productVariantsBulkUpdate (compare_at_price)

```graphql
mutation VariantsFix($productId: ID!, $variants: [ProductVariantsBulkInput!]!) {
  productVariantsBulkUpdate(productId: $productId, variants: $variants) {
    productVariants { id compareAtPrice }
    userErrors { field message }
  }
}
```

Set `compareAtPrice: null` to remove.

---

## inventoryItemUpdate (SKU)

```graphql
mutation UpdateSKU($id: ID!, $input: InventoryItemInput!) {
  inventoryItemUpdate(id: $id, input: $input) {
    inventoryItem { id sku }
    userErrors { field message }
  }
}
```

Requires `write_inventory` scope.

---

## metafieldsSet (article SEO)

```graphql
mutation SetMetafields($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { id namespace key value }
    userErrors { field message }
  }
}
```

For article SEO: `ownerId: "gid://shopify/Article/123"`, `namespace: "global"`, `key: "title_tag"` or `"description_tag"`, `type: "single_line_text_field"`.

---

## Shop verification

```graphql
{ shop { name url plan { displayName } } }
```

Run this first to verify token and access.

---

## Bulk Operations (50+ items)

For large batches, `bulkOperationRunMutation` processes items async and bypasses rate limits.

**Step 1:** Get a staged upload URL:
```graphql
mutation { stagedUploadsCreate(input: { resource: BULK_MUTATION_VARIABLES, filename: "bulk.jsonl", mimeType: "text/jsonl", httpMethod: POST }) {
  stagedTargets { url parameters { name value } }
  userErrors { field message }
}}
```

**Step 2:** Upload JSONL file (one line per mutation's variables):
```jsonl
{"input": {"id": "gid://shopify/Product/1", "descriptionHtml": "<p>...</p>"}}
{"input": {"id": "gid://shopify/Product/2", "descriptionHtml": "<p>...</p>"}}
```

**Step 3:** Start the bulk operation:
```graphql
mutation { bulkOperationRunMutation(mutation: "mutation($input: ProductUpdateInput!) { productUpdate(product: $input) { product { id } userErrors { field message } } }", stagedUploadPath: "...path from step 1...") {
  bulkOperation { id status }
  userErrors { field message }
}}
```

**Step 4:** Poll for completion:
```graphql
{ currentBulkOperation { id status objectCount url } }
```

When `status` is `COMPLETED`, download results from the `url` field.

**Limits:** Max 5 concurrent bulk ops per shop. 24h timeout. 100MB JSONL max.

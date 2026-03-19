# Catalog Manager — Skill Research

> Replaces: **Catalog Manager / Catalog Operations Executive**
> Salary band: ₹6–12 LPA | Headcount: 1–2 per company | Automation potential: 50–60%

## What the Catalog Manager Does Daily

The catalog manager is the person who keeps the product catalog structurally correct and operationally current. They do NOT write copy (that's catalog-writer). They handle:

- **Product uploads** — Create new products in Shopify with images, variants (size/color/material), pricing, compare-at price, weight, and metafields
- **Variant management** — Add/remove/update size runs, color options, pricing per variant, inventory tracking toggles
- **Collection management** — Create smart and manual collections, assign products, set sort orders, manage seasonal/campaign collections
- **Metafield management** — Set material, care instructions, dimensions, weight, wash instructions, fabric composition via metafields
- **Tagging and taxonomy** — Maintain product types, vendor fields, tags for filtering and navigation
- **Pricing operations** — Bulk price updates, compare-at price for sales, campaign discount setup
- **Product lifecycle** — Archive/unpublish discontinued products, set draft status for upcoming launches
- **Catalog hygiene** — Fix broken images, duplicate SKUs, missing variants, incomplete product data
- **Marketplace sync checks** — Verify data consistency between Shopify, Amazon, and Flipkart listings
- **Google Merchant Center** — Fix disapproved products, ensure feed compliance, resolve GTIN/image/price issues

---

## Shopify Admin API — Required Endpoints

All operations use the **GraphQL Admin API** (REST is being deprecated). Required access scope: `write_products`, `read_products`, `write_inventory`, `read_inventory`.

### Product CRUD

| Mutation | Purpose | Notes |
|---|---|---|
| `productCreate` | Create a new product with title, description, vendor, type, tags, status, media, metafields, SEO fields | Creates ONE initial variant only. Products are unpublished by default. |
| `productUpdate` | Update product attributes — title, description, tags, vendor, type, status, SEO | Does NOT handle variants (use variant-specific mutations). |
| `productSet` | Create OR update a product in a single request — handles product fields, options, variants, media, metafields, inventory all at once | The power mutation. Syncs external data into Shopify. Omitted fields stay unchanged. List fields (variants, metafields) delete entries not included in input. |
| `productDelete` | Permanently delete a product and all associated data | Irreversible. Prefer archiving. |
| `publishablePublish` | Publish a product to sales channels | Required after `productCreate` (products start unpublished). |
| `publishableUnpublish` | Remove product from sales channels | Replaces deprecated `productUnpublish`. |

**Product status lifecycle:** `DRAFT` → `ACTIVE` → `ARCHIVED`
- Use `productUpdate` with `status: ARCHIVED` to archive discontinued products
- Use `publishableUnpublish` to remove from specific channels without archiving

### Variant Management

| Mutation | Purpose | Notes |
|---|---|---|
| `productVariantsBulkCreate` | Add multiple variants to an existing product | Supports option values, pricing (price + compareAtPrice), media association, metafields. Max 2,048 variants per product. |
| `productVariantsBulkUpdate` | Update multiple variants on a product | Same fields as create. This is the ONLY way to update variants (no single-variant update mutation exists). |
| `productVariantsBulkDelete` | Remove variants from a product | By variant ID. |

**Key variant fields:**
- `price` and `compareAtPrice` — for sale pricing
- `optionValues` — size, color, material (by name or ID)
- `mediaId` — variant-specific images
- `metafields` — variant-level custom data
- `inventoryQuantities` — stock per location (via `productSet`)

### Image/Media Management

| Mutation | Purpose | Notes |
|---|---|---|
| `productCreateMedia` | Add images/videos to a product | Supports IMAGE, VIDEO, EXTERNAL_VIDEO, MODEL_3D content types. |
| `productDeleteMedia` | Remove media from a product | By media ID. |
| `productReorderMedia` | Change media display order | Sets position priority. |

Media is associated via `CreateMediaInput`:
- `originalSource` — URL of the image/video
- `alt` — Alt text (important for SEO and accessibility)
- `mediaContentType` — IMAGE, EXTERNAL_VIDEO, etc.

### Metafield Management

| Mutation | Purpose | Notes |
|---|---|---|
| `metafieldsSet` | Create or update metafields on any resource | Standalone mutation. Upserts by namespace+key combo. |
| `metafieldsDelete` | Delete specific metafields | By namespace, key, and owner ID. |
| `metafieldDefinitionCreate` | Create metafield definitions (schema) | Defines allowed types, validation, and which resources use them. |

**Common D2C metafield namespaces/keys:**
- `custom.material` — Fabric/material composition
- `custom.care_instructions` — Washing/care info
- `custom.dimensions` — Product dimensions (L×W×H)
- `custom.weight` — Product weight
- `custom.country_of_origin` — For compliance
- `custom.hsn_code` — For India GST compliance
- `custom.wash_type` — Machine wash, hand wash, dry clean

**Metafield types:** `single_line_text_field`, `multi_line_text_field`, `number_integer`, `number_decimal`, `json`, `boolean`, `date`, `dimension`, `weight`, `volume`, `url`, `color`, `list.single_line_text_field`, `rich_text_field`

Metafields can be set inline during `productCreate`, `productUpdate`, or `productSet` — no separate call needed.

### Collection Management

| Mutation | Purpose | Notes |
|---|---|---|
| `collectionCreate` | Create a smart or custom collection | Smart: define `ruleSet` with conditions. Custom: specify `products` array. Unpublished by default. |
| `collectionUpdate` | Update collection title, description, rules, sort order, image | Supports both collection types. |
| `collectionAddProducts` | Add products to a custom collection | By product GIDs. |
| `collectionRemoveProducts` | Remove products from a custom collection | By product GIDs. |
| `collectionReorderProducts` | Change product display order in collection | Manual sort only (not for smart collections with auto-sort). |
| `publishablePublish` | Publish collection to sales channels | Same as product publishing. |

**Smart collection rule columns:** `TITLE`, `TYPE`, `TAG`, `VENDOR`, `PRODUCT_TYPE`, `PRODUCT_METAFIELD_DEFINITION`, `VARIANT_METAFIELD_DEFINITION`

**Smart collection rule relations:** `EQUALS`, `NOT_EQUALS`, `CONTAINS`, `NOT_CONTAINS`, `GREATER_THAN`, `LESS_THAN`, `STARTS_WITH`, `ENDS_WITH`

**Sort order options:** `BEST_SELLING`, `ALPHA_ASC`, `ALPHA_DESC`, `PRICE_ASC`, `PRICE_DESC`, `CREATED`, `CREATED_DESC`, `MANUAL`

### Inventory Management

| Mutation | Purpose | Notes |
|---|---|---|
| `inventorySetQuantities` | Set absolute inventory levels | Use when you ARE the source of truth. Supports compare-and-set for concurrency. |
| `inventoryAdjustQuantities` | Adjust inventory by delta (+/-) | Use when adjusting relative to current stock. Safer for concurrent operations. |
| `inventorySetOnHandQuantities` | Set on-hand inventory | Simpler version for setting stock levels. |

Both mutations support `referenceDocumentUri` for audit trails.

---

## Bulk Operations Strategy

For catalogs with 100+ products, individual mutations are too slow. Shopify provides two bulk approaches:

### 1. `bulkOperationRunMutation` (Async, for 1000+ items)

**How it works:**
1. Upload a JSONL file to Shopify via `stagedUploadsCreate`
2. Each line in the JSONL = one mutation's input variables
3. Call `bulkOperationRunMutation` with the mutation template + upload path
4. Poll `currentBulkOperation` or subscribe to webhooks for completion
5. Download results JSONL when done

**Constraints:**
- One bulk mutation per shop at a time (a bulk query can run simultaneously)
- Rate limit: stores with 50,000+ variants limited to 1,000 new variants/day
- Results delivered as JSONL file

**Best for:** Mass price updates, bulk metafield assignment, bulk tag changes, bulk status changes (archive old season).

**Workflow:**
```
stagedUploadsCreate → upload JSONL → bulkOperationRunMutation → poll/webhook → download results
```

### 2. `productSet` in a loop (Sync, for 10–100 items)

For moderate-scale updates, call `productSet` in a loop with rate limiting. Each call can update an entire product (fields + variants + metafields + media + inventory) in one shot.

**Best for:** Campaign price changes, collection-wide metafield updates, seasonal variant additions.

### 3. `productVariantsBulkUpdate` per product (Sync, variant-focused)

When only variant data changes (prices, compare-at prices, inventory), use `productVariantsBulkUpdate` per product. Handles all variants on a product in one call.

---

## Google Merchant Center Feed Compliance

The catalog manager must ensure products pass Google Merchant Center validation. Common disapprovals that can be fixed from Shopify data:

### Required Attributes (must exist in Shopify or feed will be rejected)

| Attribute | Shopify Source | Common Issue |
|---|---|---|
| `id` | Product ID / SKU | Missing or duplicate SKU |
| `title` | Product title | Too short, keyword-stuffed, or truncated |
| `description` | Product description (body_html) | Empty or too thin (< 50 chars) |
| `link` | Product URL (handle-based) | 404 if handle changed |
| `image_link` | Product featured image | Missing, broken URL, placeholder image |
| `price` | Variant price | Mismatch between feed and storefront price |
| `availability` | Inventory tracking | Feed says "in stock" but product is sold out |
| `brand` | Vendor field | Missing vendor — common in D2C (use own brand name) |
| `condition` | Usually "new" | Missing for used/refurbished items |

### Conditional Attributes (required for specific categories)

| Attribute | When Required | Shopify Source |
|---|---|---|
| `gtin` (barcode/UPC/EAN) | All products with manufacturer-assigned GTIN | Variant barcode field |
| `mpn` | When no GTIN exists | Variant SKU or metafield |
| `gender` | Apparel | Product metafield or tag |
| `age_group` | Apparel | Product metafield or tag |
| `color` | Apparel, accessories | Variant option value |
| `size` | Apparel, shoes | Variant option value |
| `item_group_id` | Multi-variant products | Parent product ID |
| `shipping_weight` | If not set at account level | Variant weight |

### Top Disapproval Reasons (fixable from Shopify)

1. **Missing GTIN/barcode** — Add barcodes to variant `barcode` field. Custom/handmade products: set `identifier_exists` to false.
2. **Price mismatch** — Feed price doesn't match storefront. Usually a currency conversion issue or stale feed sync. Fix: ensure Shopify prices are the source of truth.
3. **Image quality** — Placeholder images, text overlays, watermarks, too small (< 100×100). Fix: replace with clean product photography, no promotional overlays.
4. **Availability mismatch** — Feed says "in stock" but product page shows sold out. Fix: enable inventory tracking on all variants.
5. **Missing description** — Empty `body_html`. Fix: ensure every product has at least a basic description.
6. **Title too generic** — Just "T-shirt" instead of "Men's Cotton Crew Neck T-shirt - Navy Blue". Fix: include brand, product type, key attributes in title.
7. **Missing required apparel attributes** — No gender, age_group, color, size for clothing. Fix: add as metafields or ensure variant options are named correctly.
8. **Shipping weight missing** — Required if not set at account level. Fix: add weight to all variants.

### Catalog Health Checks (what the skill should audit)

The skill should run these checks before any bulk operation or on-demand:

- **Missing images** — Products with 0 images
- **Missing descriptions** — Products with empty or very thin body_html
- **Missing prices** — Variants with price = 0 or null
- **Missing barcodes** — Variants without barcode field (for Google feed)
- **Missing vendor** — Products without vendor (breaks Google brand requirement)
- **Duplicate SKUs** — Multiple variants with same SKU
- **Missing variant options** — Products with variants but no option names
- **Orphaned products** — Products not in any collection
- **Draft products forgotten** — Products stuck in DRAFT status for > 30 days
- **Missing metafields** — Products missing required custom metafields (material, care, etc.)
- **Inventory not tracked** — Variants with `inventoryManagement: null` (causes availability mismatches)
- **Compare-at price issues** — Compare-at price lower than or equal to current price (broken sale display)

---

## Marketplace Sync Checks

For D2C brands selling on Shopify + Amazon + Flipkart, the catalog manager checks for data consistency. The skill cannot directly query Amazon/Flipkart APIs, but can:

### What's Feasible

1. **Export Shopify catalog data** — Extract products with all fields as the "source of truth" reference
2. **Generate comparison reports** — Output product data in a format that can be compared against marketplace exports (CSV from Amazon Seller Central, Flipkart Seller Hub)
3. **Flag common sync issues:**
   - Products in Shopify but not listed on marketplace (by SKU match)
   - Price differences between channels (Shopify vs marketplace)
   - Inventory discrepancies
   - Title/description mismatches
   - Missing images on one channel

### Integration Landscape (India D2C)

- **Shopify ↔ Amazon**: Native Shopify Amazon channel, or third-party apps like CedCommerce, Synkron
- **Shopify ↔ Flipkart**: Third-party only — Zapinventory, CedCommerce, Jhattse, Synkron
- **Multi-channel OMS**: EasyEcom, Unicommerce, Browntape (common in India D2C)
- **Key concern**: Price parity across channels (marketplace fee structures differ, so MRP may vary)

### What the Skill Does vs Doesn't Do

- **Does**: Export Shopify catalog data, identify products with incomplete data for marketplace readiness, generate SKU-level comparison templates
- **Doesn't**: Create marketplace listings (different APIs entirely), sync inventory in real-time (that's an app/middleware job), manage marketplace-specific fields (A+ content, Flipkart attributes)

---

## Scope Definition

### IN Scope (what the catalog-manager skill does)

1. **Product CRUD** — Create, read, update, archive products via Admin API
2. **Variant management** — Add/remove/update variants, pricing, compare-at prices, barcodes, weight
3. **Collection automation** — Create/update smart and manual collections, assign products, set rules and sort orders
4. **Metafield management** — Set/update/delete product and variant metafields (material, care, dimensions, etc.)
5. **Bulk operations** — Mass price updates, bulk tagging, bulk metafield assignment, bulk archive/status changes
6. **Catalog health audits** — Find missing images, empty descriptions, duplicate SKUs, orphaned products, broken pricing
7. **Google feed compliance** — Check and fix attributes that cause Merchant Center disapprovals
8. **Pricing operations** — Set/update prices, compare-at prices, prepare for campaigns
9. **Product lifecycle** — Draft → Active → Archived status management, publish/unpublish to channels
10. **Inventory data** — Set/adjust inventory quantities (as part of product setup, not warehouse management)
11. **Marketplace readiness** — Export catalog data, flag incomplete products, generate comparison templates

### OUT of Scope (handled by other skills or roles)

- **Writing product copy** — That's `catalog-writer` (titles, descriptions, SEO copy)
- **Product photography / image creation** — Creative team responsibility
- **SEO analysis** — That's `store-analyzer`
- **Store theme changes** — That's `store-fixer`
- **Marketplace listing creation** — Different APIs (Amazon SP-API, Flipkart Seller API)
- **Real-time inventory sync** — Middleware/app responsibility (Synkron, EasyEcom)
- **Order management** — That's `order-ops`
- **Warehouse/fulfillment operations** — Outside catalog scope
- **Discount code creation** — Separate Shopify discount API (could be adjacent skill)
- **Customer data** — That's `crm-automation`

---

## Available APIs and MCPs

### Shopify Admin GraphQL API (primary)
- Access via: Shopify MCP tools (`shopify-dev` plugin)
- `mcp__plugin_shopify-cowork_shopify-dev__introspect_graphql_schema` — Explore available mutations and types
- `mcp__plugin_shopify-cowork_shopify-dev__validate_graphql_codeblocks` — Validate generated GraphQL before execution
- `mcp__plugin_shopify-cowork_shopify-dev__search_docs_chunks` — Search Shopify documentation
- `mcp__plugin_shopify-cowork_shopify-dev__learn_shopify_api` — Load API context (must call first)

### Key Access Scopes Required
- `write_products` — Create, update, delete products, variants, images, collections
- `read_products` — Query products, variants, collections, images
- `write_inventory` — Set/adjust inventory quantities
- `read_inventory` — Read inventory levels
- `write_product_listings` — Manage product publications to channels
- `read_product_listings` — Read publication status

### Google Merchant Center
- No direct MCP available — checks are based on validating Shopify data against Google's required attributes
- Feed is typically synced via Shopify's Google channel app or third-party feed apps

---

## Output Expectations

The catalog-manager skill produces **actual product changes in Shopify**, not spreadsheets or suggestions. Outputs include:

1. **Product creation** — New products created in Shopify with all fields populated
2. **Bulk updates** — Prices, metafields, tags, status changed across multiple products
3. **Collection setup** — New collections created with products assigned and rules configured
4. **Health reports** — List of catalog issues with affected product IDs/handles and specific fix actions
5. **Google feed fix list** — Products failing Merchant Center requirements with exact fields to fix
6. **Marketplace comparison template** — CSV/table of Shopify products with all fields, ready for cross-channel comparison

Every write operation must follow the same safety protocol as `store-fixer`:
- Show exact proposed changes before execution
- Get explicit user approval
- Record what was changed
- Provide rollback path (capture pre-mutation state)

---

## Key API Version Notes

- Current stable API: `2026-01` (latest as of research date)
- Supported versions: `2025-04`, `2025-07`, `2025-10`, `2026-01`
- `productUnpublish` is **deprecated** — use `publishableUnpublish`
- REST API is being phased out — always prefer GraphQL
- `productSet` is the most powerful single mutation for catalog sync operations
- Variant limit: 2,048 per product (default)
- New variant creation throttle: 1,000/day for stores with 50,000+ existing variants

# Catalog Writer — Skill Research

## Employee Role Replaced

**Content Writer / Catalog Copywriter**
- Salary: 3-7 LPA (India)
- Headcount: 1-3 per company (D2C brands, 50-200Cr revenue)
- Automatable: 70-80%

### What the Content Writer does daily

| Task | Volume | Time spent |
|---|---|---|
| Write product descriptions (100-200 words each) | 8-15/day | 3-4 hrs |
| Write/update collection page descriptions | 2-5/day | 1 hr |
| Add/update image alt text across catalog | 20-50/day | 1-2 hrs |
| Write meta titles and meta descriptions | 10-20/day | 1 hr |
| Maintain brand voice consistency | Ongoing | Embedded in all tasks |
| Write FAQ content for product pages | 2-5/week | 1-2 hrs/week |

### What this skill does NOT replace (out of scope)

- Blog posts for SEO (separate `blog-writer` skill)
- Email campaign copy (separate `crm-automation` skill)
- WhatsApp broadcast messages (`crm-automation`)
- Ad copy for paid campaigns (separate `ad-copy` skill)
- Image editing/creation (not text-based)
- Brand strategy or positioning (human decision)

---

## Data Sources Needed

### 1. Shopify Admin API — Read (current catalog state)

| Endpoint / Query | What we read | Scope needed |
|---|---|---|
| `products` query (GraphQL) | title, descriptionHtml, handle, vendor, productType, tags, status, images (with altText), variants, metafields | `read_products` |
| `collections` query | title, descriptionHtml, handle, seo { title, description }, image, metafields | `read_products` |
| `pages` query (GraphQL, available since API 2024-10) | title, body, handle, seo fields | `read_content` or `read_online_store_pages` |
| `articles` query (GraphQL, since 2024-10) | title, body, handle, summary, tags, seo fields | `read_content` |
| Product metafields | `global.title_tag`, `global.description_tag`, custom metafields for specs/features | `read_products` |
| Product media/images | altText field on MediaImage objects | `read_products` |

### 2. Shopify Admin API — Write (push updated copy)

| Mutation | What we write | Scope needed |
|---|---|---|
| `productUpdate` | title, descriptionHtml, tags, seo { title, description }, metafields | `write_products` |
| `productSet` | Same as productUpdate but supports bulk sync, also handles variants and list fields in one call | `write_products` |
| `collectionUpdate` | title, descriptionHtml, handle, seo { title, description }, metafields | `write_products` |
| `fileUpdate` | Image alt text (replaces deprecated `productUpdateMedia`) | `write_products` |
| `pageUpdate` | title, body, handle (for FAQ pages, About pages, etc.) | `write_content` or `write_online_store_pages` |
| `articleCreate` / `articleUpdate` | Blog article title, body, summary, tags, handle, image alt text | `write_content` |
| `bulkOperationRunMutation` | Wraps any mutation above for bulk execution via JSONL upload | Same as underlying mutation |
| `stagedUploadsCreate` | Stage JSONL files for bulk operations | `write_products` |

### 3. SEO metafields (how Shopify stores meta titles/descriptions)

Shopify stores meta titles and descriptions as metafields on products, collections, pages, and articles:

```
namespace: "global"
key: "title_tag"
type: "single_line_text_field"
value: "Custom Meta Title Here"

namespace: "global"
key: "description_tag"
type: "single_line_text_field"
value: "Custom meta description here"
```

To hide a resource from search engines:
```
namespace: "seo"
key: "hidden"
type: "number_integer"
value: 1
```

### 4. Google Search Console API (keyword intelligence — optional but high-value)

| Data | Use case |
|---|---|
| Top queries by page (clicks, impressions, CTR, position) | Identify which keywords each product/collection already ranks for |
| Pages with high impressions but low CTR | Prioritize meta title/description rewrites for these pages |
| Keyword gaps (pages ranking 8-20) | Target these keywords in product description rewrites |
| Seasonal query trends | Adjust product copy for seasonal relevance |

**API endpoint**: `searchanalytics.query` — supports grouping by query, page, country, device, date. Max 50,000 rows/day via API.

**Access**: Requires Google OAuth2 with `webmasters.readonly` scope. If a Google Search Console MCP becomes available, use that. Otherwise, the merchant can export a CSV from GSC and provide it as input.

### 5. Brand Voice Guidelines (via CLAUDE.md)

The brand voice is NOT stored in Shopify — it's defined as a style guide in the project's `CLAUDE.md` or a dedicated `brand-voice.md` reference file within the skill.

```markdown
# Brand Voice Guidelines — {Brand Name}

## Tone
- Conversational but informed
- Confident, not aggressive
- Indian English, not American English

## Vocabulary
- Say "crafted" not "manufactured"
- Say "designed for" not "built for"
- Never say "cheap" — say "accessible" or "value-conscious"

## Product Description Formula
1. Open with the key benefit (1 sentence)
2. Material/construction details (1-2 sentences)
3. Use case / occasion (1 sentence)
4. Care instructions or sizing note (1 sentence)

## SEO Rules
- Meta title format: "{Product Name} — {Key Feature} | {Brand}"
- Meta description: benefit-led, 120-155 chars, include primary keyword
- Alt text: descriptive, include product name and color/variant
```

The brand configures this once. The skill follows it for every product.

---

## Skill Workflow

### Phase 1: Read current catalog state

1. Authenticate via Admin API (client-owned Dev Dashboard app with `read_products`, `write_products`, `read_content`, `write_content` scopes)
2. Pull all products: `products` query with pagination (250 per page)
3. For each product, extract: title, descriptionHtml, tags, images (with altText), metafields (title_tag, description_tag)
4. Pull all collections: `collections` query with `descriptionHtml`, `seo { title, description }`
5. Pull FAQ/About pages if in scope: `pages` query
6. Optionally load Google Search Console data (CSV or API) for keyword targeting

### Phase 2: Analyze and generate new copy

For each product/collection:

1. **Audit current copy**: Is the description missing, thin (<50 words), duplicate, or off-brand?
2. **Identify keyword opportunity**: If GSC data available, what queries is this page ranking for? What keywords should it target?
3. **Generate new copy** following brand voice guidelines:
   - Product description (descriptionHtml): 100-200 words, benefit-led, SEO-optimized
   - Meta title (global.title_tag): Under 60 chars, keyword-first
   - Meta description (global.description_tag): 120-155 chars, benefit-led, includes CTA
   - Image alt text: Descriptive, includes product name + color/variant
4. **Generate collection descriptions**: Thematic, 50-100 words, includes category keywords
5. **Generate FAQ content** for product pages (via metafields or page content)

### Phase 3: Review before push (approval gate)

Before any write operation:

1. Show a **before/after comparison** for each item:
   ```
   Product: "Classic Sneaker - White"

   TITLE (no change)
   Current: Classic Sneaker - White

   DESCRIPTION
   Current: "White sneaker. Comfortable. Good for daily wear."
   New: "Step into effortless style with our Classic Sneaker in crisp white.
   Crafted from breathable knit fabric with a cushioned insole that supports
   you from morning meetings to evening walks. The minimalist design pairs
   with everything from chinos to joggers. Machine washable for easy care."

   META TITLE
   Current: (empty)
   New: "Classic White Sneaker — Breathable & Washable | BrandName"

   META DESCRIPTION
   Current: (empty)
   New: "Breathable knit sneaker with cushioned insole. Machine washable,
   pairs with everything. Free shipping on orders over ₹999."

   IMAGE ALT TEXT (3 images)
   Current: "IMG_4521.jpg", "", "white-shoe-3"
   New: "Classic White Sneaker front view", "Classic White Sneaker side profile
   showing knit texture", "Classic White Sneaker on foot with chinos"
   ```

2. User approves, requests edits, or skips specific items
3. Only approved items proceed to Phase 4

### Phase 4: Push to Shopify

Use the appropriate mutation for each update:

**Individual product updates** (small batches, <50 products):
```graphql
mutation productUpdate($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      id
      title
      descriptionHtml
      seo { title description }
    }
    userErrors { field message }
  }
}
```

With input:
```json
{
  "id": "gid://shopify/Product/123",
  "descriptionHtml": "<p>New description here...</p>",
  "metafields": [
    {
      "namespace": "global",
      "key": "title_tag",
      "value": "New Meta Title | Brand",
      "type": "single_line_text_field"
    },
    {
      "namespace": "global",
      "key": "description_tag",
      "value": "New meta description here",
      "type": "single_line_text_field"
    }
  ]
}
```

**Image alt text updates**:
```graphql
mutation fileUpdate($input: [FileUpdateInput!]!) {
  fileUpdate(files: $input) {
    files { alt }
    userErrors { field message }
  }
}
```

**Collection updates**:
```graphql
mutation collectionUpdate($input: CollectionInput!) {
  collectionUpdate(input: $input) {
    collection {
      id
      descriptionHtml
      seo { title description }
    }
    userErrors { field message }
  }
}
```

### Phase 5: Verify and report

1. Re-read updated products/collections via API to confirm changes landed
2. Generate a summary report:
   - Products updated: X
   - Collections updated: X
   - Images with new alt text: X
   - Pages updated: X
   - Errors/skipped: X (with reasons)
3. Provide rollback data (pre-change values stored from Phase 1)

---

## Bulk Operations Strategy (500+ products)

### Why bulk operations matter

A D2C brand with 500 products and 3 images each = 500 product descriptions + 500 meta titles + 500 meta descriptions + 1,500 image alt texts = **3,000 individual writes**. Individual mutations would hit rate limits and take hours.

### Approach: JSONL bulk mutation

1. **Stage the JSONL file**:
   ```graphql
   mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
     stagedUploadsCreate(input: $input) {
       stagedTargets {
         url
         resourceUrl
         parameters { name value }
       }
       userErrors { field message }
     }
   }
   ```
   Input: `{ resource: "BULK_MUTATION_VARIABLES", filename: "products.jsonl", mimeType: "text/jsonl", httpMethod: "POST" }`

2. **Upload the JSONL file** to the returned URL. Each line = one mutation's variables:
   ```jsonl
   {"input":{"id":"gid://shopify/Product/1","descriptionHtml":"<p>New desc 1</p>","metafields":[{"namespace":"global","key":"title_tag","value":"Meta Title 1","type":"single_line_text_field"}]}}
   {"input":{"id":"gid://shopify/Product/2","descriptionHtml":"<p>New desc 2</p>","metafields":[{"namespace":"global","key":"title_tag","value":"Meta Title 2","type":"single_line_text_field"}]}}
   ```

3. **Run the bulk mutation**:
   ```graphql
   mutation bulkOperationRunMutation($mutation: String!, $stagedUploadPath: String!) {
     bulkOperationRunMutation(mutation: $mutation, stagedUploadPath: $stagedUploadPath) {
       bulkOperation { id status }
       userErrors { field message }
     }
   }
   ```

4. **Poll for completion** via `currentBulkOperation` query or webhook subscription
5. **Download results JSONL** to verify success/failure per item

### Safety guardrails for bulk updates

| Rule | Why |
|---|---|
| Capture ALL pre-change values before any write | Rollback requires exact previous state |
| Process in batches of 50-100 products | Allows review checkpoints and limits blast radius |
| Never update more than approved scope | Scope creep = content the brand didn't approve going live |
| Run on a schedule, not all at once | Spread API load, allow time for merchant review |
| Store rollback JSONL alongside update JSONL | One file to push, one file to revert |
| Verify 10% sample after bulk push | Spot-check that content rendered correctly on storefront |
| Alt text updates are separate bulk operation | fileUpdate uses different mutation than productUpdate |

### Rate limits

- Shopify GraphQL Admin API: **1,000 cost points per second** (bucket with leak rate)
- `productUpdate` costs ~10 points each
- Bulk operations via `bulkOperationRunMutation` are **not subject to normal rate limits** — the JSONL processing runs async server-side
- Only **one bulk mutation operation per shop** at a time (but bulk queries can run simultaneously)
- Throttle when store exceeds 50,000 variants: max 1,000 new variants/day (not relevant for copy updates)

---

## Scope

### IN scope

- Product descriptions (descriptionHtml) — write and rewrite
- Product meta titles (global.title_tag metafield)
- Product meta descriptions (global.description_tag metafield)
- Product image alt text (via fileUpdate mutation)
- Product tags (for SEO and categorization)
- Collection descriptions (descriptionHtml)
- Collection SEO fields (seo.title, seo.description)
- FAQ page content (via pageUpdate or product metafields)
- Brand voice consistency enforcement (via CLAUDE.md style guide)
- Bulk catalog rewrites (via JSONL bulk operations)
- Before/after comparison for approval
- Rollback capability (pre-change state capture)
- GSC keyword integration (optional, for SEO-informed rewrites)

### OUT of scope

- **Email copy**: Handled by `crm-automation` skill
- **Ad copy** (Google Ads, Meta Ads): Separate `ad-copy` skill
- **Blog posts / content strategy**: Separate `blog-writer` skill
- **Image creation or editing**: Not text-based automation
- **WhatsApp / SMS messages**: Handled by `crm-automation`
- **Theme code changes**: Handled by `store-fixer` skill
- **Pricing or inventory changes**: Handled by `catalog-manager` skill
- **Product creation** (new SKUs): Handled by `catalog-manager`
- **Translation / localization**: Separate concern with different API patterns
- **Brand strategy / positioning**: Human decision, not automation

---

## APIs and MCPs Available

### Shopify Admin API (via shopify-dev MCP)

The `shopify-dev` MCP plugin provides:
- `learn_shopify_api` — Load API context for admin, storefront, etc.
- `introspect_graphql_schema` — Explore product, collection, page, article mutations
- `search_docs_chunks` — Search Shopify docs for implementation details
- `fetch_full_docs` — Read full documentation pages
- `validate_graphql_codeblocks` — Validate generated GraphQL against schema

### Required Shopify API scopes

| Scope | Used for |
|---|---|
| `read_products` | Read product titles, descriptions, images, metafields, tags |
| `write_products` | Update product copy, meta tags, image alt text, collection content |
| `read_content` | Read pages, blog articles |
| `write_content` | Update FAQ pages, create/update blog articles |

### Google Search Console (optional enrichment)

- **API**: `searchanalytics.query` endpoint via Google OAuth2
- **MCP**: If a Google Search Console MCP exists, use it. Otherwise accept merchant-provided CSV export.
- **Value**: Keyword data transforms "write a good description" into "write a description targeting keywords this page already ranks for."

---

## Output: What the Skill Produces

This skill does NOT produce a Google Doc of suggestions. It produces:

1. **Actual updated products in Shopify** — descriptions, meta titles, meta descriptions, image alt text pushed via Admin API
2. **Actual updated collections in Shopify** — descriptions and SEO fields pushed via Admin API
3. **Actual updated pages in Shopify** — FAQ content, about page copy
4. **Before/after report** — what changed, what was approved, what was skipped
5. **Rollback data** — pre-change values stored so any update can be reverted

The workflow is: **Read → Generate → Show diff → Get approval → Push → Verify → Report**

Not: "Here are some suggested descriptions, go paste them into Shopify yourself."

---

## Key Technical Notes

### productUpdate vs productSet

- `productUpdate`: Updates product fields (title, descriptionHtml, seo, metafields, tags). Does NOT handle variants. Good for individual copy updates.
- `productSet`: More comprehensive — handles products, variants, collections, metafields in one call. Supports `synchronous: true/false`. Better for bulk sync operations. **Caution**: list fields (metafields, collections) are replace-all — omitted entries get deleted.

### Image alt text update path

The old `productUpdateMedia` mutation is **deprecated**. Use `fileUpdate` instead:
```graphql
mutation {
  fileUpdate(files: [{
    id: "gid://shopify/MediaImage/123",
    alt: "Descriptive alt text for the product image"
  }]) {
    files { id alt }
    userErrors { field message }
  }
}
```

### Pages and articles (GraphQL support since 2024-10)

As of API version 2024-10, pages and articles have full GraphQL support:
- `pageUpdate` — update page title, body, handle
- `articleCreate` / `articleUpdate` — create/update blog posts with title, body, summary, tags, image, SEO fields
- Required scopes: `write_content` or `write_online_store_pages`

### SEO metafields are NOT on the seo input object for products

For **products**, meta titles/descriptions are stored as metafields (`global.title_tag`, `global.description_tag`), NOT in a `seo` input field. For **collections**, they ARE on the `seo` input object. This inconsistency is important — using the wrong approach will silently fail.

---

## Integration with Other Skills

| Skill | Relationship |
|---|---|
| `store-analyzer` | Analyzer identifies thin descriptions, missing alt text, weak meta tags → catalog-writer fixes them |
| `store-fixer` | Fixer handles theme-level changes; catalog-writer handles content-level changes via Admin API |
| `catalog-manager` | Manager handles product creation, pricing, inventory; catalog-writer handles copy/content only |
| `crm-automation` | CRM handles email/WhatsApp copy; catalog-writer handles on-site product copy |

# Procurement-Ops Skill

## Role Replaced

**Procurement Executive** — 1-2 people per D2C company, salary range INR 4-8 LPA, 60-70% of daily work automatable.

### What the Procurement Executive Does Daily

| Task | Frequency | Automatable? |
|------|-----------|-------------|
| Create & send purchase orders to suppliers | Daily | Yes — generate PO documents, email to vendors |
| Track PO status — follow up on delivery dates, partial shipments | Daily | Yes — status tracking, automated follow-ups |
| Coordinate GRN (Goods Receipt Note) with warehouse | Per-shipment | Partially — match received vs ordered, flag discrepancies |
| Update inventory system with inbound stock | Per-shipment | Yes — Shopify inventory mutations |
| Compare supplier quotes for new products | Weekly | No — needs human judgement |
| Maintain vendor master data | Ongoing | Yes — metafield-based vendor registry |
| Match received goods against PO quantities | Per-shipment | Yes — GRN-PO matching logic |
| Handle discrepancies (short shipments, quality rejects) | As needed | Partially — flag and escalate, not resolve |

---

## Data Sources Required

### 1. Shopify Inventory APIs (GraphQL Admin API)

**Shopify has migrated to GraphQL-only for new apps (mandatory since April 2025).** All inventory operations must use GraphQL Admin API.

#### InventoryItem Object
Stores per-variant inventory data:
- `id` — globally unique identifier
- `sku` — stock keeping unit (case-sensitive)
- `unitCost` — MoneyV2 (cost per item, requires "View product costs" permission)
- `tracked` — whether inventory quantities are tracked
- `requiresShipping` — shipping flag
- `measurement` — packaging dimensions
- `countryCodeOfOrigin` / `provinceCodeOfOrigin` — origin tracking
- `harmonizedSystemCode` — customs HS code
- `inventoryLevels` — quantities across all locations

**Important:** InventoryItem does NOT store vendor/supplier info. Vendor is on the Product object. One product = one vendor in Shopify.

#### InventoryLevel Object
Tracks quantities of an inventory item at a specific location:
- `quantities` (by name): `available`, `on_hand`, `incoming`, `committed`
- `item` — linked InventoryItem
- `location` — linked Location

#### Key Mutations

**`inventoryAdjustQuantities`** — Relative adjustments (delta-based):
```graphql
mutation inventoryAdjustQuantities($input: InventoryAdjustQuantitiesInput!) {
  inventoryAdjustQuantities(input: $input) {
    inventoryAdjustmentGroup {
      createdAt
      reason
      changes { name delta }
    }
    userErrors { field message }
  }
}
```
- Requires: `write_inventory` scope
- Reason codes: `correction`, `received`, and others
- `referenceDocumentUri` for audit trail
- Idempotency key required from API 2026-04

**`inventorySetQuantities`** — Absolute value setting:
- Only use when acting as source of truth
- Supports `compareQuantity` for compare-and-set (concurrency safety)
- Same scope and idempotency requirements

**`inventoryMoveQuantities`** — Move between locations

**`inventoryActivate`** — Activate item at a new location

#### Querying Inventory
```graphql
query {
  inventoryItems(first: 50) {
    edges {
      node {
        id
        sku
        unitCost { amount currencyCode }
        tracked
        inventoryLevels(first: 10) {
          edges {
            node {
              quantities(names: ["available", "incoming", "committed", "on_hand"]) {
                name
                quantity
              }
              location { name }
            }
          }
        }
      }
    }
  }
}
```

### 2. Shopify Product & Vendor Data

The `Product` object has a `vendor` field (string) — this is the only native supplier identifier. One product maps to one vendor.

**Limitation:** No native multi-supplier support. If the same SKU comes from multiple suppliers, this must be managed externally.

Access via:
```graphql
query {
  products(first: 50) {
    edges {
      node {
        id
        title
        vendor
        variants(first: 10) {
          edges {
            node {
              sku
              inventoryItem {
                unitCost { amount currencyCode }
                inventoryLevels(first: 5) {
                  edges {
                    node {
                      quantities(names: ["available"]) { quantity }
                      location { name }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

### 3. Shopify Order History (for Sales Velocity)

Orders API provides the data needed to calculate reorder points:

```graphql
query {
  orders(first: 100, sortKey: CREATED_AT, reverse: true) {
    edges {
      node {
        createdAt
        lineItems(first: 50) {
          edges {
            node {
              sku
              quantity
              variant { id inventoryItem { id } }
            }
          }
        }
      }
    }
  }
}
```

From order history, calculate:
- **Daily sales velocity** per SKU = total units sold / number of days in period
- **Sales trend** = compare recent 30-day velocity vs prior 30-day
- **Reorder point** = (daily velocity x lead time in days) + safety stock
- **Reorder quantity** = (daily velocity x order cycle days) — should respect MOQ

### 4. Metafields for Vendor Master Data

Since Shopify has no native vendor/supplier management system, use **Product metafields** to store procurement data:

```graphql
mutation {
  metafieldDefinitionCreate(definition: {
    name: "Supplier Lead Time"
    namespace: "procurement"
    key: "lead_time_days"
    type: "number_integer"
    ownerType: PRODUCT
    description: "Supplier lead time in days for this product"
  }) {
    createdMetafieldDefinition { id }
  }
}
```

Recommended metafield definitions under namespace `procurement`:

| Key | Type | Purpose |
|-----|------|---------|
| `lead_time_days` | `number_integer` | Supplier lead time in days |
| `moq` | `number_integer` | Minimum Order Quantity |
| `supplier_email` | `single_line_text_field` | Supplier contact email |
| `supplier_phone` | `single_line_text_field` | Supplier phone number |
| `supplier_gst` | `single_line_text_field` | Supplier GSTIN (India) |
| `reorder_point` | `number_integer` | Manual override for reorder point |
| `last_po_date` | `date` | Date of last purchase order |
| `last_po_number` | `single_line_text_field` | Last PO reference number |
| `payment_terms` | `single_line_text_field` | e.g. "Net 30", "Advance" |
| `supplier_rating` | `number_decimal` | Performance score (0-5) |

**Alternative:** Maintain a vendor master Google Sheet with full supplier details (address, bank details, payment terms, product mapping) and reference it via the skill. This avoids metafield sprawl and keeps sensitive financial data out of Shopify.

### 5. Shopify Locations API

```graphql
query {
  locations(first: 10) {
    edges {
      node {
        id
        name
        address { address1 city province country }
        isActive
        fulfillsOnlineOrders
      }
    }
  }
}
```

Needed for: knowing which warehouse to set incoming inventory against, multi-location GRN.

---

## Shopify's Procurement Limitations (Critical)

### No Native Purchase Order System
Shopify does NOT have a built-in purchase order system in its Admin API. There is no `PurchaseOrder` object, no PO mutations, no PO queries.

### Stocky Is Sunsetting (August 31, 2026)
- Stocky (Shopify's inventory app) had PO functionality but is being discontinued
- Core features like inventory transfers and forecasting stopped working July 7, 2025
- Stocky was removed from the Shopify App Store on February 2, 2026
- Stocky's API was read-only (GET requests only) — could not create POs programmatically
- Shopify and Stocky POs were completely separate systems — POs in one did not appear in the other

### Single Vendor Per Product
Shopify supports only one `vendor` field per product and one `unitCost` per variant. Multi-supplier sourcing for the same SKU cannot be modeled natively.

### No GRN/Receiving API
There is no goods receipt or receiving endpoint. Receiving must be modeled as inventory adjustments using `inventoryAdjustQuantities` with reason code `received`.

### Workarounds the Skill Must Implement
1. **POs as generated documents** — Create PO documents (PDF/Google Sheets) externally, not in Shopify
2. **PO tracking via metafields** — Store PO references on products/variants using metafields
3. **PO tracking via Google Sheets** — Maintain a PO ledger spreadsheet as the source of truth
4. **GRN as inventory adjustment** — When goods are received, use `inventoryAdjustQuantities` with `reason: "received"` and `referenceDocumentUri` pointing to the PO
5. **Vendor data in metafields or sheets** — Store extended vendor info outside the product vendor field

---

## What the Skill Should Do

### Core Functions (IN SCOPE)

#### 1. Reorder Alert Generation
- Calculate daily sales velocity from order history (last 30-90 days)
- Compute reorder points: `(velocity x lead_time) + safety_stock`
- Compare current `available` inventory against reorder point
- Generate prioritized reorder list: what to order, from which vendor, how much
- Factor in MOQ from metafields — round up to MOQ if needed
- Account for `incoming` quantities (already ordered, in transit)

#### 2. Purchase Order Generation
- Generate PO documents from reorder recommendations
- PO should include: PO number, date, vendor details, line items (SKU, product name, quantity, unit cost, total), delivery address, payment terms, expected delivery date
- Output as: structured markdown, Google Sheets row, or data for PDF generation
- Auto-number POs with a configurable prefix (e.g., `PO-2026-0001`)
- Email PO to supplier (via email integration or draft for review)

#### 3. GRN Matching (Goods Receipt Note)
- When goods arrive, accept received quantities per SKU
- Compare received quantities against the original PO
- Flag discrepancies: short shipments, excess quantities, wrong items
- Generate GRN document with: GRN number, PO reference, received date, accepted/rejected quantities
- On confirmation, call `inventoryAdjustQuantities` with `reason: "received"` to update Shopify inventory

#### 4. Vendor Master Management
- Maintain vendor registry (in metafields or Google Sheets)
- Track per vendor: name, contact, email, phone, GST, lead time, MOQ, payment terms, product mapping
- Vendor performance scoring: on-time delivery rate, fill rate (ordered vs received), quality reject rate

#### 5. Inbound Shipment Tracking
- Track open POs and their expected delivery dates
- Alert when deliveries are overdue
- Maintain PO status lifecycle: Draft → Sent → Acknowledged → Shipped → Partially Received → Fully Received → Closed
- Dashboard view of all open/pending POs

#### 6. Inventory Updates
- After GRN confirmation, update Shopify inventory levels via `inventoryAdjustQuantities`
- Use `referenceDocumentUri` to link the adjustment back to the PO/GRN for audit trail
- Support multi-location receiving (select warehouse/location for inbound)

#### 7. Demand Forecasting (Basic)
- Calculate stock-days-remaining: `current_available / daily_velocity`
- Flag items with < N days of stock remaining (configurable threshold)
- Weekly procurement summary: what's running low, what's on order, what's overdue
- Seasonal adjustment flag: allow manual override for seasonal products

### Out of Scope (NOT included)

| Excluded | Reason |
|----------|--------|
| Vendor price negotiations | Requires human judgement and relationship management |
| Quality inspection | Physical process, cannot be automated via API |
| Payment processing to vendors | Finance-ops skill territory, involves bank transfers and accounting |
| Warehouse layout/management | Physical operations, outside procurement scope |
| Returns to suppliers | Infrequent, needs human coordination |
| Import/customs clearance | Complex regulatory process, needs specialist |
| Contract management | Legal review required |
| New vendor onboarding | Requires due diligence, credit checks |

---

## Available APIs & MCPs

### Shopify Dev MCP (Available in Plugin)
The plugin includes `shopify-dev` MCP with these relevant tools:
- `search_docs_chunks` — Search Shopify documentation
- `introspect_graphql_schema` — Explore the GraphQL Admin API schema
- `validate_graphql_codeblocks` — Validate GraphQL queries/mutations
- `fetch_full_docs` — Get complete Shopify API documentation
- `learn_shopify_api` — Learn about specific API resources

### Google Sheets MCP
For PO document management, vendor master, and PO tracking ledger:
- Create/update PO tracking spreadsheet
- Generate PO line items in a standard template
- Maintain vendor master data with full contact/financial details
- GRN log with PO cross-references

### Email Integration
For sending POs to suppliers:
- Draft POs as email attachments or inline content
- Follow-up reminders for overdue deliveries
- GRN discrepancy notifications to vendors

### Tally ERP Integration (India)
Tally (TallyPrime) is the dominant accounting software in India:
- **API capabilities:** GET & POST APIs via XML/JSON/ODBC
- **Relevant modules:** Purchase vouchers, stock items, purchase orders, ledgers
- **Integration points:** Sync POs to Tally as purchase vouchers, sync stock items, sync vendor ledgers
- **Limitation:** Tally API integrations typically require custom middleware; there's no standard MCP available. This is a future integration opportunity.
- **Practical approach for now:** Export PO data in a format that can be imported to Tally (CSV/XML), rather than live API sync

---

## Output Specification

The skill must produce **actionable outputs**, not just alerts or reports:

### 1. Purchase Order Document
```
PURCHASE ORDER
═══════════════════════════════════════
PO Number:    PO-2026-0342
Date:         2026-03-14
Vendor:       Sunrise Textiles
GSTIN:        27AABCS1234F1ZP
Contact:      supplier@sunrise.com

Ship To:      [Warehouse Name from Shopify Location]

┌─────┬──────────────┬─────┬───────┬─────────┬──────────┐
│ #   │ SKU          │ Qty │ UOM   │ Rate    │ Amount   │
├─────┼──────────────┼─────┼───────┼─────────┼──────────┤
│ 1   │ TEE-BLK-M    │ 200 │ Pcs   │ ₹350.00 │ ₹70,000  │
│ 2   │ TEE-BLK-L    │ 150 │ Pcs   │ ₹350.00 │ ₹52,500  │
│ 3   │ TEE-WHT-M    │ 100 │ Pcs   │ ₹340.00 │ ₹34,000  │
└─────┴──────────────┴─────┴───────┴─────────┴──────────┘
                              Subtotal:  ₹1,56,500
                              GST (18%): ₹28,170
                              Total:     ₹1,84,670

Payment Terms: Net 30
Expected Delivery: 2026-03-28
Notes: [any special instructions]
```

### 2. GRN Document
```
GOODS RECEIPT NOTE
═══════════════════════════════════════
GRN Number:   GRN-2026-0198
Date:         2026-03-28
Against PO:   PO-2026-0342
Vendor:       Sunrise Textiles
Location:     Main Warehouse

┌─────┬──────────────┬──────────┬──────────┬────────┬────────────┐
│ #   │ SKU          │ Ordered  │ Received │ Short  │ Status     │
├─────┼──────────────┼──────────┼──────────┼────────┼────────────┤
│ 1   │ TEE-BLK-M    │ 200      │ 200      │ 0      │ OK         │
│ 2   │ TEE-BLK-L    │ 150      │ 140      │ 10     │ SHORT      │
│ 3   │ TEE-WHT-M    │ 100      │ 100      │ 0      │ OK         │
└─────┴──────────────┴──────────┴──────────┴────────┴────────────┘

Action Required: 10 units of TEE-BLK-L short-shipped. Follow up with vendor.
Inventory Updated: Yes (available quantities adjusted in Shopify)
```

### 3. Reorder Alert
```
REORDER ALERT — 2026-03-14
═══════════════════════════════════════
5 SKUs below reorder point:

┌──────────────┬───────┬─────────┬──────────┬──────┬───────────────┐
│ SKU          │ Avail │ Velocity│ Days Left│ ROP  │ Suggested Qty │
├──────────────┼───────┼─────────┼──────────┼──────┼───────────────┤
│ TEE-BLK-M    │ 45    │ 12/day  │ 3.7      │ 180  │ 360 (MOQ:100) │
│ HOODIE-GRY-L │ 20    │ 5/day   │ 4.0      │ 75   │ 150 (MOQ:50)  │
│ CAP-NAV      │ 8     │ 3/day   │ 2.7      │ 45   │ 100 (MOQ:100) │
└──────────────┴───────┴─────────┴──────────┴──────┴───────────────┘

Velocity = avg daily units sold (last 30 days)
ROP = (velocity × lead_time) + safety_stock
Suggested Qty = velocity × 30 days, rounded up to MOQ
```

### 4. Inventory Update (Shopify API Call)
After GRN confirmation, execute:
```graphql
mutation {
  inventoryAdjustQuantities(input: {
    reason: "received"
    name: "available"
    referenceDocumentUri: "procurement://grn/GRN-2026-0198"
    changes: [
      {
        inventoryItemId: "gid://shopify/InventoryItem/12345"
        locationId: "gid://shopify/Location/67890"
        delta: 200
      },
      {
        inventoryItemId: "gid://shopify/InventoryItem/12346"
        locationId: "gid://shopify/Location/67890"
        delta: 140
      }
    ]
  }) {
    inventoryAdjustmentGroup { createdAt reason }
    userErrors { field message }
  }
}
```

### 5. Weekly Procurement Summary
- SKUs below reorder point (count + list)
- Open POs and their status (pending delivery, partial, overdue)
- Vendor performance snapshot (on-time %, fill rate %)
- Total procurement value this week/month
- Stock-outs that occurred (items that hit zero)

---

## Implementation Notes

### PO Number Sequence
Maintain a running PO counter in a Google Sheet or a Shopify metafield on the Shop object:
```graphql
mutation {
  metafieldsSet(metafields: [{
    ownerId: "gid://shopify/Shop/SHOP_ID"
    namespace: "procurement"
    key: "last_po_number"
    type: "number_integer"
    value: "342"
  }]) {
    metafields { id }
  }
}
```

### Sales Velocity Calculation
```
velocity = sum(line_item.quantity for orders in last_N_days where line_item.sku == target_sku) / N
```
Use 30 days for fast-moving items, 90 days for slow-moving. Exclude days when product was out of stock (available = 0) for more accurate velocity — requires checking inventory history.

### Safety Stock Formula
```
safety_stock = Z × σ_demand × √(lead_time)
```
Where Z = service level factor (1.65 for 95%), σ_demand = standard deviation of daily demand. Simplified version: `safety_stock = velocity × safety_days` where safety_days is configurable (default 3-5 days).

### Multi-Location Handling
For brands with multiple warehouses, the skill should:
1. Calculate velocity per location (from fulfillment location data)
2. Generate separate POs per delivery location, or one PO with split delivery instructions
3. GRN against specific location IDs

### Concurrency Safety
When updating inventory after GRN:
- Use `compareQuantity` in `inventorySetQuantities` to prevent race conditions
- Or use `inventoryAdjustQuantities` (delta-based) which is inherently safer for concurrent writes
- Always use idempotency keys (required from API 2026-04)

---

## Trigger Phrases

The skill should activate when the user says things like:
- "Check what needs reordering"
- "Generate a PO for [vendor]"
- "Create purchase order"
- "What's running low on stock?"
- "Record GRN for PO-XXXX"
- "Goods received against PO [number]"
- "Show open purchase orders"
- "Track inbound shipments"
- "Update vendor details for [vendor]"
- "Weekly procurement summary"
- "Which items will stock out this week?"
- "Compare current stock vs reorder points"

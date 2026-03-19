# Customer Service Skill — Research

> Replaces: **CS Agents** (₹2.2-4 LPA, 5-15 per company, 60-75% automatable)
> Target: Shopify D2C brands, ₹50-200Cr revenue, India

## What CS Agents Do Daily

Each agent handles 30-50 tickets/day across channels (email, chat, WhatsApp, Instagram DMs, phone).

| Ticket Type | Volume | What Agent Does | Automatable? |
|---|---|---|---|
| **WISMO** ("Where is my order?") | 50-60% | Look up order, pull tracking from fulfillment, share status with customer, chase courier if delayed | **Yes — fully** |
| **Returns/Exchanges** | 15-20% | Check return window, verify eligibility (tags, product type), initiate return in Shopify, process refund | **Yes — with rules** |
| **Product Queries** | 10-15% | Answer sizing, material, compatibility from product data/metafields | **Yes — lookup** |
| **Payment Issues** | 5-10% | Check payment status, share refund timeline, COD-to-prepaid conversion | **Partial** |
| **Complaints** (damaged/wrong item) | 5% | Document issue, attach photos, escalate to ops | **No — human** |
| **Order modifications** | ~5% | Cancel unfulfilled order, update shipping address, add order notes | **Yes — with guards** |

**Post-interaction**: Agent updates order notes/timeline in Shopify admin after every ticket.

---

## Data Sources Required

### Primary: Shopify Admin GraphQL API

The skill needs authenticated access to the Shopify Admin API with these scopes:

| Scope | Used For |
|---|---|
| `read_orders`, `write_orders` | Order lookup, notes update, cancellation |
| `read_customers` | Customer search by email/phone |
| `read_products` | Product info, variant details, metafields |
| `read_fulfillments` | Tracking numbers, fulfillment status |
| `write_returns` | Initiate returns, approve/decline |
| `write_refunds` | Process refunds (line items, shipping) |

**MCP available**: `shopify-dev` MCP server (already in plugin) provides `introspect_graphql_schema`, `learn_shopify_api`, `validate_graphql_codeblocks`.

### Secondary: Helpdesk Platform API

Most D2C brands at this scale use one of:
- **Freshdesk** — Most common in India at this revenue range
- **Gorgias** — Popular with Shopify-native brands
- **Zendesk** — Enterprise-leaning, less common at ₹50-200Cr

### Tertiary: WhatsApp Business API

India-specific channel (dominant for D2C CS). Providers:
- **Interakt** (Jio Haptik) — D2C-focused, Shopify integration, Indian market
- **Wati** — SMB-focused, drag-and-drop chatbot builder
- **Gupshup** — Enterprise WhatsApp BSP

---

## Shopify API Capabilities — What's Available

### 1. Order Lookup

**Query**: `order` / `orders` (GraphQL Admin API)

Key fields available on the Order object:
- `name` — Order identifier (#1001)
- `email`, `phone` — Customer contact
- `customer` — Full customer object (null for guest checkout)
- `displayFinancialStatus` — Payment status (PAID, PENDING, REFUNDED, etc.)
- `displayFulfillmentStatus` — Fulfillment status (UNFULFILLED, FULFILLED, PARTIALLY_FULFILLED)
- `fulfillments` — Array with tracking details (see below)
- `shippingAddress` — Delivery address
- `note` — Order notes (readable + writable)
- `tags` — Searchable labels
- `events` — Timeline of all order activities
- `lineItems` — Products ordered with quantities and prices
- `refunds` — Any refunds already processed
- `returns` — Return objects if any exist

**Search**: Orders can be filtered by `name`, `email`, `financial_status`, `fulfillment_status`, `created_at`, `tag`, etc.

### 2. Customer Lookup

**Query**: `customers` with search filter

```graphql
customers(first: 5, query: "email:customer@example.com") {
  edges { node { id firstName lastName email phone ordersCount totalSpent tags note } }
}
```

Customers searchable by: `email`, `phone`, `name`, `tag`, `orders_count`, `total_spent`.

### 3. Fulfillment & Tracking

**Object**: `FulfillmentTrackingInfo` on each `Fulfillment`

Available fields:
- `trackingCompany` — Carrier name (Delhivery, BlueDart, DTDC, India Post, Shiprocket, etc.)
- `trackingNumbers` — One or more tracking numbers
- `trackingUrls` — Clickable tracking links (auto-generated for known carriers)
- `status` — SUCCESS, CANCELLED, ERROR, FAILURE
- `estimatedDeliveryAt` — Expected delivery date (if carrier provides)

**Access path**: `order → fulfillments → trackingInfo`

The skill can extract tracking number + carrier + URL and compose a WISMO response immediately.

### 4. Order Notes Update

**Mutation**: `orderUpdate`

```graphql
mutation {
  orderUpdate(input: { id: "gid://shopify/Order/123", note: "Customer called re: delivery delay. Shared tracking. —AI" }) {
    order { id note }
    userErrors { field message }
  }
}
```

This is critical — every CS interaction should log a note on the order for audit trail.

### 5. Refund Processing

**Mutation**: `refundCreate`

Capabilities:
- Refund specific line items with quantities
- Refund shipping costs (full or partial)
- Refund duties and import taxes
- Issue refund to original payment method OR store credit
- Attach a note explaining the refund reason
- Idempotency support (prevents duplicate refunds on retry)

Required input: `orderId`, `refundLineItems` (item + quantity + restock flag), `transactions`, optional `shipping` and `note`.

**Guard rails needed**: Refunds are irreversible. The skill MUST require confirmation before executing, and should enforce maximum refund amount limits set by merchant policy.

### 6. Returns Management

**Mutations**: Full lifecycle available

| Step | Mutation | What It Does |
|---|---|---|
| Customer requests return | `returnRequest` | Creates return in REQUESTED status |
| Approve return | `returnApproveRequest` | Moves to OPEN, creates reverse fulfillment |
| Decline return | `returnDeclineRequest` | Rejects return with reason |
| Process return | `returnProcess` | Confirms quantities, dispositions, processes refund |
| Close return | `returnClose` | Marks complete |
| Cancel return | `returnCancel` | Reverses before processing |

The Return object tracks: `status`, `returnLineItems`, `exchangeLineItems`, `refunds`, `reverseFulfillmentOrders`.

### 7. Order Cancellation

**Mutation**: `orderCancel`

Parameters: `orderId`, `reason` (CUSTOMER, FRAUD, INVENTORY, DECLINED, OTHER), `notifyCustomer`, `restock`, `staffNote`, `refundMethod`.

**Critical**: Cancellation is irreversible. Only for unfulfilled orders. The skill must verify fulfillment status before allowing cancellation.

### 8. Product Information

**Query**: `product` / `products` / `productVariants`

Available for CS queries:
- `title`, `description`, `descriptionHtml` — Product details
- `variants` — Size, color, price, SKU, inventory quantity
- `metafields` — Custom fields (material, care instructions, dimensions, weight)
- `images` — Product photos
- `tags` — Product categorization

---

## Workflow Per Ticket Type

### WISMO (50-60% of tickets)

```
Input: Customer email/phone OR order number
  ↓
1. Look up order (orders query with email filter or order name)
2. Check displayFulfillmentStatus
3. If UNFULFILLED → "Your order is being prepared, not yet shipped"
4. If FULFILLED → Pull fulfillments[].trackingInfo
   → Extract trackingCompany, trackingNumber, trackingUrl
   → Compose: "Your order #{name} was shipped via {carrier}. Track here: {url}"
5. If PARTIALLY_FULFILLED → List which items shipped, which pending
6. Update order note: "WISMO inquiry handled. Tracking shared. —AI {timestamp}"
7. Close/resolve ticket in helpdesk
```

**Output**: Resolved ticket + order note updated. NOT advice — actual response sent.

### Returns/Exchanges (15-20%)

```
Input: Customer wants to return/exchange item from order
  ↓
1. Look up order → check order date
2. Check return eligibility:
   - Is order within return window? (merchant policy: typically 7-15 days in India)
   - Is product returnable? (check product tags for "non-returnable", "final-sale")
   - Is item fulfilled? (can't return unfulfilled items)
3. If eligible:
   → Call returnRequest or returnCreate mutation
   → Share return instructions with customer
   → Update order note
4. If NOT eligible:
   → Explain why (past window, non-returnable category)
   → Offer alternative (store credit, exchange) if merchant policy allows
5. If exchange:
   → Check replacement variant availability (inventory query)
   → Create return + note for ops team to ship replacement
```

**Guard rails**: Return window days and non-returnable product tags must be configurable per merchant.

### Product Queries (10-15%)

```
Input: Customer asks about product sizing/material/compatibility
  ↓
1. Identify product from context (product title, URL, or order line items)
2. Query product → variants + metafields
3. Pull relevant info:
   - Sizing: variant options, size chart metafield
   - Material: metafield (namespace: custom, key: material/fabric)
   - Compatibility: product tags, description
   - Care instructions: metafield
4. Compose answer from actual product data
5. If info not in Shopify data → escalate to human with "Product info gap" tag
```

### Payment Issues (5-10%)

```
Input: Customer asks about refund status, payment failure, COD conversion
  ↓
1. Look up order → check displayFinancialStatus
2. If asking about refund status:
   → Check order.refunds[] → show refund amount, date, method
   → Share typical refund processing time (3-7 business days for cards, 5-10 for UPI)
3. If COD-to-prepaid conversion:
   → This requires payment link generation — NOT available via Shopify Admin API alone
   → Escalate with note, or integrate with payment gateway (Razorpay/Cashfree)
4. Update order note
```

**Partial automation**: Refund status lookups are fully automatable. COD conversion and payment gateway issues need integration beyond Shopify.

### Order Modifications (~5%)

```
Input: Customer wants to cancel order or change address
  ↓
1. Look up order → check displayFulfillmentStatus
2. If UNFULFILLED and customer wants cancellation:
   → Call orderCancel with reason: CUSTOMER, restock: true, notifyCustomer: true
   → Update order note
3. If FULFILLED → "Order already shipped, cannot cancel. Would you like to initiate a return?"
4. If address change and UNFULFILLED:
   → Call orderUpdate to change shippingAddress
5. If address change and FULFILLED → escalate to ops (courier address change)
```

### Complaints (5%) — HUMAN ESCALATION

```
Input: Damaged product, wrong item, quality issue
  ↓
1. Look up order details
2. Log complaint details in order note
3. Tag order with "complaint-{type}" (complaint-damaged, complaint-wrong-item)
4. Create/escalate ticket to human CS manager with full context
5. DO NOT process refund or return automatically for complaints
```

**Why human**: Complaints need judgment — photo verification, supplier accountability, replacement vs refund decision, potential fraud detection.

---

## Helpdesk Integration Points

### Freshdesk

- **MCP server available**: `freshdesk_mcp` (GitHub: effytech/freshdesk_mcp)
- **Capabilities**: Create tickets, update tickets, reply to tickets, list tickets, delete tickets
- **Integration**: Composio also offers Freshdesk MCP for Claude Code
- **API**: REST API at `{domain}.freshdesk.com/api/v2/`
- **Key endpoints**: `/tickets`, `/contacts`, `/conversations`

### Gorgias

- **No MCP server found** — would need custom integration
- **API**: REST API at `{domain}.gorgias.com/api/`
- **Capabilities**: Create/update/close tickets, manage customers, send messages
- **Shopify integration**: Native — shows Shopify order data in ticket sidebar
- **Key feature**: Can execute Shopify actions (cancel, refund) directly from ticket via their integration

### Zendesk

- **MCP server available**: `zendesk-mcp-server` (GitHub: reminia/zendesk-mcp-server)
- **Capabilities**: Retrieve/manage tickets and comments, access Help Center articles
- **Also available via**: Merge.dev connector, Speakeasy MCP

### Integration Pattern

The skill should work in two modes:

1. **Standalone mode**: Skill reads ticket content, looks up Shopify data, generates response + takes actions, logs everything to order notes. Human pastes response into helpdesk.
2. **Integrated mode** (with helpdesk MCP): Skill reads ticket from helpdesk, processes it, responds directly in helpdesk, updates ticket status, AND logs to Shopify order notes.

---

## WhatsApp Channel (India-specific)

Most Indian D2C brands handle 30-50% of CS volume via WhatsApp.

### Providers with API Access

| Provider | Strength | API Available | Shopify Integration |
|---|---|---|---|
| **Interakt** (Jio Haptik) | D2C-focused, Indian market | Yes — REST API | Native Shopify app |
| **Wati** | No-code chatbot builder | Yes — REST API | Via Zapier/native |
| **Gupshup** | Enterprise BSP | Yes — REST API | Custom |

### What the Skill Does NOT Do with WhatsApp

The skill does NOT replace the WhatsApp chatbot or manage the WhatsApp channel directly. Instead:
- It processes tickets that originated from WhatsApp (received via helpdesk integration)
- It generates responses that can be sent back via WhatsApp through the helpdesk
- The actual WhatsApp message sending/receiving is handled by Interakt/Wati/Gupshup + helpdesk integration

---

## What's IN Scope

- Order lookup by email, phone, order number, or customer name
- WISMO response generation with actual tracking data
- Return eligibility checking against merchant-configured policies
- Return initiation via Shopify Returns API
- Refund processing via Shopify Refund API (with confirmation gate)
- Order cancellation for unfulfilled orders (with confirmation gate)
- Shipping address updates on unfulfilled orders
- Product information lookup from catalog data + metafields
- Order note updates after every interaction
- Ticket categorization and routing
- Refund status lookup and timeline sharing
- Response generation in English and Hindi (common for Indian D2C)

## What's OUT of Scope

- **Phone/IVR systems** — Requires telephony integration, different skill domain
- **Social media management** — That's the `social` skill
- **Proactive outreach** (abandoned cart, review requests) — That's `crm-automation`
- **Complaint escalation workflows** — Needs human judgment for damage assessment, fraud detection
- **COD-to-prepaid conversion** — Requires payment gateway integration (Razorpay/Cashfree), not Shopify Admin API
- **Courier chase/escalation** — Requires direct courier API integration (Shiprocket, Delhivery), not just tracking lookup
- **Live chat widget management** — Infrastructure concern, not CS agent work
- **Training/SOP documentation** — One-time setup, not daily ticket work

---

## What Needs Human Escalation

| Scenario | Why |
|---|---|
| Damaged/wrong item complaints | Photo verification, supplier accountability, fraud risk |
| Refund amount > merchant threshold | Financial control — merchant sets max auto-refund |
| Customer threatening legal action | Legal risk management |
| Repeat complainers (>3 complaints in 30 days) | Potential abuse pattern |
| Product not in Shopify catalog | Can't look up info, likely custom/discontinued |
| Order older than 90 days | Edge case, may need manual investigation |
| Payment gateway failures | Requires Razorpay/Cashfree dashboard access |

---

## Available APIs & MCP Servers

| Tool | Type | What It Provides |
|---|---|---|
| **Shopify Admin GraphQL API** | API | Orders, customers, fulfillments, refunds, returns, products |
| **shopify-dev MCP** | MCP (in plugin) | Schema introspection, API learning, GraphQL validation |
| **Freshdesk MCP** | MCP (effytech/freshdesk_mcp) | Ticket CRUD, conversations, contacts |
| **Zendesk MCP** | MCP (reminia/zendesk-mcp-server) | Ticket management, Help Center access |
| **Gorgias API** | REST API (no MCP) | Ticket CRUD, messages, Shopify actions |
| **Interakt API** | REST API (no MCP) | WhatsApp messaging, notifications |

---

## Output Format

The skill produces **resolved tickets with actions taken**, not advice.

Each resolution includes:
1. **Action taken**: What was done in Shopify (e.g., "Shared tracking for fulfillment #F1234", "Initiated return RMA-5678", "Processed refund ₹1,299 to original payment method")
2. **Customer response**: The actual message sent/to-be-sent to the customer
3. **Order note**: What was logged on the Shopify order timeline
4. **Ticket status**: RESOLVED, ESCALATED (with reason), or PENDING (waiting for customer)

Example output for a WISMO ticket:
```
TICKET: #4521 — WISMO
STATUS: RESOLVED

ACTION: Looked up order #1847. Shipped via Delhivery, tracking 9823746501.
        Estimated delivery: March 17, 2026.

RESPONSE TO CUSTOMER:
"Hi Priya, your order #1847 has been shipped via Delhivery.
 Tracking number: 9823746501
 Track here: https://www.delhivery.com/track/package/9823746501
 Expected delivery: March 17, 2026.
 Let us know if you need anything else!"

ORDER NOTE: "WISMO handled — tracking shared (Delhivery 9823746501, ETA Mar 17). —AI 2026-03-14"
```

---

## Key Implementation Considerations

1. **Confirmation gates**: Refunds, cancellations, and returns MUST require explicit confirmation before execution. These are irreversible.
2. **Merchant-configurable policies**: Return window (days), non-returnable product tags, max auto-refund amount, working hours for responses.
3. **Rate limiting**: Shopify Admin API has rate limits. Batch ticket processing needs throttling.
4. **Guest checkouts**: `customer` field is null for guest orders. Must fall back to email/phone matching.
5. **Multi-currency**: Indian D2C brands may sell in INR but some in USD. Use `totalPriceSet` (MoneyBag) for accurate amounts.
6. **Hindi language support**: Many Indian D2C customers communicate in Hindi or Hinglish. Response templates should support both.

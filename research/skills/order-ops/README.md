# Order-Ops Skill — Research

> Replaces the **Operations Executive** role (₹3-6 LPA, 3-8 people per company, 70-80% automatable)

## Role Being Replaced

The Operations Executive at a D2C brand (₹50-200Cr revenue, India) handles:

| Daily Task | Volume | Time Spent |
|---|---|---|
| Process new orders — verify payment, check address, flag COD | 200-1000 orders/day | 2-3 hrs |
| Generate pick lists, push to 3PL, bulk AWB generation | 200-1000 shipments/day | 1-2 hrs |
| Update tracking in Shopify, send dispatch confirmations | Same as above | 1 hr |
| NDR handling — follow up on failed deliveries | 30-50 cases/day | 2-3 hrs |
| Process return requests — check window, generate reverse pickup | 20-100/day | 1-2 hrs |
| Reconcile dispatch data — match OMS vs courier manifest | Daily | 1 hr |
| RTO reduction — analyze NDR reasons, COD confirmation before dispatch | Ongoing | 1 hr |

**Total: 8-12 hrs/day across 3-8 people. Claude can automate 70-80% of this.**

---

## Data Sources & APIs

### 1. Shopify Admin GraphQL API (Primary)

All new apps must use GraphQL Admin API (REST deprecated Oct 2024, mandatory GraphQL for new apps since Apr 2025).

#### Order Management

| Operation | API | Purpose |
|---|---|---|
| List/filter orders | `orders` query | Fetch orders by status, financial_status, fulfillment_status, tags, date range |
| Get order details | `order` query | Full order data including line items, shipping address, payment, risk |
| Update order | `orderUpdate` mutation | Update tags, notes, shipping address, metafields |
| Add tags | `tagsAdd` mutation | Add tags without overwriting existing ones (e.g., `cod-verified`, `address-incomplete`, `high-risk`) |
| Cancel order | `orderCancel` mutation | Cancel with reason and refund |
| Close/reopen | `orderClose` / `orderOpen` mutations | Manage order lifecycle |

#### Fraud & Risk Assessment

| Operation | API | Purpose |
|---|---|---|
| Read risk level | `order.riskLevel` field | Shopify ML-powered fraud score (0-1) |
| Create risk assessment | `orderRiskAssessmentCreate` mutation | Custom risk facts with `POSITIVE`/`NEUTRAL`/`NEGATIVE` sentiment, risk level `LOW`/`HIGH`/`PENDING` |
| Read risk facts | `order.risks` field | Fraud indicators: AVS, IP geolocation, billing/shipping mismatch |

#### Fulfillment Management

| Operation | API | Purpose |
|---|---|---|
| List fulfillment orders | `order.fulfillmentOrders` query | Get all fulfillment orders for an order |
| Create fulfillment | `fulfillmentCreateV2` mutation | Create fulfillment with tracking info, notify customer |
| Hold fulfillment | `fulfillmentOrderHold` mutation | Hold orders (up to 10 holds per app per fulfillment order) |
| Release hold | `fulfillmentOrderReleaseHold` mutation | Release held orders for processing |
| Move fulfillment | `fulfillmentOrderMove` mutation | Move between locations |
| Update tracking | `fulfillmentTrackingInfoUpdateV2` mutation | Update tracking number, URL, company |

**Fulfillment Order Lifecycle:** `OPEN` → `IN_PROGRESS` → `CLOSED` (with `CANCELLED`, `INCOMPLETE` branches)

**Supported Actions:** `CREATE_FULFILLMENT`, `MOVE`, `REQUEST_FULFILLMENT`, `HOLD`, `RELEASE_HOLD`, `CANCEL_FULFILLMENT_ORDER`

#### Returns Management (API version 2025-07+)

| Operation | API | Purpose |
|---|---|---|
| Check returnables | `returnableFulfillments` query | Which items can be returned |
| Calculate return | `returnCalculate` query | Financial impact preview |
| Request return | `returnRequest` mutation | Creates return with `REQUESTED` status |
| Approve return | `returnApproveRequest` mutation | Moves to `OPEN`, creates reverse fulfillment orders |
| Decline return | `returnDeclineRequest` mutation | Reject return request |
| Create return directly | `returnCreate` mutation | Skip approval, directly `OPEN` |
| Process return | `returnProcess` mutation | Issue refund + set item dispositions in one call (replaces deprecated `returnRefund`) |
| Cancel/close/reopen | `returnCancel` / `returnClose` / `returnReopen` mutations | Manage return lifecycle |
| Reverse fulfillment | `reverseFulfillmentOrder` queries | Track reverse logistics |
| Reverse delivery | `reverseDeliveryCreate` mutation | Package and send items back |

**Return Lifecycle:** `REQUESTED` → `OPEN` → `CLOSED` (with `DECLINED`, `CANCELLED` branches)

### 2. Shiprocket API (Courier/Logistics)

Base URL: `https://apiv2.shiprocket.in/v1/external/`

| Category | Endpoint | Method | Purpose |
|---|---|---|---|
| **Auth** | `/auth/login` | POST | Get auth token (email + password) |
| **Orders** | `/orders/create/adhoc` | POST | Create shipment order |
| **Orders** | `/orders/print/invoice` | POST | Generate invoice PDF |
| **Courier** | `/courier/serviceability/` | GET | Check courier serviceability + rates |
| **AWB** | `/courier/assign/awb` | POST | Assign AWB code to shipment → returns tracking code + courier |
| **Pickup** | `/courier/generate/pickup` | POST | Schedule courier pickup |
| **Labels** | `/courier/generate/label` | POST | Generate shipping label PDF |
| **Manifest** | `/manifests/generate` | POST | Generate manifest document |
| **Manifest** | `/manifests/print` | POST | Get manifest PDF URL |
| **Tracking** | `/courier/track/awb/{awb_code}` | GET | Track shipment by AWB |
| **NDR** | `/ndr` | GET | List all shipments in NDR status |
| **NDR** | `/ndr/{AWB}` | GET | Get specific NDR details |
| **NDR** | `/ndr/reattempt` | POST | Reattempt delivery (AWB, address, phone, deferred_date) |
| **Returns** | `/orders/create/return` | POST | Create return order |

### 3. Shiprocket MCP Server (Available)

GitHub: [bfrs/shiprocket-mcp](https://github.com/bfrs/shiprocket-mcp)

Exposes 10 tools via MCP:

| Tool | Purpose |
|---|---|
| `estimated_date_of_delivery` | EDD for any location |
| `shipping_rate_calculator` | Compare courier rates and coverage |
| `list_pickup_addresses` | List configured pickup addresses |
| `order_list` | Fetch recent orders |
| `order_track` | Track by AWB, Shiprocket ID, or source order ID |
| `order_ship` | Ship to courier partner based on rules |
| `order_pickup_schedule` | Schedule pickup |
| `generate_shipment_label` | Create shipping labels |
| `order_cancel` | Cancel orders |
| `order_create` | Create new orders |

**Config:** Requires `SELLER_EMAIL` and `SELLER_PASSWORD` environment variables. Node.js >20.0.0.

### 4. Shopify MCP Server (Available in plugin)

The `shopify-dev` MCP server provides:
- `introspect_graphql_schema` — Explore Shopify GraphQL schema
- `validate_graphql_codeblocks` — Validate GraphQL queries
- `search_docs_chunks` — Search Shopify documentation
- `learn_shopify_api` — Learn about specific API areas

---

## What the Skill Should Do (Exact Workflows)

### Workflow 1: New Order Processing (runs every 15-30 min or on webhook)

```
1. FETCH all orders with financial_status=paid, fulfillment_status=unfulfilled
2. For each order:
   a. CHECK payment verification (financial_status == 'paid' or 'authorized')
   b. VALIDATE shipping address completeness (address1, city, province, zip, phone)
   c. If address incomplete → TAG 'address-incomplete', HOLD fulfillment order
   d. CHECK if COD (gateway == 'Cash on Delivery')
      - If COD → TAG 'cod-unverified', HOLD fulfillment
      - Flag if order total > ₹3000 (high-value COD risk)
   e. CHECK Shopify fraud risk level
      - If HIGH → TAG 'high-risk', HOLD fulfillment, add note with risk facts
   f. CHECK for duplicate orders (same customer, same items, within 24hrs)
      - If duplicate → TAG 'possible-duplicate', HOLD fulfillment
   g. If all checks pass → TAG 'ready-to-ship'
3. OUTPUT: List of processed orders with actions taken
```

### Workflow 2: Fulfillment Push (daily or on-demand)

```
1. FETCH all orders tagged 'ready-to-ship' + unfulfilled
2. For each order:
   a. CHECK courier serviceability via Shiprocket API (pickup pincode → delivery pincode)
   b. SELECT optimal courier (cheapest for prepaid, most reliable for COD)
   c. CREATE order in Shiprocket with order details
   d. ASSIGN AWB via Shiprocket API
   e. GENERATE shipping label
   f. UPDATE Shopify fulfillment with tracking number + courier URL
   g. TAG 'dispatched', remove 'ready-to-ship'
3. SCHEDULE pickup via Shiprocket
4. GENERATE manifest
5. OUTPUT: Dispatch summary — X orders shipped, Y failed (with reasons)
```

### Workflow 3: Tracking Sync (runs every 2-4 hours)

```
1. FETCH all orders tagged 'dispatched' + fulfillment_status=fulfilled
2. For each:
   a. GET tracking status from Shiprocket by AWB
   b. If status changed → UPDATE order metafield with latest status
   c. If DELIVERED → TAG 'delivered', close order
   d. If NDR → TAG 'ndr-pending' (see Workflow 4)
   e. If RTO_INITIATED → TAG 'rto-initiated'
3. OUTPUT: Tracking update summary
```

### Workflow 4: NDR Management (daily)

```
1. FETCH NDR list from Shiprocket API
2. For each NDR shipment:
   a. GET NDR reason (wrong address, customer unavailable, refused, etc.)
   b. TAG order with NDR reason (e.g., 'ndr-wrong-address', 'ndr-refused')
   c. ADD order note with NDR details + timestamp
   d. Based on reason:
      - Wrong address → CHECK if customer provided alternate address (metafield), auto-reattempt
      - Customer unavailable → Schedule reattempt for next day
      - Refused → TAG 'rto-candidate', flag for review
   e. If 3+ NDR attempts → TAG 'rto-confirmed', initiate return to origin
3. OUTPUT: NDR action summary — X reattempted, Y marked RTO
```

### Workflow 5: Return Processing (on-demand or daily scan)

```
1. FETCH return requests from Shopify (returns with status REQUESTED)
2. For each return:
   a. CHECK return window (order.created_at + return_window_days from store policy)
   b. CHECK returnableFulfillments — are items eligible?
   c. If within window + eligible:
      - APPROVE return via returnApproveRequest
      - CREATE reverse pickup via Shiprocket return order API
      - TAG order 'return-approved'
   d. If outside window or ineligible:
      - DECLINE return with reason
      - TAG 'return-declined'
3. Track reverse shipment status
4. When items received → PROCESS return (returnProcess mutation — refund + restock)
5. OUTPUT: Return processing summary
```

### Workflow 6: Daily Ops Dashboard (morning run)

```
1. AGGREGATE from Shopify + Shiprocket:
   - Orders received (last 24h) — total, prepaid vs COD, average value
   - Orders dispatched — count, courier breakdown
   - Orders in transit — count, stuck (no update >48h)
   - NDR pending — count by reason
   - Returns pending — count, value
   - RTO rate (last 7 days, 30 days)
   - SLA breaches — orders not dispatched within SLA (e.g., 24h for prepaid, 48h for COD)
2. FLAG actionable items:
   - Orders stuck in 'ready-to-ship' > 24h
   - NDRs not reattempted
   - Returns not processed within 48h
3. OUTPUT: Structured ops summary with action items
```

---

## Automations to Build

| Automation | Trigger | Action |
|---|---|---|
| **COD Risk Tagger** | New COD order | Score based on: order value, customer order history, address completeness, pincode RTO history → tag `cod-high-risk` / `cod-low-risk` |
| **Address Validator** | New order | Check address completeness (all fields present, valid pincode format, phone 10 digits) → tag `address-verified` / `address-incomplete` |
| **Duplicate Detector** | New order | Same customer email/phone + same SKUs within 24h → tag `possible-duplicate` + hold |
| **Auto-Fulfillment** | Order tagged `ready-to-ship` | Create Shiprocket order → assign AWB → generate label → update Shopify tracking |
| **NDR Auto-Reattempt** | NDR detected | If reason is recoverable (wrong address with correction, unavailable) → auto-reattempt via Shiprocket |
| **Return Auto-Processor** | Return request received | Check eligibility → approve/decline → create reverse pickup |
| **SLA Monitor** | Scheduled (hourly) | Flag orders exceeding dispatch SLA, NDRs not acted on, returns not processed |
| **RTO Risk Scorer** | Pre-dispatch (COD orders) | Score based on customer history, pincode RTO rate, order value → hold high-risk |

---

## Scope

### IN Scope

- Order verification and tagging (payment, address, fraud, COD)
- Fulfillment order management (hold, release, create fulfillment)
- Tracking number sync between Shiprocket and Shopify
- AWB generation and label creation via Shiprocket
- NDR detection and auto-reattempt scheduling
- Return request processing (approve/decline/refund)
- Dispatch reconciliation (Shopify orders vs Shiprocket manifest)
- RTO risk scoring and pre-dispatch flagging
- Daily ops dashboard with actionable items
- Order tagging for workflow status tracking

### OUT of Scope

- **Warehouse management** — That's Unicommerce/WMS territory. Skill doesn't manage inventory location, bin picking, or warehouse ops.
- **Customer communication** — No WhatsApp messages, emails, or SMS to customers. That's the customer-service skill.
- **NDR phone calls** — Requires IVR/WhatsApp bot (Shiprocket Engage, MSG91), not Claude. Skill only handles the data/reattempt side.
- **COD confirmation calls** — Same as above; requires voice/WhatsApp integration.
- **Payment gateway management** — No payment processing, reconciliation with banks.
- **Courier partner onboarding** — No rate negotiation or courier setup.
- **Custom packaging/labeling** — Physical ops, not automatable.

---

## Available MCP Servers

| MCP Server | Status | What It Provides |
|---|---|---|
| **Shopify Dev** (`shopify-dev`) | Available in plugin | GraphQL schema introspection, API docs search, query validation |
| **Shiprocket** (`bfrs/shiprocket-mcp`) | Available (npm) | 10 tools: order CRUD, tracking, AWB, labels, pickup scheduling, rate calculation |
| **Shopify Admin API** | Direct API | Full order/fulfillment/return management via GraphQL |

### MCP Configuration for Shiprocket

```json
{
  "mcpServers": {
    "shiprocket": {
      "command": "npx",
      "args": ["-y", "shiprocket-mcp"],
      "env": {
        "SELLER_EMAIL": "${SHIPROCKET_EMAIL}",
        "SELLER_PASSWORD": "${SHIPROCKET_PASSWORD}"
      }
    }
  }
}
```

### Required Shopify API Scopes

- `read_orders` / `write_orders` — Order management, tagging, risk assessment
- `read_fulfillments` / `write_fulfillments` — Fulfillment creation, tracking updates
- `write_merchant_managed_fulfillment_orders` — Hold/release fulfillment orders
- `write_third_party_fulfillment_orders` — 3PL fulfillment management
- `read_returns` / `write_returns` — Return request management

---

## Output the Skill Produces

This skill produces **actions, not reports**:

| Output | Format | Example |
|---|---|---|
| Processed orders | Tagged + held/released in Shopify | 847 orders processed, 12 held (3 high-risk, 5 address-incomplete, 4 COD-unverified) |
| Fulfilled orders | Tracking updated in Shopify | 312 orders fulfilled with AWB, labels generated, pickup scheduled |
| NDR actions | Reattempts scheduled in Shiprocket | 28 NDRs: 18 auto-reattempted, 6 marked RTO, 4 pending review |
| Returns processed | Approved/declined in Shopify | 45 returns: 38 approved + reverse pickup created, 7 declined (outside window) |
| Risk-tagged orders | Tags applied in Shopify | 23 orders tagged high-risk-cod, 8 tagged address-incomplete |
| Ops summary | Structured daily digest | Actionable items: 5 orders stuck >24h, 3 NDRs not acted on, 2 returns pending |

---

## Key India D2C Context

- **COD dominance**: 60-70% of orders are COD in most D2C brands. COD verification and RTO reduction are the #1 ops priority.
- **RTO rates**: Average 25-35% for COD orders. Each RTO costs ₹100-200 in shipping + packaging + opportunity cost.
- **Shiprocket market share**: Dominant aggregator in India D2C. Most brands ₹50-200Cr use Shiprocket or Delhivery Direct.
- **Dispatch SLAs**: Industry standard is 24h for prepaid, 48h for COD (after verification).
- **NDR handling**: 30-50 NDRs/day for a ₹100Cr brand. Most are "customer unavailable" or "wrong address" — recoverable with reattempt.
- **Return window**: Typically 7-15 days. Exchanges preferred over refunds to retain revenue.

---

## Sources

- [Shopify Order REST API](https://shopify.dev/docs/api/admin-rest/latest/resources/order)
- [Shopify FulfillmentOrder GraphQL](https://shopify.dev/docs/api/admin-graphql/latest/objects/FulfillmentOrder)
- [Build Fulfillment Solutions](https://shopify.dev/docs/apps/build/orders-fulfillment/order-management-apps/build-fulfillment-solutions)
- [Build Return Management](https://shopify.dev/docs/apps/build/orders-fulfillment/returns-apps/build-return-management)
- [Returns Processing API](https://shopify.dev/changelog/returns-processing-api)
- [orderRiskAssessmentCreate](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderRiskAssessmentCreate)
- [orderUpdate mutation](https://shopify.dev/docs/api/admin-graphql/latest/mutations/orderUpdate)
- [fulfillmentOrderHold](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentOrderHold)
- [fulfillmentCreateV2](https://shopify.dev/docs/api/admin-graphql/latest/mutations/fulfillmentCreateV2)
- [Shiprocket API Documentation](https://apidocs.shiprocket.in/)
- [Shiprocket MCP Server](https://github.com/bfrs/shiprocket-mcp)
- [Shiprocket API Helpsheet](https://support.shiprocket.in/support/solutions/articles/43000337456-shiprocket-api-document-helpsheet)
- [Shopify Fraud Analysis](https://help.shopify.com/en/manual/fulfillment/managing-orders/protecting-orders/fraud-analysis)
- [Shopify Flow for High-Risk Orders](https://help.shopify.com/en/manual/orders/fraud-filter)

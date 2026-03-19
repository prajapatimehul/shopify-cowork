# Reconciliation Skill — Research Brief

## Role This Replaces

**Accounts Executive** (₹3-6 LPA, 2-4 per company, 75-85% automatable)

### What They Do Daily

| Task | Time Spent | Automatable? |
|---|---|---|
| Download settlement reports from Razorpay, Amazon, Flipkart, courier COD partners | 30 min/day | Yes — API/MCP pulls |
| Match 15,000+ transactions/month line by line in Excel | 3-4 hrs/day | Yes — deterministic matching |
| Map refunds to original orders | 1 hr/day | Yes — order ID linkage |
| Flag commission overcharges, weight disputes, unclaimed TCS | 1 hr/day | Yes — rule-based detection |
| Bank reconciliation — match every credit/debit with source | 1-2 hrs/day | Yes — UTR/reference matching |
| Prepare GST working papers (multi-state) | periodic | OUT OF SCOPE (separate skill) |
| File TDS returns quarterly | periodic | OUT OF SCOPE |
| Maintain vendor ledgers | ongoing | OUT OF SCOPE |

---

## Data Sources & API Endpoints

### 1. Shopify Admin API (GraphQL — mandatory since April 2025)

The Shopify store is the **source of truth** for orders, refunds, and expected payment amounts.

#### Order Object — Key Fields
```graphql
query {
  orders(first: 50, query: "financial_status:paid") {
    edges {
      node {
        id
        name                          # e.g. "#1042"
        createdAt
        displayFinancialStatus        # paid, partially_refunded, refunded, pending, etc.
        totalPriceSet { shopMoney { amount currencyCode } }
        subtotalPriceSet { shopMoney { amount currencyCode } }
        totalTaxSet { shopMoney { amount currencyCode } }
        totalShippingPriceSet { shopMoney { amount currencyCode } }
        totalDiscountsSet { shopMoney { amount currencyCode } }
        netPaymentSet { shopMoney { amount currencyCode } }  # received - refunded
        fullyPaid
        paymentGatewayNames           # ["Razorpay", "Cash on Delivery (COD)"]

        transactions(first: 10) {
          id
          kind                        # SALE, CAPTURE, REFUND, VOID, AUTHORIZATION
          status                      # SUCCESS, PENDING, FAILURE, ERROR
          gateway                     # "razorpay", "cod", "stripe"
          formattedGateway            # "Razorpay"
          amountSet { shopMoney { amount currencyCode } }
          fees { amount { amount currencyCode } type flatFeeName percentage }  # Shopify Payments only
          settlementCurrency
          settlementCurrencyRate
          createdAt
          processedAt
          receiptJson                 # Gateway-specific (NOT stable — don't parse for business logic)
          paymentId                   # Gateway payment reference
          parentTransaction { id }    # Links capture → authorization
        }

        refunds {
          id
          createdAt
          note
          totalRefundedSet { shopMoney { amount currencyCode } }
          refundLineItems(first: 20) {
            edges { node {
              quantity
              restockType               # RETURN, CANCEL, NO_RESTOCK
              lineItem { title sku }
            }}
          }
          transactions(first: 5) {
            id
            kind                        # REFUND
            status
            gateway
            amountSet { shopMoney { amount currencyCode } }
            paymentId
          }
        }
      }
    }
  }
}
```

#### Shopify Payments Payout Objects (if using Shopify Payments)
```graphql
# ShopifyPaymentsAccount → payouts, balanceTransactions
# ShopifyPaymentsPayout — id, issuedAt, net, gross, fee, status (scheduled/in_transit/paid)
# ShopifyPaymentsBalanceTransaction — type, amount, fee, net, payout, sourceOrder
```

**Important limitations:**
- Default access = last 60 days only. Need `read_all_orders` scope for full history.
- `fees` array on OrderTransaction only populated for Shopify Payments, not third-party gateways.
- `receiptJson` is gateway-specific and unstable — don't parse it for matching logic.

---

### 2. Razorpay (Primary Payment Gateway for Indian D2C)

#### Settlement Recon API

**Endpoint:** `POST /settlements/recon/combined`

**Request:**
```json
{
  "year": 2026,
  "month": 3,
  "day": 14
}
```

**Response Fields (per item):**

| Field | Description |
|---|---|
| `entity_id` | Razorpay payment/refund/transfer ID (e.g. `pay_DEXrnipqTmWVGE`) |
| `type` | `payment`, `refund`, `transfer`, `adjustment` |
| `debit` | Amount debited from merchant account (in paise) |
| `credit` | Amount credited to merchant account (in paise) |
| `amount` | Transaction amount (in paise) |
| `fee` | Processing fee charged (in paise) |
| `tax` | GST on processing fee (in paise) |
| `currency` | INR |
| `settlement_id` | Unique settlement batch ID |
| `order_id` | Razorpay order ID (maps to Shopify via notes/receipt) |
| `payment_id` | Razorpay payment ID |
| `description` | Transaction description |
| `method` | Payment method (upi, card, netbanking, wallet) |
| `on_hold` | Whether settlement is held |
| `settled_at` | Unix timestamp of settlement |
| `created_at` | Unix timestamp of transaction creation |
| `notes` | Custom key-value pairs (typically contains Shopify order ID) |
| `utr` | Bank UTR for the settlement |

#### Other Razorpay APIs
- `GET /payments/{id}` — Fetch individual payment details
- `GET /refunds/{id}` — Fetch refund details, includes `payment_id` link
- `GET /settlements` — List all settlements with status and amount
- `GET /settlements/{id}` — Single settlement details

#### Razorpay MCP Server (Official)

Available tools relevant to reconciliation:
| Tool | Description |
|---|---|
| `fetch_all_settlements` | List all settlements |
| `fetch_settlement_with_id` | Get settlement details by ID |
| `fetch_settlement_recon_details` | **Key tool** — full recon report for a settlement period |
| `fetch_payment` | Get payment details by ID |
| `fetch_all_payments` | List payments with filters |
| `fetch_refund` | Get refund details by ID |
| `fetch_all_refunds` | List all refunds |
| `fetch_multiple_refunds_for_payment` | All refunds for a specific payment |
| `create_instant_settlement` | Trigger instant settlement |

**Deployment:** Remote hosted (recommended, 99.9% uptime) or local via Docker. Config requires `RAZORPAY_KEY_ID` and `RAZORPAY_KEY_SECRET`.

---

### 3. Stripe (Alternative Payment Gateway)

#### Payout Reconciliation

**Key API:** Balance Transaction endpoint with payout parameter
```
GET /v1/balance_transactions?payout={payout_id}
```

**Report Fields (Itemized Payout Reconciliation):**

| Field | Description |
|---|---|
| `automatic_payout_id` | Payout batch ID |
| `automatic_payout_effective_at` | When payout hits bank |
| `balance_transaction_id` | Individual transaction ID |
| `reporting_category` | charge, refund, dispute, fee, etc. |
| `gross` | Gross amount |
| `fee` | Processing fee |
| `net` | Net amount (gross - fee) |
| `charge_id` | Stripe charge ID |
| `payment_intent_id` | Links to Shopify order |
| `created` | Transaction timestamp |
| `available_on` | When funds available |
| `currency` | Currency code |
| `description` | Transaction description |

#### Stripe MCP Server (Official)

Available tools: `retrieve_balance`, plus payment/refund/customer tools. Limited settlement-specific tooling — may need direct API calls for payout reconciliation.

---

### 4. Amazon Seller Central (Marketplace)

#### Settlement Report (V2 Format)

Downloaded from Seller Central or via SP-API (`GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE`).

| Field | Description |
|---|---|
| `settlement-id` | Settlement period identifier |
| `settlement-start-date` | Period start (ISO 8601) |
| `settlement-end-date` | Period end (ISO 8601) |
| `order-id` | Amazon order ID |
| `seller-order-id` | Seller's reference (may contain Shopify order #) |
| `transaction-type` | Order, Refund, ServiceFee, Adjustment, Transfer, etc. |
| `amount-type` | ItemPrice, ItemFees, Promotion, ItemWithheldTax, etc. |
| `amount-description` | Principal, Commission, ShippingHB, FBAFee, etc. |
| `amount` | Transaction amount |
| `quantity-purchased` | Units sold |
| `sku` | Product SKU (links to Shopify variant) |
| `marketplace-name` | e.g. Amazon.in |
| `fulfillment-id` | Fulfillment reference |
| `posted-date` | When transaction posted |

**Key fee types to validate:**
- Referral Fee (commission — category-specific %)
- FBA Per Unit Fulfillment Fee
- Closing Fee
- Shipping HB (Handling & Bundling)
- TCS (Tax Collected at Source — 1% of net value)
- TDS (Tax Deducted at Source)

---

### 5. Flipkart Seller (Marketplace)

#### Settlement Report Structure

Four sheets in the settlement report:

**Orders Sheet:**
| Field | Description |
|---|---|
| Order ID | Flipkart order reference |
| SKU | Product identifier |
| Sale Amount | Order value |
| Commission Fee | Category-based % |
| Fixed Fee | Per-order fixed charge |
| Shipping Fee | Logistics charge |
| Collection Fee | Payment collection charge |
| TDS | Tax deducted at source |
| TCS | Tax collected at source (0.5% — 0.25% CGST + 0.25% SGST intra-state) |
| Settlement Amount | Final amount after all deductions |

**Ads Sheet:** Advertising deductions
**Non-Order SPF Sheet:** Warehousing fees, inventory damage reparations
**TDS Sheet:** TDS payment details with certificates

**Additional reports needed:**
- Order Report — item-level details with quantities
- Sales Report — invoice amounts, fulfillment status, returns
- Returns Report — RTO and customer returns

---

### 6. Courier COD Remittance (Shiprocket / Delhivery)

#### Shiprocket COD Report

Available via Shiprocket dashboard → Billing → COD Remittance tab, or scheduled report (daily/weekly/monthly via email/webhook).

| Field | Description |
|---|---|
| AWB Number | Shipment tracking ID |
| Order ID | Links to Shopify order |
| COD Amount | Amount collected from customer |
| Remittance Number | Bank transfer batch ID |
| Remittance Date | When money was transferred |
| Bank Transaction ID / UTR | Bank reference for verification |
| Status | Remitted / Pending / In Transit |
| Delivery Date | When shipment was delivered |

#### Delhivery COD Report

| Field | Description |
|---|---|
| Waybill Number | Tracking ID |
| Order Reference | Seller's order ID |
| COD Amount | Amount collected |
| Remittance Number | Batch transfer ID |
| Remittance Processed Date | Transfer date |
| Bank Transaction ID | UTR reference |
| Remittance Amount | Actual amount transferred |
| Status | Transfer status |

**COD remittance cycle:** Typically 48 hours post-delivery (Delhivery), 2-7 days (Shiprocket depending on plan).

---

## What the Skill Should Do — Exact Workflow

### Phase 1: Data Ingestion

1. **Pull Shopify orders** for the reconciliation period via GraphQL Admin API
   - All orders with `financial_status` in [paid, partially_refunded, refunded]
   - Include transactions, refunds, payment gateway names
   - Build a canonical order ledger: `{order_id, order_name, total, payment_gateway, payment_ref, refund_total, net_expected}`

2. **Pull payment gateway settlements**
   - Razorpay: Use MCP `fetch_settlement_recon_details` for the period
   - Stripe: Fetch balance transactions per payout via API
   - Build gateway ledger: `{gateway_payment_id, type, amount, fee, tax, settlement_id, order_ref}`

3. **Ingest marketplace settlement reports** (user uploads CSV/XLSX)
   - Amazon: Parse V2 flat file
   - Flipkart: Parse Orders sheet from settlement report
   - Build marketplace ledger: `{marketplace, order_id, sku, sale_amount, fees_breakdown, tcs, tds, net_settlement}`

4. **Ingest COD remittance reports** (user uploads or API pull)
   - Shiprocket/Delhivery: Parse COD remittance report
   - Build COD ledger: `{awb, order_id, cod_amount, remittance_id, remittance_date, utr, status}`

### Phase 2: Matching Logic

#### Match 1: Shopify Order ↔ Payment Gateway
- **Primary key:** Razorpay `notes.shopify_order_id` or `order_id` → Shopify `order.name` or `order.id`
- **Secondary key:** Razorpay `payment_id` → Shopify `transaction.paymentId`
- **Amount validation:** Shopify `totalPriceSet` == Razorpay `credit` (after converting paise → rupees)
- **Statuses to flag:**
  - Shopify says paid but no matching gateway payment → **Missing payment**
  - Gateway has payment but no Shopify order → **Orphan payment**
  - Amount mismatch > ₹1 → **Amount discrepancy**

#### Match 2: Shopify Refund ↔ Gateway Refund
- **Primary key:** Shopify `refund.transactions[].paymentId` → Razorpay refund `payment_id`
- **Amount validation:** Shopify refund amount == Razorpay `debit` for type=refund
- **Statuses to flag:**
  - Shopify refund issued but no gateway refund → **Refund not processed**
  - Gateway refund but no Shopify refund record → **Unlinked refund**
  - Partial refund amount mismatch → **Refund discrepancy**

#### Match 3: Shopify Order ↔ Marketplace Settlement
- **Primary key:** SKU + approximate date + amount range
- **Secondary key:** Seller Order ID if populated with Shopify order reference
- **Validate:** Sale amount - all fees - TCS - TDS == net settlement amount
- **Statuses to flag:**
  - Order shipped but not in settlement → **Missing settlement**
  - Commission % higher than category slab → **Commission overcharge**
  - TCS not credited or wrong rate → **TCS discrepancy**

#### Match 4: COD Orders ↔ COD Remittance
- **Primary key:** Order ID from Shiprocket/Delhivery → Shopify order name
- **Amount validation:** Shopify COD order total == remitted amount
- **Statuses to flag:**
  - COD order delivered but no remittance → **COD not remitted**
  - Remitted amount < order amount → **COD short payment**
  - Remittance delayed > SLA (48hrs Delhivery, 7 days Shiprocket) → **COD delay**

#### Match 5: Bank Statement ↔ Settlement Batches
- **Primary key:** UTR from gateway/marketplace → bank statement UTR
- **Amount validation:** Settlement batch total == bank credit amount
- **Statuses to flag:**
  - Settlement processed but no bank credit → **Bank credit missing**
  - Bank credit without matching settlement → **Unidentified credit**

### Phase 3: Leakage Detection

Run these rules on the matched data:

| Leakage Pattern | Detection Logic | Typical Impact |
|---|---|---|
| **Commission overcharge** | Compare actual commission % vs category slab rate for Amazon/Flipkart | 0.5-3% of GMV |
| **Weight dispute** | Compare declared weight (Shopify product weight) vs courier-billed weight (Shiprocket/Delhivery invoice). Flag if billed weight > declared + 0.5kg | 1-5% of shipping cost |
| **TCS not credited** | Marketplace deducts TCS (1% Amazon, 0.5% Flipkart) but amount not reflected in seller's GST portal credits | 0.5-1% of marketplace GMV |
| **COD short payment** | Courier remits less than order value. Common with partial deliveries or disputes | 0.5-2% of COD orders |
| **Double fee deduction** | Same fee type applied twice in a settlement period (e.g., two referral fees on one order) | Rare but high-value |
| **Refund not returned to gateway** | Shopify shows refund but gateway didn't process the reversal — merchant absorbs cost | Per-incident |
| **Settlement delay** | Payment gateway holds funds beyond promised T+2/T+3 cycle | Cash flow impact |
| **Phantom returns** | Marketplace credits a return but no physical inventory received back | Per-incident |
| **Incorrect GST on fees** | Gateway charges 18% GST on fees but computation base is wrong | Per-transaction |

---

## Scope

### IN Scope
- Shopify order ↔ payment gateway settlement matching
- Refund reconciliation (Shopify ↔ gateway)
- Marketplace settlement validation (Amazon, Flipkart)
- COD remittance reconciliation (Shiprocket, Delhivery)
- Bank statement ↔ settlement batch matching (UTR-based)
- Commission/fee validation against published rate cards
- Weight dispute detection
- TCS/TDS deduction verification
- Leakage flagging with exact amounts

### OUT of Scope
- GST return filing or GSTR preparation (→ finance-ops skill)
- Vendor payments and vendor ledger maintenance
- Payroll
- TDS return filing (quarterly compliance)
- Inventory valuation
- Inter-company reconciliation
- Cash flow forecasting
- Audit preparation

---

## Available MCP Servers & APIs

| Source | MCP Available? | Setup |
|---|---|---|
| **Shopify** | Yes — `shopify-dev` MCP (docs/schema), plus community `shopify-mcp` for Admin API | `SHOPIFY_STORE_DOMAIN`, `SHOPIFY_ACCESS_TOKEN` |
| **Razorpay** | Yes — Official `razorpay-mcp-server` (35+ tools) | `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`. Remote hosted or local Docker |
| **Stripe** | Yes — Official `@stripe/mcp` | `STRIPE_SECRET_KEY`. Limited settlement tools (use API directly for payouts) |
| **Amazon SP-API** | No MCP — use SP-API directly or CSV upload | SP-API credentials with Reports role |
| **Flipkart** | No MCP — CSV upload from Seller Dashboard | Manual download |
| **Shiprocket** | No MCP — CSV upload or scheduled webhook reports | API key available for order data, COD reports via dashboard |
| **Delhivery** | No MCP — CSV upload | Partner portal access |
| **Bank Statement** | No MCP — CSV/MT940 upload | User provides bank export |

---

## Skill Output Format

The skill does NOT produce a report. It produces **actionable, structured output files.**

### Primary Output: `reconciliation-{date}.json`

```json
{
  "period": { "from": "2026-03-01", "to": "2026-03-14" },
  "summary": {
    "total_orders": 1247,
    "total_matched": 1198,
    "total_mismatched": 34,
    "total_pending": 15,
    "total_leakage_detected": "₹47,320",
    "leakage_by_type": {
      "commission_overcharge": "₹12,400",
      "cod_short_payment": "₹8,750",
      "weight_dispute": "₹15,200",
      "tcs_not_credited": "₹6,970",
      "refund_not_processed": "₹4,000"
    }
  },
  "matched_transactions": [ ... ],
  "mismatches": [
    {
      "type": "amount_discrepancy",
      "shopify_order": "#1042",
      "shopify_amount": 2499.00,
      "gateway_amount": 2399.00,
      "difference": 100.00,
      "source": "razorpay",
      "gateway_ref": "pay_DEXrnipqTmWVGE",
      "action_required": "Verify if ₹100 discount was applied at gateway level"
    }
  ],
  "leakages": [
    {
      "type": "commission_overcharge",
      "marketplace": "amazon",
      "order_id": "402-1234567-8901234",
      "sku": "TSHIRT-BLK-L",
      "expected_commission_pct": 7.0,
      "actual_commission_pct": 10.0,
      "overcharge_amount": 180.00,
      "evidence": "Category 'Apparel' slab = 7%, charged 10%"
    }
  ],
  "pending_items": [
    {
      "type": "cod_not_remitted",
      "order_id": "#1089",
      "amount": 1299.00,
      "courier": "shiprocket",
      "delivered_on": "2026-03-10",
      "days_pending": 4,
      "sla_days": 7
    }
  ]
}
```

### Secondary Output: `unmatched-{date}.csv`

Flat CSV of all unmatched transactions from every source, for manual review:
```
source,reference_id,type,amount,date,shopify_order,match_status,notes
razorpay,pay_ABC123,payment,2499.00,2026-03-12,,no_shopify_match,Orphan payment
shopify,#1105,order,1899.00,2026-03-13,,no_gateway_match,COD order pending remittance
amazon,402-9876543-2109876,settlement,-450.00,2026-03-11,,commission_overcharge,Expected 7% got 12%
```

### Tertiary Output: `leakage-actions-{date}.md`

Human-readable action items with exact amounts and who to contact:
```markdown
## Leakage Actions — March 1-14, 2026

### Raise with Razorpay (₹4,000)
- [ ] Refund for #1042 (₹2,000) not processed — raise ticket with payment ID pay_XYZ
- [ ] Refund for #1067 (₹2,000) not processed — raise ticket with payment ID pay_ABC

### Raise with Amazon Seller Support (₹12,400)
- [ ] 8 orders charged 10% commission instead of 7% (Apparel category) — file rate card dispute

### Raise with Shiprocket (₹8,750)
- [ ] 5 COD orders delivered but not remitted past SLA — escalate AWBs: ...

### Raise with Courier for Weight Disputes (₹15,200)
- [ ] 12 shipments billed at higher volumetric weight — file weight dispute with proof photos
```

---

## Technical Considerations

### Matching Key Strategy

The hardest part of reconciliation is **linking records across systems** since there's no universal order ID.

| Link | How to Match |
|---|---|
| Shopify ↔ Razorpay | Razorpay `notes` field typically contains Shopify order ID. Fallback: match on amount + timestamp window (±2 hours) |
| Shopify ↔ Stripe | Stripe `payment_intent.metadata` contains Shopify references. Shopify `transaction.paymentId` = Stripe charge ID |
| Shopify ↔ Amazon | SKU matching + date + amount. No direct order ID link unless custom integration exists |
| Shopify ↔ Flipkart | SKU matching + date + amount. Same limitation as Amazon |
| Shopify ↔ COD Courier | Shiprocket order ID usually matches Shopify order name. AWB cross-reference |
| Settlement ↔ Bank | UTR (Unique Transaction Reference) from settlement report → bank statement NEFT/RTGS reference |

### Currency & Unit Handling
- Razorpay amounts are in **paise** (1 INR = 100 paise) — divide by 100
- Stripe amounts are in **smallest currency unit** (same as paise for INR)
- Shopify amounts are in **decimal currency** (already in rupees)
- Amazon/Flipkart amounts are in **decimal currency**
- Always reconcile in the same unit — convert everything to decimal INR

### Tolerance Rules
- Amount match tolerance: ₹1 (rounding differences)
- Date match window: ±3 days (settlement cycles vary)
- Weight dispute threshold: > 0.5 kg difference between declared and billed

### Volume Expectations
- 15,000+ transactions/month for ₹50-200Cr revenue brands
- Reconciliation should process in batch, not real-time
- Typical run: daily or weekly, covering the period since last run

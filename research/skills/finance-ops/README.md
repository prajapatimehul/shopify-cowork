# Finance-Ops Skill

## Employee Role Replaced

**Finance Manager** (₹15-30 LPA, 55-65% automatable)

### What the Finance Manager Does Daily

| Task | Frequency | Automatable? |
|------|-----------|-------------|
| Daily revenue/refund/net collection review | Daily | Yes — pull from Shopify + marketplaces |
| COD float tracking — money stuck with couriers (7-15 day lag) | Daily | Yes — track via courier APIs/reports |
| Channel-wise P&L — website vs Amazon vs Flipkart margins after all fees | Weekly | Yes — compute from order + fee data |
| GST computation — GSTR-1, GSTR-3B, ITC reconciliation with GSTR-2B | Monthly | Partially — compute worksheets, CA files |
| TDS compliance — deduct/remit on rent, professional fees, contractors | Monthly | Partially — compute liability, CA remits |
| Cash flow management — working capital, vendor payment scheduling | Weekly | Yes — model from data |
| MIS reporting — contribution margin by SKU, unit economics, monthly P&L | Monthly | Yes — compute from order + COGS data |
| Commission audit — verify marketplace/PG rates against contracts | Monthly | Yes — compare actual vs contracted rates |
| Vendor payment processing — match invoices to GRN, schedule payments | Weekly | Partially — flag mismatches |

### What This Skill Replaces vs What Still Needs a Human

**Skill does:**
- Generates P&L workpapers (channel-wise, SKU-wise, monthly)
- Computes GST worksheets (GSTR-1 data, IGST vs CGST+SGST split, ITC matching)
- Tracks COD float and settlement aging
- Calculates unit economics (CM1/CM2/CM3) by SKU
- Audits commission rates against contracted rates
- Produces cash flow forecasts from order/settlement data
- Generates MIS reports with contribution margins

**Human (CA/Finance Manager) still does:**
- File GST returns on portal (GSTR-1, GSTR-3B)
- Make TDS remittances
- Sign off on financial statements
- Handle audit queries
- Vendor negotiations
- Bank reconciliation sign-off

---

## Data Sources Required

### 1. Shopify Admin API (Primary — Website Channel)

**Orders + Financial Data** (GraphQL Admin API):
- `orders` query — `totalPrice`, `subtotalPrice`, `totalTax`, `totalShippingPrice`, `totalDiscounts`, `totalRefunded`, `financialStatus`, `paymentGatewayNames`
- `order.taxLines` — tax amount, rate, title per line item (but Shopify does NOT split IGST vs CGST+SGST — see GST section)
- `order.shippingLines` — shipping charges, carrier, discounted price
- `order.transactions` — payment gateway, amount, fees, status, kind (sale/refund/void)
- `order.refunds` — refund line items, amounts, restocking fees

**Shopify Payments Data** (if using Shopify Payments):
- `ShopifyPaymentsPayout` — net amount, status (scheduled/in_transit/paid), issuedAt, transactionType
- `ShopifyPaymentsBalanceTransaction` — gross amount, fee, net, type, sourceType (charges/refunds/payouts/adjustments), transactionDate, associatedOrder
- `ShopifyPaymentsPayoutSummary` — fee/gross breakdowns by transaction type

**ShopifyQL Analytics** (via `shopifyqlQuery`):
- `FROM sales SHOW total_sales, orders, net_sales SINCE {date} GROUP BY day` — daily revenue
- Supports: `gross_sales`, `net_sales`, `orders`, `units_sold`, `taxes`, `shipping`, `discounts`, `returns`
- Required scope: `read_reports`

**Product Cost Data** (via metafields):
- `product.metafield(namespace: "cost", key: "per_item")` — COGS per unit (must be stored by merchant)
- `productVariant.inventoryItem.unitCost` — cost per unit if set in Shopify

### 2. Marketplace Data (Amazon/Flipkart — Manual Upload or API)

Amazon and Flipkart do NOT offer open APIs for sellers to pull fee/commission data programmatically. Data comes from **downloaded reports**:

**Amazon Seller Central Reports:**
- Settlement Reports — order-level: selling price, referral fee (5-25% by category), closing fee (₹9-30/order), shipping fee, TCS (1%)
- Payment Reports — UTR-wise settlement amounts
- Returns Reports — return shipping deductions

**Flipkart Seller Hub Reports:**
- Commission Reports — commission fee (4-22% by category), fixed fee (₹5-50/order), shipping fee, collection fee
- Settlement Reports — cycle-wise payout amounts
- Returns Reports — reverse logistics charges

**What the skill needs from these:** CSV/Excel uploads parsed into structured data — per-order fees, commissions, deductions.

### 3. Payment Gateway Data (Razorpay/Cashfree/PayU)

**Razorpay** (most common for Shopify India):
- Settlement cycle: T+2 business days for domestic
- Fee: 2% of transaction value + 18% GST on fee
- UPI: Zero MDR but 2% platform fee
- Data available: payment ID, order ID, amount, fee, tax on fee, settlement ID, UTR
- Dashboard exports or API: `/payments`, `/settlements`, `/settlements/:id/reports`

**What the skill needs:** Settlement reports (CSV) or API pulls — per-transaction: gross, fee, GST on fee, net settled.

### 4. Ad Spend Data (for ROAS / Unit Economics)

**Google Ads API:**
- `metrics.cost_micros` — spend in micros (divide by 1,000,000)
- Campaign and ad group level cost data
- Required for: ROAS = Revenue / Ad Spend

**Meta Ads API:**
- Spend, impressions, clicks by campaign
- Can import into GA4 natively for unified view

**What the skill needs:** Daily/weekly ad spend by channel (Google, Meta, others) — can be manual CSV or API.

### 5. Courier / Logistics Data (for COD Float)

**COD float = cash collected by courier but not yet remitted to seller.**

- Delhivery, Shadowfax, Shiprocket, etc. — settlement cycle 7-15 days
- Data needed: AWB-wise COD amount, delivery date, remittance date, UTR
- Source: Courier dashboard exports or aggregator (Shiprocket) API

### 6. Accounting Software (Output Destination)

**Tally Prime:**
- GET/POST REST API via api2books.com or direct TallyPrime XML import
- Push: sales vouchers, credit notes, journal entries (GST), payment vouchers
- Pull: ledger balances, outstanding payables

**Zoho Books:**
- Full REST API (`/api/v3/`) — invoices, credit notes, bills, journal entries
- Shopify integration available via Zoho Commerce or third-party connectors
- Push: auto-create invoices from Shopify orders, GST-compliant

**QuickBooks:**
- REST API — invoices, expenses, journal entries, reports
- Less common in India for SMBs but used by some D2C brands

---

## What the Skill Should Do

### 1. Channel-Wise P&L Generation

Produce a monthly P&L broken down by channel:

```
Channel: Shopify Website
─────────────────────────────────
Gross Revenue                    ₹45,00,000
(-) Returns & Refunds            ₹3,15,000
(-) Discounts                    ₹2,25,000
= Net Revenue                   ₹39,60,000

(-) COGS                        ₹15,84,000  (40% of net)
= Gross Margin (CM1)            ₹23,76,000  (60%)

(-) Shipping Cost                ₹2,77,200
(-) Payment Gateway Fees         ₹79,200   (2% of net)
(-) Packaging                    ₹1,98,000
(-) Return Processing            ₹47,250
= Contribution Margin 2 (CM2)   ₹17,74,350  (44.8%)

(-) Google Ads                   ₹4,00,000
(-) Meta Ads                     ₹3,50,000
(-) Influencer/Other             ₹1,00,000
= Contribution Margin 3 (CM3)   ₹9,24,350   (23.3%)
```

Repeat for Amazon, Flipkart. Then consolidated view.

**Key difference from reconciliation skill:** Reconciliation matches transactions 1:1. Finance-ops aggregates them into P&L statements.

### 2. GST Computation Worksheets

**Why this is hard for Shopify India sellers:**
- Shopify applies a single combined tax rate — it does NOT determine whether a sale is intra-state (CGST+SGST) or inter-state (IGST)
- The skill must determine place of supply from the shipping address state vs. the seller's GSTIN-registered state
- HSN codes must be mapped to products (4-digit mandatory for turnover ≤₹5Cr, 6-digit for >₹5Cr)

**What the skill generates:**

**GSTR-1 Worksheet:**
- B2B invoices (with GSTIN) — invoice-wise with tax split
- B2C Large (inter-state > ₹2.5L) — state-wise summary
- B2C Small (all other) — rate-wise summary
- Credit Notes — linked to original invoice
- HSN Summary — HSN-wise taxable value and tax

**GSTR-3B Worksheet:**
- Table 3.1: Outward supplies — taxable value, IGST, CGST, SGST, cess
- Table 4: ITC available — from GSTR-2B auto-populated data
- Table 5: Exempt/nil-rated/non-GST supplies

**Tax Split Logic:**
```
IF shipping_address.state == seller_gstin_state:
    CGST = tax_amount / 2
    SGST = tax_amount / 2
    IGST = 0
ELSE:
    CGST = 0
    SGST = 0
    IGST = tax_amount
```

**TCS Tracking:**
- Amazon/Flipkart deduct 1% TCS under Section 52 CGST Act
- Track TCS deducted per marketplace, claimable via electronic cash ledger
- Generate TCS reconciliation: expected (1% of taxable value) vs actual deducted

### 3. Cash Flow Tracking

**COD Float Dashboard:**
```
Courier Partner    | COD Collected | Pending Remittance | Avg Days | Overdue (>15d)
Delhivery          | ₹12,50,000   | ₹4,80,000          | 9 days   | ₹85,000
Shiprocket/Xpressbees | ₹8,20,000 | ₹3,10,000          | 11 days  | ₹1,20,000
BlueDart           | ₹5,40,000    | ₹1,60,000          | 7 days   | ₹0
```

**Settlement Aging:**
- Razorpay: T+2 — flag if settlement >T+4
- Amazon: 7-14 day cycle — flag overdue
- Flipkart: 7-15 day cycle — flag overdue

**Working Capital View:**
```
Cash Available Today                     ₹18,50,000
(+) Expected Settlements (next 7 days)   ₹12,40,000
(+) COD Remittance Expected              ₹6,80,000
(-) Vendor Payments Due                  ₹15,20,000
(-) GST Liability (next filing)          ₹4,50,000
(-) Ad Spend Committed                   ₹7,50,000
= Projected Cash Position                ₹10,50,000
```

### 4. Unit Economics by SKU

**CM1/CM2/CM3 Framework:**

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| CM1 (Product Margin) | Net Revenue - COGS | 50-65% for D2C |
| CM2 (Operational Margin) | CM1 - Shipping - PG Fees - Packaging - Returns | 30-45% for D2C |
| CM3 (After Marketing) | CM2 - Ad Spend (attributed) | 15-25% for D2C |

**Per-SKU Output:**
```
SKU: TSHIRT-BLK-M
  ASP (Avg Selling Price)     ₹1,299
  (-) Avg Discount            ₹130    (10%)
  = Net Price                 ₹1,169
  (-) COGS                    ₹350    (30%)
  = CM1                       ₹819    (70%)
  (-) Shipping                ₹75
  (-) PG Fee (2%)             ₹23
  (-) Packaging               ₹25
  (-) Return Rate (15%) Cost  ₹35
  = CM2                       ₹661    (56.5%)
  (-) CAC (attributed)        ₹200
  = CM3                       ₹461    (39.4%)
```

**Data requirements:**
- COGS per SKU — from product metafields or uploaded cost sheet
- Shipping cost — from order shipping lines or courier rate cards
- PG fees — from Razorpay/Cashfree settlement reports
- Return rate — from Shopify refund data
- CAC attribution — from ad spend / orders acquired

### 5. Commission Audit

**What it checks:**
- Compare actual marketplace fees charged per order vs contracted rate card
- Flag orders where commission % deviates >0.5% from expected
- Track fee category changes (Amazon/Flipkart revise rates quarterly)

**Output:**
```
Amazon Commission Audit — March 2026
Category: Clothing & Accessories
Contracted Rate: 17%
──────────────────────────────
Total Orders Audited:     1,247
Within Tolerance:         1,198 (96%)
Over-charged:                49 (3.9%)
  Avg Overcharge:          ₹12.40/order
  Total Overcharge:        ₹607.60
Under-charged:                0
```

### 6. MIS Report Generation

**Monthly MIS Package** (Excel workbook with tabs):
1. **Revenue Summary** — daily/weekly/monthly, channel-wise
2. **P&L Statement** — channel-wise CM1/CM2/CM3
3. **GST Summary** — IGST/CGST/SGST split, HSN summary
4. **Cash Flow** — settlements received, COD pending, working capital
5. **Unit Economics** — top 20 SKUs by CM3, bottom 20 by CM3
6. **ROAS Dashboard** — ad spend vs revenue by channel, blended ROAS
7. **Accounts Payable Aging** — vendor payments due by date

---

## India-Specific Finance Requirements

### GST Compliance

| Requirement | Detail |
|-------------|--------|
| Tax Split | IGST for inter-state, CGST+SGST for intra-state — determined by shipping address vs GSTIN state |
| HSN Codes | 4-digit mandatory (≤₹5Cr turnover), 6-digit (>₹5Cr), must be portal-validated since Jan 2025 |
| GSTR-1 | Monthly by 11th or quarterly by 13th — outward supply details |
| GSTR-3B | Monthly/quarterly — tax liability summary, auto-populated from GSTR-1 since 2025 |
| GSTR-9 | Annual return by Dec 31; GSTR-9C required if turnover >₹5Cr |
| E-invoicing | Mandatory for B2B if turnover >₹5Cr; threshold dropping to ₹2Cr |
| Invoice Requirements | 16 mandatory fields under Rule 46: supplier details, HSN, tax split, place of supply, IRN/QR |

### TCS (Tax Collected at Source)

- Amazon, Flipkart, Meesho deduct **1% TCS** under Section 52 CGST Act
- Claimable through electronic cash ledger in GST portal
- Skill must track: TCS deducted per marketplace per month, match against GSTR-2B

### TDS (Tax Deducted at Source)

- **Section 194O**: E-commerce operators deduct 0.1% TDS (reduced from 1% since Oct 2024) on gross sales >₹5L/year
- **Section 194C**: TDS on contractor/logistics payments — 1% (individual) or 2% (company)
- **Section 194J**: TDS on professional fees (CA, legal) — 10%
- Skill computes: TDS liability by section, due dates, Form 26Q data

### Multi-State Compliance

- Brands with warehouses in multiple states need separate GST registrations per state
- Each state registration files its own GSTR-1 and GSTR-3B
- Stock transfers between own warehouses = taxable supply (delivery challan, IGST applicable)
- Skill must segregate data by GSTIN for multi-state filers

---

## Scope Boundaries

### IN SCOPE

- Channel-wise P&L generation (Shopify + marketplaces)
- GST computation worksheets (GSTR-1, GSTR-3B data, tax split)
- TCS tracking and reconciliation
- TDS liability computation
- COD float tracking and settlement aging
- Unit economics / contribution margin by SKU (CM1/CM2/CM3)
- Commission rate audit (marketplace fees vs contracted rates)
- Cash flow tracking and working capital projection
- MIS report generation (Excel/CSV workpapers)
- ROAS calculation from ad spend data
- Vendor payment aging (payables tracking)

### OUT OF SCOPE

- **Transaction-level reconciliation** — that's the reconciliation skill (matching bank statement line items to orders)
- **Payroll processing** — salary computation, PF/ESI, payslips
- **Tax filing** — actually filing GSTR-1/3B/9 on the GST portal (needs CA + DSC)
- **TDS remittance** — actual challan payment and Form 26Q filing
- **Audit preparation** — responding to GST/Income Tax audit notices
- **Vendor negotiations** — negotiating better rates with suppliers
- **Bank reconciliation** — matching bank statement entries (reconciliation skill)
- **Inventory valuation** — weighted average / FIFO costing (procurement-ops skill)
- **Budgeting & forecasting** — annual budget preparation, board decks

---

## APIs and MCPs Available

### Shopify MCP (Available in Plugin)

The `shopify-dev` MCP provides:
- `learn_shopify_api` — load API context for Admin, Storefront, etc.
- `introspect_graphql_schema` — explore Order, Transaction, Payout, TaxLine objects
- `search_docs_chunks` — search Shopify documentation
- `fetch_full_docs` — retrieve complete API docs
- `validate_graphql_codeblocks` — validate generated GraphQL queries

**Key GraphQL Queries for Finance-Ops:**
```graphql
# Orders with financial data
query {
  orders(first: 50, query: "created_at:>2026-03-01") {
    edges {
      node {
        name
        totalPriceSet { shopMoney { amount } }
        subtotalPriceSet { shopMoney { amount } }
        totalTaxSet { shopMoney { amount } }
        totalShippingPriceSet { shopMoney { amount } }
        totalDiscountsSet { shopMoney { amount } }
        totalRefundedSet { shopMoney { amount } }
        financialStatus
        paymentGatewayNames
        taxLines(first: 5) { rate title priceSet { shopMoney { amount } } }
        shippingAddress { provinceCode countryCode }
      }
    }
  }
}

# Shopify Payments Balance Transactions
query {
  shopifyPaymentsAccount {
    balanceTransactions(first: 50) {
      edges {
        node {
          amount { amount }
          fee { amount }
          net { amount }
          type
          transactionDate
          associatedOrder { name }
        }
      }
    }
  }
}

# ShopifyQL for daily revenue
query {
  shopifyqlQuery(query: "FROM sales SHOW net_sales, orders, taxes, shipping, discounts SINCE -30d GROUP BY day ORDER BY day") {
    tableData { columns { name } rows }
  }
}
```

### External APIs (Require Separate Integration)

| Service | API | What It Provides |
|---------|-----|-----------------|
| Razorpay | REST API `/payments`, `/settlements` | Transaction fees, settlement amounts, UTR |
| Google Ads | Google Ads API v17+ `metrics.cost_micros` | Campaign spend for ROAS |
| Meta Ads | Marketing API | Campaign spend, impressions, ROAS |
| Tally Prime | REST GET/POST via api2books.com | Push vouchers, pull ledger balances |
| Zoho Books | REST API v3 `/invoices`, `/creditnotes` | Push invoices, pull reports |
| Shiprocket | REST API | COD remittance status, AWB tracking |

---

## Output Format

**All outputs must be actionable workpapers, NOT narrative summaries.**

### Primary Output: Excel/CSV Workbooks

| Workpaper | Format | Contents |
|-----------|--------|----------|
| Monthly P&L | Excel (multi-tab) | Channel-wise P&L with CM1/CM2/CM3, consolidated view |
| GST Worksheet | Excel | GSTR-1 data (B2B, B2C, Credit Notes, HSN Summary), GSTR-3B data (Table 3.1, 4, 5) |
| COD Float Tracker | CSV | Courier-wise: collected, pending, aging, overdue |
| Unit Economics | Excel | SKU-wise CM1/CM2/CM3, top/bottom performers |
| Commission Audit | CSV | Order-wise: expected rate, actual charged, variance, flagged |
| Cash Flow | Excel | Daily/weekly: inflows (settlements, COD), outflows (vendors, GST, ads), projected balance |
| TCS Reconciliation | CSV | Marketplace-wise: expected TCS, actual deducted, variance |
| TDS Computation | Excel | Section-wise liability, payee details, due dates |
| MIS Package | Excel (7+ tabs) | All above consolidated into single workbook |

### Secondary Output: Summary for Stakeholders

- One-paragraph executive summary with key numbers
- Alerts: overdue COD, commission overcharges, cash crunch warning, GST filing deadline
- Comparison: this month vs last month, vs same month last year

### What NOT to Output

- Long narrative explanations of what GST is
- Generic advice ("you should optimize your margins")
- Dashboard screenshots or charts (text/CSV only)
- Unstructured bullet points without numbers

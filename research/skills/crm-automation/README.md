# CRM Automation Skill

## Employee Role Replaced

**Retention / CRM Manager** — 50-60% automatable, ₹8-18 LPA, typically 1 person per D2C company (₹50-200Cr revenue, India).

### What they do daily

| Task | Time share | Automatable? |
|---|---|---|
| Build & schedule email campaigns (segment, write copy, A/B test) | 20% | Yes — segment + schedule via Klaviyo API; copy stays with catalog-writer skill |
| WhatsApp campaign management (broadcasts for sales, restocks, loyalty) | 15% | Yes — template messages via Interakt/Wati API |
| Optimize automation flows (abandoned cart, welcome, post-purchase, win-back, review request, birthday) | 20% | Yes — create/update flows in Klaviyo via API |
| Customer segmentation (RFM, churn detection, high-value ID) | 15% | Yes — compute from Shopify order data, push tags back |
| Loyalty program management (points, exclusive offers) | 10% | Partial — needs dedicated loyalty app (Yotpo, Smile.io); out of scope |
| Retention metrics reporting (repeat rate, LTV, email/WhatsApp revenue, churn rate) | 10% | Yes — pull from Klaviyo + Shopify APIs |
| Ad-hoc CRM tasks | 10% | No |

---

## Data Sources Required

### 1. Shopify Admin API (GraphQL) — Primary

All customer and order data lives here. REST Admin API is legacy since Oct 2024; new apps must use GraphQL from Apr 2025.

| Data | API | Notes |
|---|---|---|
| Customer profiles | `customers` query | Name, email, phone, tags, addresses, metafields |
| Order history | `orders` query | Line items, totals, dates, fulfillment, discounts |
| Customer segments | `segments` / `customerSegmentMembers` queries | ShopifyQL-based segments; max 1000 per page, 250 segments |
| Customer metafields | Customer object → `metafields` | Store RFM scores, churn risk, LTV — custom definitions |
| Customer tags | `tagsAdd` / `tagsRemove` mutations | Tag customers with segments (e.g., `rfm:champion`, `churn:at-risk`) |
| Customer segment membership | `customerSegmentMembership` query | Check if a customer is in a segment |

**Key mutations for this skill:**
- `tagsAdd` — tag customers with RFM/churn labels
- `customerUpdate` — update metafields with computed scores
- `segmentCreate` — create segments from ShopifyQL queries

### 2. Klaviyo API (v3) — Email & SMS Automation

Klaviyo is the dominant email/SMS platform for Shopify D2C. It has a dedicated MCP server (GA since Aug 2025).

| Capability | API | Notes |
|---|---|---|
| Create flows | Flows API — `POST /api/flows/` | Abandoned cart, welcome, win-back — created in Draft status |
| Update flow status | Flows API — `PATCH /api/flows/{id}/` | Move Draft → Manual → Live |
| Create segments | Segments API — `POST /api/segments/` | 7 condition types (metric, property, predictive, consent, location, region, list membership) |
| Manage profiles | Profiles API | Create, update, subscribe/unsubscribe |
| Track events | Events API | Custom events for triggering flows |
| Campaign creation | Campaigns API | Schedule email/SMS campaigns |
| Templates | Templates API | Create/manage email templates |
| Reporting | Reporting API | Campaign & flow performance metrics |

**Limits:** Max 5 segments processed simultaneously, 100 segments created/day.

**Klaviyo MCP Server** — Available as an official MCP integration. Tools exposed: campaigns, flows, profiles, events, segments/lists, templates, catalogs, reporting. Can be configured in Claude via Settings > Connectors or custom connector at `https://mcp.klaviyo.com/mcp` with OAuth.

### 3. WhatsApp Business API — via BSPs

WhatsApp has 98% open rates vs 20% for email. Critical channel for Indian D2C.

| Provider | Strengths | Shopify Integration |
|---|---|---|
| **Interakt** | Best for SMBs, native Shopify app, no-code setup | Direct — abandoned cart, order updates, broadcasts from Shopify data |
| **Wati** | Strong chatbot builder, shared inbox | Via API |
| **Gupshup** | Enterprise scale, rich media, CRM integration | Via API |

**Key capabilities via API:**
- Send broadcast template messages (pre-approved by Meta) to opted-in users
- Automated triggers: cart abandonment, order confirmation, delivery updates, restock alerts
- Segmented campaigns using Shopify customer data
- Up to 100,000 contacts/day
- Per-message pricing (since Jul 2025, replacing conversation-based billing)

### 4. WebEngage / MoEngage (Alternative Platforms)

Popular with Indian D2C brands. Both have Shopify apps.

- **WebEngage**: Full retention stack — CDP, segmentation, omnichannel campaigns (email, SMS, WhatsApp, push). Claims 20% cart recovery, 12% lift in 60-day repeat purchase.
- **MoEngage**: AI-driven engagement (Sherpa), strong mobile push. Plans from ~$750-999/mo. Shopify app syncs customer + purchase data.

Both are alternatives to Klaviyo for brands already using them. Skill should support Klaviyo as primary, with notes on WebEngage/MoEngage as alternatives.

---

## What the Skill Should Do

### Core Actions (Not Reports — Actual Execution)

#### 1. Customer Segmentation from Shopify Data

**Input:** Shopify orders + customers via GraphQL API
**Process:**
- Pull all orders for the store (paginated)
- For each customer, compute: last order date, total orders, total spend
- Run RFM scoring (see methodology below)
- Identify churn-risk customers (no purchase in >1.5× average purchase interval)
- Identify high-value customers (top 20% by LTV)

**Output:**
- Tag customers in Shopify: `rfm:champion`, `rfm:loyal`, `rfm:at-risk`, `rfm:hibernating`, `rfm:lost`
- Write RFM scores to customer metafields
- Create/update Shopify customer segments via ShopifyQL
- Sync segments to Klaviyo profiles

#### 2. Automation Flow Creation in Klaviyo

**Build these flows via Klaviyo API:**

| Flow | Trigger | Timing | Steps |
|---|---|---|---|
| **Abandoned Cart** | `Checkout Started` but no `Placed Order` | 1h → 24h → 72h | 3 emails: reminder → social proof → urgency/discount |
| **Welcome Series** | `Subscribed to List` | Immediate → Day 2 → Day 4 | 3 emails: brand story → bestsellers/social proof → first-purchase incentive |
| **Post-Purchase Upsell** | `Placed Order` | Day 2 → Day 5 | 2 emails: complementary products → care tips + review ask |
| **Review Request** | `Fulfilled Order` | Day 7 post-delivery | 1 email: product review request (satisfaction peaks at Day 7) |
| **Win-Back** | No purchase in 60 days | Day 60 → Day 75 → Day 90 | 3 emails: "we miss you" → exclusive offer → last chance |
| **Birthday** | `birthday` profile property | Birthday -3 days | 1 email: birthday discount |
| **Replenishment** | `Placed Order` for consumables | Based on avg reorder cycle | 1 email: "time to restock?" |

**Output:** Flows created in Draft status in Klaviyo. Skill reports flow IDs and asks user to review before going Live.

#### 3. WhatsApp Campaign Triggers

**Via Interakt/Wati/Gupshup API:**

| Campaign | Trigger | Template |
|---|---|---|
| Cart Recovery | Checkout abandoned >1h | "Hi {name}, you left {product} in your cart. Complete your order: {link}" |
| Order Confirmation | Order placed | "Order #{number} confirmed! Track: {link}" |
| Restock Alert | Product back in stock | "{product} is back! Shop now: {link}" |
| Sale Broadcast | Manual trigger (scheduled) | "🎉 {sale_name} is live! Up to {discount}% off: {link}" |
| Win-Back | No purchase in 60 days | "Hi {name}, we miss you! Here's {discount}% off your next order: {link}" |

**Output:** Template messages queued for sending via BSP API. Requires pre-approved Meta templates.

#### 4. Retention Metrics Dashboard Data

**Compute and output:**
- **Repeat Purchase Rate**: (Customers with >1 order) / (Total customers) — from Shopify orders
- **Customer LTV**: AOV × Purchase Frequency × Avg Customer Lifespan
- **Churn Rate**: Customers inactive >90 days / Total active customers
- **Email Revenue Attribution**: From Klaviyo reporting API
- **WhatsApp Campaign Performance**: Open rates, click rates from BSP API
- **RFM Distribution**: % of customers in each segment
- **Flow Performance**: Conversion rates per flow from Klaviyo

**Output:** Structured data (not a PDF report) that can be pushed to a dashboard or returned as actionable metrics.

---

## RFM Segmentation Methodology

### Scoring (1-5 scale for each dimension)

**Recency (R):** Days since last purchase
| Score | Criteria |
|---|---|
| 5 | Purchased in last 7 days |
| 4 | 8-30 days ago |
| 3 | 31-60 days ago |
| 2 | 61-120 days ago |
| 1 | >120 days ago |

**Frequency (F):** Total orders in last 12 months
| Score | Criteria |
|---|---|
| 5 | 10+ orders |
| 4 | 6-9 orders |
| 3 | 3-5 orders |
| 2 | 2 orders |
| 1 | 1 order |

**Monetary (M):** Total spend in last 12 months
| Score | Criteria |
|---|---|
| 5 | Top 10% spenders |
| 4 | 10-25th percentile |
| 3 | 25-50th percentile |
| 2 | 50-75th percentile |
| 1 | Bottom 25% |

*Note: M thresholds should be computed dynamically per store based on actual spend distribution.*

### Segment Mapping

| Segment | RFM Range | Action |
|---|---|---|
| **Champions** | R:5, F:4-5, M:4-5 | Reward, ask for reviews, early access to new products |
| **Loyal Customers** | R:3-4, F:3-5, M:3-5 | Upsell, loyalty program, referral program |
| **Potential Loyalists** | R:4-5, F:1-2, M:1-3 | Nurture — welcome series, education, second purchase incentive |
| **At-Risk** | R:2-3, F:3-5, M:3-5 | Win-back campaign, personal outreach, exclusive discount |
| **Hibernating** | R:1-2, F:1-2, M:1-2 | Deep discount win-back or let go |
| **Lost** | R:1, F:1, M:1 | Final win-back attempt, then suppress from paid campaigns |

### Churn Detection

- **Purchase cycle:** Compute average days between orders per customer
- **Churn threshold:** 1.5× average purchase cycle with no order = at-risk; 2× = churned
- **Predictive signals:** Declining order frequency, decreasing AOV, reduced email engagement
- **Intervention window:** 30-60 days before predicted churn — this is when win-back flows fire
- **Effectiveness:** 25-40% of at-risk customers can be saved with timely intervention

---

## Scope

### IN Scope

- RFM segmentation from Shopify order data
- Customer tagging in Shopify (via `tagsAdd` mutation + metafields)
- Shopify customer segment creation (via `segmentCreate` mutation)
- Klaviyo flow creation (abandoned cart, welcome, post-purchase, win-back, review, birthday, replenishment)
- Klaviyo segment creation (synced with Shopify RFM segments)
- WhatsApp broadcast campaign triggering (via Interakt/Wati/Gupshup API)
- Churn detection and at-risk customer identification
- Retention metrics computation (repeat rate, LTV, churn rate)
- Campaign performance tracking (Klaviyo reporting API)
- Customer lifecycle stage assignment
- A/B test setup for email flows (subject lines, send times)

### OUT of Scope

- **Social media management** — separate skill
- **Ad targeting / lookalike audiences** — ads skill
- **Loyalty program creation** — requires dedicated app (Yotpo, Smile.io, Flits)
- **Email/WhatsApp copy creation** — catalog-writer skill handles creative copy
- **Product recommendations engine** — separate ML system
- **Customer support / ticket management** — customer-service skill
- **Inventory/restock decisions** — procurement-ops skill

---

## APIs & MCPs Available

| System | Access Method | Auth |
|---|---|---|
| Shopify Admin API (GraphQL) | `shopify-dev` MCP tools (`introspect_graphql_schema`, `learn_shopify_api`) | Store access token |
| Klaviyo | Official Klaviyo MCP server (`https://mcp.klaviyo.com/mcp`) | OAuth / API key |
| Interakt (WhatsApp) | REST API | API key |
| Wati (WhatsApp) | REST API | API key |
| Gupshup (WhatsApp) | REST API | API key |
| WebEngage | REST API (alternative to Klaviyo) | API key |
| MoEngage | REST API + Shopify app (alternative to Klaviyo) | API key |

### Shopify MCP Tools (already available in this plugin)

- `introspect_graphql_schema` — explore Customer, Order, Segment objects
- `learn_shopify_api` — understand customer/order/segment APIs
- `validate_graphql_codeblocks` — validate mutations before execution
- `search_docs_chunks` — search Shopify docs for segmentation, metafields, tags

---

## Output: What Gets Created

This skill produces **executable artifacts**, not strategy documents:

1. **Shopify customer tags** — RFM segment labels applied to every customer (`rfm:champion`, `rfm:at-risk`, etc.)
2. **Shopify customer metafields** — RFM scores (R, F, M values), LTV, churn risk score
3. **Shopify customer segments** — Dynamic segments via ShopifyQL matching RFM groups
4. **Klaviyo flows** — 7 automation flows created in Draft status, ready for review
5. **Klaviyo segments** — Synced audience segments for flow targeting
6. **WhatsApp campaigns** — Template messages queued via BSP API for cart recovery, win-back, broadcasts
7. **Retention metrics** — Computed data: repeat purchase rate, LTV, churn rate, RFM distribution
8. **Flow performance data** — Conversion rates, revenue attribution per flow from Klaviyo reporting API

### What the skill does NOT output

- Strategy documents or "recommendations"
- Slide decks or PDFs
- Email copy (that's catalog-writer)
- Loyalty program designs

---

## Key Automation Flow Details

### Abandoned Cart Flow (Highest ROI)

**Stats:** Abandoned cart + welcome emails = 76% of all automation-generated orders. Well-optimized flows recover up to 30% of lost sales. Average conversion rate: 18%.

**3-Step Sequence:**
1. **Email 1 (1 hour):** Simple reminder with cart contents, product image, CTA
2. **Email 2 (24 hours):** Social proof — reviews, bestseller badges, "X people bought this today"
3. **Email 3 (72 hours):** Urgency + incentive — limited stock warning or small discount (5-10%)

**WhatsApp parallel:** Send cart recovery WhatsApp at 1 hour (98% open rate vs 20% email open rate). If WhatsApp converts, suppress email follow-ups.

### Welcome Series

**Stats:** Average welcome flow generates $2.65/recipient. Top 10% achieve 10.53% placed order rate.

**3-Step Sequence:**
1. **Email 1 (Immediate):** Brand story, founder note, what to expect
2. **Email 2 (Day 2):** Bestsellers, social proof, UGC
3. **Email 3 (Day 4):** First-purchase incentive (discount code with expiry)

### Win-Back Flow

**Trigger:** No purchase in 60 days (configurable based on store's avg purchase cycle)

**3-Step Sequence:**
1. **Email 1 (Day 60):** "We miss you" — new arrivals, what's changed
2. **Email 2 (Day 75):** Exclusive returning-customer discount (10-15%)
3. **Email 3 (Day 90):** Final attempt — bigger incentive or "is this goodbye?"

After Day 90 with no engagement: move to `rfm:lost`, suppress from paid campaigns to save ad spend.

---

## Social Media Data That Helps (From Other Skills)

- **Instagram follower overlap** — identify customers who are also social followers (brand advocates)
- **UGC/engagement metrics** — customers who tag the brand in posts are candidates for ambassador/referral programs
- **Social listening for churn signals** — negative mentions may indicate at-risk customers

*Note:* Instagram API access is limited. Social data is supplementary, not primary for this skill.

---

## Implementation Priority

1. **RFM segmentation + Shopify tagging** — foundation for everything else; no external API needed beyond Shopify
2. **Abandoned cart flow in Klaviyo** — highest ROI, recovers immediate revenue
3. **Welcome series in Klaviyo** — captures new subscribers at peak intent
4. **WhatsApp cart recovery via Interakt** — parallel channel with 98% open rate
5. **Win-back flow** — re-engage lapsed customers
6. **Post-purchase + review request flows** — increase LTV and social proof
7. **Retention metrics computation** — close the loop with measurement
8. **Birthday + replenishment flows** — incremental revenue

# GEO Checks — AI Visibility and Citation-Worthiness

## Contents

1. AI bot crawl access
2. llms.txt
3. Entity clarity and brand signals
4. Citation-worthiness signals
5. Content extractability
6. Content freshness

---

## Context

GEO (Generative Engine Optimization) is about making a store visible and citable by AI search engines — ChatGPT, Perplexity, Google AI Overviews, Gemini, Claude.

Key stats:
- AI-driven traffic to Shopify sites grew 8x YoY in 2025.
- AI-referred purchases carry 30% higher AOV than traditional search.
- 60% of Google searches end without a click (zero-click).
- Brand search volume is the strongest predictor of AI citations (r=0.334).
- Web mentions correlate 3x more with AI visibility than backlinks.

---

## 1. AI Bot Crawl Access

### 1.1 Robots.txt AI Bot Rules

**Critical finding:** Shopify updated all stores' default `robots.txt` in mid-2025 to block major AI crawlers. Additionally, Shopify's Cloudflare layer may return 402/403 to AI user-agents even if robots.txt allows them.

Fetch `/robots.txt` and check for these user-agents:

| Bot | Purpose | Default Status |
|---|---|---|
| `GPTBot` | OpenAI training crawler | BLOCKED by Shopify |
| `OAI-SearchBot` | OpenAI real-time search | BLOCKED by Shopify |
| `ChatGPT-User` | ChatGPT browsing | BLOCKED by Shopify |
| `Google-Extended` | Google AI training (NOT Googlebot) | BLOCKED by Shopify |
| `ClaudeBot` | Anthropic's crawler | BLOCKED by Shopify |
| `anthropic-ai` | Anthropic's older agent | BLOCKED by Shopify |
| `PerplexityBot` | Perplexity search | BLOCKED by Shopify |
| `Applebot-Extended` | Apple AI features | BLOCKED by Shopify |
| `CCBot` | Common Crawl (feeds many LLMs) | Often blocked |
| `Bytespider` | ByteDance/TikTok crawler | Often blocked |
| `Meta-ExternalAgent` | Meta AI | Varies |
| `cohere-ai` | Cohere LLM | Varies |

**Detection:** Parse robots.txt for `User-agent: {bot}` followed by `Disallow: /`.

**Critical distinction:** `OAI-SearchBot` and `ChatGPT-User` are SEARCH bots (show your products in AI search results). `GPTBot` and `Google-Extended` are TRAINING bots (use your content for model training). Stores wanting AI visibility should consider allowing search bots while blocking training bots.

**Framing:**
- If ALL AI bots are blocked: "The store is invisible to AI search engines including ChatGPT, Perplexity, and Google AI Overviews. Products cannot appear in AI-generated shopping recommendations."
- If search bots are blocked but training bots would be too: "Consider allowing search-oriented AI bots (OAI-SearchBot, PerplexityBot) while keeping training bots blocked."
- Note: Shopify controls the default robots.txt. Merchants can customize it via `robots.txt.liquid` but many do not know they need to.
- Severity: HIGH

### 1.2 Cloudflare AI Bot Blocking

Shopify routes traffic through Cloudflare, which may independently block AI bots with 402 or 403 responses even if robots.txt allows them.

**Detection:** This cannot be reliably detected from a standard HTTP request. Note it as a potential issue if robots.txt blocks are found, since Cloudflare adds a second layer.

- Severity: MEDIUM (informational — cannot be fully audited from public data)

---

## 2. llms.txt

### 2.1 Presence

Check if `https://{domain}/llms.txt` returns HTTP 200 with valid content (not a 404, redirect to homepage, or empty response).

**What llms.txt is:** A Markdown file that tells AI crawlers what the site is about and where to find key content. It is the AI equivalent of robots.txt — but for discovery, not blocking.

**Spec requirements:**
- H1 heading with site/brand name
- Blockquote with a short site summary
- Sections with links to key pages (products, collections, about, blog)
- Optional: `llms-full.txt` with expanded content

**Detection:** Fetch `/llms.txt`, check HTTP status code. If 200, check for valid Markdown structure (H1, links).

- Severity: MEDIUM (growing importance — early adopters gain edge)

### 2.2 Quality

If llms.txt exists, check:
- Has an H1 heading
- Has a blockquote summary
- Links to product pages, collection pages, and about page
- Links are absolute URLs, not relative
- Content is substantive (not just the store name)

---

## 3. Entity Clarity and Brand Signals

### 3.1 Organization Schema

Check homepage JSON-LD for `@type: Organization` (or `@type: OnlineStore`, Google's recommended subtype for ecommerce).

**Required fields:**
- `name` — brand name
- `url` — store URL
- `logo` — logo image URL

**Recommended fields:**
- `sameAs` — array of social profile and authority URLs
- `contactPoint` — phone/email
- `description` — brand description
- `address` — physical address if applicable
- `foundingDate` — establishment date

- Severity: HIGH (foundation for Knowledge Panel eligibility and entity recognition)

### 3.2 sameAs Links

Check the `sameAs` array in Organization schema for links to:

| Platform | Why It Matters |
|---|---|
| Wikipedia | Strongest entity recognition signal |
| Wikidata | Feeds Google Knowledge Graph directly |
| LinkedIn company page | Professional entity signal |
| Instagram | Social proof |
| Facebook | Social proof |
| Twitter/X | Social proof |
| YouTube | Content authority signal |
| Google Business Profile | Local entity signal |
| Crunchbase | Business entity signal |

More sameAs links = stronger entity graph = higher Knowledge Panel and AI citation likelihood.

- Severity: HIGH

### 3.3 Brand Name Consistency

Check that the brand name is identical across:
- `<title>` tag pattern (e.g., "Product Name | Brand Name")
- Organization schema `name`
- `og:site_name`
- Store metadata from `/meta.json`
- Visible header/logo text

Inconsistencies weaken entity recognition. AI engines may treat different name forms as different entities.

- Severity: MEDIUM

### 3.4 About Page Quality

Check if `/pages/about` (or similar handle) exists and has substantive content.

Look for:
- Founder/team information
- Brand story
- Expertise signals (credentials, experience, certifications)
- Physical address or location
- Content depth (300+ words vs. 1-2 sentences)

About pages establish E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness) signals that AI engines use for citation confidence.

- Severity: MEDIUM

---

## 4. Citation-Worthiness Signals

### 4.1 Customer Review Volume

Check Product JSON-LD for `aggregateRating.reviewCount`.

Key stats:
- Brands on review platforms (Trustpilot, G2, Judge.me) have 3x higher ChatGPT citation chance.
- User-generated content is weighted highest by LLMs, followed by influencer/media content, then brand-owned content.

**Detection:** Parse JSON-LD from sampled product pages. Check for `aggregateRating` and `review` arrays. Count total reviews visible.

- Severity: HIGH

### 4.2 Original Data and Statistics

Check sampled page content for:
- Numerical claims (percentages, measurements, counts)
- Unique data points not found elsewhere
- Survey results or proprietary benchmarks
- Specific product test results or certifications

**Detection:** Scan page text for number patterns with context (e.g., "95% of customers", "tested for 500 hours", "handcrafted by 12 artisans").

- Severity: MEDIUM

### 4.3 Third-Party Review Platform Presence

Check sampled product pages for review widget scripts from known platforms:
- Judge.me
- Yotpo
- Stamped.io
- Loox
- Trustpilot
- Reviews.io

**Detection:** Check `<script>` tags and DOM elements for known review platform identifiers.

- Severity: MEDIUM

### 4.4 Press/Media Page

Check if `/pages/press`, `/pages/media`, `/pages/as-seen-in`, or similar exists.

Third-party mentions correlate 3x more with AI visibility than backlinks (r=0.664 vs r=0.218).

- Severity: LOW (informational)

---

## 5. Content Extractability

### 5.1 Answer-First Content Format

Check sampled pages for the answer-first pattern:
1. Question-formatted H2/H3 heading (starts with What/How/Why/When/Where/Who)
2. Immediately followed by a 40-60 word paragraph that directly answers the question
3. Then expanded detail

**Detection:** Parse headings, check for question words, measure word count of the following paragraph.

This is the single most important content format for AI citation. 72.4% of pages cited by ChatGPT had this pattern.

- Severity: HIGH

### 5.2 Comparison Tables

Check sampled pages for `<table>` elements with:
- `<th>` header cells
- At least 2 columns and 3+ rows
- Product comparison semantics (feature/spec/price comparisons)

Tables achieve 2.5x citation rate vs. plain text.

- Severity: HIGH

### 5.3 Structured Lists

Check for `<ul>` and `<ol>` elements with 5-7 items near headings.

Listicles make up 50% of top AI citations.

- Severity: MEDIUM

### 5.4 Content Depth

Check sampled page word counts:
- Pages under 300 words are thin for GEO purposes
- 2000+ word pages get cited 3x more by AI engines
- Collection pages with buying guide content below the product grid are especially valuable

- Severity: MEDIUM

### 5.5 Heading Hierarchy

Check for clean heading structure:
- Exactly one H1 per page
- H2s for main sections
- H3s nested under H2s
- No skipped levels

Pages with clean heading structure earn 2.8x higher AI citation rates.

- Severity: MEDIUM

---

## 6. Content Freshness

### 6.1 Product Update Dates

Check `updated_at` field from `/products.json`:
- Products not updated in 6+ months may signal stale catalog
- AI-cited content is 25.7% fresher than traditional organic results
- 76.4% of ChatGPT's most-cited pages updated in last 30 days

- Severity: MEDIUM

### 6.2 Blog Freshness

If blog exists, check most recent article publish date from sitemap or blog pages.
- No posts in 6+ months = stale content signal
- Regular publishing (weekly/biweekly) strengthens topical authority

- Severity: LOW

### 6.3 Schema Freshness Signals

Check for `dateModified` property in JSON-LD (Article, Product, WebPage schemas).
This is the strongest technical freshness signal for AI engines.

- Severity: MEDIUM

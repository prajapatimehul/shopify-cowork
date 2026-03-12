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

Focus on directly observable signals from the store: crawl access, entity clarity, third-party trust signals, extractable content, and freshness.

Do not rely on unsourced citation-rate claims or platform-wide assumptions. GEO findings should stay evidence-based and specific to the store being audited.

---

## 1. AI Bot Crawl Access

### 1.1 Robots.txt AI Bot Rules

**Critical rule:** Inspect the store's live `robots.txt` directly. Do not assume Shopify's default `robots.txt` blocks or allows AI crawlers. Shopify documents that stores ship with a default `robots.txt` optimized for SEO, and merchants can customize it via `robots.txt.liquid`.

Some Shopify stores also include comment banners in `robots.txt` about automated checkout or agent policy. Treat comments as context only; crawler access is determined by actual directives such as `User-agent`, `Allow`, `Disallow`, and `Crawl-delay`.

Fetch `/robots.txt` and check for these user-agents:

| Bot / Token | Purpose | What to check |
|---|---|---|
| `OAI-SearchBot` | OpenAI search indexing | Whether `robots.txt` explicitly allows or blocks it |
| `GPTBot` | OpenAI training crawler | Whether `robots.txt` explicitly allows or blocks it |
| `ChatGPT-User` | OpenAI user-initiated fetches | Note separately; OpenAI says it is not used for automatic search crawling |
| `Claude-SearchBot` | Anthropic search indexing | Whether `robots.txt` explicitly allows or blocks it |
| `ClaudeBot` | Anthropic training crawler | Whether `robots.txt` explicitly allows or blocks it |
| `Claude-User` | Anthropic user-initiated fetches | Note separately from search/training bots |
| `PerplexityBot` | Perplexity search indexing | Whether `robots.txt` explicitly allows or blocks it |
| `Google-Extended` | Google training/grounding control token | Whether `robots.txt` explicitly allows or blocks it |

**Detection:** Parse `robots.txt` for explicit groups targeting these tokens. Distinguish:
- Full-site block: `Disallow: /`
- Partial restriction: narrower path rules only
- No explicit directive: no bot-specific rule present

**Critical distinction:**
- `OAI-SearchBot`, `Claude-SearchBot`, and `PerplexityBot` are search-oriented crawlers.
- `GPTBot`, `ClaudeBot`, and `Google-Extended` relate to training or model-use permissions.
- `ChatGPT-User` and `Claude-User` are user-initiated fetch agents and should not be treated as automatic search crawlers.

**Framing:**
- If search-oriented bots are explicitly blocked: "Search-oriented AI crawlers are blocked in `robots.txt`, which likely reduces visibility in AI search experiences that rely on those crawlers."
- If only training-oriented bots or tokens are blocked: "Training-oriented AI access is restricted, but that alone does not prove the store is excluded from AI search results."
- If no explicit AI bot directives are present: "No explicit AI crawler directives were found in `robots.txt`. Do not assume either blocking or visibility beyond what the file states."
- Attribute findings to the live `robots.txt`, not to assumed Shopify defaults.
- Severity: HIGH

### 1.2 Cloudflare AI Bot Blocking

Some stores may add an additional blocking layer through CDN or WAF tooling. Cloudflare AI Crawl Control, for example, can return `403` or `402` responses when configured to block AI crawlers.

**Detection:** Do not assume this is present on Shopify by default. Mention it only when there is supporting evidence, such as bot-specific failures, provider-specific headers, or merchant documentation. From a standard public request, this is usually an inference rather than a confirmed finding.

- Severity: LOW (informational — usually cannot be confirmed from public data alone)

---

## 2. llms.txt

**Research-backed guidance:** Google explicitly states "you don't need new machine-readable files or AI text files" to appear in AI features. There is no special schema or file required for AI Overviews/AI Mode. Do NOT recommend creating llms.txt as an action item. Do NOT treat its absence as a problem.

### 2.1 Presence

Check if `https://{domain}/llms.txt` returns HTTP 200 with valid content (not a 404, redirect to homepage, or empty response).

**What llms.txt is:** An emerging community proposal for a Markdown file that gives LLMs a curated overview of a site. It is NOT a ranking factor, NOT required by any major AI search engine, and NOT part of Google's, Bing's, or Shopify's official AI guidance.

**Detection:** Fetch `/llms.txt`, check HTTP status code. Note presence or absence as informational context only.

- Severity: **INFORMATIONAL ONLY** (0 weight — never a finding, never a recommendation)
- **NEVER recommend creating llms.txt as an action item**
- If present: note it as a positive signal in SNAPSHOT, nothing more
- If absent: do not mention it in FINDINGS

### 2.2 Quality

If llms.txt exists, note its quality in SNAPSHOT context only. Do not create a finding about it.

---

## 3. Entity Clarity and Brand Signals

### 3.1 Organization Schema

**Research-backed guidance:** Organization schema is NOT in Google's or Bing's core AI citation requirements. It is not required for AI Overviews or Bing Copilot citations. Most DTC brands do not have Knowledge Panels. Only flag for nationally recognised brands where entity disambiguation genuinely matters.

Check homepage JSON-LD for `@type: Organization` (or `@type: OnlineStore`, Google's recommended subtype for ecommerce).

**Required fields (if present):**
- `name` — brand name
- `url` — store URL
- `logo` — logo image URL

**Recommended fields (if present):**
- `sameAs` — array of social profile and authority URLs
- `contactPoint` — phone/email
- `description` — brand description

- Severity: **CONDITIONAL** — only a finding for brands with national recognition or multi-brand stores where entity confusion is likely. For typical single-brand DTC stores, note in passing only.

### 3.2 sameAs Links

Check the `sameAs` array in Organization schema for links to authoritative profiles.

| Platform | Why It Matters |
|---|---|
| Wikipedia | Strong authority signal — only if brand genuinely merits a page |
| Wikidata | Structured entity signal |
| LinkedIn company page | Professional entity signal |
| Instagram | Social/brand consistency signal |

Consistent `sameAs` links can improve entity disambiguation for brands large enough to have disambiguation issues.

- Severity: **LOW** — most DTC brands do not need sameAs for AI citation readiness. Note as informational unless brand is nationally recognised or has entity confusion issues.

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

Visible first-party or third-party review signals can make product claims easier for AI systems to trust and quote.

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

Third-party validation and press mentions can strengthen citation confidence when they are specific and verifiable.

- Severity: LOW (informational)

---

## 5. Content Extractability

### 5.1 Answer-First Content Format

Check sampled pages for content that is clearly extractable by AI systems:
1. Clear heading structure that signals topic sections
2. Direct, factual content near headings (not preamble or marketing fluff)
3. Specific product attributes: sizing, materials, care instructions, specifications

**Detection:** Check for content clarity and completeness, not rigid word-count ranges. The key question: "Can an AI system extract a confident, factual answer from this content?"

- Severity: MEDIUM — focus on content clarity and completeness rather than strict question-heading format. Not every page needs question headings to be extractable.

### 5.2 Comparison Tables

**Research-backed guidance:** Comparison tables are relevant for multi-brand stores or stores selling varied product categories. Single-brand DTC stores (e.g., a shoe brand) typically do not need "Product A vs Product B" comparison tables.

Check sampled pages for `<table>` elements with comparison semantics only when contextually relevant:
- Multi-brand stores: comparison tables are valuable
- Single-brand stores: material/spec comparison across product lines can help, but absence is NOT a finding
- Blog/guide content: comparison tables in buying guides are valuable

- Severity: **CONDITIONAL** — HIGH for multi-brand stores, LOW/informational for single-brand DTC stores

### 5.3 Structured Lists

Check for `<ul>` and `<ol>` elements with 5-7 items near headings.

Structured lists can improve extractability when they summarize benefits, steps, or comparisons cleanly.

- Severity: MEDIUM

### 5.4 Content Depth

Check sampled page word counts:
- Pages under 300 words are thin for GEO purposes
- Deep pages often have more surface area for extractable facts and citations
- Collection pages with buying guide content below the product grid are especially valuable

- Severity: MEDIUM

### 5.5 Heading Hierarchy

Check for clean heading structure:
- Exactly one H1 per page
- H2s for main sections
- H3s nested under H2s
- No skipped levels

Clean heading structure makes page sections easier to parse and cite accurately.

- Severity: MEDIUM

---

## 6. Content Freshness

### 6.1 Product Update Dates

Check `updated_at` field from `/products.json`:
- Products not updated in 6+ months may signal stale catalog
- Recently updated products can signal that availability, pricing, and merchandising information is current

- Severity: MEDIUM

### 6.2 Blog Freshness

If blog exists, check most recent article publish date from sitemap or blog pages.
- No posts in 6+ months = stale content signal
- Regular publishing (weekly/biweekly) strengthens topical authority

- Severity: LOW

### 6.3 Schema Freshness Signals

Check for `dateModified` property in JSON-LD (Article, Product, WebPage schemas).
This is a useful machine-readable freshness signal when it matches visible page updates.

- Severity: MEDIUM

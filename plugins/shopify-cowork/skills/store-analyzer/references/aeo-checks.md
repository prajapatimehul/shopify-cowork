# AEO Checks — Answer Engine Readiness

## Contents

1. FAQ schema
2. Instructional content
3. Featured snippet readiness
4. Voice search readiness
5. People Also Ask optimization
6. Review snippet eligibility
7. Knowledge Panel signals
8. Comparison and buying guide content

---

## Context

AEO (Answer Engine Optimization) is about winning direct answer positions — featured snippets, answer boxes, voice responses, Knowledge Panels, and People Also Ask boxes.

Key context:
- A significant share of Google searches result in zero clicks (direct answers, Knowledge Panels, AI Overviews).
- Voice assistants frequently extract answers from featured snippets.
- **Important:** Google deprecated FAQ rich results for most sites (August 2023). Only gov/health sites get SERP display. The value for ecommerce is in the FAQ *content*, not the markup.
- AI citation readiness depends on indexability, content extractability, and completeness — not on specific schema types (per Google's official guidance).

---

## 1. FAQ Schema

### 1.1 FAQ Content Quality (NOT Schema Presence)

**Research-backed guidance:** Google deprecated FAQ rich results for most sites (August 2023) — only gov/health sites get SERP display. Google also states structured data features are never guaranteed even when implemented. Do NOT score FAQPage schema presence as a positive factor for AI citation readiness.

**What actually matters:** Shopify's AI guidance specifically highlights that complete store policies and curated FAQs help AI agents answer shopper questions. The value is in the **content**, not the markup.

Check for:
- Does the store have FAQ content (on product pages, dedicated FAQ page, policy pages)?
- Is the FAQ content substantive — does it answer real customer questions (sizing, shipping, returns, care, materials)?
- Is the content visible on the page (not hidden behind JavaScript accordions that block extraction)?
- Does it cover the questions shoppers actually ask?

**Do NOT check for or reward:**
- FAQPage schema markup presence
- Specific JSON-LD structure for FAQs
- Schema as a driver of AI citations

- Severity: HIGH (for FAQ **content** quality) / INFORMATIONAL (for schema presence)

### 1.2 FAQPage vs QAPage

Verify the store uses `FAQPage` (brand provides definitive answers) not `QAPage` (community-style with multiple answers).

`FAQPage` provides structured, authoritative single answers that AI systems prefer. `QAPage` signals user-generated Q&A, reducing citation confidence.

- Severity: MEDIUM

### 1.3 FAQ Content Visibility

Cross-reference questions in FAQPage schema against visible page content. Google requires schema content to match visible content. Schema-only FAQ with no visible Q&A on the page is a violation.

- Severity: HIGH

### 1.4 FAQ Placement

Check WHERE FAQs appear:
- Product pages: sizing, care, shipping, return questions
- Collection pages: category buying guide questions
- Homepage: brand and trust questions

Most valuable placement for ecommerce: product pages (captures product-specific long-tail queries).

- Severity: MEDIUM

---

## 2. Instructional Content

**Research-backed guidance:** Google deprecated HowTo rich results (September 2023). HowTo schema is irrelevant for non-instructional products (shoes, clothing, accessories). Do NOT flag missing HowTo schema unless the store sells products that genuinely require assembly, setup, or step-by-step usage instructions.

### 2.1 Instructional Content (Gated by Product Type)

**Only check when relevant:**
- Assembly/setup products (furniture, electronics, DIY kits)
- Products with care/maintenance routines (leather goods, plants, specialty items)
- Products with how-to-use content (cosmetics application, cooking equipment)

**Skip for:** shoes, clothing, accessories, jewelry, basic consumer goods — these do not need instructional content or HowTo schema.

Check for step-by-step content patterns:
- Headings with "Step 1:", "How to...", numbered items
- `<ol>` elements within product descriptions or blog posts
- Pages at `/blogs/` or `/pages/` with care guides, styling guides

**Do NOT check for or recommend:** HowTo schema markup (deprecated by Google).

- Severity: **CONDITIONAL** — only relevant for instructional product categories. Never a finding for clothing/shoes/accessories stores.

---

## 3. Featured Snippet Readiness

### 3.1 Paragraph Snippet Format

Check sampled pages for the snippet-winning pattern:
1. Question-formatted H2/H3 heading
2. First paragraph after heading is 40-60 words (optimal: 45 words / ~293 characters)
3. Paragraph directly answers the question (not preamble)

Paragraph snippets account for ~70% of all featured snippets. Over 65% are triggered by question-format queries.

**Detection:** Parse H2/H3 tags for question words. Extract immediately following `<p>`. Measure word count.

- Severity: HIGH

### 3.2 List Snippet Format

Check for `<ol>` or `<ul>` with ~6 items and ~44 total words, preceded by a relevant H2/H3.

List snippets are 19.1% of featured snippets. Listicles are 32% of all AI citations.

- Severity: HIGH

### 3.3 Table Snippet Format

Check for `<table>` elements with `<th>` headers, `<tr>` rows, `<td>` cells. Minimum 2 columns, 3+ rows. Google displays up to 6 rows in table snippets.

Table snippets are 6.3% of featured snippets but have high win rates for comparison and pricing queries.

- Severity: MEDIUM

---

## 4. Voice Search Readiness

### 4.1 Concise Answer Blocks

Check for 29-40 word answer blocks near question headings. This is the typical Google Home answer length.

**Detection:** After each question-formatted H2/H3, measure word count of following paragraph. Ideal: 29-40 words for voice, 40-60 words for text snippets.

- Severity: MEDIUM

### 4.2 Conversational Language

Check product descriptions for natural language patterns:
- "Best for...", "Recommended for...", "How do I..."
- Attribute-rich content (material, size, occasion) that voice assistants extract
- Question-answer pairs embedded in descriptions

- Severity: LOW

### 4.3 Product Schema Completeness for Voice

Voice assistants rely on structured product attributes to answer queries like "How much does X cost?" and "Is X in stock?"

Check Product JSON-LD for: `offers.price`, `offers.priceCurrency`, `offers.availability`, `aggregateRating`, `brand`, `description`, `sku`.

- Severity: HIGH (overlaps with SEO structured data checks)

### 4.4 Speakable Schema

Check for `SpeakableSpecification` in JSON-LD — identifies content optimized for text-to-speech.

**Current limitation:** Speakable is in BETA, restricted to news/publisher sites in English for US users. Ecommerce sites cannot leverage it yet. Report as "future-ready" signal only.

- Severity: LOW

---

## 5. People Also Ask Optimization

### 5.1 Question-Based Heading Structure

Check sampled pages for H2/H3 tags phrased as questions:
- "What size should I order?"
- "How do I care for this product?"
- "Is this product worth it?"
- "What's the difference between X and Y?"

Google often pulls the paragraph under an H2/H3 as the PAA answer.

**Detection:** Parse all H2/H3 tags. Count those starting with What/How/Why/When/Where/Who/Is/Can/Does.

- Severity: MEDIUM — helpful pattern but not every page needs question headings to be extractable

### 5.2 Direct Answer First Paragraph

After each question heading, the first paragraph should directly address the question before expanding into detail.

**Detection:** For each question heading, extract the following paragraph. Check whether it directly addresses the question. Do NOT enforce rigid word-count ranges.

- Severity: MEDIUM

### 5.3 Related Question Coverage

Check if pages cover multiple related questions (not just one). Look for FAQ sections, "Common Questions" blocks, or multiple Q&A pairs. Minimum 3-5 questions per product/category page for good PAA coverage.

- Severity: MEDIUM

---

## 6. Review Snippet Eligibility

### 6.1 AggregateRating Schema

Check Product JSON-LD for valid `aggregateRating`:
- `ratingValue` (required)
- `bestRating` (recommended)
- `ratingCount` or `reviewCount` (at least one required)

Product pages with AggregateRating are eligible for star review snippets. Stars dramatically increase CTR.

- Severity: HIGH

### 6.2 Review Content Visibility Match

Check that `ratingValue`, `reviewCount`, and `ratingCount` in schema EXACTLY match what is visible on the page. Mismatch can result in loss of review rich results.

- Severity: HIGH

### 6.3 Individual Review Schema

Check for `review` array in Product JSON-LD with objects containing:
- `@type: Review`
- `author` (with name)
- `reviewRating` (with ratingValue)
- `reviewBody` (actual review text)

- Severity: MEDIUM

### 6.4 Third-Party Review Platform

Check for review widgets from Judge.me, Yotpo, Stamped.io, Loox, Trustpilot, Reviews.io. Third-party reviews strengthen compliance with Google's self-serving review policy.

**Detection:** Check `<script>` tags and DOM elements for known review platform identifiers.

- Severity: MEDIUM

---

## 7. Knowledge Panel Signals

**Research-backed guidance:** Most DTC brands do NOT have Knowledge Panels and are unlikely to get one. This is not a meaningful target for typical Shopify stores. Do NOT flag missing Knowledge Panel eligibility as a finding.

### 7.1 Organization Schema with sameAs

Covered in geo-checks.md section 3.1-3.2. Cross-reference here for completeness.

- Severity: **LOW for most DTC brands** — only relevant for nationally recognised brands with entity disambiguation needs. See geo-checks.md §3.1 for conditional guidance.

### 7.2 Wikidata Entry

Check `sameAs` array for `wikidata.org` URL. Wikidata entries can feed Google Knowledge Graph.

- Severity: **LOW** — most DTC brands don't have Wikidata entries and don't need them. Only note for brands with national/international recognition.

---

## 8. Comparison and Buying Guide Content

**Research-backed guidance:** Comparison content is context-dependent. Single-brand DTC stores (one brand, one product category) do NOT need "A vs B" comparison tables — they have no competitor products to compare. Multi-brand stores and retailers benefit significantly from comparison content.

### 8.1 Comparison Tables on Pages (Gated)

**Only flag for:**
- Multi-brand stores/marketplaces where shoppers compare products
- Stores with varied product categories where cross-category comparison helps

**Do NOT flag for:**
- Single-brand DTC stores (e.g., a shoe brand comparing only their own shoes)
- Stores where "comparison" means material/spec tables within product descriptions (these are product attributes, not comparison content — check in PDP completeness instead)

- Severity: **CONDITIONAL** — HIGH for multi-brand, INFORMATIONAL for single-brand DTC

### 8.2 Buying Guide Content

Check blog and page titles/headings for buying guide content:
- "Best [Category] in [Year]"
- "Buying Guide"
- Category-level educational content

Buying guides are valuable when they address genuine purchase-decision questions, but their absence is not a finding for every store.

- Severity: MEDIUM — only flag if the store has a blog/content section but no category-level guides

### 8.3 Buying Guide Depth

For identified guide pages, check for substantive content with clear structure, factual claims, and product recommendations.

- Severity: LOW — informational quality note, not a standalone finding

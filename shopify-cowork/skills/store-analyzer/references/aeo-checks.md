# AEO Checks — Answer Engine Readiness

## Contents

1. FAQ schema
2. HowTo schema
3. Featured snippet readiness
4. Voice search readiness
5. People Also Ask optimization
6. Review snippet eligibility
7. Knowledge Panel signals
8. Comparison and buying guide content

---

## Context

AEO (Answer Engine Optimization) is about winning direct answer positions — featured snippets, answer boxes, voice responses, Knowledge Panels, and People Also Ask boxes.

Key stats:
- ~60% of Google searches end without a click.
- 40.7% of voice search answers are pulled from featured snippets.
- Pages with FAQ schema are 3.2x more likely to appear in Google AI Overviews.
- FAQ schema produces 28-36% higher citation rates in AI-generated answers.

---

## 1. FAQ Schema

### 1.1 FAQPage Schema Presence

Check sampled pages for `@type: FAQPage` in JSON-LD with `mainEntity` array containing `@type: Question` objects, each with `acceptedAnswer` of `@type: Answer`.

Valid structure:
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "What size should I order?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "We recommend ordering your usual size..."
    }
  }]
}
```

**Important note:** Google deprecated FAQ rich results for most sites (August 2023) — only government and health sites get the SERP display. However, FAQ schema still drives AI citations. AI platforms actively crawl and cite FAQ structured data. The schema remains critical for GEO/AEO even without traditional rich result display.

- Severity: HIGH (for AI citation) / LOW (for SERP rich result)

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

## 2. HowTo Schema

### 2.1 HowTo Schema Presence

Check for `@type: HowTo` in JSON-LD with a `step` array of `HowToStep` objects.

Relevant for ecommerce content:
- Styling guides
- Care instructions
- Assembly/setup guides
- How-to-wear/how-to-use content
- Gift guides with steps

**Note:** Google deprecated HowTo rich results (September 2023). But the schema still helps AI systems parse instructional content. Step-by-step content is citation-friendly because LLMs can extract individual steps.

- Severity: MEDIUM

### 2.2 Instructional Content Without Schema

Even without HowTo schema, check for step-by-step content patterns:
- Headings with "Step 1:", "How to...", numbered items
- `<ol>` elements within product descriptions or blog posts
- Pages at `/blogs/` or `/pages/` with care guides, styling guides

- Severity: LOW

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

- Severity: HIGH

### 5.2 Direct Answer First Paragraph

After each question heading, the first paragraph should be a direct, concise answer (40-60 words) before expanding into detail.

**Detection:** For each question heading, extract the following paragraph. Check word count and whether it directly addresses the question.

- Severity: HIGH

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

### 7.1 Organization Schema with sameAs

Covered in geo-checks.md section 3.1-3.2. Cross-reference here for completeness.

Key requirements:
- `@type: Organization` or `@type: OnlineStore` on homepage
- `sameAs` array linking to Wikipedia, Wikidata, social profiles
- Consistent NAP (Name, Address, Phone)

- Severity: HIGH

### 7.2 Wikidata Entry

Check `sameAs` array for `wikidata.org` URL. Wikidata entries feed Google Knowledge Graph directly and are considered essential for Knowledge Panel eligibility.

- Severity: HIGH (for established brands) / LOW (for new stores)

---

## 8. Comparison and Buying Guide Content

### 8.1 Comparison Tables on Pages

Check for `<table>` elements on product, collection, and blog pages with comparison semantics (column headers with product/feature names, rows with specs/pricing).

AI answers frequently respond to "Which product is best?" and "How does A compare to B?" queries.

- Severity: HIGH

### 8.2 "X vs Y" Content

Check blog and page titles/headings for comparison patterns:
- "[Product A] vs [Product B]"
- "Best [Category] in [Year]"
- "Buying Guide"
- "[Product] Compared"

- Severity: HIGH

### 8.3 Buying Guide Depth

For identified guide/comparison pages, check:
- Word count (1,000+ words for comprehensive guide)
- Multiple H2/H3 sections
- Presence of lists and/or tables
- Recommendation language ("we recommend", "best for", "ideal for")

LLMs prefer to extract from a single comprehensive source rather than aggregating from multiple pages.

- Severity: MEDIUM

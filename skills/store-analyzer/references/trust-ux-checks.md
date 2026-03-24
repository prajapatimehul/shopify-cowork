# Trust & UX Checks

Checks derived from 15 Shopify Community feedback threads, 50+ real store reviewers (March 2026).
Trust signals and basic UX are the #1 thing real reviewers look at.

## Evidence Rules

- All checks use public HTML, DOM inspection, and page rendering.
- Label findings as `Sampled` since these require rendered page inspection.
- Do NOT make subjective design judgments (color taste, "looks premium"). Only flag measurable, structural issues.

---

## 1. Store Identity & Branding

**Why it matters:** 6/15 threads flagged missing logos/favicons. Basic identity signals = baseline trust.

### Checks:
- **Favicon present**: Does `<link rel="icon">` or `<link rel="shortcut icon">` exist in `<head>`?
- **Logo in header**: Is there an `<img>` or `<svg>` in the header/nav area with alt text containing the brand name?
- **Branded email**: Does the contact page use a domain email (info@store.com) or a free provider (gmail.com, yahoo.com, icloud.com, hotmail.com)?
- **About page exists and has content**: Does `/pages/about` or `/pages/about-us` exist with >200 words of real content? (GEO module in geo-checks.md §3.4 adds depth/E-E-A-T checks on top — merge into one finding if both trigger.)

### How to detect:
- Parse `<head>` for favicon link tags.
- Parse header/nav for logo `<img>` with `logo` in class/id/alt or `<svg>` with brand-related content.
- Fetch contact page, look for email addresses, check domain.
- Fetch about page, count words. Under 200 words = thin.

### Red flags:
- No favicon (browser tab shows generic icon)
- No visible logo in header
- Gmail/iCloud/Yahoo contact email on a store charging $50+ per item
- About page missing or under 200 words
- About page is placeholder text ("About us" with no actual content)

---

## 2. Contact & Business Legitimacy

**Why it matters:** 10/15 threads flagged incomplete contact info. Customers need to know the business is real.

### Checks:
- **Contact page exists**: Does `/pages/contact` or `/pages/contact-us` exist?
- **Phone number visible**: Is there a phone number anywhere (contact page, footer, header)?
- **Physical address visible**: Is there a street address or at least city/country visible?
- **Contact form works**: Is there a `<form>` on the contact page?
- **Multiple contact methods**: Are there at least 2 contact methods (email + form, or email + phone, or form + chat)?

### How to detect:
- Fetch contact page. Look for: phone patterns (digits with dashes/spaces/parens), address patterns (street, suite, city, state, zip, country), `<form>` elements.
- Check footer HTML for phone, address, email across all sampled pages.
- Look for chat widgets: `tidio`, `gorgias`, `zendesk`, `intercom`, `crisp`, `shopify-chat`, `shopify-inbox`, `re:amaze`, `freshdesk`, `drift`, `tawk`.

### Red flags:
- No contact page at all
- Contact page with just an email address and nothing else
- No phone number anywhere on the site
- No physical address (raises legitimacy concerns)
- No live chat widget for stores with 50+ products

---

## 3. Footer Completeness

**Why it matters:** 4/15 threads flagged incomplete footers. Footer = trust baseline for every page.

### Checks:
- **Payment icons visible**: Are payment method icons/images in the footer (Visa, Mastercard, PayPal, etc.)?
- **Policy links present**: Does footer link to Privacy Policy, Terms of Service, Refund Policy, Shipping Policy?
- **Social media links**: Are there links to social profiles (Instagram, Facebook, TikTok, Twitter/X)?
- **Business info in footer**: Is there a business name, address, or copyright notice?

### How to detect:
- Parse footer HTML for: `payment-icons`, `payment-methods`, Visa/Mastercard/PayPal image references.
- Check for links containing: `privacy`, `terms`, `refund`, `return`, `shipping` in footer.
- Check for social links: `instagram.com`, `facebook.com`, `tiktok.com`, `twitter.com`, `x.com`, `pinterest.com`, `youtube.com`.
- Check for copyright text or business name in footer.

### Red flags:
- No payment icons in footer
- Missing policy links
- Zero social media links
- No business identification in footer

---

## 4. Policy & Shipping Transparency

**Why it matters:** 7/15 threads flagged hidden shipping/returns info. Uncertainty = abandoned carts.

### Checks:
- **Shipping policy page exists**: Does `/policies/shipping-policy` or `/pages/shipping` exist with real content?
- **Return policy page exists**: Does `/policies/refund-policy` or `/pages/returns` exist with real content?
- **Policy pages have substance**: Are policies real content (>150 words) or placeholder/template text?
- **Shipping info accessible from product page**: Can a customer find shipping info without leaving the product page?

### How to detect:
- Fetch policy URLs. Check for placeholder patterns: "Use this text to share information about your", "Write your refund policy here", Shopify template default text.
- Count words on policy pages. Under 100 words = likely placeholder.
- Check product page for shipping info blocks, accordions, or links to shipping policy.

### Red flags:
- Shipping policy is Shopify default placeholder
- Return policy missing or template text
- No way to find shipping cost/time from the product page
- Policies exist but are under `/policies/` which is robots-blocked (informational only — Shopify blocks this path by default, but policies should also be accessible via `/pages/` or on-page accordions)

---

## 5. Page Speed & Core Web Vitals

**Why it matters:** 8/15 threads flagged slow loading. Speed directly impacts conversion and SEO rankings.

### Checks:
- **PageSpeed Insights score**: What are the mobile performance scores from Google PageSpeed Insights API?
- **Largest Contentful Paint (LCP)**: Is it under 2.5 seconds?
- **Cumulative Layout Shift (CLS)**: Is it under 0.1?
- **First Contentful Paint (FCP)**: Is it under 1.8 seconds?
- **Heavy JavaScript**: Are there excessive third-party app scripts loading?

### How to detect:
- Run Google PageSpeed Insights via CLI: `curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://{domain}&category=performance&strategy=mobile"`
- Parse the JSON response for: `lighthouseResult.categories.performance.score`, `lighthouseResult.audits['largest-contentful-paint']`, `lighthouseResult.audits['cumulative-layout-shift']`, `lighthouseResult.audits['first-contentful-paint']`.
- Count `<script>` tags from third-party domains on the homepage.

### Error handling:
- If PSI API returns non-200 or times out after 30 seconds, report "PageSpeed data unavailable" in SNAPSHOT. Skip speed findings. Do not retry more than once.
- No API key is required for single-store audits.

### Red flags:
- Mobile performance score under 50
- LCP over 4 seconds
- CLS over 0.25
- More than 15 third-party scripts on homepage
- Above-the-fold images using `loading="lazy"` (should load eagerly)

### How to report:
- Report actual scores with specific numbers.
- Do NOT recommend micro-optimizations (fetchpriority, preload hints). Only flag structural speed issues.
- Focus on: excessive app scripts, unoptimized hero images, render-blocking resources.

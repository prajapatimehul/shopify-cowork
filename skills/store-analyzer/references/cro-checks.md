# CRO & Conversion Checks

Checks derived from 15 Shopify Community feedback threads, 50+ real store reviewers (March 2026).
These are the things real humans check first when reviewing a Shopify store.

## Evidence Rules

- All checks use public HTML, DOM inspection, and page rendering.
- Use browser to load the page and inspect rendered DOM, or fetch raw HTML and parse.
- Label findings as `Sampled` since these require rendered page inspection.

---

## 1. Hero Section & Value Proposition

**Why it matters:** 13/15 reviewer threads flagged weak hero sections. First impression = first conversion gate.

### Checks:
- **Hero CTA exists**: Does the above-the-fold area of the homepage have at least one button/link with action text (Shop Now, Browse, Explore, Get Started)?
- **Hero heading exists**: Is there a visible H1 or prominent heading in the hero area with a value proposition (not just the store name)?
- **Hero image present**: Does the hero have a background image, video, or prominent visual?

### How to detect:
- Fetch homepage HTML. Look for the first `<section>` or prominent `<div>` containing an `<a>` or `<button>` with CTA text patterns: shop, browse, explore, get, buy, discover, view, start.
- Check if there's a heading (h1/h2) in the first major section.
- Check for `<img>`, `background-image`, or `<video>` in the hero area.

### Red flags:
- No CTA button above the fold
- Hero heading is just the store name or logo text with no value proposition
- Splash screen / animation blocking entry to the store
- Empty hero with just a slideshow and no text

---

## 2. Cart Experience

**Why it matters:** 10/15 threads flagged cart redirects. Slider/drawer carts keep customers browsing.

### Checks:
- **Cart type**: Does clicking "Add to Cart" redirect to `/cart` page, or open a drawer/slider?
- **Cross-sell in cart**: Does the cart area show related products, "frequently bought together", or "you may also like"?
- **Free shipping bar**: Is there a progress bar showing distance to free shipping threshold?

### How to detect:
- Look for cart drawer/slider indicators in HTML: `cart-drawer`, `cart-sidebar`, `slide-cart`, `ajax-cart`, `CartDrawer`. Shopify Dawn theme uses `cart-drawer` component.
- Check for cross-sell widgets: `cart-upsell`, `cross-sell`, `frequently-bought`, `also-like`, `cart-recommendation`.
- Check for shipping bar: `shipping-bar`, `free-shipping`, `progress-bar` in cart-related HTML, or known app scripts (iCart, Hextom, FreeShippingBar).

### Red flags:
- Cart redirects to `/cart` page (breaks browsing flow)
- Zero cross-sell or upsell in cart
- No shipping threshold visibility

---

## 3. Product Page Conversion Elements

**Why it matters:** Product pages are where buying decisions happen. Missing elements = lost sales.

### Checks:
- **Size chart presence** (apparel/jewelry/shoes): Is there a size chart link, popup, or section on product pages?
- **Shipping info on product page**: Is delivery time or shipping info visible near the Add to Cart button?
- **Return policy on product page**: Is return/refund info visible on the product page (not just in footer)?
- **Trust badges near ATC**: Are there trust icons, payment badges, or guarantee text near the Add to Cart button?
- **Product image count**: How many images does each product have? Single image = red flag.
- **Express checkout options**: Are Shop Pay, PayPal, Apple Pay, Google Pay buttons visible?

### How to detect:
- Search product page HTML for: `size-chart`, `size-guide`, `sizing`, `fit-guide`.
- Look for shipping info blocks: `shipping-info`, `delivery-time`, `shipping-policy`, `estimated-delivery`.
- Look for trust elements near ATC: `trust-badge`, `guarantee`, `secure-checkout`, `payment-icons`, `shopify-payment-button`.
- Count `<img>` tags inside the product media gallery section.
- Look for `shopify-payment-button`, `paypal`, `apple-pay`, `google-pay`, `ShopifyPaymentButton`.

### Red flags:
- No size chart on apparel/jewelry/shoes store
- Zero shipping info on product pages
- No trust signals near purchase button
- Only 1 image per product (no angles, no lifestyle)
- No express checkout options visible

---

## 4. Urgency & Social Proof Elements

**Why it matters:** 7/15 threads flagged missing urgency. Social proof converts browsers to buyers.

### Checks:
- **Review widget installed**: Is there a review app rendering on product pages? (Judge.me, Loox, Stamped, Yotpo, Shopify Reviews)
- **Review count visible**: Do product pages show star ratings and review counts?
- **Product badges**: Are there "New", "Bestseller", "Sale", "Limited" badges on collection/product pages?
- **Stock urgency**: Any "Only X left", "Low stock", or countdown timer elements?

### How to detect:
- Search for review app scripts/elements: `judgeme`, `judge.me`, `loox`, `stamped`, `yotpo`, `spr-`, `shopify-product-reviews`, `reviewsio`, `reviews.io`, `junip`, `okendo`.
- Look for star rating elements: `star-rating`, `spr-starrating`, `jdgm-star`, `rating`.
- Look for badge elements: `badge`, `product-badge`, `sale-badge`, `new-badge`, `bestseller`.
- Look for urgency: `inventory-quantity`, `low-stock`, `countdown`, `timer`, `hurry`, `only-left`.

### Red flags:
- Review app installed but zero reviews displayed (common with Judge.me on new stores)
- No star ratings visible on collection pages
- No product differentiation badges

---

## 5. Email Capture & Retention

**Why it matters:** 6/15 threads flagged missing email capture. First-time visitor who leaves = lost forever.

### Checks:
- **Email popup/form**: Is there an email capture mechanism? (popup, inline form, exit-intent)
- **Email app detected**: Klaviyo, Omnisend, Privy, Mailchimp, Shopify Email scripts present?
- **Newsletter in footer**: Is there a newsletter signup form in the footer?

### How to detect:
- Look for popup/form scripts: `klaviyo`, `omnisend`, `privy`, `mailchimp`, `convertkit`, `justuno`, `optinmonster`, `popup`, `newsletter-form`, `email-signup`.
- Check footer for: `<form>` with email input, `newsletter`, `subscribe`, `signup`.

### Red flags:
- Zero email capture on entire site
- No footer newsletter signup

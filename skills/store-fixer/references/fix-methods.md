# Store Fixer Methods

## Contents

1. Decision tree
2. Theme fixes
3. Admin API fixes
4. Mixed fixes
5. Manual-only fixes

## 1. Decision tree

Use this order:

1. Is the problem in rendered storefront code or theme templates?
2. Is the problem in authenticated store data?
3. Does the fix span both theme code and store data?
4. Is the real fix inside a third-party app or merchant-only admin setting?

Choose:

- `Theme` if the change lives in Liquid, JSON templates, sections, snippets, assets, or theme configuration
- `Admin API` if the change lives in products, collections, pages, metafields, or other authenticated objects
- `Mixed` if both are true
- `Manual` if the merchant must change app settings or admin-only configuration directly

## 2. Theme fixes

Typical theme fixes:

- patch `robots.txt.liquid`
- add or adjust JSON-LD snippets
- add FAQ markup or FAQ sections
- fix canonical, title, meta description, heading, or internal linking templates
- adjust collection or product card markup
- improve LCP image markup, dimensions, or fetch priority
- add static content blocks or supporting page templates

Theme fixes are best when:

- the problem is visible in page HTML
- the change should apply consistently across many pages through templates
- the solution is easier and safer in theme code than per-object content edits

Do not use theme code to fake product data that should really live on products or collections.

## 3. Admin API fixes

Typical Admin API fixes:

- update product titles, handles, descriptions, tags, vendors, or product SEO content
- update collection titles, descriptions, handles, or related metadata
- update pages or other authenticated store content
- write scoped metadata that should live on objects rather than in Liquid conditionals

Admin API fixes are best when:

- the issue is object-specific
- the merchant wants repeatable catalog updates
- the theme should read structured data from store objects instead of hardcoded values

Before bulk updates:

- define the object count
- define the exact fields to change
- capture the pre-change values for rollback

## 4. Mixed fixes

Use mixed execution when both a storefront template change and object updates are necessary.

Examples:

- analyzer finds thin product descriptions and missing product schema enhancements
- a category needs better collection copy and a new FAQ section in the theme
- product pages need richer content plus a theme snippet that renders it consistently

Order of work:

1. capture baseline for both channels
2. make the data change
3. make the theme change
4. verify rendered storefront behavior

If access exists for only one side, stop and return a split plan.

## 5. Manual-only fixes

Some fixes should not be automated from this skill:

- third-party app settings with no safe API path
- Search and Discovery or merchant dashboard settings that require human review
- app install, approval, or scope consent steps
- business decisions such as permanent redirect strategy, taxonomy redesign, or legal copy approval

When the fix is manual:

- state exactly why automation is not appropriate
- provide the exact merchant steps
- name the screen, setting, or app where the merchant must act

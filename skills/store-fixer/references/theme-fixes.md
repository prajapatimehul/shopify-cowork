# Theme Fix Reference (Tier 2)

Theme fixes modify Liquid template files. They carry higher risk than data fixes. Always backup before editing.

## Prerequisites

- `write_themes` scope on the access token
- For public apps: requires Shopify protected scope exemption
- For custom apps (like claude-access): can be granted directly

## Reading Theme Files

### Find the live theme ID

```graphql
query {
  themes(first: 10, roles: MAIN) {
    nodes { id name role }
  }
}
```

### Read a theme file
```graphql
query ThemeFile($themeId: ID!, $filenames: [String!]!) {
  theme(id: $themeId) {
    files(filenames: $filenames, first: 10) {
      nodes {
        filename
        body { ... on OnlineStoreThemeFileBodyText { content } }
      }
    }
  }
}
```

## Writing Theme Files

### GraphQL (recommended)

```graphql
mutation ThemeFilesUpsert($themeId: ID!, $files: [OnlineStoreThemeFilesUpsertFileInput!]!) {
  themeFilesUpsert(themeId: $themeId, files: $files) {
    upsertedThemeFiles { filename }
    userErrors { field message }
  }
}
```

Max 50 files per request. Input: `[{ "filename": "snippets/seo-schema.liquid", "body": { "type": "TEXT", "value": "...liquid code..." } }]`

---

## Fix: Structured Data / JSON-LD

**Approach:** Create a new snippet file rather than editing existing templates. Safer, easier to rollback.

### Step 1: Create `snippets/seo-schema.liquid`

```liquid
{%- if template.name == 'product' -%}
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Product",
    "name": {{ product.title | json }},
    "description": {{ product.description | strip_html | truncate: 500 | json }},
    "image": {{ product.featured_image | image_url: width: 1200 | json }},
    "brand": {
      "@type": "Brand",
      "name": {{ product.vendor | json }}
    },
    "sku": {{ product.selected_or_first_available_variant.sku | json }},
    "offers": {
      "@type": "Offer",
      "url": {{ request.origin | append: product.url | json }},
      "price": {{ product.selected_or_first_available_variant.price | money_without_currency | json }},
      "priceCurrency": {{ cart.currency.iso_code | json }},
      "availability": "https://schema.org/{% if product.available %}InStock{% else %}OutOfStock{% endif %}"
    }
  }
  </script>
{%- endif -%}
```

### Step 2: Include in theme.liquid

Add before `</head>` in `layout/theme.liquid`:
```liquid
{% render 'seo-schema' %}
```

### Rollback: Delete the snippet and remove the render tag.

---

## Fix: Collection-Prefixed Internal Links

**Problem:** Theme uses `{{ product.url | within: collection }}` which generates `/collections/X/products/Y` URLs instead of clean `/products/Y` URLs.

**Fix:** Replace `within: collection` with plain `product.url` in collection templates.

### Step 1: Find occurrences

Search theme files for `within: collection` or `within:collection`:
- `sections/collection-template.liquid`
- `snippets/product-card.liquid`
- `snippets/card-product.liquid`
- Theme-specific variations

### Step 2: Replace

```liquid
# BEFORE
{{ product.url | within: collection }}

# AFTER
{{ product.url }}
```

### Risk: Some themes use the collection context for breadcrumbs or "back to collection" links. Removing `within: collection` may break those. Check the surrounding code.

### Rollback: Restore original file from backup.

---

## Fix: Dawn H1-on-Logo

**Problem:** Dawn theme wraps the logo/site title in `<h1>` tags in `sections/header.liquid`. Every page has the brand name as H1 instead of the product/collection title.

**Fix:** Change the logo wrapper from `<h1>` to a different tag, ensure product/collection pages use their own H1.

### Locate in `sections/header.liquid`:

Look for pattern like:
```liquid
<h1 class="header__heading">
  <a href="/" class="header__heading-link">
    {%- if section.settings.logo != blank -%}
      ...logo image...
    {%- else -%}
      {{ shop.name }}
    {%- endif -%}
  </a>
</h1>
```

### Replace with:

```liquid
{%- if request.page_type == 'index' -%}
  <h1 class="header__heading">
{%- else -%}
  <div class="header__heading">
{%- endif -%}
  <a href="/" class="header__heading-link">
    {%- if section.settings.logo != blank -%}
      ...logo image...
    {%- else -%}
      {{ shop.name }}
    {%- endif -%}
  </a>
{%- if request.page_type == 'index' -%}
  </h1>
{%- else -%}
  </div>
{%- endif -%}
```

This keeps H1 on the homepage (where the brand name IS the H1) but uses `<div>` on all other pages, allowing the product/collection title to be the H1.

### Risk: CSS may target `h1.header__heading`. Check `assets/section-header.css` or equivalent.

### Rollback: Restore original `sections/header.liquid` from backup.

---

## Fix: Robots.txt AI Bot Rules

**Problem:** Store's robots.txt doesn't explicitly allow AI search crawlers.

**Fix:** Create `templates/robots.txt.liquid` to extend defaults with AI bot rules.

```liquid
{% comment %}
  Customized robots.txt — allows AI search crawlers for GEO visibility.
  Created by store-fixer. Original defaults preserved.
{% endcomment %}

{% for group in robots.default_groups %}
  {{- group -}}
{% endfor %}

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: {{ shop.url }}/sitemap.xml
```

### Risk: If the store intentionally blocks AI crawlers, this overrides that decision. Always confirm with the user.

### Rollback: Delete `templates/robots.txt.liquid` — Shopify will revert to auto-generated defaults.

---

## Backup

Before ANY theme edit, read the current file and save to the rollback manifest. See [safety-and-rollback.md](safety-and-rollback.md) for the canonical manifest format.

---
name: store-check
description: Shopify store health check — validates theme structure, Liquid files, and config using ~~shopify dev tools
---

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

You are a Shopify store health-check assistant.

When invoked, run through this checklist for the current project:

## 1. Theme Structure

Check if the project has a standard Shopify theme layout:
- `layout/` — theme layouts (theme.liquid)
- `templates/` — page templates
- `sections/` — theme sections
- `snippets/` — reusable snippets
- `assets/` — CSS, JS, images
- `config/` — settings_schema.json, settings_data.json
- `locales/` — translation files

## 2. Liquid Validation

If `~~shopify dev tools` is connected, use it to:
- Run theme checks on any `.liquid` files found
- Report linting errors or warnings
- Flag deprecated Liquid tags or filters

## 3. Config Check

- Look for `config/settings_schema.json` and `config/settings_data.json`
- Validate JSON syntax if found

## 4. Dependencies

- Check if `package.json` exists and list any Shopify-related dependencies (`@shopify/*`, `shopify-*`)

If no Shopify theme files are found, let the user know and confirm the plugin is working correctly.

Arguments: "$ARGUMENTS"

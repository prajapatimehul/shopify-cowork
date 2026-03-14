# Store Fixer Access Setup

## Contents

1. Theme access
2. Admin API access
3. Mixed access
4. Missing-access response

## 1. Theme access

Use theme access for:

- `shopify theme list`
- `shopify theme pull`
- `shopify theme push`
- `shopify theme dev`
- previewing and editing Liquid, sections, snippets, templates, and assets

Shopify theme commands can authenticate with:

- a Shopify account that has store access
- a Theme Access password
- a custom app access token

For client work, prefer one of these:

### Theme Access app

Best when the job is limited to theme code.

Ask the client for:

- store domain, for example `client-store.myshopify.com`
- Theme Access password
- storefront password only if the storefront itself is password protected

Typical commands:

```bash
export SHOPIFY_FLAG_STORE="client-store.myshopify.com"
export SHOPIFY_CLI_THEME_TOKEN="<theme-access-password>"

shopify theme list --password "$SHOPIFY_CLI_THEME_TOKEN"
shopify theme pull --live --path work/client-live --password "$SHOPIFY_CLI_THEME_TOKEN"
shopify theme push --path work/client-live --password "$SHOPIFY_CLI_THEME_TOKEN"
```

Password-protected storefront preview:

```bash
shopify theme dev \
  --path work/client-live \
  --password "$SHOPIFY_CLI_THEME_TOKEN" \
  --store-password "<storefront-password>"
```

Important distinction:

- `--password` is the Theme Access password or CLI auth token for theme commands
- `--store-password` is the storefront password shown to customers

### Collaborator or staff account

Use this when theme work is required and the merchant is willing to grant store access through Shopify accounts.

Important limitation:

- collaborator access is enough for theme work
- collaborator access is not enough to manage Dev Dashboard apps because that requires organization-level permissions

If the client wants us to create or manage the app directly, they need to add us as staff with app-development permissions.

## 2. Admin API access

Use Admin API access for:

- product and collection updates
- page or metafield changes
- bulk authenticated catalog work
- any mutation that is not purely a theme file change

For this project, the safe baseline is a client-owned Dev Dashboard app in the merchant's organization.

Ask the client for:

- store domain
- `client_id`
- `client_secret`
- approved scopes

Common scopes for this project:

- `read_products`
- `write_products`
- `read_themes`
- `write_themes`

Only ask for the scopes required by the task.

Request a short-lived token at the start of each session:

```bash
export SHOPIFY_SHOP="client-store.myshopify.com"
export SHOPIFY_CLIENT_ID="<client-id>"
export SHOPIFY_CLIENT_SECRET="<client-secret>"

curl -X POST "https://$SHOPIFY_SHOP/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=$SHOPIFY_CLIENT_ID" \
  --data-urlencode "client_secret=$SHOPIFY_CLIENT_SECRET"
```

Expected response fields:

- `access_token`
- `scope`
- `expires_in`

Treat the token as session-scoped. Re-fetch it before each work session.

### Scope changes

If new scopes are needed later:

1. update the app version
2. release the new version
3. have the merchant approve the new scopes in admin

Do not assume new scopes are active until the merchant has approved them.

## 3. Mixed access

Use `Mixed` when both channels are required.

Common examples:

- update product content through Admin API and patch theme schema snippets
- fix internal linking in theme code and update collection metadata
- implement analyzer findings that span Liquid, products, and collections

Do not start mixed execution until both access paths are confirmed.

## 4. Missing-access response

If access is missing, do not guess or partially execute hidden steps.

Return:

- exact access path missing: `Theme`, `Admin API`, or both
- exact merchant ask
- exact scopes needed if Admin API is required
- whether execution can continue in `Plan` mode without credentials

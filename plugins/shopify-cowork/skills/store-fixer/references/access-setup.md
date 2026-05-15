# Access Setup

## Admin API (Client Credentials Grant)

The merchant creates a custom app, installs it, and shares credentials.

**Ask the client for:** store domain, `client_id`, `client_secret`, approved scopes.

**Scope reference:**

| Scope | Needed For |
|-------|-----------|
| `read_products` | Query products, collections, media |
| `write_products` | Descriptions, SEO, tags, vendor, images |
| `write_content` | Redirects, article meta tags |
| `write_inventory` | Variant SKUs |
| `read_themes` | Read theme files (Tier 2) |
| `write_themes` | Modify theme files (Tier 2, protected scope) |

Only request the scopes needed for the current task.

**Fetch token (24h expiry):**

```bash
curl -X POST "https://$SHOPIFY_SHOP/admin/oauth/access_token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=client_credentials" \
  --data-urlencode "client_id=$SHOPIFY_CLIENT_ID" \
  --data-urlencode "client_secret=$SHOPIFY_CLIENT_SECRET"
```

Re-fetch at the start of each session.

**Scope changes:** Update `shopify.app.toml`, run `shopify app deploy`, merchant must approve new scopes.

## Theme Access (Alternative for Theme-Only Work)

When the client only grants Theme Access (no Admin API):

```bash
export SHOPIFY_FLAG_STORE="client-store.myshopify.com"
export SHOPIFY_CLI_THEME_TOKEN="<theme-access-password>"

shopify theme pull --live --path work/client-live --password "$SHOPIFY_CLI_THEME_TOKEN"
# edit locally, then push
shopify theme push --path work/client-live --password "$SHOPIFY_CLI_THEME_TOKEN"
```

Note: `--password` = Theme Access token. `--store-password` = storefront password (separate, for password-protected stores).

## Missing Access

If access is missing, switch to Plan mode and return:

```
ACCESS REQUIRED

  Missing: {Admin API / Theme / Both}
  Client needs to:
    1. {exact step}
    2. {exact step}
  Scopes needed: {list}
  I can proceed in Plan mode without credentials.
```

FIX PLAN — {domain}

API ACCESS
  Token: verified  |  Store: {shop_name}  |  Plan: {plan}
  Scopes: {available_scopes}

TIER 1 — Data Fixes (safe, API-only)

  #{n}  {finding title — business language, not technical}
    What:    {what's wrong — one line}
    Count:   {exact number of affected resources}
    Fix:     {what we'll do — one line}
    API:     {mutation name}

  {repeat for each Tier 1 fix}

TIER 2 — Theme Fixes (requires separate approval)

  #{n}  {finding title}
    What:    {what's wrong — one line}
    Risk:    {Low / Medium / High}
    Fix:     {what we'll change in the theme}
    Backup:  {which file will be backed up}

  {only if Tier 2 fixes are requested}

SUMMARY
  Tier 1 fixes: {n} ({total resources affected})
  Tier 2 fixes: {n} (requires write_themes scope)
  Estimated API calls: ~{n}
  Rollback: Full state saved before each batch

Proceed with Tier 1 fixes? (y/n)

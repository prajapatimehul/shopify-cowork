# Store Fixer Testing

## Contents

1. Trigger tests
2. Non-trigger tests
3. Execution tests
4. Plan-only tests
5. Acceptance checks

## 1. Trigger tests

These prompts should trigger the skill:

1. `Fix the issues from this Shopify audit`
2. `Update these product descriptions in Shopify`
3. `Patch robots.txt and schema on this Shopify store`
4. `Implement the top 3 SEO fixes from this analyzer report`
5. `What access do we need before fixing this Shopify store?`
6. `Roll out these collection metadata changes on Shopify`
7. `Make these theme updates on the store but do not push to live yet`
8. `Use Shopify auth to update products and theme schema`

## 2. Non-trigger tests

These prompts should NOT trigger the skill:

1. `Audit this Shopify store for AI visibility` (should trigger `store-analyzer`)
2. `Write product descriptions for my store`
3. `Run competitor research on this niche`
4. `Set up Google Ads for my products`
5. `Build a public Shopify app for multiple merchants`
6. `Analyze my GA4 export`

## 3. Execution tests

1. `Take this analyzer report and implement the top 3 fixes`
Expected: classify each fix channel, confirm access, present the exact change set with rollback, wait for approval, then make only the approved changes and verify.

2. `Fix missing FAQ schema and weak internal linking on this Shopify theme`
Expected: theme-first workflow with approval before push, rollback point, and preview verification.

3. `Update product titles and descriptions for these 20 products`
Expected: Admin API workflow with exact approved object scope, batching, verification, and rollback data.

## 4. Plan-only tests

1. `What credentials do we need before we can fix product SEO and theme schema?`
Expected: no execution, exact access checklist, exact scopes, and smallest next step.

2. `Do not change anything yet. Give me the implementation plan for these fixes.`
Expected: `Plan` mode with channel classification and rollback strategy.

3. `Review these changes and tell me if they were applied correctly.`
Expected: `Review` mode with verification, not blind reimplementation.

## 5. Acceptance checks

A good response should:

- choose `Theme`, `Admin API`, `Mixed`, or `Manual` correctly
- name the exact access missing when blocked
- require explicit approval before any Shopify mutation
- capture or require rollback data before execution
- describe the exact files or objects changed
- include verification evidence
- avoid claiming success without proof
- avoid re-running a full audit when the user already provided the target fixes

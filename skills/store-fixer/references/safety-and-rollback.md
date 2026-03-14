# Store Fixer Safety And Rollback

## Contents

1. Universal checklist
2. Theme checklist
3. Admin API checklist
4. Verification checklist
5. Rollback patterns

## 1. Universal checklist

Before any execution:

- confirm store domain
- confirm mode: `Execute`, `Plan`, or `Review`
- confirm access path
- confirm exact scope of objects or files to change
- present the exact proposed change set to the user
- get explicit user approval before any mutation
- capture a rollback point
- avoid mixing unrelated fixes into the same push or mutation batch

Execution must not start unless all three are true:

- the user approved the exact scope
- rollback data is captured
- the target surface and verification method are known

## 2. Theme checklist

Before theme edits:

- identify the target theme ID and whether it is live or unpublished
- pull the latest theme state locally before editing
- tell the user which theme and which files will be changed
- keep the diff focused on the requested fix
- prefer testing on an unpublished theme or preview when the risk is moderate or high

Suggested baseline flow:

```bash
export SHOPIFY_FLAG_STORE="client-store.myshopify.com"
shopify theme list
shopify theme pull --live --path work/client-live
```

After edits:

- inspect the diff
- preview rendered pages
- push only the intended changes

Before push:

- confirm the push matches the approved scope
- stop if additional file changes became necessary and ask for approval again

## 3. Admin API checklist

Before Admin API mutations:

- confirm token and scopes
- fetch the current object data
- store the fields needed for rollback
- define the exact object count
- tell the user the exact objects and fields that will be mutated
- use batches for larger updates instead of one uncontrolled burst

For bulk work:

- start with a small sample
- verify the sample result
- continue only if the sample is correct

If the mutation target changes during execution, stop and ask for approval again.

## 4. Verification checklist

Theme verification:

- preview URL loads
- target pages render correctly
- HTML or structured data reflects the intended change
- no obvious template regressions on adjacent pages

Admin API verification:

- follow-up read confirms the updated field values
- storefront rendering reflects the new data where relevant
- object count changed matches the intended scope

Mixed verification:

- verify data objects first
- verify storefront rendering second
- verify at least one unaffected page to catch spillover regressions

## 5. Rollback patterns

Theme rollback:

- keep the pre-change theme pull or git diff
- revert the local change and push the revert
- if needed, switch the merchant back to the prior theme version or unpublished copy

Admin API rollback:

- reapply the captured pre-change values to the same objects
- keep object IDs and original fields together so restoration is deterministic

If rollback data was not captured, say that clearly and stop broad execution until a safer process is in place.

If rollback is not possible for the requested operation, do not execute it from this skill.

---
name: Goal usage report
about: Record final persistent-goal usage as evidence for future goal sizing
title: "Goal usage: "
labels: "goal-usage"
assignees: ""
---

<!-- fspp-issue-contract:v1 type=goal-usage-report -->

<!-- fspp-goal-usage:v1 -->

<!-- Keep existing reports on their original version. Changing a required
heading, field, or field meaning requires a new schema version. -->

## Objective

Preserve one persistent goal's final usage and outcome shape so comparable
future goals can be sized with evidence and human judgment.

## Governing sources

- Owning issue or milestone tracking issue:
- Goal completion result:
- Relevant closeout records:

## Scope

- One final `complete` or `blocked` persistent goal.
- One immutable issue or milestone goal scope.

## Suggested branch prefix

No branch is required. This issue is the durable usage record.

## Exclusions

- This report is not a productivity score, quota, estimate guarantee, or acceptance decision.
- Do not compare unlike goal scopes or materially different risk cohorts.

## Constraints and invariants

- Copy exact final usage from the goal completion result; do not estimate it.
- Keep the owner as the authority for intent, implementation, evidence, and closeout.
- Keep the schema marker, required headings, and field labels unchanged.
- Derive a sizing signal only after at least three comparable records exist.

## Expected evidence

- [ ] All required fields contain final values.
- [ ] Counts can be reconciled with the owner, PRs, and closeouts.
- [ ] The qualitative assessment explains coherence, coordination, risk, and uncertainty.
- [ ] `summarize-goal-usage` accepts the record.

## Permissions

- May link existing repository issues, PRs, and goal completion values.
- Must not revise the owning contract or substitute this report for human closeout.

## Stopping conditions

Stop if exact final usage is unavailable, the owner cannot be identified, or
recording the report would require changing the completed goal's scope.

## Goal identity

- Goal scope: <!-- issue | milestone -->
- Owner:
- Goal objective:
- Final status: <!-- complete | blocked -->
- Completed at: <!-- ISO 8601 timestamp -->

## Final usage

- Tokens used: <!-- non-negative integer -->
- Token budget: <!-- non-negative integer | not set -->
- Elapsed seconds: <!-- non-negative integer -->

## Outcome shape

- Child issues completed: <!-- non-negative integer -->
- Pull requests merged: <!-- non-negative integer -->
- Human closeouts: <!-- non-negative integer -->
- Risk and uncertainty: <!-- low | medium | high -->

## Sizing assessment

- Assessment: <!-- undersized | right-sized | oversized | inconclusive -->

<!-- Explain whether the goal remained one coherent outcome, where coordination
or uncertainty accumulated, and why the assessment follows from that evidence. -->

## Future sizing recommendation

<!-- State what should be retained or changed for the next comparable goal. Keep
coherence and preserved intent more important than hitting a numeric target. -->

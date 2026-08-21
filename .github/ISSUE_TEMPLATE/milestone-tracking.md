---
name: Milestone tracking
about: Lightweight tracker for milestone state, child issues, and follow-on readiness
title: "Track <milestone name>"
labels: "tracking, project"
assignees: ""
---

<!-- fspp-issue-contract:v1 type=milestone-tracking -->

## Objective

What milestone outcome does this issue track?

## Governing sources

- 

## Scope

This issue tracks milestone state. Child issues remain the bounded task
contracts for implementation, discovery, decision, or evidence work.

Child issues:

- [ ] #

## Suggested branch prefix

Use `project/` for milestone tracking and project-governance work.

## Exclusions

- Do not use this tracking issue as a substitute for child task contracts.
- Do not implement feature, extraction, model, or publication behavior here.
- Do not approve source-derived artifacts, claim promotion, or public release from this tracker alone.

## Constraints and invariants

- Keep this issue as a lightweight milestone map.
- Update the checklist as child issues close, move, or change scope.
- Keep unresolved uncertainty visible instead of forcing premature decisions.

## Expected evidence

- [ ] Child issues are closed, moved, or explicitly deferred.
- [ ] Project docs reflect resolved decisions and remaining open questions.
- [ ] Follow-on issues are ready to create from the resulting knowledge.

## Permissions

- May update this checklist and milestone notes.
- May add or remove child issue links when milestone scope changes.
- Must not use this issue to expand child issue scope silently.

## Stopping conditions

Stop and ask if milestone scope expands into feature implementation, release or
export decisions, source-rights risk acceptance, codebook semantics, or claim
promotion.

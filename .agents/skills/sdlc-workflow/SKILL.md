---
name: sdlc-workflow
description: "Use when Codex or Claude needs to manage software development lifecycle work in this repo: persistent milestone- or issue-scoped goals, intent checkpoints, human closeout, branches, commits, pull requests, review, merge, issue closure, or milestone tracking. Treat sdlc, sldc, and $sdlc-workflow as explicit triggers."
---

# SDLC Workflow

Use this skill to keep FSPP Research Workbench GitHub work consistent,
reviewable, and easy to audit.

## Repository Defaults

- GitHub repo: `ashitaka-emishi/fspp-research-wrokbench`
- Default branch: `master`
- Repository visibility: public unless the maintainer chooses otherwise before push
- Runtime language: Python package with Quarto publication site
- Python namespace: `fspp_workbench`
- CLI: `fspp`
- Full local validation:

```bash
uv run ruff check .
uv run pytest
uv run fspp schema check
uv run fspp validate
make site
```

Follow `AGENTS.md` first. Use it when deciding scope, rigor, review depth,
human authority, and whether evidence is sufficient.

For nontrivial issue work, consult the governing sources in this order:

1. `projects/sacrificial-debt/research/` and the versioned codebook for
   Sacrificial Debt definitions.
2. `docs/architecture/` for shared infrastructure boundaries.
3. `docs/design/` for accepted design context and migration rationale.
4. `publication/` for Quarto publication structure.
5. Tests and `fspp` validation output for executable guardrails.

Do not treat `.gitignore` as a source-rights or confidentiality policy
mechanism. Keep generated outputs under their designated generated/output
directories and ensure they remain rebuildable from canonical sources.

## Operating Principles

- Start from a GitHub issue or milestone whenever possible.
- Begin with purpose and evidence: identify the observed need and expected
  outcome before choosing an implementation.
- Prefer one issue per branch and one branch per pull request.
- Keep scope narrow; create follow-up issues for new work discovered along the
  way.
- Build the smallest coherent change that can be reviewed and verified.
- Preserve unrelated user changes in the working tree.
- Make human authority explicit for source-rights decisions, codebook semantics,
  claim promotion, accepted risk, external distribution, and release readiness.
- Surface uncertainty visibly instead of silently accepting ambiguous evidence,
  conflicting requirements, or failed validation.
- Update relevant `tracking` issues when child issues close or change
  order/status.
- Open pull requests as ready for review, not draft.
- Keep a human control point between pull request creation and merge. Do not
  merge or close issues unless the user explicitly asks for that workflow or has
  clearly delegated it.
- Before closing issue-directed SDLC work, record exactly one marked closeout
  comment on the GitHub issue using `.github/ISSUE_CLOSEOUT_TEMPLATE.md`. Plain
  PR comments are useful review notes, but they are not issue closeout records
  and are not counted by the milestone helper.
- Use squash merge for pull requests unless the user explicitly overrides this
  rule for a specific PR.

## Command Interpretation

Treat `sdlc`, `sldc`, and `$sdlc-workflow` as requests to use this workflow.
`sldc` is an accepted shorthand/typo, not a reason to ask for clarification.

Issue-number commands are issue-directed workflow requests:

```text
sdlc <issue-number>
sldc <issue-number>
sdlc implement issue <issue-number>
use sdlc to finish #<issue-number>
```

Multi-issue commands are ordered batch workflow requests. Interpret
comma-separated issue numbers and inclusive ranges as an ordered list,
preserving the user's order:

```text
sdlc 12-14,18
sldc 7,9,10
```

For a multi-issue request, do each issue completely before starting the next
one. The batch request is explicit merge/close delegation for every listed issue
unless the user adds a narrower instruction. Stop the batch if checks fail,
review blocks the PR, the issue is ambiguous, or the user interrupts.

`sdlc next` and `sldc next` are selection requests, not implementation approval.
Inspect open issues and relevant milestone ordering, recommend the next issue,
explain the selection briefly, and stop for user confirmation before branching
or editing files.

When an active persistent goal governs milestone or issue SDLC work, or the user
asks for goal-scoped SDLC, read [`references/goal-workflow.md`](references/goal-workflow.md)
before creating issues, editing files, merging, or closing. Keep the declared
`milestone` or `issue` scope immutable. The goal is execution context; the
milestone tracker or issue contract owns durable intent.

For any issue-directed request, first collect deterministic state for the issue
and choose the smallest correct continuation:

- If the issue is open and no implementation branch or PR exists, start issue
  work.
- If a branch exists, inspect local/remote branch state and continue from it
  when safe.
- If an open PR exists, inspect PR status, checks, review comments, and remaining
  scope before changing code.
- If the issue is already closed, report the closure state and do not create new
  work unless the user asks to reopen or follow up.

## Bounded Task Contract

Before nontrivial implementation, identify or create a task contract in the
issue, prompt, plan, or PR description:

- Objective: desired outcome.
- Governing sources: specifications, requirements, decisions, source evidence,
  examples, or issue reproduction.
- Scope and exclusions: what may change and what must not change.
- Constraints and invariants: behavior, architecture, source-rights, data,
  validation, compatibility, and branch rules.
- Expected evidence: tests, commands, source review, site render evidence, or
  human review.
- Permissions: dependency installs, network, generated artifacts,
  source-derived data, Quarto publication changes, or external services.
- Stopping conditions: conflicting sources, missing authority, failed checks,
  destructive actions, or unverifiable results.

Stop and report when the contract cannot be satisfied without expanded scope or
authority.

## Dual Authority And Conflict Handling

Treat specifications, requirements, decisions, and accepted examples as intended
behavior. Treat accepted code, data, and generated artifacts as current
behavior.

When they disagree, classify the mismatch before changing files:

- Implementation defect: fix implementation to satisfy accepted intent.
- Specification defect: revise the governing source with human judgment.
- Unresolved ambiguity: keep the conflict visible and seek evidence.
- Accepted limitation: document the gap, impact, and accepted risk.

## Deterministic Helpers

Run the state helper before creating a branch, editing files, opening a PR,
addressing review, or merging issue-directed work:

```bash
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py inspect-issue <issue-number> --repo ashitaka-emishi/fspp-research-wrokbench --cwd .
```

Use `--json` when the next step needs machine-readable output. Treat the helper
output as the factual baseline for issue state, contract schema, marked closeout,
local status, matching local/remote branches, open PRs, PR checks, review
decision, and same-milestone `tracking` issues. If the helper reports unavailable
state, stop and report the exact unavailable command instead of inventing state.

Inspect milestone contract, child, closeout, and acceptance facts with:

```bash
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py inspect-milestone <milestone-number> --repo ashitaka-emishi/fspp-research-wrokbench --cwd .
```

Summarize completed goal-usage records by comparable scope and risk with:

```bash
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py summarize-goal-usage --repo ashitaka-emishi/fspp-research-wrokbench --scope milestone --risk high
```

The command reports min/median/max observations but withholds a sizing signal
until three comparable records exist. Treat any resulting signal as input to
human judgment, never as a quota, productivity score, or automatic scope rule.

Validate all versioned issue-contract and closeout templates with:

```bash
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py validate-templates --root .
```

For tracker updates after merge, format checklist entries with:

```bash
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py tracker-entry <issue-number> --title "<issue title>" --state closed --url "<issue URL>"
```

When creating a new milestone, create one tracking issue from
`.github/ISSUE_TEMPLATE/milestone-tracking.md`, apply the `tracking` label, and
list child issues as checklist items. The tracking issue owns the coherent
milestone outcome, boundaries, acceptance evidence, and closeout obligation;
its checklist is only a state view. Keep implementation, discovery, decision,
and evidence contracts in child issues rather than in the tracker.

## Start Issue Work

1. Run `sdlc_state.py inspect-issue` for the issue.
2. Read the issue, linked tracking issue, milestone, and helper continuation.
3. Use the helper's local status and branch report to avoid duplicating existing
   issue branches.
4. If work needs code or docs changes, create a branch from `master`.
5. Name the branch by issue type:
   - `fix/<issue-number>-<short-slug>`
   - `feature/<issue-number>-<short-slug>`
   - `docs/<issue-number>-<short-slug>`
   - `chore/<issue-number>-<short-slug>`
   - `project/<issue-number>-<short-slug>` for discovery, decisions,
     requirements, acceptance criteria, milestone planning,
     issue-template/process work, and other project-governance changes.

## Implement

1. Inspect relevant files before editing.
2. Preserve intent: if implementation changes a consequential design decision,
   update the design deliberately.
3. Make the smallest coherent change that satisfies the issue.
4. Keep intent, implementation, and evidence distinguishable in code, docs, and
   data.
5. Keep generated artifacts separate from source edits.
6. Keep reusable behavior in `src/fspp_workbench`; keep scripts thin.
7. Preserve provenance, stable IDs, rights metadata, and research/source
   boundaries for corpus records, evidence, annotations, claims, publications,
   and exports.
8. Run validation scaled to scope, risk, and uncertainty.

Full validation is:

```bash
uv run ruff check .
uv run pytest
uv run fspp schema check
uv run fspp validate
make site
```

For SDLC helper or template-schema changes, also run:

```bash
python3 -m unittest discover -s .agents/skills/sdlc-workflow/tests -p 'test_*.py'
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py validate-templates --root .
```

Run the full command for changes to source code, scripts, data, patches,
resource manifests, or tests. For documentation-only changes, at minimum run
`git diff --check`; run full validation when docs describe executable behavior,
schemas, resource policy, or release gates.

When a change alters research policy, provenance rules, codebook semantics,
architecture decisions, validation/release behavior, public-facing project
state, or user-facing documentation, check whether the Quarto static site needs
a lock-step update. If publication should not change, record that explicitly in
the PR. If publication should change, update the relevant `publication/` page in
the same PR and run `make site`.

## Pre-PR Review

Before opening a pull request, perform a code review over the intended PR diff.
Use the standard review stance: prioritize bugs, behavioral regressions, broken
validation, missing tests, schema drift, source-provenance gaps, and
documentation mismatches.

Review should also ask whether the change preserved purpose, intent, evidence,
human authority, and visible uncertainty. Do not treat more artifacts as better
by default; keep only artifacts that constrain consequential action, record a
meaningful decision, provide useful evidence, or reduce material risk.

Review must also check static-site parity: public-facing research, provenance,
codebook, architecture, validation, or project-status changes should either be
reflected in the relevant Quarto page or explicitly deferred with a reason.

Handle findings before PR creation:

1. Fix actionable in-scope findings with the smallest change.
2. Re-run validation scaled to the fix.
3. Run another review when fixes are non-trivial, touch shared behavior, change
   validation, or alter generated artifacts.
4. File separate GitHub issues for valid out-of-scope findings when they should
   not be solved in the PR.

## Commit

1. Review the diff before staging.
2. Stage only files that belong to the issue.
3. Use a concise imperative commit message.
4. Mention the issue number in the commit body when helpful.
5. Add exactly one AI co-contributor trailer when an AI agent materially
   performed the work:
   - Codex: `Co-authored-by: OpenAI Codex <codex@openai.com>`
   - Claude: `Co-authored-by: Claude <noreply@anthropic.com>`
   - Do not use a generic AI trailer.
   - Do not include both Codex and Claude unless both materially contributed to
     the same commit.

## Open A Pull Request

1. Push the branch.
2. Confirm the pre-PR review has run and actionable findings are fixed or
   explicitly deferred.
3. Open a ready PR, not a draft PR.
4. Include:
   - linked issue, using `Closes #N` only when merge should close it;
   - summary of changes;
   - validation commands and results;
   - static-site/publication consequence;
   - known limitations or follow-up work;
   - any unresolved uncertainty or accepted risk.
5. Stop after PR creation unless the user explicitly asks to merge. In a
   multi-issue command, the batch request itself is merge authorization.
6. For goal-scoped work, complete the paired human closeout in
   `references/goal-workflow.md` before merge even when merge was otherwise
   delegated.

## Address Review

1. Read review comments and classify each as actionable, question, or out of
   scope.
2. Fix actionable items with the smallest change.
3. Re-run relevant validation.
4. Run another review pass when fixes are complex, risky, or touch areas not
   covered by the original review.
5. Push a follow-up commit.
6. Reply or summarize what changed, especially for comments not fully addressed.

## Merge And Close

Only do this when the user explicitly asks, except for multi-issue batch
commands where merge/close is already delegated.

For issue-directed work, re-inspect the issue and require exactly one valid
marked closeout comment on the GitHub issue before merge and issue closure. Use
`.github/ISSUE_CLOSEOUT_TEMPLATE.md`; fill in the human approver, acceptance
time, accepted result, evidence reconciliation, remaining uncertainty, and the
explicit final state change authorized by the user. A PR comment without the
`fspp-closeout` marker does not satisfy closeout. A batch or persistent goal may
authorize implementation, but it does not replace human closeout. Require
explicit authorization for the final state change after closeout acceptance.

1. Run `sdlc_state.py inspect-issue` again.
2. Confirm the PR is approved or the user wants to merge despite pending review.
3. Post the issue closeout comment, or verify the existing issue closeout is
   valid with `sdlc_state.py inspect-issue`.
4. Confirm required checks and relevant local validation passed, or report any
   skipped checks.
5. Merge with squash merge.
6. Confirm linked issues closed as expected.
7. Update open same-milestone issues labeled `tracking` when applicable.
8. Suggest the next recommended ticket without starting it, unless an accepted
   milestone-scoped goal already delegates continuation after closeout.

## If Blocked

Report the exact blocker, what was verified, and the smallest next action. Do
not invent branch, PR, merge, review, or issue state; check GitHub or local Git
first.

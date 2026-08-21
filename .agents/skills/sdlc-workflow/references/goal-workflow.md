# Goal-Scoped SDLC

Use this workflow when a persistent goal governs FSPP Research Workbench milestone or issue work.
Treat the goal as task-local execution state. Keep durable intent in GitHub and
the governing project knowledge base.

## Establish Scope And Intent

1. Classify the goal as `milestone` or `issue` scoped before execution.
2. If scope is missing, ask one question, explain why the choice matters, offer
   ranked options with a recommendation, and allow a free-text answer.
3. Keep the selected scope immutable. Stop or start a new goal when the work
   would cross from milestone to issue scope or the reverse.
4. For milestone scope, run `sdlc_state.py inspect-milestone` and use the
   tracking issue as the durable milestone contract. Treat its checklist as a
   state view, not the milestone definition.
5. For issue scope, run `sdlc_state.py inspect-issue` and use the issue body as
   the durable task contract.
6. Preserve the initial intent. Record human-approved refinements separately;
   do not rewrite the starting point or rely on goal edits as project history.

Do not let a goal broaden repository permissions, merge authority, risk
acceptance, source-rights authority, or release authority.

## Resolve Consequential Design

Ask only for choices that materially change intent, architecture, scope,
constraints, evidence, authority, or closeout. Ask one question at a time. For
each question:

1. Explain why the decision matters.
2. Give rank-ordered options with the recommendation first.
3. Include a free-text alternative.
4. Restate the accepted decision before moving on.

Prune brainstorming. Retain an idea only when it constrains consequential
action, records a meaningful decision, provides evidence, or reduces material
risk or misunderstanding.

## Check Intent During Work

Run a concise intent check:

- after planning and before implementation;
- after consequential discoveries, uncertainty, or scope pressure;
- before opening the final PR when the implementation materially changed; and
- before merge, issue closure, or milestone closure.

Compare preserved intent and approved refinements with the current plan, diff,
and evidence. Classify the result as aligned, drift, or new knowledge. Correct
drift, obtain a human-approved refinement, or stop. Add checkpoints only when
risk or uncertainty warrants them.

## Execute A Milestone Goal

1. Verify that the tracker states a coherent outcome, governing sources,
   boundaries, acceptance evidence, permissions, and stopping conditions.
2. Create the smallest ordered child issues needed to achieve and verify that
   outcome. Keep each child as its own bounded contract.
3. Implement one child issue at a time through a ready PR.
4. Stop for the child issue's human closeout before merge, even when the goal
   delegates creation and implementation of the full milestone sequence.
5. After authorized merge, update the tracker with `tracker-entry`, inspect the
   milestone again, and continue to the next accepted child.
6. When child issues are closed or explicitly deferred, verify the milestone
   outcome and acceptance evidence. Child disposition alone is insufficient.
7. Perform human milestone closeout on the tracking issue before requesting
   authorization to close the tracker or GitHub milestone.

## Execute An Issue Goal

Follow the normal issue workflow through a ready PR. Preserve the issue body as
the initial contract. Append approved refinements in comments or durable project
sources instead of rewriting the issue. Stop for human closeout before merge.

## Perform Human Closeout

Review first and publish once:

1. Prepare the closeout from `.github/ISSUE_CLOSEOUT_TEMPLATE.md` after the
   implementation, PR, and verification evidence exist.
2. Compare intended and achieved outcome, planned and actual design, preserved
   or changed constraints, and proposed and reconciled decisions.
3. Trace consequential intent claims to implementation and verification
   evidence. Treat tests as evidence, not the source of intent.
4. Classify candidate knowledge as `promote`, `already captured`, `defer`, or
   `discard`. Promote retained knowledge to its existing authoritative source.
5. State remaining uncertainty, limitations, and residual risk.
6. Resolve consequential differences with the human one question at a time.
7. Obtain explicit human acceptance and separate authorization for the final
   state change.
8. Post one final comment containing `<!-- fspp-closeout:v1 -->`; do not post
   draft closeout comments or mutate the initial issue contract.
9. Re-run deterministic state inspection, then perform only the authorized
   merge or milestone closure.

Stop when the contract is unavailable or invalid, evidence cannot support the
claimed outcome, closeout markers are missing or duplicated, sources conflict,
scope would change, or human authority is required and absent.

## Record Final Goal Usage

After the persistent goal reaches its final `complete` or `blocked` state and
the runtime returns exact usage, create one standalone issue from
`.github/ISSUE_TEMPLATE/goal-usage-report.md`. Apply `goal-usage`, do not assign
a milestone, validate the completed report, and close it as a finished evidence
record. Link the owning issue or milestone tracker; that owner remains the
authority for intent, implementation, evidence, and human closeout.

Copy exact tokens, elapsed seconds, and any explicit budget from the final goal
result. Reconcile outcome counts with GitHub state. Add a short human-readable
assessment of scope coherence, coordination, risk, and uncertainty. Do not
estimate missing runtime values or reopen the owner merely to add telemetry.

Use `summarize-goal-usage` to compare only like goal scopes and risk cohorts.
Require at least three comparable records before treating the summary as a
sizing signal. Use medians, ranges, qualitative assessments, and the history of
blocked goals together. The signal may suggest retaining, shrinking, or
combining a future coherent scope, but it must not become a productivity score,
hard quota, automatic split, acceptance gate, or substitute for human judgment.

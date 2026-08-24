# AGENTS.md — Mandatory Research-Engineering Rules

These instructions apply to Codex and every AI coding/research agent working in this repository.

## 0. Agent routing and SDLC workflow

Codex is the primary AI coding agent for this repository. Claude AI may be used
as a backup agent, but it must follow these same repository rules and the same
SDLC workflow.

When the user types `sdlc`, `sldc`, or `$sdlc-workflow` — with or without a
following issue number, issue range, or `next` — read and follow
`.agents/skills/sdlc-workflow/SKILL.md` in full before taking action.

Important SDLC defaults:

- `sdlc next` / `sldc next`: inspect open issues and milestone ordering,
  recommend the next issue, and stop for user confirmation before branching or
  editing anything.
- `sdlc <N>` / `sldc <N>`: run the state helper first, determine the smallest
  correct continuation, then proceed according to the skill.
- State helper:

```bash
python3 .agents/skills/sdlc-workflow/scripts/sdlc_state.py inspect-issue <N> --repo ashitaka-emishi/fspp-research-wrokbench --cwd .
```

- Codex-authored commits use:
  `Co-authored-by: OpenAI Codex <codex@openai.com>`
- Claude-authored commits use:
  `Co-authored-by: Claude <noreply@anthropic.com>`
- Open PRs as ready, not draft. Do not merge or close issues without explicit
  user instruction, except for a multi-issue SDLC batch where the skill treats
  the batch request as delegated merge/close authority.
- Use squash merge only unless the user explicitly overrides it for a specific
  PR.

## 1. Authority order

1. `projects/sacrificial-debt/research/` and the versioned codebook are authoritative for substantive Sacrificial Debt definitions.
2. `docs/architecture/` is authoritative for infrastructure boundaries.
3. Tests encode non-negotiable methodological guardrails.
4. AI suggestions never silently change research theory, categories, or historical annotations.

When requirements conflict, **stop changing semantics and record the conflict in the decision log**.

## 2. Separation of concerns

Shared `fspp_workbench` infrastructure may know how to store, validate, version, compare, audit, and publish evidence. It must not contain Sacrificial Debt-specific theoretical categories except generic extension interfaces.

Project-specific theory belongs under:

- `src/fspp_workbench/projects/sacrificial_debt/`
- `projects/sacrificial-debt/research/`
- `projects/sacrificial-debt/codebook/`

Never import `fspp_workbench.projects.*` from shared modules.

## 3. Manual-first research rule

Do not implement large-scale LLM/NLP extraction as the primary coding path until the manual pilot, codebook stabilization, and reliability gates are met.

Permitted early automation:

- ingestion and provenance checks;
- normalization/segmentation;
- candidate retrieval;
- lexical concordance;
- QC and consistency checks;
- reliability calculations;
- evidence-chain/claim-audit generation;
- reproducible tables and publication builds.

AI may **review** reference annotations but may not overwrite them.

## 4. Identification before interpretation

Sacrificial Debt annotations use a state machine. Interpretive fields must not become analyzable reference evidence until observable textual structure is reviewed and locked.

Do not collapse:

- sacrificial asymmetry into debt;
- behavior into essentialization;
- rhetoric into reception;
- rhetoric into policy causation;
- coercive severity into sacrificial-debt framing;
- model agreement into human reliability;
- Tier 3 hits into coded evidence.

## 5. Evidence and falsification

A strong Sacrificial Debt annotation requires the project codebook's minimum evidence rule. Never infer debt merely from hostility, casualties, persecution, or generic sacrifice praise.

Negative evidence, exceptions, absence searches, rival explanations, and chronology contradictions are first-class records. A workflow that makes confirming evidence easier to store than disconfirming evidence is a bug.

## 6. Stable IDs and immutability

Released identifiers are permanent. Never renumber an ID because ordering changed.

For splits/merges/corrections:

- preserve old records;
- mark supersession explicitly;
- create new IDs;
- preserve the relation in lineage metadata.

Reference annotations that entered a release are append-only/superseded, not destructively edited. Model/human review and adjudication preserve original values.

## 7. Canonical vs generated

Canonical data live under `projects/sacrificial-debt/data/`, corpus/provenance manifests, research files, and codebook files.

Generated outputs live under `projects/sacrificial-debt/generated/` and must be rebuildable. Never hand-edit generated output as a source of truth.

## 8. Source integrity

Every proposition must resolve to exact source coordinates. Every source must carry provenance and checksum metadata. High-value translated evidence must preserve the original-language text.

Do not invent missing bibliographic or archival fields. Use explicit unknown/uncertain states where allowed.

## 9. Historical sensitivity

The project includes Holocaust/genocide material. Do not:

- represent victims as voluntary sacrificial participants when they were subjected to violence;
- equate combat death with genocide;
- reproduce perpetrator moral logic as project endorsement;
- turn Sacrificial Debt into a total explanation of the Holocaust;
- strip quotations from provenance/context;
- hide speculative inference;
- confuse actor claims with researcher conclusions.

## 10. Code changes

Before completing a change:

```bash
uv run ruff check .
uv run pytest
uv run fspp schema check
uv run fspp validate
```

For Quarto publication or navigation changes, also run:

```bash
make site
```

When a PR changes research policy, provenance rules, codebook semantics,
architecture decisions, validation/release behavior, public-facing project
state, or user-facing documentation, check whether the Quarto static site needs
a lock-step update. If the site should not change, state that explicitly in the
PR. If it should change, update the relevant `publication/` page in the same PR
and run `make site`.

Add tests for new methodological constraints. Prefer semantic module names over numbered pipeline stages. Keep scripts thin; reusable logic belongs in `src/fspp_workbench`.

## 11. Pull requests

Every PR touching research data, schemas, or codebook semantics must state:

- research consequence;
- data/schema migration consequence;
- reproducibility consequence;
- static-site/publication consequence;
- whether existing released records change meaning;
- tests/validation run.

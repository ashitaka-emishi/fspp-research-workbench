# Contributing

Thank you for helping improve the FSPP Research Workbench. This repository combines research software, evidence infrastructure, project-specific theory, and publication tooling, so contributions need to preserve both engineering quality and methodological guardrails.

## Start Here

Read these before making substantive changes:

1. `AGENTS.md`
2. `README.md`
3. `docs/architecture/FSPP_RESEARCH_WORKBENCH_PRINCIPLES.md`
4. `projects/sacrificial-debt/research/RESEARCH_AUTHORITY.md`
5. `projects/sacrificial-debt/codebook/CODEBOOK.md`

## Local Setup

```bash
uv venv .venv --python 3.14
uv sync --all-extras
```

## Required Checks

Run these before opening a pull request:

```bash
uv run ruff check .
uv run pytest
uv run fspp schema check
uv run fspp validate
```

For website changes, also run:

```bash
make site
```

## Issues

Use the Markdown issue templates under `.github/ISSUE_TEMPLATE/`. They contain
the versioned `fspp-issue-contract` marker and required SDLC headings used by
the repository helper. Do not use ad hoc issue forms for tracked SDLC work.

## Research Boundaries

- Shared infrastructure belongs under `src/fspp_workbench/`.
- Project-specific theory belongs under project modules, research files, and codebooks.
- Shared infrastructure must not import `fspp_workbench.projects.*`.
- AI/model output may review but must not overwrite reference annotations.
- Generated outputs must remain rebuildable and must not become canonical evidence.

## Pull Requests

Every PR that touches research data, schemas, codebook semantics, or publication claims must state:

- research consequence;
- data/schema migration consequence;
- reproducibility consequence;
- static-site/publication consequence;
- whether existing released records change meaning;
- tests and validation run.

If a requested change conflicts with authoritative research files or codebook definitions, stop and record the conflict as a research-engineering decision rather than silently changing semantics.

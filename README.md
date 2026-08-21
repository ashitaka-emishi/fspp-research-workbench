# FSPP Research Workbench

This repository is the **reusable research environment** for the Foundation for the Study of Political Pathology. It begins with the **Sacrificial Debt** research program, but its shared infrastructure is intentionally project-agnostic so that Lincoln, Sacrifice Law, and future projects can converge on one auditable research architecture.

Website: <https://ashitaka-emishi.github.io/fspp-research-wrokbench/>

Repository: <https://github.com/ashitaka-emishi/fspp-research-wrokbench>

## Why this repo exists

Earlier digital-humanities and computational research projects established useful patterns—stable corpus IDs, provenance registries, reliability passes, adjudication, evidence chains, claim audits, Quarto publication, and release gates. This scaffold turns those lessons into reusable infrastructure rather than rebuilding them per project.

The governing principle is:

> **The shared layer knows how to register and audit evidence; project modules define what the evidence means.**

## Start here

### Requirements

- Python 3.14+
- Node.js 24.19.0, the current LTS line
- [uv](https://docs.astral.sh/uv/) recommended
- Quarto for publication rendering (optional until publication work begins)
- Git

### Bootstrap

```bash
uv venv .venv --python 3.14
uv sync --all-extras
uv run fspp doctor
uv run fspp schema build
uv run fspp validate
uv run pytest
```

`uv` should create and use the project-local `.venv/`. The directory is intentionally ignored by Git; commit `.python-version`, `pyproject.toml`, and the lockfile when one is generated, not the environment itself.

If you prefer standard Python:

```bash
python3.14 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e '.[dev]'
fspp doctor
pytest
```

### Open in VS Code

```bash
code .
```

Then read, in order:

1. `AGENTS.md` — mandatory instructions for Codex/AI agents.
2. `docs/architecture/FSPP_RESEARCH_WORKBENCH_PRINCIPLES.md` — architectural lessons carried forward.
3. `projects/sacrificial-debt/README.md` — project-specific entry point.
4. `projects/sacrificial-debt/research/` — frozen substantive research definitions.
5. `projects/sacrificial-debt/codebook/` — coding rules and decision log.

For contribution and repository governance:

- `CONTRIBUTING.md`
- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `SUPPORT.md`

## Repository map

```text
src/fspp_workbench/                           reusable research infrastructure
src/fspp_workbench/projects/sacrificial_debt/ Sacrificial Debt domain logic
projects/sacrificial-debt/                    research corpus, canonical data, codebook, analysis
publication/                                  top-level Quarto website shell
publication/engineering/                      Engineering Quarto subsite
publication/projects/sacrificial-debt/        Sacrificial Debt Quarto subsite
schemas/                                      checked-in generated JSON Schema
scripts/                                      thin developer entry points only
tests/                                        infrastructure + methodological guardrail tests
docs/                                         architecture, ADRs, methods, migration notes
.github/                                      CI and contribution templates
```

## Architectural rules

- Canonical research data are version-controlled JSONL/text/manifests.
- Generated DuckDB/Parquet/tables/site output are derivatives and may be deleted/rebuilt.
- Reference human annotations are immutable after release.
- AI/model review is derivative review evidence, never the reference layer.
- Corpus tiers have explicit evidentiary permissions.
- Proposition is the principal interpretive unit for Sacrificial Debt.
- Identification is locked before interpretation.
- Negative/falsifying evidence is first-class data.
- Rhetoric, reception, and policy are separate evidence domains.
- Claims link to supporting, contradicting, and qualifying evidence.
- Published outputs require a run manifest.

## First milestone

The scaffold is intentionally **manual-first**. Milestone 1 is not automated extraction. It is:

1. register a small Tier 1 corpus;
2. preserve source provenance and checksums;
3. normalize/segment reproducibly;
4. create stable proposition IDs;
5. manually code observable Layer A;
6. lock observation;
7. manually code interpretive Layers B–G;
8. capture negative evidence and rivals;
9. build evidence chains and claim records;
10. reproduce the first controlled tables/site pages.

See `projects/sacrificial-debt/BACKLOG.md`.

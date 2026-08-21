# Sacrificial Debt Workbench

**Research program:** *Sacrificial Debt: How Unequal Suffering Turns Survival into Political Guilt*

This directory contains the project-specific research assets. Shared infrastructure lives in `src/fspp_workbench/`. The rendered publication pages for this project live in the top-level Workbench website under `publication/projects/sacrificial-debt/`.

## Research sequence

```text
source acquisition
→ provenance
→ corpus registration
→ normalization
→ stable segmentation
→ proposition definition
→ manual observation coding
→ observation lock
→ theoretical interpretation
→ negative evidence + rivals
→ reliability/model review
→ adjudication
→ evidence chains
→ controlled analysis
→ process tracing
→ claim audit
→ publication
```

## Day-one workflow

1. Read `research/RESEARCH_AUTHORITY.md`.
2. Review `codebook/CODEBOOK.md` and `codebook/DECISION_LOG.md`.
3. Add sources to `data/sources.jsonl` and corpus provenance manifests.
4. Add documents/segments/propositions with stable IDs.
5. Manually code observation-layer annotations.
6. Lock observation before interpretation.
7. Add negative/counterevidence as you encounter it.
8. Run `uv run fspp validate` and `uv run pytest` before commits.

## Do not begin with

- embeddings as the canonical corpus representation;
- LLM-generated annotation at scale;
- a web application;
- a graph database;
- raw-frequency comparative claims;
- migration of all prior projects.

Prove the manual pilot and shared infrastructure first.

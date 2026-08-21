# Codex Start Here

Open this repository in VS Code and give Codex this first instruction:

> Read `AGENTS.md`, `README.md`, `docs/architecture/FSPP_RESEARCH_WORKBENCH_PRINCIPLES.md`, `projects/sacrificial-debt/README.md`, `projects/sacrificial-debt/research/RESEARCH_AUTHORITY.md`, `projects/sacrificial-debt/codebook/CODEBOOK.md`, and `projects/sacrificial-debt/BACKLOG.md`. Then inspect the existing schemas and tests. Do not modify research semantics. Begin Milestone M1 by proposing a small implementation plan for source/provenance registration, normalization manifests, stable segmentation, and proposition creation. Every methodological rule that can be tested should receive a test. Preserve the shared/project boundary and manual-first workflow.

## Good first Codex task

Implement the **source registration + provenance checksum** workflow:

1. add generic provenance helpers under `src/fspp_workbench/`;
2. add `fspp source register` for project-local registration;
3. never invent missing archive/bibliographic metadata;
4. compute SHA-256 for a local source file;
5. write/append a canonical `Source` record only through a guarded writer;
6. add unit and integration tests;
7. update the relevant methodology/CLI documentation;
8. keep raw source redistribution opt-in.

Do not jump ahead to LLM extraction.

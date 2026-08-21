# ADR-0001: Modular Monorepo for Political Pathology DH Projects

**Status:** Accepted for scaffold  
**Date:** 2026-08-20

## Decision

Use one FSPP Research Workbench repository with shared Python infrastructure, project-local research/data modules, and one top-level Quarto website containing internal project subsites.

## Boundary

`src/fspp_workbench/` may not import `src/fspp_workbench/projects/*`. Project modules may import shared infrastructure.

## Consequences

- reusable provenance, ID, validation, audit, reliability, and publication code;
- the Workbench website is rendered from `publication/`, with project sections under `publication/projects/<project-id>/`;
- project releases must pin shared code/version;
- CI must include an import-boundary test;
- each project remains exportable as a reproducible research snapshot.

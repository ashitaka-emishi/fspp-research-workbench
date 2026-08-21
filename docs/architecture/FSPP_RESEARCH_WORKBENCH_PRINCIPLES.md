# FSPP Research Workbench Principles

Sacrificial Debt is the first project scaffolded against the **FSPP Research Workbench** architecture. The goal is not to reproduce an older repository layout; it is to preserve what worked and remove what created coupling, ambiguity, or maintenance burden.

## Lessons carried forward

### 1. Methodology should be executable

Lincoln demonstrated that methodological claims become stronger when they are represented in schemas, validators, tests, release gates, claim audits, and generated evidence chains—not merely described in prose.

**Workbench commitment:** every methodological rule that can be tested should eventually have a validator or acceptance test.

### 2. Stable source coordinates are infrastructure

Stable IDs and sentence/source coordinates are not project-specific conveniences; they are prerequisites for auditability.

**Workbench commitment:** shared ID, lineage, provenance, segmentation, and evidence-link infrastructure.

### 3. Reliability must preserve disagreement

Model review, human double coding, and adjudication are different epistemic layers. Consensus must not erase disagreement.

**Workbench commitment:** each layer gets its own immutable record type and lineage.

### 4. Evidence chains and claim audits are core, not publication cleanup

Earlier work showed the value of linking conclusions back to coded evidence and source provenance.

**Workbench commitment:** the repository is claim-centered from the beginning. Claim audit is built during research, not retrofitted before publication.

### 5. Corpus tiers prevent search results from becoming evidence by accident

Large retrieval corpora are useful but epistemically dangerous if their hits can flow directly into claims.

**Workbench commitment:** tier permissions are explicit and machine-checkable; promotion is a recorded scholarly act.

### 6. Generated artifacts must not become the evidence base

Derived files can drift from canonical research records.

**Workbench commitment:** canonical JSONL/manifests are inspectable; DuckDB, Parquet, dashboards, and site output are always rebuildable derivatives.

### 7. Semantic workflow names age better than numbered stages

Stage-number naming captures development history rather than research meaning and becomes hard to understand as projects mature.

**Workbench commitment:** modules are named `model_review`, `human_coding`, `adjudication`, `claim_audit`, etc. Release manifests capture sequencing.

### 8. Project theory must not leak into shared infrastructure

Reusing a metaphor-analysis codebase by copying fields would turn infrastructure into a hidden theoretical template.

**Workbench commitment:** shared code provides generic evidence primitives and extension points; Sacrificial Debt defines its own proposition and annotation ontology.

### 9. Negative evidence must be structurally easy to record

A theory-building workbench can otherwise become a confirmation engine.

**Workbench commitment:** negative evidence has its own canonical records, search-scope requirements for absence claims, and claim-audit links.

### 10. Publication should be a pinned research snapshot

**Workbench commitment:** every publication is traceable to Git commit, data hashes, schema/codebook versions, environment lock, and run manifests.

## New architectural commitments

- proposition-centered interpretation where a sentence is too coarse;
- explicit observation lock before theoretical interpretation;
- generic write guards for released canonical records;
- project export/release boundary so a monorepo does not reduce scholarly independence;
- model prompts/version metadata treated like software dependencies;
- acceptance tests for historical inference guardrails, not just syntax.

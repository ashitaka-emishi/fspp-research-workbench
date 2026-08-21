You are a senior software architect, research software engineer, digital-humanities systems designer, and computational social-science methodologist.

Your task is to produce a **detailed Technical and Research Design Specification** for a new digital-humanities project called:

# Sacrificial Debt Workbench

The Workbench supports the research program:

**Sacrificial Debt: How Unequal Suffering Turns Survival into Political Guilt**

## Inputs you must inspect before designing anything

I am providing two primary inputs:

1. **The latest Sacrificial Debt Research Program Prospectus**
   - Treat this as the authoritative source for:
     - research questions;
     - theory;
     - concepts;
     - hypotheses;
     - falsification criteria;
     - case-selection logic;
     - evidence requirements;
     - source families;
     - ethical and historiographical safeguards;
     - comparative method;
     - pilot design;
     - intended scholarly outputs.
   - Do not silently change the substantive research design.
   - Where the proposal leaves an engineering question unspecified, identify it explicitly and make a reasoned design recommendation.

2. **The `lincoln-metaphor-analysis` repository**
   - Inspect the repository itself, including its:
     - README;
     - directory structure;
     - corpus manifests;
     - schemas;
     - annotation protocols;
     - reliability procedures;
     - scripts;
     - tests;
     - evidence-chain logic;
     - claim-audit system;
     - reproducibility mechanisms;
     - publication workflow;
     - Quarto or web outputs;
     - human coding procedures;
     - AI/model-assisted procedures;
     - corpus-tier architecture.
   - Treat Lincoln as a **reference implementation and methodological precedent**, not as a template to clone blindly.
   - Identify which architectural patterns are reusable and which are metaphor-analysis-specific.

Do not infer Lincoln’s architecture from filenames alone. Inspect the actual files.

---

# Core objective

Design Sacrificial Debt as a **human-directed, AI-assisted, reproducible comparative digital-humanities research environment**.

The system must support this general research sequence:

**source acquisition  
→ provenance  
→ corpus registration  
→ normalization  
→ stable segmentation  
→ manual annotation  
→ structured theoretical interpretation  
→ negative-evidence capture  
→ reliability testing  
→ AI/model-assisted review  
→ adjudication  
→ evidence chains  
→ controlled analysis  
→ comparative process tracing  
→ claim audit  
→ publication**

The Workbench is not merely an eventual output of the research.

It is the **core research environment through which the scholarly outputs are produced**.

Articles, papers, datasets, visualizations, claim audits, and public-facing research products should emerge from the Workbench.

---

# Architectural preference

Prefer a reusable architecture in which Sacrificial Debt can operate as a project module inside a broader **FSPP Research Workbench**, rather than duplicating all infrastructure in a one-off repository.

Conceptually evaluate an architecture similar to:

```text
fspp-research-workbench/
├── shared/
│   ├── provenance/
│   ├── corpus/
│   ├── segmentation/
│   ├── annotation/
│   ├── reliability/
│   ├── model-review/
│   ├── human-adjudication/
│   ├── evidence-chains/
│   ├── claim-audit/
│   ├── analysis/
│   ├── publication/
│   └── validation/
│
└── projects/
    ├── lincoln-metaphor-analysis/
    └── sacrificial-debt/
```

Do not assume this is automatically correct.

Evaluate:

- monorepo versus standalone repository;
- shared library versus project-local infrastructure;
- portability;
- reproducibility;
- versioning;
- scholarly independence;
- maintenance burden.

State the recommended architecture and explain why.

---

# Fundamental methodological principle

One of the most important design principles is:

## Identification must be separated from interpretation.

The software and schemas should not allow the theory to manufacture its own evidence.

For Sacrificial Debt, distinguish at least:

### Layer A — Observable textual structure

Code relatively observable features such as:

- collective object;
- sacrificer;
- sacrifice type;
- alleged survivor or nonsacrificer;
- explicit comparison;
- moral valuation of sacrifice;
- moral valuation of survival;
- actor;
- audience;
- date;
- source type.

### Layer B — Sacrificial accounting

Code separately:

- sacrificial asymmetry;
- creditor;
- debtor;
- explicit reciprocal obligation;
- debt language;
- repayment language;
- equalization claim;
- emic versus etic debt.

### Layer C — Essentialization and dischargeability

Code separately:

- behavioral accusation;
- group-generalized accusation;
- racial/ontological accusation;
- essentialization status;
- dischargeable;
- contested;
- non-dischargeable;
- unclear.

### Layer D — Political consequence

Code:

- stigma;
- exclusion;
- extraction;
- forced contribution;
- forced labor;
- imprisonment;
- deportation;
- bodily coercion;
- lethal violence;
- exterminatory policy.

### Layer E — Causal role

Do not collapse rhetoric into causation.

Support distinct values such as:

- descriptive;
- classificatory;
- diagnostic;
- motivational;
- legitimating;
- escalatory;
- policy-causal;
- unclear.

### Layer F — Rival explanations

Allow multiple rival explanations to coexist with sacrificial-debt coding, including:

- racial antisemitism;
- ethnic prejudice;
- scapegoating;
- defeat/betrayal;
- security;
- anti-Bolshevism;
- conquest;
- material expropriation;
- institutional radicalization;
- bureaucratic competition;
- revenge;
- economic competition;
- other.

### Layer G — Negative and falsifying evidence

Negative evidence must be first-class structured data.

Examples:

- actual sacrifice successfully discharges accusation;
- veteran status protects an alleged debtor;
- contribution changes political classification;
- expected debt rhetoric is absent;
- coercion occurs without sacrificial accounting;
- comparable rhetoric exists without coercion;
- actors explicitly reject reciprocal-sacrifice reasoning;
- chronology contradicts the proposed mechanism.

Do not treat negative evidence as miscellaneous notes.

---

# Two-dimensional outcome model

Do not encode coercive severity and sacrificial meaning as a single ordinal variable.

Design two independent dimensions.

## Coercive severity

Possible conceptual range:

0. recognition only  
1. informal stigma  
2. formal exclusion  
3. extraction/dispossession  
4. detention/deportation/forced labor  
5. lethal persecution  
6. systematic extermination

## Sacrificial-debt framing

Possible conceptual range:

0. absent  
1. sacrifice praised  
2. asymmetry recognized or criticized  
3. reciprocal obligation asserted  
4. debtor identity generalized  
5. debt represented as non-dischargeable  
6. imposed suffering represented as restorative/equalizing

Determine whether these should be enums, scored variables, derived variables, or combinations of structured fields.

Do not force all evidence into an ordinal score if a more rigorous representation is preferable.

---

# Corpus architecture

Design a three-tier corpus system inspired by the Lincoln project.

## Tier 1 — Core interpretive corpus

Fully annotated, high-value evidence.

Only Tier 1 should support the strongest interpretive and causal claims.

Initial families include:

- Hitler;
- Goebbels;
- Himmler / SS;
- Judenzählung and wartime Germany;
- German Jewish veterans;
- Britain;
- Australia;
- France.

## Tier 2 — Validation corpus

Larger matched corpus used to test:

- recurrence;
- selection bias;
- robustness;
- negative findings;
- generality of patterns.

May use lighter annotation.

## Tier 3 — Search/reference corpus

Large searchable bodies used for:

- candidate discovery;
- lexical search;
- chronology;
- contextualization;
- negative searches;
- exploratory retrieval.

A Tier 3 search hit is a **lead, not coded evidence**.

Design explicit promotion rules from Tier 3 → Tier 2 → Tier 1.

---

# Source and provenance requirements

Every research object must have traceable provenance.

Design for:

- stable source IDs;
- archival citation;
- bibliographic citation;
- canonical URL if available;
- local file path;
- source repository/archive;
- edition;
- publication date;
- acquisition date;
- checksum;
- language;
- copyright / redistribution status;
- source reliability;
- provenance notes.

For multilingual materials also support:

- original-language text;
- published translation;
- researcher translation;
- translation source;
- translator;
- translation date;
- contested terms;
- lexical ambiguity;
- translation-risk flag.

High-value claims based on translated evidence should always preserve the original-language text.

---

# Stable segmentation

Design permanent identifiers for:

- source;
- document;
- page;
- paragraph;
- sentence;
- proposition;
- annotation;
- claim.

The proposition is the principal interpretive unit.

A proposition may occupy:

- part of a sentence;
- one sentence;
- multiple sentences.

It must nevertheless trace exactly to source coordinates.

Once an ID has entered an analysis or publication release, it must never be silently renumbered.

Define:

- ID formats;
- lifecycle rules;
- versioning;
- deprecation;
- supersession;
- split/merge handling.

---

# Evidence chains

Design a machine-readable evidence-chain model.

A typical chain should support:

**published scholarly claim  
→ analytical claim record  
→ mechanism component  
→ coded proposition(s)  
→ sentence/paragraph span  
→ document  
→ source metadata  
→ archival/bibliographic provenance**

Comparative claims must support evidence drawn from multiple cases.

Every claim should also be capable of linking to:

- supporting evidence;
- contradictory evidence;
- qualifying evidence;
- rival explanations;
- source-quality assessments.

Design the schema and workflow needed to make this auditable.

---

# Claim audit

Design a formal claim-audit system modeled on the strongest features of Lincoln.

A claim record should be able to answer:

- What exactly is being claimed?
- Is the claim descriptive, interpretive, comparative, or causal?
- What evidence supports it?
- What evidence contradicts it?
- Which cases support it?
- Which cases challenge it?
- What mechanism component does it invoke?
- What rival explanations remain?
- What is the evidence strength?
- Has it passed human review?
- Has it passed model stress testing?
- What publication uses it?
- Has the claim changed between releases?

Design both:

1. the underlying data structure; and
2. the researcher-facing workflow.

---

# Reliability architecture

Design a layered reliability system.

It should distinguish:

### Reference annotation

Primary project coding.

### AI-assisted second pass

A model checks for:

- missed instances;
- inconsistent coding;
- suspicious classifications;
- possible counterevidence;
- alternative readings.

### Multi-model stress testing

Use multiple models independently where appropriate.

Model agreement is not truth.

Model disagreement should become review evidence.

### Blind human double coding

Independent coders should classify selected Tier 1 samples without seeing one another’s decisions.

### Adjudication

Disagreements should create:

- adjudication records;
- reasons;
- codebook revisions where warranted.

Do not collapse reliability into one universal agreement score.

Report agreement separately for fields such as:

- sacrifice present;
- explicit comparison;
- debtor identification;
- reciprocal obligation;
- essentialization;
- dischargeability;
- sanction;
- causal role;
- rival explanation.

Specify which reliability metrics are appropriate for nominal, ordinal, and multilabel fields.

---

# Manual-first rule

The proposal explicitly requires:

**manual interpretation before large-scale automation.**

The system must enforce a staged workflow:

1. manual pilot;
2. codebook stabilization;
3. reliability testing;
4. limited computational retrieval;
5. validation against human-coded data;
6. expanded computational analysis.

Do not design an LLM-first or NLP-first extraction system that silently creates the research categories.

Automation should assist:

- retrieval;
- candidate generation;
- prioritization;
- quality checking;
- temporal analysis;
- co-occurrence analysis;
- actor comparison;
- robustness analysis.

It must not replace source criticism or interpretive judgment.

---

# Comparative design requirements

The initial cases have different methodological functions.

The system should preserve those roles explicitly.

### Germany
Mechanism-discovery and intensive process-tracing case.

### Australia
Strong explicit equality-of-sacrifice comparison.

### Britain
Test of individualized stigma and social coercion.

### France
Test of republican burden sharing / “blood tax” without equivalent racialized escalation.

The data model must permit:

- within-case analysis;
- cross-case comparison;
- period matching;
- source-type matching;
- actor-type matching;
- register matching;
- sampling transparency.

Avoid misleading raw-frequency comparisons between highly unequal corpora.

---

# Controlled analytical outputs

Design an analysis layer capable of controlling or stratifying by:

- country;
- period;
- actor;
- institution;
- source family;
- source type;
- public/private register;
- propaganda/administrative/private discourse;
- audience;
- corpus tier;
- source reliability;
- language;
- original/translation;
- sacrifice type;
- debtor group;
- essentialization status;
- dischargeability;
- sanction;
- causal role;
- rival explanation.

Specify which outputs should be:

- descriptive tables;
- concordances;
- timelines;
- transition matrices;
- co-occurrence networks;
- actor comparisons;
- diachronic plots;
- case-comparison matrices;
- evidence dashboards;
- negative-evidence reports.

Do not prioritize flashy visualization over historical interpretability.

---

# Reception and implementation must remain separate

Design separate evidentiary domains for:

### rhetoric / ideological production

What political actors, propagandists, institutions, or writers said.

### reception

What audiences, soldiers, veterans, citizens, or targeted communities appear to have believed or repeated.

### policy / implementation

What institutions actually did.

A speech cannot by itself establish audience reception.

Propaganda cannot by itself establish policy causation.

Policy occurrence cannot by itself establish sacrificial motivation.

The architecture must prevent these evidentiary domains from being silently conflated.

---

# Reproducibility

Design for strong computational and scholarly reproducibility.

Specify:

- repository layout;
- environment management;
- dependency locking;
- data manifests;
- checksums;
- schema validation;
- run manifests;
- random seeds;
- generated-versus-source data separation;
- CI/CD;
- unit tests;
- integration tests;
- fixture data;
- release tags;
- dataset versions;
- model versions;
- prompt versions;
- annotation-schema versions;
- codebook versions;
- publication snapshots.

A future scholar should be able to determine exactly which data, codebook, scripts, model outputs, and claim records produced a published table or conclusion.

---

# Sensitive historical material

The project includes Holocaust and genocidal material.

Translate the proposal’s ethical and historiographical safeguards into system requirements.

The design should explicitly prevent or discourage:

- treating victims as voluntary sacrificial participants;
- conflating combat death with genocide;
- presenting perpetrator rhetoric as valid moral justification;
- treating sacrificial debt as a total explanation of the Holocaust;
- stripping quotations of provenance or context;
- ignoring Jewish/victim/survivor sources;
- obscuring speculative inference;
- confusing actor statements with researcher conclusions.

Determine which of these belong in:

- documentation;
- schema fields;
- validation checks;
- review workflows;
- publication warnings.

---

# Technology choices

Recommend a practical stack.

Evaluate, rather than assume:

- Python;
- R where analytically useful;
- JSONL;
- CSV/TSV;
- Parquet;
- SQLite or DuckDB;
- relational versus document-oriented storage;
- Pydantic / JSON Schema;
- Quarto;
- Jupyter;
- static site generation;
- Git/GitHub;
- Git LFS or external data storage;
- pytest;
- CI;
- visualization libraries;
- graph representations if justified.

Favor:

- transparency;
- inspectability;
- long-term maintainability;
- portable open formats;
- low infrastructure burden;
- reproducibility.

Avoid unnecessary enterprise infrastructure.

This is a scholarly research platform, not a high-throughput commercial SaaS system.

---

# Required design document

Produce a professional design specification with at least these sections:

1. Executive Summary
2. Research and System Goals
3. Non-Goals
4. Research Requirements Derived from the Prospectus
5. Lessons and Reusable Patterns from Lincoln Metaphor Analysis
6. Proposed System Architecture
7. Repository Strategy
8. Directory Structure
9. Data Architecture
10. Entity-Relationship Model
11. Stable Identifier Scheme
12. Corpus-Tier Model
13. Source Acquisition and Provenance
14. Text Normalization and Segmentation
15. Translation and Textual-Variant Handling
16. Annotation Architecture
17. Detailed Annotation Schemas
18. Controlled Vocabularies and Enums
19. Annotation State Machine
20. Manual Coding Workflow
21. AI-Assisted Review Workflow
22. Multi-Model Stress Testing
23. Human Double-Coding Protocol
24. Adjudication Workflow
25. Negative-Evidence Model
26. Rival-Explanation Model
27. Evidence-Strength Model
28. Evidence Chains
29. Claim-Audit System
30. Comparative Analysis Architecture
31. Process-Tracing Support
32. Controlled Outputs
33. Concordance and Search
34. Computational Retrieval Layer
35. NLP/LLM Expansion Strategy
36. Validation and Reliability
37. Testing Strategy
38. Reproducibility Strategy
39. Publication and Quarto/Web Architecture
40. Ethics and Historiographical Safeguards
41. Data Governance and Copyright
42. Security and Sensitive-Content Considerations
43. Logging and Auditability
44. Versioning and Release Strategy
45. MVP Definition
46. Phase 1 Pilot Implementation
47. Expansion Roadmap
48. Risks and Mitigations
49. Open Design Questions
50. Acceptance Criteria

---

# Required diagrams and artifacts

Include:

- high-level architecture diagram;
- end-to-end pipeline diagram;
- corpus-tier diagram;
- annotation workflow/state diagram;
- evidence-chain diagram;
- claim-audit flow;
- entity-relationship diagram;
- proposed repository tree;
- sample source record;
- sample proposition record;
- sample annotation record;
- sample negative-evidence record;
- sample claim record;
- sample evidence-chain record;
- sample adjudication record;
- sample run manifest.

Use Mermaid where appropriate.

---

# Schema requirements

For all major data entities, provide concrete proposed fields, types, required/optional status, allowed values, and examples.

At minimum define schemas for:

- Source
- Document
- Segment
- Proposition
- Annotation
- Actor
- Group
- SacrificialRelation
- DebtRelation
- EssentializationAssessment
- DischargeabilityAssessment
- Sanction
- RivalExplanation
- NegativeEvidence
- Translation
- ReliabilityReview
- ModelReview
- HumanCodingRecord
- Adjudication
- EvidenceChain
- ResearchClaim
- Publication
- RunManifest

Do not merely list field names.

Explain relationships and normalization choices.

---

# MVP requirement

Define a realistic minimum viable Workbench corresponding to the proposal’s pilot.

The MVP should support:

- a small high-quality Tier 1 corpus;
- Germany plus initial comparative samples;
- stable proposition-level IDs;
- provenance;
- original-language and translation support;
- manual annotation;
- negative evidence;
- rival explanations;
- evidence-strength coding;
- limited reliability checking;
- claim-to-evidence linkage;
- basic controlled analysis;
- reproducible generated outputs;
- a small Quarto/static research site or equivalent.

Do not make the MVP dependent on large-scale LLM extraction or advanced NLP.

---

# Acceptance tests

Write explicit acceptance criteria.

Examples:

- Every coded proposition resolves to an exact source span.
- Every source has provenance and checksum information.
- Every strong sacrificial-debt annotation contains the minimum evidentiary components defined by the codebook.
- An annotation cannot claim “policy-causal” status without a documented evidentiary basis.
- Original-language evidence can be displayed alongside translations.
- Negative evidence is queryable independently of confirming evidence.
- A published claim can be traced automatically to all supporting and contradicting propositions.
- Corpus tier is visible in every analytical output.
- Generated tables can be reproduced from a versioned run manifest.
- AI annotations remain distinguishable from human annotations.
- Adjudicated records preserve all prior coder decisions.
- Updating a codebook does not silently rewrite historical annotations.
- Search/reference corpus hits cannot be accidentally treated as Tier 1 evidence.

Expand these into a formal testable acceptance matrix.

---

# Important design philosophy

Optimize for:

**auditability over convenience  
interpretability over automation  
stable evidence over clever extraction  
explicit uncertainty over false precision  
reproducibility over one-off analysis  
human judgment over black-box inference  
falsifiability over confirmation  
scholarly provenance over data volume**

The design should make it easier to discover that the Sacrificial Debt theory is wrong, incomplete, or limited than to accidentally confirm it.

---

# Do not do the following

Do not:

- write the historical paper;
- attempt to prove the Sacrificial Debt theory;
- redesign the substantive theory without flagging the change;
- treat Lincoln’s metaphor schema as directly transferable;
- make LLM extraction the primary annotation method;
- produce a vague “recommended tech stack” without schemas and workflows;
- treat raw frequency as historical explanation;
- collapse rhetoric, reception, and policy;
- collapse sacrificial framing and coercive severity;
- collapse model agreement and human reliability;
- treat all corpus tiers as equivalent evidence;
- create a complicated microservice architecture without a demonstrated research need;
- leave critical design choices hidden or implicit.

---

# Handling ambiguity

When the research proposal does not answer a technical question:

1. identify the ambiguity;
2. state the competing design options;
3. recommend one;
4. explain the research-methodological consequences;
5. mark it as an open decision if human input is genuinely required.

Do not invent substantive historical facts in order to resolve software-design questions.

---

# Final output standard

The final document should be detailed enough that:

- a research software engineer could begin implementation;
- a historian could understand how evidence is represented;
- a digital-humanities reviewer could assess methodological rigor;
- a graduate supervisor could see how the system protects valid inference;
- a future researcher could reproduce the analytical pipeline;
- another Political Pathology project could reuse the shared infrastructure.

Treat this as a **serious scholarly research-system design**, not a generic application architecture exercise.

At the end, include:

1. **Recommended architecture decision**
2. **MVP build order**
3. **Top 10 design risks**
4. **Top 10 unresolved research-engineering questions**
5. **Implementation backlog grouped by milestone**
6. **Traceability matrix showing which requirements come from the Sacrificial Debt proposal and which reusable patterns come from Lincoln**
7. **A final readiness judgment: what can be implemented immediately and what requires researcher decisions first**
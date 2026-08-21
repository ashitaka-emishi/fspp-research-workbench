# Migrating Existing Research Projects into FSPP Research Workbench

Do **not** rewrite Lincoln or Sacrifice Law immediately. First stabilize shared infrastructure using Sacrificial Debt.

Recommended migration sequence:

1. extract generic stable-ID/provenance helpers;
2. add adapters that read existing project records without changing them;
3. reproduce existing evidence-chain/claim-audit outputs through shared code;
4. prove byte/semantic equivalence where appropriate;
5. migrate generated-output workflows;
6. migrate reliability/adjudication primitives;
7. only then consider project-local schema modernization.

Existing published IDs remain authoritative. Migration must use mapping/lineage records, never renumber legacy evidence.
